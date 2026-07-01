# Backup Completo del Sistema Hermes

**Creado:** 2026-06-20  
**Contexto:** El usuario pidió "guardar todo en mastermind" para no perder nada si Hermes se cae. Se descubrió que solo los skills estaban en GitHub, pero config.yaml, memories/, notes/, scripts/ NO.

## Problema Descubierto

Al auditar la vulnerabilidad del sistema:
- **Skills:** 245 en `/hermes-home/skills/` → 244 en GitHub ✅
- **NOTAS:** 25 en `/hermes-home/notes/` → solo 6 en GitHub ❌
- **CONFIG:** `config.yaml` (200+ líneas) NO en GitHub ❌
- **MEMORIES:** `memories/MEMORY.md` (9 entradas) y `USER.md` (perfil) NO en GitHub ❌
- **SCRIPTS:** 167 scripts NO en GitHub ❌

## Patrón de Backup Completo

### Paso 1: Vulnerability Assessment

Comparar `/hermes-home/` con `/root/workspace/Mastermind/` para identificar qué NO está en GitHub:

```python
import os

hermes_items = {}
for item in os.listdir('/hermes-home'):
    path = f'/hermes-home/{item}'
    if os.path.isfile(path):
        hermes_items[item] = os.path.getsize(path)
    elif os.path.isdir(path):
        total = sum(os.path.getsize(os.path.join(dp, f)) 
                    for dp, dn, files in os.walk(path) for f in files)
        hermes_items[item] = total

repo_items = {}
for item in os.listdir('/root/workspace/Mastermind'):
    path = f'/root/workspace/Mastermind/{item}'
    if os.path.isfile(path):
        repo_items[item] = os.path.getsize(path)
    elif os.path.isdir(path):
        total = sum(os.path.getsize(os.path.join(dp, f)) 
                    for dp, dn, files in os.walk(path) for f in files)
        repo_items[item] = total

# Comparar
for item in hermes_items:
    if item not in repo_items:
        size_kb = hermes_items[item] / 1024
        print(f"❌ {item:40s} {size_kb:8.0f} KB (NO EN REPO)")
```

### Paso 2: Copiar Archivos Críticos

**Qué SÍ copiar:**
```
/hermes-home/config.yaml          → hermes-backup/config.yaml
/hermes-home/memories/            → hermes-backup/memories/
/hermes-home/notes/               → hermes-backup/notes/
/hermes-home/scripts/             → hermes-backup/scripts/
/hermes-home/skills/INDEX.md      → hermes-backup/INDEX.md
/hermes-home/skills/STEM-INDEX.md → hermes-backup/STEM-INDEX.md
/hermes-home/skills/skill-learning.log → hermes-backup/skill-learning.log
```

**Qué NO copiar (caches regenerables):**
```
/hermes-home/.env          → secrets (correcto no subir)
/hermes-home/chromadb-data → se regenera con indexar-skills.py
/hermes-home/chromadb-venv → se recrea con pip install
/hermes-home/sessions/     → solo historial de conversaciones
/hermes-home/cache/        → caches
/hermes-home/lsp/          → language server cache
/hermes-home/webui/        → UI cache
/hermes-home/audio_cache/  → se regenera con TTS
/hermes-home/logs/         → logs
/hermes-home/profiles/     → perfiles TTS
/hermes-home/models_dev_cache.json → cache de modelos
```

### Paso 3: Commit + Push

```bash
cd /root/workspace/Mastermind
git add hermes-backup/
git commit -m "🛡️ Backup completo de Hermes: config, memories, scripts, notes"
git push origin master
```

### Paso 4: Crear README de Recuperación

Crear `hermes-backup/README.md` con:
- Guía paso a paso para recuperar si Hermes se cae
- Tabla de estado: X skills en Hermes, Y en GitHub
- Lista de archivos críticos y su ubicación

### Paso 5: Configurar Auto-Sync

Cron job cada 6h que:
1. Copia config.yaml, memories/, scripts/, notes/ al repo
2. Compara conteo de skills entre Hermes y GitHub
3. Copia skills faltantes si es necesario
4. Commit + push

## Archivos Críticos Detallados

### config.yaml (8.6 KB)
Contiene:
- Modelo: qwen3.6 vía NaN.builders
- TTS: Edge (es-ES-AlvaroNeural)
- STT: Local
- Cron jobs, toolsets, gateways
- Integraciones (Telegram, Discord, Slack)
- Configuración de delegación, compression, security
- **200+ líneas** — si se pierde, todo el sistema se desconfigura

### memories/MEMORY.md (1.9 KB)
Contiene:
- 9 entradas de memoria persistente
- Reglas críticas (no crear repos sin verificar, nombres sensibles)
- Estado de proyectos activos (wave3, nogal9, timeineco)
- Estado de stars-explorer (117 repos, 27 procesados)
- ChromaDB status (261 skills indexados)

### memories/USER.md (1.3 KB)
Contiene:
- Perfil de David: edad (36), nombre (Ntizar)
- CSS: azul #2563eb + naranja #f97316, fondo CLARO
- TTS: voz Álvaro (es-ES-AlvaroNeural)
- Estilo: español tuteo, informal, cercano
- Atribución: "Hecho con ❤️ por David Antizar"

### scripts/ (7.8 MB, 167 archivos)
Contiene:
- `consultar-skills.py` — consulta ChromaDB
- `indexar-skills.py` — indexa skills en ChromaDB
- `start-chromadb.sh` — arranque de ChromaDB
- `backup-hermes-memory.sh` — backup manual
- `bicimad-alert.py` — alertas bicimad
- `control-m/` — reports de control-m
- `mastermind-weekly-maintenance.sh` — mantenimiento semanal
- Y 150+ scripts más...

### notes/ (25 archivos)
Contiene:
- Notas de sesiones y auditorías
- Análisis de aprendizaje (deep-learning)
- Formato: `YYYY-MM-DD-titulo.md`

## Verificación Post-Backup

```bash
# Verificar que todo está en GitHub
cd /root/workspace/Mastermind
echo "Skills: $(find skills -name SKILL.md | wc -l)"
echo "Config: $(test -f hermes-backup/config.yaml && echo ✅ || echo ❌)"
echo "Memories: $(test -f hermes-backup/memories/MEMORY.md && echo ✅ || echo ❌)"
echo "Notes: $(find hermes-backup/notes -name '*.md' | wc -l)"
echo "Scripts: $(find hermes-backup/scripts -type f | wc -l)"

# Verificar que el push fue exitoso
git log --oneline -3
```

## Pitfalls Descubiertos (2026-06-20)

### cp -r crea rutas duplicadas
`cp -r /hermes-home/memories/ /dest/memories/` crea `/dest/memories/memories/` (doble nesting).
**Solución:** `cp -r /hermes-home/memories/* /dest/memories/` o `cp -rT /hermes-home/memories/ /dest/memories/`.
Lo mismo aplica para `notes/`, `scripts/`, etc.

### skill-learning.log está en .gitignore
El archivo `skill-learning.log` está en el `.gitignore` del repo. Se necesita `git add -f` para forzarlo.
**Solución:** `git add -f hermes-backup/skill-learning.log`

### Metadata skills con DESCRIPTION.md
Algunos skills del sistema solo tienen `DESCRIPTION.md`, no `SKILL.md`. No cuentan en el conteo de SKILL.md.
**Ejemplos:** diagramming, domain, email, inference-sh, note-taking, smart-home, social-media.
Al comparar conteos, la diferencia puede ser estos skills metadata.

### 7 skills metadata copiados (2026-06-20)
Se copiaron 7 directorios nuevos al repo: diagramming, domain, email, inference-sh, note-taking, smart-home, social-media.
Todos tienen solo `DESCRIPTION.md` (no `SKILL.md`). Son metadata de skills, no ejecutables.
El conteo de SKILL.md sigue siendo 245 (hermes) vs 244 (repo) — la diferencia es `.curator_backups`.

## Comparación de Skills (2026-06-21)

Al comparar conteo de SKILL.md entre hermes y repo:

```bash
# Contar SKILL.md en hermes (excluyendo .hub/quarantine/)
HERMES_SKILLS=$(find /hermes-home/skills/ -name 'SKILL.md' -type f 2>/dev/null | wc -l)

# Contar SKILL.md en repo
REPO_SKILLS=$(find /root/workspace/Mastermind/skills/ -name 'SKILL.md' -type f 2>/dev/null | wc -l)

# Encontrar faltantes (excluyendo .hub/)
HERMES_LIST=$(find /hermes-home/skills/ -name 'SKILL.md' -type f 2>/dev/null | sed 's|/hermes-home/skills/||;s|/SKILL.md||' | sort)
REPO_LIST=$(find /root/workspace/Mastermind/skills/ -name 'SKILL.md' -type f 2>/dev/null | sed 's|/root/workspace/Mastermind/skills/||;s|/SKILL.md||' | sort)
MISSING=$(comm -23 <(echo "$HERMES_LIST") <(echo "$REPO_LIST"))

# Filtrar .hub/quarantine/ del diff
MISSING_CLEAN=$(echo "$MISSING" | grep -v '^\.hub/' || true)
```

**Regla:** `.hub/quarantine/` se excluye del conteo. Si la única diferencia es un skill en `.hub/quarantine/`, está OK — no hay nada que copiar.

**Pitfall:** Si `comm -23` muestra skills que NO están en `.hub/quarantine/`, hay que copiarlos al repo antes del commit.
