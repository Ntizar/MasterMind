---
name: gaze-tracking
version: "1.0.0"
description: >
  GazeTracking — librería Python para eye tracking usando OpenCV. 
  Implementa detección de ojos, seguimiento de mirada y mapeo de 
  coordenadas. Útil para control hands-free, accesibilidad, UX research.
license: MIT
tags: [computer-vision, gaze, eye-tracking, MediaPipe]

---

# GazeTracking — Eye Tracking Library

## Visión General

[GazeTracking](https://github.com/antoinelame/GazeTracking) (2.6k⭐) es una librería Python para eye tracking fácilmente implementable en proyectos. Usa OpenCV para detección de ojos y seguimiento de mirada.

## Instalación

```bash
pip install gaze_tracking
```

## Uso Básico

```python
from gaze_tracking import GazeTracking

gaze = GazeTracking()
camera = cv2.VideoCapture(0)

while True:
    _, frame = camera.read()
    gaze.refresh(frame)
    
    # Detectar si el usuario está mirando
    if gaze.is_center():
        print("Mirando al centro")
    
    # Obtener coordenadas de mirada
    pupil_left = gaze.pupil_left_coords()
    pupil_right = gaze.pupil_right_coords()
    
    # Dibujar overlay
    gaze.draw_base(frame)
    gaze.draw_pupil_left(frame)
    gaze.draw_pupil_right(frame)
    
    cv2.imshow('Gaze Tracking', frame)
    
    if cv2.waitKey(1) == 27:  # ESC para salir
        break
```

## Funcionalidades

### Detección de Ojos
- Detección de región de ojos en tiempo real
- Soporte para cámaras web estándar
- Procesamiento a ~30 FPS

### Seguimiento de Mirada
- Coordenadas de pupilas izquierda y derecha
- Punto central de mirada
- Detección de dirección (arriba, abajo, izquierda, derecha)

### Indicadores
- `is_blinking()` — ¿El usuario está parpadeando?
- `is_center()` — ¿Mirando al centro?
- `get_direction()` — Dirección de mirada
- `pupil_left_coords()` — Coordenadas pupila izquierda
- `pupil_right_coords()` — Coordenadas pupila derecha

## Integración con Control Hands-Free

```python
# Ejemplo: Control por mirada
if gaze.get_direction() == "left":
    action("navigate_back")
elif gaze.get_direction() == "right":
    action("navigate_forward")
elif gaze.is_blinking():
    action("select")
```

## Referencias
- [GazeTracking GitHub](https://github.com/antoinelame/GazeTracking)
- [FreeHands](https://github.com/Ntizar/FreeHands) — Control hands-free con gaze + gestures + voice
