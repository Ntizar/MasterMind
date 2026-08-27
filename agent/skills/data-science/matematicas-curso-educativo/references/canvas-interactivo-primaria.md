# Patrón: Canvas Interactivo — Pizarra Mágica

## Cuándo usarlo

En primaria (1º-3º), cuando el tema sea sobre figuras geométricas, formas, o conceptos visuales. Permite al alumno practicar dibujando la figura elegida.

## Implementación

### HTML

```html
<h2 class="chapter-title">🎨 ¡Dibuja figuras!</h2>

<div class="interactive">
<h3>🖌️ Pizarra mágica de figuras</h3>
<p>Elige una figura y haz clic en la pizarra para dibujarla.</p>
<div style="text-align:center;margin:1rem 0">
<button onclick="drawShape('circulo')" style="background:#2563eb;color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;margin:.3rem">⭕ Círculo</button>
<button onclick="drawShape('cuadrado')" style="background:#f97316;color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;margin:.3rem">🟧 Cuadrado</button>
<button onclick="drawShape('triangulo')" style="background:#10b981;color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;margin:.3rem">🔺 Triángulo</button>
<button onclick="drawShape('rectangulo')" style="background:#8b5cf6;color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;margin:.3rem">▭ Rectángulo</button>
<button onclick="clearCanvas()" style="background:#ef4444;color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;margin:.3rem">🗑️ Borrar</button>
</div>
<canvas id="drawCanvas" width="500" height="300" style="border:3px dashed #cbd5e1;border-radius:12px;background:#fff;cursor:crosshair;display:block;margin:0 auto;max-width:100%"></canvas>
<div id="drawResult" class="result" style="display:none;text-align:center;margin-top:.8rem"></div>
</div>
```

### JavaScript

```javascript
let currentShape = null;
const canvas = document.getElementById('drawCanvas');
const ctx = canvas.getContext('2d');

function drawShape(shape){
  currentShape = shape;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const colors = {circulo:'#2563eb',cuadrado:'#f97316',triangulo:'#10b981',rectangulo:'#8b5cf6'};
  const names = {circulo:'círculo',cuadrado:'cuadrado',triangulo:'triángulo',rectangulo:'rectángulo'};
  document.getElementById('drawResult').style.display = 'block';
  document.getElementById('drawResult').className = 'result';
  document.getElementById('drawResult').textContent = '🎨 Haz clic en la pizarra para dibujar un '+names[shape]+'!';
}

canvas.addEventListener('click', function(e){
  if(!currentShape) return;
  const rect = canvas.getBoundingClientRect();
  const x = (e.clientX - rect.left) * (canvas.width / rect.width);
  const y = (e.clientY - rect.top) * (canvas.height / rect.height);
  const colors = {circulo:'#2563eb',cuadrado:'#f97316',triangulo:'#10b981',rectangulo:'#8b5cf6'};
  ctx.fillStyle = colors[currentShape] + '33';
  ctx.strokeStyle = colors[currentShape];
  ctx.lineWidth = 3;
  
  if(currentShape === 'circulo'){
    ctx.beginPath();
    ctx.arc(x, y, 40, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  } else if(currentShape === 'cuadrado'){
    ctx.fillRect(x-35, y-35, 70, 70);
    ctx.strokeRect(x-35, y-35, 70, 70);
  } else if(currentShape === 'triangulo'){
    ctx.beginPath();
    ctx.moveTo(x, y-40);
    ctx.lineTo(x+40, y+35);
    ctx.lineTo(x-40, y+35);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else if(currentShape === 'rectangulo'){
    ctx.fillRect(x-45, y-25, 90, 50);
    ctx.strokeRect(x-45, y-25, 90, 50);
  }
  
  const result = document.getElementById('drawResult');
  result.style.display = 'block';
  result.className = 'result ok';
  result.textContent = '✅ ¡Has dibujado un '+currentShape+'! ¿Lo ves en algo de tu habitación?';
});

function clearCanvas(){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  currentShape = null;
  document.getElementById('drawResult').style.display = 'block';
  document.getElementById('drawResult').className = 'result';
  document.getElementById('drawResult').textContent = '🗑️ Pizarra limpia. ¡Elige una figura para dibujar!';
}
```

## Reglas

- Colores deben coincidir con CSS variables del tema
- Canvas debe ser responsive: `max-width: 100%`
- Feedback siempre positivo y contextual ("¿Lo ves en algo de tu habitación?")
- Botón borrar siempre disponible
- No usar Plotly para este tipo de interacción — canvas es más apropiado para dibujo libre

## Primer uso

Implementado en `s01-7-figuras-basicas.html` (2026-06-09).
