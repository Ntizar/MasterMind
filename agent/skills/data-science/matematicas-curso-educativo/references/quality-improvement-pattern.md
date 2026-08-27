# Patrón de Mejora de Calidad — DeSumarIntegrar

## Cuándo usarlo

Cuando el cron de mejora continua o un agente manual necesita mejorar la calidad de un HTML existente sin añadir cantidad innecesaria.

## Procedimiento

### 1. Leer estado
```
read_file("/root/workspace/DeSumarIntegrar/progress.json")
```
Extraer: priority, status, improvement_count, scores actuales.

### 2. Seleccionar tema
- Prioridad 1 (pending) → Prioridad 2 → Prioridad 3
- Si improvement_count >= 4, saltar (máximo alcanzado)
- Si improvement_count < 4, puede mejorar
- **Criterio de selección:** elegir el tema con MENOR score total primero. Si empatados, menor difficulty_range primero.

### 3. Leer HTML y ANALIZAR (CRÍTICO)
**NO asumir qué falta. Leer el archivo real.**

Mapeo: las keys de progress.json NO son nombres de archivo reales.
```python
import os
filepath = f"/root/workspace/DeSumarIntegrar/{progress_key}"
if not os.path.exists(filepath):
    # Buscar archivo real con ls o find
    pass
```

Contar y analizar:
- Tipos de ejercicio existentes (quiz, completar hueco, V/F, ordenar, problema contextualizado, input numérico, problema inverso)
- Casos reales (¿genéricos como "sumar sirve para contar" o cotidianos como "supermercado con latas de atún"?)
- Visualizaciones (canvas, Plotly) — ¿aportan al aprendizaje o son decorativas?
- Cajas de error común (¿existen?)
- Conexiones con otros temas (¿existen?)
- Errores de contenido (ej: resta en página de suma, opciones duplicadas en quiz)

### 4. Planificar mejoras (solo lo que falta)

**Regla de oro: Si un ejercicio no aporta conocimiento nuevo, NO lo añadas.**

**Tipos de ejercicio a añadir (si faltan):**
1. Completar hueco: `X + ___ = Y` (el alumno completa el sumando)
2. Verdadero/Falso: `X + Y = Z → Falso` (detecta errores conceptuales)
3. Problema contextualizado: "En un autobús hay 425 pasajeros..." (historia, no genérico)
4. Ordenar: "Ordena de menor a mayor" (comparar magnitudes)
5. Problema inverso: "Quieres 15 galletas, ya hiciste 8. ¿Cuántas faltan?" (pensamiento reverso)
6. Input numérico directo: `X + Y = ?` (solo si no existe)

**Regla de variedad:** Máximo 5-8 ejercicios por tema, cada uno de tipo DIFERENTE. NO repitas el mismo tipo más de 2 veces.

**Patrones de mejora estructural (no solo ejercicios):**
- **Explicación estructurada:** Formato 4 preguntas (¿qué es? ¿para qué? ¿cómo? ¿error común?) — reemplaza bloques de texto plano.
- **Caja de error común:** `box-error` con "⚠️ Error típico: ..." — siempre aporta valor.
- **Caja de conexión:** `box-idea` con "🔗 Conexión: [tema] y [otro tema]" — conecta conceptos.
- **Casos reales:** Deben ser cotidianos y específicos. ❌ "Sumar sirve para contar" ✅ "Tu equipo marcó 2 goles en la primera mitad y 3 en la segunda. ¿Cuántos goles marcó en total?"

### 5. Eliminar contenido problemático

Antes de añadir, limpiar:
- ❌ Ejercicios de otro tema (ej: resta en página de suma)
- ❌ Ejercicios repetitivos del mismo tipo (ej: 7 quizzes de botones idénticos)
- ❌ Opciones duplicadas en quiz (dos botones con el mismo texto)

### 6. Insertar con write_file o patch

- **write_file:** archivo ≤ 20KB y 3+ cambios estructurales
- **patch:** cambios puntuales (1-2 secciones, CSS nuevo)
- Insertar ejercicios ANTES del `<div class="summary">`
- Insertar casos reales y cajas ANTES de los ejercicios
- Insertar funciones JS nuevas ANTES de las funciones existentes

### 7. Verificar calidad (antes de escribir)

Para CADA ejercicio propuesto, preguntar:
1. ¿Este ejercicio es diferente a los demás?
2. ¿Aporta algo nuevo al alumno?
3. ¿La respuesta es correcta?
4. ¿El enunciado es claro?

Si alguna respuesta es "no", NO añadir.

### 8. Verificación post-patch (CRÍTICO)

Después de CADA patch en HTML, verificar:
1. **Etiquetas rotas:** `grep -c '<li><li>' archivo` → debe ser 0
2. **Balance de tags:** `grep -c '<section' archivo` == `grep -c '</section>' archivo`
3. **Balance de li:** `grep -c '<li>' archivo` == `grep -c '</li>' archivo`
4. **Funciones JS duplicadas:** `grep -c 'function nombre' archivo` → debe ser 1
5. **Cierre HTML:** `tail -3 archivo` debe terminar con `</script></body></html>`

Si algo falla, hacer un patch corrector antes de commit.

### 9. Git commit + push + actualizar progress.json

## Ejemplos de funciones JS

### checkVF — Verdadero/Falso (botón directo)
```javascript
function checkVF(btn, isCorrect) {
  const parent = btn.parentElement;
  parent.querySelectorAll('button').forEach(b => {
    b.disabled = true;
    b.classList.remove('correct','wrong');
  });
  btn.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = document.getElementById('e3-fb');
  fb.textContent = isCorrect ? '✅ ¡Correcto! 8 + 6 = 14, es verdadero.' : '✅ ¡Bien pensado! 8 + 6 = 14.';
  fb.className = 'feedback correct';
}
```

### checkOrden — Ordenar de menor a mayor
```javascript
let ordenarStep = 0;
let ordenarOrder = [1, 2, 3]; // valores esperados en orden
function checkOrden(btn, value) {
  ordenarStep++;
  if (value === ordenarOrder[ordenarStep - 1]) {
    btn.classList.add('correct');
    btn.disabled = true;
    if (ordenarStep === 3) {
      document.getElementById('e5-fb').textContent = '✅ ¡Perfecto! 3+2=5 < 5+5=10 < 7+4=11';
      document.getElementById('e5-fb').className = 'feedback correct';
    }
  } else {
    btn.classList.add('wrong');
    btn.disabled = true;
    document.getElementById('e5-fb').textContent = '❌ Ese no es el siguiente. Piensa: ¿cuál suma da menos?';
    document.getElementById('e5-fb').className = 'feedback incorrect';
    ordenarStep = 0;
    setTimeout(() => {
      document.querySelectorAll('#ordenar-quiz button').forEach(b => {
        b.disabled = false;
        b.classList.remove('correct','wrong');
      });
      document.getElementById('e5-fb').textContent = '';
    }, 1500);
  }
}
```

## Scores objetivo tras mejora

| Score | Objetivo |
|-------|----------|
| exercises | 6-10 (variedad, no cantidad) |
| text | 10-12 |
| visual | 3-4 |
| real_world | 8+ |
| connections | 2+ |
| difficulty_range | 5-6 |

## Lecciones aprendidas (2026-06-10)

### Lección: Eliminar > Añadir
Cuando un tema tiene muchos ejercicios repetitivos del mismo tipo (ej: 10 quizzes de botones), NO añadir más del mismo tipo. En su lugar:
1. Eliminar los ejercicios repetitivos
2. Reemplazarlos con ejercicios de tipos diferentes
3. El resultado final puede tener MENOS ejercicios pero MÁS variedad y valor

### Lección: Verificar coherencia temática
Antes de añadir un ejercicio, verificar que NO sea de otro tema. Ejemplo: un ejercicio de resta en una página de sumar confunde al alumno. Siempre verificar el contexto del tema.

### Lección: Conexiones = score 0 → 1+
Los temas con score `connections=0` suelen necesitar al menos una caja `box-idea` que conecte el tema actual con otro ya aprendido (ej: "sumar conecta con contar porque..."). Esto eleva el score de conexiones y refuerza el aprendizaje.

### Pitfall: botones de quiz con parámetro booleano (2026-06-10)
Cuando se usa `checkQuiz(num, isCorrect)` con parámetro booleano, TODOS los botones deben pasar `true` o `false`. **NUNCA pasar un número** (como el valor de la respuesta). Python/JS trata `5` como `True` (truthy), por lo que el primer botón incorrecto se marcaría como correcto.

**Patrón correcto:**
```html
<button onclick="checkQuiz(11, false)">4</button>
<button onclick="checkQuiz(11, true)">5</button>
<button onclick="checkQuiz(11, false)">6</button>
<button onclick="checkQuiz(11, false)">8</button>
```

**Patrón incorrecto (bug):**
```html
<button onclick="checkQuiz(11, 5)">4</button>  <!-- 5 es truthy → se marca como correcto -->
<button onclick="checkQuiz(11, true)">5</button>
```

### Pitfall: página índice vs página de lección (2026-06-10)
Algunos archivos en progress.json son páginas índice/overview que listan sesiones pero NO tienen ejercicios interactivos. Ejemplos: `s04-4primaria.html`, `s07-1eso.html`, `s08-2-3eso.html`.

**Detección:** si el HTML no contiene `<div class="exercise">` ni `<div class="interactive">`, es un índice.

**Acción diferenciada según tipo:**

- **Página de lección** (tiene ejercicios) → mejorar con ejercicios variados, casos reales, cajas pedagógicas (ver sección "Planificar mejoras" arriba).
- **Página índice/landing** (sin ejercicios, solo session cards) → mejorar con:
  1. **Mini quiz interactivo** (1 pregunta engancha antes de empezar) — captura atención, no evalúa
  2. **Diseño glassmorphism** — gradientes, backdrop-filter, hover en tarjetas
  3. **Tags por categoría** — cada sesión con tag temático (Fracciones, Decimales, Geometría...)
  4. **Caja intro con objetivos claros** — 5-8 objetivos concretos y medibles
  5. **CSS mejorado** — tarjetas con hover, transiciones, diseño moderno

**NO añadir ejercicios de lección a páginas índice.** El objetivo es hacer la página de navegación más atractiva y funcional, no convertirla en una lección.

**Ejemplo de mini quiz para landing page:**
```html
<div class="mini-quiz" id="miniQuiz">
<h3>🎯 ¡Pruébalo antes de empezar!</h3>
<p>Si repartes 3 pizzas entre 4 amigos, ¿qué parte de pizza le toca a cada uno?</p>
<div class="quiz-options">
<button onclick="checkQuiz(0)">3/4 ✅</button>
<button onclick="checkQuiz(1)">1/4</button>
<button onclick="checkQuiz(2)">1/3</button>
</div>
<div class="quiz-feedback" id="quizFeedback"></div>
</div>
```

**JS mínimo para landing quiz:**
```javascript
function checkQuiz(index) {
  const buttons = document.querySelectorAll('#quizOptions button');
  const feedback = document.getElementById('quizFeedback');
  buttons.forEach(b => { b.disabled = true; b.classList.remove('correct','wrong'); });
  buttons[index].classList.add('correct');
  feedback.textContent = '✅ ¡Exacto! 3 pizzas entre 4 amigos → cada uno se lleva 3/4. ¡Descúbrelo en la sesión 1!';
  feedback.className = 'quiz-feedback correct';
}
```

**CSS necesario para mini-quiz:**
```css
.mini-quiz{background:linear-gradient(135deg,var(--azul-claro),var(--naranja-claro));border-radius:16px;padding:1.5rem;margin:2rem 0;border:2px solid var(--azul)}
.quiz-options{display:flex;gap:.5rem;flex-wrap:wrap;margin:.8rem 0}
.quiz-options button{flex:1;min-width:100px;padding:.7rem 1rem;border:2px solid #e2e8f0;border-radius:10px;background:#fff;cursor:pointer;font-size:1rem;font-weight:600;transition:all .2s}
.quiz-options button:hover{border-color:var(--azul);background:var(--azul-claro);transform:scale(1.03)}
.quiz-options button.correct{background:var(--verde);color:#fff;border-color:var(--verde)}
.quiz-options button.wrong{background:var(--rojo);color:#fff;border-color:var(--rojo)}
.quiz-options button:disabled{opacity:.6;cursor:not-allowed;transform:none}
.quiz-feedback{font-size:1rem;font-weight:600;margin:.5rem 0}
.quiz-feedback.correct{color:var(--verde)}
.quiz-feedback.wrong{color:var(--rojo)}
```

### Pattern: Canvas de línea numérica interactiva — NUEVO 2026-06-10
Para temas de suma/resta en primaria, un canvas de línea numérica es MUY efectivo pedagógicamente. Diferente del SVG recta numérica (eso1-enteros): este usa canvas 2D con saltos visuales.

**Estructura:**
1. Dibujar línea horizontal con ticks y números (0-20)
2. Primer salto en azul: `a` pasos desde 0
3. Segundo salto en naranja: `b` pasos desde el punto anterior
4. Resultado en verde en el punto final

**Pedagogía:** El alumno "ve" la suma como saltos de rana en la línea. Conecta la operación abstracta con movimiento espacial.

**JS clave:**
```javascript
function nuevaLinea() {
  const a = Math.floor(Math.random() * 5) + 1;
  const b = Math.floor(Math.random() * 5) + 1;
  const canvas = document.getElementById('canvas-linea');
  const ctx = canvas.getContext('2d');
  // ... dibujar línea, ticks, saltos con quadraticCurve
  window._lineaA = a;
  window._lineaB = b;
}
```

**Diferencia con SVG recta numérica:** Canvas = animación interactiva con saltos (primaria). SVG = recta interactiva con clic (ESO enteros). Ver `references/svg-recta-numerica.md`.

### Pattern: checkMatch — Emparejar sumas iguales
Para tipo de ejercicio "emparejar sumas iguales" (tipo 14 del catálogo).

**JS:**
```javascript
function checkMatch(btn, correct) {
  const parent = btn.parentElement;
  parent.querySelectorAll('button').forEach(b => {
    b.disabled = true;
    b.classList.remove('correct','wrong');
  });
  btn.classList.add(correct ? 'correct' : 'wrong');
  const fb = document.getElementById('e7-fb');
  if (correct) {
    fb.textContent = '✅ ¡Correcto! 6+2=8, igual que 5+3=8';
    fb.className = 'feedback correct';
  } else {
    fb.textContent = '❌ No es esa. Busca la que también dé 8.';
    fb.className = 'feedback incorrect';
  }
}
```

**Regla:** Usar `true`/`false` explícitamente, NUNCA números (bug de booleano).

### Pattern: Input numérico con pista contextual — NUEVO 2026-06-10
Para ejercicios de completar hueco numérico (patrón +3, patrón inverso +5, etc.), usar input con **pista contextual** en vez de solo "correcto/incorrecto".

**Estructura:**
```html
<div class="exercise">
<p>✏️ <b>Completa el hueco:</b> En el patrón 3, 6, 9, 12, ___ el siguiente número es:</p>
<div style="display:flex;align-items:center;gap:.8rem;margin:.5rem 0">
<input type="number" class="input-pattern" id="patInput1" placeholder="?">
<button class="quiz-btn" style="background:var(--azul);color:#fff;border:none" onclick="checkInputPat1()">Comprobar</button>
</div>
<div class="result" id="patResult1"></div>
</div>
```

**CSS:**
```css
.input-pattern{width:60px;padding:.4rem;border:2px solid var(--azul);border-radius:6px;font-size:1rem;text-align:center;font-weight:700}
.input-pattern:focus{outline:none;border-color:var(--naranja);box-shadow:0 0 0 3px rgba(249,115,22,.2)}
```

**JS con pista contextual:**
```javascript
function checkInputPat1(){
  const input = document.getElementById('patInput1');
  const result = document.getElementById('patResult1');
  const val = parseInt(input.value);
  if(val === 15){
    result.className = 'result ok';
    result.textContent = '✅ ¡Correcto! El patrón es +3: 3, 6, 9, 12, 15';
    input.style.borderColor = 'var(--verde)';
  } else {
    result.className = 'result fail';
    result.textContent = '❌ No es correcto. Pista: ¿cuánto sumas cada vez? 3→6 (+3), 6→9 (+3)...';
    input.style.borderColor = 'var(--rojo)';
  }
}
```

**Clave:** La pista debe ser específica al ejercicio (no genérica). En vez de "Intenta de nuevo", dar una pista que guíe al razonamiento: "¿cuánto sumas cada vez?".

### Pattern: Conexión con el futuro (forward-looking)
Las cajas de conexión pueden mirar al **futuro** (preparar para ESO/Bachiller) no solo al **pasado** (recordar lo aprendido).

**Estructura dentro de `box-idea`:**
```html
<div class="box box-idea">
<strong>⚠️ Error común</strong>
No confundir patrón con aleatorio...

<strong>🔗 Conexión con el futuro</strong>
Los patrones son la base del álgebra. Cuando en 1º ESO veas "x, x+2, x+4, x+6", eso es un patrón. ¡Ya sabes lo que es!
</div>
```

**Uso:** Ideal para temas de primaria que son base de conceptos ESO (patrones → álgebra, sumas → ecuaciones, fracciones → proporcionalidad). Eleva el score `connections` y motiva al alumno mostrando utilidad futura.

### Pitfall: Inconsistencia HTML↔JS (2026-06-10)
Cuando se patchea un ejercicio, la función JS puede quedar desfasada:
1. `id="eNresult"` referenced por `onclick` no existe o apunta a otro ejercicio
2. Los números de operación en el enunciado NO coinciden con los de la función JS
3. Los parámetros booleanos de los botones están invertidos (`true`/`false` swap)

**Ejemplo:** Enunciado "5−5=0" pero `onclick="checkVF(this, false)"` y la función verifica "10−4=6". El alumno ve feedback de una operación que no existe en el ejercicio.

**Checklist post-patch:**
1. ¿El `id` referenced en `onclick` existe en el mismo bloque de ejercicio?
2. ¿Los números del enunciado coinciden con los de la función JS?
3. ¿Los parámetros booleanos de los botones son correctos? (`true` = correcto)
4. ¿El mensaje de feedback usa los mismos números que el enunciado?

Ver `references/consistency-verification.md` para ejemplos detallados y checklist completo.
