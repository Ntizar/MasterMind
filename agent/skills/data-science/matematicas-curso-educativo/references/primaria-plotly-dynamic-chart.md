# Patrón: Gráfico Plotly de barras interactivo con controles para Primaria

Desde la ronda 2 de mejora continua (2026-06-09), se añadió Plotly a archivos de primaria con botones interactivos.

## Estructura HTML

```html
<div class="chart-container">
<h3>📊 Visualización: Título del gráfico</h3>
<p class="chart-desc">Descripción breve. ¿Puedes adivinar...?</p>
<div id="plotly-{id}" class="chart-canvas"></div>
<div class="chart-controls">
<button onclick="randomizar{Id}()">🎲 Nuevos datos</button>
<button onclick="ordenar{Id}()">📈 Ordenar por resultado</button>
</div>
</div>
```

## Funciones JS

```javascript
function renderPlotly{Id}() {
  const data = [{
    x: ['245+178', '356+243', '428+265'],
    y: [423, 599, 693],
    type: 'bar',
    marker: { color: ['#2563eb','#f97316','#10b981'] },
    text: [423, 599, 693],
    textposition: 'auto'
  }];
  const layout = {
    margin: {t: 20, b: 80, l: 50, r: 20},
    xaxis: {tickangle: -30, tickfont: {size: 10}},
    yaxis: {title: 'Resultado', range: [0, 1100]},
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
  };
  Plotly.newPlot('plotly-{id}', data, layout, {responsive: true, displayModeBar: false});
}

function randomizar{Id}() {
  const ops = [];
  for (let i = 0; i < 9; i++) {
    const a = Math.floor(Math.random() * 600) + 100;
    const b = Math.floor(Math.random() * 600) + 100;
    ops.push({label: a+'+'+b, value: a+b});
  }
  const data = [{
    x: ops.map(o => o.label),
    y: ops.map(o => o.value),
    type: 'bar',
    marker: {color: ops.map((_,i) => ['#2563eb','#f97316','#10b981','#a855f7','#ef4444'][i%5])},
    text: ops.map(o => o.value),
    textposition: 'auto'
  }];
  const layout = {
    margin: {t: 20, b: 80, l: 50, r: 20},
    xaxis: {tickangle: -30, tickfont: {size: 9}},
    yaxis: {title: 'Resultado'},
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
  };
  Plotly.newPlot('plotly-{id}', data, layout, {responsive: true, displayModeBar: false});
}

function ordenar{Id}() {
  // Ordenar datos por resultado (y) de menor a mayor
  const sorted = ops.sort((a,b) => a.value - b.value);
  // ... mismo layout, datos ordenados
  Plotly.newPlot('plotly-{id}', data, layout, {responsive: true, displayModeBar: false});
}
```

## Llamar en DOMContentLoaded

```javascript
document.addEventListener('DOMContentLoaded', () => {
  renderPlotly{Id}();
});
```

## Notas

- Ya existe CDN de Plotly en la mayoría de archivos (verificar con `read_file`)
- `displayModeBar: false` para no mostrar la barra de herramientas de Plotly
- `paper_bgcolor` y `plot_bgcolor` en `rgba(0,0,0,0)` para transparencia
- Colores cíclicos con `[...][i%5]` para barras múltiples
- `textposition: 'auto'` muestra el valor encima de cada barra

## Primer uso

- **2026-06-09:** `s02-1primaria.html` — gráfico de 9 sumas de 3 cifras con botones randomizar y ordenar.
