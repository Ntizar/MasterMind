# Canvas de línea numérica interactiva — Patrón "Sapo que salta"

**Descubierto:** 2026-06-10  
**Aplica a:** Primaria (restar, sumar visual)  
**Diferente de:** `svg-recta-numerica.md` (SVG accesible para ESO), `canvas-balanza-peso.md` (balanza para peso/masa)

## Cuándo usarlo

- Temas de restar con números grandes (11-20) en primaria
- Cuando necesitas que el alumno VEJA la resta como movimiento
- Cuando Plotly es excesivo para un concepto de movimiento en línea

## Estructura

```html
<div class="canvas-container">
<canvas id="numberLine" width="700" height="150"></canvas>
</div>
<div style="text-align:center;margin:1rem 0">
<label>Empieza en: <input type="number" id="nlStart" value="15"></label>
<label>Salta hacia atrás: <input type="number" id="nlJump" value="7"></label>
<button onclick="drawNumberLine()">¡Saltar!</button>
</div>
<div class="result" id="nlResult"></div>
```

## Función JS principal

```javascript
function drawNumberLine(){
  const canvas = document.getElementById('numberLine');
  const ctx = canvas.getContext('2d');
  const start = parseInt(document.getElementById('nlStart').value);
  const jump = parseInt(document.getElementById('nlJump').value);
  const end = start - jump;
  const result = document.getElementById('nlResult');

  if(jump >= start){
    result.className = 'result fail';
    result.innerHTML = '❌ No puedes saltar ' + jump + ' pasos desde ' + start + '.';
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const y = 80;
  const stepX = 30;
  const startX = 50;

  ctx.strokeStyle = '#94a3b8';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(startX, y);
  ctx.lineTo(startX + 20 * stepX, y);
  ctx.stroke();

  ctx.font = 'bold 14px Inter, sans-serif';
  ctx.textAlign = 'center';
  for(let i = 0; i <= 20; i++){
    const x = startX + i * stepX;
    ctx.fillRect(x - 1, y - 15, 2, 30);
    ctx.fillText(i.toString(), x, y + 35);
  }

  const startXPos = startX + start * stepX;
  ctx.fillStyle = '#10b981';
  ctx.beginPath();
  ctx.arc(startXPos, y, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 16px Inter, sans-serif';
  ctx.fillText(start.toString(), startXPos, y + 6);

  ctx.strokeStyle = '#f97316';
  ctx.lineWidth = 3;
  const jumpX = startX + end * stepX;
  const arrowY = y - 30;
  ctx.beginPath();
  ctx.moveTo(startXPos, y - 18);
  ctx.lineTo(jumpX, arrowY);
  ctx.stroke();

  ctx.fillStyle = '#f97316';
  ctx.font = 'bold 13px Inter, sans-serif';
  ctx.fillText('−' + jump, (startXPos + jumpX) / 2, arrowY - 8);

  ctx.fillStyle = '#2563eb';
  ctx.beginPath();
  ctx.arc(jumpX, y, 18, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#fff';
  ctx.font = 'bold 16px Inter, sans-serif';
  ctx.fillText(end.toString(), jumpX, y + 6);

  ctx.font = '24px sans-serif';
  ctx.fillText('🐸', startXPos - 5, y - 22);
  ctx.fillText('🐸', jumpX - 5, y - 22);

  result.className = 'result ok';
  result.innerHTML = '🐸 ¡El sapo saltó de ' + start + ' hacia atrás ' + jump + ' pasos y llegó a ' + end + '!';
}
```

## CSS necesario

```css
.canvas-container{text-align:center;margin:1rem 0}
.canvas-container canvas{border-radius:12px;background:#fff;max-width:100%}
```

## Variantes

- **Suma:** cambiar flecha para que vaya hacia adelante (izquierda a derecha)
- **Conteo visual:** dibujar emojis en cada posición de la línea
- **Inicialización automática:** llamar `drawNumberLine()` en `window.onload` con valores por defecto

## Ejemplo real

Aplicado en `s01-6-restar-hasta-20.html` (2026-06-10): reemplazó Plotly decorativo por canvas interactivo donde el sapo salta hacia atrás para restar. Los alumnos pueden cambiar los valores y ver el salto en tiempo real.
