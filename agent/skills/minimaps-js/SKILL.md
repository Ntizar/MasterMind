---
name: minimaps-js
version: "2.0.0"
description: "Use al generar relieves 3D tipo puck desde mapa web."
tags: [threejs, terrain, dem, satelite, opentopography, 3d-print, geospatial]
related_skills: [monolith-terrain, threejs-3d-maps, map33-js]
---

# Minimap Maker — Relieves 3D ("pucks") desde Mapa Web

**Repo fuente:** `github.com/drjenkin/minimaps` (MIT, JS + Flask, ~45⭐, activo 2026) — https://github.com/drjenkin/minimaps

> ⚠️ Corrección 2026-09-02 (stars-explorer): la v1 de este skill describía mal el repo como "librería de minimapas interactivos". **No es una librería npm** — es una app web generadora de relieves 3D imprimibles. Reescrito con el README real.

## When to Use

- Cuando pidas **maquetas/relieves 3D de terreno** (zonas de hasta 40 km de ancho) a partir de un mapa, para impresión 3D o visualización.
- Cuando busques patrón **imágenes satélite + DEM → malla 3D texturizada en el navegador** (draping).
- Cuando necesites exportar terreno como **STL/OBJ/GLB** (impresión 3D) o **PNG/WebM** (vídeo).

## Qué es

Generador browser-based de "pucks" de relieve: teselas de terreno cuadradas construidas con **imágenes satélite cosidas y draped sobre modelo de elevación real**. Enmarcas una región en un mapa satelital → captura → sale un modelo 3D texturizado con controles de estilo (filtros, iluminación, **exageración Z**) → exportas.

- **Motor 3D:** three.js; librería de pucks guardada **en el propio navegador**.
- **Backend:** Flask mínimo (`python backend/app.py` → http://127.0.0.1:5001/); en Windows también `launch.bat`.
- **Fuentes de elevación:**
  - **Copernicus DEM 30m** (default, más nítido) vía OpenTopography — requiere **API key gratuita** (se guarda solo en el navegador).
  - **AWS Terrain tiles** — global y **sin key** (fallback recomendado si OpenTopography bloquea: lección conocida en Water3J, donde opentopodata sí estaba bloqueado por el ISP y EMODnet funcionaba).
- **Imágenes:** Esri World Imagery; bordes/etiquetas OSM + Nominatim para topónimos.

## Uso

```bash
git clone https://github.com/drjenkin/minimaps.git
cd minimaps
python -m venv .venv && .venv/Scripts/activate   # Windows
pip install -r requirements.txt
python backend/app.py
# abrir http://127.0.0.1:5001/ → enmarcar región → Capture → elegir DEM → exportar
```

## Patrón reutilizable (lo que hay que aprender del repo)

1. **Pipeline captura→malla**: tile stitching de imagery por bbox + muestra del DEM en rejilla + geometría `PlaneGeometry` de three.js desplazada por altura + textura combinada = puck en un paso, sin GIS de escritorio.
2. **Exageración Z como control de usuario**, no hardcodeada (relieves suaves se leen mejor con ×2–×5).
3. **Export múltiple desde la misma malla**: STL/OBJ/GLB (impresión) + PNG/WebM (difusión).
4. **Dos fuentes DEM con degradación keyless** (Copernicus vía OpenTopography → AWS Terrain) — patrón robusto ante CORS/bloqueos de ISP.

## Pitfalls

- No es librería instalable — clonar y servir la app (o extraer su patrón a una tool propia).
- Copernicus vía OpenTopography exige key gratuita; AWS Terrain es más basto.
- Pucks derivados de Esri/OSM/Copernicus: al redistribuir, respetar licencias de cada proveedor (ODbL en OSM, términos Esri).
- Repo personal (~8 ficheros JS + 1 py): sin tests ni SLA; tratar como referencia de patrón, no como dependencia.
- Áreas urbanas llanas dan pucks poco espectaculares — funciona mejor con relieve (Pirineos, Sistema Central, costa vasca).

## Verificación

Tras montar la app localmente: capturar Mollepata (Cusco) o cualquier pico pirineo ≤40 km, exportar GLB y comprobar que la textura sigue el relieve sin desgarros en los bordes.

## Referencias

- Creado por stars-explorer 2026-09-02; reescrito v1→v2 tras leer el README real del repo.
