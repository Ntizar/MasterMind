# Patrón: Teclado Virtual Dual-Layout por Ojos

Implementado en FreeHands como mejora #22.

## Concepto

Dividir el teclado virtual en dos mitades (izquierda/derecha) y mostrar solo la mitad correspondiente al lado de la pantalla donde está el cursor de mirada. Esto reduce el espacio de búsqueda a la mitad, acelerando la selección de teclas.

## Implementación

### 1. Clase `LayoutSide` (enum)

```python
class LayoutSide(Enum):
    BOTH = auto()    # teclado completo
    LEFT = auto()    # solo mitad izquierda
    RIGHT = auto()   # solo mitad derecha
```

### 2. Marcado de teclas izquierda/derecha

Al construir las teclas en `_build_keys()`, cada una recibe `is_left_key: bool`:

```python
half_pos = len(row) // 2
is_left = col_idx < half_pos
```

### 3. Filtrado dinámico de teclas visibles

```python
def get_visible_keys(self) -> list[KeyDefinition]:
    if not self._dual_layout or self._state.layout_side == LayoutSide.BOTH:
        return self._state.keys
    side = self._state.layout_side
    return [k for k in self._state.keys if k.is_left_key == (side == LayoutSide.LEFT)]
```

### 4. Detección de lado por posición del cursor

```python
def update_layout_side(self, cursor_x: int | None) -> None:
    if not self._dual_layout or cursor_x is None:
        self._state.layout_side = LayoutSide.BOTH
        return
    centre = self._screen_width // 2
    tolerance = self._screen_width // 10  # 10% como zona centro
    if abs(cursor_x - centre) <= tolerance:
        new_side = LayoutSide.BOTH
    elif cursor_x < centre:
        new_side = LayoutSide.LEFT
    else:
        new_side = LayoutSide.RIGHT
    if self._state.layout_side != new_side:
        self._state.layout_side = new_side
        self.layout_changed.emit(side_name)
```

### 5. Integración en `main.py`

```python
# Crear con dual_layout=True
virtual_kb = VirtualKeyboardWidget(dual_layout=True)

# Conectar signal para feedback
def on_kb_layout_changed(side: str) -> None:
    audio_feedback.play_gesture_confirmation()
    overlay.flash_action(f"teclado: lado {side}")

virtual_kb.layout_changed.connect(on_kb_layout_changed)

# En tick():
virtual_kb.update_dwell(result.cursor_xy)  # actualiza layout automáticamente
```

## Patrón extensible

Este patrón de "split view basado en posición" es reutilizable para cualquier widget que tenga regiones izquierda/derecha:
- Menús de contexto (izq = acciones principales, der = secundarias)
- Paneles de configuración (izq = categorías, der = opciones)
- Visualizaciones de datos (izq = serie A, der = serie B)

## Archivos modificados en FreeHands

- `src/freehands/ui/virtual_keyboard.py` — lógica principal
- `src/freehands/main.py` — integración con pipeline
