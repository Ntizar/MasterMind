# Token Extraction + Git Push to Private Repos

## Extraer token de gh config (sin gh CLI)

El token de GitHub está en `/root/.config/gh/hosts.yml` con formato YAML:

```yaml
github.com:
    oauth_token: ghp_xxxxxxxxxxxxxxxxxxxx
    user: Ntizar
```

**Python (recomendado):**
```python
import yaml
with open('/root/.config/gh/hosts.yml') as f:
    config = yaml.safe_load(f)
token = config['github.com']['oauth_token']
```

**Bash (sin yaml):**
```bash
token=$(sed -n '/oauth_token:/s/.*oauth_token: *//p' /root/.config/gh/hosts.yml)
```

## Crear repo privado vía API

```python
import yaml, requests

with open('/root/.config/gh/hosts.yml') as f:
    config = yaml.safe_load(f)
token = config['github.com']['oauth_token']

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

r = requests.post(
    'https://api.github.com/user/repos',
    headers=headers,
    json={
        'name': 'REPO_NAME',
        'description': 'Description',
        'private': True,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
)
```

## Git push con token (evita URL rotas)

**Problema:** `https://user:ghp_token/with/slashes@github.com/OWNER/REPO.git`  
Los caracteres especiales (`/`, `+`, `=`) en el token rompen la URL incluso escapados.

**Solución: GIT_ASKPASS + stdin**

```python
import yaml, subprocess, os

with open('/root/.config/gh/hosts.yml') as f:
    token = yaml.safe_load(f)['github.com']['oauth_token']

# Remote sin token en la URL
subprocess.run(['git', '-C', '/repo', 'remote', 'add', 'origin',
    'https://github.com/OWNER/REPO.git'])

# Push con token por stdin
env = os.environ.copy()
env['GIT_ASKPASS'] = '/dev/null'
subprocess.run(
    ['git', '-C', '/repo', 'push', '-u', 'origin', 'main'],
    capture_output=True, text=True,
    input=f'{token}\n\n',
    timeout=30
)
```

**Cómo funciona GIT_ASKPASS:**
1. Git necesita usuario/contraseña → ejecuta el programa GIT_ASKPASS
2. Le pasamos `/dev/null` que devuelve vacío
3. Pero también le pasamos `input=f'{token}\n\n'` → git lee de stdin como fallback
4. Primera línea = usuario (vacío), segunda línea = password (el token)
5. Git lo interpreta como autenticación básica sin URL embedding

## Habilitar GitHub Pages vía API

```python
import yaml, requests

with open('/root/.config/gh/hosts.yml') as f:
    token = yaml.safe_load(f)['github.com']['oauth_token']

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

r = requests.post(
    f'https://api.github.com/repos/OWNER/REPO/pages',
    headers=headers,
    json={
        'source': {'branch': 'main', 'path': '/'}
    }
)
```

**Nota:** GitHub Pages en repos privados requiere GitHub Pro/Team. En repos públicos funciona gratis.