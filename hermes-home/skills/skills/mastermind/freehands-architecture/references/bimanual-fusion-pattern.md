# Patrón de Fusión Bimanual (HandFusion)

Módulo `gestures/hand_fusion.py` que asigna roles complementarios a dos manos detectadas simultáneamente.

## Principio

Cuando **ambas manos** están visibles en el frame:
- **Mano derecha** → offset de cursor fino (±10px basado en posición relativa al centro de pantalla)
- **Mano izquierda** → scroll vertical (barrido) + zoom (pinch open/close)

Cuando **una sola mano** está visible → no-op, comportamiento normal de un solo hand.

## Clases

### `HandFusion`

```python
from freehands.gestures.hand_fusion import HandFusion, BimanualResult

bimanual = HandFusion()  # en run_system()
```

Método principal:
```python
result = bimanual.update(hands, handedness, confidence)
```

### `BimanualResult`

```python
@dataclass
class BimanualResult:
    cursor_offset: tuple[float, float] = (0.0, 0.0)  # (dx, dy) para cursor
    scroll_action: str | None = None                  # "scroll_up" / "scroll_down"
    zoom_action: str | None = None                    # "zoom_in" / "zoom_out"
    left_hand_centroid: tuple[float, float] | None = None
    right_hand_centroid: tuple[float, float] | None = None
    left_active: bool = False
    right_active: bool = False
```

## Integración en main.py

### 1. Importar

```python
from .gestures import HandFusion
from .fusion import FusionResult
```

### 2. Instanciar en run_system()

```python
bimanual = HandFusion()
```

### 3. En el loop tick(), DESPUÉS de volume_control, ANTES de fusion.step_and_voice()

```python
# Bimanual fusion
bimanual_result = bimanual.update(
    hand_obs.hands,
    hand_obs.handedness,
    hand_obs.confidence,
)

# Ejecutar scroll/zoom si se detectaron
if bimanual_result.scroll_action and fusion.sm.state != State.IDLE:
    if dispatcher.execute(bimanual_result.scroll_action, at_xy=cursor):
        overlay.flash_action(f"bimanual: {bimanual_result.scroll_action}")
        panel.set_last_action(f"bimanual: {bimanual_result.scroll_action}")
        audio_feedback.play_gesture_confirmation()

if bimanual_result.zoom_action and fusion.sm.state != State.IDLE:
    if dispatcher.execute(bimanual_result.zoom_action, at_xy=cursor):
        overlay.flash_action(f"bimanual: {bimanual_result.zoom_action}")
        panel.set_last_action(f"bimanual: {bimanual_result.zoom_action}")
        audio_feedback.play_gesture_confirmation()

# Aplicar cursor offset SOLO cuando ambas manos están activas
if (bimanual_result.right_active and bimanual_result.left_active
        and result.cursor_xy is not None):
    ox, oy = bimanual_result.cursor_offset
    result = FusionResult(
        cursor_xy=(result.cursor_xy[0] + int(ox), result.cursor_xy[1] + int(oy)),
        state=result.state,
        dwell_progress=result.dwell_progress,
        fired_action=result.fired_action,
        blink=result.blink,
        blink_event=result.blink_event,
        voice_action=result.voice_action,
        gaze_confirmed=result.gaze_confirmed,
        head_pose_active=result.head_pose_active,
        head_coarse_dx=result.head_coarse_dx,
        head_coarse_dy=result.head_coarse_dy,
    )

# Reset cuando se pierden las manos
if not hand_obs.hands:
    bimanual.reset()
```

## Umbrales configurables

```python
LEFT_HAND_SCROLL_THRESHOLD = 0.012   # desplazamiento mínimo Y normalizado
LEFT_HAND_SCROLL_COOLDOWN = 3        # frames entre scrolls
ZOOM_PINCH_CLOSE_DIST = 0.05         # dedos cerrados → zoom out
ZOOM_PINCH_OPEN_DIST = 0.10          # dedos abiertos → zoom in
ZOOM_PINCH_DELTA = 0.02              # delta mínimo para detectar apertura
ZOOM_COOLDOWN_FRAMES = 5             # frames entre zooms
```

## Diferencias con otros módulos de mano

| Módulo | Tipo | Entrada | Salida |
|--------|------|---------|--------|
| `HandTracker` | Clasificación de pose | landmarks → gesture_id | `pointing_up`, `open_palm`, etc. |
| `VolumeControl` | Posición de zona | centroid Y | `volume_up` / `volume_down` |
| `HandFusion` | Fusión bimanual | 2 manos → roles | scroll + zoom + cursor offset |
| Palm-scroll (en HandTracker) | Motion-based | wrist Y delta | `scroll_up` / `scroll_down` |
| Air-scroll (en HandTracker) | Motion-based | centroid delta | `scroll_up` / `scroll_down` |

## Pitfalls

1. **El cursor offset solo se aplica cuando ambas manos están activas.** Si una mano desaparece, el offset se vuelve (0,0) automáticamente porque `right_active` y `left_active` son False.
2. **No confundir con palm-scroll/air-scroll:** palm-scroll requiere palma abierta, air-scroll funciona con cualquier pose pero es un gesto de mano única. HandFusion es específicamente para DOS manos simultáneas con roles separados.
3. **El orden en tick() importa:** bimanual debe ejecutarse ANTES de `fusion.step_and_voice()` porque el cursor offset se aplica al resultado de fusion.
4. **Reset al perder manos:** siempre llamar `bimanual.reset()` cuando `hand_obs.hands` está vacío, para que el scroll no dispare en el frame siguiente sin movimiento real.
