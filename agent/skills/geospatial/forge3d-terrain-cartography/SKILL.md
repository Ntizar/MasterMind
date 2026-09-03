---
name: forge3d-terrain-cartography
description: "Use al renderizar terreno 3D en mapas de impresión."
version: "1.0.0"
tags: [gis, terrain, webgpu, rust, python, cartography, dem, path-tracing, headless-rendering]
---

# Forge3D — Terreno path-traced y cartografía desde Python

**Repo:** github.com/milos-agathon/forge3d (640⭐, Rust+Python, MIT/Apache-2.0 core, actualizado ago-2026)
**Docs:** https://milos-agathon.github.io/forge3d/ · **Galería:** /gallery/ (masters hasta 7200×7200)

## Qué es y cuándo usarlo

Motor de render **offline** (path tracing con iluminación global y sombras) expuesto como wheels de Python. A diferencia de los visores web que ya cubrimos (three.js/MapLibre/globos → skills `photorealistic-3d-tiles-threejs`, `navara-3d-globe-engine`, `monolith-terrain`), forge3d produce **mapas cartográficos finalizados a resolución de impresión** — títulos, leyendas, escala y norte incluidos, compuestos in-engine, sin compositor externo.

Usar cuando se necesite:
- Visualizaciones de terreno fotorrealistas para **informes/PDF** (sombras solares, relieve, hidrología)
- **Secuencias de frames** animadas (bucle Python + ffmpeg): humo de incendios, evolución temporal de campos
- Mapas temáticos sobre DEM: densidad poblacional extruida (WorldPop/GHSL), land cover Sentinel-2, clima TerraClimate, hidrológica HydroSHEDS
- Cartografía de ciudades con edificios LOD2 (CityGML/CityJSON sobre RGE ALTI)

## Instalación

```bash
pip install forge3d              # core open-source (MIT OR Apache-2.0)
pip install "forge3d[jupyter]"   # widget de notebook
pip install "forge3d[datasets]"  # datasets de muestra on-demand
pip install "forge3d[all]"       # todo
```

Requiere GPU con WebGPU (o fallback Vulkan). Python 3.10+.

## Patrón núcleo: 60 segundos a un render

```python
import forge3d as f3d

dem_path = f3d.fetch_dem("rainier")          # DEM de muestra on-demand

with f3d.open_viewer_async(terrain_path=dem_path, width=1440, height=900) as viewer:
    viewer.set_z_scale(0.1)                   # exageración vertical
    viewer.set_orbit_camera(phi_deg=28, theta_deg=49, radius=5400, fov_deg=42)
    viewer.set_sun(azimuth_deg=302, elevation_deg=24)   # sol = clave para sombras
    viewer.snapshot("rainier.png", width=1920, height=1080)
```

`fetch_dem` baja el modelo de elevación, `open_viewer_async` abre ventana orbitable real, `snapshot` escribe el frame a la resolución pedida.

## Superficie del motor (lo que cubre)

| Área | Capacidad |
|---|---|
| **Terrain** | `open_viewer_async()`, `ViewerHandle`, GeoTIFF o DEMs numpy, clipmaps para regiones grandes |
| **Rendering** | Path tracing, materiales PBR, subsurface scattering, agua con reflejos, nubes y contact shadows, AOV + salida EXR |
| **Data** | Streaming COG, helpers CRS, nubes de puntos LAZ/COPC/EPT, 3D Tiles, GeoJSON, CityJSON, datasets on-demand |
| **Cartografía** | Overlays ráster/vector, labels con halo y oclusión, graticules, `Legend`, `ScaleBar`, `NorthArrow`, `MapPlate` |
| **Offscreen** | `Scene`, `Session`, `TerrainRenderer` + `TerrainRenderParams` para trabajo headless y batch |
| **Output** | PNG y PNG16, **exportación vectorial SVG y PDF**, scene bundles, widgets notebook |

## Patrón animación temporal (time-lapse)

Las escenas se pilotan 100% desde Python: "un eje temporal es otro bucle más" — fetch de campos (p. ej. predicción HRRR para humo volumétrico), step del reloj, `snapshot()` por frame, y los frames van a ffmpeg. Mismo scene graph que los stills, una sola cámara, sin compositing.

## Integración con proyectos de David

- **Sombras solares Madrid / shadeMap**: `set_sun(azimuth_deg, elevation_deg)` + path tracing = sombras reales con GI para las horas críticas; exportar PNG16/SVG para informes.
- **DataHub España / informes**: figuras de relieve e hipometría vectoriales (SVG/PDF) en vez de PNG rasterizados.
- **Agua (Water3J)**: agua con reflejos PBR del motor para láminas de inundación sobre terreno.
- Alternativa **offline Python** a `monolith-terrain` / `three-scope-map` (que son navegador).

## Comparativa de alternativas (consulta 2026-09-04)

| Herramienta | Liga | Cuándo gana |
|---|---|---|
| **forge3d** (640⭐) | Render offline Python | Fotorrealismo path-traced + cartografía publicable + time-lapse |
| `monolith-terrain` / `three-scope-map` / `map33-js` | Navegador three.js | Interactividad en web pública, gratis, sin GPU local |
| `navara-3d-globe-engine` (MapLibre 3D) | WebGIS teselas | Mapa-base con teselas oficiales, contexto de ciudad |
| QGIS + Blender | Desktop tradicional | Control total pero manual, sin scripting Python integrado |

## Pitfalls

- **Funciones Pro de pago**: composición `MapPlate`, exportación vectorial y pipelines de importación de edificios están gatingados — desbloqueo con `forge3d.set_license_key(...)`. El core (terreno, path tracing, overlays, PNG) es libre. Para SVG/PDF vectoriales sin licencia → render core + recomponer fuera. (David: SOLO herramientas gratuitas → tratar Pro como extra opcional, nunca base de pipeline.)
- **GPU obligatoria**: WebGPU/Vulkan. En máquina sin GPU discreta, headless puede fallar o ir lento — probar primero con un DEM pequeño (`fetch_dem`).
- **`set_z_scale` crítico**: los DEM vienen en metros; sin exageración vertical (0.05–0.2) el terreno sale plano en renders a distancia orbital.
- **Proyecto joven (creado 2025-07, 640⭐)**: API sujeta a cambios; fijar versión en requirements si entra en pipeline de producción.
- Los renders de README/galería van downsampled — los masters reales llegan a 7200×7200 (peso alto en PNG16/EXR).

## Verificación

```bash
python -c "import forge3d as f3d; print(f3d.__version__)"
# Smoke test: dem = f3d.fetch_dem("rainier") → snapshot 800×600 → comprobar PNG existe y pesa >0
```

## Referencias

- Quickstart: https://milos-agathon.github.io/forge3d/start/quickstart.html
- Feature map: https://milos-agathon.github.io/forge3d/guides/feature_map.html
- Tutorials GIS/Python: https://milos-agathon.github.io/forge3d/tutorials/index.html
- API reference: https://milos-agathon.github.io/forge3d/api/api_reference.html
- Ejemplo live orbitable (Mount Shasta): https://milosgis.com/
