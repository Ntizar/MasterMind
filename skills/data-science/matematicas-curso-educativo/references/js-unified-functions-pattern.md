# Patrón de Funciones JS Unificadas — DeSumarIntegrar

## Contexto

Cuando se mejoran HTMLs de primaria con múltiples tipos de ejercicio nuevos, **no añadir funciones JS individuales con patch()**. En su lugar, reescribir todo el bloque JS con `write_file` usando funciones unificadas.

## Funciones unificadas

### 1. checkE(num, correct) — Completar hueco / Input numérico

```javascript
function checkE(num, correct) {
  const input = document.getElementById('e' + num);
  const feedback = document.getElementById('e' + num + '-fb');
  if (!input || !feedback) return;
  const value = parseInt(input.value);
  if (isNaN(value)) {
    feedback.textContent = 'Introduce un número';
    feedback.className = 'feedback incorrect';
    return;
  }
  if (value === correct) {
    feedback.textContent = '¡Correcto! 🎉';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = 'Incorrecto. La respuesta es ' + correct;
    feedback.className = 'feedback incorrect';
  }
}
```

**Uso:** Cualquier ejercicio con `<input type="number">` o `<input type="text">`.

### 2. checkVF(num, expected) — Verdadero/Falso con diccionario

```javascript
function checkVF(num, userAnswer) {
  const feedback = document.getElementById('e' + num + '-fb');
  // Diccionario: {ejercicio: respuesta_correcta}
  const answers = {5: true, 6: false};
  if (userAnswer === answers[num]) {
    feedback.textContent = '✅ ¡Correcto! ¡Muy bien!';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = '❌ ¡Casi! Piénsalo de nuevo.';
    feedback.className = 'feedback incorrect';
  }
}
```

**Uso:** Ejercicios VF con botones Verdadero/Falso. El diccionario permite que cada ejercicio tenga su respuesta correcta sin lógica hard-coded.

**Patrón VF invertido:** Para reforzar un concepto, añadir dos VF opuestos:
- e5: "1/2 > 1/4" → `answers[5] = true`
- e6: "1/4 > 1/2" → `answers[6] = false`

### 3. selectQuiz(num, btn, selected) — Quiz visual con botones

```javascript
function selectQuiz(num, btn, selected) {
  const feedback = document.getElementById('e' + num + '-fb');
  const correct = '1/2'; // respuesta correcta
  const buttons = btn.parentElement.querySelectorAll('button');
  buttons.forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  if (selected === correct) {
    feedback.textContent = '✅ ¡Correcto! 1/2 es la más grande.';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = '❌ No es ese. Recuerda: más partes = trozos más pequeños.';
    feedback.className = 'feedback incorrect';
  }
}
```

**Uso:** Ejercicios con `<div class="quiz-options">` y botones de opciones.

### 4. checkOrderN() — Ordenar con radio buttons

```javascript
function checkOrder9() {
  const feedback = document.getElementById('e9-fb');
  const radios = document.querySelectorAll('input[name="order9"]');
  const values = [];
  radios.forEach(r => { if (r.checked) values.push(parseInt(r.value)); });
  if (values.length < 3) {
    feedback.textContent = 'Selecciona el orden para los 3.';
    feedback.className = 'feedback incorrect';
    return;
  }
  // Correct order: 1/8 (value 1), 1/4 (value 2), 1/2 (value 3)
  if (values[0] === 1 && values[1] === 2 && values[2] === 3) {
    feedback.textContent = '✅ ¡Correcto! 1/8 < 1/4 < 1/2';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = '❌ Orden incorrecto. Recuerda: más partes = trozos más pequeños.';
    feedback.className = 'feedback incorrect';
  }
}
```

**Uso:** Ejercicios de ordenar con radio buttons. Cada `<li>` tiene un radio con `value` indicando su posición correcta en la secuencia.

## Regla de oro

**Cada función se usa para MÚLTIPLES ejercicios.** No crear una función por ejercicio. El número de ejercicio (`num`) es el identificador, no el nombre de la función.

## CSS necesario para VF y quiz

```css
.vf-buttons{display:flex;gap:.8rem;margin:.8rem 0}
.vf-buttons button{padding:.6rem 1.5rem;border:none;border-radius:8px;font-size:1rem;font-weight:600;cursor:pointer}
.vf-buttons button.vf-true{background:var(--verde);color:#fff}
.vf-buttons button.vf-false{background:var(--rojo);color:#fff}
.quiz-options{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;margin:.8rem 0}
.quiz-options button{padding:.6rem 1rem;border:2px solid #e2e8f0;border-radius:8px;background:#fff;font-size:1rem;cursor:pointer}
.quiz-options button:hover{border-color:var(--azul);background:var(--azul-claro)}
.quiz-options button.selected{border-color:var(--azul);background:var(--azul-claro)}
.order-list{list-style:none;padding:0}
.order-list li{padding:.5rem .8rem;margin:.3rem 0;background:#fff;border-radius:6px;border:1px solid #e2e8f0;display:flex;align-items:center;gap:.5rem}
.order-list li input[type="radio"]{width:20px;height:20px;cursor:pointer}
```

## Ejemplo completo: s02-5primaria.html

Antes (run 0): 2 ejercicios, funciones checkPizzaE1() y checkPizzaE2() separadas.
Después (run 16): 10 ejercicios, 4 funciones unificadas: checkE, checkVF, selectQuiz, checkOrder9.
