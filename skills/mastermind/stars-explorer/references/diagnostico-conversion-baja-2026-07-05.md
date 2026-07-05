# Diagnóstico: Tasa de Conversión Baja (2026-07-05)

## Contexto

El usuario (David) notó que el sistema no estaba creciendo en skills a pesar de tener muchas stars de GitHub interesantes. Pregunta directa: *"Realmente eres más potente que hace dos meses o sigues igual?"*

## Estado del registry antes del fix

| Métrica | Valor |
|---------|-------|
| Runs totales | 11 |
| Repos explorados | 132 |
| Skills generados | 9 |
| **Tasa de conversión** | **8.5%** |
| Repos en "pending" | 108 |
| Repos con skill creado | 11 |

## Distribución por categoría

```
pending: 108  ← PROBLEMA: 83% de repos sin procesar
skip: 8
domain: 6
pattern: 4
reference: 2
core: 1
```

## Causas raíz

1. **Batch demasiado pequeño:** 3 repos por run = 3 por noche. A 132 repos explorados en 11 runs, solo procesaba ~12 repos por noche de fetch, pero el agent solo creaba skills de ~1 de cada 12.
2. **Criterios demasiado conservadores:** El skill exigía ">1000 stars" y "3+ patterns detectados" para crear skill. Muchos repos de mapas/3D con 500-4000 stars quedaban excluidos.
3. **Repos de mapas/3D/visualización sin procesar:** 19 repos relacionados con mapas/3D/three.js estaban en "pending", incluyendo:
   - nagix/mini-tokyo-3d (⭐4.1K) — mapa 3D de tránsito de Tokyo
   - maptalks/maptalks.three (⭐646) — three.js layer para maptalks
   - tentone/geo-three (⭐938) — mapas 3D tile-based en three.js
   - blaze33/map33.js (⭐500) — mapas 3D con three.js
   - opengeos/GeoLibre (⭐1.4K) — plataforma GIS cloud-native
   - mrdoob/three.js (⭐113K) — marcado como "reference" sin skill

## Fix aplicado

1. **Batch size:** 3 → 8 repos por run (cambio en `explorar-stars.py` DEFAULT_BATCH)
2. **Criterios:** Umbral bajado de 500 a 100 en la matriz de decisión. Criterios reescritos para ser agresivos ("umbral bajo, sé generoso").
3. **Prompt del cron:** Actualizado para instruir al agent a ser generoso creando skills.
4. **Skills creados manualmente:** 3 skills geospatial nuevos (threejs-3d-maps, transit-3d-realtime, geolibre-gis-platform).
5. **Registry actualizado:** 6 repos marcados como `skill_created`.

## Resultado después del fix

| Métrica | Antes | Después |
|---------|-------|---------|
| Skills totales | 244 | 247 |
| ChromaDB index | 264 | 267 |
| Batch por run | 3 | 8 |
| Repos con skill | 11 | 17 |
| Pending | 108 | 103 |
| Skills generados (stats) | 9 | 15 |

## Lección

El usuario quiere crecimiento agresivo del sistema de skills. El stars-explorer debe tener un umbral BAJO para crear skills. Mejor crear un skill que se use poco que no crearlo. La tasa de conversión objetivo es 30-50% (no 8.5%).

## Proyección

Con batch de 8 y criterios agresivos:
- 8 repos/noche × 30% conversión = ~2.4 skills/noche
- En una semana: +17 skills
- En un mes: +73 skills
- Meta: 300+ skills para finales de 2026
