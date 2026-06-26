# FreeHands: Kalman Cursor Implementation

## Session: 30/05/2026 — 9009 Pipeline, Mejora #15

### Contexto

FreeHands usa `GazeRegressor.predict()` que aplicaba un EMA (alpha=0.5) para suavizar el cursor. Reemplazado por `KalmanCursorFilter` con modelo de velocidad constante [x, y, vx, vy].

### Archivos creados/modificados

| Archivo | Acción | Líneas |
|---------|--------|--------|
| `src/freehands/gaze/kalman_filter.py` | Creado | 147 |
| `src/freehands/gaze/calibration.py` | Modificado | -9 +14 |
| `src/freehands/gaze/__init__.py` | Modificado | +4 |
| `tests/test_kalman_filter.py` | Creado | 18 tests |

### Integración en GazeRegressor

```python
# calibration.py — __init__ modificado:
def __init__(
    self,
    model: GazeModel,
    screen_size: tuple[int, int],
    *,
    kalman_params: KalmanParams | None = None,
) -> None:
    # ...existing...
    self._kalman = KalmanCursorFilter(kalman_params)

# predict() modificado:
def predict(self, features: np.ndarray) -> tuple[int, int] | None:
    # ...existing regression math...
    smoothed = self._kalman.update((x, y))
    return int(round(smoothed[0])), int(round(smoothed[1]))
```

### Verificación

- 15 tests existentes de gaze_calibration: ✅ pasando
- 18 tests nuevos de kalman_filter: ✅ pasando
- 81 tests totales en el suite relevante: ✅ pasando
- `ruff check`: ✅ limpio
- `ast.parse()`: ✅ todos los archivos

### Sintonía de parámetros elegida

```python
# Default (equilibrio recomendado)
process_noise = 25.0
measurement_noise = 400.0
```

### Notas de diseño

- El filtro asume FPS constante (30 fps en FreeHands), dt=1 frame
- El clamping de coordenadas se mantiene en `GazeRegressor.predict()` ANTES de pasar al Kalman
- `GazeRegressor` es retrocompatible: acepta `kalman_params=None` (usa defaults)
- Los tests de integración verifican que `GazeRegressor` tiene `_kalman` attribute y que las predicciones son suavizadas
