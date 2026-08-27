---
name: esios-indicators-correct
description: "IDs correctos y unidades de indicadores ESIOS/REE — ACTUALIZADO 2026-05-29: ya no usar time_trunc=hour ni dividir entre 10. Nueva resolución 5min."
version: 2.1.0
author: Ntizar
tags: [esios, indicadores, unidades, IDs]

---

# Indicadores ESIOS Correctos — ACTUALIZADO 2026-05-29

## 🔥 CAMBIO RADICAL: Sin time_trunc=hour, sin /10, datos cada 5 min

Se ha eliminado `time_trunc=hour` del cliente ESIOS. Con los datos **sin truncar**, los valores ya vienen en **unidades reales** (MW, €/MWh, tCO₂/h) **cada 5 minutos** (288 slots/día).

**Los antiguos DIV10_IDS ya no existen.** Todos los IDs de telemedida, demanda, CO2, interconexiones etc. son ahora DIRECTOS.

**NUEVO 2026-05-29:** Añadido **Pool OMIE (ID 600) — Precio mercado SPOT Diario** al dashboard. Se usa junto a PVPC (1001) para comparativa pool vs PVPC, mostrando los componentes adicionales que separan ambos precios.

## 📊 Resolución de 5 minutos (NUEVO)

La API devuelve ahora 12 valores por hora (cada 5 minutos). El dashboard expone dos endpoints:

- **`/api/esios/summary`** — Promedia los 12 valores de 5 min en 24 slots horarios (compatibilidad)
- **`/api/esios/summary-5min`** — Devuelve los 288 valores de 5 min sin colapsar (NUEVO)

Cada valor de 5 min en la API ESIOS viene con su datetime exacto (ej. `2026-05-27T21:05:00.000+02:00`), y `get5MinuteValues()` en `madrid.js` los mapea a slots `"HH:MM"` como `"21:05"`, `"21:10"`, etc.

## Indicadores que SÍ funcionan

### Precios y demanda — DIRECTOS (sin dividir)

| ID | Nombre | Unidad | Raw → MW |
|---|---|---|---|
| 1001 | PVPC 2.0TD | €/MWh | directo |
| 600 | Precio mercado SPOT Diario (Pool OMIE) | €/MWh | directo |
| 1293 | Demanda real | MW | directo |
| 2052 | Demanda prevista nacional | MW | directo |
| 602 | Energía asignada Mercado SPOT Diario España | MWh | directo |
| 579 | Precio TNP Balear sin enlace SEPE | €/MWh | directo |

### Generación por tipo — Telemedida Nacional (IDs 2038-2067) — DIRECTOS

Estos IDs devuelven valores en **MW reales** cada 5 minutos.

| ID | Nombre | REE 21:00 27/05 | API raw | 
|---|---|---|---|
| 2039 | Nuclear nacional | 5,040 MW | 5,040 ✅ |
| 2041 | Ciclo combinado nacional | 10,243 MW | ~11,228 MW |
| 2040 | Carbón nacional | 165 MW | 166 MW ✅ |
| 2038 | Eólica nacional | 4,668 MW | 4,782 MW |
| 2044 | Solar FV nacional | 2,283 MW | 2,308 MW ✅ |
| 2067 | Hidráulica nacional | ~3 MW | 6,425 MW (incluye bombeo) |
| 2051 | Cogeneración y residuos | 1,581 MW | — |

### Agregados de generación — DIRECTOS

| ID | Nombre | Unidad |
|---|---|---|
| 10351 | Gen real renovable | MW directo |
| 10352 | Gen real no renovable | MW directo |
| 10206 | Gen real Solar | MW directo |
| 10006 | Gen libre CO2 | MW directo |

### CO2 e interconexiones — DIRECTOS

| ID | Nombre | Unidad |
|---|---|---|
| 10355 | CO2 asociado gen T.Real | tCO₂/h directo |
| 10033 | % generación libre de CO2 | % directo |
| 10207 | Saldo neto interconexión Francia | MW directo |
| 10208 | Saldo neto interconexión Portugal | MW directo |
| 10209 | Saldo neto interconexión Marruecos | MW directo |

### Previsión — DIRECTOS

| ID | Nombre | Unidad |
|---|---|---|
| 1777 | Previsión D+1 eólica | MW directo |
| 1779 | Previsión D+1 fotovoltaica | MW directo |
| 10358 | Previsión D+1 renovable | MW directo |

## Reglas de conversión (ACTUALIZADAS 2026-05-29)

| Magnitud | Conversión |
|---|---|
| Telemedida nacional (2038-2067) | **DIRECTO** (MW) — ya no /10 |
| Demanda (1293), previsión (2052) | **DIRECTO** (MW) |
| Gen real agregados (10351, 10352, 10206, 10006) | **DIRECTO** (MW) |
| Potencia disponible (10232), Batería (2198, 2199) | **DIRECTO** (MW) |
| Interconexiones (10207-10209) | **DIRECTO** (MW) |
| Precios PVPC (1001) | **DIRECTO** (€/MWh) |
| **Precio Pool OMIE (600)** | **DIRECTO** (€/MWh) — precio marginal mercado diario |
| CO2 (10355, 10356) | **DIRECTO** (tCO₂/MWh) |
| PBF programados (IDs 1-462, 623) | /1000 (MWh/periodo → MW) |
| **NO usar time_trunc=hour** | Los datos ya vienen cada 5 min en MW |

## ⚠️ CRON JOB esios-telegram.js — Corrección de unidades (2026-05-30)

El script `/root/workspace/Mastermind/scripts/esios-telegram.js` tenía un bug crítico:
- `DIV10_IDS` contenía IDs que son DIRECTOS (10206, 1293, 2052, 10351, 10352, 10006, 10232, 2198, 2199)
- Esto hacía que demanda, solar, generación se mostraran **10× demasiado altos**
- Ejemplo: demanda de 31,300 MW → se mostraba como 313,000 MW ("313k MW")
- **Solución aplicada**: Eliminar `DIV10_IDS`, mover todos esos IDs a `DIRECT_IDS`
- **Adicional**: Quitar `time_trunc=hour` del fetch, implementar agrupación por hora con promedio de los 12 valores de 5 min
- **Verificación**: El script ahora produce valores consistentes con el dashboard esios-dashboard

## 🔥 Lo que CAMBIÓ

**ANTES (erróneo):**
- `time_trunc=hour` sumaba 12 valores → ej. nuclear 60,502
- DIV10_IDS dividía /10 → nuclear 6,050 ❌ (REE decía 5,040)

**AHORA (correcto):**
- Sin `time_trunc` → datos cada 5 min → nuclear 5,040 MW ✅
- DIRECT_IDS abarca TODOS los IDs → sin división
- Solo IDs PBF (1-462) necesitan /1000
- Nuevo endpoint `/api/esios/summary-5min` con 288 slots/día

## 📎 Archivos de referencia

- `references/verificacion-unidades.md` — Procedimiento completo para detectar unidades incorrectas, incluyendo señales de alerta (10×, 1000×) y pasos de verificación