# Barrido de un backlog de 33 stars (2026-09-15) — receta con números reales

Caso: el cron de stars llevaba 6 días sin correr (PC apagado) → 33 repos nuevos acumulados.
El usuario pidió "ponte las pilas con las nuevas stars". Resultado: 11 skills nuevos + 11 upgrades + 5 referencias + 6 skips, en una sesión.

## Contexto de partida

| Dato | Valor |
|---|---|
| Stars vivas de Ntizar (paginado `/starred`) | 380 |
| Entradas en `data/stars-registry.json` | 352 |
| Backlog detectado (380 − 352) | **33** |
| Skills existentes (ChromaDB sincronizada) | 467 (478 al final) |

Prompt diagnóstico clave: **restar el estado persistente de la fuente real** — el `--status` del script puede decir `all_done` con backlog pendiente.

## Secuencia ejecutada

1. `git pull --rebase` + `sincronizar-skills.py` + `indexar-skills.py` **antes** del dedup (si ChromaDB va desfasado, el dedup miente).
2. Clasificación: 1 `GET /repos/{owner}/{repo}` por repo → stars, lenguaje, `pushed_at`, `archived`, topics, descripción → JSON en `%TEMP%` (33 peticiones, ~1 min).
3. Dedup semántico por lote: script temporal que invoca `consultar-skills.py "<descripción>" --json` por repo y guarda el top-3 (`name`/`score`/`path`). **`--json` devuelve lista plana**, no dict.
4. `hermes cron pause` del scout (evita push cruzado durante el barrido).
5. 3 subagentes × 11 repos vía `delegate_task` con `output_schema` + dedup ya calculado en el `context` + orden de leer el README real (`gh api .../readme --jq .content | base64 -d`).
6. Orquestador: 11 `skill_manage(create)`, 11 patches de comparativa en skills existentes, registro de las 33 decisiones en el registry (CRLF + `indent=2` preservados), nota en `notes/`, `sincronizar-skills.py`, `indexar-skills.py`, commit + `git pull --rebase` + push.
7. `hermes cron resume` del scout.

## Reparto de veredictos

- 15 `CREATE` propuestos por los hijos → **11 creados**; 4 degradados a `REFERENCE` (repos de 3-17 ⭐, colecciones de ejemplos, toolkits sin comunidad).
- 11 `UPGRADE` (sección "Comparativa de alternativas" añadida al skill existente, en vez de skill nuevo).
- 6 `SKIP` (awesome-lists, compilador de un lenguaje, librería ya cubierta con dedup 0.815).

## Falsos positivos del dedup (por eso el README manda)

| Repo | Score vs skill vecino | Realidad |
|---|---|---|
| `localai-org/sam3d.cpp` | 0.747 vs `trellis2-img-to-3d` | Imagen→3D vs recuperación de cuerpo/objetos desde vídeo: **nada que ver** |
| `debpalash/VoiceStudio` | 0.837 vs `media/voicebox` | Mismo nicho TTS local → upgrade, no skill nuevo |
| `acrosa/GridKit` | 0.612 vs `business-model-canvas` | Overlay de retícula de diseño: **ruido temático** |

## Coste / tiempos medidos

- 3 subagentes en paralelo: **~3,5 min** (17, 13 y 12 llamadas API respectivamente).
- Indexado final: 23 skills (11 nuevos + 12 modificados) en un par de minutos.
- Total de la sesión (diagnóstico de crons + barrido + commit): ~1 h.
