---
name: gaze-tracking
description: "Usa a hacer eye tracking con GazeTracking."
version: "2.0.0"
tags: [gaze, eye-tracking, opencv, dlib, python, vision]
related_skills: [gaze-tracking, openpose-pose-estimation, fast-alpr]
---

# GazeTracking — eye tracking (OpenCV + dlib)

> ⚠️ Corrección 2026-09-05 (auditoría): los métodos `draw_base()`/`draw_pupil_left()`/`draw_pupil_right()`/`get_direction()` **no existen**. API real: `refresh()`, `pupil_left_coords()`, `pupil_right_coords()`, `horizontal_ratio()`/`vertical_ratio()`, `is_left()`/`is_right()`/`is_center()`/`is_blinking()`, `annotated_frame()`. Instalación: clonar + `pip install -e .`; tag MediaPipe incorrecto (usa OpenCV+dlib).

**Repo:** `https://github.com/antoinelame/GazeTracking` (Python, ~2.6K⭐).

## When to Use

- Cuando pidas **seguimiento de la mirada** (detectar pupilas, parpadeo, dirección) con OpenCV+dlib en una webcam.

## Uso (API real)

```python
from gaze_tracking import GazeTracking
gaze = GazeTracking()
gaze.refresh(frame)                     # procesa un frame
ratio = gaze.horizontal_ratio()         # y vertical_ratio()
gaze.is_blinking(), gaze.is_left(), gaze.is_right(), gaze.is_center()
annotated = gaze.annotated_frame()      # frame con overlay (no draw_base)
```

## Pitfalls

- Métodos reales: `annotated_frame()`, `horizontal_ratio()`, `vertical_ratio()`, `is_*()`; **no** `draw_base`/`draw_pupil_left`/`draw_pupil_right`/`get_direction`.
- Install: clonar + `pip install -e .` (el paquete PyPI `gaze-tracking` v0.0.1 es viejo/distinto).
- Tag: usa **OpenCV + dlib**, no MediaPipe.

## Verificación

- `gaze.refresh(frame)` y `gaze.annotated_frame()`; probar `is_blinking()`.
