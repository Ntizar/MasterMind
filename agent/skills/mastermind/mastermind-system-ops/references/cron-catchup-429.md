# Incidente: avalancha de catch-up tras 6 días apagado (2026-09-15)

## Qué pasó

El PC de David estuvo apagado del **2026-09-09 17:42** al **2026-09-15 16:30**. Al arrancar el
gateway, el scheduler detectó **13 jobs vencidos** y los lanzó todos en el mismo tick
(16:34–16:35), sin límite de paralelismo.

Resultado: 9 jobs LLM `error` con el MISMO mensaje, y 4 jobs `no_agent` (script) `ok`.

```
RuntimeError: HTTP 429: Rate limit exceeded for api_key: ***.
Limit type: max_parallel_requests. Current limit: 5, Remaining: 0.
Limit resets at: 2026-09-15 14:35:5x UTC
```

## Víctimas (9)

| job_id | nombre | modelo | entrega |
|---|---|---|---|
| bc390c1bf06a | mastermind-scout | qwen3.8-flash | local |
| d8e9eb7ce270 | mastermind-weekly-digest | qwen3.8-flash | local |
| cceb83c1026c | mastermind-doctor | qwen3.8-flash | local |
| 7f86939758e2 | Gobierno IA — Pase de lista matinal | qwen3.6 | origin |
| d8c606f0f8da | Gobierno IA — Consejo de Ministros | qwen3.6 | origin |
| 7fba6b3bdf69 | Gobierno IA — Informe presidencial | qwen3.6 | origin |
| 107b96a17053 | Gobierno IA — Auditoría del Estado | qwen3.6 | origin |
| e518c0973b6a | kit72h-vigilante | qwen3.8-flash | telegram |
| 0f0a44af121e | Gobierno IA — Café informal | qwen3.6 | origin |

`no_agent` que pasaron (script puro, sin LLM): `vigia-cron`, `kit72h-buscador`,
`kit72h-editor`, `skills-usage-report`.

## Evidencia

```bash
# 1) jobs con estado no-ok (el status NO trae el detalle)
python - <<'PY'   # en la práctica: script temporal en %TEMP% + python <ruta>
import json, os
d = json.load(open(os.path.join(os.environ["LOCALAPPDATA"], "hermes", "cron", "jobs.json"), encoding="utf-8"))
jobs = d if isinstance(d, list) else d.get("jobs", d)
for j in jobs:
    if not str(j.get("last_status") or "").lower().startswith("ok"):
        print(j["id"], j["name"], j.get("last_run_at"), j.get("last_status"))
PY

# 2) error REAL de cada run
grep -A4 '## Error' "%LOCALAPPDATA%/hermes/cron/output/<job_id>/*.md" | tail -8

# 3) confirmar la avalancha
grep 'missed its scheduled time' "$LOCALAPPDATA/hermes/logs/agent.log" | tail -15
```

Las líneas de (3) dan la hora original perdida de cada job y su re-anclaje
(`grace=7200s`, `next run provisionally set to ... (re-anchored on completion)`).

## Fix aplicado

```bash
hermes config set cron.max_parallel_jobs 1     # antes: unbounded (default)
```

Verificación de que la clave es real: `hermes-agent/cron/scheduler.py`, junto a
`max parallel workers`:

```python
# Resolve max parallel workers: env var > config.yaml > unbounded.
# Set HERMES_CRON_MAX_PARALLEL=1 to restore old serial behaviour.
_ucfg.get("cron", {}).get("max_parallel_jobs")
```

## Decisión de relanzamiento (no relanzar todo a lo loco)

- **Sí relanzar** (informes idempotentes o de proyecto activo): doctor, digest semanal,
  scout de stars (o hacer el backlog a mano), vigilante del proyecto vivo.
- **NO relanzar** los jobs de contenido seriado diario (Gobierno IA: pase de lista, café,
  consejo, auditoría, informe presidencial): duplicaría sesiones del serial 30 sesiones;
  reanudan solos en su siguiente hora (el Consejo lo hace el mismo día a las 22:00).
- Nunca lanzar varios a mano a la vez: es la misma avalancha que causó el 429.

## Contexto asociado

El mismo día, 33 repos nuevos acumulados en las stars de David (registry parado desde el
2026-09-09) porque el `mastermind-scout` no había corrido. Ver el flujo bulk en el skill
`stars-explorer` (`consultar-skills.py --json` devuelve **lista**, 3 subagentes por oleada,
pausar el scout mientras se hace el bulk).
