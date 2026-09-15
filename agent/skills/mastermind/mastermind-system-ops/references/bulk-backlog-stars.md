# Barrido de un backlog grande de stars (flujo verificado 2026-09-15, 33 repos)

El pipeline canónico de stars vive en el skill `stars-explorer` (para mejorarlo,
`skill_manage(action='patch')` sobre él y sincronizar al repo). Aquí va el flujo de
EMERGENCIA para cuando el cron ha estado parado días y el backlog no se absorbe con
`--batch 3` (33 repos = 11 noches). Ejecutado en sesión, con evidencia real.

## Cuándo

El scout (`bc390c1bf06a`, cada 6h) no corre desde hace días — típicamente por un apagón del
PC con catch-up fallido (ver `references/cron-catchup-429.md`). Señal: `run-stars-explorer.sh
--status` muestra `Last run:` con fecha vieja y el cross-check de `/starred` da decenas de
repos no registrados.

## Fases

1. **Detectar los nuevos** — paginar las stars vivas y restar el registry:

   ```python
   # GET /users/Ntizar/starred?per_page=100&page=N con gh auth token
   known = set(reg["processed"]) | {k for k, v in reg.items()
                                    if isinstance(v, dict) and "category" in v}
   nuevos = [s for s in stars if s not in known]
   ```

   Verificado: 380 stars vivas vs 352 entradas → **33 nuevas**. Revisar también entradas
   `category: "pending"` huérfanas de runs anteriores.

2. **Clasificar con 1 req/repo** — `GET /repos/{owner}/{repo}` → `stars`, `language`,
   `pushed_at`, `archived`, `topics`, `description`. Volcar a JSON en `%TEMP%` (nunca
   escribir el registry todavía) y ordenar por stars. Da la lista para repartir en subagentes.

3. **Sincronizar + indexar ANTES del dedup** — `sincronizar-skills.py` y
   `indexar-skills.py`. Si ChromaDB va desfasado, el dedup miente (en esta sesión: 4 skills
   desincronizados, corregidos antes de consultar).

4. **Dedup semántico en lote** — script temporal que invoca
   `consultar-skills.py "<descripción del repo>" --json` por repo y guarda los 3 top
   (`name`, `score`, `path`). OJO: `--json` es una **lista plana**, no un dict. Los scores
   orientan (≥0.8 = probablemente cubierto; 0.4-0.6 = ruido temático).

5. **Pausar el scout** mientras dura el barrido (`hermes cron pause bc390c1bf06a`) para no
   colisionar en el push del repo; reanudarlo al terminar.

6. **Analizar con ≤4 subagentes** (NaN limita a 5 peticiones LLM simultáneas; 3 fue el
   número usado con éxito). Cada subagente recibe:
   - su lista explícita de ~11 repos,
   - los **scores de dedup ya calculados** (ahorra que investiguen desde cero),
   - la orden de leer el README REAL (`gh api repos/{o}/{r}/readme --jq .content | base64 -d`
     o `raw.githubusercontent.com/{o}/{r}/HEAD/README.md`),
   - criterios `CREATE / SKIP / UPGRADE / REFERENCE`,
   - `output_schema` que fuerce el JSON,
   - la prohibición de tocar skills (los subagentes investigan; el orquestador aplica).

7. **Aplicar veredictos en el orquestador** — `skill_manage(create/patch)` + marcar el
   registry (`category`, `skill_created`, `explored_at`; CRLF + `indent=2`, ver el pitfall
   del registry en `stars-explorer`) + `indexar-skills.py` + commit/push con
   `git pull --rebase`.

## Pitfalls nuevos

- **`delegate_task` rechaza `<>` en el `goal`**: aborta con `Task N goal contains an
  unexpanded template marker ('<path del skill si UPGRADE>')`. El JSON de ejemplo incrustado
  en el goal para fijar el formato cuenta como placeholder → escribir el goal (y la
  plantilla) sin ángulos: `owner/repo`, `path del skill si UPGRADE`. El `context` no tiene
  esa restricción.
- **`hermes cron run <job_id>` por CLI se queda esperando** la ejecución (timeout del
  terminal a los 60s, sin encolar nada visible). Para forzar un run inmediato: tool
  `cronjob(action='run', job_id=...)` (background). `hermes cron runs <job_id>` es solo
  para leer el historial.
- **Distinguir el veredicto del `dedup` con el skill real**: un score alto no decide solo;
  hay que leer el SKILL.md del skill vecino (`%LOCALAPPDATA%\hermes\skills\<path>\SKILL.md`)
  y comparar alcance. Ejemplos de esta sesión: `VoiceStudio` 0.837 vs `voicebox` (mismo
  nicho TTS local → SKIP/UPGRADE, no skill nuevo), `carla` 0.737 vs `airsim-simulation`
  (mismo nicho simulador → comparar, no duplicar), `gtfs-lib` 0.815 vs `node-gtfs` (cubierto).
