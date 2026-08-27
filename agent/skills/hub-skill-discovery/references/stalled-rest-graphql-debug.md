# rest-graphql-debug — Skill atascado

## Qué es
Debug REST/GraphQL APIs. Flujo en capas: conectividad → timeouts → TLS → auth → formato → parseo → semántica. Autor: eren-karakus0, MIT.

## Estado
Atascado en índice 4 desde 2026-06-06. 4 intentos fallidos consecutivos (timeout 120s cada uno).
Skill en `.hub/quarantine/rest-graphql-debug/SKILL.md`.

## Causa probable
`hermes skills install official/web/rest-graphql-debug` tarda más de 120s. El script timeout antes de ejecutar `save_state`, por lo que el `current_index` no avanza.

## Fix manual
Editar `agent/skills/.skill-learning-state.json`:
- `current_index`: 5
- `skipped`: ["rest-graphql-debug"]

O mover manualmente el skill desde quarantine a su destino.
