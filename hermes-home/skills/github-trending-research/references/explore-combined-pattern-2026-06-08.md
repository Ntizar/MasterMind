# Patrón de exploración combinada — 2026-06-08

## Problema

La sesión del 2026-06-06 usaba 3 scripts separados para enriquecer datos:
1. `enrich_trending.py` → API GitHub (stars, topics, license)
2. `explore_repos.py` → README + tree del repo
3. `check_double_trending.py` → repos doble trending

Cada script hacía llamadas API independientes a los mismos repos.

## Solución: Script combinado

Un solo script que para cada repos hace:
1. **GET /repos/OWNER/REPO** → stars, forks, language, topics, license, created_at, updated_at, description
2. **GET /repos/OWNER/REPO/README.md** → primer README encontrado (main → master → develop)
3. **GET /repos/OWNER/REPO/git/trees/main?recursive=1** → estructura de archivos

```python
import urllib.request, json, os

env_path = '/root/workspace/Mastermind/.env'
token = ''
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                token = line.split('=', 1)[1].strip()

repos = ['OWNER/REPO1', 'OWNER/REPO2', ...]

for repo in repos:
    # 1. API repo info
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url)
    if token: req.add_header('Authorization', f'token {token}')
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    
    # 2. README
    for branch in ['main', 'master', 'develop']:
        readme_url = f"https://raw.githubusercontent.com/{repo}/{branch}/README.md"
        req2 = urllib.request.Request(readme_url)
        if token: req2.add_header('Authorization', f'token {token}')
        try:
            with urllib.request.urlopen(req2, timeout=10) as resp2:
                print(resp2.read().decode()[:2000])
                break
        except: continue
    
    # 3. Tree
    tree_url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    req3 = urllib.request.Request(tree_url)
    if token: req3.add_header('Authorization', f'token {token}')
    try:
        with urllib.request.urlopen(req3, timeout=10) as resp3:
            tree_data = json.loads(resp3.read().decode())
            files = [f['path'] for f in tree_data.get('tree', [])
                     if '/' not in f['path'] or f['path'].count('/') == 1]
            print(f"Top-level: {', '.join(sorted(files)[:30])}")
    except: pass
```

## Beneficios

- Menos llamadas API → un request por repo en lugar de tres
- Menos scripts → un archivo en lugar de tres
- Output estructurado → todo el info de un repo en un bloque

## Fecha
2026-06-08 — Sesión de trending discovery
