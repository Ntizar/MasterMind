# Catálogo de Tipos de Ejercicio — DeSumarIntegrar

## Regla de oro
**Antes de añadir ejercicios: leer el HTML y contar qué tipos YA existen. Solo añadir tipos ausentes.**

## Tipos de ejercicio

### 1. Quiz con botones
**Cuándo:** Conceptos simples, reconocimiento, memoria.
**HTML:**
```html
<div class="exercise">
<p>¿Cuántos lados tiene un triángulo?</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, true)">3</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">4</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">2</button>
</div>
</div>
```
**Regla:** Todas las opciones deben tener texto ÚNICO. Nunca repetir texto.

### 2. Completar hueco
**Cuándo:** Fórmulas, cálculos rápidos, completar datos.
**HTML:**
```html
<div class="exercise">
<p>Completa: Un triángulo tiene ___ lados.</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, false)">4</button>
<button class="quiz-btn" onclick="checkExercise(this, true)">3</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">5</button>
</div>
</div>
```

### 3. Verdadero / Falso
**Cuándo:** Detectar errores conceptuales, afirmaciones que confunden.
**HTML:**
```html
<div class="exercise">
<p>Verdadero o Falso: Un cuadrado tiene 4 lados iguales.</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkVF(this, true)">Verdadero ✅</button>
<button class="quiz-btn" onclick="checkVF(this, false)">Falso ❌</button>
</div>
</div>
```
**Tip:** Usar afirmaciones que los alumnos suelen creer falsas (ej: "el círculo tiene muchos lados").
**JS:** `checkVF(btn, isCorrect)` — ver SKILL.md.

### 4. Ordenar
**Cuándo:** Comparar magnitudes, rangos, progresiones.
**HTML:**
```html
<div class="exercise">
<p>Ordena de menos a más lados: círculo, triángulo, cuadrado.</p>
<div id="sortExercise" style="display:flex;gap:.5rem;flex-wrap:wrap;margin:.5rem 0">
<button class="quiz-btn" onclick="sortCheck(this,'circulo')" data-shape="circulo">⭕ Círculo</button>
<button class="quiz-btn" onclick="sortCheck(this,'triangulo')" data-shape="triangulo">🔺 Triángulo</button>
<button class="quiz-btn" onclick="sortCheck(this,'cuadrado')" data-shape="cuadrado">🟧 Cuadrado</button>
</div>
<div id="sortResult" class="result" style="display:none"></div>
</div>
```
**JS:** `sortCheck(btn, shape)` — ver SKILL.md para implementación completa.
**Nota:** El número de items debe coincidir con `selected.length === N` en la función.

### 5. Ordenar por texto (múltiple choice)
**Cuándo:** Ordenar 3-5 items con opciones predefinidas. Más robusto que el click-order para primaria.
**HTML:**
```html
<div class="exercise">
<p><b>Ordena de más ligero a más pesado:</b></p>
<p>🪶 pluma &nbsp; 📱 móvil &nbsp; 📚 libro</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkOrden(this, ['pluma','movil','libro'])">Pluma → Móvil → Libro</button>
<button class="quiz-btn" onclick="checkOrden(this, ['libro','movil','pluma'])">Libro → Móvil → Pluma</button>
<button class="quiz-btn" onclick="checkOrden(this, ['pluma','libro','movil'])">Pluma → Libro → Móvil</button>
</div>
</div>
```
**JS:** `checkOrden(btn, correctOrder)` — ver SKILL.md para implementación completa.
**Ventaja:** No requiere tracking de clicks ni estado global. El botón correcto se identifica por su texto.

### 6. Problema contextualizado
**Cuándo:** Aplicar múltiples pasos, conectar con vida real.
**HTML:**
```html
<div class="exercise">
<p>Si tienes 3 ventanas en forma de rectángulo y 2 ventanas en forma de cuadrado, ¿cuántas esquinas hay en total?</p>
<p style="font-size:0.85rem;color:#64748b;margin-bottom:.5rem">Pista: un rectángulo tiene 4 vértices y un cuadrado también</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, false)">5</button>
<button class="quiz-btn" onclick="checkExercise(this, true)">20</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">10</button>
</div>
</div>
```
**Regla:** Incluir pista para alumnos que se atasquen.

### 7. Problema de cálculo
**Cuándo:** Operaciones, fórmulas, aplicar reglas.
**HTML:**
```html
<div class="exercise">
<p>Si un triángulo tiene 3 lados y cada lado mide 5 cm, ¿cuánto mide el perímetro?</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, true)">15 cm</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">8 cm</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">10 cm</button>
</div>
</div>
```

### 8. Input de texto (ESO+)
**Cuándo:** Cálculos libres, respuestas abiertas.
**HTML:**
```html
<div class="exercise">
<p>Resuelve: 2x + 5 = 15. ¿Cuánto vale x?</p>
<div class="exercise-input">
<input type="text" id="exX" placeholder="Tu respuesta">
<button onclick="checkExercise('exX', '5', this)">Comprobar</button>
</div>
<p class="feedback"></p>
</div>
```

### 9. Sección intermedia de teoría
**Cuándo:** Un tema tiene dos dimensiones (ej: tamaño Y peso) y la estructura original solo cubre una.
**Patrón:** Insertar una nueva `<section class="chapter">` entre la sección de teoría existente y los ejercicios, con su propia `box-teoria` + `box-ejemplo`. Esto evita que el alumno confunda dos conceptos distintos.

### 10. Encontrar la regla
**Cuándo:** El alumno debe identificar la operación o patrón que genera una secuencia. Es el paso siguiente a "completar hueco" — requiere comprensión profunda.
**HTML:**
```html
<div class="exercise">
<p>🧠 <b>Encuentra la regla:</b> En la secuencia 2, 4, 6, 8, ¿qué regla sigue?</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, false)">Sumar 1</button>
<button class="quiz-btn" onclick="checkExercise(this, true)">Sumar 2</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">Restar 2</button>
</div>
</div>
```
**Pedagogía:** Este tipo de ejercicio es más profundo que completar hueco porque obliga al alumno a abstraer la regla, no solo aplicar un patrón mecánico.
**Tip:** Para primaria, usar reglas simples (sumar X, restar X). Para ESO+, usar reglas más complejas (multiplicar por X, patrón alternado).

### 11. Identificar NO-patrón / NO-ejemplo
**Cuándo:** El alumno debe distinguir qué elemento NO pertenece a un conjunto o secuencia. Desarrolla pensamiento crítico y capacidad de discriminación.
**HTML:**
```html
<div class="exercise">
<p>🧩 <b>¿Cuál NO es un patrón?</b></p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, false)">🔴🔵🔴🔵🔴🔵</button>
<button class="quiz-btn" onclick="checkExercise(this, true)">🔴🟡🟢🔵🟣⚫</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">⭐🌙⭐🌙⭐🌙</button>
</div>
</div>
```
**Pedagogía:** Reconocer qué NO es algo es tan importante como reconocer qué SÍ lo es. Este ejercicio fuerza al alumno a analizar cada opción, no solo buscar la respuesta correcta.
**Variantes:** "¿Cuál NO es un número par?", "¿Cuál NO es un triángulo?", "¿Cuál NO tiene patrón de repetición?"

### 12. Crear tu propio patrón / ejemplo
**Cuándo:** El alumno debe identificar el tipo o estructura de algo que genera. Es el nivel más alto de comprensión (Bloom: crear).
**HTML:**
```html
<div class="exercise">
<p>🎨 <b>Crea tu patrón:</b> Si tuvieras 6 fichas: 🟡🟡🟢🟡🟡🟢, ¿qué patrón formaría?</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, true)">AAB (dos amarillas, una verde)</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">AB (una amarilla, una verde)</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">ABC (tres colores)</button>
</div>
</div>
```
**Pedagogía:** Identificar la estructura de un patrón dado es más profundo que completarlo. Requiere abstracción.

### 13. Completar ritmo / secuencia auditiva
**Cuándo:** Para temas donde el patrón se presenta como ritmo, sonido o secuencia temporal. Conecta con la música y el movimiento.
**HTML:**
```html
<div class="exercise">
<p>🎵 <b>Completa el ritmo:</b> Escucha este ritmo: ta-ta-pausa, ta-ta-pausa, ta-ta-___</p>
<div class="quiz-options">
<button class="quiz-btn" onclick="checkExercise(this, true)">pausa</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">ta</button>
<button class="quiz-btn" onclick="checkExercise(this, false)">ta-ta</button>
</div>
</div>
```
**Pedagogía:** Los patrones no son solo visuales. Conectar con el ritmo musical hace el concepto más tangible para niños pequeños.

## Patrón de análisis previo

```python
# Antes de añadir ejercicios, contar tipos existentes:
import re
with open(file) as f:
    html = f.read()

quiz = len(re.findall(r'quiz-btn', html))
sort = 'sortCheck' in html or 'checkOrden' in html
input_text = 'exercise-input' in html
v_f = 'Verdadero' in html and 'Falso' in html
hueco = 'Completa:' in html or '___' in html
regla = 'Encuentra la regla' in html or 'regla' in html.lower()
no_patron = 'NO' in html and ('patrón' in html or 'ejemplo' in html)
crear = 'Crea tu' in html or 'Crear tu' in html

print(f"Quiz: {quiz//3} | Ordenar: {sort} | Input: {input_text} | V/F: {v_f} | Hueco: {hueco} | Regla: {regla} | NO-patrón: {no_patron} | Crear: {crear}")
```

### 14. Emparejar sumas iguales (equivalencia) — NUEVO 2026-06-10
**Cuándo:** El alumno debe encontrar qué otra suma produce el MISMO resultado. Entrena el pensamiento algebraico temprano.
**HTML:**
```html
<div class="exercise">
<p>🧩 ¿Qué suma es IGUAL a 5 + 3?</p>
<div class="quiz-options">
<button onclick="checkMatch(this, false)">4 + 4</button>
<button onclick="checkMatch(this, true)">6 + 2</button>
<button onclick="checkMatch(this, false)">7 + 3</button>
</div>
<div class="feedback" id="eX-fb"></div>
<p style="font-size:0.9rem;color:#64748b;margin-top:0.3rem">💡 5+3=8. Busca la que también dé 8.</p>
</div>
```
**JS:** `checkMatch(btn, correct)` — ver SKILL.md para implementación completa.
**Pedagogía:** Este tipo de ejercicio es diferente del quiz normal porque el alumno no calcula un resultado, sino que encuentra equivalencia. Es un puente hacia el álgebra.
**Regla:** La respuesta correcta debe ser una suma con números diferentes pero mismo resultado. Las incorrectas deben ser plausibles (resultados cercanos).

### 15. Conteo visual con emojis — NUEVO 2026-06-10
**Cuándo:** Conectar la abstracción numérica con lo visual. Ideal para primaria baja.
**HTML:**
```html
<div class="exercise">
<p>🍎🍎🍎 + 🍎🍎🍎🍎🍎 = ¿Cuántos hay en total?</p>
<div class="emoji-big">🍎🍎🍎 ➕ 🍎🍎🍎🍎🍎</div>
<div class="exercise-input">
<input type="number" id="eX" placeholder="?">
<button onclick="checkE(X, 8)">Comprobar</button>
</div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**Pedagogía:** El alumno ve los emojis y los cuenta. Conecta el símbolo numérico con la cantidad visual. Diferente del input directo porque el enunciado visual es la pregunta, no un número abstracto.

## Patrón de análisis previo

```python
# Antes de añadir ejercicios, contar tipos existentes:
import re
with open(file) as f:
    html = f.read()

quiz = len(re.findall(r'quiz-btn', html))
sort = 'sortCheck' in html or 'checkOrden' in html
input_text = 'exercise-input' in html
v_f = 'Verdadero' in html and 'Falso' in html
hueco = 'Completa:' in html or '___' in html
regla = 'Encuentra la regla' in html or 'regla' in html.lower()
no_patron = 'NO' in html and ('patrón' in html or 'ejemplo' in html)
crear = 'Crea tu' in html or 'Crear tu' in html
emparejar = 'checkMatch' in html or 'emparejar' in html.lower()
conteo_visual = 'emoji-big' in html and 'Comprobar' in html

print(f"Quiz: {quiz//3} | Ordenar: {sort} | Input: {input_text} | V/F: {v_f} | Hueco: {hueco} | Regla: {regla} | NO-patrón: {no_patron} | Crear: {crear} | Emparejar: {emparejar} | Conteo visual: {conteo_visual}")
```

### 16. Decidir operación (sumar vs restar) — NUEVO 2026-06-10
**Cuándo:** El alumno debe identificar CUÁL operación aplicar a un problema contextual, no calcular el resultado. Entrena la comprensión conceptual antes del cálculo.
**HTML:**
```html
<div class="exercise">
<p>🎬 <b>¿Qué operación?</b> En el cine había 16 personas. Salieron 7 al acabar la película. ¿Cuántas quedan?</p>
<p>¿Sumamos o restamos?</p>
<div style="display:flex;gap:0.8rem;margin:.8rem 0;flex-wrap:wrap">
<button onclick="checkOperacion(X, true)" style="background:var(--verde);color:#fff;border:none;padding:.6rem 1.5rem;border-radius:8px;cursor:pointer;font-size:1rem;font-weight:600">➖ Restar: 16 - 7 = 9</button>
<button onclick="checkOperacion(X, false)" style="background:var(--azul);color:#fff;border:none;padding:.6rem 1.5rem;border-radius:8px;cursor:pointer;font-size:1rem;font-weight:600">➕ Sumar: 16 + 7 = 23</button>
</div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**JS:** `checkOperacion(num, esRestar)` — `true` si el alumno eligió restar correctamente, `false` si eligió sumar.
**Pedagogía:** Muchos alumnos calculan rápido pero no saben CUÁNDO sumar o restar. Este ejercicio fuerza la comprensión antes del cálculo.
**Regla:** El enunciado debe tener palabras clave claras: "salieron/quitaron/perdieron" → restar; "llegaron/añadieron/ganaron" → sumar.

### 17. Emparejar: identificar pareja INCORRECTA — NUEVO 2026-06-10
**Cuándo:** El alumno debe analizar pares de restas/sumas y encontrar cuál NO coincide. Diferente del tipo 14 (emparejar sumas iguales) porque aquí el objetivo es encontrar la pareja INCORRECTA, no la correcta.
**HTML:**
```html
<div class="exercise">
<p>🔗 <b>¿Cuál pareja es INCORRECTA?</b> Une cada resta con su pareja que da el mismo resultado:</p>
<p>🅰️ 10 - 4 = <strong>6</strong> &nbsp;&nbsp; 🔵 12 - 6 = <strong>6</strong><br>
🅱️ 15 - 8 = <strong>7</strong> &nbsp;&nbsp; 🔵 9 - 2 = <strong>7</strong><br>
🅲️ 11 - 5 = <strong>6</strong> &nbsp;&nbsp; 🔵 8 - 3 = <strong>5</strong></p>
<p>¿Qué pareja NO da el mismo resultado?</p>
<div style="display:flex;gap:0.8rem;margin:.8rem 0;flex-wrap:wrap">
<button onclick="checkEmparejar(X, false)" style="background:var(--azul);color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;font-weight:600">🅰️-🔵 (6 y 6)</button>
<button onclick="checkEmparejar(X, true)" style="background:var(--azul);color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;font-weight:600">🅲️-🔵 (6 y 5)</button>
<button onclick="checkEmparejar(X, false)" style="background:var(--azul);color:#fff;border:none;padding:.6rem 1.2rem;border-radius:8px;cursor:pointer;font-size:1rem;font-weight:600">🅱️-🔵 (7 y 7)</button>
</div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**JS:** `checkEmparejar(num, esIncorrecta)` — `true` si el alumno identificó correctamente la pareja INCORRECTA.
**Pedagogía:** Forzar al alumno a verificar TODAS las opciones, no solo buscar la correcta. Desarrolla pensamiento crítico y verificación.
**Diferencia con tipo 14:** Tipo 14 = "encuentra la pareja correcta" (positivo). Tipo 17 = "encuentra la pareja INCORRECTA" (negativo). Más difícil, más profundo.

### 18. Ordenar por resultado (cálculo + comparación) — NUEVO 2026-06-10
**Cuándo:** El alumno debe calcular el resultado de varias operaciones y luego ordenarlas. Combina cálculo con comparación.
**HTML:**
```html
<div class="exercise">
<p>📊 <b>De mayor a menor resultado:</b></p>
<p>🅰️ 15 - 8 = <input type="number" id="o1" style="width:60px;padding:.4rem;border:2px solid #e2e8f0;border-radius:6px;font-size:1rem"> &nbsp;&nbsp;
🅱️ 12 - 5 = <input type="number" id="o2" style="width:60px;padding:.4rem;border:2px solid #e2e8f0;border-radius:6px;font-size:1rem"> &nbsp;&nbsp;
🅲️ 10 - 3 = <input type="number" id="o3" style="width:60px;padding:.4rem;border:2px solid #e2e8f0;border-radius:6px;font-size:1rem"></p>
<p>¿Cuál tiene el resultado <strong>más grande</strong>? <input type="number" id="o4" placeholder="?" style="width:60px;padding:.4rem;border:2px solid #e2e8f0;border-radius:6px;font-size:1rem"></p>
<div class="exercise-input"><button onclick="checkOrden2()" style="background:var(--azul);color:#fff;border:none;padding:.5rem 1.2rem;border-radius:8px;cursor:pointer;font-weight:600;font-size:1rem">Comprobar</button></div>
<div class="feedback" id="eX-fb"></div>
</div>
```
**JS:** `checkOrden2()` — verifica cada resultado individual y el mayor/menor.
**Pedagogía:** Combina dos habilidades: calcular y comparar. Útil cuando el alumno ya sabe operar pero necesita practicar la relación entre resultados.
**Variante:** Si todas las operaciones dan el mismo resultado, el ejercicio enseña que resultados iguales pueden venir de operaciones diferentes (ej: 15-8=7, 12-5=7, 10-3=7).

### 19. Emparejar dos columnas (match pairs) — NUEVO 2026-06-10
**Cuándo:** El alumno debe emparejar elementos de dos columnas (ej: resta con su resultado). Entrena la asociación visual y la memoria de relaciones.
**HTML:**
```html
<div class="exercise">
<p>🔗 Empareja cada resta con su resultado. Pulsa la resta y luego su resultado:</p>
<div style="display:flex;gap:2rem;justify-content:center;flex-wrap:wrap;margin:1rem 0">
<div>
<p style="font-weight:600;margin-bottom:.5rem;color:var(--azul)">Resta</p>
<button class="quiz-btn" id="match1" onclick="matchPair(this,'m1')">12 − 5</button>
<button class="quiz-btn" id="match2" onclick="matchPair(this,'m2')">16 − 6</button>
<button class="quiz-btn" id="match3" onclick="matchPair(this,'m3')">11 − 11</button>
</div>
<div>
<p style="font-weight:600;margin-bottom:.5rem;color:var(--naranja)">Resultado</p>
<button class="quiz-btn" id="matchA" onclick="matchPair(this,'m3')">0</button>
<button class="quiz-btn" id="matchB" onclick="matchPair(this,'m1')">7</button>
<button class="quiz-btn" id="matchC" onclick="matchPair(this,'m2')">10</button>
</div>
</div>
<div class="result" id="eXresult" style="display:none;text-align:center"></div>
</div>
```
**JS:** `matchPair(btn, pairId)` — estado global `matchState = { selected: null, matched: new Set(), pairs: 0 }`. Al primer clic marca amarillo; al segundo clic compara pairId. Si coinciden → verde y deshabilita. Si no → rojo temporal.
**Pedagogía:** Diferente del quiz normal porque el alumno NO calcula un resultado sino que asocia dos elementos. Diferente de tipo 14 (emparejar sumas iguales) porque aquí son dos columnas separadas con estado de selección.
**Regla:** Cada par debe tener un `pairId` único. Las columnas deben estar claramente etiquetadas. El feedback final debe listar todos los pares emparejados.
**Diferencias con tipos 14 y 17:**
- Tipo 14: "¿qué suma es igual?" — un solo grupo de opciones
- Tipo 17: "¿cuál pareja es INCORRECTA?" — identificar la errónea
- Tipo 19: dos columnas separadas, emparejar TODOS los pares correctamente

## Checklist post-mejora

- [ ] ¿Hay al menos 4 tipos diferentes de ejercicio?
- [ ] ¿Cada tipo aparece como máximo 3 veces?
- [ ] ¿Todas las opciones de quiz tienen texto único?
- [ ] ¿Los problemas tienen pista?
- [ ] ¿El JS de sortCheck coincide con el número de items?
- [ ] ¿Hay al menos un ejercicio de tipo profundo (regla, NO-patrón, crear)?
