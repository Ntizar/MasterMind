# Patrón SVG Animado — Ronda 2

## CSS Keyframes (completo)

Añadir al `<style>` del archivo, justo antes de `</style>`:

```css
@keyframes pulse-point { 0%,100%{r:4;opacity:1} 50%{r:7;opacity:.6} }
@keyframes draw-line { 0%{stroke-dashoffset:200} 100%{stroke-dashoffset:0} }
@keyframes fade-in { 0%{opacity:0;transform:translateY(10px)} 100%{opacity:1;transform:translateY(0)} }
@keyframes highlight-glow { 0%,100%{filter:drop-shadow(0 0 3px rgba(16,185,129,.4))} 50%{filter:drop-shadow(0 0 8px rgba(16,185,129,.8))} }
.svg-element { transition: all .3s ease; cursor: pointer; }
.svg-element:hover { filter: brightness(1.15) drop-shadow(0 0 4px rgba(37,99,235,.3)); }
.svg-element.active { filter: brightness(1.2) drop-shadow(0 0 6px rgba(16,185,129,.6)); stroke-width: 4 !important; }
.pulse { animation: pulse-point 1.5s ease-in-out infinite; }
.animate { stroke-dasharray: 200; stroke-dashoffset: 200; animation: draw-line 1s ease forwards; }
.fade-in { animation: fade-in .5s ease forwards; }
.highlight-glow { animation: highlight-glow 2s ease-in-out infinite; }
```

## Clases CSS aplicadas

| Clase | Elemento | Efecto |
|-------|----------|--------|
| `svg-element clickable` | líneas, círculos SVG | cursor:pointer + hover glow |
| `svg-element active` | elementos clickeados | borde verde + glow |
| `pulse` | círculos de intersección | pulso infinito (r:4→7) |
| `animate` | líneas de referencia | stroke-dashoffset 200→0 |
| `fade-in` | textos, grupos | opacity 0→1 + slide up |
| `highlight-glow` | elementos destacados | drop-shadow pulsante |

## Aplicación práctica

### 1. SVG interactivo (paso 1 — el SVG principal)
```html
<line x1="80" y1="130" x2="320" y2="50"
  class="svg-element clickable"
  onclick="toggleHighlight(this)"
  data-info="r': proyección vertical — acortada, no es VM"/>
<!-- Puntos de intersección pulsantes -->
<circle cx="80" cy="50" r="4" fill="#ef4444" class="pulse"
  onclick="toggleHighlight(this)"
  data-info="Punto A: extremo de la recta"/>
```

### 2. SVG de pasos intermedios (paso 2/3 — animación progresiva)
```html
<line x1="80" y1="80" x2="320" y2="80" class="vm-line animate" stroke="#10b981" stroke-width="3"/>
<text x="330" y="84" class="fade-in">r' (VM)</text>
<circle cx="80" cy="80" r="4" fill="#10b981" class="pulse"
  onclick="toggleHighlight(this)" data-info="VM empieza aquí"/>
```

### 3. Función toggleHighlight
```javascript
function toggleHighlight(el) {
  el.classList.toggle('active');
  var info = el.getAttribute('data-info');
  if (info) {
    var result = document.getElementById('vm-status');
    if (result) {
      result.textContent = '📌 ' + info;
      result.setAttribute('fill', '#64748b');
    }
  }
}
```

### 4. Mejorar showStep() para re-trigger animaciones
```javascript
function showStep(n) {
  for (var i = 1; i <= 4; i++) {
    var step = document.getElementById('step' + i);
    var dot = document.getElementById('sd' + i);
    if (step) step.style.display = (i === n) ? 'block' : 'none';
    if (dot) {
      if (i === n) { dot.classList.add('active'); dot.style.background = 'var(--azul)'; }
      else { dot.classList.remove('active'); dot.style.background = '#94a3b8'; }
    }
  }
  // Re-trigger SVG animations when switching steps
  if (n >= 2) {
    var activeStep = document.getElementById('step' + n);
    if (activeStep) {
      var animElements = activeStep.querySelectorAll('.animate, .fade-in, .pulse');
      animElements.forEach(function(el) {
        el.style.animation = 'none';
        el.offsetHeight;
        el.style.animation = '';
      });
    }
  }
}
```

## Ejemplos aplicados

- **b04-06-vm.html** (2026-06-15): SVG principal con toggleHighlight + pulse en 2 puntos, SVG paso 2 con animate en flecha, SVG paso 3 con animate en 3 líneas + fade-in en textos + 2 círculos pulse
- **b04-09-resumen-diedrico.html** (2026-06-15): SVG paso 1 con línea animate + punto 3D pulse, SVG paso 4 con círculos svg-element clickable + data-info + pulse en Th

## Reglas

- NO añadir animaciones en ronda 1 (temas nuevos)
- SOLO en ronda 2+ cuando el tema ya tiene SVG interactivo
- Máximo 2 tipos de animación por SVG para no saturar
- Siempre añadir `data-info` a elementos `svg-element clickable`
- Siempre mejorar `showStep()` para re-trigger animaciones al cambiar de paso
- Eliminar funciones duplicadas (showStep, checkFillIn) ANTES de aplicar el patrón
