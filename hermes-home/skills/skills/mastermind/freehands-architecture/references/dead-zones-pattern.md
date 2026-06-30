# Dead Zones — Patrón de implementación

**Fecha:** 2026-05-29  
**Mejora:** #2 del pipeline 9009  
**Archivo:** `src/freehands/gaze/dead_zones.py`

## Problema

Las coordenadas del gaze pueden alcanzar los bordes extremos de pantalla (0,0), (width,height), donde:
- El cursor se sale de zona útil
- Se activan hotspots del SO (taskbar Windows, menú macOS)
- Los ruidos de detección causan movimientos bruscos

## Solución

Clamper de coordenadas configurable por porcentaje:

```python
from freehands.gaze.dead_zones import DeadZoneClamper, DeadZoneConfig

# 5% de margen en cada lado, mínimo 40px
clamper = DeadZoneClamper(screen_width=1920, screen_height=1080)
cursor = clamper.clamp((0, 0))  # → (96, 54) en vez de (0, 0)

# Configurable: 10% de margen
config = DeadZoneConfig(edge_margin_pct=0.10)
clamper = DeadZoneClamper(1920, 1080, config=config)

# Reutilizable: update_screen para multi-monitor
clamper.update_screen(3840, 2160)
```

## Integración en main.py

El clamper se aplica **antes** del FineAimPointer:

```python
# En run_system():
dead_zone = DeadZoneClamper(screen.width(), screen.height())

# En tick():
cursor = regressor.predict(feats.vector) if feats else None
if cursor is not None and fusion.sm.state != State.IDLE:
    cursor = dead_zone.clamp(cursor)  # ← antes de fine_aim
    cursor = fine_aim.update(cursor)
```

## Tests

`tests/test_dead_zones.py` cubre:
- Clamping en bordes (mín/máx)
- Coordenadas centrales sin modificar
- Configuración de porcentaje
- Validación de parámetros inválidos
- Re-computación con update_screen
- Margen mínimo en pantallas pequeñas
- Validación de integración en main.py