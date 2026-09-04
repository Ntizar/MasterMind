---
name: aws-dem-terrain-tiles
version: "1.0.0"
description: "Descarga tiles DEM Terrarium de AWS con bbox y zooms."
tags: [dem, terrain, elevation, tiles, aws, cli, maplibre]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [dem, terrain, tiles, aws, cli]
    related_skills: [ign-wmts-tiles, threejs-3d-maps, monolith-terrain, forge3d-terrain-cartography]
---
# AWS Terrarium DEM Tile Downloader

## Resumen
CLI Python que descarga y verifica tiles de elevación (Digital Elevation Model) con codificación **Terrarium** del dataset **AWS Open Data Terrain Tiles**. Define el área y los niveles de zoom y genera los tiles en estructura estándar `z/x/y` más un `tiles.json` listo para proyectos de mapas. Requiere Python 3.7+.

## Instalación
```bash
git clone <repo-url> && cd AWS-Dem-Downloader
python3 -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt
chmod +x terrain_cli.py           # Linux/macOS (opcional)
```

## Uso (CLI real)
```bash
./terrain_cli.py [OPTIONS] COMMAND [ARGS]...
./terrain_cli.py download [OPTIONS] -- <min_lon,min_lat,max_lon,max_lat>
```
- **Importante**: el `--` antes del BBOX es **obligatorio** si tu longitud mínima (`min_lon`) es negativa — indica que es argumento, no opción.
- **Argumento** `<min_lon,min_lat,max_lon,max_lat>`: bounding box WGS84.
- **Opciones**:
  - `-z, --zoom-range <min,max>`: niveles de zoom (ej. `10,14`). Default: `10,15`. Max: `15`.
  - `-o, --output-dir <dir>`: dónde guardar tiles. Default: `terrain_tiles`.
  - `-c, --concurrency <int>`: hilos de descarga. Default: `10`.
  - `--only-missing`: modo inteligente — descarga solo los tiles que faltan.
- Opciones globales: `-h, --help`, `--version`.

## Patrones / Arquitectura
- Descarga de precisión por bounding box.
- Control de zoom (0-15).
- Descarga concurrente multihilo.
- Verificación de integridad del caché (chequeo dimensional básico de tiles corruptos/faltantes).
- Genera `tiles.json` metadata compatible con MapLibre GL JS, Leaflet, Mapbox GL JS, etc.
- Informes JSON detallados del estado de descarga/verificación, incluyendo fallos.

## Pitfalls
- Omitir el `--` delante de un bbox con longitud negativa rompe el parseo.
- `--only-missing` ahorra tiempo/ancho de banda al reutilizar caché.

## Verificación
- Descargar un bbox pequeño, confirmar estructura `z/x/y`, `tiles.json` y el informe JSON sin fallos.

## Referencia
- Repo: https://github.com/orcunkok/AWS-Dem-Downloader (MIT). Fuente de datos: AWS Open Data Terrain Tiles (codificación Terrarium).
