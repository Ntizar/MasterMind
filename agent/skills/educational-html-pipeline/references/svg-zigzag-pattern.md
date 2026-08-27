# Patrón SVG Zigzag Animado — Corte Escalonado

## Uso

Para SVGs de corte escalonado (Dibujo Técnico, Bachillerato): línea de corte en zigzag con animación draw + pulsación al interactuar.

## CSS Keyframes

```css
@keyframes draw-line{from{stroke-dashoffset:500}to{stroke-dashoffset:0}}
@keyframes zigzag-pulse{0%{stroke-width:2.5}50%{stroke-width:5}100%{stroke-width:2.5}}
.animate{stroke-dasharray:500;stroke-dashoffset:500;animation:draw-line 2s ease-out forwards}
.zig-active{animation:zigzag-pulse 1s ease-in-out 3}
```

## SVG

```html
<g id="zigzag-line" onclick="toggleZigzag()" style="cursor:pointer">
<line x1="60" y1="70" x2="60" y2="100" stroke="#ef4444" stroke-width="2.5" class="zig-seg animate"/>
<!-- ... más segmentos ... -->
</g>
<!-- Puntos de cambio pulsantes -->
<circle cx="60" cy="100" r="4" fill="#f97316" class="pulse"/>
```

## JS

```js
var zigzagActive = false;
function toggleZigzag() {
  var segs = document.querySelectorAll('.zig-seg');
  zigzagActive = !zigzagActive;
  segs.forEach(function(s) {
    if (zigzagActive) {
      s.setAttribute('stroke-width', '4');
      s.setAttribute('stroke', '#a855f7');
      s.classList.add('zig-active');
      s.style.animation = 'none'; s.offsetHeight; s.style.animation = '';
    } else {
      s.setAttribute('stroke-width', '2.5');
      s.setAttribute('stroke', '#ef4444');
      s.classList.remove('zig-active');
    }
  });
}
```

## Re-trigger animación

Siempre usar el patrón `style.animation = 'none'; g.offsetHeight; g.style.animation = ''` para re-trigger CSS animations en cada interacción.
