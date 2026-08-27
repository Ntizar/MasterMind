# Tipos de ejercicio para DeSumarIntegrar — Sesión 2026-06-10

## Tipos añadidos en esta sesión

### 16. Completar hueco inverso
**Cuándo:** El alumno debe hallar el dividendo. Entrena la relación inversa ÷→×.
**HTML:**
```html
<div class="exercise">
<p>🍫 <strong>Ejercicio (Completar hueco inverso):</strong> ___ ÷ 5 = 4</p>
<p style="font-size:0.9rem;color:#64748b">💡 Piensa: ¿Qué número dividido entre 5 da 4? Es decir: ? × 5 = 20</p>
<div class="exercise-input"><input type="number" id="eX"><button onclick="checkE(X, 20)">Comprobar</button></div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**Pedagogía:** Es más profundo que completar hueco normal porque obliga a pensar en la operación inversa.

### 17. Problema inverso con doble input
**Cuándo:** Conectar multiplicación y división como operaciones inversas.
**HTML:**
```html
<div class="exercise">
<p>🔄 <strong>Ejercicio (Problema inverso):</strong> Si 4 × 7 = 28, ¿cuánto es 28 ÷ 4? ¿Y 28 ÷ 7?</p>
<p style="font-size:0.9rem;color:#64748b">💡 La división es lo contrario de multiplicar. Si 4 × 7 = 28, entonces 28 ÷ 4 = 7 y 28 ÷ 7 = 4</p>
<div class="exercise-input">
<input type="number" id="eXa" placeholder="28÷4" style="width:80px"> + <input type="number" id="eXb" placeholder="28÷7" style="width:80px">
<button onclick="checkE14()">Comprobar</button>
</div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**JS:** Leer ambos inputs, verificar ambos valores correctos. Feedback debe explicar PORQUÉ: "Si 4×7=28, entonces 28÷4=7 y 28÷7=4".

### 18. Ordenar por texto libre (input con coma)
**Cuándo:** Ordenar 3-5 items con input de texto libre. Más flexible que radio buttons.
**HTML:**
```html
<div class="exercise">
<p>🔢 <strong>Ejercicio (Ordenar):</strong> Ordena de menor a mayor: 18÷3, 12÷4, 20÷5</p>
<p style="font-size:0.9rem;color:#64748b">💡 Calcula cada división y ordénalas</p>
<div class="exercise-input">
<input type="text" id="eX" placeholder="ej: 3,4,6">
<button onclick="checkOrden()">Comprobar</button>
</div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**JS:**
```javascript
function checkOrden() {
  const input = document.getElementById('eX').value;
  const fb = document.getElementById('eX-fb');
  const normalized = input.replace(/\s/g, '').toLowerCase();
  if (normalized === '3,4,6') {
    fb.className = 'feedback correct';
    fb.textContent = '✅ ¡Perfecto! 12÷4=3, 20÷5=4, 18÷3=6 → 3, 4, 6';
  } else {
    fb.className = 'feedback incorrect';
    fb.textContent = '❌ Recuerda: 18÷3=6, 12÷4=3, 20÷5=4. Ordena de menor a mayor.';
  }
}
```
**Ventaja:** No requiere tracking de clicks ni estado global. El alumno escribe la respuesta directamente.

## Regla de variedad (actualizada)
- **Ningún tipo debe superar 30% del total** de ejercicios
- **Mínimo 4 tipos diferentes** por tema
- Si un tipo aparece >3 veces → eliminar los peores repetitivos ANTES de añadir nuevos
