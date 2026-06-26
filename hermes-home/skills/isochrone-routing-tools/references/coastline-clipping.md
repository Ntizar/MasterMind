# Coastline Clipping con turf.js — Implementación completa

Recorte de isocronas a tierra firme usando Natural Earth coastline + turf.js.
Implementado en TimeIneco (js/clip.js, junio 2026).

## Estructura de clip.js

```
clip.js
├── loadCoastline()        → Carga lazy del GeoJSON (una vez)
├── clipToLand(coords, lat, lng) → Recorte principal
├── esZonaCostera(lat, lng)  → Detección por ciudades
├── createMinimalPolygon(lat, lng) → Fallback marítimo
└── getBBox(coords)        → BBox helper
```

## Integración (isochrones.js)

Se llama desde `calcularIsocronaAsync()` tanto para ORS real como para simulación:

```javascript
// En ambos caminos de retorno:
return await aplicarClipeo({ ...resultado, real: true/false }, lat, lng);
```

La función `aplicarClipeo()`:
1. Extrae `coordinates[0]` del Feature GeoJSON
2. Llama a `clipToLand(coords, lat, lng)`
3. Si hubo recorte, actualiza `geometry.coordinates` y recalcula `areaKm2`
4. Devuelve el resultado modificado

## Rendimiento

| Operación | Tiempo |
|-----------|--------|
| Carga coastline (lazy, una vez) | ~50ms (135KB) |
| Filtrado por bbox (turf.booleanIntersects) | ~2ms por feature |
| turf.intersect() | ~5ms por feature intersectante |
| turf.union() (si múltiples partes) | ~10ms |
| **Total por isócrona costera** | **~15-30ms** |

## Edge cases manejados

1. **Punto no costero** → no carga coastline, devuelve coords originales
2. **Coastline no disponible** (fetch error) → devuelve coords originales con console.warn
3. **Isócrona completamente en tierra** → intersect devuelve el polígono original
4. **Isócrona parcialmente en mar** → intersect recorta la parte marina
5. **Isócrona completamente en mar** → fallback a polígono mínimo (~50m radio)
6. **Resultado MultiPolygon** → selecciona el polígono más grande por área
7. **turf.union() falla** (geometrías complejas) → selecciona la parte más grande sin unir

## Cobertura de ciudades costeras

| Ciudad | lat | lng | radio (°) | radio (km) |
|--------|-----|-----|-----------|-----------|
| Gijón | 43.53 | -5.66 | 0.15 | ~16.7 |
| Barcelona | 41.38 | 2.18 | 0.15 | ~16.7 |
| Valencia | 39.47 | -0.38 | 0.15 | ~16.7 |
| Málaga | 36.72 | -4.42 | 0.15 | ~16.7 |
| Cádiz | 36.53 | -6.29 | 0.20 | ~22.2 |
| Palma | 39.57 | 2.65 | 0.20 | ~22.2 |

El radio de 0.15° (~16.7km) cubre isocronas de hasta 30min bici o 15min coche.
El radio de 0.20° (~22.2km) cubre hasta 60min bici o 30min coche.
Para ciudades con bahías/penínsulas (Cádiz, Palma), usar radio mayor.

## Próximas mejoras posibles

1. **Detección por Overpass API** en vez de lista fija de ciudades
2. **Spatial index** (RBush) para filtrar features más rápido
3. **Costline 50m** para zonas donde 110m sea demasiado grueso
4. **Cache persistente** del coastline en IndexedDB
