# Simulación multiagente persistente con perfiles Hermes (Bot Mode)

Probado en Gobierno IA (Ntizar/gobierno-ia, 2026-08-29): 3 ministros + auditor con personalidad, KPIs y conversación por rondas, todo público en GitHub Pages. **v2 (2026-08-31): capa de emoción, noticias reales y laboratorio de disrupción** — ver sección al final.

## Cuándo usar perfiles en vez de delegate_task
`delegate_task` = subagentes efímeros sin memoria. Perfiles Hermes = agentes persistentes con identidad, KPIs e historial. Usar perfiles cuando el usuario quiere agentes con **personalidad y memoria** que interactúan entre sí (consejos, debates, simulaciones).

## Setup por perfil (PASO OBLIGATORIO — los perfiles nuevos no heredan nada)
1. `hermes profile create <nombre>`
2. Escribir `SOUL.md` en `C:/Users/d_ant/AppData/Local/hermes/profiles/<nombre>/` (identidad, voz, reglas, marcado "versión IA, ficticia").
3. Copiar líneas `OPENAI_API_KEY|OPENAI_BASE_URL` del `.env` principal (`$LOCALAPPDATA/hermes/.env`) al `.env` del perfil.
4. Escribir `config.yaml` del perfil con el modelo (ej. glm5.3-flash / openai-api / https://api.nan.builders/v1) — sin esto da 401 o usa el modelo por defecto.
5. **Test antes del lanzamiento**: `hermes -p <perfil> chat -q "test"` y verificar que ejecuta tool calls (fallo típico: respuesta en 2s sin tools = sin credenciales).

Sintaxis CLI: `hermes -p <perfil> chat -q "<prompt>"` (NO existen `--print` ni `-z`).

## Arquitectura conversacional
- **Ficheros markdown como canal**: toda la comunicación entre agentes pasa por ficheros del repo (ej. `consejo/ronda1-<agente>.md`). Auditable y versionado — feature, no bug.
- **Rondas estructuradas, no chat libre**: r1 exposición (paralelo), r2 réplica cruzada (cada uno lee los ficheros de los otros), r3 decisión del orquestador. Límite de rondas para evitar divagación.
- **Lanzamiento paralelo**: `terminal(background=true)` o `subprocess` por agente + poll de los ficheros de salida.
- **Anti-invención**: cada agente solo puede citar fuentes descargadas a ficheros del repo; propuesta sin referencia exacta → rechazada. Git = versionado.
- **Auditor independiente**: perfil aparte que solo juzga (VALIDADA/OBSERVACIONES/RECHAZADA), puede contradecir al orquestador, veredictos sin filtrar.
- **KPIs evolutivos**: `kpis.md` por agente con histórico diario + sección Lecciones; cada ciclo los actualizan.
- **Crons por rol**: pase de lista, reunión, informe, auditoría — `deliver='origin'`.
- **Publicidad**: `scripts/generar_boletin.py` regenera `docs/index.html` desde los ficheros y push → Pages. El usuario pidió explícitamente "informes de cada paso y que se vea todo en el index".

## Pitfalls
- **Regex del generador vs formato libre de los agentes**: los agentes escriben tablas markdown y `**APROBADO**` en celdas. El parser debe tolerar (`\*?\*?`, espacios, filas de tabla), no asumir formato fijo. Si el index no muestra una sección, comparar regex vs fichero real antes de culpar al pipeline.
- **Pages tarda 3-5 min en reconstruir** tras el push — verificar con `gh api repos/<o>/<r>/pages/builds/latest --jq '.status'` antes de asumir fallo.
- **Roles reales**: verificar nombres/personalidades con web_search contra fuentes actuales (los gobiernos cambian); siempre "versión IA, ficticia".
- **Repo privado no tiene Pages** con el plan gratuito → `gh repo edit <o>/<r> --visibility public --accept-visibility-change-consequences` (solo si no hay secretos dentro).
- **BOE**: curl funciona; urllib con User-Agent custom da HTTP 400. Ver skill `boe-borme-api`.

## v2.2 (2026-09-04) — Re-target de modelo/fleet por capas y el tope `max_tokens`

Cuando el usuario pide "pasar todo el proyecto a otro modelo, sin límite de tokens" (Gobierno IA → qwen3.6), retarget en DOS capas — cambiar solo una deja el sistema híbrido:

1. **Perfiles de bots** (los que ejecutan la ley). Cada bot es un perfil Hermes con su propio `config.yaml`; el coordinador los lanza con `hermes -p <perfil> chat -q`, así que el modelo del bot lo fija SU perfil, no el cron. Profes para Gobierno IA: `ministro-hacienda`, `ministro-sanidad`, `ministro-ecologia`, `auditor`. Cambiar por CLI (nunca hand-edit, el guard lo bloquea):
   ```bash
   hermes -p <perfil> config set model.default qwen3.6
   hermes -p <perfil> config set model.max_tokens 16384
   ```
2. **Cron coordinador** (el que orquesta: pase de lista `7f86939758e2`, consejo `d8c606f0f8da`, informe presidencial `7fba6b3bdf69`, auditoría `107b96a17053`). En los crons `model` se cambia con `hermes cron edit <job_id> --model <m>` (el tool `cronjob` no persiste modelo — ver PITFALL abajo).
   ```bash
   hermes cron edit <job_id> --model qwen3.6
   ```

**PITFALL "sin límite de tokens" NO es literal (verificado 2026-09-04):** Hermes NO tiene un tope infinito; cuando `model.max_tokens` no está definido manda `max_tokens or 4096` (`agent/agent_init.py` / `chat_completion_helpers.py`), y ese 4096 es justo el que corta el razonamiento/JSON del modelo con reasoning. "Sin límite" = dejar `max_tokens` ALTO (16384 es seguro; más y la API puede devolver 400 por exceder la capacidad del modelo). El tope se pone en el **perfil** (`model.max_tokens`), no en el cron — y como el cron delega al perfil, los bots lo heredan igualmente. `model.max_tokens` NO se puede fijar por job cron.

**Verificación post-cambio**: leer el config de cada perfil (`grep -E "default:|max_tokens:") y `model` en `cron/jobs.json` (cat vía python), no confiar en el output del set. Los 4 crons + 4 perfiles deben quedar en el mismo modelo.

## v2.1 (2026-09-01) — Escenas informales off-record (el "café")
Pedidos tipo "que los ministros se tomen un café y hablen de sus problemas" = otra clase de escena, complementaria al Consejo:
- **Off-record real**: sin citas BOE, sin bloques [aXXX], sin formato propuesta — se desahogan, no legislan. Encabezado que lo declare: "escena no oficial: no genera acuerdos".
- **Anclaje en datos reales del repo**: el prompt del cron debe leer `ministerios/*/agenda.md`, `diario.md` y el último `auditoria/*.md` y SACAR de ahí los problemas (noticias reales de la agenda), no inventarlos.
- **Formato guion suelto** (`**Nombre**: …`, ~550-750 palabras) en `ministerios/cafe/YYYY-MM-DD-cafe.md`, NO acta: que se interrumpan, discrepen, ironicen. Prohibido romper el personaje dentro del guion (nada de IAs/tokens ahí; sí en los diarios).
- **Efecto secundario útil**: cada ministro deja huella en SU `diario.md` (append, nunca borrar) — con diarios en semillas, una escena informal los estrena.
- El coordinador añade 2-3 frases propias al final de la entrega. Entrega `deliver='origin'` con la escena ÍNTEGRA (no resumen).
