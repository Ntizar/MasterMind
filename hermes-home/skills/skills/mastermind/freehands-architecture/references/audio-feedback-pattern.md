# Audio Feedback Pattern — FreeHands

Patrón para añadir feedback auditivo de confirmación en FreeHands.

## Cuándo usar
- Cualquier evento que merezca confirmación al usuario: gesto confirmado, comando de voz, error.
- El usuario no tiene auriculares, así que el audio es el feedback primario.

## Implementación

### 1. Crear el módulo `src/freehands/ui/audio_feedback.py`

```python
"""Minimal audio feedback for gesture and voice confirmation."""
from __future__ import annotations
import time
from dataclasses import dataclass, field

@dataclass
class AudioFeedback:
    enabled: bool = True
    _last_beep_at: float = field(default=0.0, repr=False)
    _min_interval_ms: int = 80  # debounce

    def play_gesture_confirmation(self) -> None:
        if not self.enabled: return
        self._beep(1200, 40)  # agudo, corto

    def play_voice_confirmation(self) -> None:
        if not self.enabled: return
        self._beep(800, 50)   # grave, medio

    def play_error(self) -> None:
        if not self.enabled: return
        self._beep(400, 60)
        time.sleep(0.08)
        self._beep(400, 60)

    def _beep(self, frequency: int, duration_ms: int) -> None:
        now = time.monotonic()
        if now - self._last_beep_at < self._min_interval_ms / 1000:
            return
        self._last_beep_at = now
        try:
            import winsound
            winsound.Beep(frequency, duration_ms)
        except ImportError:
            pass  # no-op en Linux/Mac
```

### 2. Exponer en `ui/__init__.py`

```python
from .audio_feedback import AudioFeedback
```

### 3. Añadir campo al Profile (`profiles/store.py`)

```python
audio_feedback_enabled: bool = True
```

### 4. Integrar en `main.py`

```python
from .ui.audio_feedback import AudioFeedback

# En run_system(), tras crear dispatcher:
audio_feedback = AudioFeedback(enabled=profile.audio_feedback_enabled)

# En tick(), tras ejecutar acción de gesto:
if result.fired_action and result.fired_action not in {"toggle_pause", "resume"}:
    dispatcher.execute(result.fired_action, at_xy=click_xy)
    audio_feedback.play_gesture_confirmation()

# En tick(), tras procesar comando de voz:
for cmd in voice_listener.drain_commands():
    handle_voice_action(cmd.action, result.cursor_xy)
    audio_feedback.play_voice_confirmation()
```

## Notas
- `winsound` es nativo de Windows. En Linux/Mac se silencia silenciosamente.
- Debounce de 80ms para evitar spam en acciones rápidas.
- Dos tonos diferenciados: agudo (gesto) vs grave (voz) — permite al usuario distinguir el origen del feedback sin mirar.