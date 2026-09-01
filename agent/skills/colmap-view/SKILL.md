---
name: colmap-view
description: "Colmap View — visualizador web drag'n'drop de modelos COLMAP (nubes de puntos, frustums de cámara, rigs, Gaussian splatting)."
version: "2.0.0"
author: "David Antizar (Ntizar) — vía stars-explorer"
license: "AGPL-3.0 (uso como herramienta web; OJO al incorporar código a proyectos propios)"
tags: [colmap, sfm, fotogrametria, threejs, wasm, pointcloud, viewer, cv]
---

# Colmap View — Visualizador Web de Reconstrucciones COLMAP

## Qué es

Colmap View (github.com/ColmapView/Colmapview.github.io, TypeScript, AGPL-3.0, demo en colmapview.github.io) es el visor drag'n'drop de reconstrucciones COLMAP más completo que existe: se abre la página, se suelta la carpeta del dataset y listo — sin instalación, con más funciones que la GUI original de COLMAP. Renderizado GPU con WASM sobre React Three Fiber (fiber + drei + @sparkjsdev/spark para splats).

## Capacidades clave (v2026-08)

- **Nube de puntos**: coloreable por RGB, error de reproyección o longitud de track; tamaño/opacidad/thinning ajustables.
- **Cámaras**: frustums piramidales, flechas o planos de imagen texturizados; coloreables por ID de cámara o rig frame; rigs multi-cámara con resaltado animado.
- **9 sistemas de coordenadas**: COLMAP, OpenCV, Three.js, OpenGL, Vulkan, Blender, Houdini, Unity, Unreal — conversión entre ellos.
- **Alineación y escala al mundo real**: 1-Point Origin (clic en un punto → origen), 2-Point Scale (dos puntos + distancia real), 3-Point Align (tres puntos → plano horizontal), Floor Detection automática con RANSAC, gizmo interactivo. Los resultados se apilan en un transform pendiente con Reset/Apply.
- **Puntos 2D en imagen**: selección de cámaras y visualización de keypoints sobre las imágenes originales (fuera del visor 3D).
- **Galería**: grid/lista con virtual scrolling para >10.000 imágenes; vista de imagen con detalles por cámara.
- **Rendimiento**: parsing WASM para >1M de puntos, lazy-loading para `images.bin` de 1.9GB+, GPU instancing para miles de cámaras.
- **Carga remota**: Load URL / Load manifest — encuentra la reconstrucción dentro de un repo o listado de Hugging Face; ZIP aceptado en lugar de carpeta; modo images-only para galerías sin reconstrucción.
- **Splats**: carga `.spz` / `.ply` (Gaussian splatting) junto a la reconstrucción.
- **Export/Captura**: screenshot, share, export; perfiles de configuración; auto-orbit para presentaciones; atajos de teclado completos (panel Help con `I` o `?`).

## Uso

```
1. Abrir https://colmapview.github.io/
2. Soltar carpeta con cameras.bin/txt + images.bin/txt + points3D.bin/txt
   (subcarpetas sparse/0/ y sparse/ escaneadas automáticamente; opcional images/ y masks/)
```

Instalación local para desarrollo: `git clone https://github.com/ColmapView/Colmapview.github.io.git && pnpm install && pnpm dev` (Vite + Playwright para tests).

## Casos de uso para David

- **Validar outputs SfM/fotogrametría** (pipeline COLMAP local o Nube) sin abrir la GUI de escritorio.
- **Geolocalización de modelos**: 2-Point Scale + 3-Point Align → pasar reconstrucciones a escala métrica real para comparar con LiDAR/Catastro.
- **Repos Hugging Face**: inspeccionar datasets 3D (splats/reconstrucciones) directo por URL — útil en investigación de visión.
- **Satellite imagery / geo-forensics**: verificar reconstrucciones antes de proyectarlas en visores GIS (Water3J, España Atlas).

## Stack y referencia de arquitectura

React 19 + Vite + TypeScript, @react-three/fiber + drei, gs-toolbox (transformaciones geométricas), libarchive.js (ZIP en navegador), fflate, gif.js, @sparkjsdev/spark (splats), tanstack/react-virtual (galería). Buen patrón a copiar para cualquier visor de datos binarios pesados en navegador: parsing WASM + lazy loading + virtual scrolling.

## Comparativa de alternativas (consultado 2026-09-01)

- **Visor oficial COLMAP** (escritorio, C++): más rápido cargando, menos herramientas de alineación/export, requiere instalación.
- **pycolmap + open3d** (scripting): para automatizar, no para inspección visual interactiva.
- **Polycam/Luma web viewers**: propietarios, cierran el flujo con fuentes abiertas.
- **Punto débil de ColmapView**: dataset grande por red puede tardar en cargar en cliente (mitigado con lazy loading y manifest de HF).

## Pitfalls

- **AGPL-3.0** — usar la web o el viewer como herramienta es libre; incorporar su código a un producto propio obliga a abrir el producto. Citar siempre.
- Los datasets `.bin` y `.txt` son equivalentes; si faltan archivos `_undistorted`, el visor puede no mostrarlos (feature de versión reciente).
- Reconstrucciones sin escalado métrico: la escala de COLMAP es arbitraria → SIEMPRE aplicar 2-Point Scale antes de cruzar con datos GIS reales.
- El repo se movió de `TobiasGiovannini/Colmapview.github.io` a la org `ColmapView/` — usar la URL nueva.

## Verificación

- El visor muestra puntos + frustums tras soltar la carpeta (si sale vacío, faltaría points3D o la carpeta sparse no se detectó).
- Tras 2-Point Scale, la distancia medida entre los dos puntos coincide con la real introducida (panel de estadísticas).
- Export/screenshot genera archivo descargable con el render actual.

