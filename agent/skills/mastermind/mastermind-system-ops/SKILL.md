---
name: mastermind-system-ops
description: "Usar al operar Mastermind en Windows: repo, ChromaDB, crons."
version: "1.0.0"
tags: [mastermind, sistema, chromadb, cron, windows, nan]
---

# Mastermind System Ops (v4.2, Windows local)

Sistema personal de agente IA de David Antizar: Hermes Desktop (Windows) + NaN.builders + ChromaDB + GitHub (`Ntizar/MasterMind`). Este skill cubre SU OPERACIÓN en el PC local — la documentación de producto vive en el repo (README.md, mastermind/stars-explorer.md).

## Ubicaciones reales

| Qué | Dónde |
|---|---|
| Repo (fuente de verdad) | `C:\Users\d_ant\Projects\MasterMind` → github.com/Ntizar/MasterMind |
| Instalación Hermes | `%LOCALAPPDATA%\hermes\` (config.yaml, .env, skills/, memories/) |
| ChromaDB | `~/.mastermind/chromadb` — colección `mastermind-skills`, embebida sin servidor |
| Gateway | Autoarranque al login (`Hermes_Gateway.vbs` en Startup); comprobar con `hermes gateway status` |

Estructura del repo: `agent/` (skills + memories + SOUL.md), `scripts/` (motor), `notes/`, `data/` (stars-registry.json), `mastermind/` (docs internos).

## Python: cuál usar (PITFALL #1)

El `python` del PATH es el venv de Hermes y NO tiene pip ni chromadb. Para ChromaDB y scripts del motor usar SIEMPRE:

```
C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe
```

## NaN API: User-Agent obligatorio (PITFALL #2)

Toda petición Python (urllib/requests) a `api.nan.builders/v1` sin header `User-Agent` custom devuelve **403** (curl sí funciona sin él). Añadir p.ej. `"User-Agent": "MastermindIndexer/2.0"` a cada Request.

Modelos disponibles: `qwen3.8-flash` (principal objetivo), `glm5.3-flash` (activo hasta agotar tokens del mes), `qwen3-embedding` (embeddings, dim 4096, coseno, threshold score > 0.25). Cambiar modelo: `hermes config set model.default <modelo>` y re-anclar crons con `hermes cron edit <job_id> --model <m> --provider openai-api` si avisa de snapshots divergentes.

## Crons (viven si el gateway está vivo)

| Job | ID | Schedule |
|---|---|---|
| mastermind-scout (stars→skills→push) | bc390c1bf06a | cada 6h |
| mastermind-weekly-digest | d8e9eb7ce270 | lunes 9:00 |
| mastermind-doctor (health check + autocura) | cceb83c1026c | diario 10:00 |

## Operación

```bash
cd C:/Users/d_ant/Projects/MasterMind
python scripts/consultar-skills.py "consulta" --json   # búsqueda semántica
python scripts/indexar-skills.py [--reset]              # indexar (tras crear skills)
python scripts/doctor.py [--json]                       # health check
python scripts/test-doctor.py [--json]                  # tests del doctor (bug-inyección, 9 casos sandbox)
bash scripts/run-stars-explorer.sh --batch 3 --json     # explorar stars manual
```

Tras tocar `doctor.py`, ejecutar SIEMPRE `test-doctor.py` (patrón bug-inyección:
inyecta cada bug real en sandboxes bajo %TEMP% y verifica que el doctor lo detecta).
Los overrides `MM_DOCTOR_REPO/HERMES/CHROMA/SANDBOX` permiten correr doctor.py
contra sandboxes aislados sin tocar el sistema real. Ruta de onboarding del repo:
`mastermind/onboarding/` (01-06, incluye recuperación desde cero).

## Pitfalls operativos

0. **Sincronizar ANTES de indexar**: la instalación (`%LOCALAPPDATA%\hermes\skills\`) y el repo divergen con facilidad (88 skills llegaron a divergir sin que nadie lo notara). Antes de indexar o confiar en el repo como fuente de verdad: `python scripts/sincronizar-skills.py` (bidireccional, unión, nunca borra). El conteo del doctor NO detecta divergencia de contenido — para eso está `python scripts/test-cobertura.py`.

1. **Rutas MSYS vs nativas**: exportar `STARS_REGISTRY=/c/Users/...` desde bash y que un python.exe nativo la lea crea literalmente `C:\c\Users\...`. Los wrappers pasan rutas en formato `C:/Users/...`.
2. **Secrets nunca en prompts de cron**: el explorador de stars usa `gh auth token` (keyring) dentro del wrapper — nunca patrones de lectura de .env en el prompt (el scanner de cron los bloquea).
3. **Embeddings en lote**: batches de 12 textos ≤3000 chars funcionan; 32×6000 puede dar 403.
4. **Reglas del repo**: NUNCA borrar del repo MasterMind (solo crear/modificar); todo en castellano; no fijar cifras de skills en docs (crecen con cada ciclo); el nombre "Koldo" está retirado — no usar.
5. **rm -rf grandes en terminal quedan bloqueados sin aprobación** del usuario; dividir limpieza en pasos pequeños o confirmar antes.
6. **Push concurrente del cron scout**: el scout pushea a `Ntizar/MasterMind` cada 6h; un push directo puede rechazarse con "fetch first". Resolver SIEMPRE con `git pull --rebase origin master && git push` — nunca con merge ni forzando. Aplica a cualquier trabajo sobre el repo.
7. **Landing del repo (`index.html`) consume Aurora v6 vía CDN** (`ntizar.css + next + three + data + patterns + motion`): el diseño se edita en el repo `~/Projects/Ntizar-Aurora`, nunca con CSS custom en MasterMind. Ver skill `aurora-design-system`. Auditoría: `python scripts/audit-aurora.py index.html` (del skill Aurora).
8. **Sincronizar skill → repo tras editar el skill local**: los skills pueden existir solo en la instalación local y olvidarse en el repo (pasó con este skill hasta 2026-08-29). Tras editar un skill aquí, copiarlo a `agent/skills/<dominio>/` del repo y commitear — el repo es la fuente de verdad y la reconstrucción depende de él.
9. **Pitfall de patches en SKILL.md**: un patch cuyo old_string coincide con una línea de definición puede SUSTITUIR la línea en vez de insertar antes (borró `resultados = []` en test-doctor.py y costó un NameError). Al insertar secciones nuevas, incluir en old_string el título de la sección siguiente y devolverlo íntegro en new_string.

## Memoria por especialista

Los skills con estado acumulativo mantienen su memoria de dominio en `references/estado-<tema>.md`
(patrón importado de javierpa95/harness: memoria por rol, comiteada y versionada). Reglas:

1. El skill describe en su SKILL.md DÓNDE está su memoria (ej. `references/estado-cromos.md`).
2. Antes de trabajar, se lee; al terminar, se actualiza con hallazgos nuevos (conciso, máximo ~200 líneas).
3. La memoria vive en el REPO (`agent/skills/<dominio>/<skill>/references/`) → versionada, backup automático.
4. Solo memoria de dominio acumulativo (hallazgos, convenciones, gotchas). Lo puntual va a notes/, no aquí.
5. Los skills de referencia pura (sin estado entre ejecuciones) NO necesitan memoria.

Reconstrucción desde cero (si se pierde el PC): restaurar el repo = restaurar las memorias.

## Reconstrucción desde cero (si se pierde el PC)

1. Instalar Hermes Agent + clonar `Ntizar/MasterMind` a `~/Projects/MasterMind`
2. `pip install chromadb` con el Python del sistema
3. Copiar `agent/skills/` → `%LOCALAPPDATA%\hermes\skills\`, `agent/MEMORY.md`/`USER.md` → `memories/`
4. `python scripts/indexar-skills.py --reset` (necesita OPENAI_API_KEY/OPENAI_BASE_URL de NaN en `.env` de Hermes)
5. `hermes gateway install` (activa los crons) + `python scripts/doctor.py` para verificar
