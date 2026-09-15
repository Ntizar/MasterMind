---
name: bulk-triage-fanout
description: "Triaje masivo con subagentes: lotes, veredictos y filtro."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [subagentes, delegate_task, triaje, lotes, veredictos, paralelismo, nan]
    related_skills: [mastermind-orchestration, stars-explorer, agent-skill-audit]
---

# Triaje masivo con fan-out de subagentes

Patrón para clasificar **N items independientes** (repos, ficheros, documentos, issues, datasets) con subagentes en paralelo, donde cada item produce un **veredicto** y el orquestador aplica las decisiones.

## When to Use (cuándo usarlo)

- Hay un conjunto grande (30-200 items) que necesita **juicio individual** (CREATE/SKIP/REFERENCE, aprobar/rechazar, migrar/no migrar).
- Los items son **independientes** (no comparten estado) → paralelizan sin riesgo de conflictos.
- El trabajo es **leer + decidir**, no escribir: los hijos investigan, el orquestador escribe.
- Ejemplo real: barrido de un backlog de stars de GitHub (33 repos → 11 skills nuevos).

## Fases

1. **Detecta el conjunto** con una consulta determinista y **resta lo ya hecho** (registry/estado persistente). Si el estado local dice 352 y la fuente real dice 380, hay 33 items nuevos — nunca deduzcas el backlog de memoria.
2. **Enriquece en 1 petición por item** (metadatos: stars, lenguaje, fecha, descripción) y **ordena por importancia**. Volcar a JSON en `%TEMP%`: todavía NO tocar el estado persistente.
3. **Pre-calcula el dedup/overlap y pásalo en el `context`** (top-3 con `name`, `score`, `path` por item). Ahorra que cada hijo recorra el catálogo desde cero y centra su juicio en la fuente real.
4. **Reparte en ≤3 subagentes** (ver "Por qué 3") con `output_schema` que fuerce JSON y la **prohibición explícita de escribir** (los leaf no pueden `skill_manage`).
5. **El orquestador aplica los veredictos** uno a uno, con **filtro de calidad**: los hijos son generosos por diseño. Registra cada decisión en el estado persistente + nota + commit.
6. **Verifica el conteo**: re-lee el estado persistente y cuadra el número de items procesados con el detectado. "Todos" significa todos, no una mayoría plausible.

## Reglas verificadas

- **Por qué 3 subagentes:** el límite real es la API (NaN: **5 peticiones LLM simultáneas** por api_key; superarlo → `HTTP 429 max_parallel_requests`), y hay que descontar las sesiones propias del gateway/crons. 3 hijos × 11 items ≈ 3,5 min y 0 errores con 33 items.
- **Exige la fuente real en el `context`:** "lee el README REAL (`gh api repos/OWNER/REPO/readme --jq .content | base64 -d`), no la descripción de la plataforma". Un score de similitud alto puede ser un falso positivo total (caso real: 0.747 entre dos repos sin relación). **El dedup orienta, no decide.**
- **`output_schema` obligatorio** con un array de veredictos y un campo de justificación: sin esquema, los hijos devuelven prosa y el parseo se rompe.
- **Filtro del orquestador:** de 15 `CREATE` propuestos, 11 se materializaron y 4 bajaron a referencia (repos de 3-17 ⭐ o colecciones de ejemplos). Regla práctica: item ≥300 ⭐ con patrón claro → adelante; <50 ⭐ o mera lista → referencia.
- **Pausa lo que pueda colisionar** durante el barrido (p.ej. un cron que hace push al mismo repo) y reanúdalo al terminar.
- **Persistencia:** el estado va con el MISMO formato que ya tenía (EOL incluido) para no generar diffs de cientos de líneas; ver `stars-explorer` para las reglas del registry.

## Pitfalls

- **`delegate_task` rechaza `<>` en el `goal`.** Un JSON de plantilla incrustado aborta con `Task N goal contains an unexpanded template marker (...)`. Escribe goal y plantilla sin ángulos (`owner/repo`, `path del skill si UPGRADE`); el `context` no tiene esa restricción.
- **Los resúmenes de los hijos vuelven truncados** al padre (head+tail + ruta del fichero completo). Guarda el JSON de cada hijo en disco y **parséalo con Python**, en vez de razonar sobre el texto truncado del mensaje.
- **Un hijo puede extralimitarse** y escribir ficheros que le prohibiste: revisa `git status` antes de commitear y decide conscientemente si ese contenido se queda.
- **No confundir "el hijo terminó" con "el trabajo está hecho":** el resultado del hijo es un auto-informe; el entregable lo aplica y lo verifica el orquestador.

## Nota de propiedad (MasterMind)

Los umbrellas de este sistema (`stars-explorer`, `mastermind-system-ops`, `mastermind-orchestration`) son **user-owned**: las escrituras autónomas del curador se rechazan con `not curator-managed`. Si hay que corregirlos, pedir al usuario `hermes curator adopt <skill>` (o hacerlo en sesión con el usuario delante — con él presente el patch sí pasa).

## Referencias

- Detalle de un barrido real (33 repos de stars, 2026-09-15): `references/barrido-stars-2026-09-15.md`
- Pipeline de stars del sistema: skill `stars-explorer` · Ops del sistema: `mastermind-system-ops`
