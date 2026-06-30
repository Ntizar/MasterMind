# Patrón SVG Interactivo — Ronda 2 (toggleHighlight)

## CSS

Añadir al `<style>` del archivo:

```css
.svg-element{transition:all .3s;cursor:pointer}
.svg-element:hover{filter:brightness(1.15) drop-shadow(0 0 4px rgba(37,99,235,.3))}
.svg-element.active{filter:brightness(1.2) drop-shadow(0 0 6px rgba(37,99,235,.5))}
.svg-pulse{animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.6}}
@keyframes drawLine{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}
.svg-draw{stroke-dasharray:1000;animation:drawLine 2s ease forwards}
```

## HTML

Añadir a elementos SVG clave:

```html
<line x1="..." x2="..." class="svg-element clickable"
      onclick="toggleHighlight(this)"
      data-info="Descripción del elemento"/>
<circle cx="..." cy="..." r="4" class="svg-element clickable"
        onclick="toggleHighlight(this)"
        data-info="Información del punto"/>
```

## JS

```javascript
var svgInfoPanel = null;
function toggleHighlight(el) {
  el.classList.toggle('active');
  var info = el.getAttribute('data-info');
  if (info) {
    if (!svgInfoPanel) {
      svgInfoPanel = document.createElement('div');
      svgInfoPanel.className = 'interactive';
      svgInfoPanel.style.marginTop = '1rem';
      svgInfoPanel.innerHTML = '<h3 id="svgInfoTitle">ℹ️ Info</h3>' +
        '<p id="svgInfoText" style="color:#64748b;margin:.5rem 0"></p>';
      var svgContainer = document.querySelector('.svg-container');
      svgContainer.parentNode.insertBefore(svgInfoPanel, svgContainer.nextSibling);
    }
    document.getElementById('svgInfoTitle').textContent = 'ℹ️ ' + info.split(':')[0];
    document.getElementById('svgInfoText').textContent = info;
  }
}
```

## Reglas

- **NO añadir a TODOS los elementos SVG** — solo a los clave (líneas principales, puntos de interés)
- **Siempre verificar** que `toggleHighlight` existe en el `<script>` ANTES de patchear los SVGs
- **Máximo 2-3 elementos interactivos por SVG** para no saturar
- **data-info** debe ser breve y descriptivo (máximo 2 líneas)
- **Si el archivo ya tiene un panel de info**, reutilizarlo en lugar de crear `svgInfoPanel`

## Ejemplos reales

- `b07-04-verdadera-magnitud.html`: 12+ elementos SVG interactivos (líneas, círculos, textos)
- `b09-02-lista-piezas.html`: Piezas SVG con info panel toggle
