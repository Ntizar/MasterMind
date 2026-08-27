# Plotly en archivos de primaria

## Contexto

La regla general era: Plotly SOLO en Bachiller/Universidad. Los archivos de primaria (s01-s06) usaban canvas o CSS+emoji para visualizaciones.

## Excepción: ronda 2 de mejora continua

En la ejecución del cron de 2026-06-09, se añadió Plotly a `s01-6-restar-hasta-20.html` (1º Primaria) con un gráfico de barras simple mostrando los resultados de las 12 restas del tema.

## Patrón correcto

### 1. Añadir CDN en el <head>

```html
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js" async></script>
```

**IMPORTANTE:** La etiqueta debe ir como hermano del bloque `<script>` existente, NO dentro. Si el HTML ya tiene `<script>...</script>`, el CDN va ANTES del `<style>` o justo después del `<title>`.

### 2. Contenedor del gráfico

```html
<div id="plotly-chart" style="min-height:300px;margin:1rem 0"></div>
```

### 3. Código JS con guard

```javascript
if(typeof plotly !== 'undefined'){
  var chartData = [{
    type: 'bar',
    x: ['15−7', '18−9', ...],
    y: [8, 9, ...],
    marker: { color: ['#2563eb','#10b981',...] },
    text: ['8','9',...],
    textposition: 'outside',
    hovertemplate: '<b>%{x}</b><br>Resultado: %{y}<extra></extra>'
  }];
  var chartLayout = {
    title: {text: '📊 Resultados', font: {size: 14}},
    xaxis: {title: 'Resta', tickangle: -45},
    yaxis: {title: 'Resultado', range: [0, 14]},
    margin: {t: 50, b: 80, l: 50, r: 20},
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)'
  };
  Plotly.newPlot('plotly-chart', chartData, chartLayout, {responsive: true, displayModeBar: false});
}
```

### 4. Verificación

Tras el patch, leer el archivo con `read_file` y verificar:
- No hay `<script><script` (etiqueta anidada inválida)
- El CDN aparece una sola vez
- El `if(typeof plotly` guard está presente

## Decision

Plotly se puede usar en primaria para gráficos de barras simples. Para visualizaciones más complejas (scatter, 3D), mantener la restricción Bachiller/Universidad.
