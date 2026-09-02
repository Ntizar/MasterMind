# 2026-09-02 — Stars Explorer: la plaga de los skills-v1 inventados

## Batch

Explorados 3 repos (quedan 55 pendientes):

| Repo | ⭐ | Decisión |
|---|---|---|
| alexwohlbruck/portolan | 48 | ✅ **skill nuevo** `geospatial/portolan-transit-maps` |
| drjenkin/minimaps | 45 | ⬆️ **upgrade** `minimaps-js` v1→v2 |
| BlinkTagInc/gtfs-to-chart | 42 | ⬆️ **upgrade** `gtfs-to-chart` v1→v2 |

## Hallazgo importante: skills de batch 2026-06-18/19 estaban INVENTADOS

2 de los 3 repos de este batch **ya tenían skill**, pero ambos describían mal el repo:

- `minimaps-js` decía "librería ligera de minimapas interactivos npm" → **falso**: es una app web (Flask + three.js) que genera relieves 3D imprimibles ("pucks") con imágenes satélite sobre DEM. Ni siquiera se instala por npm.
- `gtfs-to-chart` decía "gráficos de frecuencia de rutas" → **falso**: genera **diagramas stringline/Marey** (tiempo × estación a escala, pendiente = velocidad).

Patrón de la v1 mala: bullets genéricos ("Lightweight / Interactive / Customizable"), casos de uso vagos ("Dashboard maps — minimapas en dashboards"), y hasta una URL de CDN inventada (`cdn.example.com/minimaps.min.js`). Las v1 se escribieron sin leer el README real — fueron relleno del maratón de 117 repos.

**Lección operativa:** el pipeline de batch masivo debe exigir fetch del README ANTES de escribir el SKILL.md, y el scout nocturno debería **auditar skills existentes** cuando se re-encuentra un repo ya procesado, no solo hacer dedup-skip. Esta vez, gracias a que los criterios mandaban comparar, se detectó y corrigió.

## Lo bueno: Portolan (el hallazgo de la noche)

Generación automática de mapas de tránsito esquemáticos (estilo metro) desde GTFS + vías OSM. Barcelona ya configurada. Su `docs/LESSONS.md` es una joya: dos pipelines muertos antes del tercero, y 8 leyes de geometría vectorial pagadas con artefactos visibles (mediana vs media ponderada, secciones perpendiculares vs proyección más-cercana, paralelismo sostenido para bundling, veto a las "pasadas de reparación"). Su scorer "golden sketch" (dibujo humano de referencia + PASS/FAIL con desviación media <2 m) es patrón exportable a cualquier pipeline geométrico nuestro.

## Pendientes

- Auditar otras v1 del maratón 2026-06-18/19 (`gtfs-tidy`, `gtfs2shp`, `colmap-view`, `quantstats-pro`…) por el mismo síntoma: bullets genéricos sin README.
