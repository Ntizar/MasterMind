---
name: github-trending-research
description: "Exploración sistemática de GitHub Trending — curl + regex parsing, API enrichment, cross-reference con Python scan de SKILL.md, creación/actualización de skills para repos relevantes"
version: "1.0.0"
author: Mastermind
tags: [github, trending, research, skills, discovery]
related_skills: [stars-explorer]
---

# GitHub Trending Research

Exploración sistemática de repositorios trending de GitHub para descubrir herramientas nuevas relevantes para el ecosistema.

## Cuándo usar

- Sesiones de aprendizaje autónomo / cron jobs de descubrimiento
- Cuando se necesita investigar tendencias en el ecosistema de desarrollo
- Cuando se quiere actualizar el catálogo de skills con novedades
- Cuando el usuario pregunta por herramientas nuevas o tendencias

## Pasos

### 1. Fetch páginas de trending

```bash
# Diario
curl -s 'https://github.com/trending?since=daily' -o /tmp/trending-daily.html

# Semanal
curl -s 'https://github.com/trending?since=weekly' -o /tmp/trending-weekly.html
```

**⚠️ Browser tool:** GitHub Trending pages are heavy SPAs. The browser tool often fails with undici/Node.js errors on these pages. Always use curl + Python parsing instead.

**⚠️ Star counts EN el HTML (actualizado 2026-06-04):** GitHub ha eliminado los star counts del HTML de Trending por completo. El patrón `aria-label="[\d, ]+ stars"` ya NO funciona (no hay estrellas en el HTML). **Solución:** extraer repos del HTML (solo nombre, descripción, lenguaje) y usar la GitHub API para TODO lo demás (stars, topics, license, created_at). Ver `references/trending-starless-2026-06-04.md` para el patrón completo.

### 2. Parsear HTML con Python (sin estrellas — solo repos)

**⚠️ 2026-06-04:** GitHub ya NO incluye star counts en el HTML de Trending. Extraer solo repo name, description, language y badge "new".

```python
import re

def extract_repos(html):
    repos = []
    articles = re.findall(r'<article class="Box-row"[^>]*>.*?</article>', html, re.DOTALL)
    
    for article in articles:
        # Skip sponsored
        if 'sponsored' in article.lower():
            continue
        
        # Repo name from h2 > a
        repo_match = re.search(r'<h2[^>]*>.*?<a href="(/[^"]+?)"[^>]*>', article, re.DOTALL)
        if not repo_match:
            continue
        repo = repo_match.group(1).strip('/')
        if '/stargazers' in repo:
            repo = repo.replace('/stargazers', '')
        
        # ⚠️ Stars: NO están en el HTML (eliminados 2026-06-04). Usar API.
        stars = '?'  # Se enriquece con la API de GitHub
        
        # Description
        desc_match = re.search(r'<p class="col-9[^"]*"[^>]*>([^<]+)', article, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ''
        
        # Language
        lang_match = re.search(r'data-language="([^"]+)"', article)
        lang = lang_match.group(1) if lang_match else ''
        
        repos.append({
            'repo': repo,
            'stars': stars,
            'description': desc,
            'language': lang
        })
    
    return repos
```

### 3. Enriquecer con API de GitHub (OBLIGATORIO desde 2026-06-04)

**⚠️ 2026-06-04:** GitHub ha eliminado los star counts del HTML. La API es la ÚNICA fuente fiable de estrellas, topics, license, created_at.

```bash
curl -s "https://api.github.com/repos/OWNER/REPO" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Stars: {data.get('stargazers_count')}\")
print(f\"Forks: {data.get('forks_count')}\")
print(f\"Created: {data.get('created_at')[:10]}\")
print(f\"Language: {data.get('language')}\")
print(f\"Topics: {data.get('topics', [])}\")
print(f\"License: {data.get('license', {}).get('spdx_id') if data.get('license') else 'N/A'}\")
"
```

**⚠️ Rate limiting:** GitHub API has 60 req/hour unauthenticated. For bulk fetching, use a token:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/OWNER/REPO"
```

### 4. Leer READMEs

```bash
# Intentar ramas en orden: main → master → develop
for branch in main master develop; do
    if curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/OWNER/REPO/$branch/README.md" | grep -q "200"; then
        curl -s "https://raw.githubusercontent.com/OWNER/REPO/$branch/README.md" | head -3000
        break
    fi
done
```

**⚠️ Algunos READMEs pueden estar en subcarpetas** (`docs/README.md`, `README.zh-CN.md`, etc.). Si el README principal no existe, buscar alternativas.

### 5. Cross-reference con skills existentes (UN SOLO PASO)

**⚠️ 2026-06-05: El enfoque de 3 fases (grep) está roto.** INDEX.md usa tablas markdown con niveles profundos (`||||| [repo](path)`) y URLs embebidas. Un simple `grep` produce 0 coincidencias (falsas negativas). **El enfoque grep NO funciona.**

**Solución correcta — un solo script Python que lee todos los SKILL.md:**

```python
import os, re

trending_repos = ['OWNER/REPO1', 'OWNER/REPO2', ...]
skills_dir = '/root/workspace/Mastermind/skills'
existing = {}
new = []

for repo in trending_repos:
    found = False
    for root, dirs, files in os.walk(skills_dir):
        for fname in files:
            if fname == 'SKILL.md':
                with open(os.path.join(root, fname), 'r') as f:
                    content = f.read()
                if repo.lower() in content.lower():
                    found = True
                    existing[repo] = os.path.join(root, fname)
                    break
        if found:
            break
    if not found:
        new.append(repo)
```

**Este enfoque es:**
- **Fiable:** lee el contenido real de cada SKILL.md, no hace regex sobre tablas
- **Completo:** encuentra skills aunque el repo aparezca como `OWNER/REPO` sin prefijo
- **Simple:** un solo paso, no tres fases de grep
- **Rápido:** lee ~50 archivos como máximo

**⚠️ 2026-06-09: Falsos positivos en cross-reference.** El script puede encontrar `OWNER/REPO` en archivos que NO son SKILL.md (ej: INDEX.md, notas, etc.). Tras encontrar un match, verificar que el archivo realmente existe en el path devuelto: `os.path.isfile(path)`. Si no existe, tratar como "new".

**No usar:** `grep -r "OWNER/REPO" skills/` — falla con tablas anidadas. **No usar:** `grep "github.com/OWNER/REPO"` — falla con paths relativos.

### 6. Seleccionar repos para explorar

Criterios de selección:
- **Doble trending** (aparece en diario Y semanal) → máxima prioridad
- **Relevancia para ecosistema** (IA, agents, MCP, dashboards, dev tools)
- **Popularidad** (estrellas, crecimiento)
- **Novedad** (¿ya tenemos skill?)
- **Utilidad práctica** (¿lo usaríamos?)

**⚠️ Patrón "skip known giants":** No crear skill para repos que son tan conocidos que no aportan valor nuevo. Ejemplos: `llama.cpp` (115k⭐), `opencv` (88k⭐). La regla es: solo crear skill para repos genuinamente nuevos o con features significativamente nuevas. Actualizar skills existentes es preferible a crear duplicados.

### 6.5 Actualizar skills existentes con nuevos conteos

Cuando los trending repos YA tienen skill (situación muy común), el trabajo se transforma:

**Patrón A — Actualizar conteos de estrellas:**
Los SKILL.md tienen star counts en formatos muy diversos. No hay un patrón único. Buscar TODAS estas variantes:
- `33.3k⭐`, `33K⭐`, `33K+⭐`, `33k+⭐`
- `33K estrellas`, `33k estrellas`
- `~24k`, `~24k⭐`
- `1,430`, `1.4k⭐`
- `207.4k⭐`, `208K+ stars`

**Método:** Script Python con lista de `(old_string, new_string)` por cada skill. Probar múltiples variantes. Si ninguna coincide, añadir la fecha de actualización al final del archivo con el nuevo conteo.

**Patrón B — Actualizar features nuevas:**
Leer el README completo y buscar secciones "What's New", "Changelog", "Releases". Si hay features significativas nuevas (nueva versión mayor, nuevo soporte, etc.), actualizar la sección correspondiente del SKILL.md.

**Patrón C — Actualizar INDEX.md:**
El INDEX.md tiene star counts en las tablas. Actualizar con `content.replace(old, new)` para cada conteo viejo → nuevo.

### 7. Crear/actualizar skills

Para cada repo seleccionado:
1. Leer README completo y estructura del repo
2. Identificar qué hace, casos de uso, patrones interesantes
3. **Verificar si ya tiene skill** → si SÍ, actualizar conteos y features (ver 6.5)
4. Si NO tiene skill, crear SKILL.md con formato estándar
5. Actualizar INDEX.md con el nuevo skill o conteos actualizados
6. Crear trending-learning-plan.md con el resumen de la sesión
7. Commit y push al repositorio

## Categorías de skills

`ia`, `backend`, `frontend`, `devops`, `data`, `herramientas`, `mcp`, `testing`, `productivity`, `creative`, `media`, `multi-agent`, `vision`, `data-science`, `mlops`, `infraestructura`, `github`, `research`, `social`

## Formato de SKILL.md

```yaml
---
name: repo-name
description: "Descripción breve de qué hace el repo"
url: https://github.com/OWNER/REPO
category: categoria
fecha: YYYY-MM-DD
---
```

Secciones obligatorias:
- ¿Qué hace?
- Casos de uso
- Snippets útiles
- Cómo integrarlo
- Pitfalls
- Fecha de descubrimiento

## Pitfalls

- **Browser tool en GitHub Trending:** Funciona (devuelve datos) pero truncado en páginas largas. Para extracción completa, usar curl + Python parsing. El browser es útil para explorar visualmente, pero no para parsing completo.
- **Sponsors aparecen primero:** GitHub Trending muestra sponsors/recomendados antes de repos orgánicos. Filtrar con `sponsored` en el HTML.
- **Star counts EN HTML (2026-06-04):** GitHub ha ELIMINADO los star counts del HTML de Trending por completo. `aria-label` con estrellas ya no existe. Extraer solo repo name + description + language del HTML, y usar la GitHub API para TODO lo demás (stars, topics, license, created_at). Ver `references/trending-starless-2026-06-04.md`.
- **Rate limiting API:** 60 req/hour sin token. Para sesiones con muchos repos, usar `$GITHUB_TOKEN`.
- **README en rama diferente:** Algunos repos usan `master`, `develop`, o ramas custom. Intentar `main` → `master` → `develop` con HTTP status code check.
- **README en subcarpeta:** Algunos repos tienen README en `docs/README.md` o versiones localizadas (`README.zh-CN.md`).
- **No duplicar skills:** Siempre verificar si ya existe skill antes de crear uno nuevo. Buscar por URL del repo y por nombre.
- **Todo en castellano:** Los skills se crean en castellano, nunca inglés.
- **Script legacy sin estrellas:** `scripts/parse-trending.py` no extrae star counts. Usar el patrón con `aria-label` directamente en el código de la sesión.
- **curl | python3 pipe bloqueado por tirith:** La seguridad del entorno bloquea tuberías de curl a interpretadores. Siempre usar un script Python independiente (`write_file` + `python3 script.py`) en lugar de `curl URL | python3 -c "..."`.
- **API GitHub con urllib:** Para enriquecer datos con la API de GitHub, usar `urllib.request` en Python en lugar de curl pipes. Cargar el token desde `.env` o `GITHUB_TOKEN` env var.
- **Inline datetime en Python (2026-06-06):** Nunca meter datetime inline en un string de Python — las comillas anidadas siempre rompen la sintaxis. Calcular fechas en el script principal directamente.
- **⚠️ INDEX.md patch tool risk.** El `patch` tool puede corromper escapes `\\` en tablas markdown. **Regla:** si la línea nueva no tiene `\\`, usar `patch`. Si tiene `\\`, usar `python3` con `readlines()` + `insert()` + `writelines()`.
- **⚠️ 2026-06-09: Nombres de skill vs nombres de repo.** No asumir que el nombre del skill en INDEX.md coincide con el nombre del repo. `ecc-agent-harness` → skill real `everything-claude-code`. `revfactory-harness` → skill real `harness`. Siempre verificar con `skill_view()` y `os.path.exists()`.
- **⚠️ 2026-06-09: INDEX.md integrity.** INDEX.md puede referenciar skills que NO existen como skills cargables. Verificar con `skill_view()` que un skill referenced en INDEX.md es realmente cargable antes de confiar en INDEX.md como fuente de verdad.

## Operational Insights (2026-06-09)

- **Patrón de trabajo real:** ~70% del trabajo del cron trending son actualizaciones de star count en skills existentes, ~30% son skills nuevos. La mayoría de commits son modificaciones de 1-2 líneas en SKILL.md existentes.
- **Skills que se actualizan repetidamente:** `agent-reach`, `last30days-skill`, `open-notebook`, `mempalace`, `headroom` — aparecen en casi todos los runs.
- **STEM skills:** Se crearon el 03-06 y se re-escribieron el 08-06 con el mismo contenido (no es aprendizaje nuevo, es re-escritura).
- **El valor real del cron** está en los ~3-5 skills nuevos por run, no en las actualizaciones de star count.
- **Skills problemáticos:** Algunos skills (ej: `fastmcp`) pueden quedar en cuarentena por timeout. Saltarlos y avanzar el índice.

## Ejemplo completo de sesión

```bash
# 1. Fetch
curl -s 'https://github.com/trending?since=daily' -o /tmp/trending-daily.html
curl -s 'https://github.com/trending?since=weekly' -o /tmp/trending-weekly.html

# 2. Parsear (script Python)
python3 /tmp/parse_trending.py

# 3. Cross-reference (UN SOLO SCRIPT PYTHON)
python3 /tmp/cross_reference.py  # lee SKILL.md directo, NO grep

# 4. Enriquecer con API (para repos seleccionados)
python3 /tmp/enrich_trending.py  # carga token desde .env, usa urllib

# 5. Leer READMEs (para los seleccionados)
python3 /tmp/explore_repos.py  # fetch README + tree + API info

# 6. Crear SKILL.md
# 7. Actualizar INDEX.md
# 8. Commit + push
```

**Nota:** Los scripts de ejemplo (`parse_trending.py`, `cross_reference.py`, `enrich_trending.py`, `explore_repos.py`) se crean en `/tmp/` con `write_file` y se ejecutan con `python3`. Nunca usar `curl | python3` pipe — el entorno lo bloquea.

## Frecuencia recomendada

- **Semanal:** Sesión automática de descubrimiento
- **Antes de añadir:** Verificar que el nuevo skill no es duplicado
- **Mensual:** Revisar skills existentes y actualizar con nueva info

## Archivos de soporte

- `references/api-enrichment.md` — GitHub API enrichment, star counts, batch scripts
- `references/cross-reference-2026-06-03.md` — Cross-reference de trending con skills existentes (sesión 2026-06-03)
- `references/cross-reference-2026-06-05.md` — Cross-reference con 5 nuevos skills: open-notebook, trivy, open-llm-vtuber, voxcpm, moneyprinterturbo. Refinamiento del cross-reference regex.
- `references/cross-reference-pattern-2026-06-06.md` — Patrón correcto de cross-reference: script Python que lee SKILL.md directo, NO grep sobre INDEX.md
- `references/cross-reference-2026-06-06.md` — Sesión 2026-06-06: 34 repos analizados, 28 existentes, 2 nuevos (copilotkit, openai-plugins)
- `references/index-md-format.md` — Formato del catálogo INDEX.md (tablas con niveles `|`, badges, reglas). ⚠️ 2026-06-08: añadir filas nuevas preferir `python3` con `readlines()` + `insert()` + `writelines()` sobre `patch` tool, que corrompe escapes `\` en tablas markdown.
- `references/trending-starless-2026-06-04.md` — ⚠️ GitHub eliminó estrellas del HTML de Trending. Patrón de API-only enrichment
- `references/enrichment-datetime-fix.md` — Fix para error de sintaxis en inline datetime de Python (sesión 2026-06-06)
- `scripts/parse-trending.py` — Script de parsing HTML (solo extrae repos, NO estrellas). ⚠️ Actualizado 2026-06-06: ya no intenta extraer star counts (patrón `aria-label` eliminado por GitHub).
- `references/explore-combined-pattern-2026-06-08.md` — Patrón de exploración combinada: un solo script para API + README + tree del repo, en lugar de 3 scripts separados.
- `references/trending-session-2026-06-08.md` — Sesión 2026-06-08: 27 repos, 5 doble trending, patrón "skip known giants" para no crear skills de repos ya conocidos.
- `references/trending-session-2026-06-09.md` — Sesión 2026-06-09: 34 repos (16+18), 4 doble trending, 2 nuevos skills (ECC, Harness), 4 actualizados.
- `references/index-md-integrity-2026-06-09.md` — ⚠️ INDEX.md puede referenciar skills que no existen como cargables. Verificar con `skill_view()` antes de confiar en INDEX.md.
- `references/update-star-counts-pattern.md` — ⚠️ Los star counts en SKILL.md tienen formatos muy diversos (33.3k⭐, 33K estrellas, ~24k, 1,430...). Script multi-variant con fallback a añadir fecha de actualización.
- `references/trending-learning-pattern-2026-06-09.md` — Patrón real del cron trending: ~70% del trabajo son actualizaciones de star count (bajo valor), ~20% son skills nuevos (alto valor). STEM skills re-escritos no son aprendizaje nuevo.
