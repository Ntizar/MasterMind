---
name: mastermind-setup
description: "Configura y mantiene el sistema personal de agentes Mastermind — sincronización de repositorio GitHub, instalación de skills, configuración de SOUL.md y auto-configuración de cron para el segundo cerebro de Ntizar."
version: 1.4.0
author: Ntizar + Hermes Agent
tags: [mastermind, setup, github, skills, soul, nan, identity]
---

# Mastermind Setup

Procedures for setting up and maintaining the Mastermind personal agent system — a private GitHub repo that serves as the agent's second brain (skills, notes, memory, config, scripts).

## Cuándo usar

- Se configura un nuevo entorno de Hermes Agent para Ntizar
- Necesitas sincronizar skills desde el repositorio Mastermind al sistema local
- El SOUL.md se corrompió o truncó y necesita recuperación
- Se necesitan configurar cron jobs de sincronización automática

## Cuándo NO usar

- Configurar un usuario diferente de Ntizar → el repo y las rutas son específicas
- Solo necesitas instalar un skill individual → usa `skill_manage(action='create')` directamente
- El sistema ya está configurado y funcionando → no reconfigurar sin necesidad

## Identity

El nombre del agente es **Mastermind**, no "Hermes Agent". Hermes es el framework subyacente; Mastermind es el nombre que David (Ntizar) le dio a su sistema de agente personal. Al presentarte o referirte a ti mismo, usa "Mastermind".

- **Framework:** Hermes Agent (el motor subyacente)
- **Nombre:** Mastermind (el agente personal)
- **Usuario:** David Antizar (Ntizar)

Esta es la identidad preferida del usuario. Siempre presentarse como Mastermind.

## Setup

### 1. Install GitHub CLI

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt-get update -qq && apt-get install -y -qq gh
```

### 2. Authenticate with GitHub

```bash
# Read token from .env
token=$(grep GITHUB_TOKEN /hermes-home/.env 2>/dev/null | cut -d= -f2-)

# ⚠️ PITFALL: gh auth login fails when GITHUB_TOKEN env var is set
# Clear it first:
GITHUB_TOKEN="" echo "$token" | gh auth login --with-token
```

### 3. Clone the repo

```bash
cd /root/workspace
git clone https://github.com/Ntizar/mastermind.git
```

### 4. Configure Hermes to use it as a skills source

In `/hermes-home/config.yaml`:

```yaml
skills:
  external_dirs:
    - /root/workspace/Mastermind/mastermind
```

Then `/reset` (new session) for Hermes to detect the new skills.

### 5. Copy skills to local directory

```bash
mkdir -p /hermes-home/skills/mastermind
cp /root/workspace/Mastermind/mastermind/*.md /hermes-home/skills/mastermind/
```

Create a `SKILL.md` umbrella in `/hermes-home/skills/mastermind/SKILL.md` listing the individual skills.

### 6. Actualizar SOUL.md

Configurar `/hermes-home/SOUL.md` con: identidad del agente, reglas, sistema de conocimiento en 3 capas, estructura del repo, modelo de subagentes, stack actual y lista de skills.

### 8. Arrancar ChromaDB local (skills vector search)

ChromaDB corre en localhost:8000 para búsqueda semántica de skills. Debe arrancar tras cada reinicio de la VM:

```bash
# Arranque manual
bash /hermes-home/scripts/start-chromadb.sh

# Verificar
curl http://localhost:8000/api/v1/version
# → "1.5.9"
```

**Script de arranque:** El script `start-chromadb.sh` está en el skill `chromadb-skills-vector-search`:
```bash
skill_view(name='chromadb-skills-vector-search', file_path='scripts/start-chromadb.sh')
# O directamente:
bash /hermes-home/skills/chromadb-skills-vector-search/scripts/start-chromadb.sh
```

**Datos persistentes:** `/hermes-home/chromadb-data/`

**Pitfall:** ChromaDB NO arranca automáticamente al reiniciar la VM. Si el agente nota que las consultas semánticas fallan, debe ejecutar `start-chromadb.sh` o reportarlo.

Ver skill `chromadb-skills-vector-search` para detalles completos de indexación y consulta.

Create a cron job that runs daily:

```bash
# Schedule: 0 9 * * * (daily at 09:00 UTC)
# Prompt:
cd /root/workspace/Mastermind && git pull origin main
cp /root/workspace/Mastermind/mastermind/*.md /hermes-home/skills/mastermind/
gh auth status || re-authenticate from /hermes-home/.env
```

See `scripts/mastermind-autoconfig.sh` for the ready-to-use sync script (includes SOUL.md size guard).
See `scripts/restore-soul.sh` for SOUL.md sync check and recovery.
See `scripts/backup-hermes-memory.sh` for manual backup of memory to repo.
See `references/backup-hermes-complete.md` for the complete backup procedure (vulnerability assessment → copy → commit → auto-sync cron).
See `references/backup-pitfalls-2026-06-22.md` for backup pitfalls: double nesting with cp, duplicate commits, .hub/quarantine exclusion, skill-learning.log gitignore.
See `references/backup-rsync-fallback.md` for rsync fallback: Python shutil-based implementation when rsync binary is not available on the VM.
See `references/backup-cp-nesting.md` for the complete `cp -r` / `cp -a` double-nesting pitfall and safe copy patterns.

## Estructura del Repositorio

```
Mastermind/
├── README.md                          ← Visión general del sistema
├── ARCHITECTURE.md                    ← Documentación técnica (capas, flujos)
├── mastermind/                             ← Skills CORE del sistema
│   ├── SKILL.md                       ← Índice umbrella de skills propios
│   ├── SOUL.md                        ← Plantilla de identidad
│   └── (skills .md individuales)
├── learning/                          ← Sistema de aprendizaje autónomo
│   ├── MEGA-PLAN-LECTURA-ESCRITURA.md ← Plan maestro del curso
│   ├── README.md                      ← Cómo funciona el sistema
│   ├── sesiones/                      ← HTMLs de lecciones generadas
│   └── indices/                       ← Índices temáticos (autores, vocab...)
├── improvement/                       ← Mejora continua de Mastermind
│   ├── skills-desapavechadas.md       ← Skills que no uso y debería
│   ├── skills-nuevas-proyecto.md      ← Skills que debería crear
│   └── INDEX.md                       ← Índice unificado de mejoras
├── skills/                            ← Skills de referencia (hub externo)
│   └── INDEX.md                       ← Catálogo completo
├── config/
│   └── skill-priority.json            ← Prioridad HIGH/MEDIUM/LOW
├── scripts/                           ← Automatizaciones
│   ├── mastermind-autoconfig.sh            ← Autoconfiguración diaria
│   ├── generate-skill-index.sh        ← Generador de índice
│   └── (otros scripts)
├── memory/                            ← Respaldo de memoria
├── notes/                             ← Notas de sesiones
│   └── _template.md                   ← Template con frontmatter YAML
└── .deploy/                           ← Deploy configs (nginx, Docker)
```

## Reglas

1. **Nunca borrar del repositorio** — solo crear nuevos archivos o modificar archivos que creaste
2. **Formato de notas:** `YYYY-MM-DD-titulo.md` en `notes/`
3. **Skills:** cada skill tiene su propio archivo en `mastermind/`
4. **Commit tras aprender:** lecciones importantes → commit al repositorio
5. **Sin secretos en notas/commits/chat**
6. **SOUL.md es la fuente de verdad** para la identidad del agente — mantenerlo sincronizado con el repo

## Backup automático de Hermes al repo (MANTENER ACTUALIZADO)

Este es el procedimiento estándar de backup completo al repo Mastermind.
Ejecutar cuando se pida o como cron.

### Pasos

1. **Verificar que el destino existe:**
   ```bash
   test -d /root/workspace/Mastermind/hermes-home/ || mkdir -p /root/workspace/Mastermind/hermes-home/
   ```

2. **Copiar archivos/carpetas (rsync o fallback):**
   ```bash
   # OPCIÓN A: rsync (si está disponible)
   rsync -av /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
   rsync -av /hermes-home/memories/ /root/workspace/Mastermind/hermes-home/memories/
   rsync -av /hermes-home/notes/ /root/workspace/Mastermind/hermes-home/notes/
   rsync -av /hermes-home/scripts/ /root/workspace/Mastermind/hermes-home/scripts/
   
   # OPCIÓN B: rm -rf + cp -a (cuando rsync no está disponible — confirmado 2026-06-29)
   rm -rf /root/workspace/Mastermind/hermes-home/skills/
   cp -a /hermes-home/skills/ /root/workspace/Mastermind/hermes-home/skills/
   rm -rf /root/workspace/Mastermind/hermes-home/memories/
   cp -a /hermes-home/memories/ /root/workspace/Mastermind/hermes-home/memories/
   rm -rf /root/workspace/Mastermind/hermes-home/notes/
   cp -a /hermes-home/notes/ /root/workspace/Mastermind/hermes-home/notes/
   rm -rf /root/workspace/Mastermind/hermes-home/scripts/
   cp -a /hermes-home/scripts/ /root/workspace/Mastermind/hermes-home/scripts/
   
   cp /hermes-home/config.yaml /root/workspace/Mastermind/hermes-home/config.yaml
   ```
   > **Por qué rsync y no `cp -r`:** `cp -r /hermes-home/memories/ /dest/hermes-home/memories/` cuando el destino ya existe produce `/dest/hermes-home/memories/memories/`. `rsync -av` no tiene este problema. Si rsync no está, usar `rm -rf` + `cp -a` como fallback confirmado.

3. **Verificar que no hay nesting:**
   ```bash
   find /root/workspace/Mastermind/hermes-home/ -mindepth 2 -maxdepth 2 -type d | while read dir; do
     parent=$(basename "$(dirname "$dir")")
     child=$(basename "$dir")
     if [ "$parent" = "$child" ]; then
       echo "NESTED: $dir"
     fi
   done
   ```
   Si hay nesting, aplicar el fix cascading (ver pitfall 2026-06-28).

4. **Contar archivos copiados:**
   ```bash
   find /root/workspace/Mastermind/hermes-home/skills -type f | wc -l
   ```

5. **git add, commit, push:**
   ```bash
   cd /root/workspace/Mastermind
   git add -A
   git commit -m "Backup semanal: $(date +%Y-%m-%d)"
   git push origin HEAD:master
   ```

### Pitfalls críticos del backup

- **DOBLE NESTING con `cp -r` (recurrente):** `cp -r /hermes-home/memories/ /dest/hermes-home/memories/` cuando `/dest/hermes-home/memories/` ya existe produce `/dest/hermes-home/memories/memories/`. **SOLUCIÓN OBLIGATORIA:** usar `rsync -av` en lugar de `cp -r`. Siempre.
- **Cascading nesting en skills:** Cuando el nesting raíz se corrige (`skills/skills/` → `skills/`), CADA categoría top-level puede tener el mismo patrón: `ai-patterns/ai-patterns/`, `creative/creative/`, `stem/stem/` — 70+ directorios. **Fix:** loop sistemático `find . -mindepth 2 -maxdepth 2 -type d | while read dir; do parent=$(basename "$(dirname "$dir")"); child=$(basename "$dir"); if [ "$parent" = "$child" ]; then mv "$dir"/* "$dir"/.* . 2>/dev/null; rm -rf "$dir"; fi; done`.
- **skill-learning.log:** puede no existir (gitignore, puede haber sido eliminado). No fallar si no está.
- **Comparación de skills:** usar `find -name 'SKILL.md'` en ambos lados, EXCLUYENDO `.hub/`. El repo puede tener más skills que Hermes (skills propios del sistema, STEM, etc.). No es problema.
- **`.hub/quarantine/` no va al backup.** Contiene installs fallidas.
- **`.lock` files:** los archivos `.lock` de memories (MEMORY.md.lock, USER.md.lock) van al backup pero son inertes. Limpiarlos con `find -name '*.lock' -delete` antes de commit si se quiere repos limpio.
- **`.hub/` en conteo:** no incluir `.hub/` al comparar conteos de SKILL.md.
- **`rsync --delete` es destructivo:** solo usar si se quiere espejo exacto. Para backup incremental seguro, usar `rsync -av` SIN `--delete`.

- **Hermes no detecta external_dirs mid-session** — reiniciar sesión (`/reset`) tras cambiar `config.yaml`
- **SKILL.md requerido** — archivos `.md` individuales no se detectan sin un `SKILL.md` umbrella
- **gh auth falla con GITHUB_TOKEN set** — limpiar primero: `GITHUB_TOKEN="" echo "$token" | gh auth login --with-token`
- **SOUL.md debe actualizarse** — instalar skills no es suficiente; la identidad debe estar en SOUL.md
- **SOUL.md puede truncarse** — puede reducirse a ~48 bytes. **Detección:** `wc -c /hermes-home/SOUL.md` — si <1000, está corrupto. **Recuperación:** `cp /root/workspace/Mastermind/mastermind/SOUL.md /hermes-home/SOUL.md`
- **Hermes memory drifts from repo** — el cron NO hace backup de memoria. Usar `scripts/backup-hermes-memory.sh` manualmente.
- **SOUL.md size guard (ACTUALIZADO 2026-06-03)** — `mastermind-autoconfig.sh` usa lógica de 3 vías: (1) si local < 1000 bytes → SIEMPRE restaurar desde repo (truncado), (2) si repo > local → restaurar, (3) si local > repo y local > 1000 → subir al repo. El guard anterior solo comparaba `repo > local`, lo que permitía corrupción parcial silenciosa.
- **Config drift silencioso** — `tts.edge.voice` y `display.language` pueden perderse tras updates de Hermes o reconfiguraciones. **Verificar periódicamente:** `grep "voice:" /hermes-home/config.yaml | head -1` debe mostrar `es-ES-AlvaroNeural`, y `grep "language:" /hermes-home/config.yaml` debe mostrar `es` en sección display. Si están en inglés → el agente responde en inglés y TTS suena raro.
- **Hermes path quirk** — algunos deployments usan `/hermes-home/` en vez de `~/.hermes/`. Verificar `$HERMES_HOME`.
- **No crear skills con write_file manual** — usar `skill_manage(action='create')`.
- **Duplicate workspace clones** — solo una copia de Mastermind repo en `/root/workspace/Mastermind/`.
- **gh CLI no instalado** — `git push` funciona sin `gh`.
- **ChromaDB no sobrevive a reinicios** — la VM de NaN puede reiniciarse. ChromaDB no tiene systemd unit. Si el agente detecta que `curl localhost:8000/api/v1/version` falla, debe ejecutar `bash /hermes-home/scripts/start-chromadb.sh` para re-arrancarlo. Los datos persisten en `/hermes-home/chromadb-data/`.
- **Debian Node.js stub crashes** — `/usr/bin/node` es un stub que crashea. Usar nvm o shebang directo al path nvm.

## Patrón de Sincronización Bidireccional

## Orquestación de Cron Jobs (Multi-Sesión con Plan Maestro)

Cuando el usuario pide generar un proyecto grande que requiere múltiples sesiones/entregas (curso de 10 sesiones, serie de informes, batch de archivos), usar este patrón.

### Pasos

1. **Crear MEGA-PLAN.md** en el directorio de trabajo
   - Estructura general del proyecto
   - Diseño visual unificado (paleta, CDN, estilo)
   - Contenido detallado por sesión/archivo
   - Requisitos técnicos
   - Checklist de calidad

2. **Crear archivo principal** (INDEX.html, README, etc.) con navegación entre entregas

3. **Crear cron jobs** con:
   - `deliver: origin` (entregar al chat actual)
   - Schedule espaciado (cada 12h o 24h para no saturar)
   - `repeat: once` (ejecutar una sola vez)
   - Cada cron con prompt autocontenido que referencie el MEGA-PLAN.md
   - Nombre descriptivo: `NombreProyecto SNN — Descripción`

4. **Verificar que los crons se crearon** con `cronjob action=list`

### Reglas
- El MEGA-PLAN.md es la fuente de verdad: TODOS los crons lo referencian
- Cada cron debe ser autocontenido (no depende del contexto del chat)
- Espaciar crons para evitar saturación de tokens
- Límite de líneas por archivo para evitar truncamiento

### Pitfalls
- NO crear crons en bucle infinito (`repeat: forever`) para proyectos de una sola vez
- NO usar `openrouter` como provider en crons de Mastermind (401 error) — usar `qwen3.6` vía `custom`
- NO olvidar que los crons corren en sesión aislada: el prompt debe ser completamente autocontenido
- **Schedule format IMPORTANTE:** El campo `schedule` REQUIERE formato ISO timestamp para one-shots: `2026-06-09T08:00:00`. El formato `once at 2026-06-09 08:00` NO funciona. Para recurring usar cron expression: `0 8 * * *`
- **repeat bug:** NO pasar `repeat` como string numérico (ej. `"forever"` como string). El parámetro `repeat` espera un string como `"forever"` o `"once"`, pero si se pasa como número causa `'<=' not supported`. Para crons recurrentes, omitir `repeat` (hereda `forever` por defecto) o pasar `repeat="forever"` como string. Para crons con schedule cron, `repeat` se infiere automáticamente.

El sistema Mastermind usa **sincronización bidireccional** entre el repositorio GitHub y Hermes Agent:

1. **GitHub → Hermes**: `cd /root/workspace/Mastermind && git pull origin main` luego `cp -n /root/workspace/Mastermind/mastermind/*.md /hermes-home/skills/mastermind/`
2. **Hermes → GitHub**: Copiar `MEMORY.md` y `USER.md` a `memory/hermes-memory.md` y `memory/hermes-user.md`, luego `git add -A && git commit -m "auto: backup de memoria $(date +%Y-%m-%d)" && git push origin main`

El script `scripts/mastermind-autoconfig.sh` automatiza ambas direcciones. Ejecutar manualmente o vía cron para sync diario.

### Pitfalls de sincronización

- **Skills ya sincronizados**: Antes de copiar, ejecuta `diff <(ls mastermind/ | sort) <(ls /hermes-home/skills/mastermind/ | sort)` — si está vacío, no se necesita copia.
- **Nombres de archivos de backup**: Usar siempre `memory/hermes-memory.md` y `memory/hermes-user.md` en el repo.
- **Mensajes redirect de git son benignos**: Si `git push` muestra redirect, el push aún funciona. No tratar como error.
- **URL canónica en minúsculas**: El repo migró a `https://github.com/Ntizar/mastermind.git` (minúsculas). Usar esta forma para evitar warnings.
- **Copia segura con `cp -n`**: Siempre usar `cp -n` para preservar archivos exclusivos de Hermes.

## Mantenimiento

### Sincronizar skills del repositorio

```bash
cd /root/workspace/Mastermind && git pull origin main
cp -n /root/workspace/Mastermind/mastermind/*.md /hermes-home/skills/mastermind/
```

### Auto-prune de sesiones

Desde 2026-06-03:
```yaml
# En /hermes-home/config.yaml
sessions:
  auto_prune: true           # ← ACTIVADO
  retention_days: 60         # ← 60 días (antes 90)
  vacuum_after_prune: true
  min_interval_hours: 24
```

Esto limpia automáticamente sesiones >60 días. La DB de state.db se mantiene bajo control sin intervención manual.

### Regenerar índice de notas

```bash
cd /root/workspace/Mastermind && python3 scripts/generate-notes-index.py
```

Esto escanea `notes/` y genera `notes/INDEX.md` con tabla agrupada por categorías. Ejecutar tras crear/modificar notas.

### Verificar skill priority

Cuando añadas skills nuevos, añadirlos a la categoría correspondiente (HIGH/MEDIUM/LOW) en `config/skill-priority.json`.

**IMPORTANTE:** ChromaDB es la fuente de verdad para relevancia de skills. El JSON es un fallback estático. Para conciliar el JSON con el filesystem real, ver `references/skill-priority-reconciliation.md`.

**Cron semanal:** `chromadb-reindex-semanal` (domingo 04:00 UTC) re-indexa todos los skills en ChromaDB. Verificar que tiene `last_status: "ok"` y `last_run_at` reciente — un cron enabled pero nunca ejecutado es deuda técnica.

### Añadir un nuevo skill al repositorio

1. Crear archivo en `mastermind/<name>.md` con frontmatter correcto
2. Actualizar `mastermind/SKILL.md` umbrella
3. Copiar a `/hermes-home/skills/mastermind/`
4. Commit y push
5. Actualizar SOUL.md si es un skill core

### Actualizar SOUL.md

Cada vez que cambie el stack (nuevo modelo, dashboard, API), actualizar SOUL.md. Es el manual operativo del agente.

## Patrón de Sub-Skill (refs adjuntos)

Para skills que importan de repos de GitHub, usar el patrón de **sub-skill con refs**:

```
skills/<nombre>/
├── SKILL.md              ← Resumen corto (~1-2KB) — carga siempre
└── references/
    ├── patron-clave.md   ← Patrón de código o procedimiento extraído del repo
    ├── otro-patron.md    ← Otro patrón clave
    └── ...
```

**Cómo funciona:**
1. SKILL.md contiene resumen + tabla de refs disponibles
2. Los refs se cargan bajo demanda: `skill_view(name='nombre', file_path='references/patron.md')`
3. El contenido viene del repo real
4. Costo: ~1-2KB siempre + ~3KB por ref

**Cuándo usar:** Skills de repos externos con valor educativo, cuando el skill necesita código real, cuando el repo tiene patrones repetibles.
**No usar para:** Skills propios del sistema Mastermind, skills con un solo procedimiento, skills de menos de 1000 estrellas.
**Ejemplo creado:** `google-eng-practices` con 3 refs.

## SOUL.md Architecture (ACTUALIZADO 2026-06-01)

SOUL.md y `agente-principal.md` son **complementarios, no duplicados**:
## Arquitectura SOUL.md (ACTUALIZADO 2026-06-01)

SOUL.md y `agente-principal.md` son **complementarios, no duplicados**:

- `SOUL.md` (~3-4 KB): Identidad breve, reglas, stack, pitfalls críticos
- `agente-principal.md` (~3 KB): Manual operativo detallado (repo structure, subagentes, seguridad)

**Reglas:**
- SOUL.md: sin tablas (Telegram no las soporta), usar listas `**clave** → valor`
- SOUL.md: sección `## Identidad` breve (nombre, usuario, TTS, CSS, idioma)
- SOUL.md: sección `## Capas de conocimiento` como lista, no tabla
- SOUL.md: pitfall section con los errores más críticos del sistema
- `agente-principal.md`: extiende con detalles operativos
- **NUNCA duplicar el mismo contenido en ambos archivos**

## Patrón de Autoauditoría

Cuando el usuario pida "autoauditar" o cuestione si el sistema funciona bien, ejecutar este check rápido:

### 1. SOUL.md integrity
```bash
wc -c /hermes-home/SOUL.md  # Debe ser >1000 bytes
diff /hermes-home/SOUL.md /root/workspace/Mastermind/mastermind/SOUL.md  # Deben ser idénticos
```

### 2. Config correctness
```bash
grep "voice:" /hermes-home/config.yaml | head -1   # Debe ser es-ES-AlvaroNeural
grep "language:" /hermes-home/config.yaml           # display section debe ser 'es'
grep "provider:" /hermes-home/config.yaml | head -1 # Debe ser 'edge' para TTS
```

### 3. Skills health
```bash
# Skills sin tags (debería ser 0)
find /hermes-home/skills -name "SKILL.md" -exec sh -c 'if head -1 "$1" | grep -q "^---"; then if ! head -10 "$1" | grep -q "^tags:"; then echo "NO TAGS: $1"; fi; fi' _ {} \;

# Skills sin versión (debería ser 0)
find /hermes-home/skills -name "SKILL.md" -exec sh -c 'if head -1 "$1" | grep -q "^---"; then if ! head -10 "$1" | grep -q "^version:"; then echo "NO VERSION: $1"; fi; fi' _ {} \;
```

### 4. Memory pressure
```bash
# Si memoria >85%, Considerar podar entradas obsoletas
wc -c /hermes-home/SOUL.md
```

### 5. Cron jobs status
```bash
hermes cron list  # Todos deben mostrar last_status: ok
```

**Frecuencia:** Cuando el usuario lo pida o cada ~2 semanas como mantenimiento preventivo.

## Patrón de Auditoría de Librería

Cuando el sistema de skills necesita mantenimiento, cargar el skill `skill-audit-pattern` para ejecutar la auditoría sistemática. El script `scripts/audit-skills.py` hace un análisis completo.

**Objetivo:** 10/10 checks pasados = 5 estrellas.

### Filtro para Crear Nuevos Skills

1. **¿Es un patrón reutilizable?** → Si es específico de un proyecto → NO es skill
2. **¿Aporta algo nuevo?** → Si solo documenta un CLI tool → NO es skill
3. **¿Es compacto?** → Si es >5KB → usar refs pattern
4. **¿Tiene tags?** → Mínimo 3 tags descriptivos
5. **¿Es necesario?** → Si ya existe un skill similar → fusionar

### Criterios de Calidad

- ✅ **Patrón reutilizable** — Patrón, procedimiento o metodología aplicable a múltiples proyectos
- ❌ **Project README** — Documenta un proyecto específico → va a `notes/`
- ❌ **CLI Wrapper** — Solo documenta cómo usar una CLI → no aporta valor
- ⚠️ **Fragmentado** — Cubre un tema pero podría fusionarse

## Skill Learning Script (`skill-learning.sh`)

Script automatizado que instala skills del hub uno a uno, avanzando un índice en `.skill-learning-state.json`.

### Estado del script

- **State file:** `/hermes-home/skills/.skill-learning-state.json`
- **Log:** `/hermes-home/skills/skill-learning.log`
- **Script:** `/hermes-home/scripts/skill-learning.sh`
- **Total skills en cola:** 118 (lista en `PRIORITY_SKILLS` del script)

### Pitfalls críticos del script

- **State desincronizado con disco:** El estado JSON puede marcar un skill como "learned" pero el archivo NO existe en `/hermes-home/skills/`. **Siempre verificar con `find`:**
  ```bash
  for skill in duckduckgo-search searxng-search scrapling code-wiki; do
    find /hermes-home/skills -name "SKILL.md" -path "*$skill*" -not -path "*/quarantine/*"
  done
  ```
- **Quarantine = instalación fallida:** Si un skill aparece en `.hub/quarantine/`, la instalación falló y el script seguirá reintentando infinitamente. **Solución:** eliminar de quarantine y dejar que el script lo intente de nuevo, o saltar a la siguiente skill.
- **Timeout en `hermes skills install`:** El script tiene timeout de 120s. Si la instalación tarda más, el script falla pero el state no avanza (el skill se reintentará en la siguiente ejecución). **Verificar:** `grep "Installing" /hermes-home/skills/skill-learning.log | tail -5`
- **Reintentos infinitos en skills de quarantine:** Si un skill está en quarantine, el script lo reintentará cada tick sin fin. **Solución manual:**
  ```bash
  # Verificar si está en quarantine
  ls /hermes-home/skills/.hub/quarantine/
  # Si es un skill problemático, eliminarlo y avanzar el índice manualmente
  rm -rf /hermes-home/skills/.hub/quarantine/<skill-name>
  python3 -c "
  import json
  with open('/hermes-home/skills/.skill-learning-state.json') as f:
      data = json.load(f)
  data['current_index'] = data['current_index'] + 1
  with open('/hermes-home/skills/.skill-learning-state.json', 'w') as f:
      json.dump(data, f, indent=2)
  "
  ```
- **Índice se reinicia:** Si el state file se pierde o corrompe, el script vuelve al índice 0 e instala los mismos skills de nuevo. **Backup:** el log es la fuente de verdad del progreso real.

### Verificación rápida de progreso

```bash
# Estado actual
cat /hermes-home/skills/.skill-learning-state.json

# Últimos 5 intentos
tail -10 /hermes-home/skills/skill-learning.log

# Skills realmente instalados vs state
python3 -c "
import json, os, subprocess
with open('/hermes-home/skills/.skill-learning-state.json') as f:
    state = json.load(f)
installed = []
for skill in state.get('learned', []):
    result = subprocess.run(['find', '/hermes-home/skills', '-name', 'SKILL.md', '-path', f'*{skill}*'], capture_output=True, text=True)
    if result.stdout and 'quarantine' not in result.stdout:
        installed.append(skill)
    else:
        print(f'MARKED BUT NOT INSTALLED: {skill}')
print(f'Installed: {len(installed)}/{len(state.get(\"learned\", []))}')
"
```

### Troubleshooting completo

Para troubleshooting detallado (state desincronizado, quarantine infinito, timeouts), ver `references/skill-learning-troubleshooting.md`.

## Notas

- Este skill consolida el skill `mastermind-system` de devops. Usar este para todas las tareas de setup/mantenimiento de Mastermind.
- El cron job `cf21b05773aa` (mastermind-autoconfig) se ejecuta diariamente a las 09:00 UTC.
- SOUL.md en `/hermes-home/SOUL.md` es la fuente de identidad del agente — mantenerlo siempre sincronizado con el repo.
- Para monitoreo y observabilidad después del setup, ver el skill `agent-observability` → `references/nan-portfolio-pattern.md`.
- Dashboard de control completo: `/root/workspace/mastermind_control_center.py` — dashboard completo con kanban, gráficos, acciones y auth. Ejecutar con `python3 mastermind_control_center.py [puerto]`.
- Para portfolio de apps en NaN Spaces, ver `agent-observability` → `references/nan-portfolio-pattern.md`.
- Para integración Apple Calendar / iCloud CalDAV, ver skill `caldav-calendar`.
- **2026-06-01:** Auditoría completa de librería. 205 → 150 skills (eliminados 55: 12 project-readmes + 25 CLI wrappers + 18 top-level project-readmes + 2 others). 100% skills con tags. 27 categorías. Skill `skill-audit-pattern` creado + cron `skill-maintenance` (83139c479ddb) para auditorías mensuales.
- **2026-06-03:** Autoauditoría del sistema. Fix: SOUL.md restaurado (3591 bytes), TTS voice corregido a `es-ES-AlvaroNeural`, display.language a `es`, 7 skills sin tags/versión arreglados, `mastermind-autoconfig.sh` mejorado con guard robusto (MIN_SOUL_SIZE=1000, lógica 3 vías). Añadido patrón de autoauditoría al skill. Pitfall de config drift documentado.
- **2026-06-06:** Script `skill-learning.sh` — documentados pitfalls de state desincronizado, quarantine infinito y timeout. Verificar progreso real con `find` vs state JSON. Añadido `references/skill-learning-troubleshooting.md` con troubleshooting completo.
- **2026-06-10:** `skill-priority.json` reconciliado con filesystem: 192 skills (antes 141, 34 stale eliminados, 85 nuevos añadidos). Distribución: HIGH 34, MEDIUM 86, LOW 72. Procedimiento capturado en `references/skill-priority-reconciliation.md`. ChromaDB actualizado a 192 skills indexados.
- **2026-06-20:** Backup completo del sistema. Se descubrió que solo los skills estaban en GitHub (244/245), pero config.yaml, memories/, notes/, scripts/ NO estaban. Se creó `hermes-backup/` en el repo con todo lo crítico + cron de auto-sync cada 6h. Procedimiento capturado en `references/backup-hermes-complete.md`. **Pitfalls nuevos:** `cp -r` crea rutas duplicadas (usar `cp -rT` o `cp -r src/* dest/`), `skill-learning.log` está en `.gitignore` (necesita `git add -f`), 7 skills metadata con solo `DESCRIPTION.md` no cuentan en conteo SKILL.md.
- **2026-06-21:** Backup cron automatizado. **Pitfall nuevo:** `.hub/quarantine/` contiene skills en cuarentena que NO deben copiarse al repo. Al comparar conteos de SKILL.md entre hermes y repo, excluir `.hub/` del conteo. La diferencia de 1 skill (245 vs 244) es `.hub/quarantine/fastmcp` — ignorar. Procedimiento exacto: `find /hermes-home/skills/ -name 'SKILL.md'` vs `find /root/workspace/Mastermind/skills/ -name 'SKILL.md'`, luego `comm -23` para encontrar faltantes. Excluir `.hub/` del diff.
- **2026-06-22:** Backup pitfall critico: `cp` de directorios con destino existente crea **doble nesting** (`/dest/memories/memories/`). Si el repo ya tiene una carpeta `hermes-backup/memories/`, `cp -r /hermes-home/memories/ /dest/hermes-backup/memories/` duplica la ruta. **Solucion:** antes de copiar, verificar si el destino existe; si existe, hacer `git reset --hard` al ultimo commit limpio, borrar `hermes-backup/` del disco, y copiar desde cero. **Otra solucion:** usar `cp -rT source/ dest/` (la T evita el nesting extra). **Pitfall en git:** los commits duplicados generan historial sucio — usar `git reset --hard <commit-limpio>` + force push para limpiar. **Pitfall adicional:** antes de hacer backup, SIEMPRE comparar conteo de SKILL.md entre hermes y repo — si el repo tiene MAS skills, no hay nada que copiar (el repo puede estar mas actualizado).
- **2026-06-23:** Backup pitfall recurrente: si el repo ya tiene `hermes-backup/` con doble nesting de sesiones anteriores, los nuevos `cp` crean `notes/notes/` y `memories/memories/`. **Fix automático:** antes de `git add`, limpiar directorios anidados: (1) mover archivos de `hermes-backup/notes/notes/` → `hermes-backup/notes/`, (2) mover archivos de `hermes-backup/memories/memories/` → `hermes-backup/memories/`, (3) eliminar `.lock` files, (4) verificar estructura plana con `find hermes-backup/ -type f | head -20`. **Prevention:** siempre hacer `rm -rf hermes-backup/` antes de copiar desde cero, o usar `cp -rT` en lugar de `cp -r`.

- **2026-06-26:** Backup pitfall: **rsync NO está disponible en la VM** de NaN. Si se pide usar `rsync`, hay que hacer fallback a Python con `shutil.copy2()` + `filecmp.cmp()` para solo copiar archivos nuevos/cambiados. Ver script de fallback en `references/backup-rsync-fallback.md`.

- **2026-06-26:** Backup pitfall: **branch divergence `main` vs `master`**. El repo tiene ambas ramas. El auto-backup cron escribe en `origin/main`, pero el backup manual suele hacer push a `origin/master`. **Solución:** hacer `git fetch origin` → `git reset --hard origin/main` → rebase de commits locales → `git push origin main:master` para sincronizar ambas ramas. No intentar `git push origin main` si el remote main tiene commits que el local no tiene (non-fast-forward).

- **2026-06-27:** Backup pitfall: **`cp -a` (archive) tiene el mismo doble nesting que `cp -r`**. `cp -a /source/ /dest/` cuando `/dest/` existe produce `/dest/source/`. **Solución OBLIGATORIA:** `rm -rf /dest/` antes de copiar. **Nuevo en este backup:** 1148 skills, 33 notes, 167 scripts.

- **2026-06-27:** **Estructura de destino actualizada:** El backup usa `hermes-home/` como prefijo plano en el repo, NO `hermes-backup/`. Rutas: `hermes-home/skills/`, `hermes-home/memories/`, `hermes-home/notes/`, `hermes-home/scripts/`, `hermes-home/config.yaml`. Esto reemplaza el patrón anterior de `hermes-backup/` (2026-06-20). La ventaja: el prefijo `hermes-home/` refleja la estructura real de `/hermes-home/` sin la capa intermedia `hermes-backup` que generaba confusión.

- **2026-06-27:** **Push workflow con branch divergence:** `git push origin HEAD` puede fallar con "non-fast-forward" si el remote tiene commits locales no tienen. **Patrón correcto:** `git pull --rebase origin main` → `git push origin HEAD` (si el remote está en `main`) o `git push origin HEAD:master` (si el remote usa `master`). Si el rebase reporta "skipped previously applied commits", eso es normal (commits ya estaban en remote). Siempre verificar con `git log --oneline -3` después del push.

- **2026-06-27:** **`git add -A` detecta renames automáticamente:** Cuando se corrige doble nesting (ej. `memories/memories/` → `memories/`), `git add -A` detecta los cambios como renames (100%) si el contenido no ha cambiado. Esto produce un commit limpio con `rename hermes-home/memories/{memories => }/INDEX.yaml (100%)`. No es necesario renombar manualmente — git lo resuelve solo.

- **2026-06-27:** **Diff-before-copy para actualizaciones selectivas:** En backups donde el repo ya tiene los archivos (solo algunos cambiaron), NO hay que copiar todo — usar `diff -rq` para comparar y solo copiar los archivos con cambios. Esto reduce tiempo, evita doble nesting innecesario y el commit queda más limpio. Patrón: `diff -rq /hermes-home/notes/ /root/workspace/Mastermind/hermes-home/notes/ | grep -v "IGUAL" | wc -l`. Si el resultado es 0, no copiar. **Optional files:** `INDEX.md` y `STEM-INDEX.md` pueden no existir en `/hermes-home/` — el backup debe omitirlos sin error (son generados). **Config check:** `config.yaml` y `SOUL.md` ya estaban actualizados en el repo tras el autoconfig cron — verificar con `diff` antes de hacer backup completo.

- **2026-06-28:** **Cascading nesting bug (CRÍTICO):** Cuando se corrige el nesting raíz (`skills/skills/` → `skills/`), **CADA categoría top-level** tiene el mismo patrón anidado dentro: `ai-patterns/ai-patterns/`, `creative/creative/`, `stem/stem/`, etc. — **70+ directorios anidados**. `cp -a /hermes-home/skills/ /dest/skills/` produce nesting a DOS niveles: primero en la raíz (`skills/skills/`), luego dentro de CADA categoría. **Solución en dos pasos:** (1) Borrar nesting raíz: `rm -rf skills/skills/` y mover contenido arriba. (2) Loop sistemático para TODAS las categorías: `find . -mindepth 2 -maxdepth 2 -type d | while read dir; do parent=$(basename "$(dirname "$dir")"); child=$(basename "$dir"); if [ "$parent" = "$child" ]; then mv "$dir"/* "$dir"/.* . 2>/dev/null; rm -rf "$dir"; fi; done`. **Verificación post-fix:** `find . -mindepth 2 -maxdepth 2 -type d | while read dir; do parent=$(basename "$(dirname "$dir")"); child=$(basename "$dir"); if [ "$parent" = "$child" ]; then echo "STILL NESTED: $dir"; fi; done` — debe devolver vacío.

- **2026-06-29:** **Backup con hermes-home/ + cp -r = nesting triple (CRÍTICO):** Cuando el repo YA tiene hermes-home/skills/, hermes-home/memories/, hermes-home/notes/ (del backup anterior), hacer cp -r /hermes-home/skills/ /repo/hermes-home/skills/ produce skills/skills/. Y cp -r /hermes-home/memories/ /repo/hermes-home/memories/ produce memories/memories/. **Solución en 3 pasos:** (1) Hacer rsync -av (NO cp -r) — rsync maneja destinos existentes correctamente, sobrescribe sin duplicar. (2) Después de rsync, verificar nesting: find hermes-home/ -mindepth 2 -maxdepth 2 -type d -exec sh -c 'p=$(basename "$(dirname "$1")"); c=$(basename "$1"); [ "$p" = "$c" ] && echo "NESTED: $1"' _ {} \; — debe devolver vacío. (3) Si hay nesting residual, limpiar con el loop cascading de arriba. **IMPORTANTE:** rsync -av SIN --delete es seguro para backup incremental. rsync -av --delete elimina archivos que ya no existen en origen — solo usar si se quiere espejo exacto.

- **2026-06-29:** **Patrón confirmado sin rsync:** rm -rf /dest/ + cp -a /source/ /dest/ es el patrón que funciona de verdad cuando rsync no está disponible. rm -rf elimina el destino existente, luego cp -a copia todo desde cero sin nesting. Más rápido y fiable que Python fallback para directorios grandes. Ver references/backup-rsync-fallback.md.

- **2026-06-30:** **rsync está completamente roto (no solo ausente):** `libpopt.so.0 => not found` en runtime. `ldd /usr/bin/rsync` confirma `libpopt.so.0 => not found`. Instalar `libpopt0` no lo arregla. **NUNCA intentar arrancar rsync** — ir directo al fallback con `cp -rf` + glob `*` o `rm -rf` + `cp -a`.
- **2026-06-30:** **Push con `git push origin HEAD:master`:** Si el remote usa `master` como branch principal (no `main`), `git push origin HEAD` puede fallar con "non-fast-forward" o "upstream branch mismatch". **Patrón correcto:** `git push origin HEAD:master`. Verificar siempre con `git remote -v` y `git log --oneline -3` después.
- **2026-06-30:** **Nuevo patrón sin rsync: `cp -rf` con glob `*`.** `cp -rf /hermes-home/skills/* /dest/skills/` copia el CONTENIDO del directorio sin nesting (el glob expande los archivos, no la carpeta). Más corto que `rm -rf` + `cp -a`. Confirmado funcionando con 1187 skills y 2452 archivos.
