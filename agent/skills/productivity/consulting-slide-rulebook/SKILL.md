---
name: consulting-slide-rulebook
description: "Usa a crear decks de consultora con rulebook de arquetipos."
version: "2.1.0"
tags: [consulting, slides, decks, presentaciones, arquetipos, pptx, skill]
related_skills: [ppt-master, powerpoint, html-to-pdf-report-pipeline]
author: Mastermind (scout stars-explorer)
license: MIT
metadata:
  hermes:
    tags: [consulting, slides, pptx]
    related_skills: [ppt-master, powerpoint]
---

# Consulting Slide Rulebook — decks de calidad consultora (McKinsey/BCG)

> Fuente: `carnot-tech/consulting-pptx-skill` (~250⭐, JavaScript, MIT, activo). Renombrado desde `gozen3ji/consulting-pptx-skill` (mismo repo, verificado por redirect de GitHub el 2026-09-07). Claude Code skill; el 100% de sus patrones son agnósticos de agente.

## When to Use

- Crear **decks de presentación de calidad consultora**: conclusiones en títulos, narrativa izquierda→derecha, tablas con ejes, cero decorativismo.
- Generar **PPTX nativo editable** desde una especificación JSON (SlideSpec) con preview HTML y QA automático.
- Auditar/mejorar decks ajenos con un rulebook mecanizable.

## Qué es (núcleo del repo)

Tres capas, en orden de importancia:

1. **`references/slide-rules.md` — EL ACTIVO REAL (~110 reglas)**: observaciones de reviews reales en 1 línea cada una. Ejemplos clave:
   - Conclusión en el título (1 línea; si no cabe, 2 líneas agrandando — NUNCA reduciendo fuente). Sin "de/masu" (体言止め). Leer solo los títulos en secuencia debe dar la historia completa.
   - Layout: 1 slide = 1 mensaje; **izquierda = hechos/diagramas, derecha = implicaciones** (nunca arriba/abajo). Prohibida la banda "POINT" inferior.
   - Tablas: fila=elemento, columna=ángulo ("tabla con ejes", no tarjetas). Columnas que no aportan a la tesis, fuera.
   - Decoración: **prohibidos los bordes redondeados**; sin borde en cajas con relleno; leyenda obligatoria si hay color.
   - "3 factores de IA-parecido": cajas flotantes / explicación redundante sin bullets / frases cortadas sin sujeto-verbo.
   - Charts: primero clasificar en 4 formas básicas (tabla / premisa-izq-der / contraste / análisis+comentario); lo creativo sobra en un chart.
2. **Catálogo de 62 arquetipos** (`assets/SlideCatalog_16x9.pdf`, `assets/SuperTemplate_62type.pptx` — 70 slides todas editables nativas; 63 definiciones SlideSpec = 36 tipos + 27 piezas de descripción libre). El catálogo es *bloc de notas de layouts*, **no** una camisa de fuerza: se elige el tipo según la narrativa y si no encaja, se tira y se compone libre.
3. **Pipeline de generación** (`pipeline/`): SlideSpec JSON → HTML preview → QA → PPTX editable (pptxgenjs) → check mecánico.

## Uso — flujo real verificado (contra package.json y SKILL.md del repo, 2026-09-07)

**Pasos comunes:**
1. *Definir antes de producir* (3-5 líneas): objetivo, entregable, alcance IN/OUT.
2. *Storyline*: 1 título por slide + "cómo mostrarlo" (diagrama / tabla / flecha / 2 columnas / stat-card). Lo que sea tendencia/composición/distribución → **gráfico, dibujado a mano, no volcado en pieza de plantilla**.

**Carril A — descripción libre (el principal, para entregables):**
- Copiar `templates/freeform_parts_16x9.html` (10 piezas: portada, overview map, tablas con eje, premisa→conclusión 2 col, stat…) y sustituir secciones.
- `python3 scripts/check_deck.py mi_deck.html` → 0 FAIL (WARN de portada permitida).
- `node scripts/check_layout.mjs mi_deck.html` → 0 FAIL en solapes/desbordes con render real (requiere playwright).
- *Fresh-eye review*: pasar `references/content-review-prompt.md` a **otro agente SIN contexto de cómo se hizo** que lea el deck crudo (HTML/PDF/PPTX, sin imagen); sus hallazgos → tabla aceptar/rechazar/pendiente con motivo → corregir solo lo aceptado y repetir check.
- PDF final y revisar todas las páginas: `chrome --headless --print-to-pdf=deck.pdf deck.html`.

**Carril B — pipeline SlideSpec (borradores en segundos / informes repetibles):**
```bash
cd pipeline && npm run setup        # 1 vez: pptxgenjs ^4.0.1 + playwright ^1.60 + chromium
node scripts/validate_spec.mjs slide-spec/mi_deck.json
node scripts/render_spec_to_html.mjs slide-spec/mi_deck.json generated/mi_deck.html
node scripts/qa_html_deck.mjs generated/mi_deck.html
node scripts/export_spec_to_editable_pptx.mjs slide-spec/mi_deck.json generated/mi_deck.pptx
python3 scripts/check_deck.py generated/mi_deck.pptx   # 0 FAIL (check PPTX requiere python-pptx)
```
- Título ≥12 caracteres en afirmación; `source` obligatorio; cero placeholders (Text N); en deck no-japonés traducir headers de `comparison_table`/`scenario_table`/`risk_table`/`cause_effect` vía `"headers": {...}` (claves en `pipeline/slide-spec/schema.json`).
- Los 28 arquetipos `.mjs` en `pipeline/scripts/archetypes/` son el generador por tipo (`_ids.json` lista el registro completo).

**Bucle de calidad (la fuente del valor):** los ajustes manuales de cada deck generan nuevas líneas en `slide-rules.md` — el rulebook se cultiva; catálogo y pipeline solo compran iteraciones rápidas.

## Pitfalls

- **No confundir versión v1 de este skill**: las cifras buenas son 62 arquetipos / ~110 reglas (no 38/~80; el propio SKILL.md del repo aún dice ~80 — el README manda, colas §4.37-4.48 y §7 añaden hasta ~110).
- Repo transferido: cualquier enlace antiguo a `gozen3ji/*` redirige a `carnot-tech/*`.
- `check_deck.py`: HTML con stdlib; PPTX exige `pip install python-pptx`.
- `check_layout.mjs` necesita chromium instalado (`npx playwright install chromium`).
- El pipeline solo rellena slots del tipo: si una slide no encaja en su molde, NO forzar — salir al carril A para esa slide.
- Para adaptar sin el repo: lo portable es el rulebook (reglas de títulos/lectura/tablas/charts) — funciona igual con python-pptx o HTML propio.

## Verificación

- Deck de prueba de 3-4 slides: título de cada slide legible como historia en secuencia, 0 FAIL en `check_deck.py`, fresh-eye review con tabla de acepta/rechaza.

## Registro (scout stars-explorer)

- 2026-09-03: primera creación (v1 imprecisa) desde `gozen3ji/consulting-pptx-skill` (103⭐ de la época).
- 2026-09-05: auditoría → v2.0.0 (cifras corregidas).
- 2026-09-07: re-encuentro del repo como `carnot-tech/consulting-pptx-skill` (250⭐, push mismo día) → **v2.1.0**: comandos verificados contra `pipeline/package.json` y `SKILL.md` reales, estructura de 2 carriles, fresh-eye review documentado.
