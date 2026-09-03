---
name: consulting-slide-rulebook
version: "1.0.0"
description: "Use al crear decks de slides con IA de calidad consultora."
tags: [pptx, presentaciones, slides, consulting, rulebook, validador, calidad]
---

# Consulting Slide Rulebook — Slides de consejo con IA

> Patrón destilado de `gozen3ji/consulting-pptx-skill` (103⭐, MIT, 2026-09-02).

## Qué es (repo de origen)

Skill de Claude Code para generar decks "de sala de juntas": catálogo de **38 arquetipos**
de slide consultora, formato **SlideSpec JSON**, pipeline de render (preview HTML →
PPTX nativamente editable), **rulebook de ~80 normas de diseño** y **checker automático**.

**Lo valioso no son los templates: es `references/slide-rules.md`** — ~80 normas destiladas
de revisiones reales de propuestas ("la conclusión va en el título", "prohibido redondear
esquinas", "sin borde sobre cajas rellenas", "un término por deck").

## El patrón reutilizable (lo que hay que aplicar)

1. **No hagas que la IA dibuje layouts.** Los layouts (posiciones, márgenes, tamaños de
   fuente, reglas de trazado) van *horneados* en el renderer como valores medidos. La IA
   solo escribe el contenido: afirmación, números, etiquetas. → Menos variabilidad, más velocidad.
2. **Reglas en archivo + lectura obligatoria antes de generar.** La IA olvida entre
   sesiones: avisarla de palabra no fija nada. El ÚNICO método es un fichero de reglas
   que se le hace leer cada vez (`slide-rules.md` → pasar como contexto/preámbulo).
3. **Validación mecánica después.** `scripts/check_deck.py` detecta violaciones del
   rulebook automáticamente. Un slide deck sin checker = reglas decorativas.
4. **Bucle de acumulación.** El ajuste fino POST-generación es donde está la calidad
   (partir tablas en dos, reescribir el título como cadena narrativa). Cada corrección
   recibida se añade como 1 línea al rulebook. El template+pipeline solo sirve para
   "sacar borrador en segundos y multiplicar las iteraciones de ajuste".

## Cómo aplicarlo Mastermind (sin usar el repo tal cual)

Para cualquier generación de slides/decks/PDF de informe (David: presentaciones internas
Ineco, demos de cliente, informes):

```
1. Crear/actualizar rulebook propio: Normas-Slides.md (~20-80 normas, 1 línea c/u,
   en español, formato "regla → por qué → ejemplo malo/bueno")
2. Antes de generar: inyectar el rulebook completo en el prompt del generador
3. Generar en DOS fases:
   a. Spec JSON por slide (plantilla + claim + datos) — NUNCA coordenadas/libre
   b. Render a partir de spec con layouts fijos por arquetipo
4. Validar: script que revise reglas mecánicas (longitud de títulos, 1 término único,
   esquinas redondeadas, relleno+borde, cifras vs fuente)
5. Correcciones del usuario → append de 1 línea al rulebook (git commit del rulebook)
```

Reglas de oro heredadas del rulebook original (válidas para decks de David también):
- La afirmación (so-what) va EN el título del slide, no "Análisis de X"
- Un solo vocablo por concepto en todo el deck (no mezclar "ingresos/facturación/ventas")
- Prohibido: cajas con relleno Y borde, esquinas redondeadas, decoraciones sin mensaje
- Leer solo los títulos seguidos debe contar la historia completa (test de lectura corrida)

## Componentes del repo (si se quiere usar directo)

- `references/slide-rules.md` — rulebook ~80 items (en japonés: traducir/destilar al español)
- 38 arquetipos con layout medido (waterfall, bridge, matriz 2×2, etc.)
- SlideSpec JSON por slide: `{"template":"waterfall","kicker":"07｜...","title":"<afirmación>","chart":{...}}`
- Pipeline: preview HTML → PPTX editable (renderers `.mjs` con node, checker `scripts/check_deck.py`)

## Pitfalls

- Repo NUEVÍSIMO (2026-09-02) y japonés: no depender de él como librería — usar el
  PATRÓN. El rulebook en japonés hay que traducirlo la primera vez que se aplique.
- No confundir con `productivity/powerpoint` (mecánica python-pptx: cómo escribir el
  .pptx) ni `ppt-master` (herramienta genérica) — este skill es METODOLOGÍA de calidad
  (qué hace bueno a un slide y cómo hacer que la IA lo cumpla consistentemente).
- La trampa clásica: dejar que el LLM "diseñe" posiciones → resultados irregulares.
  El layout SIEMPRE determinista en el renderer.
- El check mecánico solo cubre reglas formalizables; el juicio (¿es este el mensaje
  correcto?) sigue siendo del bucle humano.

## Verificación

Al entregar un deck generado:
1. ¿Cada título es una afirmación con número o consecuencia?
2. ¿Se pasó el checker y salió limpio (o con excepciones justificadas)?
3. ¿Vocabulario único por concepto en todo el deck?
4. ¿Cada corrección del usuario quedó añadida como 1 línea al rulebook versionado?

## Referencias

- Repo: https://github.com/gozen3ji/consulting-pptx-skill (103⭐, MIT)
- Explorado por stars-explorer: 2026-09-03
- Relacionados: `productivity/powerpoint`, `ppt-master`, `devops/html-to-pdf-report-pipeline`
