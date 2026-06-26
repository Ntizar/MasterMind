---
name: educational-html-nightly
description: "Procedimiento estricto v2 para mejorar sesiones HTML educativas existentes: selección de temas por prioridad/rotación, análisis de dimensiones débiles, mejoras dirigidas (ejercicios, texto, visual, real_world, conexiones, difficulty_range, manim), quality gates obligatorios, y actualización de tracking."
version: 2.1.0
author: Hermes Agent
tags: [html, education, nightly, quality-improvement, educational-content]
---

# Educational HTML Nightly — Mejora Nocturna de Sesiones Educativas

Procedimiento estricto para mejorar HTML educativos existentes de forma sistemática, con quality gates obligatorios y rotación de niveles.

## Cuándo usar

- Cron job nocturno de mejora de contenido educativo
- Sesión de mejora de calidad de un proyecto HTML educativo
- Cuando se necesita elevar el nivel pedagógico de archivos existentes
- **Proyecto DeSumarIntegrar**: `/root/workspace/DeSumarIntegrar`
- **Proyecto DibujoTecnico**: `/root/workspace/DibujoTecnico` (Bachillerato)

## Flujo de trabajo

### Paso 1 — SELECCIONAR TEMAS (2-3 por sesión)

Leer `INVENTARIO.md` (fuente de verdad de temas) y `progress.json` (tracking).

**Nota sobre `last_improved`:** `progress.json` tiene un campo raíz `last_improved` (usado por el sistema cron para evitar repetir temas en la misma sesión). Los temas individuales también tienen su propio `last_improved`. **Filtrar ambos:**
- Excluir temas cuyo `last_improved` (campo individual) coincida con la fecha actual
- Excluir temas cuyo `last_improved` (campo raíz, si está presente) coincida con la fecha actual

**Criterios de selección:**
1. **Prioridad:** Menos `improvement_count` → más bajo → primera prioridad
2. **ROTACIÓN DE NIVELES:** Si los últimos 3 temas fueron de un nivel (ej: Universidad), elegir de otro nivel (ej: Primaria, ESO)
3. **EXCLUIR:** Temas marcados como `index` o `duplicate`, archivos mejorados hoy (`last_improved` = fecha actual)

**Caso especial — Ronda 2 (todos en score 9):** Cuando todos los temas tienen score 9 (común en ronda 2), ignorar `avg_score` como criterio de desempate. Usar orden: (a) `improvement_count` ASC, (b) `last_improved` más antiguo, (c) bloque temático (priorizar bloques más avanzados).

**Filtro automático:**
```python
# Excluir index
if info.get('is_index', False) or info.get('status') == 'index':
    continue
# Excluir duplicados
if 'duplicate' in str(info.get('status', '')):
    continue
# Excluir mejorados hoy
if li and li.startswith('2026-06-15'):  # fecha actual
    continue
```

### Paso 2 — PARA CADA TEMA (MODO ESTRICTO)

#### Paso A — BACKUP
```bash
cp tema.html tema.html.bak
```

#### Paso B — ANALIZAR (2 dimensiones más débiles)

Leer el HTML actual y evaluar cada dimensión:

| Dimensión | Qué buscar |
|-----------|-----------|
| `exercises` | ¿Tiene 3+ tipos diferentes de ejercicios? (quiz, VF, completar hueco, ordenar, problema, emparejar, input) |
| `text` | ¿Sigue patrón 4 pasos: qué es → para qué → cómo → error? |
| `visual` | ¿Tiene SVG/gráficos que aporten información, no decorativos? |
| `real_world` | ¿Tiene casos cotidianos concretos? |
| `connections` | ¿Conecta con otros temas (connection-box, enlaces)? |
| `difficulty_range` | ¿Tiene ejercicios de fácil, medio y difícil (badges)? |
| `manim_quality` | ¿Tiene animaciones (Manim o SVG animado)? Para bachiller/universidad |
| `css_coherence` | ¿Tiene TODAS las clases del template base? |

**Clases CSS requeridas (template base):**
`header`, `container`, `chapter-title`, `box`, `box-teoria`, `box-ejemplo`, `box-error`, `box-idea`, `box-success`, `interactive`, `exercises`, `exercise`, `quiz-options`, `quiz-btn`, `summary`, `nav`, `footer`

**Detección rápida con grep:**
```bash
grep -c 'class="box box-teoria' file.html
grep -c 'class="box box-error' file.html
grep -c 'class="box box-success' file.html
grep -c '<svg' file.html
grep -c 'difficulty-badge' file.html
grep -c 'connection-box' file.html
grep -c 'onclick=' file.html
```

#### Paso C — MEJORAR (exactamente lo que falta)

**Reglas de oro:**
- NO crear temas nuevos
- NO más de 3 ejercicios nuevos por tema
- NO ejercicios del mismo tipo seguidos
- NO Plotly en temas de primaria básica
- NO SVG decorativos sin propósito

**Mejoras por dimensión:**

- **exercises:** 2-3 ejercicios de tipos DIFERENTES (completar, V/F, ordenar, problema, quiz, emparejar, input numérico)
- **text:** 1 explicación 4 pasos (qué es → para qué → cómo → error común)
- **visual:** 1 SVG/gráfico que aporte información (NO decorativo) — ej: diagrama de regiones de rechazo, gráfico de barras de posiciones, etc.
- **real_world:** 1 caso cotidiano concreto — ej: "fábrica de tornillos", "nave espacial", "test medicamento"
- **connections:** 1 connection-box con 4-6 enlaces a temas relacionados
- **difficulty_range:** Badges `difficulty-badge easy/medium/hard` en ejercicios
- **manim_quality:** SVG animado o Manim para temas de bachiller/universidad
- **CSS:** Añadir clases faltantes (`box-error`, `box-success`, `connection-box`, `difficulty-badge`, `svg-container`)

#### Paso D — QUALITY GATES (OBLIGATORIO)

```bash
# Gate 1: HTML válido
grep -q '</html>' tema.html || { echo "FAIL: Falta </html>"; exit 1; }
grep -q '<!DOCTYPE html>' tema.html || { echo "FAIL: Falta DOCTYPE"; exit 1; }

# Gate 2: Ejercicios funcionales
grep -q 'onclick=' tema.html || echo "WARN: Sin onclick en ejercicios"

# Gate 3: CSS coherence — verificar TODAS las clases requeridas
for class in header container chapter-title box box-teoria box-ejemplo box-error box-idea box-success interactive exercises exercise quiz-options quiz-btn summary nav footer; do
    grep -q "\.$class" tema.html || { echo "FAIL: Falta clase .$class"; exit 1; }
done

# Gate 4: Sin títulos duplicados
TITLE=$(grep -oP '<title>[^<]+</title>' tema.html | head -1)
DUPLICATE=$(grep -rl "$TITLE" /root/workspace/DeSumarIntegrar --include="*.html" | grep -v "tema.html" | grep -v "tema.html.bak" | head -1)
[ -n "$DUPLICATE" ] && { echo "FAIL: Título duplicado en $DUPLICATE"; exit 1; }
```

#### Paso E — Si algún gate FALLA

```bash
cp tema.html.bak tema.html  # Restaurar backup
# Pasar al siguiente tema
```

#### Paso F — Si todos OK

1. Actualizar `progress.json` (scores, improvements, status, last_improved)
2. Git commit: `cd /root/workspace/DeSumarIntegrar && git add -A && git commit -m "v2: [tema] - [dimensiones mejoradas]"`
3. Eliminar backup: `rm tema.html.bak`

### Paso 3 — AUTO-AUDITORÍA FINAL

Elegir 3 HTMLs aleatorios del proyecto y verificar CSS coherence:
```python
# Verificar que las 17 clases requeridas están en cada archivo
required_classes = ['header', 'container', 'chapter-title', 'box', 'box-teoria',
    'box-ejemplo', 'box-error', 'box-idea', 'box-success',
    'interactive', 'exercises', 'exercise', 'quiz-options', 'quiz-btn',
    'summary', 'nav', 'footer']
```

## Actualización de progress.json

```python
# Estructura de mejora:
{
    'run': run_number,
    'date': '2026-06-15',
    'added': 'descripción detallada de mejoras'
}

# Scores: valores 0-15 por dimensión
# improvement_count: contador de rondas
# status: 'pending' | 'improved_1' | 'improved_2' | 'improved_3' | 'improved_v2'
```

## Reglas estrictas

- **NO crear temas nuevos** — solo mejorar existentes
- **NO más de 3 ejercicios nuevos por tema**
- **NO ejercicios del mismo tipo seguidos**
- **NO Plotly en temas de primaria básica**
- **NO SVG decorativos sin propósito**
- **Si un gate falla, REVERTIR** — no hacer commit con HTML roto
- **Siempre usar backup** — `cp tema.html tema.html.bak` antes de cualquier cambio

## Pitfalls

- **🔴 DOBLE ESCAPE EN KATEX (`\\\\\\\\` vs `\\\\`):** Al usar `patch` con contenido que contiene `$\\\\\\\\pm$` o `$\\\\\\\\leq$`, el patch tool puede escapar doblemente generando `$\\\\\\\\\\\\\\\\pm$`. **Siempre verificar** con `grep '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\' file.html` tras el patch. Si hay doble escape, corregir con `patch` de nuevo.
- **🟡 KATEX AUTO-RENDER DOBLE ESCAPE (sistema):** El `renderMathInElement` call en el `<head>` a veces tiene `\\\\\\\\[` y `\\\\\\\\(` en lugar de `\\[` y `\\(`. **Siempre verificar** la línea del `<script defer src="...auto-render.min.js">` tras cualquier mejora. Fix: `\\\\\\\\[` → `\\[`, `\\\\\\\\(` → `\\(`. Detectar con: `grep '\\\\\\\\[' file.html` — si encuentra algo, está roto.
- **🟡 CSS DUPLICACIÓN MASIVA:** Algunos archivos (ej: `s08-2-3eso.html`) tienen clases CSS duplicadas 3-5 veces en el `<style>` (`.btn-blue-solid`, `.input-w60`, `.text-sm`, etc.). Esto no rompe nada pero infla el archivo y hace los patches más frágiles. **Al analizar un archivo, contar duplicados CSS:** `grep -oP '\.\w+' file.html | sort | uniq -d | head -20`. Si hay >10 duplicados, documentarlo en la nota de mejora pero NO limpiarlos (cambiar una clase duplicada podría romper HTML existente).
- **🔴 `read_file` con offset/limit no carga todo el archivo:** Si se lee con `offset/limit` y luego se hace `patch`, el patch puede fallar si el `old_string` no está en la porción leída. **Siempre leer el archivo completo** antes de patchear, o verificar que el `old_string` está dentro del rango leído.
- **🔴 `connection-box` vs `conexion-box`:** El CSS define `.connection-box` pero algunos archivos antiguos usan `class="conexion-box"`. **Siempre usar `class="connection-box"`** (con la 'n'). El CSS no reconocerá `conexion-box`.
- **🔴 `difficulty-badge` CSS no definido en todos los archivos:** Algunos archivos template no tienen las clases `.difficulty-badge`, `.difficulty-badge.easy`, `.difficulty-badge.medium`, `.difficulty-badge.hard` en su CSS. **Añadir siempre** estas 4 clases al `<style>` del archivo.
- **🔴 `svg-container` CSS no definido:** Algunos archivos no tienen `.svg-container` en el CSS. **Añadir** `.svg-container{text-align:center;margin:1.5rem 0}` al `<style>`.
- **🔴 CONVERSIÓN KATEX EN PATCHES:** Al patchear contenido con `$\\\\neq$` o `$\\\\leq$`, el patch tool puede escapar la barra invertida. **Verificar siempre** con grep tras patchear contenido matemático.
- **🔴 `patch` con contenido que ya fue leído con offset/limit:** Si se leyó el archivo con `offset/limit` y luego se intenta patchear una sección que no estaba en el rango leído, el patch fallará silenciosamente o aplicará mal. **Siempre leer el archivo completo** antes de patchear.
- **🔴 PATCH ENTRE `</div>` PIERDE WRAPPER:** Al patchear contenido entre `</div>` consecutivos, el patch tool puede eliminar accidentalmente un `<div class="chapter">` wrapper. **Siempre verificar la estructura HTML** tras el patch con `read_file` en las líneas afectadas. Si el wrapper se perdió, patchear de nuevo para añadirlo.
- **🔴 `box-success` CSS definido pero nunca usado:** El quality gate verifica que `.box-success` está en el CSS, pero NO que se usa en HTML. Un archivo puede pasar todos los gates sin tener ningún `<div class="box box-success">`. **Añadir siempre** al menos un `box-success` cuando se mejora la dimensión `real_world` o se añade un "truco/tip".
- **🔴 Añadir V/F requiere añadir la función JS:** Si añades un ejercicio V/F con `onclick="checkVF(this, true)"`, asegúrate de que la función `checkVF` existe en el `<script>`. Si el archivo solo tiene `checkExercise`, añade `checkVF` antes del patch del ejercicio. Lo mismo para `checkCompleta`, `checkOrden`, `checkProblem`, etc. **Verificar que la función referenciada en onclick existe antes de aplicar el patch.**
- **🟡 NO bajar scores ya en 10:** Al actualizar `progress.json`, nunca reduzcas un score que ya está en 10 (máximo). Si una dimensión ya es 10, déjala en 10 y solo actualiza las que realmente mejoraron. Bajar scores existentes corrompe el historial de mejora.
- **🔴 NO reemplazar ejercicio sin mantener diversidad de tipos:** Al sustituir un ejercicio (ej: cambiar fill-in por VF), el tipo de ejercicio se pierde. Si el tema ya tiene pocos tipos, añadir un nuevo tipo en lugar de reemplazar. **Mantener siempre ≥5 tipos diferentes.**
- **🟡 CSS coherence audit revela archivos legacy:** La verificación de las 17 clases CSS muestra que ~23 archivos (index pages, legacy) tienen clases faltantes. Los quality gates solo verifican el archivo ACTUAL, no el proyecto completo. No intentar arreglar todos de golpe — solo los que se mejoran en la sesión.
- **🔴 Añadir exercise divs requiere div.exercises wrapper:** Los nuevos ejercicios deben ir dentro de `<div class="exercises">...</div>`. Si el archivo no tiene un div.exercises contenedor, añadirlo. Los ejercicios sueltos sin el wrapper no se ven correctamente y no pasan la coherencia CSS.
- **🔴 Ejercicios FUERA de div.exercises (legacy):** Algunos archivos tienen ejercicios fuera del wrapper `div.exercises` (ej: b04-08-giro.html tenía ejercicios 6-10 fuera). **Siempre verificar:** leer el archivo completo y buscar `class="exercises"` → contar ejercicios dentro del wrapper vs total en el archivo. Si hay ejercicios fuera, moverlos dentro del wrapper con `replace()` en Python. El patrón típico es: `</div>\n</section>\n\n\n<div class="exercise">\n<p>📐 Ejercicio 6` — reemplazar `</div>\n</section>` por `</div>\n\n` (quitar el cierre de section) y luego añadir `</div>` después del último ejercicio.
- **🔴 `.bak` files en git:** Los archivos `.bak` se crean con `cp` pero NO deben entrar en el commit. **Siempre hacer `git rm --cached *.bak && rm -f *.bak && git commit --amend`** tras el commit inicial para eliminarlos. Alternativa: añadir `*.bak` a `.gitignore` del proyecto.
- **🔴 FUNCIONES JS DUPLICADAS:** Al leer el `<script>` de un HTML educativo, contar funciones con `grep -c 'function checkVF' file.html` (o `checkAnswer`, `checkFillIn`, etc.). Si hay >1 definición de la misma función, la segunda sobrescribe la primera silenciosamente. **Eliminar la duplicada** con `patch` antes de cualquier otra mejora. Ejemplo: `b07-03-interseccion-recta-recta.html` tenía `checkVF` definida dos veces (líneas 544 y 655).
- **🟡 SVG ANIMADO RONDA 2:** En ronda 2, los SVGs interactivos deben tener animaciones CSS. Añadir: (1) `@keyframes pulse-point` para puntos de intersección pulsantes, (2) `@keyframes draw-line` para líneas de referencia animadas, (3) `@keyframes fade-in` para transición entre pasos SVG. Añadir `class="pulse"` a círculos de intersección y `class="animate"` a líneas de referencia. Mejorar `showPaso()` para re-trigger animación con `g.style.animation = 'none'; g.offsetHeight; g.style.animation = ''`.

- **🔴 DibujoTecnico: títulos de ejercicios en `<p>`, no en `<strong>`:** En el proyecto DibujoTecnico, los títulos de ejercicios están dentro de `<p>` tags dentro del `<div class="exercise">` (ej: `<p>📐 Ejercicio 1 (Quiz): ...</p>`). Para añadir difficulty badges, patchear el `<p>`, NO el `<strong>`. En DeSumarIntegrar los títulos usan `<strong>`. **Siempre verificar la estructura del archivo ANTES de patchear.**

- **🔴 CLOSURE ONCLICK ROTO (`checkFillIn` pattern):** `onclick="checkFillIn(['respuesta'])()"` es un patrón de closure que **SIEMPRE está roto**. `checkFillIn` devuelve una función `function(btn) { ... }` que espera un argumento `btn`, pero `onclick="...()()"` la llama sin argumentos → `btn` es `undefined` → `btn.closest('.exercise')` falla. **Fix:** cambiar `onclick="checkFillIn(['respuesta'])()"` → `onclick="checkFillIn(['respuesta'])(this)"`. Aplicar a todos los ejercicios con `checkFillIn`, `checkCompleta`, y cualquier closure que devuelva una función que espera `event/btn`.

- **🔴 SVG INTERACTIVIDAD RONDA 2 (toggleHighlight):** Patrón probado para SVG interactivo: (1) Añadir CSS `.svg-element{transition:all .3s;cursor:pointer}.svg-element:hover{filter:brightness(1.15) drop-shadow(...)}` y `.svg-element.active{filter:brightness(1.2) drop-shadow(...)}`, (2) Añadir atributo `class="svg-element clickable"` y `onclick="toggleHighlight(this)"` + `data-info="texto descriptivo"` a elementos SVG clave, (3) Función JS `toggleHighlight(el)` que togglea `.active` y muestra info en un panel inyectado o existente. **Verificar que la función existe en el `<script>` ANTES de patchear los SVGs.**

- **🔴 PATCH DEJA CONTENIDO DUPLICADO:** Al patchear contenido que reemplaza un bloque inline (ej: `<div class="comparison">...</div>` en una sola línea), el patch puede insertar la versión mejorada PERO dejar la original inline. **Siempre verificar después del patch:** `grep -c 'class="comparison"' file.html` — si el conteo subió inesperadamente, buscar y eliminar la versión duplicada.

- **🟡 DibujoTecnico SVGs: muchos elementos repetitivos** — Los SVGs de DibujoTecnico tienen docenas de líneas, círculos y rectángulos con atributos similares. El `patch` tool puede fallar por non-unique old_string. **Usar Python `replace()` con strings exactos** para bloques SVG grandes, o verificar que el old_string es único con `grep -c 'old_string' file.html` antes de patchear.

- **🔴 Ronda 2: SVG interactividad requiere ≥5 data-info:** No basta con que el CSS tenga `.svg-element` y `.clickable`. Los elementos SVG deben tener atributo `data-info` para que la interactividad sea funcional. **Mínimo 5 elementos SVG con `data-info`** para pasar el gate de ronda 2. Si el tema tiene pocos, añadir `data-info` a rectángulos clickeables, círculos, líneas de unión, etc.

- **🟡 `connection-box` GATE CHECK FALSE NEGATIVE:** El gate que verifica `class="connection-box"` falla cuando el uso real es `class="box connection-box"` (clase compuesta). **Fix en el script de gates:** verificar `'connection-box' in content` en lugar de `class="connection-box"` exacto.

- **🟡 `box-success` GATE CHECK FALSE NEGATIVE:** Similar a connection-box — el gate verifica `.box-success` en CSS (que puede estar definido) pero no verifica `class="box box-success"` en HTML. **Fix:** verificar `class="box box-success"` en HTML como gate separado.

- **🔴 `progress.json` improvements field puede ser string o lista:** Al actualizar `progress.json`, el campo `improvements` de un tema puede ser un string (ronda 1) o una lista de dicts (ronda 2+). **Siempre normalizar antes de append:** `if isinstance(t.get('improvements'), str): t['improvements'] = [t['improvements']]`. Si no se normaliza, `t['improvements'].append(...)` lanza `AttributeError: 'str' object has no attribute 'append'`. Lo mismo aplica al campo raíz `improvements` en `progress.json`.

- **🔴 DibujoTecnico progress.json: claves con .html y scores anidados:** El proyecto DibujoTecnico (`/root/workspace/DibujoTecnico`) usa claves con extensión `.html` (ej: `b06-02-metodos-acotacion.html`) y los scores están en un campo `scores` dict anidado, NO en el nivel raíz del tema. **Siempre verificar estructura antes de actualizar:** `t = topics[topic_id + '.html']`, `scores = t.get('scores', {})`, actualizar `scores[d]`, luego `t['scores'] = scores`. Ver `references/dibujotecnico-ronda2-patterns.md` para ejemplos completos.

## Linked Files

- `references/quality-gates-checklist.md` — Checklist visual de quality gates para referencia rápida durante la sesión
- `references/svg-area-model-decimal.md` — Patrón SVG de modelo de área para multiplicación de decimales (primaria)
- `references/svg-bar-chart-calendar.md` — Patrón SVG de gráfico de barras para temas de calendario/tiempo (días por mes, etc.)
- `references/katex-double-escape-fix.md` — Procedimiento de detección y corrección del doble escape en KaTeX (sistema)
- `references/svg-animation-pattern.md` — Patrón CSS keyframes (pulse/draw/fade-in) para SVG animado en ronda 2
- `references/closure-onclick-fix.md` — Patrón closure onclick roto (checkFillIn) y cómo detectarlo/fixarlo
- `references/svg-interactivity-pattern.md` — Patrón toggleHighlight con data-info y panel de info inyectado para SVG interactivo ronda 2
- `references/duplicate-content-after-patch.md` — Cómo detectar y eliminar contenido duplicado tras patch de bloques inline
- `references/svg-zigzag-pattern.md` — Patrón SVG zigzag animado (draw-line + zigzag-pulse) para cortes escalonados
- `references/ronda2-selection-pattern.md` — Patrón de selección de temas cuando todos están en score 9 (ronda 2)
- `references/dibujotecnico-ronda2-patterns.md` — Diferencias específicas de DibujoTecnico vs DeSumarIntegrar: estructura progress.json con .html en claves, scores anidados en dict, títulos en <p>, ejemplos de actualización
