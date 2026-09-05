---
name: cctv-yolo
description: "Usa a detectar objetos en CCTV con YOLOv5."
version: "2.0.0"
tags: [cctv, yolo, deteccion, video, gradio, yolov5, python]
related_skills: [cctv-yolo, roboflow-supervision, fast-alpr, rf-detr]
---

# CCTV + YOLO — detección de objetos sobre cámaras (YOLOv5)

> ⚠️ Corrección 2026-09-05 (auditoría): el repo usa **YOLOv5** con una app **Gradio** (`python app.py`), no ultralytics/yolov8. La clase "objetos abandonados" no existe en el repo.

**Repo (fuente):** repo de detección CCTV con YOLOv5 (app Gradio, `python app.py`) — verificar el repo exacto en el SKILL.md.

## When to Use

- Cuando pidas **detectar/contar objetos (tráfico, personas)** sobre un vídeo o cámara con YOLO en local.

## Qué es

Aplicación de detección de objetos sobre CCTV/streams. Stack: **YOLOv5** + **Gradio** (UI) — arranca con `python app.py`.

## Uso

```bash
pip install -r requirements.txt
python app.py        # arranca la UI Gradio de detección
```

## Pitfalls

- Modelo: **YOLOv5** (no YOLOv8/ultralytics).
- Arranque: **`python app.py`** (Gradio), no otro CLS.
- No hay clase "objetos abandonados" en el repo (no inventar clases).

## Verificación

- `python app.py` → subir un vídeo y comprobar que detecta/cuenta objetos.
