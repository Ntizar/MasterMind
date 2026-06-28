# Patrón de integración: Menú OSD Radial

Implementado como mejora #10 del pipeline 9009 (30/05/2026).

## Resumen

Widget PyQt6 translúcido que muestra 8 acciones en disposición circular. Se abre con palm-hold sostenido (1.5s) y se cierra con dwell en un sector o al pausar el sistema.

## Archivos creados/modificados

| Archivo | Acción |
|---------|--------|
| `src/freehands/ui/radial_menu.py` | **Creado** — Widget completo (~370 líneas) |
| `src/freehands/ui/__init__.py` | **Modificado** — Exporta nuevas clases |
| `src/freehands/main.py` | **Modificado** — Integración en pipeline |

## Clases principales

### `RadialMenuWidget`
```python
class RadialMenuWidget(QtWidgets.QWidget):
    action_selected = pyqtSignal(str)  # action_id emitido al confirmar
    
    def open_at(self, x: int, y: int) -> None  # Abre menú en posición
    def close(self) -> None                     # Cierra con animación
    def update_dwell(self, cursor_xy: tuple[int, int] | None) -> None  # Actualiza dwell por sector
    def set_actions(self, actions: list[RadialAction]) -> None  # Personaliza acciones
```

### `RadialAction`
```python
@dataclass(frozen=True)
class RadialAction:
    action_id: str    # coincide con dispatcher ACTIONS
    label: str        # texto visible
    icon: str         # emoji/icono
    color: str        # color de acento
```

## Lógica de integración en main.py

### Trigger de apertura
```python
# Track open-palm hold frames
if confirmed in {"left_open_palm", "right_open_palm", ...}:
    radial_menu_open_hold_frames += 1
    if radial_menu_open_hold_frames >= frames_needed:
        radial_menu.open_at(cursor_x, cursor_y)
```

### Cierre automático
- Estado IDLE → `radial_menu.close()`
- Segundo palm-hold → se ejecuta toggle_pause, menú se cierra implícitamente
- Cursor fuera de sectores → dwell reset

### Hit-test angular
- 8 sectores de 45° cada uno
- Tolerancia ±22° por sector
- Distancia mínima al centro: `MENU_RADIUS - MENU_ITEM_RADIUS - 10`
- Distancia máxima: `MENU_RADIUS + MENU_ITEM_RADIUS + 10`

## Constantes clave

| Constante | Valor | Significado |
|-----------|-------|-------------|
| `MENU_RADIUS` | 140px | Radio del menú |
| `MENU_ITEM_RADIUS` | 36px | Radio de cada icono |
| `MENU_DWELL_MS` | 400ms | Tiempo para confirmar acción |
| `MENU_OPEN_DURATION_MS` | 1500ms | Hold palm para abrir |
| `MENU_ANIM_DURATION_MS` | 250ms | Duración animación |
| `MENU_MAX_ACTIONS` | 8 | Máximo acciones visibles |
| `SECTOR_TOLERANCE` | 22° | Tolerancia hit-test |

## Pitfalls detectados

1. **No usar walrus operator en lambda de signal** — `result` no está definido en scope de conexión. Usar función named en su lugar.
2. **Importar constantes desde el módulo, no copiarlas** — `MENU_OPEN_DURATION_MS` se importa de `radial_menu` a `main.py`, no se redefine.
3. **`nonlocal` obligatorio** — Las variables de hold frames y gesture deben ser `nonlocal` en `tick()` para poder modificarlas.
4. **Cierre en IDLE** — El menú debe cerrarse también cuando el estado va a IDLE, no solo cuando se confirma una acción.

## Acciones por defecto

1. Click (azul)
2. Right click (naranja)
3. Double click (azul)
4. Scroll up (verde)
5. Scroll down (amarillo)
6. Zoom in (azul suave)
7. Zoom out (naranja suave)
8. Escape (rojo)
