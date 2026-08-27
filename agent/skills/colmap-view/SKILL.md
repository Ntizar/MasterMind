---
name: colmap-view
description: Colmap View — visualizador web de modelos 3D generados con COLMAP (fotogrametría/SfM).
category: computer-vision
---

# Colmap View — Visualizador Web de Modelos 3D

## Qué es

Colmap View es un visualizador web para modelos 3D generados por COLMAP:
- **COLMAP integration** — carga directamente outputs de COLMAP
- **Web-based** — visualización en navegador sin instalar nada
- **Point cloud** — visualiza nubes de puntos
- **Camera poses** — muestra poses de cámara del reconstrucción

## Instalación

```bash
# COLMAP需要先安装
# https://github.com/colmap/colmap

# Luego usar Colmap View
git clone https://github.com/ColmapView/Colmapview.github.io.git
cd Colmapview.github.io
# Servir con cualquier HTTP server
python -m http.server 8000
```

## Casos de uso para David

- **Fotogrametría** — visualizar reconstrucciones 3D de fotos
- **SfM pipelines** — validar outputs de Structure-from-Motion
- **Satellite imagery** — aplicar fotogrametría a imágenes satelitales
- **3D content** — generar assets 3D para Three.js scenes

## Pitfalls

- COLMAP requiere mucho RAM para datasets grandes
- Los modelos 3D completos pueden ser pesados (>GB)
- El visualizador web es básico — funcionalidades limitadas
- COLMAP es lento para datasets grandes

## Referencias

- Repo: `github.com/ColmapView/Colmapview.github.io` (61⭐)
- COLMAP: `github.com/colmap/colmap`
