---
name: github-workflow
description: "Flujo completo de trabajo con GitHub: autenticación, gestión de repos, PR lifecycle, code review, issues, knowledge repo como base de conocimiento persistente, deploy estático en Pages, y recuperación de repos corruptos."
version: 1.3.0
author: Hermes Agent
tags: [github, git, workflow, deployment, knowledge-repo, recovery]
---

# GitHub Workflow — Guía Completa

Flujo completo de trabajo con GitHub para agentes IA.

## Tabla de Contenidos

1. [Autenticación](#1-autenticación) — Tokens, SSH, gh CLI
2. [Gestión de Repos](#2-gestión-de-repos) — Clone, create, fork, remotes
3. [PR Lifecycle](#3-pr-lifecycle) — Branch, commit, open, CI, merge
4. [Code Review](#4-code-review) — Diffs, inline comments, gh CLI
5. [Issues](#5-issues) — Create, triage, label, assign
6. [Knowledge Repo](#6-knowledge-repo) — Base de conocimiento persistente
7. [GitHub Pages](#7-github-pages) — Deploy estático
8. [Repo Recovery](#8-repo-recovery) — Remote overwritten, force push restore
9. [Branch Rename + Pages Reconfig](#9-branch-rename--github-pages-reconfig) — master→main completo
10. [Environment Protection Rules](#10-github-pages--environment-protection-rules) — Pitfall con deployment_branch_policy
11. [Deploy Pages para Repo EXISTENTE](#11-deploy-pages-para-repo-existente) — **Verificar existencia antes de crear**
12. [Deploy Estático desde Cero](#12-deploy-estático-desde-cero-repo-nuevo--pages) — Crear repo + push + activar Pages

---

## 1. Autenticación

**GitHub CLI:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null
apt-get update -qq && apt-get install -y -qq gh
```

**Auth con token:**
```bash
token=$(grep GITHUB_TOKEN /hermes-home/.env | cut -d= -f2-)
# ⚠️ GH CLI falla con GITHUB_TOKEN env var set
GITHUB_TOKEN="" echo "$token" | gh auth login --with-token
```

## 2. Gestión de Repos

```bash
git clone https://github.com/OWNER/REPO.git
git remote add upstream https://github.com/ORIGINAL/REPO.git
git fetch upstream && git merge upstream/main
```

## 3. PR Lifecycle

```bash
git checkout -b feature/titulo
# ... changes ...
git add -A && git commit -m "feat: description"
git push -u origin feature/titulo
gh pr create --title "feat: title" --body "description"
gh pr merge --auto  # auto-merge si CI pasa
```

## 4. Code Review

```bash
gh pr diff 123     # Ver diff
gh pr comments 123  # Ver comentarios
gh pr review 123 --approve   # Aprobar
gh pr review 123 --comment -b "feedback"  # Comentar
```

## 5. Issues

```bash
gh issue create --title "Bug: ..." --body "description" --label "bug"
gh issue list --state open
gh issue edit 456 --add-label "priority-high"
```

## 6. Knowledge Repo

Usar un repos GitHub como base de conocimiento persistente:
- `notes/` — Notas con formato `YYYY-MM-DD-titulo.md`
- `mastermind/` o `skills/` — SKILL.md files
- `memory/` — Backups de memoria
- `scripts/` — Automatizaciones
- `config/` — Configuraciones

**Sync:** `git pull` → `cp -n mastermind/*.md /hermes-home/skills/mastermind/`

### 7.0 Decidir: GitHub Pages vs NaN

| Criterio | GitHub Pages | NaN.builders |
|----------|-------------|--------------|
| **Estático puro** (HTML/CSS/JS) | ✅ Ideal — gratis, simple | ❌ Overkill |
| **Node.js backend** | ❌ No soportado | ✅ Necesario |
| **APIs/proxy CORS** | ❌ No (usar proxy público) | ✅ Servidor propio |
| **Variables de entorno** | ❌ No | ✅ Sí |
| **Velocidad deploy** | 1-2 min (workflow) | 2-5 min (Kaniko) |
| **Control total** | Limitado | Completo |

**Regla:** Estáticos puros → GitHub Pages. Todo lo que necesite servidor → NaN.

### 7.0b Pitfall: GitHub Pages `legacy` + `/dashboard` path

Cuando GitHub Pages está en modo `legacy` con `source.path: "/"`:
- **Solo acepta** `/` o `/docs` como paths. `/dashboard` devuelve **422**.
- El PUT no cambia el build_type automáticamente — sigue en legacy.

**Solución A — iframe en index.html raíz (fallback inmediato):**
```html
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Título</title></head>
<body>
    <iframe src="./dashboard/index.html" style="width:100vw;height:100vh;border:none;margin:0;padding:0;"></iframe>
</body>
</html>
```
Funciona inmediatamente sin cambiar build_type. El workflow de Pages puede seguir existiendo sin conflictos.

**Solución B — Intentar activar workflow primero:**
1. Crear `.github/workflows/pages.yml` con `actions/deploy-pages@v4`
2. Commit + push
3. Esperar 60s, verificar con `curl`
4. Si sigue `errored` → usar iframe como fallback

**Verificar estado de Pages:**
```bash
curl -s https://api.github.com/repos/OWNER/REPO/pages \
  -H "Authorization: token $TOKEN" | jq '{build_type, status, source}'
# build_type: "legacy" + status: "errored" = bloqueado con paths nuevos
```

**Pitfalls:**
- El workflow dispatch manual (`POST /actions/workflows/X/dispatches`) devuelve **422** si el workflow NO tiene `workflow_dispatch` en su trigger — no es error de deploy
- `GET /repos/.../pages` muestra `build_type: "legacy"` + `status: "errored"` = bloqueado con paths nuevos
- `POST /repos/.../pages` con `build_type: "workflow"` devuelve **409** si Pages ya está activo
- `PUT /repos/.../pages` con `source.path: "/dashboard"` devuelve **422** si está en legacy mode

## 7. GitHub Pages

### 7.1 Deploy básico

**Activar Pages via API REST (sin gh CLI):**

```python
import urllib.request, json

token = ''  # leer de .env
data = json.dumps({"build_type": "workflow"}).encode()
req = urllib.request.Request(
    'https://api.github.com/repos/OWNER/REPO/pages',
    data=data,
    headers={
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    },
    method='POST'
)
resp = urllib.request.urlopen(req)
print(json.loads(resp.read())['html_url'])
# → https://OWNER.github.io/REPO/
```

**Activar con gh CLI:**
```bash
gh api repos/:owner/:repo/pages -X POST \
  -f source.branch=main -f source.path=/
```

**Pitfall:** `build_type: "workflow"` requiere que exista un workflow de GitHub Actions que use `actions/deploy-pages@v4`. Si el workflow no existe, el deploy falla silenciosamente.

### 7.1a Fix: legacy → workflow via PUT (cuando POST devuelve legacy stuck)

El POST a `/pages` a menudo devuelve `build_type: "legacy"` aunque el repo tenga un workflow de Pages. Legacy puede quedarse en `status: "building"` indefinidamente (probado con HTML de 138KB). **Fix:** hacer PUT para forzar `build_type: "workflow"`:

```bash
# 1. POST activa Pages (devuelve build_type: legacy)
curl -s -X POST https://api.github.com/repos/OWNER/REPO/pages \
  -H "Authorization: token $TOKEN" \
  -d '{"source":{"branch":"main","path":"/"}}'
# → build_type: "legacy", status: "building"

# 2. PUT cambia a workflow mode (204 = OK)
curl -s -X PUT https://api.github.com/repos/OWNER/REPO/pages \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"source":{"branch":"main","path":"/"},"build_type":"workflow"}'
# → 204 = success

# 3. Esperar y verificar
sleep 30
curl -s -o /dev/null -w "%{http_code}" https://OWNER.github.io/REPO/
# → 200
```

**Pitfall:** El PUT requiere que el workflow de Pages YA exista en el repo (commit + push antes de activar Pages). Si el workflow no existe, el PUT falla o el deploy falla silenciosamente.

**Secuencia completa correcta para activar Pages en repo estático existente:**
1. Crear `.nojekyll` en raíz
2. Crear `.github/workflows/pages.yml` con `actions/deploy-pages@v4`
3. Commit + push
4. `POST /repos/.../pages` → activa (devuelve legacy)
5. `PUT /repos/.../pages` con `build_type: "workflow"` → corrige
6. Verificar con `curl -sI`

### 7.1b Deploy ultra-rápido con branch gh-pages (HTML puro, sin build)

Para un HTML estático SIN build step (sin Vite, sin Node.js), el deploy más rápido es usar el branch `gh-pages` directamente. No requiere workflow de Actions, no requiere esperar a que GitHub Pages "active" el sitio.

**Pasos:**

```bash
# 1. Crear branch gh-pages desde main (con el HTML ya en la raíz)
git checkout -b gh-pages
git push origin gh-pages

# 2. Activar Pages via API apuntando a gh-pages
curl -X POST https://api.github.com/repos/OWNER/REPO/pages \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"branch":"gh-pages","source":{"branch":"gh-pages","path":"/"}}'

# 3. Esperar build y verificar
sleep 45
curl -sI https://OWNER.github.io/REPO/ | head -1
# → HTTP/2 200
```

**Ventajas sobre workflow de Actions:**
- Sin necesidad de crear `.github/workflows/pages.yml`
- Sin environment protection rules que puedan bloquear
- Sin `actions/deploy-pages@v4` que pueda fallar
- Build más rápido (GitHub Pages construye directamente el branch)

**Pitfall:** Si Pages ya estaba activado (por un workflow anterior), el `POST` devuelve 409 ("Pages is already enabled"). En ese caso, el branch gh-pages ya se usa y no hace falta la llamada API.

**Pitfall:** Si el workflow de Actions existe pero falla, el branch gh-pages sigue siendo una alternativa válida.

### 7.2 Workflow para sites estáticos

Crear `.github/workflows/pages.yml`:

```yaml
name: Desplegar a GitHub Pages
on:
  push:
    branches: ["master"]  # o "main"
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: "pages"
  cancel-in-progress: false
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
        id: deployment
```

**Pitfall:** Para sites estáticos HTML (sin build), crear `.nojekyll` en la raíz del repo para evitar que GitHub procese con Jekyll.

### 7.2 Vite + GitHub Pages con Service Worker (patrón crítico)

Cuando usas Vite para build + GH Pages para deploy, hay 4 problemas que se repiten:

#### 7.2.1 Service Worker no se despliega

Vite solo procesa lo que rollup toca. El SW (`sw.js`) existe en la raíz del repo pero **no se copia al `dist/`** automáticamente.

**Fix:** Añadir copia manual en `postbuild.js`:

```javascript
// postbuild.js
const swSrc = path.join(__dirname, 'sw.js');
const swDest = path.join(distDir, 'sw.js');
if (fs.existsSync(swSrc)) {
  fs.copyFileSync(swSrc, swDest);
}
```

Asegurar que `package.json` ejecuta postbuild:
```json
"build": "vite build && node postbuild.js"
```

#### 7.2.2 Ruta del SW — absoluta vs relativa

❌ `navigator.serviceWorker.register('/sw.js')` — busca en la raíz del dominio (`ntizar.github.io/sw.js`), no en el subpath del repo.

✅ `navigator.serviceWorker.register('./sw.js')` — busca relativo al path del sitio (`ntizar.github.io/SistemaElectricoFuturo/sw.js`), que es donde realmente está.

#### 7.2.3 STATIC_ASSETS desalineados con el build

El SW típicamente lista assets como `/css/app.css`, `/js/app.js`, etc. Pero tras un build de Vite:
- Los CSS pueden ir a `/assets/index-XXXX.css` (con hash)
- Los JS IIFE pueden estar en `/js/app.js` si se copian con postbuild
- Los CSS legacy pueden no existir si Vite los bundlea

**Fix:** STATIC_ASSETS del SW debe listar solo archivos que realmente existen en `dist/` después del build. Si el postbuild copia JS a `dist/js/`, las rutas en el SW deben coincidir.

```javascript
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/js/app.js',       // Solo si postbuild.js los copia
  // NO '/css/app.css' si Vite lo bundlea a /assets/index-XXXX.css
];
```

#### 7.2.4 SW cache addAll() → fail silencioso → app rota

Si `cache.addAll(STATIC_ASSETS)` encuentra un 404 (porque un asset listado no existe), **todo el `install` event falla**. El SW nuevo nunca se activa y el navegador sigue usando la caché vieja. Síntoma: fondo blanco, CSS/JS no cargan, hard refresh no funciona.

**Diagnóstico:** DevTools → Application → Service Workers → ver si el SW nuevo está en estado "waiting" o "errored". Mirar el output de `cache.addAll()`.

**Fix (3 pasos obligatorios):**
1. Eliminar referencias a assets que no existen en `dist/` del `STATIC_ASSETS`
2. **Bump CACHE_NAME** (ej. `v3.4` → `v4.1`) para forzar re-caché completo desde cero
3. Hard refresh (`Ctrl+Shift+R`) o Unregister en DevTools después del deploy

### 7.3 favicon.ico 404 en GitHub Pages

GitHub Pages busca `favicon.ico` en la raíz del dominio (`ntizar.github.io/favicon.ico`), no en el subpath del repo. Si no existe, aparece error 404 en consola.

**Fix:** Crear `favicon.svg` en el repo, añadirlo al `<head>`:
```html
<link rel="icon" type="image/svg+xml" href="favicon.svg">
```
Y copiarlo al `dist/` en el postbuild (igual que el SW).

### 7.4 CORS proxy para API externas en sitios estáticos

GitHub Pages es hosting estático — no hay backend para hacer proxy. Las APIs que no envían `Access-Control-Allow-Origin: *` no se pueden llamar directamente desde el navegador.

**Patrón:** Usar un proxy CORS público como intermediario:

```javascript
const rawUrl = `https://api-externa.com/data?param=value`;
const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent(rawUrl)}`;

fetch(proxyUrl)
  .then(r => r.text()) // IMPORTANTE: .text() no .json() (allorigins devuelve texto plano)
  .then(text => {
    const data = JSON.parse(text);
    // procesar...
  })
  .catch(() => null); // fallback silencioso
```

**Alternativas de proxy:**
- `https://api.allorigins.win/raw?url=...` ✅ probado
- `https://corsproxy.io/?url=...`
- `https://api.allorigins.win/get?url=...` (versión con metadata wrapper)

**⚠️ No asumir que el proxy devuelve JSON:** allorigins.win devuelve HTML plano a veces. Usar `.text()` + `JSON.parse()` para mejorar tolerancia.

### 7.5 Debugging de errores 404 en GitHub Pages

Cuando un sitio GH Pages muestra fondo blanco o faltan recursos, el flujo de diagnóstico es:

1. **curl a la página principal** → `curl -sI https://user.github.io/repo/` → verificar 200 OK
2. **curl a cada asset referenciado**:
   ```bash
   curl -sI https://user.github.io/repo/js/app.js | head -3
   curl -sI https://user.github.io/repo/assets/index-XXXX.css | head -3
   ```
3. **Inspeccionar el HTML servido** → `curl -s https://user.github.io/repo/ | grep -E '(script src|link.*css|sw\.js|favicon)'`
4. **Buscar rutas absolutas** en el HTML: `/css/...` en vez de `./css/...` o `/SistemaElectricoFuturo/css/...`
5. **Verificar Service Worker en DevTools** → Application → Service Workers → ver si cache.addAll() está fallando

**Causas comunes:**
- Ruta absoluta `/js/app.js` cuando el sitio está en un subpath → 404
- Vite genera `/assets/index-XXXX.css` sin prefijo del subpath → 404
- postbuild.js no copia assets necesarios (SW, favicon, CSS legacy)
- SW cacheado sirve assets viejos que ya no existen → **bump CACHE_NAME**


## 8. Repo Recovery

Cuando el remote fue reemplazado con un repositorio mínimo:
1. Backup local: `cp -r repo /tmp/repo-backup`
2. Reset local: `git reset --hard origin/main`
3. Restaurar backup: `rm -rf repo && cp -r /tmp/repo-backup repo`
4. Force push: `git push origin main --force`

**⚠️ Siempre backup primero.** Force push es destructivo.

---

## Linked Files

- `references/environment-protection-rules.md` — Pitfall con environment protection rules al renombrar branch
- `references/branch-merge-selectivo-mastermind.md` — Fusión inteligente de dos ramas
- `references/deploy-existing-repo.md` — **Verificar existencia de repo antes de crear** (nueva)

## 9. Branch Rename + GitHub Pages Reconfig

Al renombrar branch de `master` a `main`, hay 3 pasos obligatorios para que Pages siga funcionando:

### Paso 1: Actualizar workflow YAML
Cambiar `branches: ["master"]` → `branches: ["main"]` en `.github/workflows/pages.yml`.

### Paso 2: Actualizar Pages via API PUT
```python
import urllib.request, json

data = json.dumps({
    "source": {"branch": "main", "path": "/"},
    "build_type": "workflow"
}).encode()

req = urllib.request.Request(
    'https://api.github.com/repos/OWNER/REPO/pages',
    data=data,
    headers={
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    },
    method='PUT'  # PUT, no POST
)
urllib.request.urlopen(req)  # 204 = OK
```

### Paso 3: Dispatch manual del workflow
```python
data = json.dumps({"ref": "main"}).encode()
req = urllib.request.Request(
    'https://api.github.com/repos/OWNER/REPO/actions/workflows/PAGE-SLUG.yml/dispatches',
    data=data,
    headers={
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    },
    method='POST'
)
urllib.request.urlopen(req)  # 204 = dispatched
```

**Pitfall:** Si solo cambias el branch en el workflow pero no actualizas Pages via API, el deploy seguirá apuntando a `master` y fallará silenciosamente.

**Pitfall:** El workflow dispatch debe ser al archivo correcto (PAGE-SLUG.yml, no siempre "pages.yml").

## 10. GitHub Pages + environment protection rules (Pitfall crítico)

Cuando un workflow de GitHub Pages usa `environment: github-pages`, el entorno puede tener reglas de protección de rama (`deployment_branch_policy`) que solo permiten `master`. Al renombrar a `main`, el deploy falla con:

> `Branch "main" is not allowed to deploy to github-pages due to environment protection rules.`

**Diagnóstico:** El workflow termina en failure en 2-5 segundos (demasiado rápido para un deploy real). Revisar annotations del job.

**Solución A — Eliminar el entorno:**
```python
# DELETE /repos/{owner}/{repo}/environments/{env_name}
# Esto elimina las reglas de protección y permite deploy sin restricciones
```

**Solución B — Usar workflow sin environment:**
Quitar `environment:` del job en el workflow YAML. El deploy funcionará sin reglas de protección:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    # Sin environment:
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
          exclude: |
            .git/
            agents/
            .opencode/
            # ... ignorar archivos no-desplegables
      - uses: actions/deploy-pages@v4
```

**Pitfall:** Si el deploy tarda 2-5 segundos y termina en failure, es casi seguro un problema de environment protection rules, no de contenido.

**Pitfall:** `POST /repos/.../pages` con `build_type: "workflow"` requiere que el workflow use `actions/deploy-pages@v4`. Si el workflow no existe o no tiene este step, el deploy falla silenciosamente.

## 11. Deploy Pages para Repo EXISTENTE (caso más común)

**Antes de crear nada, verificar si el repo ya existe.**

### Flujo seguro

```bash
# 1. CLONAR PRIMERO — si el clone falla, el repo no existe
git clone https://github.com/Ntizar/nombre-repo.git
# Si falla → repo no existe → ir a sección 12 (crear desde cero)
# Si funciona → repo existe → continuar

# 2. Verificar si Pages ya está activo
curl -s https://api.github.com/repos/Ntizar/nombre-repo/pages \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" | jq '.html_url'
# → "https://Ntizar.github.io/nombre-repo/" = ya activo
# → 404 = Pages no configurado → activar con POST

# 3. Si Pages ya está activo → VERIFICAR QUE SIRVE
curl -s -o /dev/null -w "%{http_code}" https://Ntizar.github.io/nombre-repo/
# → 200 = OK, no hacer nada más
# → 404 = Pages activo pero build fallido → verificar workflow, trigger, etc.

# 4. Si Pages no está activo → activar
curl -s -X POST https://api.github.com/repos/Ntizar/nombre-repo/pages \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"source":{"branch":"main","path":"/"}}'
# → 409 = ya activo (conflicto con estado previo)
```

### Pitfalls críticos

- **NUNCA crear un repo nuevo sin verificar primero que no existe.** El nombre puede ser similar a otro existente (ej: `farospain` vs `farosspain`). Siempre intentar clonar primero.
- **Pages puede estar activo con build_type diferente** (workflow vs legacy). Verificar con la API antes de intentar reactivar.
- **El workflow de Pages puede existir pero no haber trigger.** Si el repo tiene `.github/workflows/pages.yml` pero no se ha hecho push a `main`/`master`, el build nunca se ejecuta.
- **Branch name:** Verificar si el repo usa `main` o `master` antes de activar Pages. El workflow YAML indica cuál.

### Checklist mental antes de actuar

1. ¿Repo existe? → `git clone` prueba
2. ¿Pages activo? → `GET /repos/.../pages`
3. ¿Sirve? → `curl -sI https://OWNER.github.io/REPO/`
4. Si todo OK → no hacer nada. Si algo falla → actuar.

---

## 12. Deploy Estático desde Cero (Repo Nuevo + Pages)

Cuando el usuario quiere crear un repositorio nuevo y desplegarlo en Pages desde cero (sin `gh` CLI):

### Flujo completo

```bash
# 1. Crear directorio y repo local
mkdir -p /path/to/newproject && cd /path/to/newproject
git init
# ... crear archivos (index.html, README.md, etc.) ...
git add -A && git commit -m "feat: initial commit"

# 2. Crear repo en GitHub vía API
curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"name":"repo-name","description":"Descripción","private":false}'

# 3. Conectar remote y push
git remote add origin https://github.com/Ntizar/repo-name.git
git push -u origin master

# 4. Activar GitHub Pages
curl -s -X POST https://api.github.com/repos/Ntizar/repo-name/pages \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d '{"source":{"branch":"master","path":"/"}}'

# 5. Verificar
sleep 15
curl -s -o /dev/null -w "%{http_code}" https://ntizar.github.io/repo-name/
# → 200 = OK
```

### Pitfalls

- **Token en URL:** NO usar `https://TOKEN@github.com/...` — los tokens tienen `/`, `+`, `=` que rompen parseo. Usar `git remote add origin https://github.com/Ntizar/REPO.git` (sin token) y dejar que git pida credenciales.
- **Pages tarda en construir:** El estado puede ser "building" tras el POST. Esperar 15-30s y verificar con `curl -sI https://OWNER.github.io/REPO/`.
- **Build con error null:** El estado "built" con `error: {message: null}` es normal en el build legacy de GitHub Pages — no bloquea el deploy.
- **index.html lowercase:** GitHub Pages solo sirve `index.html` (minúsculas). `INDEX.html` → 404 en root URL.

### Push con GITHUB_TOKEN (patrón que funciona)

El token de GitHub puede funcionar para la API REST pero **fallar con git credential store** o `credential.helper` normal. El patrón que funciona es:

```bash
source /hermes-home/.env
cd /path/to/repo
GIT_TERMINAL_PROMPT=0 git -c 'credential.helper=!f() { echo "username=oauth2"; echo "password='$GITHUB_TOKEN'"; }; f' push -u origin main
```

**Por qué funciona:** El `credential.helper` inline inyecta las credenciales directamente sin pasar por el sistema de credenciales de git. `oauth2` como username es el formato que GitHub espera para tokens.

**Pitfall:** El primer push puede funcionar pero los siguientes fallan si el credential helper se resetea. Siempre usar el mismo patrón con `-c 'credential.helper=...'` en cada push.

**Pitfall:** Si el token es de instalación (no user token), puede funcionar con la API pero NO con git. Verificar con `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user` — si devuelve 200, funciona para ambas cosas.

## 13. Branch Merge Selectivo — Fusión Inteligente de Dos Ramas

**Ver referencia:** `references/branch-merge-selectivo-mastermind.md` para el caso completo.

Cuando dos ramas tienen fortalezas complementarias (una con mejor diseño, otra con contenido más actualizado), el `git merge` directo no sirve. Patrón:

### Resumen rápido

```bash
# 1. Inventario
git ls-tree -r --name-only master | sort > /tmp/m.txt
git ls-tree -r --name-only main | sort > /tmp/mn.txt
comm -23 /tmp/m.txt /tmp/mn.txt  # solo en master
comm -13 /tmp/m.txt /tmp/mn.txt  # solo en main

# 2. Clasificar por archivo: ¿master, main, o fusión manual?
# 3. Ejecutar fusión manual (reemplazos + limpieza)
# 4. Verificar: search_files('obsidian|opencode', path='.')
# 5. Actualizar GitHub description vía API REST
```

### Decisiones típicas por archivo

| Archivo | Decisión | Razón |
|---------|----------|-------|
| `README.md` | Fusión manual | Diseño de master + contenido de main |
| `index.html` | Fusión manual | Diseño de master + limpiar legacy |
| `SOUL.md`, `AGENTS.md`, `CHANGELOG.md` | ✅ main | Solo existen en la versión actual |
| Archivos únicos de master | mover a `legacy/` o eliminar según relevancia |

### Fallos comunes del merge automático

- `git merge` con `--strategy-option=theirs` solo funciona si no hay cambios en el working tree
- `Already up to date` si main ya absorbió master via rebase → hay que hacer fusión manual
- Archivos que cambian de nombre entre ramas (e.g. `agents/` → `legacy/agents/`) → el merge no detecta la relación

### Pitfalls específicos

- **NUNCA eliminar branches sin preguntar** — el usuario puede preferir el diseño de una rama aunque otra tenga el contenido más reciente
- **GitHub description** se actualiza vía `PATCH /repos/{owner}/{repo}` con token, NO está en el repo
- **CDN Aurora** → siempre `@latest`, NUNCA `@master`
- **Referencias residuales** → escanear con `search_files` nombres de plataforma antigua en TODOS los archivos activos (excluyendo `legacy/`)