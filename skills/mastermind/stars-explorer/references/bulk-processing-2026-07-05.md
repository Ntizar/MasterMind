# Bulk Processing 2026-07-05 — Patrón que funciona

## Contexto

El usuario notó que el sistema llevaba 2 meses en ~200 skills sin crecer. Auditoría reveló:
- 11 runs del stars-explorer, 132 repos explorados, solo 9 skills creados (8.5%)
- 103 repos en "pending" sin procesar
- Batch de 3 repos/run era insuficiente
- Criterios de creación demasiado conservadores

## Patrón que funciona (sin subagentes)

### Paso 1: Fetch masivo de READMEs

```python
import urllib.request, json, os

api_key = os.environ.get('GITHUB_TOKEN', '')
results = []
for repo in pending_repos:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/readme",
            headers={
                "Authorization": f"token {api_key}",
                "Accept": "application/vnd.github.v3.raw"
            }
        )
        readme = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='replace')[:8000]
        results.append({"repo": repo, "readme": readme})
    except Exception as e:
        results.append({"repo": repo, "readme": "", "error": str(e)})
```

- 103 repos en ~60 segundos
- Usar `execute_code` (no terminal — el output es muy grande)
- Timeout de 10s por repo para no bloquear

### Paso 2: Categorizar programáticamente

```python
categories = {
    "skill_created": {},  # repo → skill_name
    "reference": [],     # ya existe skill similar
    "skip": []           # awesome lists, juegos, too niche
}

# Heurísticas:
# - "awesome" in name.lower() → skip
# - repo ya tiene skill en ChromaDB → reference
# - repo tiene patrón útil para David (mapas, 3D, datos, IA) → skill_created
```

### Paso 3: Crear skills directo (NO delegar)

```python
# Ráfagas de 3 skill_manage calls simultáneas (paralelas)
# El agente principal puede hacer esto sin timeout
skill_manage(action='create', name='transit-data-resources', category='geospatial', content=...)
skill_manage(action='create', name='transit-map-simulation', category='geospatial', content=...)
skill_manage(action='create', name='gtfs-to-html-timetables', category='geospatial', content=...)
```

- 3 calls simultáneas = ~15 segundos
- 18 skills en ~3 minutos total
- NO usar delegate_task — timeout a 600s

### Paso 4: Actualizar registry

```python
import json
from pathlib import Path
from datetime import datetime, timezone

registry = json.loads(Path("/hermes-home/data/stars-registry.json").read_text())
processed = registry.get("processed", {})

for repo, skill_name in skills_created_map.items():
    processed[repo] = {
        "explored_at": datetime.now(timezone.utc).isoformat(),
        "category": "skill_created",
        "skill_created": skill_name
    }

for repo in skip_repos:
    processed[repo]["category"] = "skip"

for repo in reference_repos:
    processed[repo]["category"] = "reference"

registry["processed"] = processed
Path("/hermes-home/data/stars-registry.json").write_text(
    json.dumps(registry, indent=2, ensure_ascii=False)
)
```

### Paso 5: Re-indexar ChromaDB + regenerar índice

```bash
bash /hermes-home/scripts/run-indexar-skills.sh
# Regenerar skills/index.json con execute_code (Python script)
```

### Paso 6: Commit + push

```bash
cd /root/workspace/Mastermind
git add -A
git commit -m "feat: +N skills de stars-explorer batch"
git push origin main
```

## Resultados

- 103 pending → 3 pending
- 18 skills creados (244 → 265 total)
- ChromaDB: 267 → 285 indexados
- Tiempo total: ~5 minutos
- Sin subagentes, sin timeouts

## Lo que NO funciona

- `delegate_task` con 3 subagentes para crear 6 skills cada uno → TODOS timeout a 600s
- `explorar-stars.py --all` → timeout a 300s
- `explorar-stars.py --batch 100` → timeout (demasiados fetches)
- Crear skills uno por uno (secuencial) → lento, mejor en ráfagas de 3
