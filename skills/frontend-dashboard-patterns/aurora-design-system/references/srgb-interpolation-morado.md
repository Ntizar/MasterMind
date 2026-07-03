# sRGB Interpolation Morado — Fix Técnico

## Problema

CSS interpola gradientes en sRGB por defecto. Cuando se hace un gradient entre azul (`#2563eb` = rgb 37,99,235) y naranja (`#f97316` = rgb 249,115,22), el navegador calcula el punto medio como:

```
R: (37 + 249) / 2 = 143
G: (99 + 115) / 2 = 107
B: (235 + 22) / 2 = 128
→ rgb(143, 107, 128) = gris morado
```

Esto ocurre **aunque no haya ninguna parada violeta** en el gradient. El morado aparece por la interpolación lineal del navegador.

## Solución 1: Parada intermedia amarilla (si se debe usar gradient)

Añadir `orange-300` (`#fdba74` = rgb 253,186,116, que es amarillento) al 15-18%. Esto fuerza la interpolación a pasar por el amarillo:

```css
--nz-gradient-aurora: linear-gradient(135deg,
  var(--nz-color-brand) 0%,        /* azul */
  var(--nz-color-orange-300) 15%,  /* amarillento — fuerza ruta */
  var(--nz-color-orange-500) 50%,  /* naranja */
  var(--nz-color-orange-600) 100%); /* naranja profundo */
```

Ahora la interpolación azul→amarillo da `rgb(145,143,176)` (azul-grisáceo, no morado) y amarillo→naranja da `rgb(251,151,69)` (naranja claro, correcto).

## Solución 2: OKLCH interpolation (CSS Color Level 4)

```css
background: linear-gradient(in oklch to right, #2563eb, #f97316);
```

OKLCH interpola en un espacio perceptualmente uniforme. El camino azul→naranja pasa por el amarillo naturalmente. Soporte: Chrome 111+, Safari 16.4+, Firefox 113+.

## Solución 3 (PREFERIDA POR DAVID): No gradientes

David rechaza gradientes entre azul y naranja completamente. Usar:
- Colores sólidos en bloques
- Three.js para elementos visuales
- Separación clara entre colores (bordes, espacios)

## Chromatic edge del glass-liquid

El glass-liquid usa OKLCH para el chromatic edge:
```css
linear-gradient(135deg,
  oklch(85% 0.15 200) 0%,    /* cyan */
  oklch(85% 0.08 280) 50%,   /* ← VIOLETA */
  oklch(85% 0.15 340) 100%)  /* rosa */
```

Fix aplicado (2026-07-02): hue 280→250 (azul), 340→50 (naranja), con parada intermedia hue 80 (amarillo):
```css
linear-gradient(135deg,
  oklch(85% 0.15 200) 0%,
  oklch(85% 0.06 250) 30%,   /* azul, baja croma */
  oklch(85% 0.10 80) 60%,    /* amarillo */
  oklch(85% 0.15 50) 100%)   /* naranja */
```

## Archivos modificados (commit 57ab041)

- `ntizar.css:159` — gradient-aurora con 4 paradas
- `ntizar.css:860` — border-color brand-mix violet→brand-strong
- `ntizar.next.css:433-436` — chromatic edge light mode
- `ntizar.next.css:541-544` — chromatic edge dark mode
- `ntizar.themes.css:34-37` — skin aurora gradient
- `ntizar.themes.css:49` — skin sunset gradient
- `ntizar.viz.css:39` — aurora-bg
- `ntizar.viz.css:202` — orb--aurora
- `ntizar.viz.css:217` — glow-ring
- `ntizar.data.css:239` — meter--aurora
- `ntizar.charts.css:201` — donut--aurora
- `ntizar.themes.css:121` — chart-3 palette
