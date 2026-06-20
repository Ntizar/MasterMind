---
name: esios-nan-deploy
description: "Procedimiento de deploy de proyectos Node.js en NaN.builders — Dockerfile, Kaniko, variables de entorno, puertos y troubleshooting."
version: 2.5.0
author: Ntizar
tags: [esios, deploy, nan, docker]
related_skills: [nan-puerto-desajuste, nan-pending-root-cause]

---

# Deploy en NaN.builders

Guía para desplegar proyectos Node.js en la plataforma NaN.builders (microVMs KVM/QEMU).

## Estructura del deploy

1. **Push a GitHub** → NaN detecta el cambio y hace build con Kaniko
2. **Kaniko build** → construye la imagen Docker sin daemon
3. **Auto-deploy** → si el build funciona, se despliega automáticamente

### Patrón de archivos .env (CRÍTICO)

Cada proyecto necesita estos 3 archivos:

```
proyecto/
├── .env              ← local, NO en Git (desarrollo)
├── .env.example      ← SÍ en Git (documentación de variables)
├── .dockerignore     ← excluye node_modules, .git (NO .env — se copia en contenedor)
└── .gitignore        ← excluye .env
```

**⚠️ Pitfall: `NAN_API` no se hereda en el contenedor de NaN**

Las variables de entorno del host (`process.env.NAN_API` en la sesión de Hermes) **NO están disponibles dentro del contenedor Docker de NaN**. El contenedor solo tiene:
1. Variables configuradas en la pestaña **Env** del dashboard NaN
2. Variables copiadas desde archivos del proyecto (`.env` copiado por `COPY . .`)

**Patrón de fallback para tokens API** (implementado en server.js de dieta):
```javascript
function getNanToken() {
  // 1) process.env.NAN_API (NaN dashboard Env)
  if (process.env.NAN_API) return process.env.NAN_API;
  // 2) NTIZAR_API (otro nombre posible)
  if (process.env.NTIZAR_API) return process.env.NTIZAR_API;
  // 3) Leer .env del proyecto (fallback local)
  try {
    const envContent = fs.readFileSync(path.join(__dirname, '.env'), 'utf8');
    const match = envContent.match(/^NAN_API=(.+)$/m);
    if (match) return match[1].trim();
  } catch (e) {}
  return '';
}
```

**Configuración para deploy:**
- Crear `.env` con el token real en el directorio del proyecto
- Añadir `.env` a `.gitignore` (NUNCA subir a Git)
- **NO** añadir `.env` a `.dockerignore` (se necesita en el contenedor)
- El Dockerfile `COPY . .` lo copiará automáticamente

**.env.example** — template con nombres y placeholders:
```
ESIOS_API_TOKEN=tu_token_aqui
PORT=4000
NAN_API_KEY=tu_clave_aqui
```

**.env** — valores reales (solo local):
```
ESIOS_API_TOKEN=abc123...
PORT=4000
```

### Dónde configurar variables en producción
- **NaN:** pestaña **Env** en la web de NaN → dashboard del espacio
- **NUNCA** en el código, commits, o .env en Git
- Se acceden via `process.env.VAR_NAME` en Node.js

### Validación en código (3 patrones)

**Patrón A — Exit early (recomendado para obligatorias):**
```javascript
// src/config/env.js
const REQUIRED = ['ESIOS_API_TOKEN'];
function loadEnv() {
  const missing = REQUIRED.filter(k => !process.env[k]);
  if (missing.length > 0) { console.error(`Faltan: ${missing.join(', ')}`); process.exit(1); }
  return { ESIOS_TOKEN: process.env.ESIOS_API_TOKEN, ... };
}
```

**Patrón B — Health endpoint con checks:**
```javascript
app.get('/readyz', (req, res) => {
  const esiosReady = Boolean(process.env.ESIOS_API_TOKEN);
  res.status(esiosReady ? 200 : 503).json({
    status: esiosReady ? 'ready' : 'degraded',
    checks: { esios_api_token: esiosReady }
  });
});
```

**Patrón C — Fallback con generación temporal:**
```javascript
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD
  || crypto.randomBytes(24).toString('base64url'); // Temporal
```

## Dockerfile mínimo para NaN

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=4000

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=deps --chown=appuser:appgroup /app/node_modules ./node_modules
COPY package.json ./
COPY server.js ./
COPY src/ ./src/
COPY public/ ./public/
COPY data/ ./data/

USER appuser
EXPOSE 4000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:4000/healthz || exit 1
CMD ["node", "server.js"]
```

## 🚧 Primer deploy: crear el espacio en NaN

Antes de que cualquier URL funcione, **hay que crear el espacio en la web de NaN**:

1. Ir a [cloud.nan.builders](https://cloud.nan.builders) e iniciar sesión
2. Crear un nuevo **Space** apuntando al repositorio GitHub
3. Configurar el puerto (debe coincidir con `EXPOSE` del Dockerfile)
4. El espacio tarda segundos en aprovisionarse

**Síntoma de espacio no creado:** La URL (`<app>-<org>-<project>.apps.nan.builders`) devuelve **404 directamente de Cloudflare** (no 502, no timeout). El DNS resuelve a IPs de Cloudflare pero no hay backend.

> ⚠️ No basta con tener el Dockerfile en el repo. **El espacio debe existir en NaN** para que el auto-deploy por polling funcione. Sin espacio, el push a GitHub no tiene efecto visible.

### Patrón de URL

NaN.builders asigna URLs con el patrón:
```
<app-name>-<owner>-<owner>.apps.nan.builders
```
Donde `app-name` es el nombre del espacio en NaN, y `owner` es el usuario/organización de GitHub. El owner aparece **duplicado** en la URL.

### Opciones de hosting alternativas

Si el espacio NaN aún no existe y la URL es urgente:

| Opción | Requisito | Comando |
|--------|-----------|---------|
| **GitHub Pages** | Repo público (o plan pago para privado) | `gh repo edit --visibility public && gh api -X POST repos/:owner/:repo/pages -f source.branch=gh-pages` |
| **Surge.sh** | Login interactivo (email + password) primero | `npm i -g surge && surge ./dist nombre.surge.sh` |
| **Vercel/Netlify** | Login vía CLI | `npx vercel deploy --prebuilt --prod` |

### ⚠️ `.env` en `.dockerignore` mata tokens de API

Si añades `.env` a `.dockerignore`, el archivo NO se copia al contenedor Docker. El servidor arranca pero `process.env.NAN_API` no existe (NaN no hereda env vars del host) y el fallback a `.env` local también falla (no está en el contenedor). **Todos los endpoints de IA (estimación comida, ejercicio, coach) devuelven "Token no configurado".**

**Síntoma:** App funciona, login OK, datos se guardan, pero todo lo que usa IA falla silenciosamente.

**Fix:** Quitar `.env` de `.dockerignore`. El `.env` DEBE estar en el contenedor para que el fallback `fs.readFileSync('.env')` funcione. El `.env` ya está en `.gitignore` (no se sube a GitHub), pero el `COPY . .` del Dockerfile lo copia al contenedor.

```dockerignore
# ❌ MAL — .env no llega al contenedor
node_modules/
.env

# ✅ BIEN — .env se copia al contenedor
node_modules/
.git
.gitignore
```

### ⚠️ CRÍTICO: `"type": "module"` + `require()` = crash silencioso

Si `package.json` tiene `"type": "module"`, Node.js ejecuta TODOS los `.js` como ESM. Si el server usa `require()` (CommonJS), el contenedor **crashea al arrancar** y el pod se queda en `Pending` — **sin error visible en el dashboard de NaN**.

**Síntomas:** Build Kaniko exitoso, `Current Image` se llena, pero URL siempre devuelve 503 o 404.

**Causa típica:** Dockerfile con `RUN echo 'require("http")...' > server.js` (inline CommonJS) en un proyecto Vite que tiene `"type": "module"`.

**Fix:** 
1. Crear `server.mjs` como archivo separado en el repo (ESM puro: `import http from "node:http"`)
2. Usar `COPY --chown=appuser:appgroup server.mjs ./` en el Dockerfile
3. Cambiar `CMD ["node", "server.js"]` → `CMD ["node", "server.mjs"]`
4. **NUNCA** hacer `echo 'require(...)' > server.js` en un proyecto con `"type": "module"`

**Verificación:** `grep '"type"' package.json` + `grep 'require(' server.js` — si ambos dan resultado, hay conflicto ESM/CJS.

### Puerto
- El espacio de NaN puede estar configurado en cualquier puerto (3500, 3700, 4000, 4500, 6000, etc.)
- **El Dockerfile EXPOSE debe coincidir con el puerto del espacio**
- **El server.js debe usar `process.env.PORT || <puerto>` como default**
- **Para sitios estáticos con nginx: el EXPOSE y el `listen` en nginx.conf deben coincidir** — no asumir que nginx escucha en 80 por defecto
- Si no coinciden → 502 Bad Gateway
- ⚠️ **NUNCA intentar escuchar en puerto 80 desde un contenedor no-root**. Cuando el Dockerfile usa `USER appuser` (que es obligatorio), el bind a puerto 80 **falla silenciosamente** — Node.js no levanta, el proceso muere, y el pod se queda en Pending. **Solo escuchar en el puerto configurado**: `http.createServer(handler).listen(process.env.PORT || 3700, "0.0.0.0")`
- **HEALTHCHECK debe apuntar al puerto configurado**, no a 80: `CMD wget -qO- http://localhost:3700/healthz || exit 1`

### Usuario no-root (crítico)
- **NaN BLOQUEA contenedores que ejecutan como root** — el pod se queda en "Pending" indefinidamente aunque Kaniko construya la imagen correctamente
- **Siempre crear usuario no-root**: `RUN addgroup -S appgroup && adduser -S appuser -G appgroup`
- **Siempre cambiar antes del CMD**: `USER appuser`
- **Ajustar permisos** de todos los archivos copiados: `RUN chown -R appuser:appgroup /app`
- Es el **mismo patrón** indispensable que usa esios-dashboard
- Síntoma: Kaniko build exitoso (se ve en logs) pero URL devuelve 404 (Cloudflare) → el pod está en Pending → revisar que el Dockerfile use no-root

### NaN auto-polling (semi-automático)
- NaN **NO** usa webhooks de GitHub
- NaN **SÍ** hace polling periódico del repositorio GitHub (cada ~1-5 minutos, depende de carga)
- Cuando detecta un nuevo commit en `main`, **reconstruye y redeploya automáticamente**
- Si la build anterior falló (ej: faltaba Dockerfile, o el contenedor era root), NaN **reintenta con el siguiente commit** — no hace falta ir al dashboard obligatoriamente
- Para forzar inmediatamente: dashboard → [cloud.nan.builders](https://cloud.nan.builders) → **Redeploy**
- `git commit --allow-empty -m "trigger redeploy" && git push` **SÍ funciona** indirectamente: el push a GitHub → NaN detecta cambio en su próximo ciclo de polling → reconstruye

### Variables de entorno
- Se configuran en la web de NaN → pestaña **Env**
- NO se suben por Git
- Se necesitan para: API keys, tokens, URLs
- `.env.example` en el repo sirve como documentación

### Kaniko
- No soporta `--build-arg` para secrets
- Las secrets VAN en variables de entorno, no en el Dockerfile
- El build puede fallar si `package-lock.json` no coincide con `package.json`
- **⚠️ `npm ci` falla si package-lock.json está desincronizado** — si añades nuevas dependencias (bcryptjs, express-session, etc.), el lockfile queda obsoleto. Regenerar con `npm install` antes de commit. Síntoma: build Kaniko exitoso pero contenedor crash al arrancar porque faltan módulos.
- **Error `error resolving dockerfile path: please provide a valid path to a Dockerfile within the build context with --dockerfile`** → No hay Dockerfile en la raíz del repo, o el Dockerfile está mal nombrado (debe llamarse exactamente `Dockerfile`)
- Si el build falla (ej: no existía Dockerfile), NaN reintenta automáticamente con el siguiente commit detectado por polling

### Dockerfile single-stage con build interno + Node.js (Vite static)

Para proyectos Vite que necesitan build y `node:alpine` en una sola etapa (más simple que multi-etapa):

```dockerfile
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3700

# 1. Dependencias
COPY package.json package-lock.json ./
RUN npm ci --include=dev   # --include=dev para que Vite esté disponible en build

# 2. Código fuente
COPY index.html vite.config.js ./
COPY public/ ./public/
COPY src/ ./src/

# 3. Build
RUN npx vite build

# 4. Usuario no-root (requisito NaN)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 5. Servidor HTTP Node.js embebido (SPA + multi-puerto)
RUN echo 'const http = require("http"); \
const fs = require("fs"); \
const path = require("path"); \
const DIST = path.join(__dirname, "dist"); \
const MIME = { \
  ".html": "text/html", ".css": "text/css", \
  ".js": "application/javascript", ".json": "application/json", \
  ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", \
  ".ico": "image/x-icon", ".woff2": "font/woff2" \
}; \
function handler(req, res) { \
  if (req.url === "/healthz") { \
    res.writeHead(200, {"Content-Type": "application/json"}); \
    res.end(JSON.stringify({status:"ok",uptime:process.uptime()})); \
    return; \
  } \
  let filePath = path.join(DIST, req.url === "/" ? "index.html" : req.url); \
  const ext = path.extname(filePath); \
  fs.readFile(filePath, (err, data) => { \
    if (err) { \
      fs.readFile(path.join(DIST, "index.html"), (e2, d2) => { \
        if (e2) { res.writeHead(500); res.end("Error"); return; } \
        res.writeHead(200, {"Content-Type": "text/html"}); \
        res.end(d2); \
      }); \
    } else { \
      res.writeHead(200, {"Content-Type": MIME[ext] || "application/octet-stream"}); \
      res.end(data); \
    } \
  }); \
} \
http.createServer(handler).listen(process.env.PORT || 3700, "0.0.0.0", () => console.log("App en puerto " + (process.env.PORT || 3700)));' > server.js

# 6. Ajustar permisos y cambiar a usuario no-root
RUN chown -R appuser:appgroup /app

USER appuser

# 7. Healthcheck en el puerto configurado (NO 80 — appuser no puede bind <1024)
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3700/healthz || exit 1

EXPOSE 3700
CMD ["node", "server.js"]
```

**Ventajas sobre multi-etapa:** Sin nginx, sin COPY entre etapas, código del servidor inlineado en el propio Dockerfile. El SPA fallback (cualquier ruta → `index.html`) va incluido.

## Diagnóstico de despliegue

### Estado "Pending" en NaN Builders
- **Qué significa:** NaN está construyendo la imagen Docker por primera vez o tras un nuevo commit. Es NORMAL la primera vez.
- **Tiempo típico:** 2-5 minutos para el primer build Kaniko. Builds posteriores: 1-2 min.
- **Cómo verificar progreso:** `curl -s https://<app>.apps.nan.builders/healthz` — si responde (200 o 404), el servidor ya está vivo. Si responde 404 de Cloudflare en texto plano ("404 page not found"), el espacio aún no existe o el build aún no terminó.
- **No hay webhook de GitHub:** NaN usa polling cada 1-5 min. Un push a `main` desencadena un nuevo build automáticamente. No hace falta hacer nada manual.
- **Si el estado se queda en "Pending" > 10 min:** Ir al dashboard → Redeploy manualmente.

### Diagnóstico de despliegue

| Síntoma | Causa | Solución |
|---|---|---|
| **Cloudflare 404 (no 502) — URL responde con "404 page not found" en texto plano** | **Espacio NaN no creado — DNS resuelve a Cloudflare pero no hay backend** | **Crear el espacio en [cloud.nan.builders](https://cloud.nan.builders) primero. No basta con push a GitHub.** |
| **Pending persistente (> 10 min), Kaniko build sin error aparente, Curren Image se genera pero URL 503** | **Contenedor crash al arrancar — ESM/CJS mismatch** | **`"type": "module"` en package.json + `require()` en server.js → Node crash por `require is not defined`. Crear `server.mjs` en ESM puro. Ver sec. ⚠️ CRÍTICO.** |
| **Build OK (Kaniko exitoso) → URL 404 / Pending** | **Contenedor ejecuta como root — NaN bloquea pods root** | **Añadir `USER appuser` al Dockerfile (ver reglas críticas). Push nuevo commit → NaN detecta por polling → reconstruye. Síntoma clásico: build history muestra "succeeded", Current Image se genera, pero status sigue "pending" > 10 min. Es la causa #1 de este síntoma.** |
| **Build OK, contenedor arranca (logs muestran puerto real), pero URL da 502** | **Puerto desalineado — NaN inyecta `PORT=<container-port>` como env var, y el server escucha en otro puerto** | **Alinear `EXPOSE` del Dockerfile, `process.env.PORT` default en server.js, y Container Port en NaN UI. Los tres deben ser el mismo número.** |
| **Build OK, contenedor arranca pero se reinicia en bucle cada ~30s, URL da 502** | **Healthcheck apunta a endpoint con auth (401) → NaN mata contenedor por unhealthy** | **Crear endpoint público `/healthz` ANTES del middleware de auth. Apuntar HEALTHCHECK a `/healthz`.** |
| **Build OK, contenedor running, 502 persistente (>5 min), healthz no responde** | **Healthcheck apunta a puerto distinto del que NaN inyecta como `PORT`** | **Alinear EXPOSE, process.env.PORT default, y Container Port de NaN. O aplicar patrón de doble puerto (punto 28). Ver skill dedicado: `nan-puerto-desajuste`.** | **Typo en SQL: `CREATE INDEX IF NOT` (sin `EXISTS`)** | **SQLite lanza `SQLITE_ERROR: near "idx_...": syntax error`. Verificar todos los `CREATE INDEX` en server.js. El correcto es `CREATE INDEX IF NOT EXISTS`.** |
| **App responde 200, HTML se sirve, pero muestra loading eterno** | **El proveedor de tiles/API externa falla y nunca dispara `load`** | **Añadir fallback automático en `map.on('error')` + timeout de 12s que oculta loading y crea mapa fallback. Ver `references/loading-screen-eterno.md`.** |
| **Pending eterno (> 15 min), Current Image: `-`, build Kaniko nunca arranca** | **NaN sin espacio en disco/recursos — cluster sobrecargado por muchas apps** | **Liberar espacio desde panel NaN (borrar apps no usadas). Multi-stage Dockerfile ayuda pero no elimina el problema. Hacer un push nuevo para re-trigger build.** |
| 502 Bad Gateway (< 2s) | App crash al arrancar | Verificar token API en pestaña Env de NaN |
| 502 Bad Gateway (2-30s) | Request lenta / hanging | Timeout en API externa, verificar red |
| 502 Bad Gateway (> 30s) | Timeout Cloudflare/NaN | Backend demasiado lento, optimizar consultas |
| Datos stale en frontend | Cache de navegador | Enviar `Cache-Control: no-cache` en HTML/JS |
| `/readyz` muestra `degraded` | Token faltante | Configurar en NaN Env |
| Error 401 en API externa | Token inválido | Revisar token en web del proveedor |
| Error 429 | Rate limit API externa | Cache más agresivo o delay entre requests |
| **Cloudflare 404 en todas las variantes de nombre** | **El nombre del espacio en NaN no coincide con el repo** | **Probar variantes: minúscula, mayúscula, con guiones: `curl -s -o /dev/null -w '%{http_code}' \"https://<variante>-<owner>-<owner>.apps.nan.builders\"`. Si todas dan 404, el espacio no existe o tiene otro nombre. Verificar en [cloud.nan.builders](https://cloud.nan.builders) el nombre exacto del espacio.** |
| **Fondo blanco, 200 OK en HTML — Vite** | **`vite.config.js` tiene `base: '/repo-name/'` (de GitHub Pages) pero NaN sirve desde raíz** | **Cambiar `base: '/'` en vite.config.js. Reconstruir con `npm run build`, push y esperar polling de NaN.** |
| **Fondo blanco tras fix, sigue igual** | **Service Worker roto — `cache.addAll()` falla con 404 → nueva versión SW nunca se activa** | **Ver `## Service Workers` más abajo. Causa: el SW lista un archivo inexistente en STATIC_ASSETS → `cache.addAll()` falla → `install` event nunca completa → SW nuevo no se activa → navegador usa caché vieja. Fix: (1) eliminar la referencia rota del SW, (2) bump CACHE_NAME (ej `sef-cache-v4.0`), (3) push + hard refresh o Unregister SW en DevTools.** |

## Diagnóstico

```bash
# Health check
curl https://<app>.apps.nan.builders/healthz

# Readiness check (verifica tokens)
curl https://<app>.apps.nan.builders/readyz

# Verificar que responde JSON real, no HTML de error
curl -s https://<app>.apps.nan.builders/api/esios/summary?fecha=2026-05-25 | head -c 100
```

## Trigger redeploy NaN

NaN NO tiene webhooks de GitHub. Para redeployar:

1. **Ir al dashboard**: [cloud.nan.builders](https://cloud.nan.builders)
2. **Encontrar la app** → botón **Redeploy** o **Rebuild**
3. Kaniko construye de nuevo desde el repo
4. Verificar con `curl <url>.apps.nan.builders`

> `git commit --allow-empty -m "trigger redeploy"` NO funciona en NaN porque no hay webhook. Solo redeploya si el usuario hace clic en el dashboard.

## Service Workers — Pitfall crítico en sitios estáticos

Los Service Workers con estrategia "cache first" pueden **atascar la actualización de un sitio** si la lista de assets incluye un archivo inexistente.

### Mecanismo de fallo

```
sw.js STATIC_ASSETS → incluye '/css/ntizar.next.css' (no existe)
  → cache.addAll() → falla con 404
    → install event nunca completa
      → SW nuevo NUNCA se activa
        → navegador sigue usando caché vieja (sef-cache-v3.4)
          → FONDO BLANCO (caché vieja + assets nuevos = incompatibilidad)
```

### Fix obligatorio (3 pasos)

1. **Eliminar la referencia rota** del archivo `sw.js` → `STATIC_ASSETS`
2. **Bump CACHE_NAME** — ej `sef-cache-v3.4` → `sef-cache-v4.0` para forzar re-cache completo
3. **Push + instructar al usuario**: hard refresh (`Ctrl+Shift+R`) o DevTools → Application → Service Workers → Unregister

### Verificación post-fix

```bash
# Confirmar que el archivo eliminado NO está en STATIC_ASSETS
grep 'ntizar.next.css' sw.js  # Debe dar vacío
# Confirmar que el cache name cambió
grep 'CACHE_NAME' sw.js
```

### Prevención

- Cuando se elimina un archivo CSS/JS del repo, **buscar también en `sw.js`** la referencia
- `cache.addAll()` es atómico: si 1 de N archivos falla, TODOS los assets se pierden de caché
- El error de `cache.addAll()` es silencioso en consola del usuario (solo visible en DevTools → Application → Service Workers)

## Patrones aprendidos

1. **Siempre exponer el puerto correcto** — NaN usa el EXPOSE del Dockerfile para mapear el tráfico
2. **Siempre usar `process.env.PORT`** — permite que el contenedor reciba el puerto del entorno
3. **NUNCA escuchar en puerto 80 desde appuser** — `USER appuser` no tiene permisos para bind a puertos <1024. El bind falla silenciosamente, el proceso muere, y el pod se queda en Pending. Solo escuchar en el puerto configurado: `http.createServer(handler).listen(process.env.PORT || 3700, "0.0.0.0")`. Si el HEALTHCHECK necesita sondear, apuntar al mismo puerto configurado.
4. **Usuario no-root es REQUISITO** — sin `USER appuser` el pod se queda en Pending indefinidamente aunque Kaniko construya bien la imagen. Es la causa #1 de "build OK → no carga"
5. **Health endpoint** — `/healthz` devuelve `{"status":"ok"}` para verificar que el app está vivo
6. **Healthcheck en puerto configurado** — el HEALTHCHECK del Dockerfile debe apuntar al mismo puerto que el server (ej: `localhost:3700/healthz`), no a 80. NaN no sondea en 80 internamente — esa es una suposición errónea que crashea el contenedor.
7. **Readiness endpoint** — `/readyz` verifica que los tokens están configurados
8. **npm ci en vez de npm install** — usa package-lock.json para builds reproducibles
9. **`.dockerignore`** — siempre excluir `.env`, `node_modules`, `.git`
10. **`.env.example`** — siempre en el repo como documentación de variables necesarias
11. **Nginx static sites** — Para sitios estáticos (HTML+CSS+JS): `FROM nginx:alpine`, sed para cambiar listen port al puerto correcto, `COPY . .` en `/usr/share/nginx/html/`, `.dockerignore` excluye `.git`, `node_modules`, `*.md`, `docs/`. El HEALTHCHECK usa `wget -qO- http://localhost:<port>/`
### 12. Vite static sites (multi-etapa) — Para proyectos Vite: usar `FROM node:20-alpine AS builder` con `npx vite build`, luego `FROM nginx:alpine` copiando `/app/dist`. Ver referencia completa en `references/dockerfile-spa-static.md`
### 24. **Persistencia de datos en NaN — GitHub Contents API**

NaN containers **pierden el filesystem en redeploy** (Kaniko reconstruye la imagen). Si la app guarda datos en JSON/SQLite dentro del contenedor, se pierden al redeployar.

**Solución:** sincronizar cambios a GitHub vía Contents API (no necesita git en el contenedor):

```javascript
async function syncToGitHub(db, token, owner, repo, path) {
  // 1. Obtener SHA actual del archivo
  const getRes = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${path}`, {
    headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/vnd.github.v3+json' }
  });
  if (!getRes.ok) return;
  const { sha } = await getRes.json();
  // 2. Subir contenido actualizado (base64)
  const b64 = Buffer.from(JSON.stringify(db, null, 2)).toString('base64');
  await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${path}`, {
    method: 'PUT',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: `Auto-sync ${new Date().toISOString().slice(0,19)}`,
      content: b64, sha
    })
  });
}
```

**Llamar en TODOS los endpoints de mutación** (POST, PUT, DELETE). El sync es async y no bloquea la respuesta — si falla, el dato queda local pero no en GitHub.

**Requisito:** el token NAN_API debe tener permisos de escritura en el repo. Verificar: `curl -H "Authorization: Bearer $TOKEN" https://api.github.com/repos/OWNER/REPO`.

**Pitfall:** el SHA es obligatorio — sin él, GitHub devuelve 422 "sha must be provided". Si el archivo es nuevo (no existe), no hay SHA y se usa CREATE en vez de UPDATE.

### 12a. Mejorar app existente vs crear nueva — Cuando el usuario pide "mejorar" una app ya desplegada, modificar el repo existente (patch dashboard.html, extender server.js), NO crear proyecto nuevo. Ver `references/improving-existing-app.md`.

### 12b. Vite + Node.js server (3-stage, recomendado para NaN) — MEJOR que nginx para NaN:
```dockerfile
# === Stage 1: Instalar TODAS las dependencias (incluidas dev para Vite) ===
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --include=dev

# === Stage 2: Build con Vite ===
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY index.html vite.config.js ./
COPY public/ ./public/
COPY src/ ./src/
RUN npx vite build

# === Stage 3: Producción (solo prod deps) ===
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3030

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Re-instalar solo producción (npm ci --omit=dev)
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Copiar build estático
COPY --from=builder --chown=appuser:appgroup /app/dist ./dist

# Servidor en archivo separado (NO inline echo)
COPY --chown=appuser:appgroup server.mjs ./

USER appuser
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3030/healthz || exit 1
EXPOSE 3030
CMD ["node", "server.mjs"]
```

**Ventajas:** El server.mjs es un archivo real en el repo (no inline), se puede lintear/testear, y evita el pitfall de `"type": "module"` (ver sección ⚠️).
13. **SPA con Node.js (recomendado para NaN)** — Más fiable que nginx multi-etapa. Server embebido con SPA fallback y multi-puerto. Ver `references/dockerfile-spa-static.md`
14. **`npx serve` sin clipboard** — Al servir localmente con `npx serve`, usar `--no-clipboard` para evitar errores de permisos
15. **Verificar archivos estáticos tras deploy** — Después de un push, comprobar que todos los `<link href>` y `<script src>` devuelven 200: `curl -sI https://<app>.apps.nan.builders/css/<archivo>.css | head -3`. Si alguno devuelve 404, el HTML referencia un archivo que no existe en el contenedor.
16. **deploy.yml job name mismatch** — Si `deploy.yml` referencia un job que no existe en el workflow CI real (ej `lint-and-test` cuando los jobs se llaman `test` y `build`), el deploy nunca se ejecuta. Verificar con: `gh run list --repo OWNER/REPO --json name,status` y comparar con los job names en deploy.yml. Fix: actualizar `needs:` en deploy.yml para que coincida con los job names reales.
17. **Vite `base` path para NaN** — Si el proyecto Vite se configuró para GitHub Pages (`base: '/repo-name/'`), **cambiar a `base: '/'`** antes de deployar en NaN. Si no, los assets JS/CSS se buscan en `/repo-name/assets/...` pero NaN sirve desde raíz → 404 silencioso → fondo blanco. Verificar que `dist/index.html` use rutas `/assets/...` (no `/repo-name/assets/...`) tras el build.
18. **NaN URL discovery** — Cuando una URL NaN devuelve 404 de Cloudflare y el usuario dice que el espacio existe, probar múltiples variantes del nombre: minúscula, mayúscula, con guiones vs sin guiones. El nombre del espacio en NaN puede diferir del nombre del repo. Comando: `for name in variante1 variante2; do curl -s -o /dev/null -w "%{http_code}" "https://\${name}-<owner>-<owner>.apps.nan.builders"; done`
19. **Estado "Pending" es normal** — NaN tarda 2-5 min en el primer build Kaniko. La URL puede responder 404 (Cloudflare) antes de que termine el build. Verificar con `curl -s https://<app>.apps.nan.builders/healthz` — si responde (200 o 404 de app, no de Cloudflare), el servidor ya está vivo. No hacer nada manual, el auto-deploy funciona por polling cada 1-5 min.
20. **Pantalla de carga eterna en SPAs con mapas** — Si `hideLoading()` solo se llama en `map.on('load')` y el proveedor de tiles falla, el loading nunca se oculta. Añadir fallback automático en `map.on('error')` + timeout de seguridad (12s). Ver `references/loading-screen-eterno.md`.
21. **Mejorar app existente vs crear nueva — CORRECCIÓN CRÍTICA** — Cuando el usuario pide "mejorar" o "añadir algo a" una app ya desplegada en NaN, **NUNCA crear un proyecto nuevo**. Modificar el repo existente con `patch`/`write_file` sobre los archivos existentes (`dashboard.html`, `server.js`, etc.). El usuario quiere evolución, no reinvención. Síntoma de fallo: crear `dieta-nan/` con `package.json`, `server.js`, `index.html` nuevos cuando el usuario pidió mejorar `dieta-ntizar.apps.nan.builders`. Fix: trabajar sobre el repo existente, añadir tabs/features al HTML existente, extender `server.js` con nuevos endpoints, actualizar Dockerfile si es necesario.
### 22. **Dockerfile existente sin USER appuser** — Un repo ya desplegado puede tener un Dockerfile que falta `USER appuser`, lo que hace que el pod se quede en Pending. Si el Dockerfile de un repo existente no tiene `USER appuser`, añadirlo inmediatamente con `patch`.
### 23. **Debugging "Unexpected token '<'"** — Cuando la IA del dashboard devuelve este error, es siempre porque el servidor devuelve HTML de error (401/500) en vez de JSON. Causa típica: token API faltante en el contenedor. Ver `references/debugging-unexpected-token-html.md`.

### 32. **JS cacheado tras refactor — version query en script tag**

Cuando se refactoriza un proyecto que tiene JS inline en HTML y se extrae a un archivo `.js` separado, o cuando se hacen cambios importantes en el JS, **el navegador puede servir la versión cacheada del JS incluso después de un redeploy en NaN**.

**Síntomas:**
- El `curl` al servidor sirve el JS nuevo correctamente
- El navegador dice "Assignment to constant variable" o errores similares que ya no existen en el código
- `fetch('/dashboard.js?t=999')` sirve el nuevo contenido, pero el navegador sigue ejecutando el viejo

**Causa:** El navegador cachea el `.js` por `max-age=14400` (4 horas) en el CDN de Cloudflare/NaN. El script tag `<script src="dashboard.js">` no tiene version query, así que el navegador usa la versión cacheada.

**Fix:** Añadir un version query al script tag en el HTML:
```html
<script src="dashboard.js?v=1718200000"></script>
```

El timestamp cambia con cada deploy, forzando al navegador a descargar la versión nueva.

**Prevención:** Cuando se extrae JS de un HTML inline a archivo separado, o cuando se hacen cambios importantes en JS, siempre añadir `?v=` con timestamp al script tag.

### 34. **Express: rutas con parámetros capturan rutas estáticas**

**Pitfall:** Si tienes `GET /:id` ANTES de `GET /stats`, Express captura `/stats` como un ID.

```typescript
// ❌ MAL — /:id captura /stats
router.get('/:id', ...)      // GET /leads/stats → id='stats'
router.get('/stats', ...)    // nunca se alcanza

// ✅ BIEN — rutas estáticas primero
router.get('/stats', ...)    // GET /leads/stats → OK
router.get('/:id', ...)      // GET /leads/abc123 → OK
```

**Regla de oro:** En Express, las rutas se emparejan en orden de definición. Las rutas estáticas (sin parámetros) deben definirse ANTES de las rutas con parámetros (`/:id`, `/:slug`, etc.). Esto aplica a todos los verbos (GET, POST, PUT, DELETE).

**Síntoma:** Endpoint devuelve "no encontrado" o error de validación cuando se accede a una ruta que parece correcta.

### 37. **Crear repos GitHub privado vía API curl (gh CLI no instalado)**

Cuando `gh` CLI no está disponible, crear repos privados vía GitHub API:

```bash
source /hermes-home/.env 2>/dev/null
curl -s -u "Ntizar:$GITHUB_TOKEN" -X POST \
  "https://api.github.com/user/repos" \
  -d '{"name":"AdelaTest01","private":true,"description":"..."}'
```

Push:
```bash
cd /path/to/project
git init
git remote add origin "https://Ntizar:$GITHUB_TOKEN@github.com/Ntizar/AdelaTest01.git"
git branch -M main
git push -u origin main
```

Verificar privado:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/Ntizar/AdelaTest01" | \
  python3 -c "import sys,json; print('PRIVADO ✅' if json.load(sys.stdin).get('private') else 'PÚBLICO ❌')"
```

**Nota:** El token debe tener permisos `repo` (full control). Verificar con `cat /hermes-home/.env | grep GITHUB_TOKEN`.

Cuando usas `sql.js` (no `better-sqlite3`), pasar `undefined` como valor de parámetro en un INSERT puede causar fallos silenciosos o errores de tipo.

```typescript
// ❌ MAL — data.descripcion puede ser undefined
db.run('INSERT INTO oportunidades (...) VALUES (?, ?, ?, ?)',
  [id, data.leadId, data.titulo, data.descripcion])

// ✅ BIEN — siempre fallback
db.run('INSERT INTO oportunidades (...) VALUES (?, ?, ?, ?)',
  [id, data.leadId, data.titulo, data.descripcion || ''])
```

**Regla:** Para TODOS los campos opcionales en INSERT con sql.js, usar `|| ''` (string), `|| 0` (número), o `|| null` (NULL explícito). Nunca dejar valores undefined.

### 36. **Debug: "respuesta vacía" → proceso viejo en el puerto**

**Pitfall:** Cuando un endpoint devuelve `{ lead: {} }`, `{"leads":{}}`, o cualquier JSON vacío, la causa más probable es que el server en el puerto de test está sirviendo código compilado antiguo (el `dist/` no se rebuildó o el proceso no se reinició).

**Síntomas:**
- `npm run build` compila sin errores
- El código fuente es correcto (verificado con `read_file`)
- El código compilado (`dist/`) parece correcto (verificado con `grep`)
- Pero las respuestas de la API son objetos vacíos
- El server no imprime logs (porque es un proceso viejo)

**Diagnóstico:**
1. Matar TODOS los procesos en el puerto: `pkill -9 -f "node.*server"` o `pkill -9 -f "node.*dist"`
2. Verificar que el puerto está libre: `sleep 2 && curl http://localhost:3099/health` (debe fallar)
3. Reiniciar el server desde cero con DB limpia: `rm -f datos.db && PORT=3099 node dist/server.js`
4. Verificar que el nuevo proceso imprime logs

**Regla:** Siempre matar procesos viejos antes de testear un endpoint nuevo o después de un cambio en el código. El síntoma de "respuesta vacía" es casi siempre un proceso viejo sirviendo código obsoleto.

### 34. **Express: rutas con parámetros capturan rutas estáticas**

**2026-06-13 (MasterFit dieta):** Intenté eliminar código de dark mode con `re.sub` y un patrón regex que buscaba desde un comentario hasta `})();`. El regex eliminó el botón HTML pero **dejó fragmentos del IIFE abierto** (bloque `try { localStorage.getItem(DARK_MODE_KEY) ... } catch(e) {}`), lo que rompió la ejecución JS. `loadData()` quedó definida pero nunca llamada.

**Causa:** Los bloques IIFE con `try { ... } catch(e) {}` anidados son difíciles de delimitar con regex. `re.sub()` deja fragmentos huérfanos que el parser JS ignora pero que cortan la ejecución.

**Fix seguro:**
1. Identificar el bloque completo (inicio comentario → cierre `})();`)
2. Eliminar con `content[:start] + content[end:]` — NO usar `re.sub`
3. Verificar que no queda ningún fragmento residual

**Verificación post-fix:** grep por todos los términos del bloque eliminado (`DARK_MODE_KEY`, `darkModeToggle`, etc.) — debe dar 0 resultados.

**Ver:** `references/nan-deploy-cache-pattern.md` para patrón completo de verificación de deploy.

### 32. **var → const/let: detectar += como reasignación**

Al migrar `var` → `const`/`let`, el patrón de búsqueda `=` no detecta reasignaciones con `+=`, `-=`, `*=`, `/=`. Esto causa errores `Assignment to constant variable` en tiempo de ejecución.

**Fix:** Al analizar scope para decidir entre `const` y `let`, buscar también estos operadores:
```python
if re.search(r'\b' + re.escape(name) + r'\s*[+\-*/]=', rest_of_scope):
    # es let, no const
```

**Pitfall común:** Variables como `sumX = 0; ... sumX += x;` dentro de un `forEach` se reasignan pero no son detectadas por un patrón de búsqueda de `=` simple.

**Verificación de sincronización post-deploy:**

```bash
# 1. Obtener SHA del archivo en GitHub
SHA_REMOTO=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/contents/data/database.json | \
  grep -o '"sha":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "SHA remoto: $SHA_REMOTO"

# 2. SHA local
SHA_LOCAL=$(sha256sum data/database.json | cut -d' ' -f1)
echo "SHA local:  $SHA_LOCAL"

# 3. Conteo de registros (personalizar según estructura)
curl -s https://APP.apps.nan.builders/api/datos | \
  python3 -c "import json,sys; d=json.load(sys.stdin); \
    print(f'pesos={len(d[\"pesos\"])} comidas={len(d[\"comidas\"])} \
    entrenos={len(d.get(\"entrenamientos\",d.get(\"entrenos\",[])))}')"

# 4. Probar una mutación en producción
curl -X POST -H "Content-Type: application/json" \
  -d '{"nota":"test sync $(date)"}' \
  -u "user:pass" https://APP.apps.nan.builders/api/entrenamientos

# 5. Re-verificar que el dato llegó a GitHub (SHA debe haber cambiado)
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/contents/data/database.json | \
  grep -o '"sha":"[^"]*"' | head -1
```

**Pitfall:** El SHA de GitHub Contents API (Git blob SHA) NO es el mismo que `sha256sum` local. No esperar que coincidan. Comparar CONTENIDO, no SHA.

**Pitfall:** Si hay dos carpetas locales del mismo repo (`dieta/` + `dieta-masterfit/`), el servidor en NaN usa el remoto, no el local. Verificar con `git remote -v` y `git log --oneline -3` en cada una para identificar cuál está actualizada.

### 25. **Build succeeded → Pending forever** — La causa #1 es contenedor root. Ver `references/nan-pending-root-cause.md` para diagnóstico completo con caso real de Mastermind Dashboard.

### 26. **NaN inyecta `PORT=<container-port>` automáticamente** — Cuando configuras el Container Port en la UI de NaN (ej: 4040), NaN pasa `PORT=4040` como variable de entorno al contenedor. Si tu server.js usa `process.env.PORT || 6060`, escuchará en 4040 aunque el Dockerfile tenga `EXPOSE 6060`. **El EXPOSE del Dockerfile y el Container Port de NaN deben coincidir**, pero además el server debe escuchar en el puerto que NaN espera. Síntoma: build succeeded, contenedor arranca (logs muestran el puerto real), pero URL da 502 porque NaN espera en otro puerto. Fix: alinear `EXPOSE`, `process.env.PORT` default, y Container Port de NaN al mismo número.

### 27. **Healthcheck necesita endpoint público (sin auth)** — Si el HEALTHCHECK del Dockerfile apunta a un endpoint protegido por Basic Auth (ej: `/api/summary`), el healthcheck devuelve 401 → NaN considera el contenedor unhealthy → lo mata → URL da 502. **Siempre crear un endpoint público de healthcheck** antes de aplicar el middleware de auth:
```javascript
// ANTES de app.use('/api', basicAuth)
app.get('/healthz', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});
```
Y en el Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:4040/healthz || exit 1
```
Síntoma: build succeeded, contenedor arranca, pero tras ~30s el pod se reinicia en bucle y URL da 502. Verificar con `curl https://<app>.apps.nan.builders/healthz` — si da 502, el healthcheck está matando el contenedor.

### 28. **Patrón de doble puerto (tolerante a desajuste)** — Cuando el Container Port en NaN no coincide con el EXPOSE del Dockerfile y no puedes cambiarlo desde el dashboard, el server puede escuchar en **ambos puertos** simultáneamente. Esto asegura que funcione independientemente de qué puerto inyecte NaN como `PORT`:

```javascript
const PORT = parseInt(process.env.PORT || '6060');
const FALLBACK_PORT = 4040; // Puerto legacy por si NaN cambia de opinión

// ... app config ...

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🔮 App → http://0.0.0.0:${PORT}`);
});

app.listen(FALLBACK_PORT, '0.0.0.0', () => {
  console.log(`   Fallback → http://0.0.0.0:${FALLBACK_PORT}`);
});
```

Y el HEALTHCHECK debe probar ambos puertos:
```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:6060/healthz || wget -qO- http://localhost:4040/healthz || exit 1
```

**Cuándo usar:** Cuando el Container Port en NaN UI está fijado a un valor (ej: 6060) pero el Dockerfile original tenía otro (ej: 4040), y no tienes acceso al dashboard para cambiarlo. El server escucha en ambos, el healthcheck prueba ambos, y NaN puede enrutar a cualquiera.

**⚠️ Pitfall:** Express permite `app.listen()` múltiples veces en el mismo objeto `app` — cada llamada crea un server independiente. Esto funciona porque Express delega a `http.Server` y cada listen crea un socket nuevo. Verificado con Express 5.2.1.

**Síntoma que resuelve:** Build succeeded, contenedor running, pero 502 persistente. El healthcheck de la imagen actual apunta a un puerto (ej: 4040) pero NaN inyecta `PORT=<otro>` (ej: 6060) y enruta tráfico a ese otro puerto. El healthcheck falla → NaN mata contenedor → 502. Con doble puerto, ambos healthchecks funcionan.

- **Ruta del script ESIOS telegram:** `/root/workspace/esios-dashboard/scripts/esios-telegram.js` — NUNCA `/root/workspace/Mastermind/scripts/esios-telegram.js` (no existe). El cron job `esios-daily-telegram` (job_id: 9e7570152a99) tiene la ruta incorrecta y necesita corrección.
- **Container Runtime Restrictions (NaN.builders)** — Los contenedores en NaN.builders tienen restricciones significativas que afectan qué comandos y APIs funcionan dentro del contenedor. **Siempre diseñar los endpoints del dashboard asumiendo que estas restricciones aplican.**

- **Ruta del script ESIOS telegram:** `/root/workspace/esios-dashboard/scripts/esios-telegram.js` — NUNCA `/root/workspace/Mastermind/scripts/esios-telegram.js` (no existe). El cron job `esios-daily-telegram` (job_id: 9e7570152a99) tiene la ruta incorrecta y necesita corrección.

### 30. Container Runtime Restrictions (NaN.builders)
|---|---|---|
| `ps aux` | Solo ve el PID 1 (el propio proceso Node.js) | `/proc` fallback, o info del ecosistema |
| `ps -o user= -p <pid>` | No tiene permisos para otros procesos | Usar `'root'` como fallback |
| `free -m` | Muestra solo la memoria del contenedor | `os.totalmem()` / `os.freemem()` de Node.js |
| `df -h` | Muestra solo el filesystem del contenedor | `process.memoryUsage()` para RSS |
| `crontab -l` | No hay cron daemon en el contenedor | Array vacío |
| `chromadb` (localhost:8000) | ChromaDB corre en la VM local, no en el contenedor | Filesystem fallback, o categorías conocidas |
| `/hermes-home/skills` | No existe en el contenedor | Categorías conocidas del ecosistema |
| `wget` / `curl` a localhost de la VM | Red aislada del contenedor | No hay alternativa — el contenedor no puede acceder a servicios de la VM host |

#### Comandos que SÍ funcionan (pero limitados)

| Comando | Funciona | Limitación |
|---|---|---|
| `node -e "..."` | ✅ | Solo Node.js, no acceso a sistema host |
| `fs.readdirSync('/proc')` | ✅ | Solo ve PIDs del contenedor (normalmente solo PID 1) |
| `fs.readFileSync('/proc/1/cmdline')` | ✅ | Solo el propio proceso |
| `os.hostname()` | ✅ | Devuelve el hostname del contenedor |
| `os.cpus()` | ✅ | Muestra CPUs asignadas al contenedor |
| `os.totalmem()` | ✅ | Memoria total del contenedor |
| `os.freemem()` | ✅ | Memoria libre del contenedor |
| `os.uptime()` | ✅ | Uptime del contenedor |
| `process.uptime()` | ✅ | Uptime del proceso Node.js |
| `process.memoryUsage()` | ✅ | RSS/heap del proceso Node.js |

#### Diseño de Endpoints para Contenedores

Cada endpoint del dashboard debe tener una cadena de fallback que termine en un **empty state honesto** (nunca datos inventados):

```javascript
// Patrón: Fuente primaria → Fuente secundaria → Empty state honesto
app.get('/api/processes', (req, res) => {
  try {
    // 1. ps aux (funciona en VM, falla en contenedor)
    const raw = sh("ps aux --sort=-%mem 2>/dev/null | head -30", '');
    if (raw && raw !== 'N/A') {
      const procs = parsePsOutput(raw);
      if (procs.length > 0) return res.json(procs);
    }
    // 2. /proc (solo ve PID 1 en contenedor)
    const pids = fs.readdirSync('/proc').filter(p => /^\d+$/.test(p));
    if (pids.length > 1) {
      const procs = parseProcDir(pids);
      if (procs.length > 1) return res.json(procs);
    }
    // 3. Info del ecosistema (marcado como no-local)
    res.json(ECOSYSTEM_PROCESSES);
  } catch {
    res.json([{ pid: 1, command: 'node server.js' }]);
  }
});
```

#### Verificación de Endpoints en Contenedor

```bash
# Probar cada endpoint en el contenedor real
for endpoint in processes crons skills agents system; do
  echo "=== $endpoint ==="
  curl -s -u 'admin:$PASS' https://app.apps.nan.builders/api/$endpoint | python3 -c "
import json,sys
d = json.load(sys.stdin)
if isinstance(d, list):
    print(f'  {len(d)} items')
elif isinstance(d, dict):
    for k,v in d.items():
        if isinstance(v, list): print(f'  {k}: {len(v)} items')
        elif isinstance(v, (str,int,float)): print(f'  {k}: {v}')
"
done
```

#### Referencia

Ver `frontend-dashboard-patterns` → `references/data-integrity-pattern.md` para implementación completa de fallback chains y empty states en el frontend.
