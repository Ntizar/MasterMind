---
name: devops-operations
description: "Patrones operativos de DevOps: deploy en NaN.builders (502, cache, env vars), cron jobs con scripts (no_agent=True), pipeline de digest estático, y GitHub Pages deployment. Todo para mantener apps en producción."
version: 1.2.0
author: Hermes Agent
tags: [devops, nan, deploy, cron, scripts, automation, production, github-pages]
---

# DevOps Operations — Patrones de Producción

Patrones operativos para mantener aplicaciones en producción.

## Tabla de Contenidos

0. [Código → NaN: Push y Verificación](#0-código--nan-flujo-de-push-y-verificación) — edit → commit → pull --rebase → push → verify
1. [NaN Deploy Troubleshooting](#1-nan-deploy-troubleshooting) — 502, cache, TDZ, OOM
2. [Cron Jobs con Scripts](#2-cron-jobs-con-scripts) — no_agent=True, Python scripts
3. [Static Digest Pipeline](#3-static-digest-pipeline) — Fetch API → scoring → JSON → HTML → Pages
4. [GitHub Pages + Vite](#4-github-pages--vite) — base path, crossorigin, deploys

---

## 0. Código → NaN: Flujo de Push y Verificación

**⚠️ Regla de oro: Después de modificar código de un app desplegada en NaN, el trabajo NO está completo hasta que el push y la verificación en producción están hechos.**

El flujo completo para cualquier cambio de código en apps NaN:

```
[1] Hacer cambios en local (dashboard.html, server.js, etc.)
[2] Verificar que funcionan localmente (curl localhost, revisar sintaxis)
[3] git add -A && git commit -m "fix: descripción clara"
[4] git pull --rebase origin main   ← CRÍTICO: la app auto-commitea database.json vía syncGitHub
[5] git push origin main
[6] Esperar ~2 min a que NaN detecte el push y redeployee
[7] Verificar en producción: curl -s https://<app>.apps.nan.builders/healthz
[8] Verificar el cambio específico: curl endpoint, grep en HTML, etc.
```

**Pitfall: `git push` rechazado por cambios remotos**
- La app tiene `syncGitHub()` que auto-commitea `data/database.json` tras cada mutación
- El repo local se queda detrás del remoto
- **Siempre hacer `git pull --rebase` antes de push** (nunca merge — mantiene historia limpia)
- Síntoma: `! [rejected] main -> main (fetch first)`

**Pitfall: No verificar en producción**
- NaN tiene polling de ~1-5 min y cache de Cloudflare
- Un push exitoso no significa que el cambio esté servido
- **Siempre verificar con curl** antes de decir "está listo":
  ```bash
  curl -s https://<app>.apps.nan.builders/ | grep "cambio esperado"
  # O para APIs:
  curl -s https://<app>.apps.nan.builders/api/entrenamientos/0 | python3 -c "import sys,json; print(json.load(sys.stdin))"
  ```
- Si el cambio no está vivo tras 3 min, forzar con `git commit --allow-empty -m "chore: trigger redeploy" && git push`

**Pitfall: Asumir que el HTML se actualiza automáticamente**
- NaN reconstruye el contenedor completo con Kaniko
- Los archivos estáticos (HTML, CSS, JS) están dentro de la imagen Docker
- No hay hot-reload — cada cambio requiere nuevo build
- Tiempo típico build+deploy: 1-5 min

**🔥 Health check que miente: key existe pero no funciona**

**Patrón común:** El endpoint `/healthz` verifica que la variable de entorno `ORS_API_KEY` exista en `.env` (string truthy check), pero NO hace una llamada real a la API para verificar que la key sea válida.

**Síntoma:** `curl /healthz` devuelve `{"ors_api": true}` pero las llamadas reales a la API retornan `403 Access disallowed` o `401 Unauthorized`.

**Fix:** El healthcheck debe hacer una llamada real (o al menos validar el formato de la key) además de verificar que exista:
```javascript
// ❌ Miente: solo verifica que exista
checks.ors_api = !!process.env.ORS_API_KEY;

// ✅ Real: verifica que la key funcione (llamada mínima)
const testResp = await fetch('https://api.openrouteservice.org/v2/isochrones/driving-car', {
  method: 'POST',
  headers: { 'Authorization': process.env.ORS_API_KEY, 'Content-Type': 'application/json' },
  body: JSON.stringify({ locations: [[0,0]], range: [1] })
});
checks.ors_api = testResp.ok;
```

**Pitfall:** Hacer la llamada real en cada request de healthcheck es lento (200-500ms). Mejor cachear el resultado y re-validar cada 5 minutos.

**🔥 .env loader manual en Node.js (sin dotenv)**

**Patrón:** Node.js NO carga `.env` automáticamente (salvo `--env-file=.env` en Node 20.6+). Si no quieres dependencia de dotenv, añade un loader manual al inicio de `server.mjs`:

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf-8');
  for (const line of envContent.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx > 0) {
      const key = trimmed.slice(0, eqIdx).trim();
      const val = trimmed.slice(eqIdx + 1).trim();
      if (!process.env[key]) process.env[key] = val; // NO sobreescribe
    }
  }
}
```

**Pitfall:** El loader SOLO carga variables que NO existen en `process.env`. Si haces `source .env` en bash ANTES de lanzar el servidor, las variables ya existen y el loader las ignora. Para testing: simplemente `node server.mjs` (el loader hace el trabajo).

**🔥 Git push falla por archivos grandes (OOM)**

**Patrón:** Proyectos con datos generados (GTFS, JSON grandes, caches) pueden acumular cientos de MB en `data/`. Git intenta hacer push de todo el history y muere con `pack-objects died of signal 9` (OOM en VMs con 2GB RAM).

**Síntoma:** `git push` falla con `pack-objects died of signal 9` o `remote end hung up unexpectedly`.

**Fix inmediato:**
```bash
# 1. Añadir al .gitignore
echo -e "\ndata/gtfs/\ndata/gtfs-cache/\n*.json\n!data/ciudades-*.json\n!data/codigos-postales-spain.json" >> .gitignore

# 2. Quitar del tracking (mantiene archivos locales)
git rm -r --cached data/gtfs/ data/gtfs-cache/
git rm --cached data/poblacion-cp.json data/salarios-*.json data/precios-vivienda.json

# 3. Commit y push
git add -A && git commit -m "chore: remove large data files from tracking"
git push origin main
```

**Si el history es demasiado grande (>100MB):** Crear repo fresco con solo código fuente:
```bash
cd /tmp && mkdir fresh-repo && cd fresh-repo && git init
cp -r /path/to/original/js . && cp -r /path/to/original/css .
cp /path/to/original/server.mjs /path/to/original/index.html .
# ... copiar solo archivos necesarios
git remote add origin <url> && git push --force origin main
```

**Prevención:** SIEMPRE añadir `data/` grande a `.gitignore` ANTES del primer commit. Los archivos GTFS raw pueden ocupar 750MB+.

## 1. NaN Deploy Troubleshooting

**TDZ (Temporal Dead Zone) — #1 causa de 502:**
- `const`/`let` usada antes de declaración → crash silencioso → Cloudflare 502
- Prevention: ordenar todas las `const` al inicio de la función

**NaN cachea contenedor Docker:**
- Después de cambios JS/CSS, NaN puede servir versión antigua durante horas
- Soluciones: cambiar Dockerfile → renombrar repo → eliminar/recrear espacio

**Scripts de verificación:**
- `verify-nan-deploy.sh <base-url>` — compara hashes MD5 locales vs remotos
- `git commit --allow-empty -m "chore: trigger redeploy" && git push` — trigger de redeploy

**Server crash silencioso:**
- Container "Running" pero endpoints devuelven 502 con ~3-4s
- Fix: `process.on('uncaughtException')` + fallback en route handlers

**🔥 Browser tool cache agresivo — HTML nuevo no se sirve**

**Error real (2026-06-11):** Tras hacer commit+push y redeploy en NaN, el browser tool seguía sirviendo HTML con JS antiguo. `typeof THREE === 'undefined'` aunque el CDN estaba en el HTML nuevo. El browser tool cachea el HTML y los scripts inline agresivamente.

**Síntoma:** `curl` desde terminal muestra HTML nuevo, pero `browser_console(expression='typeof THREE')` devuelve `undefined`. Los scripts CDN aparecen en el HTML pero no se ejecutan.

**Soluciones (en orden de efectividad):**
1. **Forzar redeploy** con un commit mínimo en `database.json` (o cualquier archivo servido por el server) → invalida cache de NaN
2. **Navegar con timestamp**: `browser_navigate(url + '?t=' + Date.now())` — fuerza recarga del HTML
3. **Esperar 2-3 minutos** — el cache de Cloudflare/NaN se expira
4. **Verificar con curl** antes de confiar en el browser tool: `curl -s https://app.apps.nan.builders/ | grep 'three.min.js'`

**Regla:** Si el HTML sirve correctamente (verificado con curl) pero el browser tool muestra comportamiento antiguo → es cache. No buscar bugs donde no los hay.

**Puerto del Dockerfile ≠ Container port de NaN — causa común de 502:**
- NaN tiene un campo **Container port** en la config del espacio (Settings > Container port)
- Si el servidor escucha en otro puerto (ej. 3000) pero NaN espera 7070 → 502 inmediato
- Fix: sincronizar ambos. Opción A: cambiar `ENV PORT=7070` + `EXPOSE 7070` en Dockerfile. Opción B: cambiar Container port en NaN a 3000
- **Recomendado:** Opción A (Dockerfile), así el build es autónomo y no depende de config manual de NaN
- Verificar: `curl -s -o /dev/null -w "%{http_code}" https://<app>.apps.nan.builders/` debe dar 200 tras el build

**Dockerfile faltante — error silencioso de Kaniko:**
- NaN usa Kaniko para construir imágenes Docker. Si el repo no tiene `Dockerfile` en la raíz, el build falla con: `Error: error resolving dockerfile path: please provide a valid path to a Dockerfile within the build context with --dockerfile`
- **Síntoma:** el build history muestra "failed" sin mensaje claro de error, solo el usage de Kaniko
- **Fix:** crear `Dockerfile` en la raíz del repo antes de conectar NaN. Mínimo viable:
  ```dockerfile
  FROM node:20-alpine
  WORKDIR /app
  COPY package.json package-lock.json ./
  RUN npm ci --only=production
  COPY . .
  EXPOSE 4040
  CMD ["node", "server.js"]
  ```
- **Pitfall:** si el repo se conectó a NaN antes de tener Dockerfile, NaN no lo detecta retroactivamente. Hay que hacer un push nuevo para triggerear el build.
- **Pitfall:** `npm ci` requiere `package-lock.json`. Si no existe, usar `npm install` en su lugar.
- **Pitfall:** no incluir `node_modules/` en `.gitignore` hace que el build suba 600+ archivos innecesarios (como pasó con el primer push del Mastermind Dashboard). Añadir `.gitignore` con `node_modules/` y hacer `git rm -r --cached node_modules` para limpiar.

**NaN build succeeded pero deployment stuck en "pending":**
- A veces el build de Kaniko termina con éxito (imagen creada en registry) pero NaN no despliega el contenedor y se queda en estado "pending" indefinidamente.
- **Síntoma:** build history muestra "succeeded" con imagen, pero la URL pública da 404 y el status de la app es "pending".
- **Causa probable:** NaN no asigna recursos al contenedor (problema de orquestación interna) o el webhook de deploy no se dispara tras el build.
- **Fixes:**
  1. Desde la UI de NaN, darle a **"Deploy"** o **"Restart"** manualmente
  2. Cambiar el **Container port** en Settings y hacer deploy de nuevo (fuerza re-asignación)
  3. Cambiar el puerto en el código (`server.js` + `Dockerfile`), pushear, y esperar nuevo build+deploy
  4. Si nada funciona, borrar la app y crearla de nuevo desde cero
- **Prevención:** no hay forma segura de evitarlo — es un problema de la plataforma NaN, no del código.

**Dashboard dual: local backend + NaN frontend:**
- El dashboard de control (monitorización del sistema) tiene dos caras:
  - **Local** (microVM, puerto 4040): backend con datos reales del sistema (CPU, RAM, procesos, ChromaDB, crons). Usa `execSync`, `os`, `fs` para datos en vivo.
  - **NaN** (contenedor): versión visual que consume APIs del local. Como el contenedor no ve el sistema real, los endpoints deben tener fallbacks graceful (try/catch con datos de ejemplo).
- **Flujo de creación:**
  1. Desarrollar y testear localmente primero (el microVM tiene todos los datos reales)
  2. Crear Dockerfile y subir a GitHub
  3. Conectar repo a NaN como app
  4. El contenedor de NaN no tiene acceso a ChromaDB local → el endpoint `/api/skills` debe devolver `{ status: 'disconnected' }` gracefulmente
  5. El contenedor de NaN no ve procesos del host → `/api/processes` debe tener fallback
- **Puerto:** elegir uno que no choque con otras apps. El puerto 4000 está ocupado por el ESIOS Dashboard (u otro proyecto de David). Usar 4040 o 6060 para nuevos dashboards.
- **Auth:** Basic Auth con contraseña vía env var `DASH_PASSWORD`
- **Auto-refresh:** frontend con `setInterval(fetch, 5000)` para datos en vivo
- **Repo privado:** `github.com/Ntizar/Mastermind-Dashboard`
- **Flujo de creación de dashboard desde cero:**
  1. Crear repo privado en GitHub via API REST (`curl -X POST -H "Authorization: token $GITHUB_TOKEN" ...`)
  2. Inicializar git local, hacer primer commit, pushear
  3. Desarrollar backend (Express) y frontend (HTML+CSS+JS) localmente
  4. Testear en localhost con datos reales del microVM
  5. Crear Dockerfile y entrypoint.sh
  6. Pushear todo → NaN detecta el push y construye automáticamente
  7. **Cuidado:** el primer push NO debe incluir `node_modules/` — añadir `.gitignore` antes del primer commit o limpiar con `git rm -r --cached node_modules` después
  8. **Cuidado:** el Dockerfile debe estar en el repo ANTES de que NaN intente construir, o el build fallará con "Dockerfile not found"

**Infinite recursion → OOM:**
- 4GB RAM hard limit, sin swap
- Fix: reemplazar recursión con fetch único

**🔥 Verificar que `patch` realmente modificó el archivo**

El tool `patch` puede reportar éxito sin modificar el archivo (fuzzy matching no encontró el string exacto, o el archivo fue leído parcialmente con offset/limit). Siempre verificar después de cada patch:

```bash
# Verificar que el archivo cambió
git diff --stat
# O verificar contenido específico
grep "nuevo_contenido" js/archivo.js
```

**Síntoma:** `patch` dice `success: true` pero el archivo en disco sigue igual. El commit pusha código viejo. El deploy sirve versión obsoleta. Bugs "fantasma" que no se explican.

**Fix:** Si el patch no aplicó, usar `write_file` para reescribir el archivo completo en vez de intentar otro patch. Es más seguro para archivos pequeños (<500 líneas).

## 8. Cron Jobs con Scripts

**⚠️ `cronjob` tool no disponible en esta VM:**
- El `cronjob` tool no existe en el entorno actual — no hay `crontab`, no hay daemon cron, no hay systemd timers
- Los scripts de mantenimiento se guardan en `/hermes-home/scripts/` y se ejecutan manualmente o desde un cron externo (SSH desde otra máquina)
- Para automatizar: configurar cron en máquina local que SSH al VM, o usar systemd timer en el VM
- Ejemplo: script `/hermes-home/scripts/mastermind-weekly-maintenance.sh` (Domingo 05:00 UTC)

**Patrón de scripts de mantenimiento:**
- Script en `/hermes-home/scripts/` con shebang `#!/bin/bash`
- Script usa `set -e` y loguea a `/var/log/<name>.log`
- Script incluye health checks antes y después de cada paso
- Script hace `git add -A && git commit && git push` al final

**Pitfalls:**
- Script path: SOLO nombre de archivo (el scheduler añade el prefix)
- Schedule usa UTC
- Scripts ejecutan en sesión aislada → no tienen contexto de chat
- Scripts deben incluir retry logic para APIs externas (3 intentos, 2s delay)
- **No usar `cronjob` tool** — no existe en esta VM. Crear scripts bash ejecutables manualmente.

## 3. Static Digest Pipeline

Pipeline para feeds periódicos:
1. Fetch API externa
2. Normalización y scoring heurístico
3. Generar JSON + HTML
4. Deploy a GitHub Pages

Ver skill `devops/static-digest-pipeline` para la implementación completa.

## 4. Deploy Audit — Verificación de despliegues

Procedimiento sistemático para auditar y verificar despliegues en NaN.builders.

### Pasos
1. Descargar deploy remoto y comparar con local (`diff`)
2. `grep -c` por elementos clave en ambos archivos
3. Verificar git status y últimos commits
4. Verificar endpoints secundarios

### Checklist de integridad HTML
- [ ] `loadData()` definida y llamada
- [ ] `renderDashboard()` definida
- [ ] Hero quick status (heroPeso, heroPerdido, heroRitmo)
- [ ] Botones de acción rápida con `switchTab`
- [ ] Tabs con `display:none` excepto tab activo
- [ ] Sin código de dark mode residual

### Pitfalls
- NaN bloquea curl desde ciertas IPs (403) → usar `curl -A "Mozilla"`
- Tamaños iguales ≠ contenido idéntico → usar `diff`

## 5. Error 502 por desajuste de puertos

NaN.builders tiene **3 lugares donde se define el puerto**, y deben coincidir:

| Lugar | Dónde está | Ejemplo |
|---|---|---|
| **Container Port** | UI de NaN → Settings del espacio | `6060` |
| **`EXPOSE`** | `Dockerfile` | `EXPOSE 6060` |
| **`process.env.PORT`** | `server.js` | `const PORT = process.env.PORT || 6060` |

### Diagnóstico rápido
```bash
grep EXPOSE Dockerfile
grep 'PORT' server.js
grep -A2 HEALTHCHECK Dockerfile
```

### Fix recomendado
Alinear todo al Container Port de NaN. O escuchar en ambos puertos (tolerante a cambios).

### Healthcheck: regla de oro
El HEALTHCHECK NUNCA debe apuntar a un endpoint protegido por auth. Crear `/healthz` ANTES del middleware de auth.

### NaN containers están AISLADOS del host
No pueden ver procesos, crons, skills, sessions ni archivos del host. Sincronizar datos vía Git.

## 6. Aurora Nightly — Mejora Continua Nocturna

Pipeline de 4 jobs nocturnos para mejora continua del CSS Aurora:
- Job #1 (01:00): Investigación web de tendencias CSS
- Job #2 (02:00): Análisis gap + Mejora CSS #1
- Job #3 (03:00): Mejora CSS #2
- Job #4 (04:00): Mejora CSS #3 + Reaprendizaje

Ver `aurora-nightly` para el procedimiento completo con investigación RSS, patrones de mejora CSS, y pitfall de no reescribir packs enteros.

### GitHub Actions Nightly Pipeline
Para proyectos con CI/CD: lint → build → test → deploy en cron nocturno. Ver `aurora-nightly-pipeline` para el workflow YAML completo.

## 7. GitHub Pages + Vite

Pitfalls comunes al desplegar proyectos Vite en GitHub Pages. Referencia completa: `references/vite-github-pages-deploy.md`.

**Checklist rápida:**
- [ ] `vite.config.js` tiene `base: '/RepoName/'` (coincide con el repo)
- [ ] No hay `crossorigin` en `<script>` ni `<link>` del HTML build
- [ ] El JS fuente no tiene strings sin cerrar (comillas simples sin par)
- [ ] GitHub Pages activado y build desplegado en `gh-pages`
- [ ] El repo es público (requisito en plan free)

**🔥 GitHub Pages CDN cachea JS agresivamente — versión vieja tras push**

**Causa:** GitHub Pages usa un CDN (Fastly/Cloudflare) que cachea archivos estáticos (JS, CSS) con `max-age` prolongado. Cuando haces push con cambios en JS, el CDN puede seguir sirviendo la versión vieja durante minutos. El `curl` desde terminal sirve el HTML nuevo, pero los archivos JS referenciados en el HTML siguen siendo los viejos.

**Síntomas:**
- `curl -s https://user.github.io/repo/` muestra HTML con `<script src="js/main.js?v=1">` (nuevo)
- Pero el contenido de `js/main.js?v=1` es la versión vieja (el CDN no invalidó)
- El navegador ejecuta código JS obsoleto → NaN, bugs fantasma
- Los features nuevos no aparecen aunque el commit está en main

**Fix: Cache busting con version query en script tags**

```html
<!-- ❌ MAL — CDN cachea el archivo sin version -->
<script type="module" src="js/main.js"></script>

<!-- ✅ BIEN — version query fuerza descarga nueva -->
<script type="module" src="js/main.js?v=4"></script>
```

**Patrón:** Incrementar `?v=N` en CADA push que modifique JS/CSS:
```html
<script type="module" src="js/main.js?v=4"></script>
<link rel="stylesheet" href="css/style.css?v=3">
```

**Verificación de que el browser cargó la versión nueva:**
```javascript
// En browser console:
document.querySelectorAll('script[type="module"]')[0].src
// Debe mostrar "?v=4" (la versión nueva), no "?v=1" (la vieja)
```

**Verificación de que el CDN sirve el contenido nuevo:**
```bash
# El HTML puede estar cacheado — verificar el JS directamente
curl -s "https://user.github.io/repo/js/main.js?v=4" | head -5
# Debe mostrar el código nuevo, no el viejo
```

**Pitfall: HTML cacheado por el browser**
A veces el browser cachea el HTML mismo (no solo el JS). Aunque el CDN tiene el HTML nuevo, el browser sigue con el viejo. Fix: `?t=timestamp` en la URL del HTML:
```
https://user.github.io/repo/index.html?t=20260630
```
O hard refresh: `Ctrl+Shift+R` / `Cmd+Shift+R`.

**Pitfall: `curl` sirve nuevo pero browser sirve viejo**
El curl bypassa el browser cache pero no el CDN cache. Si `curl` muestra el HTML nuevo pero el browser no, es browser cache. Si `curl` también muestra viejo, es CDN cache (esperar 2-5 min o forzar con otro push).

**🔥 GitHub Pages NO funciona en repos privados con plan free**

**2026-06-18 (AtlasMadrid2024):** `POST /repos/{owner}/{repo}/pages` devuelve 422: "Your current plan does not support GitHub Pages for this repository." Incluso tras crear el sitio de Pages vía API, el workflow de GitHub Actions falla en "Setup Pages" con el mismo error.

**Fix:** Cambiar el repo a público antes de activar Pages:
```bash
curl -X PATCH -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/OWNER/REPO" \
  -d '{"private":false}'
# Esperar ~5 segundos
curl -X POST -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/pages" \
  -d '{"build_type":"workflow","source":{"branch":"main","path":"/"}}'
```

**Workflows que fallan sin Pages habilitado:** El step "Setup Pages" (`actions/configure-pages@v5`) falla → "Upload artifact" y "Deploy" se saltan. No hay error claro de "Pages not enabled" — solo falla genérica.

**Detección:** Si el workflow falla en "Setup Pages" y el repo es privado → Pages no está soportado en este plan.

**Alternativa si no se puede hacer público:** Deploy manual a `gh-pages` branch con `git subtree` o deploy a otro hosting (NaN.builders, Vercel, Netlify).

**Patrón de deploy manual (cuando no hay GitHub Actions):**
```bash
npm run build
sed -i 's/ crossorigin//g' dist/index.html
git init /tmp/gh-deploy && cp -r dist/* /tmp/gh-deploy/
git -C /tmp/gh-deploy remote add origin https://github.com/USER/REPO.git
git -C /tmp/gh-deploy push origin master:gh-pages --force
```
