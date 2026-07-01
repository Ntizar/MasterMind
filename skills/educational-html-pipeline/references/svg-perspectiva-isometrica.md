# SVG — Perspectiva Isométrica: Ejes

## Patrón para b03-01 (ejes isométricos)

### Estructura del SVG
- **Viewport:** `viewBox="0 0 600 450"`
- **Origen O:** centro del SVG (300, 350) — desplazado abajo para dar espacio a etiquetas y ángulos
- **Línea horizontal de referencia:** punteada, para mostrar el 0° de referencia y los 30°

### Los tres ejes (colores corregidos 2026-06-10)
| Eje | Dirección | Color | Coordenadas (origen→extremo) |
|-----|-----------|-------|------------------------------|
| Z | Vertical arriba | `#10b981` (verde) | (300,350) → (300,60) |
| X | 30° abajo-derecha | `#f97316` (naranja) | (300,350) → (520,463) |
| Y | 30° abajo-izquierda | `#2563eb` (azul) | (300,350) → (80,463) |

> **Nota:** Z en verde (altura = crecimiento), X en naranja (longitud), Y en azul (anchura). Más intuitivo que el esquema anterior.

### Marcadores de flecha
```xml
<marker id="arrowZ" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
  <polygon points="0 0, 10 3.5, 0 7" fill="#10b981"/>
</marker>
```
Repetir para X (`#f97316`) e Y (`#2563eb`).

### Arcos de ángulo
- **120° entre ejes:** usar `A` (arc) con radio 60 para los tres pares, color `#a855f7` (púrpura)
- **30° de referencia:** línea punteada horizontal + arco pequeño para mostrar el ángulo con la horizontal
- Los tres arcos de 120° deben ser visibles y etiquetados

### Cubo de referencia
- Dibujado con `opacity="0.15"` como guía visual sutil
- Aristas paralelas a los tres ejes desde un punto intermedio
- Muestra cómo se proyectan las tres caras del cubo

### Cuadrícula isométrica de fondo
- Usar `<pattern>` SVG para patrón repetible
- Líneas sutiles (`stroke="#e2e8f0" stroke-width="0.5" opacity="0.4"`)
- Patrón con tres familias de líneas paralelas a cada eje
- Solo decorativas, no interfieren con los ejes principales

### Etiquetas
- **Ejes:** letra grande (22px) + negrita + color del eje + posición en extremo
- **Magnitudes:** texto pequeño (13px) junto a cada eje (altura, longitud, anchura)
- **Origen:** "O" en negrita junto al punto de intersección
- **Ángulos:** 120° en púrpura entre cada par de ejes, 30° en color del eje correspondiente

### Leyenda
- `<rect>` con fondo blanco y borde sutil en esquina superior izquierda
- Muestra los tres ejes con sus colores y descripciones
- Incluye nota "3 ejes = 3 × 120°"
