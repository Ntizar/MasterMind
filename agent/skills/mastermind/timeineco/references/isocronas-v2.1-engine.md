# Isocronas Simuladas v2.1 — Referencia Técnica

## Resumen

Mejoras del motor de simulación de isocronas (TimeIneco2, 2026-06-22):
- Ruido multicapa 8 capas
- Elevación real SRTM + simulación geográfica
- Corredores viales Overpass API
- Suavizado Gaussiano con kernel real
- Tiempos de espera metro/bus configurables

## Ruido Multicapa (8 capas)

Frecuencias: 0.5, 1.0, 1.8, 2.5, 3.7, 5.0, 7.3, 11.0, 17.1
Amplitudes: 15%, 12%, 9%, 7%, 5%, 3.5%, 2.5%, 1.5%, 1%

Imita: macro-relieve → colinas → lomas → ondulaciones → micro-relieve → detalle fino → textura

## Corredores Viales (Overpass API)

**URL:** `https://overpass-api.de/api/interpreter`
**Query:** way["highway"~"motorway|trunk|primary|secondary"]
**Peso por tipo:**
- motorway: 0.25
- trunk: 0.22
- primary: 0.16
- secondary: 0.08 (default)

**Cache key:** `${lat.toFixed(4)},${lng.toFixed(4)},${Math.round(radioM)}`

**Fallback:** 12 calles sintéticas cada ~30° si Overpass falla.

## Elevación

**API real:** `https://api.srtm.gl.itch.io/v1.0/get_elevation?lat=${lat}&lon=${lng}`
**Fallback simulado:** 8 capas con parámetros por zona geográfica:
- Norte (>42° lat): base 300m, amplitud 80m (montañoso)
- Centro (39-42°): base 600m, amplitud 40m (meseta)
- Sur (<39°): base 200m, amplitud 60m (variado)

**Penalización:** CONFIG.ELEVATION_PENALTY_BIKE (5%) / WALK (3%) por cada 10m desnivel.

## Suavizado Gaussiano

- Kernel: exp(-d² / (2σ²)) con σ=1.5
- Ventana: ±3 índices alrededor del punto
- Salto: cada 3 puntos (72→24 vértices)
- Normalización: divide por suma de pesos

## GTFS Wait Times

- METRO_WAIT_TIME: 150s (2.5 min)
- BUS_WAIT_TIME: 240s (4 min)
- Se suman a tiempoViajePorParada en el BFS
