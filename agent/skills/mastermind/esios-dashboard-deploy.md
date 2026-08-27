---
name: esios-dashboard-deploy
description: "Procedimiento completo para desplegar el dashboard ESIOS (esios-work) en NaN.builders — estructura, variables de entorno, Dockerfile, endpoints y troubleshooting."
version: 1.0.0
author: Ntizar
---

# Deploy Dashboard ESIOS en NaN.builders

Guía paso a paso para desplegar el proyecto `esios-work` (dashboard energético español) en NaN.builders.

## 📁 Repositorio y ubicación

- **Repo:** `github.com/Ntizar/esios-work`
- **Local:** `/root/workspace/esios-work`
- **Stack:** Node.js 20, Express, Docker multi-stage
- **Puerto:** 4000

## 🏗️ Arquitectura del proyecto

```
esios-work/
├── server.js              # Express principal (bootstrap + routing)
├── Dockerfile             # Multi-stage (node:20-alpine)
├── .env.example           # Template de variables
├── .dockerignore          # Excluye node_modules, .env, .git
├── package.json           # Express, helmet, dotenv, csv, pdfkit
├── public/                # Frontend estático (HTML, CSS, JS modular)
├── src/
│   ├── config/env.js      # Validación de variables de entorno
│   ├── domains/
│   │   ├── energy/        # energy.service.js, summary.service.js
│   │   ├── forecast/      # montecarlo.service.js
│   │   └── reports/       # report.service.js
│   ├── infra/
│   │   ├── cache/         # memory-cache.js
│   │   └── clients/       # esios.client.js, nan.client.js
│   ├── jobs/
│   └── shared/
│       ├── io/            # csv.repository.js
│       ├── time/          # madrid.js (timezone Europe/Madrid)
│       └── validation/
├── data/
│   ├── all-esios-indicators.json
│   ├── esios-indicator-index.json
│   └── esios-indicator-index.md
└── scripts/               # fetch-esios.js, montecarlo.js, telegram, etc.
```

## 🔑 Variables de Entorno (CRÍTICO)

### Dónde configurarlas
- **NaN:** pestaña **Env** en la web de NaN → dashboard del espacio
- **NUNCA** en el código, commits, o .env en Git

### Variables del proyecto

| Variable | Obligatorio | Descripción |
|---|---|---|
| `ESIOS_API_TOKEN` | ✅ SÍ | Token API de ESIOS/REE. Se obtiene en https://esos.ree.es |
| `PORT` | No (default: 4000) | Puerto del servidor — **debe coincidir con EXPOSE del Dockerfile** |
| `NAN_API_KEY` | No | Clave API de NaN para informes con IA. Si falta, endpoint `/informe` se desactiva |
| `ALLOWED_ORIGINS` | No (default: *) | Orígenes CORS permitidos, coma separados |
| `CACHE_TTL_MS` | No (default: 300000) | TTL del cache en ms (5 min) |

### Validación
El archivo `src/config/env.js` verifica `ESIOS_API_TOKEN` al arranque. Si falta, el proceso **exita con código 1**.

### Health checks
- `/healthz` → `{ status: "ok", uptime, ts }` — siempre responde
- `/readyz` → `{ status: "ready"/"degraded", checks: { esios_api_token: true/false, nan_api_key: true/false } }` — verifica tokens

## 🐳 Dockerfile

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
COPY scripts/ ./scripts/

USER appuser
EXPOSE 4000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- http://localhost:4000/healthz || exit 1
CMD ["node", "server.js"]
```

**Puntos clave:**
- Multi-stage build con `node:20-alpine`
- Usuario no-root (`appuser`)
- `EXPOSE 4000` — **debe coincidir con el puerto del espacio NaN**
- HEALTHCHECK configurado
- Copia selectiva: solo lo necesario

## 🌐 Endpoints API

| Endpoint | Descripción |
|---|---|
| `GET /api/esios/precios?fecha=YYYY-MM-DD` | PVPC €/MWh por hora |
| `GET /api/esios/demanda?fecha=YYYY-MM-DD` | Demanda real vs prevista |
| `GET /api/esios/generacion?fecha=YYYY-MM-DD` | Generación por tipo (hídrica, eólica, solar, etc.) |
| `GET /api/esios/co2?fecha=YYYY-MM-DD` | CO2 libre y emisiones |
| `GET /api/esios/interconexiones?fecha=YYYY-MM-DD` | Francia, Portugal, Marruecos |
| `GET /api/esios/generacion-real?fecha=YYYY-MM-DD` | Renovables vs no renovables |
| `GET /api/esios/prevision?fecha=YYYY-MM-DD` | Previsión eólica, solar, renovable (D1/H3) |
| `GET /api/esios/mercado?fecha=YYYY-MM-DD` | Spot, intra-día, restricciones |
| `GET /api/esios/capacidad?fecha=YYYY-MM-DD` | Potencia disponible e instalada |
| `GET /api/esios/summary?fecha=YYYY-MM-DD` | Resumen completo combinado |
| `GET /api/esios/prediccion?fecha=YYYY-MM-DD` | Monte Carlo con 1000 simulaciones |
| `GET /api/esios/informe?fecha=YYYY-MM-DD` | Informe IA (requiere NAN_API_KEY) |
| `GET /metrics` | Prometheus metrics (cache, uptime) |

## 🚀 Procedimiento de Deploy

### Paso 1: Push a GitHub
```bash
cd /root/workspace/esios-work
git add -A
git commit -m "feat: descripción del cambio"
git push origin main
```

### Paso 2: Configurar en NaN
1. Ir al espacio en NaN.builders
2. Verificar que el **puerto del espacio** coincide con `EXPOSE 4000` del Dockerfile
3. Ir a pestaña **Env** y configurar:
   - `ESIOS_API_TOKEN` = tu_token_de_esios
   - `NAN_API_KEY` = tu_clave_nan (opcional)
   - `ALLOWED_ORIGINS` = https://tu-dominio.com (en producción)

### Paso 3: Verificar deploy
```bash
# Health check
curl https://esios-dashboard-ntizar-ntizar.apps.nan.builders/healthz

# Readiness check (verifica tokens)
curl https://esios-dashboard-ntizar-ntizar.apps.nan.builders/readyz

# API endpoint
curl -s "https://esios-dashboard-ntizar-ntizar.apps.nan.builders/api/esios/summary?fecha=2026-05-25" | head -c 200
```

### Trigger redeploy si se atasca
```bash
cd /root/workspace/esios-work
git commit --allow-empty -m "chore: trigger redeploy"
git push origin main
```

## ⚠️ Reglas Críticas

1. **Puerto:** Dockerfile EXPOSE = server.js PORT = espacio NaN. Si no coinciden → 502 Bad Gateway
2. **ESIOS_API_TOKEN:** Obligatoria. Sin ella el proceso exita al arranque
3. **NUNCA** hacer commit de .env ni tokens
4. **npm ci** en vez de npm install — reproducibilidad en builds
5. **Cache:** Los datos se cachean en memoria (5 min default). Cambiar con `CACHE_TTL_MS`
6. **CORS:** En producción poner `ALLOWED_ORIGINS` específico, no `*`
7. **Timezone:** Todo en `Europe/Madrid`

## 🐛 Troubleshooting

| Síntoma | Causa | Solución |
|---|---|---|
| 502 Bad Gateway (< 2s) | App crash al arrancar | Verificar `ESIOS_API_TOKEN` en pestaña Env de NaN |
| 502 Bad Gateway (2-30s) | Request lenta / hanging | Timeout en API ESIOS, verificar red |
| 502 Bad Gateway (> 30s) | Timeout Cloudflare/NaN | Backend demasiado lento, optimizar |
| Datos stale en frontend | Cache de navegador | El server envía `Cache-Control: no-cache` para HTML/JS |
| `/readyz` muestra `degraded` | Token ESIOS faltante | Configurar `ESIOS_API_TOKEN` en NaN Env |
| Error 401 ESIOS | Token inválido | Revisar token en https://esos.ree.es |
| Error 429 | Rate limit ESIOS | Esperar 1s entre requests |

## 📊 Indicadores ESIOS — Reglas de Unidades (CRÍTICO)

### kWh → MW (dividir entre 1000)
IDs: 10035-10041 (generación medida), 10205 (solar medida), 10351-10352 (renovable/no renovable real)

### MW directo
IDs: 1001 (PVPC), 1293 (demanda), 10006 (CO2 libre), 4 (nuclear), 12 (eólica prog.), 14 (solar FV prog.)

### CO2 específico
- `10006` → MW (potencia limpia), NO % ni kWh
- `10355` → tCO₂/MWh (ratio específico), NO t/h

### Pitfall: ID 10042 vs 10041
- **10041** = "Otras renovables medida" (el correcto)
- **10042** = "Total Gen + Interconexiones programada P48" (NO es renovables)
- Si se usa 10042 → datos null o incorrectos

## 🧪 Tests

```bash
cd /root/workspace/esios-work
npm test          # Jest (24/24 passing)
npm run test:watch
```

## 📦 Dependencias

- **Runtime:** express, helmet, dotenv, csv-parse, csv-stringify, pdfkit
- **Dev:** jest, supertest, nock, eslint, vitest
