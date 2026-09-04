---
name: mastermind-system-ops
description: "Usar al operar Mastermind en Windows: repo, ChromaDB, crons, gateway Telegram (colapso por token revocado y su restauración), backups y monitorización."
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

Modelos disponibles en NaN (verificado 2026-08-31, `/v1/models` + smoke test): `qwen3.8-flash` (vivo; default global hasta 2026-09-03, sigue pinneado en los crons), `deepseek-v4-flash` (vivo, el más barato; **nuevo default global desde 2026-09-03** — smoke test de texto+tools+visión superado), `glm5.3-flash` (vivo hasta agotar cuota), `qwen3.6` (vivo), `qwen3-embedding` (embeddings, dim 4096, coseno, threshold score > 0.25); `minimax-h3` responde 401 = fuera de plan. Cambiar modelo global: `hermes config set model.default <modelo>` — AVISA de los crons "unpinned" con model_snapshot divergente que fallarán closed: re-anclar TODOS con `hermes cron edit <job_id> --model <m> --provider openai-api` (ambas flags obligatorias juntas).

**PITFALL #2b — cuota de glm5.3 y fallos silenciosos de cron (verificado 2026-08-31):** glm5.3-flash agota los tokens del mes ANTES de fin de mes → los crons asignados a él revientan con `RuntimeError: HTTP 402`. Como el digest/scout/doctor entregan a `local`, el error queda enterrado en `cron/output/<job_id>/*.md` sin aviso (ese día fallaron 3 de 9 crons sin que nadie se enterara). Reglas: 1) ante 402/429 el fallback natural es reintentar/anclar a qwen3.8-flash; 2) para detectar fallos ajenos, revisar `cronjob list` (campo `last_status`) o leer las salidas en `cron/output/` — un error de modelo NO es un fallo del script, comprobar el .md del run antes de tocar el prompt; 3) **solución activa: job `vigia-cron` (no_agent, cada 30min, deliver telegram) con `scripts/vigia-cron.py` de esta skill** — lee jobs.json, alerta SOLO fallos NUEVOS (estado no-ok + hash name|last_run_at en vigia-estado.json; stdout vacío = silencio). Si se pierde el job: `hermes cron create "*/30 * * * *" --name vigia-cron --no-agent --script vigia-cron.py --deliver telegram` (--script exige ruta RELATIVA a ~/.hermes/scripts/, un path absoluto falla en silencio).

## Gateway caído / token de Telegram revocado (verificado 2026-09-02)

Síntoma del colapso: `hermes gateway status` = "No gateway process" y en `logs/gateway.log`: `Telegram bot token rejected ... non-retryable startup conflict` → el gateway MUERE al arrancar si el token es inválido (no reintenta). Los crons siguen corriendo y entregando error `Telegram send failed: Unauthorized`. Diagnóstico en 3 comandos: `hermes gateway status`, `tail gateway.log`, `curl -s https://api.telegram.org/bot<TOKEN>/getMe` (401 = token revocado → David pide /token o /newbot en @BotFather).

**Procedimiento de restauración del bot**: 1) validar token nuevo contra `getMe` ANTES de nada; 2) escribirlo en `.env` (`TELEGRAM_BOT_TOKEN`); 3) `hermes gateway restart`; 4) verificar `telegram connected` en gateway.log; 5) prueba REAL de entrega con `sendMessage` al chat 7288273982. Si el bot es NUEVO (@/newbot), David debe hacer `/start` al bot antes de que pueda escribirle, y re-añadirlo al grupo -1004341345827.

**Pitfalls**: a) `getUpdates` devuelve 409 "terminated by other getUpdates" cuando el gateway ya está polling — es BUENA señal, no borrar nada; b) `curl` desde git-bash con emojis/tildes a Telegram da `strings must be encoded in UTF-8` — usar texto plano ASCII o python; c) copiar un token viejo de BotFather parece nuevo pero la ID de bot (prefijo numérico) delata: bot nuevo = prefijo nuevo; d) NUNCA pegar el token en chat sin verificar — puede ser el revocado.

**Watchdog (auto-curación)**: tarea `Hermes_Gateway_Watchdog` del Task Scheduler (cada 10 min, `scripts/vigia-gateway.ps1` en instalación + repo `scripts/`) — si no hay gateway: lo relanza, comprueba en gateway.log si "telegram connected", escribe en `logs/vigia-gateway.log` y AVISA por Telegram (lee token del .env; si Telegram no conecta, el aviso alerta del token revocado). Vive FUERA del gateway a propósito: un cron de Hermes no puede vigilar al gateway que lo ejecuta. Registro: `powershell -File scripts/registrar-vigia-gateway.ps1`.

## Cambiar el modelo global del bot: flujo de reinicio (verificado 2026-09-03)

`hermes config set model.default <m>` NO relee el proceso gateway en marcha: el bot sigue con el modelo que leyó al arrancar; solo las sesiones nuevas tras un reinicio estrenan el default. Flujo completo para "que lo estrene ya":

1. **Smoke test ANTES de cambiar** contra `https://api.nan.builders/v1/chat/completions` (con User-Agent custom): texto, `tools`+`tool_choice` (el bot sin tool calling no opera) y **visión** — imagen 1×1 roja como data URL PNG en un content part `image_url`, preguntar el color y esperar «Rojo». Catálogo: GET `/v1/models`.
2. **Reiniciar**: el gateway es un *login item* (.vbs), NO un servicio — `hermes gateway restart` no lo gestiona. Matar PID: `taskkill /PID <pid> /F` (con un slash; `//PID` lo rechaza taskkill — no aplicar la doble-barra de cygwin aquí). Luego el watchdog tarda hasta 10 min → no esperar: invocar `powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "%LOCALAPPDATA%\hermes\scripts\vigia-gateway.ps1"` y verificar `hermes gateway status` con PID nuevo en ~20s.
3. **Verificar en `logs/agent.log`**: el reinicio hace `session_reset` del DM de Telegram (nace sesión nueva → atrapa el default); confirmar línea `model=<nuevo>` o el session_reset + respuesta enviada. Las sesiones de escritorio ya abiertas NO cambian (prompt caching) — es comportamiento esperado, no un bug.
4. Recordar al usuario: los **crons pinneados no se mueven** con el default; `/model <m>` revierte por sesión.

## Crons (viven si el gateway está vivo)

### PITFALL — el tool `cronjob` NO persiste el modelo (verificado 2026-09-01)
Crear un job vía el tool `cronjob` (action=create) deja `model: null` → el run usa el default (glm5.3 → 402). `cronjob action=update` con solo `model` falla con "No updates provided" (no es un campo editable ahí). Fix SIEMPRE por CLI: `hermes cron edit <job_id> --model qwen3.8-flash --provider openai-api`. Tras crear cualquier cron, verificar `model` en `cronjob list` y re-anclar si sale null.
**Cron "ahora mismo" (one-shot inmediato)**: `schedule` en ISO (`2026-09-01T00:17:00`) a 2-3 min vista + `repeat: 1`; reprogramar el fuego con `hermes cron edit <id> --schedule <ISO>`; confirmar arranque con `hermes cron runs <job_id>` (estado `running`).

### Cron con ventana horaria (maratones de N batches en M horas)

Pedido tipo "tira crons de aprendizaje durante 6 horas" → UN solo cron con expr de ventana + `repeat: N`: p.ej. `*/25 1-6 1 9 *` = cada 25 min entre 01:00-06:59 del 1 de septiembre, 18 fuegos. El prompt de cada batch debe ser autocontenido: dedup contra registry/estado persistente (así los batches no se pisan), commit+push por batch, append a un notes/ compartible (`### Batch — HH:MM`, nunca borrar secciones ajenas), y reporte final ≤5 líneas (llega de madrugada, el usuario duerme). `hermes cron edit <id> --repeat N` sí funciona para ajustar el número de batches tras crear el job.

**PITFALL — orden de campos en expr cron con fecha fija**: es `min hora día mes dow`. Escribir `*/25 1-6 9 1 *` queriendo "1 de septiembre" da día=9, mes=1 → `next_run_at: 2027-01-09`. SIEMPRE verificar `next_run_at` en la respuesta de creación (o `cronjob list`) tras programar Anything fechado, y corregir con `hermes cron edit <id> --schedule "<expr>"`.

**Colisión con cron regular (obligatorio)**: un maratón sobre el mismo repo NO puede solaparse con el scout regular (push cruzado "fetch first"). Pausar el regular (`hermes cron pause <id>`) y crear un one-shot `no_agent` con script que haga `hermes cron resume <id>` y avise por telegram a la hora de fin del maratón (ej. 07:15). Nunca depender de reactivar a mano. Script de ejemplo: `scripts/reactivar-scout.py` (subprocess → `hermes cron resume`, stdout solo si algo va mal o para confirmación única).

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

## TTS / voz (es-ES-AlvaroNeural)

La voz de David es **Álvaro (`es-ES-AlvaroNeural`)**. Si un audio sale en inglés o con voz femenina:

1. **Causa típica**: falta el bloque `tts:` en config.yaml → Hermes usa el default de edge (voz inglesa). Verificar: `grep -n -A6 '^tts:' "$LOCALAPPDATA/hermes/config.yaml"`.
2. **Fix (persistente)**: `hermes config set tts.provider edge && hermes config set tts.voice es-ES-AlvaroNeural`. La config se carga al ARRANCAR la sesión — no aplica en caliente en la sesión actual.
3. **Regenerar en caliente (misma sesión)**: llamar edge-tts directamente con el Python del venv (`import edge_tts` funciona ahí), voice="es-ES-AlvaroNeural", y convertir a OGG/Opus con ffmpeg (`-c:a libopus -b:a 48k -vbr on`) para que Telegram lo entregue como burbuja de voz.
4. `patch`/write directo sobre config.yaml está BLOQUEADO para el agente (refuse de seguridad) — siempre vía `hermes config set`.
5. `tts.voice` y `tts.speed` no son claves reconocidas por `hermes config set` (avisa pero las guarda y tts_tool.py sí las lee: `tts_config.get("voice")` en tools/tts_tool.py).

STT ya configurado: local faster-whisper, model base, language en (auto-transcribe notas de voz de Telegram).

## Pitfalls operativos

0. **Sincronizar ANTES de indexar** (bug corregido 2026-09-04): la instalación (`%LOCALAPPDATA%\hermes\skills\`) y el repo divergen con facilidad — llegaron a divergir en **88 skills** (incl. comfyui con scripts/tests) sin que nadie lo notara. **La instalación es la fuente VIVA; el repo (`agent/skills/`) es el backup/committed.** Antes de indexar o confiar en el repo: `python scripts/sincronizar-skills.py` (bidireccional, unión, nunca borra).

   **BUG del sincronizador ANTES de 2026-09-04**: solo copiaba skills que existían en un lado (`solo_i`/`solo_r`) y NO propagaba los que existían en ambos pero con CONTENIDO distinto → los patches en la instalación nunca llegaban al repo, y el repo se quedaba atrás. **Corregido**: ahora también copia instalación→repo los comunes cuyo contenido difiere (la instalación GANA). Verificar siempre el diff (`git diff --ignore-all-space`) tras sincronizar: 147 archivos con cambio "real" ignorando whitespace era en parte line-ending. El conteo del doctor NO detecta divergencia de contenido — `python scripts/test-cobertura.py` sí. Para reflejar contenido actualizado en la búsqueda semántica, tras sincronizar correr `python scripts/indexar-skills.py --reset` (re-indexa todos, no solo los nuevos).

1. **Rutas MSYS vs nativas**: exportar `STARS_REGISTRY=/c/Users/...` desde bash y que un python.exe nativo la lea crea literalmente `C:\c\Users\...`. Los wrappers pasan rutas en formato `C:/Users/...`.
2. **Secrets nunca en prompts de cron**: el explorador de stars usa `gh auth token` (keyring) dentro del wrapper — nunca patrones de lectura de .env en el prompt (el scanner de cron los bloquea).
3. **Embeddings en lote**: batches de 12 textos ≤3000 chars funcionan; 32×6000 puede dar 403.
4. **Reglas del repo**: NUNCA borrar del repo MasterMind (solo crear/modificar); todo en castellano; no fijar cifras de skills en docs (crecen con cada ciclo); nombre público del bot de Telegram: **NtizarBot** (@Ntizarbot) — "Koldo" es solo el apodo privado de David, jamás debe aparecer en textos públicos, presentaciones, configs visibles ni docs.
5. **rm -rf grandes en terminal quedan bloqueados sin aprobación** del usuario; dividir limpieza en pasos pequeños o confirmar antes.
6. **Push concurrente del cron scout**: el scout pushea a `Ntizar/MasterMind` cada 6h; un push directo puede rechazarse con "fetch first". Resolver SIEMPRE con `git pull --rebase origin master && git push` — nunca con merge ni forzando. Aplica a cualquier trabajo sobre el repo.
7. **Deploy a GitHub Pages: habilitar Pages ANTES de la Action (verificado 2026-09-03).** Una workflow `configure-pages@v5` en un repo nuevo falla en el paso "Configurar Pages" con `Get Pages site failed ... Error: Not Found` si el repo no tiene Pages habilitado. Antes de desplegar, habilitar la API (o `gh`): `gh api -X POST repos/<owner>/<repo>/pages -f 'build_type=workflow'`. Esto devuelve el `html_url` (p.ej. `https://ntizar.github.io/aurora-prism/`). Luego relanzar la workflow (`gh workflow run deploy-pages.yml --ref main`) y verificar `gh run list` hasta `success` + `curl -s -o /dev/null -w "%{http_code}" <html_url>` = 200. Verificar también la base de Vite (`base: './'`) para rutas relativas correctas en Pages.
7. **Landing del repo (`index.html`) consume Aurora v6 vía CDN** (`ntizar.css + next + three + data + patterns + motion`): el diseño se edita en el repo `~/Projects/Ntizar-Aurora`, nunca con CSS custom en MasterMind. Ver skill `aurora-design-system`. Auditoría: `python scripts/audit-aurora.py index.html` (del skill Aurora).
8. **Sincronizar skill → repo tras editar el skill local**: los skills pueden existir solo en la instalación local y olvidarse en el repo (pasó con este skill hasta 2026-08-29). Tras editar un skill aquí, copiarlo a `agent/skills/<dominio>/` del repo y commitear — el repo es la fuente de verdad y la reconstrucción depende de él.
9. **Pitfall de patches en SKILL.md**: un patch cuyo old_string coincide con una línea de definición puede SUSTITUIR la línea en vez de insertar antes (borró `resultados = []` en test-doctor.py y costó un NameError). Al insertar secciones nuevas, incluir en old_string el título de la sección siguiente y devolverlo íntegro en new_string.

## Auditoría de consumo real de tokens (state.db)

Método primario para responder "¿cuántos tokens me he comido hoy/esta semana?" — MEDIR, no estimar. **Script listo: `python scripts/auditar-tokens.py [YYYY-MM-DD]`** (en este skill; sin args = hoy). Fuente: `%LOCALAPPDATA%\hermes\state.db`, tabla `sessions`, columnas ya existentes: `input_tokens, output_tokens, cache_read_tokens, reasoning_tokens, api_call_count, tool_call_count, started_at, last_activity_at, model, profile_name, title`.

```python
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)  # read-only: no bloquea el gateway
rows = con.execute("SELECT id,profile_name,model,started_at,last_activity_at,input_tokens,output_tokens,cache_read_tokens,reasoning_tokens,api_call_count,estimated_cost_usd,title FROM sessions").fetchall()
# started_at/last_activity_at son FLOATS unix → filtrar el día con datetime.fromtimestamp() EN PYTHON
```

Pitfalls verificados (2026-09-01):
- `estimated_cost_usd`/`actual_cost_usd` salen **0/NULL con NaN** (cost_status='unknown') → calcular el coste a mano con precios NaN (~$0,50/M qwen3.8-flash).
- Función SQL user-defined sobre timestamps que recibe None/str tumba la query entera → procesar en Python.
- `profile_name` NULL = perfil default → `p or "default"`.
- Fuga nº1 = `input_tokens / api_call_count` (contexto medio reenviado por llamada); una sesión con 130 llamadas × contexto grande come más que un día entero de crons. `cache_read_tokens` alto amortiza.
- 429/concurrencia: `logs/errors.log` (grep fecha) y `sessions/request_dump_*.json` (reason='max_retries_exhausted', error 429 'qwen3.8-flash concurrency limit: max 5').
- **Framing para David:** 10M tokens/día ≈ 4-5 € con flash — el problema real es cuota/concurrencia, no euros; decirlo siempre para no alarmar.
- El log manual `tokens/tokens-log.json` vive en `~/Projects/MasterMind/tokens/` (el skill `token-tracking` dice `/hermes-home/tokens/` que no existe en Windows — ruta real verificada).

## ¿Dónde están las conversaciones de cada plataforma? (verificado 2026-09-02)

TODO (desktop, Telegram, cron, subagentes) se guarda en la MISMA tabla `sessions` de
`%LOCALAPPDATA%\hermes\state.db`, etiquetado por la columna `source`. Que algo no
aparezca en el sidebar de Hermes Desktop NUNCA significa que no se guardara: el sidebar
**secciona por fuente** (`source` / `exclude_sources` en `GET /api/sessions`) en
Recientes (locales: `cli`, `desktop`, `tui`…) + una sección **Mensajería** agrupada por
plataforma (Telegram, Discord…) + Cron jobs. Comprobado: telegram 19 sesiones / 2165
mensajes frente a desktop 13 / 1496 — el bot acumula más charla que el escritorio.

Ante "¿no se guardan aquí las conversaciones de Telegram?": **MEDIR, no especular**.

```python
con = sqlite3.connect("file:" + dbpath + "?mode=ro", uri=True)   # read-only: no bloquea al gateway
con.execute("select source,count(*),sum(message_count) from sessions group by source")
# y las de una plataforma, con los flags que explican ausencias en la UI:
con.execute("select id,title,message_count,hidden,archived,parent_session_id,"
            "datetime(last_activity_at,'unixepoch','localtime') from sessions "
            "where source='telegram' order by last_activity_at desc limit 10")
```

`hermes sessions stats` da lo mismo de un vistazo. Flags `hidden`/`archived` = ocultas en
la UI pero intactas en la base. Las cadenas de compresión/branch (`parent_session_id`) se
proyectan como **una sola entrada** en las listas → el conteo del sidebar jamás cuadra con
las filas brutas de la tabla: no es un bug, no volver a insistir en ello.

Cómo tenerlas a mano (decírselo así al usuario): desplegar **Mensajería → Telegram** en la
barra lateral y clicar una sesión para leer la transcripción completa; o `session_search`
para ir a contenido concreto; o `hermes sessions export --session-id <id> --format md`
para sacarla a archivo. (Seguir hablando con el bot se hace desde Telegram; la sesión
continúa ahí tal cual.)

**PITFALL al investigar el UI de escritorio**: NO greppees `apps/desktop/dist/assets/*.js`
— está minificado (identificadores `IXe`/`$Ue`, todo en una línea) y no se aprende nada.
El árbol legible, con los comentarios que explican el *porqué*, está en
`apps/desktop/src/`: p.ej. `src/lib/session-source.ts` (`LOCAL_SESSION_SOURCE_IDS`,
`MESSAGING_SESSION_SOURCE_IDS`, `isMessagingSource`) y `src/api/sessions.ts`; los `.test.ts`
adyacentes muestran la forma exacta de las peticiones. Ese árbol existe incluso con la app
empaquetada, bajo `%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\src`. En el backend:
`hermes_cli/web_routers/sessions.py` y `list_sessions_rich` en `hermes_state.py`.

## Simulación multiagente con perfiles Hermes (Bot Mode)

Para agentes persistentes con personalidad/KPIs que conversan entre sí (Gobierno IA, etc.): setup de perfiles, conversación por rondas vía ficheros, auditor independiente, boletín público Pages. Ver `references/bots-multagente-persistentes.md` (probado 2026-08 en Ntizar/gobierno-ia). Incluye el retarget de modelo por capas + el tope `max_tokens` (v2.2).

## Memoria por especialista

> **Criterio al aprender de un set curado (estrellas/favoritos) — NO descartar por estrellas ni overlap:
> extraer el ÁNGULO y convertirlo en UPGRADE/NEW_SKILL/REFERENCE.** Ver `references/criterio-aprendizaje-set-curado.md`.

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
