---
name: rf-detr
description: "Usa a detectar objetos con RF-DETR (tiempo real)."
version: "2.0.0"
tags: [rf-detr, deteccion, transformer, yolo, vision, tiempo-real]
related_skills: [rf-detr, roboflow-supervision, cctv-yolo, fast-alpr]
---

# RF-DETR — detección en tiempo real (comparativa corregida)

> ⚠️ Corrección 2026-09-05 (auditoría): RF-DETR-L es **más rápido y ligero** que YOLO26-X, pero **ligeramente inferior** en COCO AP50:95 (56.5 vs 56.9); su ventaja es en **AP50** (75.1 vs 74.0). No "supera" engeneral. La latencia <7ms solo aplica a N/S/M/L (XL 11.5ms, 2XL 17.2ms).

**Repo:** `https://github.com/roboflow/rf-detr` (Python, ~9.2K⭐).

## When to Use

- Cuando pidas **detección de objetos en tiempo real** con un modelo Transformer DETR de Roboflow.

## Qué es

Familia DETR de tiempo real (N/S/M/L/XL/2XL). Ventajas frente a YOLO: **latencia baja y peso ligero**; pero RF-DETR-L (56.5 AP50:95) es *ligeramente menor* que YOLO26-X (56.9) — la ventaja real de RF-DETR está en **COCO AP50** y en velocidad/peso.

## Uso

```python
from ultralytics import YOLO   # los pesos de rf-detr se cargan con ultralytics o supervisión
# (ver README del repo para el método exacto de carga y clases)
```

## Pitfalls

- **No** afirmar "supera a YOLO26-X en AP50:95" — es menor (56.5 vs 56.9); gana en AP50 y en velocidad/peso.
- "<7ms" solo para **N/S/M/L**; XL/2XL superan los 7ms.

## Verificación

- Inferir con un modelo RF-DETR sobre un fotograma y comprobar detecciones + latencia según tamaño.
