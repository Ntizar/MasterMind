# Blink Detection via Eye Aspect Ratio (EAR)

**Fecha:** 2026-05-29  
**Mejora:** #5 del pipeline 9009  
**Archivo:** `src/freehands/gaze/blink_detector.py`

## Problema

El usuario necesita un gesto de clic que no requiera manos ni gestos visibles. El parpadeo es el gesto más natural e involuntario que puede usarse como señal intencional.

## Solución: EAR (Eye Aspect Ratio)

El EAR es la proporción entre la altura vertical del ojo y su anchura horizontal. Cuando el ojo se cierra (parpadeo), el EAR cae drásticamente.

```python
# MediaPipe FaceMesh landmarks para párpados:
LEFT_EYE_VERTICAL = (159, 145)   # upper, lower eyelid
RIGHT_EYE_VERTICAL = (386, 374)  # upper, lower eyelid

# EAR = (dist(upper, lower) / dist(outer, inner))
# Normalizado: típicamente 0.3-0.5 cuando abierto, ~0 cuando cerrado
```

### Implementación (`BlinkDetector`)

```python
from freehands.gaze.blink_detector import BlinkDetector

detector = BlinkDetector(
    ear_close_threshold=0.25,    # EAR < este valor = ojo cerrado
    min_blink_frames=3,          # Min frames cerrados para detectar blink
    max_blink_frames=15,         # Si > esto, no es blink (ojos cerrados naturales)
    recovery_frames=2,           # Frames abiertos tras cierre para confirmar
    debounce_seconds=0.3,        # Min tiempo entre blinks consecutivos
)

# Por frame:
event = detector.update(left_ear_norm, right_ear_norm, now=now)
if event:
    print(f"Blink detectado: {event.frame_count} frames, conf={event.confidence}")
```

### Parámetros clave

| Parámetro | Valor default | Explicación |
|-----------|---------------|-------------|
| `ear_close_threshold` | 0.25 | Umbral EAR para considerar ojo cerrado |
| `min_blink_frames` | 3 | Min frames cerrados consecutivos |
| `max_blink_frames` | 15 | Si se excede, se descarta (ojos cerrados) |
| `recovery_frames` | 2 | Frames abiertos tras cierre para confirmar |
| `debounce_seconds` | 0.3 | Min tiempo entre blinks consecutivos |

### Suavizado con deque

- `deque(maxlen=2)` por ojo: suaviza jitter sin retardar la detección
- **Pitfall:** `maxlen=5` hace que el EAR promedio se mantenga alto durante el parpadeo (falsos negativos)
- `reset()` debe limpiar los deques para evitar contaminación entre sesiones

### Integración en GazeTracker

```python
# En tracker.py extract():
l_upper = pt(LEFT_EYE_VERTICAL[0])
l_lower = pt(LEFT_EYE_VERTICAL[1])
r_upper = pt(RIGHT_EYE_VERTICAL[0])
r_lower = pt(RIGHT_EYE_VERTICAL[1])
left_ear = ((l_upper[1] - l_lower[1]) / l_w) if l_w > 0 else 1.0
right_ear = ((r_upper[1] - r_lower[1]) / r_w) if r_w > 0 else 1.0
max_expected_ear = 0.5
left_ear_norm = min(left_ear / max_expected_ear, 1.0)
right_ear_norm = min(right_ear / max_expected_ear, 1.0)
blink_detected = self._blink_detector.update(left_ear_norm, right_ear_norm) is not None
```

### Integración en Fusion (bypass instantáneo)

```python
# En fusion.py step():
def step(self, cursor_xy, confirmed_gesture, blink=False):
    if blink:
        return FusionResult(cursor_xy, self.sm.state, 0.0, "click", blink=True)
    # ... resto del pipeline
```

El blink es el gesto más rápido del sistema: bypass total del state machine y dwell.

### Tests

`tests/test_blink_detector.py` — 8 tests unitarios:
- No blink cuando ojos abiertos
- Blink tras frames cerrados + recovery
- No blink con pocos frames cerrados
- Debounce entre blinks rápidos
- Blink tras ventana de debounce
- Cierre prolongado se descarta
- Ojos asimétricos
- Propiedad `is_blinking`

## Referencia académica

Kotsia, I., & Pitas, I. (2006). "Roulette Wheel Eye-blink Detection for Human-Robot Interaction". Usa la métrica Eye Aspect Ratio, ampliamente adoptada en eye-tracking y reconocimiento de gestos.
