# Test definitivo: ¿los skills son útiles o slop?

**Fecha:** 2026-08-29 · Método: retro-análisis con session_search (10 sesiones muestreadas,
10 queries de discovery, role_filter='tool') + test de cobertura semántica con 20 consultas.

## Resultado del retro-análisis

**6 de 10 sesiones recientes de trabajo con evidencia clara de uso de skill** (las otras:
sesión trivial de 2 mensajes, cron doctor, y una no verificable al detalle). Ejemplos
con influencia literal en el resultado (informe completo del subagente en cache/delegation):

1. Visor accidentes ERA (@session:default/20260828_110757_bc91dd) — `pdf-processing` +
   `government-data-pipelines`; el ANALISIS.md del proyecto cita las lecciones del skill.
2. Rediseño Mastermind (@session:default/20260828_194329_98d419) — `aurora-design-system`;
   el resultado consume Aurora v6 vía CDN con clases .nz exclusivamente.
3. Auditoría Gentle-AI (@session:default/20260828_184227_abbe98) — CHEATSHEET de Aurora
   descargado y verificado ("no inventar ninguna clase").
4. Fixes de Telegram/Hermes (2 sesiones) — `hermes-agent` con references/troubleshooting.
5. Demo Aluche 10x (@session:default/20260828_102236_b3c6c1) — `prospeccion-demos-locales`.
6. Sombras ShadeMap (@session:default/20260828_104447_50b841) — cargó los skills de sombras
   para NO duplicar y creó `shademap-competidor-madrid` + reindexado.

**Skills más usados:** hermes-agent (≥4), aurora-design-system (≥3), mastermind-system-ops,
government-data-pipelines, pdf-processing, prospeccion-demos-locales.

## Cobertura semántica (data/queries-test.json)

Primer run: **70% (14/20)** → el test cazó un bug sistémico: **88 skills que Hermes carga
a diario no existían en el repo** (la sincronización instalación→repo estaba rota) y el
conteo 314=314 del doctor enmascaraba contenido divergente. Tras `sincronizar-skills.py`
+ reindexado (402=402): **100% (20/20)**.

## Hallazgos negativos (los importantes)

- **La búsqueda semántica ChromaDB casi no se usa en sesiones interactivas** — Hermes carga
  skills por su sistema nativo (skill_view). El script `consultar-skills.py` opera en el
  ciclo autónomo (dedup del scout) y en la migración. La promesa "se consultan por
  significado" se cumple en el loop autónomo, no en el flujo interactivo.
- El doctor comparaba conteos, no contenido: un índice completo pero con los ficheros
  equivocados daba verde. El test de cobertura cubre ese hueco.

## Veredicto

Los skills NO son decoración: en tareas de dominio se cargan al inicio y sus
comandos/patrones se ejecutan literalmente. La capa semántica ChromaDB es el motor del
scout y del dedup, no del chat interactivo — y eso está bien, pero conviene saberlo.
