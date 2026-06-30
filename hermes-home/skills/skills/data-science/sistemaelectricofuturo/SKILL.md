---
name: sistemaelectricofuturo
version: "1.0.0"
title: Sistema Eléctrico Futuro
description: Simulador horario del sistema eléctrico español 2026-2035 — despacho por orden de mérito SRMC, políticas energéticas (CfD, tope ibérico, cierre nuclear ENRESA), Monte Carlo multi-semilla y KPIs de seguridad de suministro (ENS, LOLE).
tags: [electricity, energy, simulation, spain, esios, ree, merit-order, srmc, monte-carlo]
added: 2026-05-29
---

# Sistema Eléctrico Futuro

> Simulador horario anual y trayectoria multianual del sistema eléctrico español peninsular.
> Proyecto: `Ntizar/SistemaElectricoFuturo` — <https://ntizar.github.io/SistemaElectricoFuturo/>
> Lengua: **castellano obligatorio** — todo el código, mensajes, documentación y commits en español.

## Arquitectura

JavaScript sin transpilación (IIFE modules), cargados por script tags en orden de dependencia. Sin package.json ni bundler. Vue 3 + Plotly vía CDN.

**Orden de carga en index.html:**
constants.js → theme.js → nuclear.js → weather.js → demand.js → storage.js → policy.js → scenarios.js → simulator.js → montecarlo.js → trajectory.js → charts.js → ree-data.js → app.js

### Módulos clave

| Módulo | Responsabilidad |
|--------|----------------|
| constants.js | PRNG Mulberry32, Utils (clamp, lerp, sum, normalizeSeries, mesDelDia), PARAMS_DEFAULT, DATOS_2025, PNIEC_2030, MODEL, FC_HISTORICOS, COSTES_REF, COLORES |
| nuclear.js | Calendario ENRESA oficial (7 reactores), función disponibleEnAnio() con prórroga |
| weather.js | Series climáticas sintéticas horarias (solar, viento, nubosidad, hidraulicidad). Devuelve cfSolarMedio, cfEolicoMedio |
| demand.js | Perfiles de demanda por sector (residencial, servicios, industria, VE, bombas calor, H₂, autoconsumo) |
| storage.js | Baterías (Li-ion con degradación por ciclos) y bombeo (gestión estacional) |
| policy.js | Políticas: tope ibérico (hipotético, expirado), CfD de doble cara, pago por capacidad, peajes |
| scenarios.js | 22 escenarios predefinidos (0-21). Los 4 últimos (18-21) son **ceteris paribus** |
| simulator.js | **Motor principal**: clase SimuladorElectrico con simular(), calcularPrecioMarginal(), balance energético |
| montecarlo.js | Sistema Monte Carlo multi-semilla: simularMultiSemilla(), calcularPercentiles() |
| charts.js | Gráficos Plotly (mix horario, precios, trayectoria, mensual) |
| app.js | App Vue 3: estado reactivo, pestañas, cálculos, renderizado |

## Motor de simulación (núcleo)

### Despacho por orden de mérito SRMC

En simulator.js → calcularPrecioMarginal():

1. Se construye array ordenMerito con 12 tecnologías ordenadas por SRMC:
   - Nuclear (must-run, SRMC ≈ 10 €/MWh)
   - Solar, eólica, offshore (SRMC ≈ 0)
   - Hidráulica fluyente (SRMC ≈ 5)
   - Baterías (SRMC ≈ 30, +15 si >200 ciclos)
   - Bombeo (SRMC ≈ 35)
   - V2G (SRMC ≈ 40)
   - Hidráulica de embalse (SRMC ≈ 45 + (1-hidraulicidad)·20)
   - Importación (SRMC = precioImport)
   - CCGT (SRMC = precioGas/η + CO₂·0.37/η + O&M)
   - Flexibilidad descendente (SRMC = precioEscasez)
2. **Precio marginal** = coste SRMC de la última tecnología con generación > 0.01 GW
3. Si déficit > 0.3 GW, precio escala hasta VoLL (~3000 €/MWh)
4. Prima por estrés de inercia (+25) y reserva (+18)
5. Precios negativos cuando renovable + must-run > demanda (ratio > 1.20)
6. Clamp final: [-50, 3000] €/MWh

### Ciclo horario (8760 horas/año)

Cada hora h:
1. Calcular generación renovable base (nuclear + solar + eólica + offshore)
2. Si excedente > 0: cargar baterías → bombear → H₂ flexible → exportar → **verter**
3. Si déficit > 0: hidro fluyente → hidro embalse (con presupuesto) → baterías descarga → bombeo → V2G → flex down → importar → **CCGT** → déficit
4. Calcular precio marginal, primas, políticas
5. Acumular KPIs (gas, emisiones, vertidos, déficit, ENS, inercia)

### Calibración renovable

Series climáticas normalizadas para que CF anual coincida con valores reales REE 2025:
- Solar: 24% (52.5 TWh / 24.7 GW / 8760h)
- Eólica terrestre: 20% (55.6 / 31.6 / 8760h)
- Offshore: 43%

Fórmula: gen.solar = p.solar × weather.solar[h] × (CF_SOLAR_REAL / cfSolarMedio)

### Hidráulica

Separada en fluyente (~38%, SRMC≈5, sin límite anual) y embalse (~62%, presupuesto anual ~37.6 TWh × hidraulicidad × 0.62, capacidad máx ~8 TWh).

### PRNG

**Mulberry32** (determinista, 32 bits, uniforme). Sustituye a Math.sin. Misma semilla = misma climatología.

### Políticas

- **Tope ibérico**: hipotético tipo RDL 10/2022 (expirado dic 2024)
- **CfD renovables**: de doble cara (productor devuelve si spot > strike)
- **Pago por capacidad**: se suma a facturación sin afectar spot

## Escenarios ceteris paribus (IDs 18-21)

Solo varían política nuclear; todo lo demás idéntico:

| ID | Nombre | Política nuclear |
|----|--------|-----------------|
| 18 | Cierre ENRESA oficial | aplicarPlanNuclear:true, prorrogaNuclear:false |
| 19 | Prórroga 10 años | prorrogaNuclear:true, prorrogaGlobal:10 |
| 20 | Prórroga 20 años (60 años vida) | prorrogaNuclear:true, prorrogaGlobal:20 |
| 21 | Cierre acelerado 2030 | aplicarPlanNuclear:true, cierreNuclear:2030 |

## Monte Carlo

SEF.MonteCarlo.simularMultiSemilla(params, semillas) — semillas por defecto [1,42,100,500,1000,2000,5000,7777,9999]. Devuelve resultados por semilla + percentiles P5/P50/P95.

## KPIs seguridad de suministro

- **ENS** (Energía No Suministrada): suma déficit horario → TWh
- **LOLE**: horasDeficit (h/año)
- **Pico déficit**: maxDeficit (GW)
- **Horas inercia crítica**: < mínimo síncrono

## Calendario ENRESA oficial

| Reactor | Código | Oficial |
|---------|:------:|:-------:|
| Almaraz I | 2027 | nov 2027 |
| Almaraz II | 2028 | oct 2028 |
| Ascó I | 2030 | oct 2030 |
| Cofrentes | 2030 | nov 2030 |
| Ascó II | 2032 | sep 2032 |
| Vandellós II | 2035 | feb 2035 |
| Trillo | 2035 | may 2035 |

Fuente: enresa.es

## Convenios

- TODO en castellano: código, commits, docs
- Sin transpilación: JavaScript IIFE plano
- PRNG determinista: Mulberry32, Math.sin prohibido como generador
- CF calibrados: usar constantes de constants.js, no asumir por nombre
- Calendario real: U.mesDelDia(dia), no bloques de 30.5 días
- Precio: clamp [-50, 3000] €/MWh
- CfD: siempre de doble cara
- Escenarios 18-21 deben mantener parámetros idénticos excepto nuclear

## Plan vivo (PLAN.md)

Este proyecto mantiene un **PLAN.md** en la raíz que sirve como documento de planificación vivo entre sesiones. Cuando trabajes en este proyecto:

1. **Actualiza PLAN.md** cada vez que completes una tarea o cambie el alcance
2. Marca tareas como ✅/⏳/❌ con fechas de versión
3. Incluye tabla resumen por fase y próximos pasos priorizados
4. Commitea PLAN.md junto con los cambios de código
5. El usuario confía en este documento para retomar en otra sesión sin pérdida de contexto

## Pestaña Información

Ver index.html + app.js:
- `INFO_LEYES` (en app.js): 10 leyes/RD del sector con enlaces a BOE
- `INFO_ORGANISMOS` (en app.js): 9 entidades reguladoras
- `INFO_GLOSARIO` (en app.js): 18 términos del sector eléctrico
- `SOURCES` (en app.js, ~16 enlaces): enlaces rápidos a fuentes oficiales
- Template en index.html v-show="tabActual === 'info'"

## Documentación metodológica

## Auditoría de Simulación Eléctrica

Patrón sistemático para auditar herramientas de modelado del sector eléctrico español. Combina revisión del núcleo de simulación, verificación de datos de referencia, calidad de la interfaz y alineamiento estratégico del producto.

### Metodología en 4 capas

**Capa 1 — Núcleo de simulación:** Verificar que el motor usa despacho por orden de mérito real (SRMC), no heurísticas con magic numbers. Verificar PRNG (Mulberry32, no Math.sin), balance energético verificable, calibración renovable con CF reales.

**Capa 2 — Calidad del dato:** Calendario nuclear ENRESA oficial, objetivos PNIEC 2030, factores de capacidad REE 2025. Incoherencias comunes: "datos en tiempo real" estáticos, clamps que contradicen parámetros.

**Capa 3 — Reproducibilidad:** PRNG determinista, test de calibración, constantes con fuente, ejecución headless, calendario real (no bloques 30.5 días).

**Capa 4 — Producto y foco:** Escenarios ceteris paribus, vista comparativa, diagnóstico automático, legislación con enlaces BOE, KPIs ENS/LOLE en primera línea.

### Ejecución post-auditoría

**Fase 0:** Correcciones inmediatas (datos erróneos, supuestos no documentados)
**Fase 1:** Tests de calibración ANTES de cambios estructurales (rangos ±30% del valor real)
**Fase 2:** Build system y CI (Vitest, ESLint, GitHub Actions)
**Fase 3:** Producto y documentación (nuevas vistas, CONSTANTS.md, METHODOLOGY.md)

### Pitfalls de auditoría
- ❌ No confundir interfaz bonita con motor correcto
- ❌ No asumir que 17 escenarios = producto completo
- ❌ No asumir que datos de referencia son correctos
- ❌ No recomendar reescribir de cero — la mayoría tienen base modular buena

## Documentación metodológica

- `docs/METHODOLOGY.md` en el repo: documento completo con 14 secciones que explican cada hipótesis del modelo (despacho SRMC, calibración renovable, hidráulica, Monte Carlo, fuentes oficiales)
- Cada sección incluye referencias a fuentes reales (REE, OMIE, BOE, ENTSO-E, ENRESA, IDAE)
- No depende del código: es legible de forma independiente

## Pitfalls

- NUNCA modificar constants.js sin verificar PARAMS_DEFAULT (shared state IIFE)
- NUNCA usar bloques de 30.5 días para meses
- NUNCA hardcodear CF de renovables; usar constantes de constants.js
- Siempre verificar node --check js/*.js tras cambios
- Siempre mantener escenarios 18-21 con mismos parámetros excepto nuclear
- Nuevos módulos: insertar script tag en orden correcto en index.html
- ⚠️ **Velocidad de ejecución:** El usuario quiere ejecución directa, no sobre-planificación. No uses delegate_task ni subagentes para trabajo de este proyecto — trabaja directamente sobre los archivos. NO sobre-planifiques ni delegues tareas que puedas hacer directamente; al usuario le frustra la espera. Haz los cambios directamente.
- **Añadir gráfico Sankey:** Patrón completo en `references/sankey-chart-pattern.md`. Requiere: (1) método `calcularFlujosSankey()` en simulator.js que usa `_ultimoMix` y `_ultimoDetalleDemanda`, (2) función `plotSankey()` en charts.js con Plotly sankey trace, (3) variable `sankeyData` en app.js calculada en `setResults()`, (4) sección HTML en tab "Análisis".
- **Añadir cualquier gráfico Plotly nuevo:** Patrón general: (1) función `plotNombre()` en charts.js con `plotOrReact()`, (2) variable de estado en app.js, (3) cálculo en `setResults()` o función dedicada, (4) renderizado en `renderizarGraficos()`, (5) canvas en HTML con id consistente, (6) usar colores de `SEF.COLORES` para consistencia visual.