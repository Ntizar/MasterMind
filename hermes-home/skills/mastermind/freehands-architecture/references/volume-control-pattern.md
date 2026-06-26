# Patrón de control de volumen por posición Y de mano

## Resumen

Detector de volumen basado en la posición vertical (eje Y normalizado) del centroid de la mano en el frame de la cámara. Es un **gesto estático de posición** — distinto de palm-scroll (motion-based) y de expresiones faciales (state-based).

## Diferencias con otros gestos

| Tipo | Ejemplo | Base | Requiere movimiento | Requiere pose específica |
|------|---------|------|---------------------|--------------------------|
| Pose estática | `open_palm`, `pointing_up` | Forma de dedos | No | Sí |
| Motion-based | `palm_scroll_up`, `air_scroll` | Cambio de posición | Sí | No (cualquier pose) |
| **Posición de zona** | `volume_up`, `volume_down` | **Zona del frame** | **No** | **No** |
| State-based | `smile`, `surprise` | Expresión facial | No | Sí |

El control de volumen es único: no depende de la forma de la mano ni de su movimiento — solo de **dónde está** en el frame.

## Implementación

### 1. Módulo `gestures/volume_control.py`

```python
class VolumeControl:
    """Detecta volumen_arriba / volumen_abajo según posición Y de la mano.

    Zonas (Y normalizado 0=topo, 1=abajo):
      - Y < 0.35  → volume_up
      - Y > 0.65  → volume_down
      - 0.35..0.65 → neutral

    Cooldown: 15 frames (~0.5s a 30fps) para evitar disparos continuos.
    """
```

**Puntos clave:**
- Usa el centroid (promedio de los 21 landmarks) en lugar de la muñeca sola → más estable
- Tracking por índice de mano (`dict[int, float]`) para soportar dos manos
- Cooldown por mano para evitar ráfagas
- Detecta desde el primer frame (no necesita frame previo para comparar)
- Reset cuando la mano se pierde

### 2. Integración en `main.py`

```python
# Instanciación en run_system()
volume_control = VolumeControl()

# En el loop tick(), después del bloque facial y antes de la fusión
volume_obs = volume_control.detect(
    hand_obs.hands,
    hand_obs.handedness,
    hand_obs.confidence,
)
if volume_obs.gesture and fusion.sm.state != State.IDLE:
    if dispatcher.execute(volume_obs.gesture, at_xy=cursor):
        overlay.flash_action(f"volumen: {volume_obs.gesture}")
        panel.set_last_action(f"volumen: {volume_obs.gesture}")
        audio_feedback.play_gesture_confirmation()
    if not hand_obs.hands:
        volume_control.reset()
```

**Importante:** No usa gesture bindings — ejecuta directamente vía dispatcher. Esto permite que funcione siempre que haya una mano visible, sin necesidad de configurar bindings en el perfil.

### 3. Registro en `profiles/store.py`

Añadir a las tres listas de gestos:

```python
GESTURE_BINDING_PRIORITY = [
    # ... existentes ...
    "volume_up",
    "volume_down",
]

INSTANT_MOUSE_GESTURES = (
    # ... existentes ...
    "volume_up",
    "volume_down",
)

# En Profile.gesture_thresholds:
"volume_up": GestureThreshold(stability_frames=1, confidence_min=0.50),
"volume_down": GestureThreshold(stability_frames=1, confidence_min=0.50),

# En Profile.gesture_bindings:
"volume_up": "",
"volume_down": "",
```

`INSTANT_MOUSE_GESTURES` es obligatorio: `_repair_instant_mouse_thresholds()` ajusta automáticamente los thresholds de gestos en esta lista.

## Umbrales recomendados

| Parámetro | Valor | Razón |
|-----------|-------|-------|
| `VOLUME_UP_THRESHOLD` | 0.35 | Zona superior del frame |
| `VOLUME_DOWN_THRESHOLD` | 0.65 | Zona inferior del frame |
| `VOLUME_COOLDOWN_FRAMES` | 15 | ~0.5s a 30fps, evita rampa continua |
| `VOLUME_MIN_CONFIDENCE` | 0.60 | Umbral mínimo de detección de mano |

Ajustar según la distancia del usuario a la cámara y el tamaño del frame.

## Pitfalls

- **No usar `gesture_bindings`**: El control de volumen se ejecuta directamente con `dispatcher.execute()`, no a través de `action_for_gesture()`. Esto permite que funcione siempre que haya una mano visible, sin configuración de perfiles.
- **Reset cuando se pierde la mano**: Si no se llama `volume_control.reset()` cuando `hand_obs.hands` está vacío, el detector mantiene el último estado y puede disparar acciones fantasma.
- **Cooldown necesario**: Sin cooldown, el volumen sube/baja continuamente mientras la mano se mantiene en la zona. 15 frames (~0.5s) da un paso por cada medio segundo.
- **Centroid vs muñeca**: Usar el centroid (promedio de los 21 landmarks) es más estable que usar solo la muñeca, que puede tener más jitter.

## Referencias cruzadas

- `freehands-architecture` — arquitectura general del proyecto
- `freehands-integration-pattern` — patrón de integración de componentes en pipeline principal
- `air-scroll-pattern` — otro gesto basado en posición, pero motion-based (requiere movimiento)
