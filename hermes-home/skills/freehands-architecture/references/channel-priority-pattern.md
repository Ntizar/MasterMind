# Channel Priority — Patrón de priorización dinámica de canales

## Problema

En un sistema multimodal (gesto + voz + mirada), cuando dos canales proponen
acciones diferentes en el mismo frame, no hay un mecanismo para decidir cuál
ejecutar. Sin priorización, los dos se ejecutarían en secuencia causando
comportamiento inesperado (ej: clic + subir volumen simultáneamente).

## Solución

Módulo `fusion/channel_priority.py` que implementa reglas de prioridad basadas
en la **naturaleza de la acción**, no en la confianza del sensor.

## Reglas de prioridad

### 1. Comandos de sistema → voz siempre gana
```
volume_up, volume_down, volume_mute, screenshot, show_desktop
```
Estos no tienen contrapartida gestual y son controles de seguridad. La voz
es el canal intencional para ellos.

### 2. Acciones idénticas en ambos canales → gesto gana
```
decide_channel_priority("click", "click") → ("click", "gesture")
```
El gesto es la modalidad primaria de FreeHands. Si ambos canales coinciden,
se ejecuta una sola vez con origen "gesture".

### 3. Acciones diferentes no-sistema → gesto gana
```
decide_channel_priority("click", "zoom_in") → ("click", "gesture")
```
El gesto lleva contexto espacial (dónde en pantalla quiere actuar el usuario).
La voz no tiene esa información.

## Implementación

### Dataclass `ChannelDecision`
```python
@dataclass(frozen=True)
class ChannelDecision:
    action: str | None          # acción a ejecutar (o None)
    source: str | None          # "gesture", "voice", o None
    gesture_confidence: float = 1.0
    voice_confidence: float = 1.0
```

### Función principal `decide_channel_priority()`
```python
def decide_channel_priority(
    gesture_action: str | None,
    voice_action: str | None,
    *,
    gesture_confidence: float = 1.0,
    voice_confidence: float = 1.0,
) -> ChannelDecision:
```

### Función auxiliar `voice_should_bypass_fusion()`
```python
def voice_should_bypass_fusion(action: str | None) -> bool:
    """True si la acción de voz bypassa el state machine de fusión."""
    return action in SYSTEM_ACTIONS or action in STATE_ACTIONS
```

## Integración en main.py

En el bucle `tick()`, después de ejecutar la acción de gesto:

1. Drain voice commands pendientes
2. Comandos de sistema y estado (pause/resume) → ya manejados por `handle_voice_action()`
3. Para acciones regulares:
   - Si gesture_action y voice_action diferentes → llamar `decide_channel_priority()`
   - Si voice gana → ejecutar override con flash "voice: X (priority)"
   - Si gesture gana → ya ejecutado arriba, ignorar
   - Si no hay gesture_action → voice action rellena el hueco

## Categorías de acciones

```python
SYSTEM_ACTIONS = {"show_desktop", "screenshot",
                  "volume_up", "volume_down", "volume_mute"}

POINTER_ACTIONS = {"click", "right_click", "double_click", "undo"}

GESTURE_ACTIONS = {"scroll_up", "scroll_down", "zoom_in", "zoom_out"}

STATE_ACTIONS = {"toggle_pause", "resume"}
```

## Tests

20 tests unitarios en `tests/test_channel_priority.py`:
- 3 tests de "no conflicto" (ambos None, solo gesto, solo voz)
- 2 tests de "misma acción" (gesto gana)
- 5 tests de "comandos de sistema" (voz gana)
- 4 tests de "acciones regulares" (gesto gana)
- 2 tests de "confianza" (passthrough)
- 4 tests de `voice_should_bypass_fusion()`

## Pitfalls

1. **No duplicar ejecución**: los comandos de sistema y estado se manejan en
   `handle_voice_action()` antes del bloque de prioridad. El bloque de
   prioridad solo gestiona acciones regulares no manejadas.

2. **Type safety**: `decision.action` es `str | None`. Siempre verificar
   `if decision.action` antes de llamar `dispatcher.execute()`.

3. **Drain queues**: `drain_commands()` consume TODOS los comandos pendientes
   en una llamada. No hay reintentos. Si hay múltiples comandos de voz en
   el mismo frame, se procesan todos.

4. **Confianza no es criterio de desempate**: las reglas se basan en la
   categoría de acción, no en la confianza. La confianza se pasa como metadata
   para logging/debugging, no para decisión.
