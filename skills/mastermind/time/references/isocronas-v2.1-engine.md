# Isocronas Simuladas v2.1 — Motor de Fallback

## Componentes
1. **72 puntos base** (5° spacing) con ruido multicapa 8 capas
2. **Corredores viales** Overpass API (motorway/trunk/primary/secondary)
3. **Elevación** SRTM API + fallback por zona geográfica
4. **Suavizado Gaussiano** kernel σ=1.5, ventana ±3

## Overpass Query
```
way["highway"~"motorway|trunk|primary|secondary"](bbBox)
```
Peso: motorway=0.25, trunk=0.22, primary=0.16, secondary=0.08

## Elevación
- API: `https://api.srtm.gl.itch.io/v1.0/get_elevation?lat=${lat}&lon=${lng}`
- Penalización: BIKE 5%, WALK 3% por cada 10m desnivel
- Fallback: Norte base 300m, Centro 600m, Sur 200m

## GTFS Wait Times
- METRO_WAIT_TIME: 150s (2.5 min)
- BUS_WAIT_TIME: 240s (4 min)
