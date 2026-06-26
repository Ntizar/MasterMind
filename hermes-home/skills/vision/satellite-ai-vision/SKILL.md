---
name: satellite-ai-vision
description: "Herramientas de visión por satélite y computer vision para análisis de tráfico, terreno y detección de objetos con IA."
version: 1.0.0
author: Mastermind (Ntizar)
tags: [vision, satellite, computer-vision, detection]

---

# Satellite AI & Computer Vision

Herramientas para análisis de tráfico satelital, visión por CCTV, terreno 3D y detección de objetos con IA.

## 1. DRISH-X (sparkyniner) ⭐228
**Qué hace:** Inteligencia de tráfico de carga desde imágenes satelitales Sentinel-2 gratuitas.
**Autor:** Sairaj Balaji (junior/student — ver notas de audit en references)
**Paper base:** Fisser et al. 2022, "Detecting Moving Trucks on Roads Using Sentinel-2 Data", Remote Sensing of Environment (https://ui.adsabs.harvard.edu/abs/2022RemS...14.1595F/abstract)
**Referencia técnica:** S2TruckDetect por Henrik Fisser

### Mecanismo científico
Sentinel-2 captura bandas espectrales con desfase temporal de ~1.01s entre B02 (blue) y B04 (red). Un vehículo a 80 km/h se desplaza ~22m en ese intervalo. A 10m/píxel, aparece en posición diferente en cada banda → **smear azul→verde→rojo de 3-5 píxeles**. El sistema detecta este patrón espectral, no el vehículo en sí.

### Pipeline técnico detallado
1. **Feature Stack (7 features/píxel):**
   - F0: varianza de RGB
   - F1: normalized_ratio(B04, B02) — red/blue
   - F2: normalized_ratio(B03, B02) — green/blue
   - F3-5: B04, B03, B02 mean-centered
   - F6: B08 (NIR) mean-centered
2. **Clasificación RF:** Random Forest sobre el feature stack → 4 clases [background, blue, green, red]. Post-processing: umbral background confidence 0.75.
3. **Extracción recursiva:** clustering neighborhood starting at blue pixels → grow through green → then red. Validación: 3 colores presentes, 3-5 píxeles, score > 1.2.
4. **Output:** lat/lon, heading, velocidad estimada, confidence score.

### Proxy fallback
Cuando no hay modelo RF (.pickle), usa heurísticas con pesos mágicos (`centered_B * 5 + var_feat * 10`). Funciona pero calidad desconocida.

### Accuracy por región
- **Europa autopistas:** 70-80% detección, 5-10% falsos positivos
- **MENA:** fuerte (árido, alto contraste, raramente nublado)
- **Asia Sur/Sudeste:** mixto (monzón limita frames útiles)
- **Sub-Sahara:** bueno en carreteras pavimentadas, débil en no pavimentadas
- **No detecta coches:** <1 píxel a 10m. No distingue tipos de vehículo.

### Limitaciones clave
- Resolución 10m: camiones (~18m) → 2 píxeles → smear a 3-5px. Coches (~4.5m) → sub-píxel invisible.
- Sin visión a través de nubes (óptico)
- Revisión cada 5 días (Sentinel-2) → trend analysis, NO real-time
- Mejora posible con PlanetScope a 3.7m (requiere API key Planet Labs)

### Código en repo
- `drishx.py` (1132 líneas) — FastAPI + engine de detección completo
- `rf_model.pickle` — modelo entrenado incluido en repo
- `frontend/` — Leaflet + Chart.js, dark tactical theme
- Dependencias: fastapi, uvicorn, sentinelhub, osmnx, geopandas, scikit-learn==1.3.2, numpy<2.0.0, rasterio

### Estado de la implementación
Ciencia sólida (paper peer-reviewed), pipeline fiel a S2TruckDetect reference implementation. Código competente pero amateur: sin tests, sin DB (historial en memoria), sin auth en APIs, sin Docker. Credenciales Copernicus en UI sin encriptación.

### Casos de uso validados
- Contar tráfico de camiones en cualquier autopista del mundo
- Analizar patrones económicos proxy (puertos, rutas comerciales)
- Monitoreo de sanciones (cambio de tráfico en fronteras)
- Respuesta a crisis (carreteras bloqueadas vs activas)
- Periodismo investigativo (datos satelitales independientes)

## 2. TrafficLab-3D (duy-phamduc68) ⭐311
**Qué hace:** Digital twin de tráfico a partir de vídeo CCTV mp4 + ubicación Google Maps.
**Autor:** Yuk (yuk068 / duy-phamduc68)
**Estado:** PoC experimental, monolítico, en proceso de refactorización a modular
**Licencia:** No especificada (contactar autor para contribuciones)
**Input:** Vídeo CCTV mp4 + coordenadas GPS de Google Maps
**Output:** Visualización 3D del tráfico en digital twin

### Pipeline técnico detallado:
1. **CCTV footage (mp4)** → YOLO para detección y tracking de vehículos (2D bounding boxes)
2. **Camera calibration** → intrinsics + extrinsics de la cámara CCTV
3. **Homography** → mapeo planar del plano de la carretera al plano de la imagen
4. **Projection mapping** → proyectar los vehículos detectados sobre un modelo 3D
5. **Satellite imagery** → imagen satelital como base georreferenciada
6. **3D visualization** → PyQt5 GUI con visualización del digital twin

### Estructura de directorios por ubicación:
```
location/{location_code}/
  footage/*.mp4              # vídeo CCTV
  sat_{location_code}.png    # imagen satelital
  cctv_{location_code}.png   # imagen crítica de referencia
  G_projection_{location_code}.json  # matriz de proyección
  illustrator/               # assets opcionales Adobe Illustrator
```

### Stack:
- **Python** + **YOLO** (detección de objetos)
- **Camera calibration** + **homography** (mapeo 2D→3D)
- **Satellite imagery** (base georreferenciada)
- **PyQt5** (GUI)
- **Projection mapping** (integración 3D)

### Temas/Topics:
3d-bbox, autonomous-driving, camera-calibration, cctv-analysis, computer-vision, digital-twin, geospatial-mapping, homography, intelligent-transportation, object-detection, object-tracking, projection-mapping, pyqt5-gui, satellite-imagery, smart-city, traffic-analysis, traffic-monitoring, urban-analytics, yolo

### Recursos:
- **Blog:** yuk068.github.io/2026/02/20/traffilclab-3d-overview
- **YouTube Demo:** TrafficLab 3D v1.0 Demo
- **YouTube Guide:** TrafficLab 3D Guide
- **Academic Report:** Google Drive (en README)

### Ideal para:
- Prototipos rápidos de digital twins sin infraestructura costosa
- Estudiantes/investigadores sin acceso a calibración profesional
- Integración con datos abiertos de flotas municipales (ej. Cantabria)
- **Patrón clave:** CCTV existente + geolocalización = digital twin funcional sin sensores IoT

### Integración con GeoAsset:
Este patrón es directamente aplicable a la gestión de flotas municipales — cámaras de tráfico existentes + detección de vehículos = datos en tiempo real para el gemelo digital.

## Referencias
- `references/cctv-to-digital-twin-pattern.md` — Patrón CCTV→Digital Twin aplicado a GeoAsset

## 3. Boxer3D (Barath19) ⭐398
**Qué hace:** Detección 3D de objetos en AR para iPhone con LiDAR.
**Tecnología:** Swift, iOS, YOLO11n + BoxerNet (Meta) + ARKit + SceneKit
**Pipeline:**
1. YOLO11n → detección 2D (top 3 boxes, 80 COCO classes)
2. BoxerNet → lifting a 7-DoF 3D boxes (center, size, yaw)
3. LiDAR depth → median depth per 16x16 patch
4. ARKit → camera pose + intrinsics + gravity
5. SceneKit → AR rendering de cajas 3D

### Requisitos:
- iPhone 12 Pro+ (LiDAR requerido)
- iOS 16.0+
- ~450MB para modelos

## 4. AWS Terrarium DEM Downloader (orcunkok) ⭐8
**Qué hace:** Descarga tiles de elevación (DEM) del dataset AWS Terrain Tiles.
**Tecnología:** Python 3.7+, concurrent downloads
**Features:**
- Bounding box precision
- Zoom levels 0-15
- Concurrent downloads (multi-threaded)
- Data integrity verification
- tiles.json output compatible con MapLibre GL JS, Leaflet, Mapbox GL JS

### Uso:
```bash
python download.py --bbox -3.7,40.4,-3.6,40.5 --zoom 12 --output ./tiles
```

## 5. City2Graph (c2g-dev) ⭐1212
**Qué hace:** Librería Python para convertir datasets geoespaciales en grafos para GNNs.
**Tecnología:** Python, GeoPandas, NetworkX, PyTorch Geometric
**Dominios:** streets, transportations, OD matrices, POI proximities
**Instalación:** `pip install city2graph` o `conda install -c conda-forge city2graph`

### Casos de uso:
- Graph Neural Networks para datos geoespaciales
- Análisis de redes de transporte
- Proximidad de POIs
- Matrices OD (origen-destino)

## Patrones Comunes

1. **Satellite → Ground:** DRISH-X usa datos satelitales para inferir tráfico terrestre
2. **CCTV → 3D:** TrafficLab convierte vídeo 2D en visualización 3D
3. **Mobile LiDAR → 3D AR:** Boxer3D usa LiDAR del iPhone para detección 3D en AR
4. **DEM → Mapping:** AWS DEM downloader para datos de elevación en proyectos de mapeo

## Integración con Mastermind

- Para análisis de tráfico: combinar DRISH-X (satélite) + TrafficLab-3D (CCTV)
- Para proyectos de mapeo: usar AWS DEM + City2Graph para grafos geoespaciales
- Para AR/3D: Boxer3D como referencia de lifting 2D→3D con LiDAR
