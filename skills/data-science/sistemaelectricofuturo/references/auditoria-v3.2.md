# Auditoría técnica — Sistema Eléctrico Futuro v3.1 → v3.2

> Fecha: mayo 2026
> Repositorio: Ntizar/SistemaElectricoFuturo

## Hallazgos corregidos (v3.2)

### 🔴 Críticos

| ID | Problema | Solución aplicada |
|----|---------|-------------------|
| S1 | "Orden de mérito" era heurística con números mágicos | Despacho real por SRMC con 12 tecnologías ordenadas por coste marginal |
| S2 | Renovables sin calibrar a CF reales; offshore = onshore×1.18 | Normalización a CF REE 2025: solar 24%, eólica 20%, offshore 43% con perfil propio |
| S3 | PRNG Math.sin defectuoso (no uniforme, correlaciones) | Mulberry32 (determinista, 32 bits, distribución uniforme) |
| D1 | Calendario ENRESA erróneo (Ascó II 2031→2032, Vandellós II 2032→2035) e inconsistente con UI | Corregido al protocolo oficial ENRESA 2019; sincronizado código y UI |

### 🟠 Altos

| ID | Problema | Solución |
|----|---------|----------|
| S4 | Hidráulica sin presupuesto energético (podía generar "infinita") | Separación fluyente (38%) + embalse (62%) con presupuesto TWh anual y capacidad máx almacenamiento |
| S5 | Demanda sectorial reescalada ≠ valores físicos | Una sola fuente de verdad: demanda = suma real de sectores |
| S6 | Meses en bloques de 30.5 días | Calendario real con DIAS_ACUM y función mesDelDia() |
| D2 | "Tiempo real" que era estático | Renombrado a "Referencia REE 2025 (estática)" |
| D3 | Tope ibérico arbitrario y caducado (números 65, +6, 0.72) | Documentado como "mecanismo hipotético tipo RDL 10/2022 (expirado dic 2024)" |
| D4 | CfD a una sola cara (sesgaba coste al alza siempre) | CfD de doble cara: productor devuelve si spot > strike |

### 🟡 Medios

| ID | Problema | Solución |
|----|---------|----------|
| D5 | clamp [-25,500] contradecía precioEscasez (hasta 600) | Clamp subido a [-50, 3000] (VOLL) |
| D6 | "Coste sistema" = facturación pool | Renombrado a "Facturación mayorista" |
| R1 | AR(1) declarado pero series sintéticas no calibradas | Texto actualizado: "generador climático sintético — no calibrado contra históricos" |
| R2 | Sin balance energético | Verificación anual al final de simular() (alerta si desviación > 0.5 TWh) |
| R3 | Magic numbers sin fuente | Documentados en docs/METHODOLOGY.md (enlace, fuente oficial) |

## Fase 3 — Añadido (v3.2)

- **Escenarios ceteris paribus** (IDs 18-21): 4 escenarios que solo varían política nuclear, con parámetros idénticos
- **Monte Carlo multi-semilla**: 9 semillas climáticas, percentiles P5/P50/P95 para 8 KPIs
- **KPIs seguridad suministro**: ENS (TWh) y LOLE (h/año) como tarjetas principales del dashboard

## Fase 4 — Añadido (v3.2)

- **docs/METHODOLOGY.md**: documentación completa con fuentes oficiales
- **Pestaña Información**: guía técnica + fuentes oficiales con enlaces (REE, OMIE, CNMC, MITECO, ENTSO-E, EU ETS)
- **API ESIOS**: pendiente de integrar (opción A del D2)

## Pendiente

- Paradas de recarga nuclear (S7): modelar paradas escalonadas por reactor (~30 días cada 18 meses)
- Vista comparativa "cierre vs prórroga" lado a lado en UI
- Vite + Vitest + GitHub Actions (tests de calibración contra REE 2025)
- package.json con versionado de dependencias
- API ESIOS real con fetch (opción A del D2)