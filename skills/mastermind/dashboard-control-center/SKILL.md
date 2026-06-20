---
name: dashboard-control-center
description: "Mastermind Dashboard — panel de control visual de infraestructura, agentes, crons y skills. Express + Aurora Liquid Glass. Repo privado en GitHub, deploy en NaN.builders o local en microVM."
version: 2.0.0
tags: [dashboard, aurora, nan, control-center, mastermind, monitoring]
---

# Dashboard Control Center

Panel de control visual de la infraestructura Mastermind. Sigue una **arquitectura dual**:

- **Local** (microVM, puerto 6060): backend con datos reales del sistema (CPU, RAM, procesos, ChromaDB, crons). Es la **fuente de datos real**.
- **NaN** (contenedor): versión visual que consume las APIs del local (con fallbacks graceful cuando no hay acceso a ChromaDB/procesos del host).

## Arquitectura v2 — Datos Reales (GitHub Sync)

NaN containers están AISLADOS del host. No pueden ver procesos, crons, skills ni archivos del host. La solución es sincronizar datos vía Git.

```
VM (host)                              NaN Container
┌──────────────────────┐               ┌──────────────────────┐
│ collect-status.py    │──git push──→  │ public/status.json   │
│ (cron cada 30min)    │   GitHub      │ (archivo estático)   │
│ Lee:                 │               │                      │
│  • /cron/jobs.json   │               │ /api/system → métricas│
│  • /skills/ (753)    │               │ /api/disk → disco     │
│  • ps aux (12 procs) │               │ /api/github → commits │
│  • /sessions/ (5)    │               │ /api/vm-status → JSON │
│  • /logs/agent.log   │               │   del status.json     │
└──────────────────────┘               └──────────────────────┘
```

**Frecuencia:** collect-status.py se ejecuta cada 30min vía cron Hermes (`dashboard-status-sync`). Push automático a GitHub triggers redeploy NaN.

## Ficheros clave

```
mastermind-dashboard/
├── server.js              # Express, port 6060 (fallback 4040)
├── Dockerfile             # Node 20 alpine, EXPOSE 6060
├── public/
│   ├── dashboard.html     # Panel principal (dark theme)
│   └── status.json        # ← Datos reales VM
├── scripts/
│   └── collect-status.py  # Recolecta datos VM → status.json
```

## Endpoints

| Ruta | Fuente datos | Actualización |
|------|-------------|---------------|
| `/healthz` | — | Tiempo real |
| `/api/system` | `os` module (NaN) | Tiempo real |
| `/api/disk` | `df -h /` (NaN) | Tiempo real |
| `/api/github` | `git log` (NaN) | Tiempo real |
| `/api/vm-status` | `status.json` | Cada 30min |

## Datos que muestra

| Sección | Fuente | Frecuencia |
|---------|--------|-----------|
| Cron Jobs (16+) | `/cron/jobs.json` | 30min |
| Skills (178+) | `/skills/` | 30min |
| Procesos VM (12+) | `ps aux` | 30min |
| Actividad | sessions + notes + logs | 30min |
| CPU/RAM NaN | `os` module | Tiempo real |
| Commits | `git log` | Tiempo real |

**Cuándo usar esta arquitectura:**
- El dashboard necesita datos del sistema real (CPU, procesos, ChromaDB)
- NaN no puede acceder a esos recursos (contenedor aislado)
- Quieres una URL pública bonita pero con datos reales

**Cómo funciona:**
1. El server.js local tiene acceso completo al sistema (execSync, ChromaDB, crontab)
2. El server.js de NaN tiene fallbacks graceful para todo lo que no puede leer
3. Ambos sirven el mismo frontend (dashboard.html)
4. El local se usa para desarrollo/datos reales, NaN para acceso público

## Pitfalls

- **🔴 NaN containers AISLADOS del host** — No pueden ver procesos, crons, skills, sessions ni archivos del host. `ps aux` solo muestra PID 1 (node server.js). `/proc` limitado. ChromaDB no accesible (localhost:8000 está en el host, no en el contenedor). **Solución:** Sincronizar datos vía Git (collect-status.py → status.json → push).
- **🔴 `collect-status.py` DEBE ejecutarse en la VM, no en NaN** — El script lee archivos de `/hermes-home/` que solo existen en la VM. Si se ejecuta en NaN, devuelve datos vacíos o erróneos.
- **🔴 `status.json` DEBE estar en `public/` del repo** — Para que NaN lo despliegue como archivo estático. Si está en otra ubicación, el endpoint `/api/vm-status` no lo encuentra.
- **Port 6060** — El 4000 es del ESIOS Dashboard, 4040 está libre pero NaN requiere coincidencia exacta Container Port = EXPOSE = PORT default.

## Repo

- **Repo:** `github.com/Ntizar/Mastermind-Dashboard` (privado)
- **Stack:** Node.js 20, Express ^5.2.1, Aurora Liquid Glass
- **Auth:** Basic auth `admin:$Nan603060`

- **CDN:** `https://cdn.jsdelivr.net/gh/Ntizar/Ntizar-Aurora@latest/ntizar.css`
- **Tema:** Oscuro (`data-nz-theme="dark"`)
- **Colores:** Azul `#2563eb` + Naranja `#f97316`
- **Fondo:** `#0a0e1c` con gradientes radiales
- **Auto-refresh:** cada 5 segundos via `setInterval`

### Secciones del dashboard

1. **KPIs** — CPU, RAM (con barra), Disco (con barra), Uptime
2. **🧠 Agentes** — Canvas animado con 6 agentes comunicándose con partículas
3. **⚙️ Procesos** — Lista de procesos con iconos por tipo (Hermes, ChromaDB, LSP)
4. **📡 Actividad** — Log en vivo de comunicación entre agentes
5. **⏰ Crons** — Jobs programados del sistema
6. **🧠 Skills** — Estado de ChromaDB con skills indexados

### Canvas de agentes

El canvas dibuja 6 agentes en un grafo radial:
- **Mastermind** (centro-arriba) — conecta con todos
- **Explorer, Planner, Implementer, Reviewer** (fila media)
- **Critic** (centro-abajo)

Las partículas vuelan entre agentes simulando comunicación. Cada 3s se dispara una actividad aleatoria.

## 🚀 Deploy en NaN

1. Push a `main` → auto-deploy (si está configurado)
2. NaN construye con Kaniko usando el Dockerfile
3. El contenedor no tiene acceso a ChromaDB local → el endpoint `/api/skills` devuelve `{ status: 'disconnected' }`
4. El contenedor no ve procesos del host → `/api/processes` tiene fallback

### Dockerfile para NaN (con usuario no-root)

⚠️ **CRÍTICO: NaN BLOQUEA contenedores root.** Sin `USER appuser` el build Kaniko funciona pero el pod se queda en "Pending" para siempre.

```dockerfile
FROM node:20-alpine
WORKDIR /app

# 1. Dependencias (cache layer)
COPY package.json package-lock.json ./
RUN npm install --production

# 2. Código (solo lo necesario, no node_modules/)
COPY server.js .
COPY public/ ./public/

# 3. Usuario no-root (REQUISITO NaN)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && \
    chown -R appuser:appgroup /app

USER appuser

EXPOSE 6060

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:6060/api/summary || exit 1

CMD ["node", "server.js"]
```

**`.dockerignore` obligatorio:**
```
node_modules/
.git/
.gitignore
*.md
entrypoint.sh
```

Sin `.dockerignore`, `COPY . .` copia `node_modules/` locales (pesados) y `.git/` (innecesario), haciendo la imagen más lenta y propensa a errores.

### Variables de entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `PORT` | `6060` | Puerto del servidor — debe coincidir con EXPOSE del Dockerfile y puerto configurado en NaN |
| `DASH_PASSWORD` | `$Nan603060` | Contraseña Basic Auth |
| `CHROMA_URL` | `http://localhost:8000` | URL de ChromaDB (solo local — el contenedor NaN no tiene acceso) |

## 🔒 Seguridad

- **Basic Auth** sobre todos los endpoints `/api/*`
- Usuario: `admin`, contraseña: `DASH_PASSWORD` (env var)
- El frontend se sirve sin auth (el login se hace desde el JS)
- Las contraseñas NUNCA van en el código ni en commits

## ⚠️ Pitfalls

1. **NaN build falla si no hay Dockerfile** — crearlo antes de conectar el repo
2. **npm ci requiere package-lock.json** — si no existe, usar `npm install`
3. **No subir node_modules** — añadir `.gitignore` y hacer `git rm -r --cached node_modules`
4. **Puerto 4000 ocupado por ESIOS** — usar 6060
5. **ChromaDB no accesible desde contenedor NaN** — el endpoint debe tener fallback graceful
6. **execSync falla en contenedor** — rodear con try/catch y devolver datos de ejemplo
7. **Trigger rebuild:** `git commit --allow-empty -m "chore: trigger redeploy" && git push`
8. **🚨 NaN bloquea contenedores root** — causa #1 de "build succeeded → pending forever". El build Kaniko funciona perfecto (se ve "succeeded" en logs) pero el pod nunca arranca. Síntoma: URL devuelve 404 de Cloudflare, status "pending" > 10 min. Fix: añadir `USER appuser` + `addgroup`/`adduser` al Dockerfile.
9. **Falta `.dockerignore`** — sin él, `COPY . .` mete `node_modules/` y `.git/` en la imagen. Crear `.dockerignore` con `node_modules/`, `.git/`, `.gitignore`, `*.md`.
10. **NaN no hereda env vars del host** — las variables de entorno del microVM NO están disponibles en el contenedor. Configurarlas en la pestaña Env de NaN o copiar `.env` en el contenedor.
11. **NaN polling vs webhook** — NaN NO usa webhooks de GitHub. Usa polling cada 1-5 min. Si el build anterior falló, NaN reintenta con el siguiente commit. Para forzar inmediato: dashboard NaN → Redeploy manual.

## 📊 Datos que monitoriza

- **CPU:** load average (1, 5, 15 min) + número de núcleos
- **RAM:** total, usada, libre, porcentaje con barra de color (verde <65%, naranja <85%, rojo >85%)
- **Disco:** total, usado, disponible, porcentaje
- **Uptime:** días + horas
- **Procesos:** top 10 por uso de memoria, clasificados por tipo
- **Crons:** jobs del sistema (crontab) + jobs de Hermes (desde `/hermes-home/cron/`)
- **Skills:** conexión a ChromaDB, skills indexados, dimensiones
- **Agentes:** 6 agentes con roles, colores y actividad simulada

## 🔮 Próximas mejoras

- [ ] Gráficos históricos de CPU/RAM (última hora)
- [ ] Logs de Hermes en tiempo real
- [ ] Botón para reiniciar servicios desde el dashboard
- [ ] Token tracking (consumo de API)
- [ ] Notificaciones cuando algo falla
- [ ] WebSockets en lugar de polling cada 5s