# Plantilla HTML Educativo Interactivo — KaTeX + Plotly.js

Plantilla base para sesiones educativas con:
- **KaTeX** (CDN) para fórmulas LaTeX
- **Plotly.js** (CDN) para gráficos interactivos
- Ejercicios con inputs y feedback
- Barra de progreso scroll
- Navegación Anterior/Siguiente

## Componentes clave

### Cajas de contenido
- `.box-teoria` → fondo azul, borde azul
- `.box-ejemplo` → fondo naranja, borde naranja
- `.box-error` → fondo rojo, borde rojo
- `.box-idea` → fondo púrpura, borde púrpura
- `.box-success` → fondo verde, borde verde

### Gráficos Plotly
```javascript
Plotly.newPlot('plot-id', [trace], {
  margin: {t: 10, r: 10, b: 40, l: 40},
  xaxis: {title: 'x'}, yaxis: {title: 'y'}
}, {responsive: true});
```

### Ejercicios
```html
<div class="exercise-input">
  <input type="number" id="e1" placeholder="?">
  <button onclick="checkExercise(1, 42)">Comprobar</button>
</div>
<div class="feedback" id="e1-fb"></div>
```

## Notas importantes

- KaTeX usa `$$...$$` para display math y `$...$` para inline
- Plotly.js es interactivo por defecto (zoom, pan, hover)
- Siempre añadir `responsive: true` en config de Plotly
- El feedback de ejercicios usa `checkExercise(num, respuesta)` con comparación exacta
- Para Bachiller/Carrera: usar colores púrpura/índigo (#6366f1) en vez de azul
- Para Primaria: mantener colores simples sin KaTeX
