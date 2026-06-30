---
name: nan-dashboard-deploy
description: "Procedimiento completo para desplegar el Portfolio/Control Center (nan-dashboard) en NaN.builders — auth, kanban, métricas, endpoints y troubleshooting."
version: 1.0.0
author: Ntizar
---

# Deploy nan-dashboard (Portfolio + Control Center) en NaN.builders

Guía paso a paso para desplegar el proyecto `nan-dashboard` (centro de control de apps de Ntizar) en NaN.builders.

## 📁 Repositorio y ubicación

- **Repo:** `github.com/Ntizar/nan-dashboard`
- **Local:** `/root/workspace/nan-dashboard`
- **Stack:** Node.js 22, Express, cookie-parser, sqlite3
- **Puerto:** 4500 (Dockerfile) / 3500 (deploy actual en Spaces)
- **URL:** `https://ntizar-ntizar.apps.nan.builders`

## 🏗️ Arquitectura del proyecto

```
nan-dashboard/
├── server.js              # Express principal (auth + kanban + métricas + acciones)
├── Dockerfile             # node:22-alpine
├── .env.example           # Template de variables
├── .gitignore
├── package.json           # Express, cookie-parser, helmet, rate-limit, sqlite3
├── apps.json              # Registro de apps (generado en runtime)
├── audit.log              # Log de auditoría (generado en runtime)
├── public/
│   ├── index.html         # Frontend principal
│   ├── css/styles.css     # CSS Esios style (azul + naranja + liquid glass)
│   └── js/
│       ├── api.js         # Client API
│       ├── cache-bust.js  # Cache busting dinámico
│       ├── config.js      # Configuración frontend
│       ├── data.js        # Gestión de datos
│       ├── render-charts.js
│       ├── render-final.js
│       ├── render.js
│       ├── state.js       # Estado global
│       ├── ui.js          # Componentes UI
│       └── utils.js       # Utilidades
├── scripts/
│   ├── daily-report.js
│   ├── esios-telegram.js
│   ├── fetch-all-indicators.js
│   ├── fetch-esios.js
│   └── montecarlo.js
└── tests/
    ├── api.test.js
    ├── env.test.js
    ├── time.test.js
    └── utils.test.js
```

## 🔑 Variables de Entorno (CRÍTICO)

### Dónde configurarlas
- **NaN:** pestaña **Env** en la web de NaN → dashboard del espacio
- **NUNCA** en el código, commits, o .env en Git

### Variables del proyecto

| Variable | Obligatorio | Descripción |
|---|---|---|
| `ADMIN_PASSWORD` | ⚠️ Parcial | Si falta, se genera una temporal (se imprime en consola al arranque). **Configurar en producción** |
| `ADMIN_USER` | No (default: admin) | Usuario de login admin |
| `PORT` | No (default: 4500) | Puerto del servidor — **debe coincidir con EXPOSE del Dockerfile** |
| `NODE_ENV` | No (default: production) | Entorno (production/development) |
| `GITHUB_TOKEN` | No | Token GitHub para operaciones (backup, sync) |
| `NAN_API_KEY` | No | Clave API de NaN para informes con IA |

### Sistema de Autenticación
- **Cookie-based session** con `cookie-parser`
- `httpOnly: true`, `secure: NODE_ENV === 'production'`
- TTL de sesión: **12 horas**
- Rate limit: **120 requests/minuto**
- Sesiones almacenadas en memoria (objeto `SESSIONS`)
- Password generada automáticamente si no se configura `ADMIN_PASSWORD`

### Health check
- `/health` → `{ status: "ok", uptime, ts }` — siempre responde

## 🐳 Dockerfile

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev 2>&1
COPY . .
RUN mkdir -p data
ENV PORT=4500
EXPOSE 4500
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:4500/health || exit 1
CMD ["node", "server.js"]
```

**Puntos clave:**
- `node:22-alpine` (más reciente que esios-work)
- `EXPOSE 4500` — **verificar que el puerto del espacio NaN coincide**
- `mkdir -p data` para directorio de datos en runtime
- Sin usuario no-root (simplificado)

## 🌐 Endpoints API

### Auth
| Endpoint | Auth | Descripción |
|---|---|---|
| `POST /api/auth/login` | No | Login: `{ user, pass }` → cookie session |
| `POST /api/auth/logout` | No | Logout: borra cookie session |

### Apps (público)
| Endpoint | Auth | Descripción |
|---|---|---|
| `GET /api/apps` | No | Lista de apps registradas |

### Métricas y sistema (requiere auth)
| Endpoint | Auth | Descripción |
|---|---|---|
| `GET /api/metrics` | ✅ | RAM, disco, servicios, proyectos, tokens, gateway |
| `GET /api/system` | ✅ | CPU, plataforma, versión Node, estado gateway/Telegram |

### Kanban (requiere auth)
| Endpoint | Auth | Descripción |
|---|---|---|
| `GET /api/kanban` | ✅ | Listar tareas (SQLite en `/hermes-home/kanban.db`) |
| `POST /api/kanban` | ✅ | Crear tarea: `{ title, priority }` |
| `PUT /api/kanban/:id` | ✅ | Actualizar tarea: `{ status, priority, result }` |

### Acciones (requiere auth)
| Endpoint | Auth | Descripción |
|---|---|---|
| `POST /api/actions/backup` | ✅ | Git backup + push a Mastermind repo |
| `POST /api/actions/sync` | ✅ | Git sync desde origin/main |
| `POST /api/actions/cron` | ✅ | Ejecutar cron jobs |
| `POST /api/actions/restart` | ✅ | Detener gateway |
| `POST /api/actions/health` | ✅ | Health check completo |
| `POST /api/actions/logs` | ✅ | Últimos 20 logs del gateway |

### Actividad
| Endpoint | Auth | Descripción |
|---|---|---|
| `GET /api/activity` | ✅ | Log de auditoría (login, tareas, acciones) |

## 🚀 Procedimiento de Deploy

### Paso 1: Push a GitHub
```bash
cd /root/workspace/nan-dashboard
git add -A
git commit -m "feat: descripción del cambio"
git push origin main
```

### Paso 2: Configurar en NaN
1. Ir al espacio en NaN.builders
2. **Verificar puerto del espacio** — debe coincidir con `EXPOSE 4500` del Dockerfile
3. Ir a pestaña **Env** y configurar:
   - `ADMIN_PASSWORD` = tu_contraseña_segura (**muy importante**)
   - `ADMIN_USER` = admin (o el que prefieras)
   - `GITHUB_TOKEN` = tu_token_github (para backup/sync)
   - `NAN_API_KEY` = tu_clave_nan (opcional)

### Paso 3: Verificar deploy
```bash
# Health check
curl https://ntizar-ntizar.apps.nan.builders/health

# Login de prueba (desde navegador)
# Ir a https://ntizar-ntizar.apps.nan.builders
# Login con ADMIN_USER / ADMIN_PASSWORD
```

### Trigger redeploy si se atasca
```bash
cd /root/workspace/nan-dashboard
git commit --allow-empty -m "chore: trigger redeploy"
git push origin main
```

## ⚠️ Reglas Críticas

1. **Puerto:** Dockerfile EXPOSE = espacio NaN. Si no coinciden → 502 Bad Gateway
2. **ADMIN_PASSWORD:** Si no se configura, se genera una temporal visible en consola. **Configurar en producción**
3. **NUNCA** hacer commit de .env ni contraseñas
4. **Sesiones en memoria:** Si el contenedor se reinicia, se pierden las sesiones activas
5. **Kanban en SQLite:** `kanban.db` en `/hermes-home/kanban.db` — sobrevive reinicios del contenedor
6. **Audit log:** `audit.log` en `/root/workspace/nan-dashboard/audit.log` — sobrevive reinicios
7. **apps.json:** Se genera en runtime en la raíz del proyecto — sobrevive reinicios

## 🎨 Frontend — Estilo Esios

- **CSS:** Azul `#2563eb` + Naranja `#f97316` + efecto liquid glass
- **Tema:** Claro
- **Fuente:** Inter
- **Componentes:** Charts (canvas), kanban board, métricas, login
- **Cache busting:** Dinámico vía `/js/cache-bust.js` con timestamp

## 🐛 Troubleshooting

| Síntoma | Causa | Solución |
|---|---|---|
| 502 Bad Gateway | Puerto no coincide | Dockerfile EXPOSE = espacio NaN |
| 502 Bad Gateway (< 2s) | App crash | Verificar logs, test local |
| Login no funciona | ADMIN_PASSWORD no configurado | Revisar pestaña Env de NaN |
| Sesiones se pierden | Reinicio de contenedor | Normal — sesiones en memoria |
| Kanban no carga | SQLite no inicializado | Crear tabla `tasks` manualmente |
| Backup falla | GITHUB_TOKEN no configurado | Configurar en NaN Env |
| Rate limit 429 | Demasiadas peticiones | Default 120/min — ajustar en code |

## 📊 Métricas del Sistema

El endpoint `/api/metrics` devuelve:
- **RAM:** Usada/Total + porcentaje
- **Disco:** Total/Usado/Libre
- **Servicios activos:** Puertos escuchando
- **Proyectos locales:** Conteo de directorios en `/root/workspace/`
- **Tokens:** Uso diario (input/output/total)
- **Gateway:** Estado (running/stopped) + PID
- **Telegram:** Estado de configuración
- **Skills:** Conteo local + Mastermind
- **Sessions:** Número de sesiones Hermes

## 📦 Dependencias

- **Runtime:** express, cookie-parser, helmet, express-rate-limit, sqlite3
- **Seguridad:** Helmet CSP, rate limiting, httpOnly cookies, secure cookies en prod

## 🔒 Seguridad

- Helmet CSP estricto (default-src: 'self', frame-ancestors: 'self')
- Rate limit: 120 requests/min
- Cookie httpOnly + secure (en producción)
- Sesión TTL: 12 horas
- X-Powered-By deshabilitado
- Audit log de todas las acciones admin
