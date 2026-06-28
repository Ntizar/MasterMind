# Patrón: Mejora de Páginas Landing/Index

## Cuándo usarlo

Cuando el cron de mejora continua encuentra un archivo que es una **página de nivel** (landing page) en lugar de una página de lección. Estas páginas listan sesiones con tarjetas pero NO tienen ejercicios interactivos.

## Detección

```python
# Si el HTML no contiene estos, es un índice/landing:
has_exercise = 'class="exercise"' in html
has_interactive = 'class="interactive"' in html
has_session_card = 'class="session-card"' in html or 'class="card"' in html

# Si has_session_card=True y (has_exercise=False y has_interactive=False) → landing page
```

## Qué NO hacer

- ❌ NO añadir ejercicios de lección (quiz, completar hueco, V/F) a una landing page
- ❌ NO convertir la landing page en una lección
- ❌ NO añadir teoría extensa

## Qué SÍ hacer

### 1. Mini quiz interactivo (1 pregunta)

Engancha al alumno ANTES de que empiece las sesiones. No evalúa, solo despierta curiosidad.

```html
<div class="mini-quiz" id="miniQuiz">
<h3>🎯 ¡Pruébalo antes de empezar!</h3>
<p id="quizQuestion">Si repartes 3 pizzas entre 4 amigos, ¿qué parte de pizza le toca a cada uno?</p>
<div class="quiz-options" id="quizOptions">
<button onclick="checkQuiz(0)">3/4</button>
<button onclick="checkQuiz(1)">1/4</button>
<button onclick="checkQuiz(2)">1/3</button>
<button onclick="checkQuiz(3)">3/12</button>
</div>
<div class="quiz-feedback" id="quizFeedback"></div>
</div>
```

**JS mínimo:**
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

### 2. Diseño glassmorphism

Mejorar las tarjetas con backdrop-filter, gradientes y hover effects.

```css
.card{
  background:rgba(255,255,255,0.75);
  backdrop-filter:blur(10px);
  border:1px solid rgba(255,255,255,0.3);
  border-radius:16px;
  padding:1.2rem;
  transition:all .3s;
  cursor:pointer;
}
.card:hover{
  transform:translateY(-3px);
  box-shadow:0 8px 30px rgba(37,99,235,0.12);
  border-color:var(--azul);
}
```

### 3. Tags por categoría

Cada sesión con un tag temático con color propio.

```html
<span class="tag tag-fracciones">Fracciones</span>
<span class="tag tag-decimales">Decimales</span>
<span class="tag tag-geometria">Geometría</span>
```

```css
.tag-fracciones{background:rgba(249,115,22,0.1);color:#ea580c}
.tag-decimales{background:rgba(37,99,235,0.1);color:#2563eb}
.tag-geometria{background:rgba(16,185,129,0.1);color:#059669}
```

### 4. Caja intro con objetivos claros

5-8 objetivos concretos y medibles en formato `<ul>`.

## Ejemplo real

Visto en `s04-4primaria.html` (2026-06-10):
- 1 mini quiz (pizzas entre 4 amigos → 3/4)
- Diseño glassmorphism con gradientes
- 8 tags por categoría
- 8 objetivos claros
- CSS mejorado con hover y transiciones

## Scores objetivo para landing pages

| Score | Objetivo |
|-------|----------|
| exercises | 1 (mini quiz) |
| text | 10 (intro + objetivos) |
| visual | 5 (glassmorphism + tags) |
| real_world | 7 (caso del quiz) |
| connections | 2 (quiz → sesión 1) |
| difficulty_range | 4 (solo 1 pregunta) |
