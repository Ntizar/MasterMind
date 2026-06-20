# Patrón: Canvas de Fracciones Equivalentes

## Cuándo usarlo

En primaria (3º-4º), cuando el tema sea fracciones equivalentes. Muestra visualmente que dos fracciones representan la misma cantidad aunque tengan distinto número de trozos.

## Implementación

### HTML

```html
<section class="chapter">
<h2 class="chapter-title">👀 Visualiza: ¿Por qué son iguales?</h2>
<div class="visual">
  <div class="visual-piece">
    <canvas id="vis1" width="120" height="120"></canvas>
    <p style="position:absolute;bottom:4px;font-size:.75rem">1/2 = 2/4</p>
  </div>
  <div class="visual-piece">
    <canvas id="vis2" width="120" height="120"></canvas>
    <p style="position:absolute;bottom:4px;font-size:.75rem">2/4 = 4/8</p>
  </div>
</div>
<p style="text-align:center;color:#64748b;font-size:.9rem">
  Mira cómo el área coloreada es la misma aunque los trozos sean de distinto tamaño
</p>
</section>
```

### JavaScript

```javascript
function drawFraction(canvas, num, den) {
  var ctx = canvas.getContext('2d');
  var w = canvas.width, h = canvas.height;
  ctx.clearRect(0, 0, w, h);
  var partW = w / den;
  for (var i = 0; i < den; i++) {
    ctx.fillStyle = i < num ? '#2563eb' : '#e2e8f0';
    ctx.fillRect(i * partW, 0, partW, h);
    ctx.strokeStyle = '#94a3b8';
    ctx.strokeRect(i * partW, 0, partW, h);
  }
}
drawFraction(document.getElementById('vis1'), 1, 2);
drawFraction(document.getElementById('vis2'), 2, 4);
```

## Reglas

- Dibujar barras horizontales divididas en `den` partes, colorear `num` partes
- Usar CSS variable `--azul` (#2563eb) para color, `#e2e8f0` para sin colorear
- Mostrar etiqueta debajo del canvas con la equivalencia
- Usar dos canvas lado a lado para comparar equivalencias
- **No usar Plotly** para este tipo de visualización — canvas es más ligero y directo
- Tamaño fijo 120×120px, responsive con `max-width: 100%` en el contenedor `.visual-piece`

## Primer uso

Implementado en `s04-4-fracciones-equivalentes.html` (2026-06-10).
