---
name: td-html-generator
description: Procedimiento completo para generar archivos HTML educativos del curso de Dibujo Técnico — mapeo de skill TD → template → HTML interactivo con SVG, quizzes y ejercicios.
tags: [stem, td, html, generator]
---

# Generador HTML — Dibujo Técnico

Genera archivos HTML auto-contenidos para cada tema del curso de Dibujo Técnico usando el template base en `generate_td.py`.

## Flujo de trabajo (número de pasos)

### Tarea simple (≤3 pasos) — directo
1. Cargar skill TD con `skill_view(name='stem/td/<nombre>')`
2. Generar HTML con `write_file`
3. Git commit + push

### Tarea compleja (5+ pasos) — seguir el flujo completo
1. **Cargar skill TD** fuente con `skill_view(name='stem/td/<skill>')`
2. **Verificar archivos existentes**: `ls /root/workspace/DibujoTecnico/` y comparar con progress.json — detectar nombres de archivo que no coinciden entre progress.json y la realidad (ej: `b06-04-reglas-acotacion.html` vs `b06-04-reglas-acotacion-iso-129.html`). Corregir progress.json si hay discrepancia.
3. **Leer template** en `/root/workspace/DibujoTecnico/generate_td.py` (líneas 8-136 = TEMPLATE string)
4. **Mapear contenido**: extraer datos del skill → rellenar placeholders del template
5. **Generar SVG interactivo**: inline SVG con ejemplos visuales del tema (mínimo 6-8 tipos de contenido visual)
6. **Generar HTML completo** con `write_file` a `/root/workspace/DibujoTecnico/<tema_id>.html`
7. **Verificar calidad**: tamaño >12KB, tiene `<svg`, tiene `quiz-btn`, tiene `David Antizar`
8. **Actualizar progress.json**: cambiar status a "completed", añadir `last_completed`
9. **Git commit + push**: `cd /root/workspace/DibujoTecnico && git add . && git commit -m "<icon> <id>: <title>" && git push`
10. **Actualizar cron**: `cronjob action='update' job_id=e6f8ad7b0c85` con prompt para el siguiente tema pending

## Estructura del HTML

### Placeholders del template (generate_td.py, línea 11-118)
```
{title}          → Ej: "📐 S01.2: Tipos de línea ISO 128"
{subtitle}       → "Dibujo Técnico — Normalización"
{key_idea}       → Idea clave en 1 frase
{learning_goals} → 4 <li> con objetivos de aprendizaje
{theory_title}   → Título de la sección teórica
{theory_text}    → Explicación teórica con negritas para conceptos
{example_1/2/3}  → 3 ejemplos prácticos
{interactive_title} → Título de la sección interactiva
{interactive_desc}  → Descripción del quiz
{svg_content}    → SVG inline con ejemplos visuales
{interactive_content} → Botones quiz con onclick="checkAnswer(...)"
{exercises_html} → 4 ejercicios variados (quiz, completar, V/F, identificar)
{summary_items}  → 5 puntos clave con <li>
{prev_link}      → Archivo HTML anterior
{next_link}      → Archivo HTML siguiente
{js_code}        → Funciones: checkAnswer, checkExercise, checkVF, selectQuiz
```

## SVG interactivo — patrón de construcción

### Reglas para SVGs en este curso:
1. **Viewport amplio**: `viewBox="0 0 700 520"` como mínimo
2. **Grid de ejemplos**: organizar en filas de 3 columnas con separadores
3. **Etiquetas descriptivas**: cada tipo/ejemplo tiene label + descripción
4. **Colores semánticos**: `#1e293b` para líneas principales, `#94a3b8` para auxiliares, `#2563eb` para títulos
5. **Tipografía**: `font-family: Inter, system-ui, sans-serif`
6. **Mínimo 6-8 tipos de contenido visual** en el SVG
7. **Separadores visuales**: líneas `#e2e8f0` entre secciones
8. **Textos explicativos** debajo de cada ejemplo

### Ejemplo de estructura SVG:
```xml
<svg viewBox="0 0 700 520" xmlns="http://www.w3.org/2000/svg">
  <!-- Fila 1: 3 ejemplos principales -->
  <text x="35" y="55">Ejemplo 1</text>
  <line ... />  <!-- visual representation -->
  <text x="35" y="155">Explicación</text>
  
  <!-- Separador -->
  <line x1="220" y1="40" x2="220" y2="170" stroke="#e2e8f0"/>
  
  <!-- Fila 2: 3 ejemplos adicionales -->
  <!-- ... -->
</svg>
```

## Funciones JS requeridas

### checkAnswer(btn, isCorrect, resultId)
- Para quizzes de selección múltiple (4 opciones)
- Deshabilita todos los botones tras respuesta
- Añade clase `correct` o `wrong` al botón
- Muestra resultado en div con id `resultId`

### checkExercise(btn, isCorrect, resultId)
- Para ejercicios de selección (4 opciones)
- Mismo patrón que checkAnswer pero con feedback específico

### checkVF(btn, isCorrect, resultId)
- Para preguntas Verdadero/Falso (2 opciones)
- Feedback específico para V/F

## Actualización de progress.json

### ⚠️ CRÍTICO: `read_file` rompe JSON
`read_file` prependea números de línea (`1|{`, `2|  "curso":...`), lo que rompe `json.loads()`. **NUNCA** usar `read_file` para leer JSON que vas a parsear con Python.

**Patrón correcto:**
```python
from hermes_tools import terminal, write_file
import json

# LEER: usar terminal(cat) en vez de read_file
result = terminal(command="cat /root/workspace/DibujoTecnico/progress.json")
progress = json.loads(result['output'])

# MODIFICAR
progress['temas'].append({...})
progress['total_temas'] = len(progress['temas'])

# ESCRIBIR: write_file sí funciona (no prependea números)
write_file(path="/root/workspace/DibujoTecnico/progress.json",
           content=json.dumps(progress, indent=2, ensure_ascii=False))
```

**Patrón alternativo (execute_code completo):**
```python
from hermes_tools import terminal, write_file
import json

result = terminal(command="cat /root/workspace/DibujoTecnico/progress.json")
progress = json.loads(result['output'])
# ... modificar progress ...
write_file(path="/root/workspace/DibujoTecnico/progress.json",
           content=json.dumps(progress, indent=2, ensure_ascii=False))
```

### Estructura del tema en progress.json:
```json
{
  "id": "b01-02",
  "file": "b01-02-tipos-linea.html",
  "title": "📐 Tipos de línea ISO 128",
  "desc": "Gruesa, fina, discontinua, ejes...",
  "bloque": "Bloque 1: Normalización",
  "icon": "📏",
  "skills": "td-normalizacion",
  "status": "completed",
  "improvement_count": 0,
  "priority": 2,
  "last_completed": "2026-06-10"
}
```

### Pasos:
1. Leer progress.json con `terminal("cat ...")` + `json.loads()` — **NO con read_file**
2. Cambiar status del tema a "completed"
3. Añadir `last_completed` con fecha actual (YYYY-MM-DD)
4. Escribir archivo completo con `write_file`

## Mapeo skill → tema

| ID tema | Skill fuente | Bloque |
|---------|-------------|--------|
| b01-01 a b01-05 | td-normalizacion | Normalización |
| b02-01 a b02-08 | td-proyecciones | Proyecciones |
| b03-01 a b03-06 | td-perspectivas | Perspectivas |
| b04-01 a b04-10 | td-diedrico-punto-recta-plano | Diedrico |
| b05-01 a b05-06 | td-cortes-secciones | Cortes y Secciones |
| b06-01 a b06-05 | td-acotacion | Acotación |
| b07-01+ | td-intersecciones-vm | Intersecciones |

## Pitfalls

- **🔴 GitHub Pages requiere `index.html` en minúsculas**: Si el archivo se llama `INDEX.html` (mayúsculas), Pages devuelve 404. **SIEMPRE** crear `index.html` (minúsculas) como punto de entrada. Mantener `INDEX.html` como referencia interna si se desea, pero Pages solo sirve `index.html`.
- **🔴 CSS CON DOBLES LLAVES `{{}}` DE TEMPLATE ENGINE** — Algunos archivos HTML generados por scripts Python/Jinja pueden contener `{{` y `}}` en bloques `<style>` en vez de `{` y `}`. Esto rompe TODOS los estilos. **Detección:** `grep -n '{{' *.html` dentro de `<style>`. **Corrección:** reemplazar `{{` → `{` y `}}` → `}` SOLO dentro de `<style>`. **Cargar skill `audit-html-project`** para el script batch de corrección. Ver `references/css-double-braces-fix.md` en audit-html-project.
- **🔴 NOMBRES DE ARCHIVO EN progress.json ≠ archivos reales**: Un generador o sesión previa puede crear archivos con nombres ligeramente distintos a los que progress.json referencia (ej: `b06-04-reglas-acotacion.html` vs `b06-04-reglas-acotacion-iso-129.html`). **SIEMPRE** verificar que el archivo referenced en progress.json existe físicamente (`os.path.exists()`) antes de asumir. Si hay discrepancia, corregir progress.json con el nombre real del archivo.
- **NO usar patch para el HTML**: siempre `write_file` con contenido completo. El template es grande y patch falla con strings largos.
- **NUNCA bajar la calidad por acelerar**: si un tema se genera sin SVGs, sin ejemplos, sin explicaciones detalladas, o con menos de 12KB, es inaceptable. El usuario prefiere esperar más tiempo a recibir contenido pobre. Cada tema debe tener: SVG explicativo, 3+ ejemplos resueltos, 5 ejercicios interactivos, teoría completa, error clásico, resumen. Mínimo 12KB de contenido real.
- **Subagentes para generación masiva**: NO delegar más de 3-4 temas por subagente. 7 temas en un solo delegate_task causa timeout (600s). Preferir generación directa con write_file para mantener control de calidad, o batches pequeños (3-4 temas) si se delega.
- **Verificar calidad post-generación**: comprobar tamaño del archivo (>12KB), presencia de SVG (buscar '<svg'), ejercicios (buscar 'quiz-btn'), y navegación (buscar 'Siguiente →'). Si algún tema no cumple, regenerarlo inmediatamente.
- **SVG con viewBox amplio**: si el SVG se corta, aumenta el viewBox y reposiciona elementos.
- **Progreso del scroll**: la barra de progreso usa `window.onscroll` con cálculo de porcentaje — no modificar esta parte del template.
- **Botones quiz**: siempre deshabilitar todos los botones tras una respuesta (`buttons[i].disabled = true`).
- **CSS variables**: el template usa `--azul`, `--naranja`, etc. No cambiar estos nombres en el CSS.
- **progress.json ya puede estar actualizado**: si otro cron procesó el tema, verificar antes de sobrescribir.
- **Colores de ejes isométricos (2026-06-10):** Z=verde `#10b981` (altura/crecimiento), X=naranja `#f97316` (longitud), Y=azul `#2563eb` (anchura). Más intuitivo que el esquema anterior (Z=azul, X=naranja, Y=verde). Ver `references/svg-perspectiva-isometrica.md` para coordenadas completas.
- **Navegación:** prev_link y next_link deben apuntar a archivos .html reales, no a IDs.
- **El cron job ID es fijo:** `e6f8ad7b0c85` para el pipeline de Dibujo Técnico.
- **Siempre leer progress.json para encontrar el siguiente tema pending**, no asumir el orden.
- **Verificar si el tema ya está completado:** antes de generar, comprobar `progress.json` y `ls` del archivo HTML. Si ya existe y está "completed", avanzar al siguiente pending.
- **Ejercicio multi-select:** para "selecciona TODAS las correctas", usar checkboxes con `<label>` + `onclick` toggle de fondo + función JS que lee `.checked` de cada checkbox y valida combinación con `&&`/`!`. Ver `references/patrones-ejercicios.md` sección 5.
- **Funciones JS específicas por pregunta:** en la sección interactiva, usar funciones dedicadas (`checkAngle`, `checkReduction`, `checkZ`) en vez de `checkAnswer` genérica, para dar feedback contextualizado a cada pregunta.
- **Patrón `showPaso(n)` para SVGs paso a paso:** la función usa `document.getElementById('panel'+n).style.display = n===X ? '' : 'none'` con `classList.toggle('active', i===n)` para step-dots. **NUNCA** usar `display:none` en el CSS del panel — siempre inline `style="display:none"` en el `<g>` del SVG, porque el CSS global `.svg-container svg * { display: block }` puede interferir.
- **Corregir `onclick` rotos:** muchos HTMLs antiguos tienen `onclick="funcion(...)` sin paréntesis de cierre `)` o sin `"` de cierre. **SIEMPRE** verificar que cada `onclick` tiene: `onclick="funcion(arg1, arg2)"` con paréntesis y comillas cerrados.

## Deploy a GitHub Pages

Para proyectos de HTML estático (sin servidor Node.js), **GitHub Pages es la opción preferida** sobre NaN.builders.

### Flujo de deploy
1. **Renombrar** `INDEX.html` → `index.html` (GitHub Pages solo sirve `index.html` en minúsculas)
2. **Añadir `index.html`** al repo (mantener `INDEX.html` si se usa como referencia interna)
3. **Push a master/main**: `git push origin master`
4. **Activar Pages** via API:
   ```bash
   source /hermes-home/.env
   curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/Ntizar/DibujoTecnico/pages \
     -d '{"source":{"branch":"master","path":"/"}}'
   ```
5. **Verificar**: `curl -s -o /dev/null -w "%{http_code}" https://ntizar.github.io/DibujoTecnico/` → debe devolver 200
6. **Commit adicional** si se renombró INDEX.html: `git add . && git commit -m "📄 Rename INDEX.html → index.html para Pages" && git push`

### Cuándo usar Pages vs NaN
| Proyecto | Plataforma |
|----------|-----------|
| HTML estático puro (educativo, portfolio) | **GitHub Pages** |
| Node.js con API/servidor | NaN.builders |
| Vite/React con build | NaN.builders (o Pages si es SPA estática) |

## Pipeline completo: Auditoría → Corrección → Generación → Deploy

Cuando el usuario pide "completar y desplegar un proyecto HTML", seguir este orden:

### Fase 1: Auditoría
1. Cargar `audit-html-project`
2. Escaneo masivo: enlaces rotos, atribución, SVGs, ejercicios, navegación
3. Generar informe con severidades (❌/⚠️/💡)
4. Guardar informe en el proyecto (ej: `AUDITORIA-YYYY-MM-DD.md`)

### Fase 2: Corrección de críticos
1. Corregir enlaces rotos de navegación (reemplazar targets incorrectos)
2. Añadir archivos huérfanos a progress.json
3. Commit: `🔧 Fix: <descripción>`

### Fase 3: Generación de temas faltantes
1. Comparar progress.json vs `ls *.html` para detectar faltantes
2. Generar por bloques de 3-6 temas
3. Actualizar progress.json después de cada bloque
4. Commit por bloque: `📝 Bloque X: <temas completados>`

### Fase 4: Deploy
1. Actualizar `index.html` si es necesario
2. Push a GitHub
3. Activar/verificar Pages

## Mejora continua nocturna (MEGA-PLAN2)

Cuando se ejecuta el cron de mejora continua (no generación de temas nuevos), seguir este ciclo:

### FASE 1: SELECCIONAR 3-5 TEMAS
1. Leer `progress.json` con `terminal("cat ...")` + `json.loads()`
2. Filtrar temas con `status == "pending"`
3. Ordenar por: prioridad (B01 primero), improvement_count (asc), scores más bajos
4. Seleccionar los 3-5 primeros

### FASE 2: MEJORAR CADA TEMA
Para cada tema seleccionado:

**Paso 1: Analizar el HTML actual**
- Leer el archivo HTML completo
- Puntuar cada dimensión (0-10): `svg_interactive`, `exercises`, `text_explanation`, `real_world`, `error_common`, `css_coherence`

**Paso 2: Mejorar 2-3 dimensiones más débiles**

Prioridades de mejora:
1. **SVG interactivo** (prioridad ALTA): hover con `onmouseover`, toggle capas con `classList.toggle`, animaciones `@keyframes`, `onclick` para mostrar/ocultar
2. **Casos reales industriales**: contexto de taller, fabricación, ingeniería mecánica. Ej: "Si este agujero está mal acotado, la pieza no encaja. 200€ perdidos."
3. **Errores comunes visuales**: comparación SVG correcto vs incorrecto, no solo texto
4. **Ejercicios variados**: NO repetir tipo. Mix de quiz visual, completar línea SVG, V/F visual, ordenar pasos
5. **CSS coherence**: verificar que el CSS tiene TODAS las clases del template base

**Clases CSS obligatorias** (si falta alguna, añadirla):
`.header`, `.container`, `.chapter-title`, `.box`, `.box-teoria`, `.box-ejemplo`, `.box-error`, `.box-idea`, `.box-success`, `.svg-container`, `.interactive`, `.exercises`, `.exercise`, `.quiz-options`, `.quiz-btn`, `.quiz-btn.correct`, `.quiz-btn.wrong`, `.summary`, `.nav`, `.footer`, `.progress-bar`, `.progress-fill`

**Variables CSS obligatorias**: `--azul:#2563eb`, `--naranja:#f97316`, `--verde:#10b981`, `--rojo:#ef4444`

**Paso 3: Verificar calidad**
- HTML no roto (etiquetas cerradas)
- Ejercicios tienen feedback (correcto/incorrecto)
- SVGs tienen viewBox correcto
- CSS coherente con template base

**Paso 4: Actualizar progress.json**
- Añadir entrada en `improvements[]`
- Actualizar scores
- Cambiar status a `improved_N`
- Incrementar `improvement_count`

**Paso 5: Git commit**
```bash
cd /root/workspace/DibujoTecnico && git add -A && git commit -m "mejora: [tema] - [qué se mejoró]" && git push
```

### FASE 3: DETECCIÓN DE CSS COHERENCE DRIFT (CRÍTICO)

**Problema sistemático detectado 2026-06-10:** Muchos temas (42/49) tienen `css_coherence=7` porque usan CSS custom en vez del template base. El patrón es consistente:

**CSS custom vs template base — diferencias típicas:**

| Clase | CSS custom (drift) ❌ | Template base ✅ |
|-------|----------------------|-----------------|
| `.comparison` | `display:grid;grid-template-columns:1fr 1fr;gap:1rem` | `display:flex;gap:1.5rem;flex-wrap:wrap` |
| `.comparison-side` | `background:#f8fafc;border-radius:12px;padding:1.5rem;border:2px solid #e2e8f0` | `flex:1;min-width:250px;text-align:center` |
| `.step-dot` | `width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;color:#fff` | `width:12px;height:12px;border-radius:50%;background:#e2e8f0;transition:all .3s` |
| `.step-dot.active` | `box-shadow:0 0 0 4px rgba(37,99,235,.3)` | `background:var(--azul);transform:scale(1.3)` |
| `.real-world-badge` | `background:linear-gradient(135deg,var(--naranja),#ea580c);padding:.3rem .8rem;border-radius:20px;font-size:.8rem;font-weight:700` | `background:var(--naranja);padding:.2rem .6rem;border-radius:12px;font-size:.75rem;font-weight:600` |
| `.stack-item` | `background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:1rem` | `border:2px solid var(--azul);background:#fff;border-radius:4px;display:flex;align-items:center;justify-content:center;font-weight:bold;color:var(--azul)` |

**Detección automática:**
```python
# En execute_code, comparar CSS de un tema con el template base
template_css_markers = [
    '.comparison{display:flex;gap:1.5rem',
    '.step-dot{width:12px;height:12px',
    '.step-dot.active{background:var(--azul)',
    '.real-world-badge{display:inline-block;background:var(--naranja)',
    '.stack-item{border:2px solid var(--azul);background:#fff;border-radius:4px'
]

custom_css_markers = [
    '.comparison{display:grid',
    '.step-dot{width:32px',
    '.step-dot.active{box-shadow:0 0 0 4px',
    '.real-world-badge{display:inline-block;background:linear-gradient',
    '.stack-item{background:#f8fafc;border:2px solid #e2e8f0'
]

for marker in custom_css_markers:
    if marker in css_content:
        print(f"DRIFT DETECTADO: {marker}")
```

**Corrección:** Reemplazar TODO el bloque de CSS custom con el template base completo (ver patrón en MODO RÁPIDO sección "Batch CSS template").

**Clase `.feedback` siempre faltante:** Ningún tema tiene `.feedback` en su CSS, pero todos la usan en ejercicios. **Siempre añadirla:**
```css
.feedback{font-size:.9rem;margin-top:.5rem;font-weight:600;padding:.4rem .8rem;border-radius:4px}
.feedback.correct{background:var(--verde-claro);color:#065f46}
.feedback.incorrect{background:var(--rojo-claro);color:#991b1b}
```

### FASE 4: AUTO-AUDITORÍA CSS (al final)
1. Elegir 3 HTMLs aleatorios (que NO sean los que acabas de mejorar)
2. Leer sus CSS y comparar con template base
3. Si hay deriva (clases faltantes, variables distintas), anotarlo
4. Actualizar `audit.last_css_audit` y `css_coherence_score` en progress.json

### FASE 4: RESUMEN
Escribir resumen: cuántos temas mejorados, qué se mejoró en cada uno, puntaje coherencia CSS, qué queda por mejorar.

### Reglas de mejora continua
- **NO** añadir ejercicios repetitivos del mismo tipo
- **NO** añadir SVG decorativos sin interacción
- **NO** romper el HTML
- **NO** cambiar el estilo visual (mantener azul #2563eb + naranja #f97316)
- **SÍ** priorizar SVG interactivos sobre texto
- **SÍ** priorizar casos reales sobre teoría abstracta
- **SÍ** mantener coherencia CSS entre todos los HTMLs
- **SÍ** hacer git commit después de cada tema mejorado

## Archivos de referencia

- `references/curriculum-map.md` → Mapa completo del curso: bloques, temas, skills, estado de cada tema (38/49 existentes)
- `references/svg-perspectiva-isometrica.md` → Patrón SVG para ejes isométricos (b03-01): colores, coordenadas, arcos de ángulo, cubo de referencia, cuadrícula de fondo
- `references/patrones-ejercicios.md` → Patrones de ejercicios interactivos: quiz, completar, V/F, identificar, multi-select checkboxes + funciones JS
- `references/casos-reales-industriales.md` → Banco de casos reales por bloque temático + errores comparativos por bloque. Usar como referencia rápida al crear secciones "Caso Real" y "Error Comparativo" en modo rápido.
- `templates/html-base-template.md` → Estructura base HTML/CSS/JS estándar (elementos fijos, secciones orden obligatorias, SVG mínimo, ejercicios pattern). Copiar y modificar para cada tema nuevo.
- `references/css-coherence-drift.md` — Detección y corrección de CSS drift: patrón sistemático donde temas tienen CSS custom en vez del template base (`.comparison` grid vs flex, `.step-dot` 32px vs 12px, etc.). Incluye comparativa drift vs template y patrón de corrección batch.
- `references/patron-svg-paso-a-paso-interactive.md` — Patrón de SVG interactivo con 3-4 paneles clickeables (inicio → proceso → resultado/comparación), step-dots animados, función `showPaso(n)`. Variantes documentadas por tema.
- `references/naming-mismatch-progress-json.md` → ⚠️ Nombres de archivo en progress.json pueden no coincidir con archivos reales. Verificar siempre con `os.path.exists()`.
- `references/skills-mapeo.md` → Mapeo skill TD → tema del curso

## 5. Template HTML — Estructura Base

Estructura HTML/CSS/JS estándar para TODOS los temas del curso (absorbido de `td-html-template`).

### Elementos fijos (NUNCA cambiar)
- CSS variables: `--azul:#2563eb`, `--naranja:#f97316`, `--verde:#10b981`, `--rojo:#ef4444`
- Estructura: `header.header` → `main.container` → `footer.footer`
- Funciones JS: `checkAnswer()`, `checkExercise()`, `window.onscroll`
- Footer: "Hecho con ❤️ por David Antizar"
- Meta tags: charset, viewport, title con emoji + SXX.X

### Secciones del contenido (orden obligatorio)
1. `chapter-title` → "¿Qué vamos a aprender?" (idea clave + objetivos)
2. `chapter-title` → número + teoría (teoría + 3 ejemplos)
3. `chapter-title` → número + "Visualiza..." (SVG inline)
4. `chapter-title` → "📝 Ejercicios" (4-5 ejercicios)
5. `box-error` → error clásico
6. `box-idea` → conexión con tema anterior/siguiente
7. `summary` → resumen de lo aprendido (5 puntos)
8. `nav` → navegación prev/next

### SVG mínimo
- viewBox: `0 0 600 300` mínimo
- Fondo: `#f8fafc` con `rx="8"`
- Título en `<text>` centrado arriba
- Elementos visuales con colores semánticos
- Leyenda en `<rect>` al final

### Sección interactiva (patrón 2026-06-10)
- `<div class="interactive">` con `<h3>` de título
- SVG dentro de `<div class="svg-container">` (antes del interactive)
- 3 preguntas mínimo en el interactivo con IDs `r1`, `r2`, `r3`
- Resultado compartido en `<div class="result" id="interactiveResult">`

## 6. Normalización en Dibujo Técnico — Referencia Rápida

Contenido de referencia técnica absorbido de `td-normalizacion`.

### Formatos de papel (ISO 216)
- Serie A: A0 (841×1189 mm) → A4 (210×297). Relación √2
- **A0 = 1 m²**
- Márgenes: con marco 10mm (3 lados) + 5mm (lomo); sin marco 10mm todos

### Tipos de línea (ISO 128-20)
| Tipo | Ancho | Uso |
|---|---|---|
| A (gruesa) | 0,5-2 mm | Contornos visibles, aristas |
| C (fina) | 0,25-1 mm | Acotaciones, hachuras, guías |
| D (fina) | 0,25-1 mm | Líneas de cota, auxiliares |
| H (fina) | 0,25-1 mm | Centro de círculos |

### Escalas (ISO 5455)
- Natural: 1:1 | Ampliación: 2:1, 5:1, 10:1 | Reducción: 1:2, 1:5, 1:10, 1:20, 1:50, 1:100
- **Siempre acotar a tamaño real**, independientemente de la escala

### Rotulación
- Altura: 2,5; 3,5; 5; 7; 10; 14; 20 mm
- Tipo A: inclinada 75° o vertical, proporción estrecha (b = 2/3 h)
- Tipo B: inclinada 75° o vertical, proporción normal (b = h/14)

### Errores comunes
- Confundir línea discontinua gruesa (ocultas) con fina (ejes) — es al revés
- Acotar en escala: siempre acotar la DIMENSIÓN REAL, no lo que se ve
- Escala: 2:1 es AMPLIACIÓN, NO reducción
- Formato: A0 = 841×1189, NO 1189×841

## MODO RÁPIDO: Mejora por batch (aprendizaje 2026-06-10)

Cuando se ejecuta un cron de mejora continua con **MODO RÁPIDO** (4-6 temas por sesión), usar este patrón de batch:

### Patrón de 3 pasos por batch

**Paso 1: Leer progress.json** con `execute_code` (Python) → filtrar temas pending, ordenar por prioridad/score bajo.

**Paso 2: Batch CSS template** — Añadir las clases CSS obligatorias a TODOS los temas del batch de golpe con un script Python:
```python
template_css = '''.comparison{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.5rem 0}
.comparison-side{background:#f8fafc;border-radius:12px;padding:1.5rem;border:2px solid #e2e8f0;text-align:center;transition:all .3s}
.comparison-side:hover{border-color:var(--azul);box-shadow:0 4px 12px rgba(37,99,235,.1)}
.real-world-badge{display:inline-block;background:linear-gradient(135deg,var(--naranja),#ea580c);color:#fff;padding:.3rem .8rem;border-radius:20px;font-size:.8rem;font-weight:700;margin-bottom:.8rem}
.step-indicator{display:flex;gap:.5rem;justify-content:center;margin:1rem 0}
.step-dot{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;color:#fff;transition:all .3s;cursor:pointer}
.step-dot:hover{transform:scale(1.2)}
.step-dot.active{box-shadow:0 0 0 4px rgba(37,99,235,.3)}
.stack-item{background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:1rem;margin:.5rem 0;transition:all .3s;cursor:pointer}
.stack-item:hover{border-color:var(--azul);transform:translateX(4px)}
.stack-item.active{border-color:var(--azul);background:var(--azul-claro)}'''

css_marker = '.nav .disabled{color:var(--gris);cursor:default;pointer-events:none}\n.footer'
content = content.replace(css_marker, '.nav .disabled{...}\n' + template_css + '\n.footer')
```

**Paso 3: Batch casos reales + errores** — Diccionario `{filename: {real, error}}` con casos industriales concretos. Insertar antes de `<div class="summary">` y `<div class="box box-error">` respectivamente.

### Casos reales por bloque temático (banco reusable)
| Bloque | Caso real típico |
|--------|-----------------|
| b02 Proyecciones | Biela de motor, brida de tubería, válvula de paso |
| b03 Perspectivas | Tuercas/arandelas, planos arquitectónicos, catálogo productos |
| b04 Diedrico | Control calidad CMM, cableado/tuberías, plano biselado |
| b05 Cortes | Motor de combustión, carcasa bomba, eje con ranura |
| b06 Acotación | Pieza aeronáutica, taladrero CNC, bloque motor |
| b07 Intersecciones | Unión tuberías HVAC, vigas acero, chimenea industrial |
| b08 Abatimientos/Giros | Aleta disipador, base máquina, rebaje eje |
| b09 Conjuntos | Caja cambios, reductor velocidad, motor eléctrico |

### Errores comparativos por bloque (banco reusable)
| Bloque | Error típico |
|--------|-------------|
| b02 | Planta encima del alzado, confundir X con Z |
| b03 | Círculo en vez de elipse en isométrica, reducción caballera incorrecta |
| b04 | Punto en 2º diedro, recta paralela a LT |
| b05 | Corte total innecesario, sin corte (líneas ocultas) |
| b06 | Cota dentro del objeto, cotas en cadena (error acumulado) |
| b07 | Intersección recta en vez de curva, sin cálculo |
| b08 | Sin abatir (forma deformada), reducción 1.0 en vez de 0.5 |
| b09 | Sin número de pieza, sin lista de materiales |

### Reglas del MODO RÁPIDO
- **4-6 temas por batch** es el ritmo óptimo
- **1 acción por dimensión**: 1 CSS batch, 1 caso real, 1 error comparativo
- **NO** hacer SVGs interactivos nuevos en modo rápido (ya existen)
- **SÍ** usar `execute_code` (Python) para todo: leer, patchear, actualizar progress.json
- **Git commit después de cada batch**, no después de cada tema individual
- **Actualizar progress.json con execute_code**, NO a mano
- **Verificar que los casos existen en el diccionario** antes de patchear (⚠️ KeyError si no)

### Pitfall crítico
- **`data` en el loop es el dict de progress.json, NO el de cases**: al iterar `for filename, _data in next6`, usar `cases.get(filename)` para acceder al caso, NO `data['real']` (eso accede a progress.json y da KeyError).
- **`onclick` rotos en HTMLs antiguos:** muchos temas tienen atributos `onclick` sin cerrar paréntesis o comillas (ej: `onclick="showPaso(1"` sin `)`). **Siempre verificar** con `grep -n 'onclick=' archivo.html` y corregir antes de confiar en la interactividad.

## Patrones de generación masiva (aprendizajes 2026-06-10)

- **Generar en batch de 3-6 temas por commit** es el ritmo óptimo. Más de 6 → commits enormes y difíciles de revisar. Menos de 3 → demasiado overhead de git.
- **Cada commit debe ser autónomo y funcional**: el repo siempre tiene un estado navegable. No dejar commits intermedios rotos.
- **progress.json se actualiza con execute_code (Python)**, NO a mano. El script JSON es demasiado largo para patch fiable.
- **El cron `td-generador-tema` nunca se ejecuta solo** — `cronjob run` no ejecuta el cron, solo lo programa. Para ejecución inmediata, usar `write_file` directo.
- **Bloques temáticos completos antes de commit**: mejor un commit "BLOQUE X COMPLETO" que 3 commits parciales del mismo bloque.
- **Template HTML reutilizable**: el CSS + estructura base es idéntica en todos los temas. Solo cambian: título, contenido, SVG, ejercicios. No regenerar el CSS cada vez.
- **SVGs inline**: cada tema necesita 1 SVG mínimo con viewBox 600x300 mínimo. Usar colores semánticos consistentes (azul=PV, naranja=PH, verde=resultado).
- **4-5 ejercicios por tema**: mix de quiz (4 opciones), V/F, completar texto. Siempre con feedback inmediato.
- **Footer obligatorio**: "Hecho con ❤️ por David Antizar" en todos los HTML.
- **Navegación prev/next**: siempre actualizar los enlaces al final de cada HTML. Si el siguiente no existe aún, dejar el link apuntando al ID esperado.
