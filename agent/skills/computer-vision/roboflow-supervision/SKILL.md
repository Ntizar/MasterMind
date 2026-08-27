---
name: roboflow-supervision
version: "1.0.0"
description: "Supervision — librería de visualización, post-procesamiento y utilidades para computer vision de Roboflow. Annotators, metrics, datasets, tracking. Complemento esencial de RF-DETR y otras CV libs."
tags: [computer-vision, visualization, annotation, metrics, object-detection, segmentation, tracking, roboflow, post-processing]
---

# Supervision — Computer Vision Utilities by Roboflow

## Resumen

**Supervision** es la librería de utilidades de Roboflow para **visualización, post-procesamiento y evaluación** de resultados de computer vision. Incluye annotators para bounding boxes, segment masks, keypoints; métricas COCO/mAP; manejo de datasets; y herramientas de tracking.

## Funcionalidades principales

### Annotators (visualización)
- `BoxAnnotator` — dibuja bounding boxes con color por clase
- `LabelAnnotator` — añade labels textuales a las boxes
- `MaskAnnotator` — visualiza segment masks con transparencia
- `KeyPointAnnotator` — dibuja keypoints con líneas de esqueleto
- `TriangleAnnotator`, `CircleAnnotator`, `ColorAnnotator` — formas alternativas

### Detections y Metadata
- `Detections` — clase central con boxes, masks, keypoints, confidences, class_ids
- `Metadata` — metadatos asociados a detecciones
- Conversión desde varios formatos: inference, coco, yolov5, yolov8, yolov11, detr

### Datasets
- Carga y export de datasets en múltiples formatos (COCO, YOLO, Roboflow)
- Split train/val/test automático
- Augmentation helpers

### Metrics
- Cálculo de mAP (COCO-style)
- confusion matrices
- Precision-recall curves

## Instalación

```bash
pip install supervision
```

## Uso con RF-DETR (patrón estándar)

```python
import supervision as sv
from rfdetr import RFDETRMedium
from rfdetr.assets.coco_classes import COCO_CLASSES

# Cargar modelo
model = RFDETRMedium()

# Inferencia
detections = model.predict("image.jpg", threshold=0.5)

# Preparar labels
labels = [COCO_CLASSES[cid] for cid in detections.class_id]

# Visualización
annotated = sv.BoxAnnotator().annotate(sv.Image(image), detections)
annotated = sv.LabelAnnotator().annotate(annotated, detections, labels)

# Guardar resultado
annotated.save("result.jpg")
```

## Uso con otros modelos

```python
# De inference API (Roboflow Inference)
from inference import get_model
model = get_model("rf-detr-medium")
predictions = model.infer(image)
detections = sv.Detections.from_inference(predictions)

# De COCO JSON
detections = sv.Detections.from_coco_json(annotation_path, image_paths)

# De YOLO
detections = sv.Detections.from_yolov8(output_file)
```

## Integración con Mastermind

- **Pipeline de CV:** RF-DETR → Supervision para visualización en dashboards
- **Visor de imágenes:** annotators para proyectos de geospatial (NAIP, Sentinel)
- **Evaluación de modelos:** métricas COCO para comparar modelos en benchmarking
- **Generación de datasets:** preparar datasets etiquetados para fine-tuning

## Referencias

- Repo: `roboflow/supervision`
- Docs: https://supervision.roboflow.com
- Complementa: `rf-detr` (detección), `vision/clip-multimodal` (embeddings)
