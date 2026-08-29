# Auditoría: javierpa95/harness vs Mastermind

**Fecha:** 2026-08-29
**Repo auditado:** https://github.com/javierpa95/harness (16★, MIT, template SDD para Claude Code + OpenCode)

## Qué es

Template de proyecto (no agente): `make init` monta 8 agentes SDD donde el
arquitecto fuerza el flujo Analizar → Spec → Implementar → Review → Docs → Decidir.
Su joya: extensión `.pi/` con máquina de estados en TypeScript (~1.100 líneas con
tests) que hace gating programático del flujo — no confía en el prompt, fuerza el
proceso en código.

## Comparativa (resumen)

| harness gana | Mastermind gana |
|---|---|
| Gates de proceso forzados por código | Cobertura de dominios (skills semánticos) |
| Doctor con tests de bug-inyección | Autonomía (crons: scout, digest, doctor) |
| Memoria por rol comiteada | Memoria global más rica |
| Onboarding numerado (7 docs) | Higiene interna (su doctor habría cazado sus bugs) |
| ATTRIBUTION.md radical | Escala viva vs template rígido |

## Lo importado (sesión 2026-08-29)

1. **`scripts/test-doctor.py`** — patrón bug-inyección: inyectar cada bug real en
   sandboxes aislados (`%TEMP%/mastermind-test-doctor/`) → doctor.py DEBE detectarlo.
   9/9 casos. Requirió hacer doctor.py testable (overrides `MM_DOCTOR_*`).
2. **Memoria por especialista** — formalizada en `mastermind/memoria-especialistas.md`
   + plantilla `agent/skills/mastermind/templates/estado-especialista.md`. Los skills
   con estado usan `references/estado-<tema>.md` comiteada (ya operaban así de facto).
3. **Onboarding numerado** — `mastermind/onboarding/` (01-06), inspirado en sus
   `docs/onboarding/`.

## Lo descartado y por qué

- Flujo SDD con gates: para equipos sobre código; Mastermind ya tiene human-loop-control.
- TUI/make/init/permisos granulares: resuelven problemas de CLI que Hermes resuelve nativo.
- ATTRIBUTION.md agregado: mucho ruido para tantos skills (decisión de David).
- Design systems de referencia: Aurora v6 es superior para este caso.

## Higiene de harness (lecciones sin integrar)

- 3 agentes architect duplicados; fechas contradictorias en docs.
- Typos ("hissho") en ATTRIBUTION.md — ironía en un doc de transparencia.
- Reconocen en su propio backlog el gap: agentes con bash pueden leer .env aunque
  `read` lo deniegue.
