# Multimodal Dictation Intent Pattern

Patrón para activar funcionalidades de dictado por voz mediante **detección multimodal**: el usuario debe mirar una región de texto (dwell) Y decir un comando de voz. Esto evita activaciones accidentales y da control preciso sobre dónde se inserta el texto dictado.

## Arquitectura

```
GazeOverlay ──cursor_xy──▶ DictationIntentDetector
TextRegionDetector ──regions──▶ DictationIntentDetector
                              │
                    gazing_at_text (bool)
                    ready_to_activate (bool)
                    hovered_region (TextRegion)
                              │
                    update_dwell(cursor, regions, cx, cy)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            VoiceListener         overlay.set_dictation_indicator()
            drain_commands()      (pulsing ring + badge)
                    │
            cmd_text in trigger list
                    │
            DictationIntentDetector.consume_ready()
                    │
            ContinuousDictationEngine.start()
```

## Implementación

### 1. Crear el detector de intención

```python
# voice/dictation_intent.py
from dataclasses import dataclass
import time

GAZE_TO_DICTATE_DWELL_MS = 500  # ms de mirada en región de texto

@dataclass
class DictationIntentState:
    gazing_at_text: bool = False
    hovered_region: TextRegion | None = None
    dwell_progress: float = 0.0
    ready_to_activate: bool = False
    ready_at: float = 0.0
    last_gaze_lost_at: float = 0.0
    gaze_lost_debounce_ms: float = 300.0

class DictationIntentDetector:
    def __init__(self, dwell_ms: int = GAZE_TO_DICTATE_DWELL_MS):
        self._dwell_ms = dwell_ms
        self._state = DictationIntentState()
        self._anim_step = 16  # ms per frame (~60fps)
        self._dwell_steps = dwell_ms / self._anim_step

    def update_dwell(self, cursor_xy, text_regions, centre_x, centre_y):
        """Update gaze state each frame."""
        if cursor_xy is None:
            self._reset_gaze_state()
            return

        hovered = self._hit_test(cursor_xy, centre_x, centre_y, text_regions)
        if hovered is not None:
            self._state.gazing_at_text = True
            self._state.hovered_region = hovered
            self._state.last_gaze_lost_at = 0.0
            self._state.dwell_progress = min(
                1.0, self._state.dwell_progress + 1.0 / self._dwell_steps
            )
            if self._state.dwell_progress >= 1.0:
                self._state.ready_to_activate = True
                self._state.ready_at = time.monotonic()
        else:
            if self._state.gazing_at_text:
                if self._state.ready_to_activate:
                    elapsed = (time.monotonic() - self._state.last_gaze_lost_at) * 1000
                    if elapsed > self._state.gaze_lost_debounce_ms:
                        self._state.ready_to_activate = False
                        self._state.dwell_progress = 0.0
                self._state.last_gaze_lost_at = time.monotonic()
            self._reset_gaze_state()

    def consume_ready(self) -> bool:
        """Consume the ready state. Returns True if was ready."""
        if not self._state.ready_to_activate:
            return False
        self._state.ready_to_activate = False
        self._state.dwell_progress = 0.0
        return True

    def _hit_test(self, cursor_xy, cx, cy, regions):
        for region in regions:
            sx = cx - 400 + region.x  # TEXT_SELECTOR_WIDTH // 2
            sy = cy - 300 + region.y  # TEXT_SELECTOR_HEIGHT // 2
            if (sx <= cursor_xy[0] < sx + region.width and
                    sy <= cursor_xy[1] < sy + region.height):
                return region
        return None

    def _reset_gaze_state(self):
        self._state.gazing_at_text = False
        self._state.hovered_region = None
        self._state.dwell_progress = 0.0
```

### 2. Integrar en main.py

```python
from .voice import DictationIntentDetector

# En run_system():
dictation_intent = DictationIntentDetector()

# En tick():
# 1. Actualizar detector con regiones del gaze_text_sel
if gaze_text_sel.visible and gaze_text_sel._state.regions:
    dictation_intent.update_dwell(
        result.cursor_xy,
        gaze_text_sel._state.regions,
        gaze_text_sel._state.centre_x,
        gaze_text_sel._state.centre_y,
    )

# 2. Check voice trigger while gazing
if (voice_listener and not dictation_active
        and dictation_intent.ready_to_activate
        and dictation_intent.gazing_at_text):
    for cmd_text in voice_actions_this_frame:
        if cmd_text in {"gaze_typing", "escribir", "escribir_texto", "start_dictation"}:
            dictation_intent.consume_ready()
            dictation_engine.start()
            dictation_active = True
            overlay.set_dictation_indicator(True, "dictando")
            break
```

### 3. Feedback visual en overlay

```python
# En GazeOverlay.__init__():
self._dictation_active = False
self._dictation_text = ""

# En paintEvent():
if self._dictation_active:
    # Pulsing ring around cursor
    pulse = 0.5 + 0.5 * abs(QTime.currentTime().msec() % 1000 - 500) / 500.0
    pen = QPen(QColor(PALETTE.orange).lighter(115 + int(pulse * 40)), 3)
    pen.setCosmetic(True)
    p.setPen(pen)
    p.drawEllipse(x - 28, y - 28, 56, 56)

    # Badge in top-right
    if self._dictation_active:
        badge_rect = QRect(self.width() - 170, 20, 150, 36)
        p.drawRoundedRect(badge_rect, 18, 18)
        p.drawText(badge_rect, Qt.AlignCenter, f"🎙 {self._dictation_text}")

def set_dictation_indicator(self, active: bool, text: str = ""):
    self._dictation_active = active
    self._dictation_text = text
    self.update()
```

## Variables clave

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `dwell_ms` | int | Tiempo de mirada antes de estar "listo" (default 500ms) |
| `gaze_lost_debounce_ms` | float | Ventana de debounce al perder el cursor (default 300ms) |
| `ready_to_activate` | bool | True cuando dwell completado sobre región de texto |
| `gazing_at_text` | bool | True cuando el cursor está sobre una región de texto |
| `consume_ready()` | bool | Consume el estado ready, resetea dwell. True si estaba listo |

## Trigger phrases

Las frases de activación multimodal comparten las mismas que el voice listener:
- `"gaze_typing"`, `"escribir"`, `"escribir_texto"`, `"start_dictation"`

## Pitfalls

1. **Hit-test usa offsets fijos** — `cx - 400` y `cy - 300` asumen `TEXT_SELECTOR_WIDTH=800, HEIGHT=600`. Si cambias el tamaño del overlay, actualiza los offsets.
2. **Regiones de texto son relativas al centro del overlay** — Las coordenadas de `TextRegion` son relativas al centro, no a la esquina superior izquierda.
3. **No confundir con `gaze_text_sel`** — El detector de intención funciona INDEPENDIENTEMENTE de si el `gaze_text_sel` está abierto o no. Solo necesita las regiones de texto.
4. **Debounce necesario** — Sin debounce, el usuario puede perder el cursor brevemente (glitch de MediaPipe) y perder el estado "ready", causando frustración.
5. **El detector se resetea cuando el dictado está activo** — Cuando `dictation_active=True`, el detector se resetea para no interferir con la transcripción continua.
