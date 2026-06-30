# Patrón de mejora: Overlay transparente PyQt6

Implementado como mejora #12 del pipeline 9009 (30/05/2026).

## Resumen

Mejora de `GazeOverlay` para funcionar como overlay transparente real sobre el escritorio: halo radial de profundidad, anillo de posición, soporte multi-monitor y pens cosméticos para consistencia visual.

## Archivos modificados

| Archivo | Acción |
|---------|--------|
| `src/freehands/ui/overlay.py` | **Modificado** — `GazeOverlay` mejorado |
| `src/freehands/ui/__init__.py` | **Modificado** — Exporta `GazeOverlay` |

## Cambios clave en GazeOverlay

### 1. Halo radial de profundidad
```python
halo = QtGui.QRadialGradient(x, y, 32)
halo.setColorAt(0, QtGui.QColor(PALETTE.blue).rgba64())
halo.setColorAt(0.3, halo_color)  # alpha=25
halo.setColorAt(1, QtGui.QColor(0, 0, 0, 0).rgba64())
p.setBrush(QtGui.QBrush(halo))
p.drawEllipse(QtCore.QRect(x - 32, y - 32, 64, 64))
```
Gradiente radial azul de 64px que ayuda a percibir la posición del cursor sobre cualquier fondo.

### 2. Anillo de posición exterior
```python
ring_pen = QtGui.QPen(QtGui.QColor(PALETTE.blue).lighter(115), 2)
ring_pen.setCosmetic(True)
p.drawEllipse(QtCore.QPoint(x, y), 14, 14)
```
Borde fino exterior para referencia de posición exacta.

### 3. Soporte multi-monitor
```python
screen_changed_conn = QtWidgets.QApplication.instance().screenChanged
if screen_changed_conn is not None:
    screen_changed_conn.connect(self._on_screen_changed)

def _on_screen_changed(self, screen: QtWidgets.QScreen) -> None:
    self.setGeometry(screen.geometry())
    self.update()
```
Reposiciona automáticamente si se detecta un nuevo monitor.

### 4. Flags Qt adicionales
```python
self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)
self.setWindowOpacity(0.92)
```
`WA_NoSystemBackground` evita parpadeos. `setWindowOpacity(0.92)` da integración visual.

### 5. Pens cosméticos
Todos los pens de dibujo (dwell ring, snap ring, border ring) usan `setCosmetic(True)` para mantener tamaño consistente a cualquier DPI/resolución.

## Pitfalls

1. **`setCosmetic(True)` es necesario** en pens de overlay — sin él, el tamaño del trazo varía con la resolución de pantalla.
2. **`WA_NoSystemBackground`** evita artefactos visuales al redibujar — el overlay no debe heredar el fondo del sistema.
3. **`screenChanged` signal puede ser `None`** en algunos entornos (sin X11/Wayland completo) — siempre verificar con `is not None`.
4. **`rgba64()` para gradientes** — `QColor.rgba64()` es más preciso que `setAlpha()` para gradientes radiales.
5. **No olvidar exportar en `__init__.py`** — si la clase no se exporta, `main.py` no puede importarla limpiamente.

## Verificación post-implementación

```python
# Syntax check (sandbox no tiene PyQt6)
import ast
ast.parse(open('src/freehands/ui/overlay.py').read())

# Import test (si PyQt6 está disponible)
from freehands.ui import GazeOverlay  # debe importar sin error
```
