# Patrón: Canvas de Figuras Compuestas Seleccionables

## Cuándo usarlo

En primaria (3º-6º), cuando el tema sea sobre figuras compuestas, áreas o perímetros. Permite al alumno **seleccionar una figura compuesta** y calcular su área/perímetro.

## Diferencia con pizarra mágica

- **Pizarra mágica** (`canvas-interactivo-primaria.md`): dibujo libre, el alumno dibuja lo que quiere.
- **Figuras seleccionables**: el alumno ELIGE una figura predefinida (L, T, H...) y calcula su área. Es evaluación, no dibujo libre.

## Implementación

### HTML

```html
<section class="chapter">
<h2 class="chapter-title">🎮 ¡Dibuja y calcula!</h2>
<div class="interactive">
<h3>Selecciona la figura compuesta y calcula su área:</h3>
<div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center;margin:1rem 0">
<button onclick="showFigure('L')" style="padding:.6rem 1rem;border:2px solid var(--azul);border-radius:8px;background:#fff;cursor:pointer;font-size:1rem">📐 Figura L</button>
<button onclick="showFigure('T')" style="padding:.6rem 1rem;border:2px solid var(--azul);border-radius:8px;background:#fff;cursor:pointer;font-size:1rem">📐 Figura T</button>
<button onclick="showFigure('H')" style="padding:.6rem 1rem;border:2px solid var(--azul);border-radius:8px;background:#fff;cursor:pointer;font-size:1rem">📐 Figura H</button>
</div>
<canvas id="figCanvas" class="figure-canvas" width="400" height="250" style="display:none"></canvas>
<div id="figQuestion" style="text-align:center;margin:1rem 0;font-weight:600;font-size:1.1rem"></div>
<div id="figButtons" style="display:flex;gap:.5rem;justify-content:center;flex-wrap:wrap"></div>
<div class="result" id="figResult"></div>
</div>
</section>
```

### JavaScript

```javascript
const figures = {
  L: {
    q: "Figura L: rectángulo vertical 4×3 + horizontal 2×3. ¿Área total?",
    opts: ["18", "21", "15"],
    correct: 0,
    explain: "12 + 6 = 18 cm²"
  },
  T: {
    q: "Figura T: rectángulo superior 4×2 + inferior 2×3. ¿Área total?",
    opts: ["14", "12", "16"],
    correct: 0,
    explain: "8 + 6 = 14 cm²"
  },
  H: {
    q: "Figura H: rectángulo vertical 3×5 + dos horizontales 2×2. ¿Área total?",
    opts: ["19", "21", "17"],
    correct: 0,
    explain: "15 + 4 + 4 = 23 cm²"
  }
};

function showFigure(type) {
  const canvas = document.getElementById('figCanvas');
  canvas.style.display = 'block';
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 400, 250);

  const f = figures[type];
  document.getElementById('figQuestion').textContent = f.q;

  // Dibujar figura compuesta
  ctx.fillStyle = '#dbeafe';
  ctx.strokeStyle = '#2563eb';
  ctx.lineWidth = 2;

  if (type === 'L') {
    ctx.fillRect(100, 50, 120, 160);
    ctx.strokeRect(100, 50, 120, 160);
    ctx.fillRect(220, 130, 80, 80);
    ctx.strokeRect(220, 130, 80, 80);
    // Línea divisoria
    ctx.setLineDash([5, 5]);
    ctx.strokeStyle = '#f97316';
    ctx.beginPath();
    ctx.moveTo(220, 50);
    ctx.lineTo(220, 210);
    ctx.stroke();
    ctx.setLineDash([]);
    // Etiquetas
    ctx.fillStyle = '#1e293b';
    ctx.font = '14px Inter';
    ctx.fillText('4×3', 130, 140);
    ctx.fillText('2×3', 240, 175);
  }
  // ... otros tipos

  // Botones quiz
  const btnsDiv = document.getElementById('figButtons');
  btnsDiv.innerHTML = '';
  document.getElementById('figResult').textContent = '';
  document.getElementById('figResult').className = 'result';

  f.opts.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'quiz-btn';
    btn.textContent = opt;
    btn.onclick = function() {
      btnsDiv.querySelectorAll('.quiz-btn').forEach(b => { b.disabled = true; b.style.pointerEvents = 'none'; });
      if(i === f.correct) {
        btn.classList.add('correct');
        document.getElementById('figResult').className = 'result ok';
        document.getElementById('figResult').textContent = '✅ ¡Correcto! ' + f.explain;
      } else {
        btn.classList.add('wrong');
        document.getElementById('figResult').className = 'result fail';
        document.getElementById('figResult').textContent = '❌ La respuesta es ' + f.opts[f.correct];
      }
    };
    btnsDiv.appendChild(btn);
  });
}
```

## Reglas

- Cada figura debe tener **etiquetas de dimensiones** visibles en el canvas
- La **línea divisoria** (dashed) debe mostrar cómo se descompone la figura
- Las **dimensiones** deben coincidir con el enunciado de la pregunta
- El **quiz** debe tener 3 opciones (1 correcta, 2 distractores plausibles)
- El resultado debe incluir la **explicación del cálculo** (no solo "correcto/incorrecto")
- CSS class `.figure-canvas` con `display:block;margin:1rem auto;border:2px solid var(--azul);border-radius:8px;background:#fff`

## Primer uso

Implementado en `s05-5-areas-perimetros.html` (2026-06-10).
