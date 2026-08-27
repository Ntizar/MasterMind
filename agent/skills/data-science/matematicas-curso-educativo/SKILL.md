---
name: matematicas-curso-educativo
description: "DeSumarIntegrar — Curso completo de matemáticas de 1º Primaria a 1º Carrera: 107+ HTML interactivos con KaTeX, Plotly.js, ejercicios con feedback. Sistema de mejora continua con cron cada 30min. CALIDAD sobre cantidad — variedad de ejercicios, visuales solo si aportan."
version: 1.11.0
category: education
tags: [data-science, education, math, html, interactive]
---

# DeSumarIntegrar — Curso de Matemáticas Completo

Curso de matemáticas de Ntizar (David Antizar) que cubre desde 1º Primaria hasta 1º de Carrera universitaria. 107+ archivos HTML interactivos, ~1.2 MB.

## Referencias

- `references/cron-course-generation-pattern.md` — Patrón de generación de cursos educativos con crons encadenados: mega-plan + progress.json + cron generador auto-actualizable + cron verificador diario. Aplica a cualquier materia, no solo matemáticas.
- `references/progress-json-schema.md` — Schema de progress.json, campos de scores, pitfall de conteo canvas
- `references/cron-mejora-continua-config.md` — Configuración del cron de mejora continua, historial de ejecuciones
- `references/patch-escape-js-multiline.md` — Pitfall: patch() escapa newlines al insertar JS multilinea en HTML
- `references/css-bar-chart-primaria.md`
- `references/css-grid-cards-table.md` — Patrón de tabla de tarjetas CSS con grid para mostrar tablas completas de resultados en primaria (reemplazo ligero de Plotly). Colores semánticos (verde/naranja/rojo). — Patrón de gráfico de barras CSS+emoji para primaria (sin Plotly). Plotly SOLO en Bachiller/Universidad (ver `primaria-plotly-pattern.md` para la excepción).
- `references/canvas-interactivo-primaria.md` — Patrón canvas interactivo (pizarra mágica) para temas de figuras geométricas en primaria
- `references/canvas-figuras-compuestas.md` — Patrón canvas de figuras compuestas seleccionables (L/T/H) con quiz integrado. Diferente de pizarra mágica: es evaluación, no dibujo libre.
- `references/canvas-balanza-peso.md` — Patrón de balanza interactiva para temas de peso/masa en primaria: animales con pesos reales, click para revelar, comparación visual
- `references/primaria-plotly-pattern.md` — Patrón para añadir Plotly a archivos de primaria: CDN, contenedor, JS con guard, verificación.
- `references/css-decimal-alignment-grid.md` — Patrón de CSS grid para visualizar alineación de comas decimales (sin canvas). Útil para temas de sumar/restar decimales en primaria.
- `references/audit-completo.md` — Script de auditoría completa del proyecto: cobertura de tecnologías (KaTeX, Plotly, ejercicios, interactividad), estado CSS (glassmorphism, variables, inline styles), por nivel, temas pendientes. Resultado 2026-06-13: 101 archivos, glassmorphism ausente en 97/101, 52/101 con >15 estilos inline, ESO sin Plotly, 17 pendientes (12 estadística).
- `references/problema-inverso-pista-contextual.md` — Patrón de ejercicios inversos (hallar minuendo/sustraendo/factor) con pistas contextuales en feedback. Incluye tabla de 4 tipos de problema inverso.
- `references/write-file-python-escaping.md` — Patrón de escape de comillas simples en write_file con Python triple-quoted strings para HTML con JS inline.
- `references/individual-feedback-functions-pattern.md` — Patrón de funciones individuales con feedback rico (checkE6, checkE7...) vs funciones unificadas. Regla de decisión: usar individual solo cuando cada ejercicio necesita explicación específica del "por qué".
- `references/primaria-plotly-dynamic-chart.md` — Patrón para gráficos Plotly de barras con botones interactivos (randomizar/ordenar) en primaria.
- `references/connection-box-pattern.md` — Patrón de caja pedagógica "Conexión" que conecta el tema actual con algo ya aprendido.
- `references/connection-espejos-pattern.md` — Patrón de conexión restar↔sumar como "espejos" (inversas). NUNCA usar multiplicación como analogía para restar en 1º Primaria.
- `references/mnemonic-trick-pattern.md` — Patrón de caja "Truco mnemotécnico" con analogía visual para recordar conceptos abstractos.
- `references/complete-repeated-addition-pattern.md` — Patrón de ejercicio "completar suma repetida" para introducción a multiplicación: `3 × 4 = __ + __ + __`.
- `references/exercise-type-verification.md` — Script Python para verificar programáticamente la variedad de ejercicios antes de commitear.
- `references/progress-filename-mapping.md`
- `references/canvas-fracciones-equivalentes.md` — Patrón canvas de barras divididas para visualizar equivalencia de fracciones (1/2 = 2/4 = misma área). — Las keys de progress.json NO son nombres de archivo reales. Mapeo conocido y regla de verificación.
- `references/svg-recta-numerica.md` — Patrón de recta numérica interactiva con SVG (clic en números, muestra signo y valor absoluto). Ideal para temas de enteros en ESO. Diferente del canvas: accesible, escalable, estilizable con CSS.
- `references/bulk-html-insert-pattern.md` — Patrón para insertar múltiples bloques HTML en posiciones específicas usando Python `.replace()` en execute_code. Útil cuando archivo > 20KB y necesitas 3+ inserciones.
- `references/exercise-variety-matrix.md` — Matriz de tipos de ejercicio para archivos con 0 ejercicios. Enfoque de 2-3 ejercicios por capítulo, cada tipo diferente, con 1 caso real + 1 error común por capítulo.
- `references/order-radio-pattern.md` — Patrón para ordenar con radio buttons (3+ items, sin tracking de estado global).
- `references/landing-page-improvement-pattern.md` — Patrón para mejorar páginas landing/index: mini quiz interactivo (1-3 quizzes), caso real cotidiano, caja "¿Sabías que?", glassmorphism, tags por categoría. Diferente de páginas de lección.
- `references/quality-improvement-pattern.md` — Patrón programático de mejora de calidad: análisis previo del HTML, mapeo progress.json→archivo real, funciones JS reutilizables (checkVF, checkOrden), verificación post-mejora. v1.3.0 con lecciones 2026-06-10. Incluye pitfall página índice vs lección con patrón de mejora para landing pages (multi-quiz 3 preguntas, caso real, caja ¿Sabías que?).
- `references/improvement-cron-workflow.md` — Workflow programático para encontrar el primer tema pending que existe (mapeo progress.json → archivo real, código Python de referencia).
- `references/exercise-types-catalog.md` — Catálogo completo de 19 tipos de ejercicio (quiz, completar hueco, V/F, ordenar click, ordenar texto, problema contextualizado, problema cálculo, input texto, sección intermedia, encontrar regla, identificar NO-patrón, crear patrón, completar ritmo, emparejar sumas iguales, conteo visual emojis, decidir operación, emparejar incorrecta, ordenar por resultado, completar hueco multi-pasos) con HTML/JS de referencia y patrón de análisis previo.
- `references/write-file-vs-patch.md` — Cuándo usar write_file vs patch para HTML de DeSumarIntegrar. Regla: ≤20KB + 3+ cambios estructurales → write_file. Incluye patrón de JS unificado (checkE, checkVF, selectQuiz, checkOrder) descubierto 2026-06-10.
- `references/canvas-balanza-peso.md` — Patrón de canvas para balanza interactiva (temas de peso/masa en primaria).
- `references/js-unified-functions-pattern.md` — Patrón de funciones JS unificadas para mejoras de calidad: checkE(num, correct), checkVF(num, expected), selectQuiz(num, btn, selected), checkOrderN(). Diccionario interno de respuestas, reutilizable entre ejercicios.
- `references/calidad-sobre-cantidad.md` — Criterios de calidad: variedad de ejercicios, vida real, visuales útiles, estructura clara.
- `references/eliminar-antes-anadir.md` — Principio de eliminar ejercicios repetitivos ANTES de añadir nuevo contenido. Regla: ningún tipo >30% del total, ≥4 tipos diferentes.
- `references/exercise-types-session-2026-06-10.md` — 3 tipos nuevos descubiertos 2026-06-10: completar hueco inverso (hallar dividendo), problema inverso con doble input (conectar ×÷), ordenar por texto libre (input con coma). Regla de variedad actualizada: ningún tipo >30% del total.
- `references/hueco-multi-pasos.md` — Patrón de completar hueco con múltiples inputs inline (2-5) para enseñar procedimientos de varios pasos: descomposición de multiplicaciones, fracciones equivalentes, pasos intermedios. Diferente de completar hueco simple (1 input).
- `references/ejercicio-comparar.md` — Patrón de ejercicio de comparar (mayor/menor resultado) para entrenar pensamiento relacional. No es cálculo, es comparación.
- `references/consistency-verification.md` — Checklist para verificar que los enunciados de ejercicios coinciden con las funciones JS que los validan (IDs, números, booleanos).
- `references/canvas-linea-numerica-sapo.md` — Patrón de canvas interactivo de línea numérica con "sapo que salta": dibujo línea 0-20, círculo verde en posición inicial, flecha naranja hacia atrás, círculo azul en resultado. Reemplazo ligero de Plotly para visualización de resta en primaria. Diferente de `svg-recta-numerica.md` (SVG para ESO) y `canvas-balanza-peso.md` (balanza para peso).

- `references/rapid-batch-improvement.md` — patrón de MODO RÁPIDO: mejora batch de 4-6 temas por sesión con rotación obligatoria de niveles (Primaria → ESO → Bachiller). Diferente de mejora individual: selección por prioridad+nivel_rotado, plantilla uniforme por tema, git commit uno por tema.
- `references/css-audit-and-standarization.md` — Patrón de auditoría CSS por niveles y estandarización. Los 4 niveles (Primaria, ESO, Bachiller, Universidad) tenían cobertura CSS desigual: Primaria 47 clases, ESO 34 clases, Bachiller 28 clases, Universidad 42 clases. Incluye lista de 20 clases esenciales, bloques CSS por nivel, patrón de auditoría Python y resultados post-estandarización.
- `references/css-visual-verification.md` — Patrón de verificación visual completa con `browser_vision()`. No confundir "clases CSS existen" con "archivo se ve bien". Incluye umbrales mínimos por nivel y priorización (CRÍTICO <20, ALTO 20-30, MEDIO 30-35, BAJO 35+).

- **v1.11.0 (2026-06-13):** Added `references/audit-completo.md` — patrón de auditoría completa del proyecto. Hallazgos: 101 archivos HTML, glassmorphism ausente en 97/101, 52/101 con >15 estilos inline, ESO sin Plotly, 17 pendientes (12 estadística). Added pitfall: "glassmorphism ausente como problema sistémico" — 97/101 archivos sin `backdrop-filter`, el sello visual de Aurora. Added pitfall: "estilos inline excesivos" — 52/101 con >15 inline styles. Added pitfall: "ESO sin Plotly" — 0/11 con gráficos. Added pitfall: "17 temas pendientes" — laguna de estadística. Added pitfall: "duplicado s04-4". Added sección "Auditoría programática completa" con patrón reutilizable.
- **v1.10.1 (2026-06-12):** Added `references/css-visual-verification.md` — patrón de verificación visual completa con browser_vision(). Lección: David vio CSS "roto" en ESO 2º/3º a pesar de la estandarización. No confundir "clases CSS existen en el archivo" con "el archivo se ve bien". Incluye umbrales mínimos por nivel (Primaria 35+, ESO 40+, Bachiller 38+, Universidad 40+) y priorización (CRÍTICO <20, ALTO 20-30, MEDIO 30-35, BAJO 35+). Added pitfall: "CSS roto percibido por el usuario" en SKILL.md body.
- **v1.10.0 (2026-06-12):** Added `references/css-audit-and-standarization.md` — patrón de auditoría CSS por niveles y estandarización. Descubierto que los 4 niveles del proyecto (Primaria, ESO, Bachiller, Universidad) tenían CSS con diferente cobertura de clases: Primaria 47 clases, ESO 34 clases, Bachiller 28 clases, Universidad 42 clases. Solución: script que añade bloques CSS faltantes (feedback, chart-container, connection-box, step-indicator, real-world-badge, svg-container, exercise-input, interactive) a cada nivel. Ver sección "Estandarización CSS" en SKILL.md.
- **v1.9.7 (2026-06-10):** Added `references/consistency-verification.md` — pitfall de inconsistencia HTML↔JS descubierto 2026-06-10.
- **v1.9.8 (2026-06-10):** Added `references/canvas-linea-numerica-sapo.md` — patrón canvas de línea numérica interactiva con sapo que salta para restar visualmente en primaria. Reemplaza Plotly cuando es excesivo.
- **v1.9.6 (2026-06-10):** Added `references/hueco-multi-pasos.md` (patrón de completar hueco multi-pasos con 2-5 inputs inline para descomposición de multiplicaciones). Added exercise type 19 to `references/exercise-types-catalog.md`. Updated catalog count from 15 to 19 types.

## Repositorio

- **GitHub:** `Ntizar/DeSumarIntegrar`
- **Local:** `/root/workspace/DeSumarIntegrar/`
- **URL:** `https://ntizar.github.io/DeSumarIntegrar/`
- **Estado actual:** 101 archivos HTML (8 índices + 93 lecciones), 62 ejecuciones cron, 17 pendientes (12 estadística), glassmorphism ausente en 97/101

- **v1.9.5 (2026-06-10):** Added 3 new exercise types to `references/exercise-types-catalog.md`: tipo 16 (decidir operación), tipo 17 (emparejar: identificar pareja INCORRECTA), tipo 18 (ordenar por resultado). Added pitfall: "analogías confusas" — nunca usar multiplicación como analogía para restar en 1º Primaria; usar "espejos" (resta↔suma inversas) en su lugar.
- **v1.9.4 (2026-06-10):** Added `references/eliminar-antes-anadir.md` (principio de eliminar ejercicios repetitivos ANTES de añadir nuevo contenido). Added "REGLA DE ELIMINACIÓN" section to SKILL.md body.
- **v1.9.3 (2026-06-10):** Added `references/css-decimal-alignment-grid.md` (CSS grid para visualizar alineación de comas decimales, alternativa ligera a canvas). Added `references/problema-inverso-pista-contextual.md` (ejercicios inversos: hallar minuendo/sustraendo/factor con pistas contextuales).
- **v1.9.2 (2026-06-10):** Updated `references/landing-page-improvement-pattern.md` — multi-quiz landing pages (3 quizzes covering different topics), real-world case box, "¿Sabías que?" curiosity box. Updated `references/quality-improvement-pattern.md` — added landing page multi-quiz pattern.
- **v1.9.0 (2026-06-10):** Added `references/quality-improvement-pattern.md` patterns: input numérico con pista contextual (pista específica en vez de "intenta de nuevo"), conexión con el futuro (forward-looking, prepara para ESO), input-pattern CSS class.
- **v1.8.0 (2026-06-10):** Added `references/svg-recta-numerica.md` (recta numérica SVG interactiva para enteros ESO).
- **v1.8.1 (2026-06-10):** Added exercise types 14-15 (emparejar sumas iguales, conteo visual emojis) a `references/exercise-types-catalog.md`. Added canvas de línea numérica interactiva pattern a `references/quality-improvement-pattern.md`. Added `checkMatch` JS function pattern.
- **v1.7.0 (2026-06-10):** Added `references/canvas-fracciones-equivalentes.md` (canvas de barras divididas para visualizar equivalencia de fracciones), added pitfalls: canvas fracciones equivalentes, quiz negativo (identificar NO-equivalente), index page detection.
- **v1.6.2 (2026-06-10):** Added pitfall: index page vs lesson page detection — skip files without `<div class="exercise">` or `<div class="interactive">`. Updated `references/quality-improvement-pattern.md` with same pitfall.
- **v1.6.1 (2026-06-10):** Updated `references/quality-improvement-pattern.md` — added "eliminar contenido problemático" step, "problema inverso" exercise type, "caja de conexión" pattern, lecciones aprendidas (eliminar > añadir, coherencia temática, conexiones score 0→1+), pitfall de botones quiz con parámetro booleano. Updated scores objetivo: exercises 6-10 (variedad, no cantidad). Updated `references/bulk-html-insert-pattern.md` — added pitfall de duplicación por anclaje auto-referencial (insertar de abajo hacia arriba).
- **v1.5.0 (2026-06-10):** Added `references/canvas-balanza-peso.md` (canvas de balanza para peso/masa), added pitfall about missing `</div>` after exercise insertion, added progress stats (105 temas, 20 ejecuciones).
- **v1.4.0 (2026-06-09):** Added exercise types 10-13 (encontrar regla, identificar NO-patrón, crear patrón, completar ritmo), added variedad de ejercicios section, added bug duplicado opciones quiz.

## Stack
- KaTeX (CDN) para fórmulas LaTeX
- Plotly.js (CDN) para gráficos interactivos
- Responsive (móvil + escritorio)

## Filosofía pedagógica

1. **Intuición primero** — ejemplo de vida real antes que fórmula
2. **Visualización siempre** — gráfico interactivo para cada concepto clave
3. **Práctica con feedback** — ejercicios interactivos con respuesta inmediata
4. **Progresión suave** — cada sesión construye sobre la anterior
5. **Casos de uso reales** — "¿Dónde encuentro esto en la vida real?"

## Estructura del curso (10 niveles)

| Nivel | Sesión | Contenido | Archivos |
|-------|--------|-----------|----------|
| S01 | 1º-3º Primaria | Contar, sumar, restar, multiplicar, dividir, patrones, medidas | 15 HTML |
| S02 | 2º Primaria | Números grandes, fracciones intro, dinero | 15 HTML |
| S03 | 3º Primaria | Multiplicar, dividir, fracciones, perímetro, estadística | 8 HTML |
| S04 | 4º Primaria | Fracciones equivalentes, decimales, áreas, capacidades, problemas | 20 HTML |
| S05 | 5º Primaria | Decimales, porcentajes, estadística, tiempo, probabilidad | 7 HTML |
| S06 | 6º Primaria | Operaciones grandes, negativos, álgebra intro, potencias, ángulos | 7 HTML |
| S07 | 1º ESO | Enteros, proporcionalidad, ecuaciones, sistemas, estadística | 1 HTML (index) |
| S08 | 2º-3º ESO | Ecuaciones avanzadas, funciones, trigonometría, probabilidad | 1 HTML (index) |
| S09 | Bachiller | Límites, derivadas, integrales, probabilidad avanzada | 11 HTML |
| S10 | 1º Carrera | Multivariable, EDOs, Fourier, álgebra lineal | 11 HTML |

## Plantilla HTML de sesión

Cada sesión sigue esta estructura exacta:

```
<header class="header">
  <h1>{title}</h1>
  <p>{subtitle}</p>
  <div class="progress-bar"><div class="progress-fill"></div></div>
</header>

<main class="container">
  <section class="chapter">
    <h2>🎯 ¿Qué vamos a aprender?</h2>
    <div class="box box-idea">💡 Idea clave</div>
    <ul>Objetivos de aprendizaje</ul>
  </section>

  <section class="chapter">
    <h2>1️⃣ {theory_title}</h2>
    <div class="box box-teoria">📖 Teoría</div>
    <div class="box box-ejemplo">🔍 Ejemplo 1</div>
    <div class="box box-ejemplo">🔍 Ejemplo 2</div>
    <div class="box box-ejemplo">🔍 Ejemplo 3</div>
  </section>

  <section class="chapter">
    <h2>2️⃣ {interactive_title}</h2>
    <div class="interactive">
      <h3>{interactive_desc}</h3>
      {interactive_content}
      <div class="result" id="interactiveResult"></div>
    </div>
  </section>

  <section class="chapter">
    <h2>📝 Ejercicios</h2>
    <div class="exercises">
      {exercises_html}
    </div>
  </section>

  <div class="summary">📋 Resumen de lo aprendido</div>
  <div class="nav">
    <a href="{prev_link}">← Anterior</a>
    <a href="{next_link}">Siguiente →</a>
  </div>
</main>

<footer class="footer">Hecho con ❤️ por David Antizar</footer>
```

## CSS variables (tokens)

```css
--azul: #2563eb
--naranja: #f97316
--verde: #10b981
--rojo: #ef4444
--pura: #a855f7
--fondo: #fff
--texto: #1e293b
--gris: #94a3b8
```

## Cajas de contenido

| Clase | Color | Uso |
|-------|-------|-----|
| `box-teoria` | Azul claro | Explicación teórica |
| `box-ejemplo` | Naranja claro | Ejemplos resueltos |
| `box-error` | Rojo claro | Errores comunes |
| `box-idea` | Púrpura claro | Idea clave / intuición |
| `box-success` | Verde claro | Confirmación / éxito |

## Generador Python (`generate_all.py`)

El script usa un template string con placeholders y un array `ALL_SESSIONS` con la definición de cada sesión.

**Campos de cada sesión:**
- `file` — nombre del archivo HTML
- `title` / `subtitle` — título y subtítulo
- `key_idea` — intuición principal
- `learning_goals[]` — objetivos en formato `<li>`
- `theory_title` / `theory_text` — sección de teoría
- `example_1/2/3` — ejemplos resueltos
- `interactive_title` / `interactive_desc` / `interactive_content` — zona interactiva
- `exercises_html[]` — array de `{q, opts, correct}`
- `summary_items[]` — puntos clave del resumen
- `prev_link` / `next_link` — navegación
- `js_code` — JavaScript interactivo

**Ejemplo de ejercicio:**
```python
{"q": "¿Cuánto es 240 ÷ 12?", "opts": ["20", "24", "12"], "correct": 0}
```

## Criterio de "sesión hecha"

1. ✅ KaTeX para fórmulas LaTeX (ESO+)
2. ✅ Al menos 1 gráfico interactivo Plotly.js
3. ✅ Al menos 3 ejercicios interactivos con feedback
4. ✅ Caso de uso real explicado
5. ✅ Resumen final con puntos clave
6. ✅ Navegación Anterior/Siguiente
7. ✅ Atribución "Hecho con ❤️ por David Antizar"
8. ✅ Responsive (móvil + escritorio)
9. ✅ Contenido matemático correcto y claro
10. ✅ Intuición antes que fórmula

## Generación con crons encadenados (patrón 2026-06-10)

Para cursos de 20+ temas, usar el patrón de **crons auto-actualizables**:

1. **Mega-plan** — definir toda la estructura (temas, progresión, template)
2. **Cron generador** — lee `progress.json`, carga skill fuente, genera HTML, se actualiza para el siguiente tema
3. **Cron verificador** — diario, revisa HTMLs generados (SVG, ejercicios, navegación, atribución)

Ver `references/cron-course-generation-pattern.md` para el patrón completo.

**Este patrón aplica a cualquier materia**, no solo matemáticas. Ejemplo: Dibujo Técnico (53 temas, 9 bloques) usa exactamente el mismo sistema.

## Generación con crons (patrón histórico)

El sistema usaba crons `once` para generar sesiones automáticamente.

## Auditoría y mantenimiento

El proyecto ha pasado 2 auditorías completas:
- **Corrección de links rotos** — s01-4primaria, s02-7primaria
- **Índices faltantes** — creados s01-1primaria-index, s02-2primaria-index, s03-3primaria-index
- **KaTeX** — añadido a todos los archivos ESO/Bachiller/Carrera
- **Navegación** — reconstruida para 73 sesiones detalladas (orden numérico, no alfabético)
- **Transiciones entre niveles** — s01-10 → s02-1, s06-10 → s07-1
- **Atribución** — añadida a todos los archivos

## Mejora continua (cron nocturno)

Cada ejecución del cron mejora EXACTAMENTE UN tema, añadiendo ejercicios y contenido de calidad.

### Procedimiento

1. **Leer** `progress.json` → buscar temas con `status: "pending"` primero, ordenados por `priority` (1 primero)
2. **Si no hay pending** → buscar temas con `improvement_count < 4` y prioridad más baja
3. **Si todos complete** → terminar con "Todos los temas están al máximo nivel"
4. **Leer** el HTML del tema seleccionado
5. **Analizar** conteo de: ejercicios (clase "exercise"), teoría (clase "box-teoria"), ejemplos (clase "box-ejemplo"), canvas/Plotly, casos reales, KaTeX
6. **Generar mejoras** según nivel (ver tabla abajo)
7. **Insertar** mejoras con `patch()` ANTES del cierre `</main>` / ANTES de la navegación `<div class="nav">`
8. **Añadir funciones JS** si faltan (`checkAnswer` para quiz, `checkExercise` para input)
9. **Actualizar** `progress.json`: incrementa `improvement_count`, `last_improved`, status = `improved_N` o `complete` si >= 4
10. **Git commit + push**

### MODO RÁPIDO (batch — 4-6 temas por sesión)

Para sesiones con recursos suficientes (agentes manuales, cron especiales), existe un **modo batch** que mejora 4-6 temas en una ejecución. **Ver `references/rapid-batch-improvement.md`** para el procedimiento completo.

**Diferencias clave:**
- Selección con **rotación de niveles obligatoria** (P → ESO → B → P...)
- **Plantilla uniforme** por tema: explicación 4 pasos + 2-3 tipos de ejercicio + caso real + error común
- Git commit **uno por tema**, no al final
- Máximo 6 temas por sesión (límite de tokens)

**Cuándo usar batch:** sesiones de mejora rápida planificadas, cuando se quiere cobertura amplia de niveles en una ejecución.
**Cuándo NO usar batch:** cuando se necesita profundidad pedagógica en un tema específico, o cuando se está debuggeando un problema concreto.

### Tabla de mejoras por nivel

| Nivel | Ejercicios nuevos | Explicaciones | Visualizaciones | Notas |
|-------|-------------------|---------------|-----------------|-------|
| Primaria (s01-s06) | 3-5 con emojis | 2-3 con analogías vida real | 1 canvas simple | Objetos cotidianos (juguetes, comida, dinero) |
| ESO (eso1, eso2, s07, s08) | 3-5 con KaTeX | 2-3 con intuición antes fórmula | 1-2 gráficos Plotly | Tablas resumen, conexiones con temas anteriores |
| Bachiller (s09) | 4-6 dificultad creciente | 3-4 conceptuales profundas | 2-3 Plotly (incl. interactivos) | Problemas física/economía, tipo examen |
| Universidad (s10) | 3-5 notación avanzada | 2-3 profundas | 2-3 gráficos 3D Plotly | Conexiones interdisciplinares, papers |

### Formato de ejercicios

**Primaria (quiz con botones):**
```html
<div class="exercise">
<p>🍎 Ejercicio X: [Descripción con emoji]</p>
<div class="quiz-options">
<button onclick="checkAnswer(this, true)">Opción correcta</button>
<button onclick="checkAnswer(this, false)">Opción incorrecta</button>
</div>
<p class="feedback"></p>
</div>
```

**ESO/Bachiller/Uni (input de texto):**
```html
<div class="exercise">
<p>📝 Ejercicio X: [Descripción con KaTeX si necesario]</p>
<div class="exercise-input">
<input type="text" id="exX" placeholder="Tu respuesta">
<button onclick="checkExercise('exX', 'respuesta', this)">Comprobar</button>
</div>
<p class="feedback"></p>
</div>
```

### Funciones JS necesarias

```javascript
function checkAnswer(btn, correct) {
  const parent = btn.parentElement;
  parent.querySelectorAll('button').forEach(b => {
    b.disabled = true; b.classList.remove('correct','wrong');
  });
  btn.classList.add(correct ? 'correct' : 'wrong');
  const feedback = parent.nextElementSibling;
  if(feedback && feedback.classList.contains('feedback')) {
    feedback.textContent = correct ? '✅ ¡Correcto! ¡Muy bien!' : '❌ ¡Intenta de nuevo!';
    feedback.className = 'feedback ' + (correct ? 'correct' : 'incorrect');
  }
}
function checkExercise(id, correct, btn) {
  const input = document.getElementById(id);
  const feedback = input.parentElement.nextElementSibling;
  const userVal = input.value.trim().toLowerCase();
  const correctVal = correct.toString().toLowerCase();
  if(userVal === correctVal) {
    feedback.textContent = '✅ ¡Correcto!';
    feedback.className = 'feedback correct';
    input.style.borderColor = 'var(--verde)';
  } else {
    feedback.textContent = '❌ Respuesta correcta: ' + correct;
    feedback.className = 'feedback incorrect';
    input.style.borderColor = 'var(--rojo)';
  }
}
```

### CSS para quiz-options (si no existe)

```css
.quiz-options{display:flex;gap:.5rem;flex-wrap:wrap;margin:.8rem 0}
.quiz-options button{flex:1;min-width:100px;padding:.6rem 1rem;border:2px solid #e2e8f0;border-radius:8px;background:#fff;cursor:pointer;font-size:1rem;font-weight:600;transition:all .2s}
.quiz-options button:hover{border-color:var(--azul);background:var(--azul-claro)}
.quiz-options button.correct{background:var(--verde);color:#fff;border-color:var(--verde)}
.quiz-options button.wrong{background:var(--rojo);color:#fff;border-color:var(--rojo)}
.quiz-options button:disabled{opacity:.6;cursor:not-allowed}
```

### Variedad de ejercicios (CRÍTICO)

**Problema:** Si no se fuerza explícitamente la variedad, el cron genera SIEMPRE el mismo tipo de ejercicio (quiz con 3 botones). David lo detectó y pidió revisión.

**Solución:** El prompt del cron debe incluir esta instrucción explícita:

> "Cada tema debe tener AL MENOS 4 TIPOS diferentes de ejercicio:
> 1. **Quiz con botones** (3-4 opciones) — para conceptos simples
> 2. **Completar hueco** (input de texto) — para cálculos
> 3. **Verdadero/Falso** (2 botones) — para afirmaciones conceptuales
> 4. **Problema con enunciado largo** — para aplicar múltiples pasos
> 5. **Ordenar** (drag/click para ordenar) — para comparar magnitudes
> 6. **Problema contextualizado** (caso real con datos) — para aplicar pasos
> 
> NO repitas el mismo tipo más de 3 veces seguidas."

**Catálogo de tipos de ejercicio:** Ver `references/exercise-types-catalog.md` (13 tipos documentados con HTML/JS de referencia: quiz, completar hueco, V/F, ordenar click, ordenar texto, problema contextualizado, problema cálculo, input texto, sección intermedia, encontrar regla, identificar NO-patrón, crear patrón, completar ritmo).

**Validación post-mejora:** Contar tipos de ejercicio y verificar que hay ≥3 tipos diferentes. Si solo hay 1 tipo, la mejora es defectuosa.

**Patrón de análisis previo (CRÍTICO — descubierto 2026-06-09):**
Antes de añadir ejercicios, SIEMPRE leer el HTML y contar qué tipos YA existen. Solo añadir tipos que NO estén representados. Ejemplo: si ya hay 5 quizzes, añadir 1 completar hueco, 1 V/F, 1 ordenar, 1 problema contextualizado — NO añadir más quizzes.

### Bug conocido: opciones duplicadas en quiz

**Problema:** Ejercicio 6 de `s01-1primaria.html` tenía DOS opciones "10 estrellas" — una marcada `true` y otra `false`. El alumno no puede distinguir.

**Causa:** El cron genera opciones sin verificar unicidad.

**Solución:** Añadir al prompt del cron:
> "Verifica que TODAS las opciones de cada quiz sean textos ÚNICOS. Nunca repitas el mismo texto en opciones diferentes."

### Actualización automática del README

El cron NO actualiza el README con el progreso. Para solucionarlo, añadir al prompt:
> "Tras cada mejora, actualiza la sección '🔄 Mejora Continua' del README.md con el estado actual de progress.json."

Ver `references/readme-auto-update-prompt.md` para el template exacto.

### REGLA DE ORO (User Preference — 2026-06-09)

**David dice: "No implementes tantos ejercicios si son iguales y no aportan conocimiento. Centra todo en mejorarlo a mejor."**

Esto significa:
- ❌ NO añadir 10 ejercicios del mismo tipo (5+5=?, 3+2=?, 4+1=?)
- ✅ SÍ añadir 3-5 ejercicios VARIADOS (quiz, completar hueco, verdadero/falso, problema)
- ❌ NO añadir dibujos solo por cumplir
- ✅ SÍ añadir visuales SOLO si aportan al aprendizaje
- ❌ NO asumir que "más contenido = mejor"
- ✅ SÍ verificar que cada elemento añadido APORTE algo nuevo

**Criterio de calidad:** Si un ejercicio no enseña algo nuevo al alumno, NO lo añadas.

Ver `references/calidad-sobre-cantidad.md` para los criterios completos.

### REGLA DE ELIMINACIÓN (2026-06-10, actualizada 2026-06-10)

**Antes de añadir, eliminar repetitivo.**

Si un tema tiene >50% de ejercicios del mismo tipo, el problema NO es "falta contenido" — es "hay demasiado repetitivo".

Procedimiento:
1. Contar tipos de ejercicio existentes (NO solo cantidad total)
2. Si un tipo aparece >3 veces → eliminar los peores repetitivos
3. Añadir SOLO tipos que falten
4. Verificar: **ningún tipo >30% del total**, ≥4 tipos diferentes

Ver `references/eliminar-antes-anadir.md` para el procedimiento completo con ejemplos.
Ver `references/exercise-types-session-2026-06-10.md` para tipos nuevos (completar hueco inverso, problema inverso doble input, ordenar texto libre).

### Reglas de mejora continua

1. NO borrar contenido existente, SOLO añadir
2. Respeta el CSS existente del archivo
3. Usa las clases CSS que ya existen (`box-teoria`, `box-ejemplo`, `exercise`, `feedback`)
4. Mantén coherencia pedagógica (no saltar de dificultad)
5. Contenido matemático debe ser CORRECTO
6. Si tema tiene KaTeX, usar KaTeX en nuevos ejercicios
7. Si tema NO tiene KaTeX, no añadirlo (primaria no lo necesita)
8. SIEMPRE git commit + push al final
9. Actualizar progress.json con scores reales tras la mejora

### Auditoría programática completa

Cuando necesites un **diagnóstico completo** del proyecto (no solo mejora de un tema), usar el patrón de auditoría:

1. **Leer** `progress.json` → extraer todos los topics
2. **Listar** archivos HTML del directorio
3. **Para cada archivo no-índice:**
   - Contar KaTeX (`katex` en content)
   - Contar Plotly (`plotly` en content)
   - Contar ejercicios (`class="exercise"`)
   - Contar interactivos (`class="interactive"`)
   - Verificar CSS: `--azul`, `--naranja`, `backdrop-filter`, `body class="nz"`
   - Contar estilos inline (`style="..."`)
   - Contar reglas CSS (`<style>` blocks)
4. **Agrupar por nivel** (Primaria/ESO/Bachiller/Universidad)
5. **Generar resumen** con estadísticas por nivel y lista de problemas

**Resultado típico:** tabla con todos los temas, estado por nivel, y lista de issues prioritarios.

Ver `references/audit-completo.md` para el patrón completo.

### Pitfalls

- **Orden alfabético vs numérico** — archivos como `s01-10` aparecen antes que `s01-2` en sorting alfabético. La navegación debe seguir orden numérico pedagógico.
- **GitHub Pages** — requiere `index.html` (minúscula), no `INDEX.html`.
- **CSS inline** — el usuario rechazó CSS compartido. Cada archivo tiene su CSS inline para mantener personalidad visual por nivel.
- **Semantic HTML** — 54 archivos (indices) usan `<div>` en lugar de `<header>/<nav>/<main>`. Mejora pendiente.
- **progress.json scores inflados** — al contar elementos HTML, `canvas` aparece también en el JS embebido. Usar conteo manual o regex más preciso para evitar scores artificialmente altos.
- **`patch()` escapa newlines en JS multilinea** — cuando `patch()` inserta JavaScript con múltiples líneas en un HTML, puede corromper el contenido insertando literales `\n` en lugar de saltos de línea reales. **Solución:** después de patchear JS, verificar el archivo con `read_file` y si encuentras `\n` literales, reemplazarlos con un segundo `patch()` que use el texto correctamente formateado con saltos de línea reales. O bien, escribir el bloque JS completo con `write_file` si el archivo es < 20KB.
- **Plotly en primaria** — La regla general es Plotly SOLO en Bachiller/Universidad. Sin embargo, desde la ronda 2 de mejora continua se añadió Plotly a `s01-6-restar-hasta-20.html` con gráfico de barras simple. **Decisión:** Plotly se puede usar en primaria si se añade el CDN explícitamente y se usa `if(typeof plotly !== 'undefined')` como guard para evitar errores si el CDN falla. El patrón CSS+emoji sigue siendo preferible para primaria simple.
- **Mapeo progress.json → nombre real de archivo** — las keys en `progress.json` (ej. `s01-5primaria.html`) NO son los nombres reales de los archivos HTML. Los archivos reales están en `/root/workspace/DeSumarIntegrar/` y tienen nombres como `s01-5-restar-hasta-10.html`. **Siempre haz `ls` o `os.listdir()` para mapear la key al archivo real.** No asumas que la key de progress.json = nombre de archivo.
- **Etiqueta `<script>` anidada** — al añadir `<script src="https://cdn.plot.ly/...">` a un HTML que ya tiene un bloque `<script>...</script>`, la etiqueta CDN debe ir como hermano (fuera del bloque existente), no dentro. Si la pones dentro, se crea `<script><script src=...></script>` que es HTML inválido. **Verifica siempre con `read_file` tras el patch.**
- **Ejercicios todos del mismo tipo** (descubierto 2026-06-09) — Sin instrucción explícita, el cron genera SOLO quiz con botones. El prompt debe forzar al menos 4 tipos diferentes: quiz, completar hueco, verdadero/falso, problema largo. La variedad es CRÍTICA para la calidad percibida.
- **Opciones duplicadas en quiz** (descubierto 2026-06-09) — El cron puede generar dos opciones con el mismo texto (ej: dos "10 estrellas"). Añadir verificación de unicidad al prompt: "Cada opción de quiz debe tener texto ÚNICO".
- **README desactualizado** — El cron no actualiza el README con el progreso. Añadir paso de actualización. Ver `references/readme-auto-update-prompt.md`.
- **Revisión de calidad periódica** — David pregunta "¿cómo va esto?" y espera ver diff concretos. Después de cada ronda, mostrar resumen de cambios y pedir feedback antes de continuar. No asumir que "más contenido = mejor".
- **Funciones JS duplicadas en HTML** (descubierto 2026-06-09) — `sortCheck` aparecía dos veces en `s01-7-figuras-basicas.html`. Antes de patchear, verificar con `grep -c "function nombre" archivo` que no hay duplicados. Si hay duplicados, eliminar la segunda ocurrencia completa.
- **HTML tags rotos: `<h2>` sin `<section>`** (descubierto 2026-06-09) — En `s01-7-figuras-basicas.html`, el `<h2 class="chapter-title">2️⃣ ...` aparecía sin su `<section class="chapter">` envolvente. Antes de patchear, verificar la estructura de secciones con `grep -n "section\|h2" archivo`.
- **Literal `\n` en JS** (descubierto 2026-06-09) — `patch()` puede dejar literales `\n` en lugar de saltos de línea reales en bloques JS. Verificar siempre con `read_file` tras patchear JS y reemplazar si es necesario.
- **Ejercicio demasiado avanzado** (descubierto 2026-06-09) — No añadir ejercicios que requieran conceptos no enseñados aún. Ejemplo: perímetro de triángulo es demasiado avanzado para 1º Primaria que solo acaba de aprender las figuras. Verificar que cada ejercicio use SOLO conceptos ya enseñados en el tema.
- **Mejora manual vs cron** (2026-06-09) — Cuando se mejora un archivo manualmente (no vía cron), el workflow es: leer progress.json → buscar key → verificar nombre real de archivo con `find` o `ls` → leer HTML → analizar tipos existentes → patchear → commit + push + actualizar progress.json manualmente. El cron no actualiza progress.json en este caso.
- **write_file vs patch para archivos pequeños con cambios estructurales** (2026-06-09) — Cuando un archivo HTML es pequeño (< 20KB) y necesita múltiples cambios estructurales (nuevas secciones, nuevo CSS, nuevas funciones JS, nuevos ejercicios de tipos diferentes), `patch()` es propenso a errores (múltiples patches encadenados, riesgo de conflicto). **Solución:** usar `write_file` para reescribir todo el archivo de una vez. Es más limpio, más rápido, y evita problemas de escape de newlines en JS. La regla general: si necesitas 3+ patches distintos, usa `write_file`.
- **HTML tags rotos: `<li><li>` anidados** (2026-06-09) — Al generar HTML con bucles o templates, se pueden crear etiquetas `<li>` anidadas: `<li><li>texto</li></li>`. Esto rompe el renderizado. **Solución:** después de cualquier patch en HTML, verificar con `grep -c '<li><li>' archivo`. Si aparece, reemplazar con `<li>texto</li>` simple. También verificar con un script que cuente `<li>` y `</li>` para que sean iguales.
- **Tipos de ejercicio profundos faltantes** (descubierto 2026-06-09) — Los tipos "encontrar regla", "identificar NO-patrón", "crear patrón" y "completar ritmo" no estaban en el catálogo original. Añadidos en v1.4.0. Ver `references/exercise-types-catalog.md` tipos 10-13.
- **write_file + JS unificado para mejoras múltiples** (2026-06-10) — Cuando se añaden múltiples tipos de ejercicio nuevos (VF, ordenar, quiz botones, completar hueco) en un tema, **no usar patch() para cada función JS individual**. Usar write_file una vez con TODO el contenido (HTML + CSS nuevo + JS unificado). Las funciones JS deben ser unificadas: `checkE(num, correct)` para inputs numéricos, `checkVF(num, expected)` para V/F con diccionario interno, `selectQuiz(num, btn, selected)` para quiz botones, `checkOrderN()` para ordenar. Esto evita duplicación y hace las funciones reutilizables. Patrón visto en `s02-5primaria.html` (fracciones intro): antes tenía 2 funciones checkE separadas, después tiene checkE(num, correct), checkVF(num, expected), selectQuiz(num, btn, selected), checkOrder9() — todas unificadas.
- **Bulk HTML insertion via Python `.replace()`** (2026-06-10) — Cuando necesitas insertar múltiples bloques HTML (ejercicios, casos reales, errores comunes) en posiciones específicas de un archivo existente, **usar `execute_code` con Python `.replace()` en lugar de `patch()`**. Ventajas: no hay problema de escape de newlines en JS, se pueden hacer múltiples reemplazos en un solo paso, y se evita el riesgo de conflictos de `patch()`. **Cuándo usarlo:** archivo > 20KB (write_file demasiado grande) pero necesitas insertar 3+ bloques en posiciones distintas. **Patrón:** leer archivo completo → definir cada bloque como string → hacer `.replace(old, new)` encadenado → escribir con `write_file`. Ver `references/bulk-html-insert-pattern.md`.
- **CSS insertion via patch() before HTML blocks** (2026-06-10) — Cuando necesitas añadir clases CSS nuevas (`.quiz-options`, `.input-answer`, `.feedback`, `.check-btn`) a un HTML existente, **usar `patch()` sobre una línea CSS existente** (ej: `.footer{...}`) para insertar las nuevas clases justo antes. Esto es más limpio que `write_file` cuando solo necesitas añadir CSS sin tocar el HTML body. **Importante:** la línea de destino debe ser única en el archivo.
- **Falta `</div>` tras ejercicio al insertar nuevos** (2026-06-10) — Cuando insertas ejercicios nuevos DESPUÉS del último ejercicio existente, verificar que el último ejercicio anterior tenga su `</div>` de cierre. Al usar `.replace()` para insertar antes del siguiente bloque, a veces el ejercicio anterior queda sin cerrar. **Patrón de verificación:** tras cada inserción, hacer `grep -n '</div>' archivo | tail -10` y contar que los cierres coincidan con aperturas. Si el ejercicio N no tiene `</div>` antes del ejercicio N+1, añadirlo antes de continuar.
- **Ejercicio variedad matriz para archivos con 0 ejercicios** (2026-06-10) — Cuando un archivo tiene TODOS los scores a 0 (0 ejercicios, 0 casos reales, 0 errores comunes), el enfoque óptimo es añadir 2-3 ejercicios por capítulo, cada uno de tipo DIFERENTE, más 1 caso real + 1 caja error común por capítulo. No añadir más de 2-3 por capítulo para mantener variedad. Tipos a cubrir: completar hueco, V/F, problema contextualizado, ordenar, encontrar moda/media. Ver `references/exercise-variety-matrix.md`.
- **Duplicación por anclaje auto-referencial en bulk insert** (2026-06-10) — Cuando se insertan múltiples bloques con `.replace()`, si el bloque insertado contiene el texto de anclaje de un `.replace()` posterior, se duplica contenido. **Solución:** insertar de abajo hacia arriba (primer `.replace()` = anclaje más cercano al final del archivo). Ver `references/bulk-html-insert-pattern.md`.
- **Botones de quiz con parámetro booleano** (2026-06-10) — `checkQuiz(num, isCorrect)` espera `true`/`false`. Si se pasa un número (como el valor de la respuesta), se trata como `True` (truthy) y el botón incorrecto se marca como correcto. **Solución:** todos los botones deben pasar `true` o `false` explícitamente. Ver `references/quality-improvement-pattern.md`.
- **Ejercicios VF con lógica invertida** (2026-06-10) — Para detectar errores conceptuales, usar pares VF donde uno es verdadero y otro es la falacia inversa. Ejemplo: e5: "1/2 > 1/4 → Verdadero" + e6: "1/4 > 1/2 → Falso". Refuerza el concepto desde dos ángulos opuestos. checkVF usa diccionario `answers = {5: true, 6: false}`.
- **Consistencia HTML↔JS** (descubierto 2026-06-10) — Cuando se patchea un ejercicio, la función JS puede quedar desfasada: `id` referenced incorrecto, números de operación distintos al enunciado, parámetros booleanos invertidos. **Siempre verificar** que el `id="eNresult"` referenced por `onclick` exista, que los números coincidan, y que `true`/`false` estén en los botones correctos. Ver `references/consistency-verification.md` para el checklist completo.
- **Página índice vs página de lección** (2026-06-10) — Algunos archivos en progress.json (ej: `s04-4primaria.html`, `s07-1eso.html`, `s08-2-3eso.html`) son páginas índice/overview que listan sesiones pero NO tienen ejercicios interactivos. **Detección:** si el HTML no contiene `<div class="exercise">` ni `<div class="interactive">`, es un índice. **Acción:** saltar estos archivos en mejora continua, targetear solo archivos de lección reales. Los índices ya tienen contenido estático (tarjetas, resumen) que no necesita ejercicios.

- **Estructura HTML inconsistente entre niveles** (2026-06-12) — Los 4 niveles usan estructuras HTML distintas: Primaria/ESO usan `<header>`, `<main>`, `<section>`; Bachiller/Universidad usan `<div class="header">`, `<div class="container">`, `<div class="chapter">`. Esto significa que el CSS debe ser compatible con ambas estructuras. **No intentes unificar la estructura HTML** — cada nivel tiene su personalidad visual (Primaria con emojis grandes, Bachiller con KaTeX/Plotly, Universidad con púrpura). Solo unifica el CSS.

- **Glassmorphism ausente como problema sistémico** (2026-06-13) — 97/101 archivos NO tienen `backdrop-filter`. Esto es el sello visual del diseño Aurora y hace que las tarjetas se vean planas en lugar de tener el efecto glass elegante. No confundir con "clases CSS existen" — el glass es un detalle visual que no se detecta con un grep simple de clases. **Solución:** añadir `backdrop-filter: blur(10px)` + `background: rgba(255,255,255,0.8)` a las tarjetas `.box-*` en cada nivel. **Prioridad:** alta — David nota el "look de IA" y el glass es lo que diferencia el diseño Aurora de un HTML genérico.

- **Estilos inline excesivos** (2026-06-13) — 52/101 archivos tienen más de 15 estilos inline (`style="..."`). Esto va en contra del principio de CSS en `<style>` blocks y hace el código más difícil de mantener. **Solución:** extraer los estilos inline a clases CSS en el bloque `<style>` del archivo. **Prioridad:** media — no afecta la funcionalidad pero sí la mantenibilidad.

- **ESO sin Plotly** (2026-06-13) — 0/11 archivos de ESO tienen gráficos Plotly. Solo Primaria (2/57) y Bachiller/Uni los usan. **Solución:** añadir al menos 1 gráfico Plotly a cada tema de ESO. **Prioridad:** media — los gráficos interactivos mejoran la comprensión de conceptos abstractos como ecuaciones y funciones.

- **17 temas pendientes** (2026-06-13) — 12 de los 17 pendientes son de estadística (s04-1 a s04-10, s05-10). Esto es una laguna importante en el curso. **Prioridad:** alta — la estadística es un tema fundamental y está completamente sin mejorar.

- **Duplicado s04-4-fracciones-equivalentes.html** (2026-06-13) — Este archivo es duplicado de s04-1-fracciones-equivalentes.html. **Solución:** eliminar o renombrar con propósito diferente.

- **Selección batch con rotación de niveles** (2026-06-10, MODO RÁPIDO) — En mejora batch (4-6 temas), la selección NO es solo "menor score primero". Hay que **rotar niveles obligatoriamente**: nunca mejorar 2 temas del mismo nivel seguidos. Alternar P → ESO → B → P → ESO → B. La fórmula de selección es: (nivel_rotado, priority ASC, improvement_count ASC, score_total ASC). Ver `references/rapid-batch-improvement.md` para el procedimiento completo.
- **Canvas de fracciones equivalentes** (2026-06-10) — Para temas de fracciones equivalentes en 3º-4º Primaria, el canvas de barras divididas es más efectivo que Plotly o texto. Dibujar barras con `num` partes coloreadas de `den` partes permite al alumno ver que 1/2 = 2/4 = misma área. Ver `references/canvas-fracciones-equivalentes.md`.
- **Quiz negativo — "¿Cuál NO es equivalente?"** (2026-06-10) — Para detectar errores conceptuales profundos, añadir ejercicios que pidan identificar la fracción que **NO** es equivalente. Esto fuerza al alumno a comprobar cada opción, no solo reconocer la correcta. Ejemplo: "¿Cuál NO es equivalente a 2/5? → 3/7 (3×5=15 ≠ 7×2=14)".
- **CSS grid para alineación decimal** (2026-06-10) — Para temas de sumar/restar decimales, un grid CSS con celdas individuales por dígito es más ligero y accesible que un canvas. La coma se colorea con `--naranja` para destacar. Ver `references/css-decimal-alignment-grid.md`.
- **Problema inverso con pista contextual** (2026-06-10) — Ejercicios donde se pide hallar un operando desconocido (minuendo, sustraendo, factor). La pista en el feedback debe explicar el PORQUÉ ("para hallar el minuendo, sumas"), no solo dar la respuesta. Ver `references/problema-inverso-pista-contextual.md`.
- **Verificación programática de variedad de ejercicios** (2026-06-10) — Antes de commitear, usar Python para contar tipos de ejercicio y verificar distribución. Patrón: leer HTML → split por `<div class="exercise">` → para cada bloque, extraer pregunta con regex `<p>\d+\.\s*(.*?)</p>` → clasificar tipo → contar con Counter. Regla: ningún tipo debe superar 50% del total, y debe haber ≥4 tipos diferentes. Ver referencia `references/exercise-type-verification.md`.
- **Patrón "completar suma repetida"** (2026-06-10) — Para temas de introducción a multiplicación, añadir ejercicios donde el alumno completa la suma repetida: `3 × 4 = __ + __ + __`. Esto conecta directamente el concepto de multiplicación con suma repetida, que ya saben. Se necesitan N inputs numéricos (uno por cada sumando). Función JS: leer N inputs, verificar que todos sean iguales al multiplicando. Ver referencia `references/complete-repeated-addition-pattern.md`.
- **Patrón "truco mnemotécnico"** (2026-06-10) — Caja pedagógica `box-teoria` con `🧠 Truco mnemotécnico` que da una analogía visual para recordar un concepto. Ejemplo: "La X echa brazos para llevar grupos". Diferente de `box-error` (error) y `box-idea` (conexión). Sirve para conceptos abstractos que necesitan un ancla visual. Ver referencia `references/mnemonic-trick-pattern.md`.
- **Patrón "caja de conexión"** (2026-06-10) — Caja pedagógica `box-idea` con `🔗 Conexión` que conecta el tema actual con algo que el alumno ya sabe. Ejemplo: "Ya sabes sumar repetido: 4+4+4=12. La multiplicación es lo mismo pero más rápido." Eleva el score `connections` de 0 a 1+. Ver referencia `references/connection-box-pattern.md`.
- **Ordenar fracciones con radio buttons** (2026-06-10) — Patrón para ordenar fracciones: radio buttons con `name="orderN"` y `value` indicando el orden correcto. checkOrderN() lee valores en orden de selección y compara con secuencia esperada. Ejemplo: 1/8 < 1/4 < 1/2 → values [1, 2, 3].
- **Canvas de fracciones equivalentes** (2026-06-10) — Para temas de fracciones equivalentes en 3º-4º Primaria, el canvas de barras divididas es más efectivo que Plotly o texto. Dibujar barras con `num` partes coloreadas de `den` partes permite al alumno ver que 1/2 = 2/4 = misma área. Ver `references/canvas-fracciones-equivalentes.md`.
- **Quiz negativo — "¿Cuál NO es equivalente?"** (2026-06-10) — Para detectar errores conceptuales profundos, añadir ejercicios que pidan identificar la fracción que **NO** es equivalente. Esto fuerza al alumno a comprobar cada opción, no solo reconocer la correcta. Ejemplo: "¿Cuál NO es equivalente a 2/5? → 3/7 (3×5=15 ≠ 7×2=14)".
- **CSS grid para alineación decimal** (2026-06-10) — Para temas de sumar/restar decimales, un grid CSS con celdas individuales por dígito es más ligero y accesible que un canvas. La coma se colorea con `--naranja` para destacar. Ver `references/css-decimal-alignment-grid.md`.
- **Problema inverso con pista contextual** (2026-06-10) — Ejercicios donde se pide hallar un operando desconocido (minuendo, sustraendo, factor). La pista en el feedback debe explicar el PORQUÉ ("para hallar el minuendo, sumas"), no solo dar la respuesta. Ver `references/problema-inverso-pista-contextual.md`.
