# Patrones de Ejercicios Interactivos — Dibujo Técnico

## Tipos de ejercicio

### 1. Quiz de selección múltiple (4 opciones)
```html
<p><strong>Ejercicio N:</strong> Pregunta...</p>
<div class="quiz-options">
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Opción A</button>
  <button class="quiz-btn" onclick="checkAnswer(this, true, 'eN')">Opción B</button>
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Opción C</button>
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Opción D</button>
</div>
```
- Cada ejercicio tiene un ID único (`e1`, `e2`, ... o `r1`, `r2` para el interactivo)
- El botón correcto tiene `isCorrect=true`
- Al pulsar, se deshabilitan TODOS los botones del grupo
- No hay feedback div por ejercicio (usa el `#interactiveResult` compartido para el interactivo)

### 2. Completar texto
```html
<p><strong>Ejercicio N:</strong> Completa: ...</p>
<input type="text" class="fill-blank" id="fillN" placeholder="?">
<button onclick="checkFillN()" style="...">Comprobar</button>
<div class="result" id="fillResult"></div>
```
- Input con clase `fill-blank` (borde inferior punteado azul)
- Función JS específica por ejercicio (`checkFill1`, `checkFill2`, ...)
- Compara con `.trim().toLowerCase()` para ser flexible

### 3. Verdadero/Falso
```html
<p><strong>Ejercicio N:</strong> Afiración...</p>
<div class="tf-options">
  <button class="tf-btn" onclick="checkVF(this, true, 'eN')">Verdadero</button>
  <button class="tf-btn" onclick="checkVF(this, false, 'eN')">Falso</button>
</div>
<div class="result" id="vfResult"></div>
```
- Dos botones con clase `tf-btn`
- Función `checkVF(btn, isCorrect, resultId)`
- Feedback en div específico por ejercicio

### 4. Identificar afirmación correcta
```html
<p><strong>Ejercicio N:</strong> ¿Cuál de estas afirmaciones es CORRECTA?</p>
<div class="quiz-options">
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Incorrecta 1</button>
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Incorrecta 2</button>
  <button class="quiz-btn" onclick="checkAnswer(this, true, 'eN')">Correcta</button>
  <button class="quiz-btn" onclick="checkAnswer(this, false, 'eN')">Incorrecta 3</button>
</div>
```
- Mismo patrón que quiz pero con enfoque de "identificar la correcta entre incorrectas"

### 5. Multi-select checkboxes (2026-06-10)
```html
<p><strong>Ejercicio N:</strong> Selecciona TODAS las afirmaciones correctas:</p>
<div class="quiz-options" id="exN-options" style="flex-direction:column;align-items:flex-start">
  <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;padding:.4rem .8rem;border-radius:6px;border:2px solid var(--azul);margin:.3rem 0" onclick="this.style.background=this.style.background==='#eff6ff'?'#fff':'#eff6ff'">
    <input type="checkbox" id="exNa" style="width:18px;height:18px;cursor:pointer">
    <span>Afirmación A (correcta)</span>
  </label>
  <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer;padding:.4rem .8rem;border-radius:6px;border:2px solid var(--azul);margin:.3rem 0" onclick="this.style.background=this.style.background==='#eff6ff'?'#fff':'#eff6ff'">
    <input type="checkbox" id="exNb" style="width:18px;height:18px;cursor:pointer">
    <span>Afirmación B (incorrecta)</span>
  </label>
  <!-- más opciones... -->
</div>
<button onclick="checkExerciseN()" style="...">Comprobar</button>
<div class="result" id="exNResult"></div>
```
- Cada `<label>` envuelve un `<input type="checkbox">`
- El `onclick` del label alterna fondo azul claro al hacer click
- La función JS lee `.checked` de cada checkbox
- Valida combinaciones: `var correct = a && b && !c && d`
- Útil cuando hay varias respuestas correctas
- **2026-06-10:** usado en b03-01 para "selecciona TODAS las afirmaciones correctas sobre perspectiva isométrica"

## Funciones JS pattern

### checkAnswer(btn, isCorrect, resultId)
```javascript
function checkAnswer(btn, isCorrect, id) {
  var parent = btn.parentElement;
  var buttons = parent.querySelectorAll('.quiz-btn');
  buttons.forEach(function(b) { b.disabled = true; b.style.pointerEvents = 'none'; });
  if (isCorrect) {
    btn.classList.add('correct');
    // mostrar feedback positivo
  } else {
    btn.classList.add('wrong');
    // marcar la correcta
    // mostrar feedback negativo con explicación
  }
}
```

### checkVF(btn, isCorrect, resultId)
```javascript
function checkVF(btn, isCorrect, id) {
  var buttons = document.querySelectorAll('.tf-btn');
  buttons.forEach(function(b) { b.disabled = true; b.style.pointerEvents = 'none'; });
  var result = document.getElementById('vfResult');
  if (isCorrect) {
    btn.classList.add('correct');
    result.className = 'result ok';
    result.textContent = '✅ Correcto + explicación';
  } else {
    btn.classList.add('wrong');
    result.className = 'result fail';
    result.textContent = '❌ Incorrecto + explicación';
  }
}
```

### checkFillN()
```javascript
function checkFillN() {
  var input = document.getElementById('fillN').value.trim().toLowerCase();
  var result = document.getElementById('fillResult');
  if (input === 'respuesta1' || input === 'respuesta2') {
    result.className = 'result ok';
    result.textContent = '✅ Correcto';
  } else {
    result.className = 'result fail';
    result.textContent = '❌ Incorrecto. La respuesta es X.';
  }
}
```

### checkMultiSelectN() (2026-06-10)
```javascript
function checkExerciseN() {
  var a = document.getElementById('exNa').checked;
  var b = document.getElementById('exNb').checked;
  var c = document.getElementById('exNc').checked;
  var d = document.getElementById('exNd').checked;
  var result = document.getElementById('exNResult');
  // Correctas: a, b, d. Incorrecta: c
  var correct = a && b && !c && d;
  if (correct) {
    result.className = 'result ok';
    result.innerHTML = '✅ ¡Perfecto! Las correctas son: A, B y D.';
  } else {
    result.className = 'result fail';
    result.innerHTML = '❌ Las correctas son: A, B y D. C es incorrecta porque...';
  }
}
```
- Lee `.checked` de cada checkbox
- Valida combinación exacta con `&&` y `!`
- Feedback detallado indicando cuáles faltan o sobran

## Reglas de los ejercicios
1. **Siempre 4 ejercicios** por tema
2. **Mix de tipos:** quiz + completar + V/F + identificar (o multi-select)
3. **Feedback inmediato** con ✅/❌ y explicación
4. **Botones deshabilitados** tras respuesta (no permitir reintentos)
5. **IDs únicos** para cada ejercicio (`e1`, `e2`, `e3`, `e4`)
6. **El interactivo** usa `r1`, `r2`, `r3` con resultado compartido en `#interactiveResult`
7. **Específicos por pregunta:** para el interactivo, usar funciones dedicadas (`checkAngle`, `checkReduction`, `checkZ`) en vez de genéricas, para dar feedback contextualizado
