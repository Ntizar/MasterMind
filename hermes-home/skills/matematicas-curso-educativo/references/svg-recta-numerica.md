# Recta numérica SVG interactiva

Patrón para crear una recta numérica interactiva con SVG en HTML de DeSumarIntegrar. Útil para temas de números enteros, comparación, ordenación y valor absoluto en ESO.

## Cuándo usarlo

- Temas de números enteros (negativos, positivos, cero)
- Comparación de números (mayor/menor)
- Valor absoluto visual
- Ordenación en la recta

## Implementación

### 1. CSS mínimo

```css
.number-line{display:flex;align-items:center;justify-content:center;margin:1.5rem 0;overflow-x:auto;padding:1rem 0}
.number-line svg{min-width:600px}
```

### 2. SVG container

```html
<div class="number-line">
<svg id="numberLineSvg" width="620" height="120" viewBox="0 0 620 120">
  <line x1="30" y1="60" x2="590" y2="60" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
  <polygon points="30,60 42,54 42,66" fill="#94a3b8"/>
  <polygon points="590,60 578,54 578,66" fill="#94a3b8"/>
</svg>
</div>
```

### 3. JS: drawNumberLine()

```javascript
function drawNumberLine() {
  const svg = document.getElementById('numberLineSvg');
  const startX = 40;
  const endX = 580;
  const y = 60;
  const range = [-10, 10];
  const totalRange = range[1] - range[0]; // 20
  const pxPerUnit = (endX - startX) / totalRange; // 27px por unidad

  // Limpiar marcas anteriores
  const existing = svg.querySelectorAll('.mark-group');
  existing.forEach(g => g.remove());

  for (let i = range[0]; i <= range[1]; i++) {
    const x = startX + (i - range[0]) * pxPerUnit;
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.classList.add('mark-group');

    // Marca vertical
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x); line.setAttribute('y1', y - 10);
    line.setAttribute('x2', x); line.setAttribute('y2', y + 10);
    line.setAttribute('stroke', i === 0 ? '#2563eb' : '#94a3b8');
    line.setAttribute('stroke-width', i === 0 ? '3' : '2');
    g.appendChild(line);

    // Etiqueta numérica
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x); text.setAttribute('y', y + 30);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('font-size', i === 0 ? '14' : '12');
    text.setAttribute('font-weight', i === 0 ? 'bold' : 'normal');
    text.setAttribute('fill', i === 0 ? '#2563eb' : '#64748b');
    text.textContent = i;
    g.appendChild(text);

    // Círculo invisible clickeable
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x); circle.setAttribute('cy', y);
    circle.setAttribute('r', '12'); circle.setAttribute('fill', 'transparent');
    circle.setAttribute('cursor', 'pointer');
    circle.onclick = function() { showPoint(i, x); };
    g.appendChild(circle);

    svg.appendChild(g);
  }
}
```

### 4. JS: showPoint() + showRandomPoint()

```javascript
function showPoint(n, x) {
  const svg = document.getElementById('numberLineSvg');
  svg.querySelectorAll('.highlight').forEach(h => h.remove());

  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.classList.add('highlight');
  const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  circle.setAttribute('cx', x); circle.setAttribute('cy', 60);
  circle.setAttribute('r', '15'); circle.setAttribute('fill', '#f97316');
  circle.setAttribute('opacity', '0.3');
  g.appendChild(circle);
  svg.appendChild(g);

  const sign = n > 0 ? 'positivo' : n < 0 ? 'negativo' : 'cero';
  const abs = Math.abs(n);
  document.getElementById('lineResult').className = 'result ok';
  document.getElementById('lineResult').innerHTML =
    `📍 <strong>${n}</strong> es ${sign}. Valor absoluto: |${n}| = ${abs}.`;
}

function showRandomPoint() {
  const n = Math.floor(Math.random() * 21) - 10;
  const startX = 40;
  const pxPerUnit = 27;
  const x = startX + (n - (-10)) * pxPerUnit;
  showPoint(n, x);
}
```

### 5. Inicialización

```javascript
drawNumberLine();
```

## Variables clave

| Variable | Valor | Significado |
|----------|-------|-------------|
| `startX` | 40 | Posición X del inicio |
| `endX` | 580 | Posición X del final |
| `y` | 60 | Posición Y de la línea |
| `range` | [-10, 10] | Rango de números visibles |
| `pxPerUnit` | 27 | Píxeles por unidad |

## Diferencias con canvas

| Aspecto | Canvas | SVG |
|---------|--------|-----|
| Interactividad | Requiere detectar coordenadas del ratón | Clic directo en elementos SVG |
| Escalabilidad | Pixel-based | Vectorial, escala perfecto |
| CSS | No se puede estilizar con CSS | Se puede estilizar con CSS |
| Accesibilidad | No accesible sin workarounds | Accesible (elementos DOM) |
| Mejor para | Gráficos complejos, animaciones | Rectas numéricas, diagramas simples |

## Ejemplo real

Implementado en `eso1-1-numeros-enteros.html` (2026-06-10): recta numérica de -10 a 10 con clic interactivo, muestra signo y valor absoluto.
