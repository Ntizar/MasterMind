# DOCX Report v2.0 — Arquitectura de Nuevas Secciones

**Fecha:** 2026-06-22  
**Archivo principal:** `js/docx-report.js`

## Resumen de cambios v2.0

Se pasaron de 10 a 14 secciones en el informe DOCX, con 4 nuevas secciones y mejoras de diseño.

## Nuevas secciones

### Sección 8: Ranking de CPs por Accesibilidad

Calcula un score compuesto para cada CP dentro de la isócrona:

```
score = (distancia × 0.35) + (coste × 0.25) + (vivienda × 0.25) + (salario × 0.15)
```

- `distScore`: inversamente proporcional a la distancia (0-1)
- `costeScore`: inversamente proporcional al % del salario en transporte
- `viviendaScore`: inversamente proporcional al €/m² de alquiler
- `salarioScore`: proporcional al salario medio del CP

**Función:** `DEMO.calcularRankingAccesibilidad(cps, resultados, tiempoRef, salarioRef)`  
**Condicional:** Solo si hay CPs con datos demográficos  
**Formato:** Tabla con Top 10 CPs ordenados por score

### Sección 9: Alertas de Oportunidad

Identifica CPs con buena relación coste+vivienda vs salario:

- 🌟 Excelente: vivienda + transporte < 30% del salario
- 🏠 Vivienda asequible: alquiler < 10 €/m²
- 🚌 Transporte barato: transporte < 15% del salario
- 💰 Salario alto: > 35.000 €/año

**Función:** `DEMO.calcularAlertasOportunidad(cps, salarioRef)`  
**Condicional:** Solo si hay CPs con `precio_alquiler_m2` y `salario_medio`  
**Formato:** Lista de CPs con sus alertas, ordenados por totalPct (menor = mejor)

### Sección 11: Comparativa Multi-Ciudad

Compara accesibilidad entre múltiples ciudades cuando se han cargado múltiples GTFS:

- Score de accesibilidad por ciudad
- Mejor modo por ciudad
- Total paradas y rutas GTFS
- Área accesible a 60 min

**Función:** `DEMO.calcularComparativaMultiCiudad(ciudades)`  
**Condicional:** Solo si `ciudades.length >= 2`  
**Formato:** Tabla comparativa + ranking

## Mejoras de diseño

### Colores institucionales

Consistentemente en todo el documento:
- Azul principal: `#2563eb` (cabeceras, títulos sección)
- Naranja: `#f97316` (subtítulos, acentos)
- Filas alternadas: `#f1f5f9`
- Texto: `#1e293b` (oscuro), `#64748b` (gris)

### Tablas mejoradas

- Cabecera con fondo azul sólido y texto blanco
- Filas pares con fondo `#f1f5f9` sutil
- Bordes delgados (1px)
- Alineación centrada para valores, izquierda para texto

### Portada mejorada

- Logo placeholder (área para imagen institucional)
- Fecha completa con hora
- Modos seleccionados con iconos
- Rangos temporales
- Barra decorativa azul + naranja

## Flujo de datos

```
main.js::handleCalcular()
  → DEMO.buscarCPsEnPoligono(coords) → cps[]
  → DEMO.calcularRankingAccesibilidad(cps, resultados) → ranking[]
  → DEMO.calcularAlertasOportunidad(cps) → alertas[]
  → generarDOCX(resultados, punto, modos, tiempos, gtfsData, transporte, {cpsEnZona, rankingAccesibilidad, alertasOportunidad})

docx-report.js::generarDOCX()
  → desestructura extras = {cpsEnZona, rankingAccesibilidad, alertasOportunidad}
  → secciones condicionales según disponibilidad de datos
```

## Integración main.js

El estado de `main.js` se enriquece con:
```javascript
state.cpsEnZona = cps;
state.rankingAccesibilidad = DEMO.calcularRankingAccesibilidad(cps, resultados, tiempoMax);
state.alertasOportunidad = DEMO.calcularAlertasOportunidad(cps);
```

Y se pasa al DOCX:
```javascript
await generarDOCX(
  state.resultados, state.punto, modos, state.tiempos,
  gtfsData, state.transporteCercano,
  { cpsEnZona: state.cpsEnZona, rankingAccesibilidad: state.rankingAccesibilidad, alertasOportunidad: state.alertasOportunidad }
);
```
