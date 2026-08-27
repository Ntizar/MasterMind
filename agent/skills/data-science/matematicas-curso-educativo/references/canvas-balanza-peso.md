# Patrón: Canvas Interactivo — Balanza de Peso

## Cuándo usarlo

En primaria (1º-3º), cuando el tema sea sobre **peso, masa, comparación de magnitudes**. Permite al alumno explorar la diferencia entre tamaño y peso de forma visual e interactiva.

## Implementación

### HTML

```html
<h2 class="chapter-title">4️⃣ ¡La balanza mágica!</h2>
<div class="interactive">
<h3>🎯 Toca los animales para ver cuánta pesa cada uno. ¿Cuál pesa más?</h3>
<canvas id="balanceCanvas" width="400" height="250" style="display:block;margin:1rem auto;background:#fff;border-radius:12px;border:2px solid #e2e8f0;cursor:pointer"></canvas>
<div id="balanceResult" class="result" style="text-align:center;margin-top:1rem"></div>
</div>
```

### JavaScript

```javascript
// Balance canvas interactive
(function() {
  const canvas = document.getElementById('balanceCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const animals = [
    {name:'🐘 Elefante', weight:5000, x:100, y:120, color:'#2563eb'},
    {name:'🐱 Gato', weight:5, x:200, y:120, color:'#f97316'},
    {name:'🐜 Hormiga', weight:0.005, x:300, y:120, color:'#10b981'}
  ];

  let selected = null;
  let resultShown = false;

  function draw() {
    ctx.clearRect(0, 0, 400, 250);

    // Draw balance beam
    ctx.strokeStyle = '#64748b';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(200, 200);
    ctx.lineTo(200, 180);
    ctx.stroke();

    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(50, 100);
    ctx.lineTo(350, 100);
    ctx.stroke();

    // Draw animals
    animals.forEach((a, i) => {
      ctx.font = '30px serif';
      ctx.fillText(a.name, a.x - 30, a.y);
      ctx.font = 'bold 12px Inter, sans-serif';
      ctx.fillStyle = a.color;
      ctx.fillText(a.weight + ' kg', a.x - 20, a.y + 25);
      ctx.fillStyle = '#1e293b';
      if (selected === i) {
        ctx.strokeStyle = a.color;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(a.x, a.y - 10, 40, 0, Math.PI * 2);
        ctx.stroke();
      }
    });

    // Draw balance scale pans
    ctx.strokeStyle = '#94a3b8';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(50, 100); ctx.lineTo(30, 140);
    ctx.moveTo(350, 100); ctx.lineTo(370, 140);
    ctx.stroke();
    ctx.fillStyle = '#f1f5f9';
    ctx.fillRect(20, 140, 60, 20);
    ctx.fillRect(320, 140, 60, 20);
    ctx.strokeRect(20, 140, 60, 20);
    ctx.strokeRect(320, 140, 60, 20);
  }

  canvas.addEventListener('click', function(e) {
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) * (400 / rect.width);
    const y = (e.clientY - rect.top) * (250 / rect.height);
    let clicked = -1;
    animals.forEach((a, i) => {
      if (Math.abs(x - a.x) < 50 && Math.abs(y - a.y) < 40) clicked = i;
    });
    if (clicked >= 0) {
      selected = clicked;
      draw();
      if (!resultShown) {
        resultShown = true;
        const r = document.getElementById('balanceResult');
        const a = animals[clicked];
        r.className = 'result ok';
        r.innerHTML = '🌟 ' + a.name + ' pesa <b>' + a.weight + ' kg</b>. ¡El elefante es el más pesado de todos!';
      }
    }
  });

  draw();
})();
```

## Reglas

- Canvas 400x250, responsive con `max-width: 100%`
- Colores coincidan con CSS variables del tema
- Feedback siempre contextual: muestra peso REAL en kg
- El resultado muestra la comparación final ("el elefante es el más pesado")
- Envolver en IIFE `(function(){ ... })();` para no contaminar scope global
- Verificar `if (!canvas) return;` como guard

## Primer uso

Implementado en `s01-8-medidas-tamano-peso.html` (2026-06-10).
