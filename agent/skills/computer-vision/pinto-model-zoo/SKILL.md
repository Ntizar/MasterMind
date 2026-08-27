---
name: pinto-model-zoo
description: Colección masiva de modelos ML pre-entrenados — YOLO, segmentación, detección, clasificación para visión por computador.
version: "1.0.0"
tags: [models, ML, CV, YOLO, segmentation, detection, pretrained]
---

# PINTO Model Zoo

## Resumen

Colección masiva de modelos ML pre-entrenados — YOLO, segmentación, detección, clasificación. 4.4k⭐.

## Repo de referencia

- **GitHub:** `github.com/PINTO0309/PINTO_model_zoo`
- **Lenguaje:** Varied (modelos ONNX, TensorRT, CoreML, etc.)
- **Licencia:** Varía por modelo

## Instalación

```bash
# Clonar el repositorio completo (es grande)
git clone --depth 1 https://github.com/PINTO0309/PINTO_model_zoo.git
cd PINTO_model_zoo
```

## Estructura

```
PINTO_model_zoo/
├── 00_YOLOv3/
├── 01_YOLOv5/
├── 02_YOLOv7/
├── 03_YOLOv8/
├── 04_YOLOv10/
├── segment_anything_model/
├── real_time_object_detection/
└── ...
```

## Uso Básico

```python
# Ejemplo: Cargar modelo YOLOv8 ONNX
import cv2
import numpy as np

# Cargar modelo
net = cv2.dnn.readNet("models/YOLOv8/yolov8n.onnx")

# Preparar imagen
img = cv2.imread("input.jpg")
blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
net.setInput(blob)

# Inferencia
output = net.forward()

# Parsear resultados
boxes = output[0][0]
```

## Modelo más populares del Zoo

1. **YOLO series:** v3, v5, v7, v8, v10, v11, v12
2. **Segment Anything (SAM):** Meta's SAM, SAM2
3. **Face recognition:** ArcFace, FaceNet
4. **Object detection:** DETR, RT-DETR
5. **Super resolution:** Real-ESRGAN
6. **Depth estimation:** MiDaS, DPT

## Integración con Mastermind

- Complementa `roboflow/rf-detr` para detección con datasets propios
- Útil para `fast-alpr` — modelos de reconocimiento de matrículas
- Fuente de modelos para `computer-vision` pipelines
- Reemplaza training from scratch para modelos comunes

## Pitfalls

- **Tamaño:** El repo completo es >50GB — clonar con `--depth 1`
- **Licencias:** Verificar licencia de cada modelo individualmente
- **Formatos:** Mix de ONNX, TensorRT, CoreML, OpenVINO
- **Organización:** Mal organizado, hay que buscar manualmente
- **Dependencias:** Cada modelo puede necesitar librerías diferentes

## Referencias

- [GitHub: PINTO0309/PINTO_model_zoo](https://github.com/PINTO0309/PINTO_model_zoo)
