---
name: shademap-competidor-madrid
description: "Usa al crear webs de sombras solares tipo ShadeMap."
version: "1.0.0"
author: "David Antizar (Mastermind)"
license: "CC BY 4.0"
tags: [sombras, webgl, dsm, madrid, shademap, solmad, gpu]
---

# Competir con ShadeMap en Madrid: motor de sombras de nivel fino

## Cuándo usar

- Al construir una web de sombras solares para Madrid o cualquier ciudad española.
- Al mejorar SolMAD (motor, alturas, árboles, horas de sol).
- Al necesitar fuentes oficiales de alturas de edificios o DSM (Ayto. Madrid, IGN PNOA).

## Qué es ShadeMap y cómo funciona (verificado en su código/librería)

- App de ted-piotrowski (README + blog svbtle + shademap.app/help). Librerías públicas: `mapbox-gl-shadow-simulator` y `leaflet-shadow-simulator` (npm, dependen solo de `suncalc`).
- **Motor**: ray-marching por PÍXEL en GPU (WebGL vía gpu.js, evolucionado a GLSL nativo). Cada píxel del mapa lanza un rayo hacia el sol; si interseca el heightmap → sombra. De ahí su finura: sombras con forma real de edificio, no polígonos extruidos aproximados.
- **Datos**: elevación en textura empaquetada. Terreno en canales RG, edificios/DSM en canales BA, escala /5000 (decodifica: `(b*255*256 + a*255)/5000`). Hasta 1000 pasos de ray por píxel, `highp float` (le costó bugs de precisión con `mediump` y `atan2` mal compilado por gpu.js).
- Edificios: OSM + Overture + Mapbox Streets. Sin altura → 3.1 m por planta. "Premium" = LiDAR/fotogrametría a 30 cm, **de pago por km²**.
- Terreno gratis: terrarium (AWS S3 `elevation-tiles-prod`) o Mapbox Terrain-DEM v1.
- Capas: sombra a fecha/hora, "horas de sol" por día, sol anual, perfil de sombra en ruta GPX.

## La clave de la finura (por qué ShadeMap parece "fino")

1. **Heightmap 3D, no raycasting 2D**: el edificio es volumen real (huella + altura por píxel), proyecta sombras con forma exacta y bordes limpios a cualquier zoom.
2. **GPU**: 2M píxeles × ray-march en paralelo; la UI va fluida mientras arrastras el slider de tiempo.
3. **Precisión float alta** y empaquetado de elevación en textura (2 canales = 65.535 m de rango).
4. **Solo viewport**: calcula únicamente lo visible en pantalla (por eso las sombras desaparecen al hacer zoom).
5. **Datos de calidad por zonas** (su modelo de negocio): OSM aproximado gratis, LiDAR 30 cm de pago.

## Datos de Madrid que ShadeMap NO usa (ventaja competitiva local)

| Fuente | Qué da | Acceso |
|---|---|---|
| **Ayto. Madrid — Alturas de edificios** | altura estimada por polígono de edificio (z máx − z mín huella), EPSG:25830, CC BY 4.0 | ArcGIS REST: `https://sigma.madrid.es/hosted/rest/services/CARTOGRAFIA/EDIFICIOS_ALTURAS/MapServer` (query por bbox) |
| **Ayto. Madrid — MDS 2023** | Modelo Digital de Superficies, nube 100 ptos/m², malla **10 cm y 1 m**, formato COG, CC BY 4.0 | `https://datos.madrid.es/dataset/300731-0-cartografia-elevaciones-mds` |
| **Ayto. Madrid — Modelo 3D LOD2** | edificios extruidos con cubiertas reales (restitución 1:1000), SLPK/OBJ por distritos | Geoportal: dataset "Modelo tridimensional de edificaciones" |
| **IGN PNOA-LiDAR** | nube de puntos clasificada (suelo/vegetación/edificio), MDS/MDT nacional | `https://centrodedescargas.cnig.es` y mapa LiDAR en pnoa.ign.es |

Pipeline Madrid ganador: **huellas del ayto + alturas oficiales** (mejor que OSM `levels*3.2`) → rasterizar a DSM de malla 0,5–1 m → sumar MDS para cubiertas y árboles reales → textura GPU. Resultado: precisión tipo "premium" de ShadeMap, gratis, para todo Madrid.

## Arquitectura recomendada (motor nuevo)

1. **Mapa**: MapLibre GL JS (gratis, mismo motor que Mapbox GL; la librería de ShadeMap funciona con ambos).
2. **Capa de sombra**: custom style layer WebGL (como hace `mapbox-gl-shadow-simulator`) con shader propio:
   - Textura A: terreno (RG) + edificios/DSM (BA), codificación /5000.
   - Uniforms: azimut/elevación solar (SunCalc o fórmula NOAA propia), bbox del viewport, color/opacity.
   - Fragment shader: ray-march desde cada píxel hacia el sol con paso adaptativo (grande al inicio, fino cerca de la superficie); máx ~256 pasos basta en ciudad plana.
   - `mediump` NO vale para sol bajo: exigir `highp` o trabajar en coordenadas locales centradas (evita catástrofes de precisión tipo la de gpu.js/atan2).
3. **Modo "horas de sol"**: N iteraciones del mismo shader con fechas distintas → raster acumulado (así hace el suyo con `sunExposure.iterations`).
4. **Tiles de datos propios**: pre-rasterizar Madrid a COG/tiles PNG de elevación (servidos estáticos desde GitHub Pages o Vercel) — nada de Overpass en runtime.
5. **Terrazas/POIs**: lo que ya tiene SolMAD (censo ayto. reproyectado EPSG:25830→WGS84).

## Plan de mejora de SolMAD (fases, cada una suma finura)

- **F1 — Alturas oficiales**: sustituir `levels*3.2` por el ArcGIS de alturas del ayto. (query por bbox, cache local). Impacto inmediato en exactitud sin tocar el motor.
- **F2 — Motor GPU**: capa WebGL con ray-march sobre heightmap rasterizado desde huellas+alturas (F1). Sustituye al worker CPU de segmentos para el render del mapa; el worker CPU puede seguir para el cálculo puntual por terraza (es rápido con pocas).
- **F3 — DSM 1 m + árboles**: fusionar MDS 2023 (canopy incluido) para sombras de árboles y cubiertas reales.
- **F4 — Horas de sol / sol anual**: acumulación GPU por píxel.
- **F5 — Rutas GPX**: perfil de sol a lo largo de un paseo (diferenciador frente a SolMAD terrazas-only).

## Pitfalls

- `atan2` en GLSL vía transpiladores (gpu.js) se compila como `atan` de 1 arg → sombras erróneas; escribir GLSL nativo.
- Precisión float: usar coordenadas locales en metros (origen = centro viewport), nunca grados absolutos dentro del shader.
- Los COG del MDS son grandes: servir tiles recortados pre-generados, no el COG completo al navegador.
- Overpass solo para actualizar huellas puntuales; el bulk va por datasets oficiales descargados.
- Licencias: datos ayto. CC BY 4.0 → atribución obligatoria; OSM ODbL si se mezcla.

## Referencias

- Librería abierta de ShadeMap: github.com/ted-piotrowski/mapbox-gl-shadow-simulator (dist ESM sin minificar contiene los shaders completos, analizarlos ahí).
- Blog del autor: tedpiotrowski.svbtle.com (primavera: break en loops GLSL + compresión de elevación = 4x; invierno: precisión mediump y bug atan2).
- SolMAD actual: `Ntizar/solmad`, worker `src/workers/shadows.worker.ts` (raycasting 2D, grid 60 m, visitToken).
- Skills relacionadas: solar-shadow-computation, solar-shadows-web-workers (patrón CPU actual de SolMAD).
