---
name: educational-html-pipeline
description: "Pipeline completo de HTML educativos: generación desde template (Dibujo Técnico), mejora nocturna iterativa (DeSumarIntegrar), quality gates, SVG interactivo, quizzes, y deploy a GitHub Pages. Incluye ambos proyectos."
version: "1.0.0"
tags: [html, education, svg, quiz, github-pages, dibujotecnico, desumarintegrar, quality-gates]
---

# Educational HTML Pipeline — Generación y Mejora de HTML Educativos

## Resumen

Pipeline completo para crear y mejorar HTML educativos interactivos en dos proyectos:
- **Dibujo Técnico** (`/root/workspace/DibujoTecnico`) — generación desde template
- **DeSumarIntegrar** (`/root/workspace/DeSumarIntegrar`) — mejora iterativa nocturna

## 1. Generación de Temas (Dibujo Técnico)

### Flujo
1. Cargar skill TD fuente (`skill_view(name='stem/td/<nombre>')`)
2. Verificar archivos existentes vs progress.json (detectar nombres mismatch)
3. Leer template en `generate_td.py` (líneas 8-136)
4. Mapear contenido → rellenar placeholders
5. Generar SVG interactivo inline (mínimo 6-8 tipos visuales, viewBox 700x520)
6. Generar HTML completo con `write_file`
7. Verificar calidad (>12KB, tiene `<svg`, tiene `quiz-btn`)
8. Actualizar progress.json → Git commit + push

### Placeholders del template
{title}, {subtitle}, {key_idea}, {learning_goals}, {theory_title}, {theory_text}, {example_1/2/3}, {interactive_title}, {interactive_desc}, {svg_content}, {interactive_content}, {exercises_html}, {summary_items}, {prev_link}, {next_link}, {js_code}

### Funciones JS requeridas
- `checkAnswer(btn, isCorrect, resultId)` — quizzes selección múltiple
- `checkExercise(btn, isCorrect, resultId)` — ejercicios selección
- `checkVF(btn, isCorrect, resultId)` — Verdadero/Falso
- `showPaso(n)` — SVG paso a paso (usar inline style.display, NO CSS global)

### Pitfalls de generación
- **NUNCA usar `read_file` para leer progress.json** → prependea números de línea → rompe JSON. Usar `terminal("cat ...")` + `json.loads()`
- **NUNCA usar `patch` para HTML** → siempre `write_file` con contenido completo
- **Mínimo 12KB de contenido real** — cada tema debe tener: SVG, 3+ ejemplos, 5 ejercicios, teoría, error clásico, resumen
- **GitHub Pages requiere `index.html` (minúsculas)** — `INDEX.html` → 404
- **CSS con dobles llaves `{{}}`** — puede venir de template engine, romper estilos. Detectar con `grep -n '{{' *.html`
- **Nombres de archivo en progress.json ≠ archivos reales** — verificar con `os.path.exists()`

### Deploy a GitHub Pages
1. Renombrar INDEX.html → index.html
2. Push a master/main
3. Activar Pages via API
4. Verificar con `curl -s -o /dev/null -w "%{http_code}" URL`

## 2. Mejora Nocturna Iterativa (DeSumarIntegrar + DibujoTecnico)

### Flujo de mejora
1. **Seleccionar temas** — priorizar menos improvement_count, rotación de niveles, excluir mejorados hoy
2. **Backup** — `cp tema.html tema.html.bak`
3. **Analizar** — evaluar 8 dimensiones: exercises, text, visual, real_world, connections, difficulty_range, manim_quality, css_coherence
4. **Mejorar** — exactamente lo que falta (máx 3 ejercicios nuevos, tipos diferentes)
5. **Quality Gates** — HTML válido, ejercicios funcionales, CSS coherence (17 clases), títulos únicos
6. **Si gate falla → REVERTIR** — `cp tema.html.bak tema.html`
7. **Si OK → actualizar progress.json + git commit**

### Dimensiones de evaluación
| Dimensión | Qué buscar |
|-----------|-----------|
| exercises | 3+ tipos diferentes (quiz, VF, completar, ordenar, problema, emparejar, input) |
| text | Patrón 4 pasos: qué es → para qué → cómo → error |
| visual | SVG/gráfico informativo (no decorativo) |
| real_world | Casos cotidianos concretos |
| connections | Connection-box con enlaces a temas relacionados |
| difficulty_range | Badges easy/medium/hard |
| manim_quality | SVG animado para bachiller/universidad |
| css_coherence | TODAS las clases del template base |

### CSS Coherente — 17 clases requeridas
`header`, `container`, `chapter-title`, `box`, `box-teoria`, `box-ejemplo`, `box-error`, `box-idea`, `box-success`, `interactive`, `exercises`, `exercise`, `quiz-options`, `quiz-btn`, `summary`, `nav`, `footer`

### CSS Coherence Drift — Patrón detectado
Muchos temas tienen CSS custom en vez del template base. Diferencias típicas:
- `.comparison` grid vs flex
- `.step-dot` 32px vs 12px
- `.real-world-badge` con gradient vs sin gradient
- `.stack-item` con fondo gris vs borde azul

**Corrección:** reemplazar CSS custom con template base completo.

### Variables CSS obligatorias
`--azul:#2563eb`, `--naranja:#f97316`, `--verde:#10b981`, `--rojo:#ef4444`

### Clases CSS siempre faltantes
- `.feedback`, `.feedback.correct`, `.feedback.incorrect` — siempre añadir
- `.svg-container` — añadir si falta
- `.difficulty-badge`, `.difficulty-badge.easy/medium/hard` — añadir si falta
- `.connection-box` — usar `class="connection-box"` (con 'n', no `conexion-box`)

### Pitfalls críticos de mejora
- **DOBLE ESCAPE KATEX** — `$\\\\\\\\pm$` vs `$\\\\pm$` — verificar con grep tras patch
- **CONVERSIÓN KATEX EN PATCHES** — el patch tool puede escapar barras invertidas
- **read_file con offset/limit no carga todo** — siempre leer archivo completo antes de patchear
- **PATCH ENTRE </div> PIERDE WRAPPER** — verificar estructura HTML tras patch
- **FUNCIONES JS DUPLICADAS** — contar con grep, eliminar duplicadas
- **CLOSURE ONCLICK ROTO** — `onclick="checkFillIn(['respuesta'])()"` → cambiar a `onclick="checkFillIn(['respuesta'])(this)"`
- **Ejercicios FUERA de div.exercises** — verificar y mover dentro del wrapper
- **Añadir V/F requiere función JS** — verificar `checkVF` existe antes de patchear ejercicio
- **box-success definido pero nunca usado** — añadir al menos un box-success cuando se mejora real_world
- **NO bajar scores ya en 10** — nunca reducir un score máximo existente
- **progress.json improvements puede ser string o lista** — normalizar antes de append
- **DibujoTecnico progress.json: claves con .html y scores anidados** — estructura diferente a DeSumarIntegrar
- **SVG interactividad ronda 2** — toggleHighlight con data-info, mínimo 5 elementos
- **`.bak` files en git** — siempre hacer `git rm --cached *.bak && rm -f *.bak && git commit --amend`

### MODO RÁPIDO (batch 4-6 temas)
- 1 acción por dimensión: 1 CSS batch, 1 caso real, 1 error comparativo
- Usar `execute_code` (Python) para todo: leer, patchear, actualizar progress.json
- Git commit después de cada batch
- NO hacer SVGs interactivos nuevos en modo rápido

### Casos reales por bloque (Dibujo Técnico)
| Bloque | Caso real |
|--------|-----------|
| b02 Proyecciones | Biela de motor, brida de tubería |
| b03 Perspectivas | Tuercas/arandelas, planos arquitectónicos |
| b04 Diedrico | Control calidad CMM, cableado/tuberías |
| b05 Cortes | Motor de combustión, carcasa bomba |
| b06 Acotación | Pieza aeronáutica, taladrero CNC |
| b07 Intersecciones | Unión tuberías HVAC, vigas acero |

### Errores comparativos por bloque
| Bloque | Error típico |
|--------|-------------|
| b02 | Planta encima del alzado, confundir X con Z |
| b03 | Círculo en vez de elipse en isométrica |
| b04 | Punto en 2º diedro, recta paralela a LT |
| b05 | Corte total innecesario, sin corte |
| b06 | Cota dentro del objeto, cotas en cadena |
| b07 | Intersección recta en vez de curva |

## 3. Pipeline Auditoría → Corrección → Generación → Deploy

Cuando el usuario pide completar y desplegar un proyecto HTML:
1. **Auditoría** — cargar `audit-html-project`, escaneo masivo, generar informe
2. **Corrección críticos** — enlaces rotos, archivos huérfanos, commit
3. **Generación temas faltantes** — batch de 3-6 temas, actualizar progress.json
4. **Deploy** — push a GitHub, activar Pages, verificar

## Reglas de oro
- NO crear temas nuevos — solo mejorar existentes (modo mejora)
- NO más de 3 ejercicios nuevos por tema
- NO ejercicios del mismo tipo seguidos
- NO SVG decorativos sin propósito
- Si un quality gate falla, REVERTIR — no hacer commit con HTML roto
- Siempre usar backup antes de cualquier cambio
- Cada commit debe ser autónomo y funcional

## Referencias
- `references/curriculum-map.md` — Mapa completo del curso Dibujo Técnico
- `references/svg-perspectiva-isometrica.md` — Patrón SVG ejes isométricos
- `references/patrones-ejercicios.md` — Patrones de ejercicios interactivos
- `references/casos-reales-industriales.md` — Banco de casos reales por bloque
- `references/css-coherence-drift.md` — Detección y corrección de CSS drift
- `references/patron-svg-paso-a-paso-interactive.md` — Patrón SVG interactivo paso a paso
- `references/katex-double-escape-fix.md` — Detección y corrección doble escape KaTeX
- `references/closure-onclick-fix.md` — Patrón closure onclick roto y fix
- `references/svg-interactivity-pattern.md` — Patrón toggleHighlight con data-info
- `references/duplicate-content-after-patch.md` — Detectar contenido duplicado tras patch
- `references/svg-animation-pattern.md` — Patrón CSS keyframes para SVG animado
- `references/svg-area-model-decimal.md` — Patrón SVG modelo de área (primaria)
- `references/svg-bar-chart-calendar.md` — Patrón SVG gráfico de barras
- `references/svg-zigzag-pattern.md` — Patrón SVG zigzag animado
- `references/ronda2-selection-pattern.md` — Patrón selección temas score 9 (ronda 2)
- `references/dibujotecnico-ronda2-patterns.md` — Diferencias DibujoTecnico vs DeSumarIntegrar
- `references/naming-mismatch-progress-json.md` — Nombres de archivo mismatch
- `references/quality-gates-checklist.md` — Checklist visual quality gates
