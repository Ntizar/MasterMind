# GitHub Trending sin estrellas en HTML

## Problema (2026-06-04)

GitHub ha eliminado los star counts del HTML de las páginas de Trending. Los patrones anteriores ya no funcionan:

- `aria-label="X stars" total-stars` ❌ (2026-06-03)
- `aria-label="[\d, ]+ stars"` ❌ (2026-06-04)

**Ningún aria-label con estrellas existe en el HTML actual.**

## Solución

### Paso 1: Extraer repos del HTML (solo metadatos básicos)

```python
import re

def extract_repos(html):
    repos = []
    articles = re.findall(r'<article class="Box-row"[^>]*>.*?</article>', html, re.DOTALL)
    
    for article in articles:
        if 'sponsored' in article.lower():
            continue
        
        repo_match = re.search(r'<h2[^>]*>.*?<a href="(/[^"]+?)"[^>]*>', article, re.DOTALL)
        if not repo_match:
            continue
        repo = repo_match.group(1).strip('/')
        if '/stargazers' in repo:
            repo = repo.replace('/stargazers', '')
        
        desc_match = re.search(r'<p class="col-9[^"]*"[^>]*>([^<]+)', article, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ''
        
        lang_match = re.search(r'data-language="([^"]+)"', article)
        lang = lang_match.group(1) if lang_match else ''
        
        repos.append({
            'repo': repo,
            'stars': '?',  # TODO: enriquecer con API
            'description': desc,
            'language': lang
        })
    
    return repos
```

### Paso 2: Enriquecer con GitHub API (OBLIGATORIO)

```python
import urllib.request
import json
import os

def enrich_repo(repo_name, token=None):
    url = f"https://api.github.com/repos/{repo_name}"
    req = urllib.request.Request(url)
    if token:
        req.add_header('Authorization', f'token {token}')
    req.add_header('Accept', 'application/vnd.github+json')
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        return {
            'stars': data.get('stargazers_count', '?'),
            'forks': data.get('forks_count', '?'),
            'topics': data.get('topics', []),
            'license': data.get('license', {}).get('spdx_id', '') if data.get('license') else '',
            'created': data.get('created_at', '')[:10] if data.get('created_at') else '',
        }
```

### Paso 3: Token para evitar rate limiting

```bash
GITHUB_TOKEN=$(grep GITHUB_TOKEN /hermes-home/.env | cut -d= -f2)
```

Sin token: 60 req/hora. Con token: 5000 req/hora.

## Referencias

- Sesión de descubrimiento: 2026-06-04
- 32 repos trending analizados, todos enriquecidos vía API
