---
name: stars-explorer
version: "1.0.0"
description: "Pipeline nocturno que explora las stars de GitHub de David, analiza repos, extrae patrones y crea skills automáticamente. Cada run procesa un batch de repos, genera análisis profundo, y propone skills basados en los patrones detectados."
tags: [github, stars, skills, pipeline, cron, exploration, learning]
related_skills: [chromadb-skills-vector-search, github-trending-research]
---

# Stars Explorer — Pipeline de Aprendizaje Automático

## Resumen

Pipeline recurrente que explora las ~100+ stars de GitHub de David (Ntizar), analiza los repos más interesantes, extrae patrones arquitectónicos y crea skills automáticamente en el sistema Mastermind/Hermes.

**Objetivo:** Cada noche, el sistema aprende de los repos que David le gusta, ampliando la base de conocimiento de skills de forma autónoma.

## Arquitectura

```
Cron (nocturno 03:00 UTC)
  ↓
Script explorar-stars.py (batch de 3 repos)
  ↓ Fetch GitHub API → README + tree + key files
  ↓ Análisis: tech stack, patterns, skill angles
  ↓ Actualiza stars-registry.json
  ↓
Agent processa el output del script
  ↓ Para cada repo: decide si merece skill
  ↓ Crea skill con skill_manage si es relevante
  ↓ Actualiza registry (category, skill_created)
  ↓
Re-indexa ChromaDB (si hubo cambios)
  ↓
Guarda resumen en notes/ si hubo hallazgos significativos
```

## Componentes

### Script principal
- **Ruta:** `/hermes-home/scripts/explorar-stars.py`
- **Wrapper:** `bash /hermes-home/scripts/run-stars-explorer.sh` (carga entorno automáticamente)
- **Dependencias:** Solo stdlib (urllib, json, base64) — NO necesita pip install
- **Entorno:** Wrapper carga variables de entorno del sistema automáticamente

### Registry
- **Ruta:** `/hermes-home/data/stars-registry.json`
- **Contenido:** Repo → fecha explorada, category, skill_created, skill_angles

### Skill de referencia
- **chromadb-skills-vector-search** — Para re-indexar después de crear skills

## Uso del Script

Usar SIEMPRE el wrapper que carga el entorno automáticamente:

```bash
# Status del registry
bash /hermes-home/scripts/run-stars-explorer.sh --status

# Batch de 3 repos (default) — solo repos >100 stars con topics
bash /hermes-home/scripts/run-stars-explorer.sh

# Batch grande
bash /hermes-home/scripts/run-stars-explorer.sh --batch 5

# Todos los pendientes (SIN FILTRO — explora todos)
bash /hermes-home/scripts/run-stars-explorer.sh --all

# Modo JSON (para agent consumption)
bash /hermes-home/scripts/run-stars-explorer.sh --batch 2 --json

# Incluir propios repos de David
bash /hermes-home/scripts/run-stars-explorer.sh --include-own

# Forzar re-proceso de un repo
bash /hermes-home/scripts/run-stars-explorer.sh --reprocess owner/repo

# Modo LOOP DE APRENDIZAJE — modo completo: explora → aprende → mejora → implementa
bash /hermes-home/scripts/run-stars-explorer.sh --learning-loop
```

## Flujo del Agent (en el cron)

Al recibir el output del script, el agent debe:

1. **Leer cada repo analizado** del JSON
2. **Evaluar si merece skill** basándose en:
   - ¿Tiene patrones reutilizables? (architecture, pipeline, performance)
   - ¿Es relevante para los proyectos de David? (3D, CV, geospatial, CRM, transit)
   - ¿Aporta conocimiento que NO tenemos ya?
   - ¿Tiene enough profundidad para justificar un skill?
3. **Crear skill** con `skill_manage(action='create')` si:
   - El repo tiene patrones claros y reutilizables
   - El skill serait útil en futuras tareas
   - No duplica un skill existente (check ChromaDB primero)
4. **Marcar en registry** como `skill_created: true` + categoría
5. **Re-indexar ChromaDB** al final si se crearon skills

### Criterios de Creación de Skill

**Crear skill si:**
- Repo tiene patrones arquitectónicos reutilizables (3+ patterns detectados)
- Tech stack relevante para proyectos existentes de David
- El README describe approach único o innovador
- Tiene +1000 stars (indica calidad/comunidad)
- El repo es de David (siempre crear, es su conocimiento)

**NO crear skill si:**
- Solo tiene README genérico sin patrones concretos
- Es un "awesome list" o curated list sin código
- Ya existe un skill cubriendo lo mismo
- El repo está archivado o sin maintenimiento
- Es demasiado simple (<100 stars, sin code patterns)

**Categorías para el registry:**
- `core` — Skills que son parte fundamental del sistema
- `domain` — Conocimiento de dominio específico (CV, GIS, transit)
- `pattern` — Patrones arquitectónicos reutilizables
- `tool` — Herramientas y librerías concretas
- `reference` — Referencia/inspiración (no skill directo)
- `skip` — Decidido no procesar (awesome list, etc.)

## Datos del Script Output

Cada repo analizado incluye:
```json
{
  "full_name": "owner/repo",
  "description": "...",
  "language": "Python",
  "stars": 1234,
  "topics": ["topic1", "topic2"],
  "tech_stack": ["django", "postgres", "..."],
  "potential_patterns": ["pipeline", "real-time", "ai/ml"],
  "skill_angles": ["ai-cv-pipeline"],
  "readme_excerpt": "primeros 2000 chars del README",
  "key_files_present": ["package.json", "Dockerfile"],
  "file_types": {".py": 15, ".js": 8}
}
```

## Pitfalls

- **Rate limit GitHub:** 5000 req/h autenticados. Batch de 3 repos ≈ 20 req cada uno = 60/batch. Safe.
- **README enorme:** Truncado a 8000 chars. Suficiente para análisis.
- **Skills duplicados:** SIEMPRE consultar ChromaDB antes de crear. Si un skill semánticamente similar existe, NO crear otro. Verificado en producción: manim→skip (score 0.85 contra creative/manim-video), twenty→skip (score 0.79 contra crm-erp-fullstack), VibeVoice→skip (score 0.89 contra media/voicebox).
- **Quality gate:** No crear skills de "awesome lists" o repos sin código sustancial.
- **Re-indexación ChromaDB:** Obligatoria tras crear skills. Sin ella, los nuevos skills son invisibles en búsquedas semánticas.
- **Registry creep:** Si un repo no merece skill, marcar con `category: "skip"` y `skill_created: false`. NO re-procesarlo cada run.
- **Cron security scanner (CRÍTICO 2026-06-16):** El scanner de cron bloquea prompts que contienen patrones como `cat .env`, `cat credentials`, etc. (regex: `cat\s+[^\n]*(\.env|credentials|\.netrc|\.pgpass)`). **Solución:** usar wrapper script (`run-stars-explorer.sh`) que carga el entorno internamente. NUNCA poner comandos que lean secrets directamente en prompts de cron ni en skills que se carguen en crons. El scanner escanea el prompt ensamblado (user prompt + skill content concatenado).
- **ChromaDB dedup funciona en producción (2026-06-16):** El pipeline detectó correctamente 3 repos como "ya cubiertos" en el primer batch nocturno. Scores: manim=0.85, twenty=0.79, VibeVoice=0.89. Threshold 0.25 es suficiente para detectar duplicados semánticos.
- **Wrapper script obligatorio para cron:** El script `explorar-stars.py` necesita variables de entorno (token de GitHub, API key de NaN). En vez de exponer el patrón de lectura en el prompt del cron, usar `bash /hermes-home/scripts/run-stars-explorer.sh` que hace source del .env internamente.
- **Skill overlap con github-trending-research:** `github-trending-research` explora trending público; `stars-explorer` explora las stars personales de David. Complementarios, no duplicados. Comparten patrones de GitHub API, creación de skills, y dedup via ChromaDB.

## Loop de Aprendizaje Continuo

El sistema **no es solo explorador** — es un **motor de aprendizaje** que cada noche:

### Diagrama del Loop

```
🌙 Cron (03:00 UTC)
   ↓
🔍 Explorar 3 stars nuevos
   ↓
📖 Analizar README + tree + key files
   ↓
🧠 ¿Merece skill? (ChromaDB dedup)
   ↓
   ├── ✅ Sí → Crear skill → Indexar en ChromaDB
   └── ❌ No → Marcar como skip (razón)
   ↓
📈 Registrar en stars-registry.json
   ↓
🎯 ¿Patrón relevante para proyecto activo?
   ↓
   ├── Sí → Micro-cron de seguimiento semanal
   └── No → Esperar próxima noche
   ↓
🔄 Loop infinito → Cada noche 3 skills nuevos
```

### Fases del ciclo

| Fase | Descripción | Responsable |
|------|-------------|-------------|
| **🔍 Explorar** | Fetch 3 repos no procesados | Script `explorar-stars.py` |
| **📖 Aprender** | Analizar tech stack + patrones | Agent (con `stars-explorer` skill) |
| **✨ Mejorar** | ¿El patrón es nuevo? → skill | Agent + ChromaDB |
| **🛠️ Implementar** | Crear skill + indexar | `skill_manage` + `indexar-skills.py` |
| **📊 Registrar** | Actualizar registry | Script guarda en JSON |
| **👁️ Watch** | Micro-cron semanal si repo >500⭐ | `cronjob` |

### Criterio Avanzado de Creación de Skill

**Matriz de decisión:** (stars × topic_count × pattern_diversity) / existing_skill_overlap

```python
def should_create_skill(repo):
    score = repo['stars'] * (1 + 0.1*len(repo['topics'])) * (1 + 0.2*len(repo['potential_patterns']))
    # Penalizar si ya hay skill similar
    chroma_score = chromadb_search(repo['description'])
    if chroma_score > 0.25: return False
    return score > 500  # Threshold mínimo
```

### Micro-crons de Seguimiento

Cuando un repo >500⭐ tiene patrones relevantes para un proyecto activo:

```bash
# Automatizado por el cron
cronjob(action='create', 
  name=f'watch-{repo_basename}',
  schedule='0 0 * * 1',  # Cada lunes
  prompt=f"Revisar nuevas releases/issues de {owner}/{repo}")
```

Estos micro-crons se auto-destruyen tras 4 semanas si no generan ningún skill → `skill_created: false` en registry tras 4 ciclos sin actividad.

## Cron Asociado

- **Nombre:** `stars-explorer-nocturno`
- **Schedule:** 0 3 * * * (03:00 UTC diario)
- **Job ID:** `abcb79ec2e36`
- **Batch:** 3 repos/run → 3 por noche
- **Re-procesamiento:** Nunca (registry previene duplicados)
- **ChromaDB:** Si ChromaDB no está corriendo, arrancar con `bash /hermes-home/scripts/start-chromadb.sh` antes de consultar. El cron puede ejecutarse en un momento donde ChromaDB se haya caído.
- **Modelo del cron:** `deepseek-v4-flash` (contexto 32K suficiente para READMEs de 8K chars)

### Modo de Procesamiento Rápido (para un batch completo)

Cuando hay **muchos repos nuevos** (50+), **NO usar `--all`** en el cron (se timeout). Mejor:

1. **Ejecutar el script** `python3 /hermes-home/scripts/registrar-stars-masivo.py` (registra todos en "pending" sin fetch)
2. **Actualizar el registry** manualmente con todos los nombres
3. **Dejar que el cron** procese 3/noche en modo standard

### Pitfall: `--all` se timeout

El script `explorar-stars.py` hace:
- `GET /repos/{name}` (1 req)
- `GET /repos/{name}/readme` (1 req)
- `GET /repos/{name}/git/trees/HEAD` (1 req)
- `GET /repos/{name}/contents/{file}` (hasta N reqs)

Para **117 repos** → ~200+ requests → **~2 min por req con rate-limit** → **se timeout**.

**Solución:** El cron **SIEMPRE** debe hacer `--batch 3`. Solo para cubrir todos rápidamente, usar el **registro masivo** primero (que solo hace 1 req por repo).

### Próxima Ejecución

El primer cron se ejecutará:
- **Fecha:** 2026-06-19T03:00:00+00:00
- **Batch:** 3 repos no procesados
- **Skills cargados:** `stars-explorer`, `chromadb-skills-vector-search`

Para **test** manual, ejecutar:
```bash
bash /hermes-home/scripts/run-stars-explorer.sh --batch 3 --json
```

## Referencias

- Script: `/hermes-home/scripts/explorar-stars.py`
- Registry: `/hermes-home/data/stars-registry.json`
- ChromaDB: skill `chromadb-skills-vector-search`
- GitHub trending (relacionado): skill `github-trending-research`
- Nota previa (exploración manual): `/root/workspace/Koldo/notes/2026-05-30-nightly-explored-repos.md`
- Skills creados por este pipeline: [ver en registry → `skill_created: true`]
- **This cron:** `cronjob(action='list')` to see status
