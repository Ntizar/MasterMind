# Patrón: Magnifier Overlay (Zoom sobre área de mirada)

**Mejora #32** — Zoom magnifier sobre área de mirada (VocalIris-OS inspiración).

## Módulo: `ui/magnifier.py`

```python
class MagnifierWidget(QtWidgets.QWidget):
    """Circular magnifying glass that enlarges the desktop around the gaze cursor."""
    
    def __init__(self, zoom_factor=2.0, radius=100, offset_x=0, offset_y=-140):
        # FramelessWindowHint | WindowStaysOnTopHint | Tool
        # WA_TranslucentBackground | WA_TransparentForMouseEvents
        # Timer interno ~80ms para refresh de pantalla
        ...
    
    def update_cursor(self, cursor: tuple[int, int] | None) -> None:
        """Show/hide magnifier and update its position."""
        ...
    
    def _capture_screen_region(self, center) -> QtGui.QPixmap | None:
        """Capture and scale up the screen region around center."""
        source_radius = int(self._radius / self._zoom_factor)
        # Clamp to screen bounds, grab with QScreen.grabWindow(), scale
        ...
    
    def paintEvent(self, _event) -> None:
        # Draw scaled pixmap clipped to circle
        # Glass highlight gradient (top-left)
        # Blue border ring (PALETTE.blue)
        ...
```

## Integración en `main.py`

### 1. Importar y crear

```python
from .ui.magnifier import MagnifierWidget

# En run_system():
magnifier = MagnifierWidget(zoom_factor=2.0, radius=100, offset_y=-140)
magnifier_visible = False
```

### 2. Interceptar comandos de voz

En `handle_voice_action()`, ANTES de llegar al dispatcher:

```python
if action in {"zoom_in", "zoom_out"}:
    nonlocal magnifier_visible
    if action == "zoom_in" and not magnifier_visible:
        magnifier_visible = True
        magnifier.show()
        overlay.flash_action("zoom: activado")
        panel.set_last_action("lupa activada")
        audio_feedback.play_gesture_confirmation()
    elif action == "zoom_out" and magnifier_visible:
        magnifier_visible = False
        magnifier.hide()
        overlay.flash_action("zoom: desactivado")
        panel.set_last_action("lupa desactivada")
        audio_feedback.play_gesture_confirmation()
    return  # No pasar al dispatcher
```

### 3. Actualizar en tick()

```python
# En nonlocal de tick():
nonlocal ..., magnifier_visible

# En el loop tick():
if magnifier_visible:
    magnifier.update_cursor(result.cursor_xy)
elif magnifier.visible:
    magnifier.update_cursor(None)
```

### 4. Cerrar en IDLE

```python
if result.state == State.IDLE:
    ...
    if magnifier_visible:
        magnifier_visible = False
        magnifier.hide()
```

## Diferencias con widgets tipo radial-menu

| Aspecto | Radial menu / teclado / emoji | Magnifier |
|---------|------------------------------|-----------|
| Apertura | Gestos o voz (hold) | Toggle voz (zoom in/out) |
| Posición | Fija o centrada en cursor | Sigue al cursor siempre |
| Refresh | Solo al moverse | Timer interno 80ms |
| Cierre | Escape / gesto / IDLE | IDLE / zoom out |
| Método | `update_dwell(cursor)` | `update_cursor(cursor)` |
| Estado | `widget.visible` | `magnifier_visible` (bool local) |

## Pitfalls

- **No usar `magnifier.flash_action()`** — el magnifier no tiene ese método. Usar `overlay.flash_action()`.
- **`magnifier_visible` debe ser `nonlocal`** en `tick()` o `handle_voice_action()` lo modifican.
- **El timer interno del magnifier** (~80ms) es independiente del tick principal (30fps). Esto evita que el magnifier se quede "congelado" si el tick se ralentiza.
- **Captura de pantalla**: `QScreen.grabWindow(0)` captura toda la pantalla. Si el área de captura excede los límites de pantalla, se clampa con `rect.intersected(screen_rect)`.
- **`set_zoom_factor()` y `set_radius()`** son métodos públicos para cambiar parámetros en runtime sin recrear el widget.
