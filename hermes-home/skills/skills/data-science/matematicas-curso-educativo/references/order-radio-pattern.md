# Patrón: Ordenar con radio buttons (s02-4primaria, 2026-06-10)

## Cuándo usarlo
Cuando necesitas que el alumno ordene 3+ items por su resultado numérico y quieres evitar tracking de estado global. Más robusto que click-order para primaria.

## HTML
```html
<div class="exercise">
<p><strong>Ejercicio X (ordenar de menor a mayor):</strong> Ordena estas divisiones por su resultado:</p>
<ul class="order-list">
<li><input type="radio" name="orderX" value="1"> 120 ÷ 4 (resultado: 30)</li>
<li><input type="radio" name="orderX" value="3"> 300 ÷ 5 (resultado: 60)</li>
<li><input type="radio" name="orderX" value="2"> 200 ÷ 4 (resultado: 50)</li>
</ul>
<p style="font-size:.9rem;color:#64748b">Selecciona en qué orden van: primero el menor, luego el del medio, luego el mayor.</p>
<div class="exercise-input"><button onclick="checkOrderX()">Comprobar orden</button></div>
<div class="feedback" id="eX-fb"></div>
</div>
```

## CSS
```css
.order-list{list-style:none;padding:0}
.order-list li{padding:.5rem .8rem;margin:.3rem 0;background:#fff;border-radius:6px;border:1px solid #e2e8f0;display:flex;align-items:center;gap:.5rem}
.order-list li input[type="radio"]{width:20px;height:20px;cursor:pointer}
```

## JS
```javascript
function checkOrderX() {
  const feedback = document.getElementById('eX-fb');
  const radios = document.querySelectorAll('input[name="orderX"]');
  const values = [];
  radios.forEach(r => { if (r.checked) values.push(parseInt(r.value)); });
  if (values.length < 3) {
    feedback.textContent = 'Selecciona el orden para los 3.';
    feedback.className = 'feedback incorrect';
    return;
  }
  // Correct order: 30 (120÷4), 50 (200÷4), 60 (300÷5) → values [1, 3, 2]
  if (values[0] === 1 && values[1] === 3 && values[2] === 2) {
    feedback.textContent = '✅ ¡Correcto! 30 < 50 < 60';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = '❌ Orden incorrecto. Recuerda: primero el resultado menor.';
    feedback.className = 'feedback incorrect';
  }
}
```

## Reglas
- Cada `<li>` tiene un `value` único que representa su posición correcta (1 = primero, 2 = segundo, etc.)
- El texto visible de cada `<li>` muestra el cálculo + resultado para ayudar al alumno
- Se requiere que los 3 radio buttons estén marcados antes de comprobar
- El feedback muestra el orden correcto si fallan
