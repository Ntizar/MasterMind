# TrafficLab-3D

- **URL:** https://github.com/duy-phamduc68/TrafficLab-3D
- **Categoría:** GIS / Computer Vision / Digital Twin
- **¿Qué hace?:** TrafficLab es un suite end-to-end de análisis de tráfico que transforma vídeo CCTV (mp4) y su ubicación en Google Maps en un "gemelo digital" 3D. Realiza calibración de cámara (undistorsión, homografía, parallax), inferencia de detección y seguimiento de objetos con YOLO, y visualización lado a lado de CCTV con bounding boxes 3D y vista satélite con floor boxes, velocidad y orientación. Todo funciona sobre un entorno plano y requiere solo un vídeo CCTV y una captura de satélite.
- **Casos de uso:**
  - Visualización de gemelo digital de tráfico a partir de CCTV existente
  - Análisis de velocidad y orientación de vehículos en tiempo real
  - Herramienta educativa para estudiantes de visión por computadora
  - Prototipado rápido de sistemas de monitorización de tráfico
  - Simulación y RL como tareas downstream a futuro
- **Snippets útiles:**

**Pipeline de inferencia (InferencePipeline):**
```python
from trafficlab.inference.pipeline import InferencePipeline
from trafficlab.projection.g_projection import GProjection
from trafficlab.motion.kinematics import TrackSmoother

# Inicializar motor de proyección G
with open("G_projection_loc.json", "r") as f:
    g_data = json.load(f)
g_engine = GProjection(g_data, base_dir="location/loc/")

# Pipeline de inferencia
pipeline = InferencePipeline(
    location_code="119NH",
    footage_path="location/119NH/footage/cctv.mp4",
    config_path="inference_config.yaml",
    output_root="output/",
    g_proj_path="location/119NH/G_projection_119NH.json",
)
pipeline.run()  # Produce output/*.json.gz con tracking, velocidad, heading, 3D boxes
```

**Motor de proyección G (GProjection):**
```python
from trafficlab.projection.g_projection import GProjection
import numpy as np

# Cargar proyección calibrada
g_proj = GProjection(config_data, base_dir="location/loc/")

# CCTV -> Satélite (con corrección de parallax para altura h)
sat_pt = g_proj.cctv_to_sat(u, v, h=1.5)

# Satélite -> CCTV (inverso)
cctv_pt = g_proj.sat_to_cctv(x, y, h=1.5)

# Obtener punto de contacto en suelo desde bounding box 2D
proj_res = g_proj.get_ground_contact_from_box(
    (x1, y1, w, h), h_meters=1.5,
    ref_method="center_bottom_side",
    proj_method="down_h"
)

# Levantar floor box de satélite a 3D box en espacio CCTV
bbox_3d = g_proj.sat_floor_to_cctv_3d(sat_poly, obj_height_m)
```

**Smoother de tracking con cinemática (TrackSmoother):**
```python
from trafficlab.motion.kinematics import TrackSmoother

smoother = TrackSmoother(config_kinematics)
result = smoother.update(
    current_sat_pos=[x, y],
    dt=0.033,          # delta time en segundos
    px_per_m=50.0,     # pixeles por metro
    svg_heading=45.0   # heading opcional desde SVG
)
# result = {"speed_kmh": 35.2, "heading": 42.5, "default_heading": False}
```

**Parsing de SVG para headings (SVGParser):**
```python
from trafficlab.projection.svg_parser import SVGParser

# Parsear SVG con líneas de orientación (grupos "Guidelines" o "Physical")
parser = SVGParser("layout.svg", alignment_matrix_A)
heading = parser.get_nearest_heading(sat_pt)
# Devuelve el ángulo en grados de la línea SVG más cercana al punto
```

**Renderer de CCTV con boxes 3D (CCTRenderer):**
```python
from trafficlab.visualization.cctv_renderer import CCTRenderer
import cv2

renderer = CCTRenderer()
pixmap = renderer.render(
    frame=bgr_frame,       # numpy array BGR de OpenCV
    objects=frame_objects, # lista de dicts con bbox_3d, heading, etc.
    show_tracking=True,
    show_3d=True,
    box_thickness=2,
    show_label=True
)
```

**Renderer de satélite con floor boxes (SatRenderer):**
```python
from trafficlab.visualization.sat_renderer import SatRenderer

renderer = SatRenderer()
pixmap = renderer.render(
    objects=frame_objects,
    scene_w=1920, scene_h=1080,
    show_tracking=True,
    show_sat_box=True,       # dibuja floor box polígono
    show_sat_arrow=True,     # dibuja flecha de heading
    show_sat_label=True,     # etiqueta "class 35.2km/h"
    sat_label_size=12
)
```

**Configuración de inferencia (inference_config.yaml):**
```yaml
configs:
  mild_smoothing:
    prior_dimensions: "measurements_visdrone"
    frames:
      fps: 30
      max_frame: 600
    model:
      weights: "./models/yolo8s-visdrone-ft.pt"
      device: "0"
      imgsz: 736
      conf: 0.35
      iou: 0.5
    tracking:
      tracker_type: "bytetrack"
      persist: true
    kinematics:
      heading_smoothing: "adaptive_ema"
      heading_ema:
        alpha_min: 0.05
        alpha_max: 0.4
        speed_ref: 3.0
      speed_smoothing: "ema"
      speed_ema_alpha: 0.4
```

**Estructura de datos de salida (JSON comprimido):**
```json
{
  "mp4_path": "footage.mp4",
  "meta": {"resolution": [1280, 720], "fps": 30.0},
  "location_code": "119NH",
  "mp4_frame_count": 1800,
  "animation_frame_count": 600,
  "frames": [
    {
      "frame_index": 0,
      "objects": [
        {
          "id": 0,
          "tracked_id": 5,
          "class": "car",
          "confidence": 0.92,
          "bbox_2d": [100.0, 200.0, 250.0, 350.0],
          "reference_point": [175.0, 275.0],
          "sat_coords": [500.0, 300.0],
          "have_heading": true,
          "have_measurements": true,
          "heading": 42.5,
          "speed_kmh": 35.2,
          "sat_floor_box": [[...], [...], [...], [...]],
          "bbox_3d": [[...], [...], [...], [...], [...], [...], [...], [...]]
        }
      ]
    }
  ]
}
```

- **Cómo integrarlo en proyectos:**
  1. **Instalación:** `conda env create -f environment.yml` (Python 3.10, PyTorch 2.5.1, ultralytics, OpenCV, PyQt5).
  2. **Preparar datos por ubicación:** Crear carpeta `location/{code}/` con `footage/*.mp4`, `cctv_{code}.png`, `sat_{code}.png`, y opcionalmente `layout_{code}.svg` y `roi_{code}.png`.
  3. **Calibrar:** Usar la GUI (`main.py` → tab Calibration) para construir el archivo `G_projection_{code}.json`. El proceso tiene 3 fases: Undistort (intrinsics + distorsión Brown-Conrady), Homography (anclajes manuales CCTV↔Satélite), Parallax (posición de cámara + escala px/m). También opcional: SVG alignment y ROI.
  4. **Inferir:** Configurar `inference_config.yaml` (modelo YOLO, tracker, parámetros cinemáticos) y `prior_dimensions.json` (dimensiones reales por clase). Ejecutar `main.py` → tab Inference. Produce archivos `.json.gz` en `output/`.
  5. **Visualizar:** Tab Visualization del GUI para ver CCTV con 3D boxes + satélite con floor boxes, velocidad y orientación lado a lado.
  6. **Integración programática:** Importar `InferencePipeline`, `GProjection`, `TrackSmoother`, `CCTRenderer`, `SatRenderer` directamente desde el paquete `trafficlab`. El pipeline es independiente de la GUI.
  7. **Modelos:** Descargar YOLOv8-s/YOLOv11-s finetuned desde el Google Drive del autor y colocarlos en `models/`.
  8. **Limitaciones conocidas:** Solo funciona en entornos planos; no sigue modelos cinemáticos de vehículos (puede haber rotaciones/teleportaciones aleatorias); la calibración inicial y creación de SVG es tediosa; la oclusión causa desaparición de objetos.
  9. **Requisitos clave:** GPU (CUDA) para inferencia, Qt5 para GUI, datos de satélite (sat_*.png) y CCTV (cctv_*.png) de la misma ubicación.

- **Fecha de aprendizaje:** 2026-05-26
