---
name: roboflow-supervision
description: "Usa a post-procesar detecciones y anotar con Supervision."
version: "2.0.0"
tags: [supervision, deteccion, anotar, yolo, roboflow, vision, python]
related_skills: [roboflow-supervision, cctv-yolo, fast-alpr, rf-detr]
---

# Supervision — post-procesado y anotaciones de visión (API actual)

> ⚠️ Corrección 2026-09-05 (auditoría): `sv.Image`, `Detections.from_yolov8` y `Detections.from_coco_json` ya **no existen** en Supervision moderno. La API actual pasa numpy/PIL directo y usa `from_ultralytics` y helpers de `supervision.dataset`.

**Repo:** `https://github.com/roboflow/supervision` (Python, ~50K⭐).

## When to Use

- Cuando pidas **anotar/visualizar/dibujar cajas** de detecciones (YOLO, etc.) o filtros/post-procesado (zone, line, byte_tracker) sobre vídeo/imagen.

## Uso (API real)

```python
import supervision as sv

# Anotar con cajas: la imagen se pasa directa (numpy/PIL), sin sv.Image
annotated = box_annotator.annotate(scene=image.copy(), detections=detections)

# Detecciones desde Ultralytics YOLO:
detections = sv.Detections.from_ultralytics(results)   # (ya no from_yolov8)

# Carga de datasets COCO: helpers de supervision.dataset
from supervision.dataset import load_coco_annotations, coco_annotations_to_detections
```

## Pitfalls

- **No** `sv.Image` — pasa la imagen numpy/PIL directamente a `annotate(scene=..., detections=...)`.
- **No** `Detections.from_yolov8` → `from_ultralytics`; `from_yolov5` sí existe.
- **No** `Detections.from_coco_json` → helpers `supervision.dataset`.

## Verificación

- `annotate(scene=image, detections=...)` y comprobar que las bboxes se dibujan; `from_ultralytics` con un modelo YOLO.
