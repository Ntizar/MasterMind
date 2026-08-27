# Sistema de Previsión de Precio Eléctrico — ESIOS Dashboard

> Actualizado 2026-06-01 — Reescritura completa tras auditoría. 
> Versión anterior tenía 8 bugs críticos: ID map invertido, Open-Meteo 1x/día, TTF 1x/día, % tecnología mal calculado.

## Arquitectura

Sistema multi-variable que combina 3 fuentes de datos para predecir el precio de la electricidad (PVPC €/MWh):

```
ESIOS (precio, demanda, mix)
  ├─ 1001 → PVPC (€/MWh) — variable objetivo
  ├─ 1293 → Demanda real (MW)
  ├─ 1000 → Eólica (MW)
  ├─ 2038 → Hidráulica (MW)  ← ANTES: mapeado a gen_eolica (BUG!)
  ├─ 2039 → Solar FV (MW)     ← ANTES: mapeado a pct_nuclear (BUG!)
  ├─ 2040 → Carbón (MW)
  ├─ 2041 → Fuel+Gas (MW)
  ├─ 2044 → Nuclear (MW)      ← ANTES: mapeado a gen_solar (BUG!)
  ├─ 2067 → Ciclo combinado   ← ANTES: mapeado a gen_hidraulica (BUG!)

Open-Meteo Archive (1 llamada/rango, NO 1/día!)
  ├─ temperature_2m_mean → Temp media (°C)
  ├─ wind_speed_10m_mean → Viento (km/h)
  ├─ shortwave_radiation_sum → Radiación solar (W/m²)

Yahoo Finance (1 llamada, NO 1/día!)
  └─ TTF=F → Precio gas TTF (€/MWh) — último cierre disponible
```

## Endpoint

```
GET /api/esios/forecast?days=90
```

**Parámetros:**
- `days`: días históricos (default 90, max 365, min 10 válidos)

**Cache:** 6h en memoria. Cache key: `forecast:${days}`

**Mínimo:** 10 días con precio_medio válido. Si no, error con `datosDisponibles`.

## Algoritmo

### 1. Recolección (`collectAllData`)

**Optimización clave — 3 fuentes, NO 3N fuentes:**
- Open-Meteo: **1 llamada** para todo el rango vía `archive-api.open-meteo.com/v1/archive`
- Yahoo TTF: **1 llamada** para todo el rango, se reusa el último cierre
- ESIOS: batches de 5 días en paralelo, 9 indicadores por día

**Rendimiento:** 90 días → ~4-5s (antes timeout por ~900 llamadas)

### 2. Feature Engineering (`buildDayFeatures`)

Por cada día:

| Feature | Fuente | Cálculo | Qué mide |
|---------|--------|---------|----------|
| precio_medio | 1001 | media de valores 5min | Precio PVPC medio diario |
| precio_max | 1001 | max de valores | Pico de precio del día |
| precio_min | 1001 | min de valores | Valle de precio del día |
| demanda_media | 1293 | media de valores | Consumo eléctrico medio |
| pct_renovable | 1000+2038+2039 | / total_gen * 100 | % renovable en mix |
| pct_eolica | 1000 | / total_gen * 100 | % eólica |
| pct_solar | 2039 | / total_gen * 100 | % solar FV |
| pct_hidraulica | 2038 | / total_gen * 100 | % hidráulica |
| pct_nuclear | 2044 | / total_gen * 100 | % nuclear |
| pct_carbon | 2040 | / total_gen * 100 | % carbón |
| pct_gas | 2041 | / total_gen * 100 | % fuel+gas |
| pct_ciclo_combinado | 2067 | / total_gen * 100 | % ciclo combinado |
| temperatura_media | Open-Meteo | mean diaria | Temp media |
| viento_medio | Open-Meteo | mean diaria | Velocidad viento |
| radiacion_total | Open-Meteo | suma diaria | Radiación solar |
| ttf_cierre | Yahoo | último cierre | Precio gas TTF |

### 3. Correlación (`calcularCorrelaciones`)

Pearson: mide relación lineal entre cada feature y el precio.
- Mínimo 5 puntos por feature
- Clasificación: |r| > 0.8 muy fuerte, > 0.6 fuerte, > 0.4 moderada, > 0.2 débil

### 4. Sensibilidad (`analisisSensibilidad`)

Regresión lineal simple: `precio = a + b * feature`
- `b` = cuántos €/MWh varía el precio por unidad de cambio
- Ej: `b = -2.5` en viento → cada km/h extra reduce ~2.5 €/MWh

### 5. Escenarios (`generarEscenarios`)

P10 (optimista)  = media - 1.28σ + ajustes
P50 (base)       = media + ajustes
P90 (pesimista)  = media + 1.28σ + ajustes

**Ajustes:**
- Renovables: -0.5 €/MWh por cada punto % sobre media (merit order)
- TTF: +0.15 €/MWh por cada €/MWh sobre 30 (coste marginal gas)
- Temperatura: +0.3 €/MWh por cada °C sobre 20 (demanda extra)

## Frontend

`public/js/render-forecast.js` — cada sección explica:
- **Resumen:** metodología (Pearson, regresión, percentiles) y fuentes
- **Predictores:** top 5 features por |r| con tarjetas
- **Correlaciones:** matriz visual de TODAS las features
- **Sensibilidad:** impacto de cada factor con explicación en texto
- **Escenarios:** 3 tarjetas P10/P50/P90 con ajustes detallados
- **Gráfico:** precio, % renovable y temperatura en Chart.js

## Errores y Fallos Conocidos (CORREGIDOS 2026-06-01)

| Bug | Síntoma | Causa | Solución |
|-----|---------|-------|----------|
| ID map invertido | Correlaciones incoherentes | 2038→eólica, 2044→solar, etc | Usar `INDICATORS` object como fuente de verdad |
| % tecnología erróneo | Sumas que no cuadran | Suma bruta vs media/ total | `media_tecnología / total_gen * 100` |
| Open-Meteo lento | Timeout en >30 días | 1 llamada/día → N llamadas | 1 llamada/rango con archive API |
| TTF lento | Timeout en >30 días | 1 llamada/día → N llamadas | 1 llamada, reusar último cierre |
| Clima siempre null | Temperatura/viento = null | `fetchOpenMeteo(dateStr)` no existe | Usar `climaMap.get(dateStr)` del fetch por rango |

## Fallos actuales monitorizados

1. **Yahoo TTF caído:** Se omite la feature TTF. No bloquea el análisis.
2. **Open-Meteo sin datos históricos:** Para fechas recientes (< 2 días), usar forecast API en vez de archive.
3. **Pocos días válidos (< 10):** El endpoint devuelve error con `diasDisponibles`.

## Deploy

Forma parte del dashboard ESIOS. Al hacer push:
1. GitHub detecta cambios
2. Kaniko rebuild en NaN.builders
3. Nueva versión desplegada en ~3 min

Para redeploy forzado: `git commit --allow-empty -m "chore: trigger redeploy" && git push`