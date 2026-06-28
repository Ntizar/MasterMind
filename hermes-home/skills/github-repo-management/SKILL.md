---
name: github-repo-management
description: "Clone/create/fork repos; manage remotes, releases."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Repositories, Git, Releases, Secrets, Configuration]
    related_skills: [github-auth, github-pr-workflow, github-issues]
---

# GitHub Repository Management

Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` + `curl` fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

### Setup

```bash
# Auth detection: prefer gh, fall back to GITHUB_TOKEN from .env or .git-credentials
AUTH="gh"
command -v gh &>/dev/null && gh auth status &>/dev/null || AUTH="git"
# Set GH_USER, OWNER, REPO as needed
```

---

## 1. Cloning Repositories

```bash
# Clone via HTTPS
git clone https://github.com/owner/repo-name.git

# Shallow clone, specific branch, SSH
git clone --depth 1 https://github.com/owner/repo-name.git
git clone --branch develop https://github.com/owner/repo-name.git
git clone git@github.com:owner/repo-name.git

# With gh shorthand
gh repo clone owner/repo-name
gh repo clone owner/repo-name -- --depth 1
```

## 2. Creating Repositories

```bash
# Public, with description, license
gh repo create my-new-project --public --description "A useful tool" --license MIT --clone

# Private, under an organization
gh repo create my-org/my-new-project --private --clone

# From existing local directory
cd /path/to/existing/project && gh repo create my-project --source . --public --push

# From a template
gh repo create my-new-app --template owner/template-repo --public --clone
```

### Pitfall: Token en `/hermes-home/.env` (sin `gh` CLI)

En Hermes VM, `gh` CLI NO está instalado. Las herramientas GitHub disponibles son `git` + `curl` con token de `/hermes-home/.env`.

**Forma correcta de obtener el token:**
```bash
source /hermes-home/.env
# $GITHUB_TOKEN está disponible

# Para curl:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos

# Para git push (¡NUNCA en la URL!):
cd /path/to/repo
git remote add origin "https://github.com/Ntizar/$REPO.git"
GIT_ASKPASS="echo" git push -u origin main <<< "$GITHUB_TOKEN"
```
**NO usar** `https://Ntizar:$TOKEN@github.com/...` en la URL remota — los tokens suelen contener `/`, `+`, `=` que rompen el parseo de URLs incluso escapadas.

### Private repo con `auto_init: true` (curl) → conflicto de merge

Cuando se crea un repo privado vía API con `"auto_init": true`, el remoto recibe un README inicial. Si luego haces `git push` desde un repo local con su propio README, falla por divergencia.

**Solución:** hacer merge (NO rebase):
```bash
cd /path/to/repo
git pull origin main --allow-unrelated-histories --no-edit  # merge, no rebase
git push origin main
```

Rebase falla con `CONFLICT (add/add)` en este caso porque ambos lados crearon el mismo archivo desde vacío.

**Private repo via curl/Python (when gh CLI is unavailable):**

**Token sourcing (Hermes):** El token está en `/hermes-home/.env` como `GITHUB_TOKEN`. NO en `gh config` (gh no está instalado en Hermes). Usar:
```bash
source /hermes-home/.env
# Ahora $GITHUB_TOKEN está disponible
```
O en Python: leer `/hermes-home/.env` y parsear `GITHUB_TOKEN=...`.

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
        'private': True,      # ← CRITICAL: omit this → public repo
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
)
```

**Git push with token from gh config (avoids special-char URL breakage):**

```python
import yaml, subprocess, os

with open('/root/.config/gh/hosts.yml') as f:
    config = yaml.safe_load(f)
token = config['github.com']['oauth_token']

subprocess.run(['git', '-C', '/path/to/repo', 'remote', 'add', 'origin',
    'https://github.com/OWNER/REPO.git'], capture_output=True)

env = os.environ.copy()
env['GIT_ASKPASS'] = '/dev/null'  # avoids embedded token in URL
result = subprocess.run(
    ['git', '-C', '/path/to/repo', 'push', '-u', 'origin', 'main'],
    capture_output=True, text=True,
    input=f'{token}\n\n',  # username + password on stdin
    timeout=30
)
```

**Why `GIT_ASKPASS` instead of `https://user:token@github.com/...`?**  
GitHub tokens often contain `'/'`, `'+'`, `'='` that break URL parsing even when URL-encoded. The askpass approach avoids this entirely.

## 3. Forking Repositories

```bash
gh repo fork owner/repo-name --clone
```

### Keeping a Fork in Sync

```bash
git fetch upstream && git checkout main && git merge upstream/main && git push origin main
gh repo sync $GH_USER/repo-name
```

## 4. Repository Information

```bash
gh repo view owner/repo-name
gh repo list --limit 20
gh search repos "machine learning" --language python --sort stars
```

For curl: `GET /repos/{owner}/{repo}`, `GET /user/repos`, `GET /search/repositories`.

## 5. Repository Settings

```bash
gh repo edit --description "Updated" --visibility public
gh repo edit --enable-wiki=false --enable-issues=true
gh repo edit --default-branch main --add-topic "machine-learning,python"
gh repo edit --enable-auto-merge
```

For curl: `PATCH /repos/{owner}/{repo}` for settings, `PUT /repos/{owner}/{repo}/topics` for topics.

## 6. Branch Protection

```bash
# View
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection

# Set up (requires curl PUT with JSON: required_status_checks, required_pull_request_reviews, enforce_admins)
```

## 7. Secrets Management (GitHub Actions)

```bash
gh secret set API_KEY --body "your-secret-value"
gh secret list
gh secret delete API_KEY
```

Note: `gh secret set` is dramatically simpler. Secrets via curl require encrypting with the repo's public key (PyNaCl). If `gh` isn't available, recommend installing it.

## 8. Releases

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease --generate-notes
gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"
gh release list
gh release download v1.0.0 --dir ./downloads
```

For curl: `POST /repos/{owner}/{repo}/releases` with JSON body. Upload assets via `POST /repos/{owner}/{repo}/releases/{id}/assets`.

## 9. GitHub Actions Workflows

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
```

For curl: `GET /repos/{owner}/{repo}/actions/workflows`, `GET /actions/runs`, `POST /actions/runs/{id}/rerun`, `POST /actions/workflows/{id}/dispatches`.

## 10. Gists

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

For curl: `POST /gists` with JSON body containing `description`, `public`, and `files`.

## 11. GitHub Pages

### ⚠️ CRITICAL: gh CLI no instalado en Hermes

En la VM de Hermes, `gh` CLI **NO está instalado**. Siempre usar `git` + `curl` con token de `/hermes-home/.env`.

### Enabling GitHub Pages

```bash
# Check if Pages is enabled
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pages | python3 -c "import sys,json; d=json.load(sys.stdin); print('status:', d.get('status'), '| source:', d.get('source',{}).get('branch','?'))"

# Enable Pages on master branch, root directory
# (Requires repo admin permissions — do via GitHub UI or API)
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/pages \
  -d '{"source":{"branch":"master","path":"/"}}'
```

### ⚠️ CRITICAL PITFALL: Case sensitivity of index.html

**GitHub Pages ONLY serves `index.html` (lowercase) at the root URL.** If your file is named `INDEX.html`, `Index.html`, or any other casing, the root URL (`https://user.github.io/repo/`) returns 404.

**Fix:** Create a lowercase `index.html` that redirects:
```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=INDEX.html">
</head>
<body>
  <p>Redirigiendo a <a href="INDEX.html">INDEX.html</a>...</p>
</body>
</html>
```

Or rename the main file to `index.html` (lowercase).

### Monitoring Build Status

After pushing changes, GitHub Pages rebuilds asynchronously. Monitor via API:

```bash
# Check build status
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pages | \
  python3 -c "import sys,json; print('status:', json.load(sys.stdin).get('status'))"

# Possible statuses: "building", "built", "errored"

# Get latest build details
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pages/builds/latest | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('status:', d.get('status'), '| commit:', d.get('commit'), '| error:', d.get('error',{}).get('message','none'))"

# Poll until built
for i in 1 2 3 4 5; do
  sleep 30
  st=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/pages | \
    python3 -c "import sys,json; print(json.load(sys.stdin).get('status','?'))")
  echo "Attempt $i: $st"
  [ "$st" = "built" ] && echo "✅ Built!" && break
done

# Verify site is live
curl -s -o /dev/null -w "%{http_code}" -L "https://$OWNER.github.io/$REPO/"
```

### Common GitHub Pages Issues

| Symptom | Cause | Fix |
|---------|-------|------|
| 404 at root URL | `index.html` named `INDEX.html` | Add lowercase `index.html` redirect |
| 404 on subpages | File not in published branch | Check source branch in Pages settings |
| Build stuck "building" | Large site or GitHub backlog | Wait, check build logs via API |
| Custom domain not working | CNAME not configured | Add CNAME file or configure in repo settings |
| HTTPS not enforced | DNS propagation delay | Wait up to 24h, check `https_enforced` in API |

## Quick Reference Table

| Action | gh | git + curl |
|--------|-----|-----------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` + `git clone` |
| Repo info | `gh repo view o/r` | `curl GET /repos/o/r` |
| Edit settings | `gh repo edit --...` | `curl PATCH /repos/o/r` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |
| List workflows | `gh workflow list` | `curl GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `curl POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `curl PUT /repos/o/r/actions/secrets/KEY` (+ encryption) |
| Private repo + push | — | `references/token-extraction-push.md` |

## Linked Files

- `references/github-api-cheatsheet.md` — Full REST API endpoint reference
- `references/token-extraction-push.md` — Token extraction from gh config + private repo creation + git push with GIT_ASKPASS
- `references/patron-tracking-dieta.md` — Patrón de tracking de dieta y ejercicio: estructura de repo privado, flujo de registro diario con timestamp, tablas de peso/pasos/comidas

## When to Use

- User wants to create, clone, fork, or manage a GitHub repository
- Need to configure repo settings (branch protection, topics, auto-merge)
- Managing GitHub Actions secrets or workflow runs
- Creating releases with assets for a project

## When NOT to Use

- The user only needs to read public repo info → `curl` without auth is enough
- Managing repos on GitLab/Bitbucket → different APIs and workflows
- Bulk repo operations across organizations → consider `gh org` or API scripting
