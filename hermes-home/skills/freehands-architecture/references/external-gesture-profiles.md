# Perfiles de gestos externos JSON — FreeHands

Implementado en mejora #6 del pipeline 9009 (29/05/2026).

## Estructura

Los perfiles de gestos externos viven en `src/freehands/profiles/gesture_profiles/` como archivos `.json`.

Cada perfil contiene:
- `gesture_bindings`: dict → `{gesture: action}` (override total sobre defaults)
- `gesture_thresholds`: dict → `{gesture: {stability_frames: N, confidence_min: F}}` (merge por campo)

## API

```python
from freehands.profiles import (
    load_gesture_profile,    # Carga un perfil JSON por nombre
    merge_gesture_profile,   # Aplica overrides sobre Profile (in-place)
    list_gesture_profiles,   # Lista nombres disponibles
    gesture_profiles_dir,    # Path al directorio
    GestureProfileOverride,  # Modelo Pydantic del formato
)
```

## Pitfall crítico: `_repair_essential_bindings` sobrescribe bindings

**Problema:** La función `_repair_essential_bindings()` reasigna `pointing_up = "click"`, `middle_up = "right_click"`, etc. si no detecta acciones de click en ningún gesture detectable. Esto destruye bindings personalizados del perfil externo.

**Solución:** `merge_gesture_profile()` pasa un set `explicit_gestures` (gestos del perfil externo) a `_repair_essential_bindings()`, que respeta esos bindings y no los sobreescribe.

```python
# En _repair_essential_bindings():
def _repair_essential_bindings(
    bindings, detectable_gestures,
    explicit_gestures: set[str] | None = None,  # <-- nuevo
) -> None:
    explicit_gestures = explicit_gestures or set()
    # ...
    elif not _has_detectable_action(bindings, detectable_gestures, action):
        if generic_gesture not in explicit_gestures:  # <-- respeta externos
            bindings[generic_gesture] = action
```

**Regla:** Nunca llamar a `_repair_essential_bindings()` sin `explicit_gestures` cuando se aplica un perfil externo.

## Ejemplos

- `gaming.json` — Alta sensibilidad, reload, switch_weapon
- `accessibility.json` — Máxima estabilidad, gestos amplios

## Tests

`tests/test_gesture_profiles.py` — 12 tests unitarios cubriendo carga, merge, invariants, partial override.
