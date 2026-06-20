# Patrón: Estimación 6DoF Head Pose desde MediaPipe FaceMesh

Implementado en mejora #17 del pipeline 9009 FreeHands. Módulo `gaze/head_pose.py`.

## Problema

MediaPipe FaceMesh proporciona 468 landmarks faciales. Necesitamos extraer rotación de cabeza (yaw, pitch, roll) para usar como canal "coarse" de desplazamiento en la fusión multimodal, complementando el pointer "fine" del gaze tracker.

## Algoritmo

### Yaw (rotación izquierda/derecha)
Usar vector nariz-ojo en plano XZ:
```
dx = nose_x - eye_center_x  (eje X en imagen)
dz = nose_z - eye_center_z  (profundidad)
yaw = atan2(dx, dz)
```
**Pitfall**: El cross-product approach falla en rostros neutros porque el denominador se acerca a cero. `arctan2` es más estable porque maneja todos los cuadrantes.

### Pitch (rotación arriba/abajo)
Usar eje frente-mentón relativo a línea horizontal ojo:
```
forehead_y = promedio de landmarks frente superior
chin_y = promedio de landmarks mentón
eye_y = promedio de landmarks ojos
pitch = atan2(forehead_y - chin_y, eye_y - chin_y)
```
**Pitfall crítico**: Usar el vector nariz-mentón para pitch **falla en neutral** porque la nariz está anatómicamente por debajo de los ojos, causando falsos positivos de pitch-up en pose neutral. La solución es usar el eje frente-mentón (que pasa por el centro del rostro) relativo a la línea horizontal ojo.

### Roll (inclinación lateral)
Inclinación de la línea ojo-ojo respecto al horizontal de la imagen.

## Integración en fusión

El head pose se aplica como desplazamiento "coarse" en `MultimodalFusion.step()`:
- `head_pose.coarse_active` determina si se aplica desplazamiento
- Dead zone de ±5° para evitar jitter en pose neutral
- `coarse_dx`, `coarse_dy` clamped a `MAX_PAN_FRACTION` (0.5) y `MAX_TILT_FRACTION` (0.4)
- El gaze fine pointer sigue siendo la modalidad primaria para precisión

## Testing

Tests unitarios en `tests/test_head_pose.py` cubren:
- Rostro neutral → yaw/pitch/roll ≈ 0
- Yaw izquierda/derecha → valores positivos/negativos
- Pitch arriba/abajo → valores positivos/negativos
- Roll lateral → valores positivos/negativos
- Dead zone clamping
- Clamping de pantalla
- Escalado a píxeles

## Referencias cruzadas

- `src/freehands/gaze/head_pose.py` — implementación
- `src/freehands/gaze/tracker.py` — integración en GazeFeatures
- `src/freehands/fusion/fusion.py` — aplicación coarse displacement
- `tests/test_head_pose.py` — tests unitarios
