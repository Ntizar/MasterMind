# Scout stars — batch 2026-09-07

Batch de 2 repos pendientes (quedan 0 tras este run).

## carnot-tech/consulting-pptx-skill (250⭐, JavaScript, MIT) → UPGRADE

- El repo es el mismo `gozen3ji/consulting-pptx-skill` que ya procesamos el 2026-09-03: **transferido/renombrado a carnot-tech**. `gh api repos/gozen3ji/...` responde con `carnot-tech/...` → el dedup por nombre no lo pilló; el dedup ChromaDB sí (0.84 vs `productivity/consulting-slide-rulebook`).
- Verificado contra el repo real (`pipeline/package.json`, `SKILL.md`, tree): 2 carriles (A: descripción libre con `templates/freeform_parts_16x9.html` — el principal; B: pipeline SlideSpec→HTML→QA→PPTX editable), checkers `check_deck.py` + `check_layout.mjs` (playwright), fresh-eye review con prompt de third-party (`references/content-review-prompt.md`), 28 generadores de arquetipo `.mjs` de los 62 del catálogo.
- **consulting-slide-rulebook → v2.1.0** reescrito con comandos y estructura reales + lecciones del propio skill (el valor es el rulebook de ~110 reglas, el pipeline solo compra iteraciones).
- Registry: `category: upgrade`, `skill_version: 2.1.0`.

## jtydhr88/screenwriting-skills (133⭐, sin código) → SKIP

- 12 skills Claude en markdown sobre dramaturgia y guion cinematográfico (19 libros, Chejov, Ozu), cuerpo en chino.
- Sin patrones técnicos reutilizables, fuera del stack de David (GIS/transporte/dashboards/CV/ML). Registry: `category: skip`.

## Nuevo pitfall en el skill stars-explorer

- Repos renombrados evaden el dedup por nombre → dedup semántico obligatorio antes de crear.

## Estado del pipeline

- Registry: 349 entradas procesadas, 0 pendientes tras este batch. El cron nocturno solo tendrá trabajo cuando David dé nuevas stars.
