---
name: pinto-model-zoo
description: "Usa a usar modelos ONNX del PINTO Model Zoo."
version: "2.0.0"
tags: [pinto, model-zoo, onnx, modelos, ml, deteccion, opencv]
related_skills: [pinto-model-zoo, roboflow-supervision, onnx-webgpu-inference, fast-alpr]
---

# PINTO Model Zoo — colección masiva de modelos ONNX

> ⚠️ Corrección 2026-09-05 (auditoría): la estructura no es `00_YOLOv3/`/`03_YOLOv8/`; los 503 subdirectorios son **numerados** (`001_deeplabv3`, `023_yolov3-nano`, ...). No existe la ruta `models/YOLOv8/yolov8n.onnx`.

**Repo:** `https://github.com/PINTO0309/PINTO_model_zoo` (Python, ~4.6K⭐).

## When to Use

- Cuando quieras **descargar modelos ONNX/NCNN (YOLO, segmentation, etc.)** listos para OpenCV/DNN, con propia conversión y quite.

## Qué es

Catálogo masivo de **modelos convertidos a ONNX** por PINTO0309: cada modelo en una carpeta numerada (`001_...`, `023_...`, hasta ~503) con pesos, metadata y scripts.

## Uso

- Navegar las carpetas **numeradas** (`<NNN>_<nombre>`); descargar el `.onnx` de la carpeta del modelo.
- P.ej. `001_deeplabv3`, `023_yolov3-nano`, etc. (NO `00_YOLOv3/`).

## Pitfalls

- Estructura: carpetas **numeradas** (`001_...`), no `00_YOLOv3/`/`03_YOLOv8/`.
- No existe `models/YOLOv8/yolov8n.onnx`.

## Verificación

- `ls` en el repo y escoger un `.onnx` de una carpeta numerada; cargarlo con `cv2.dnn.readNet`.
