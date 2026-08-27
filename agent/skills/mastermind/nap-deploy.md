---
name: nap-deploy
description: "Despliegue del NAP Dashboard (React + Vite) en NaN.builders con servidor Express + proxy API"
version: 1.0.0
author: Mastermind
tags: [nap, deploy, nan, web, express, proxy]
---

# NAP Deploy — NaN.builders

## Stack
- Frontend: React + Vite + TypeScript + Tailwind + Leaflet + Recharts
- Backend: Express (servidor estático + proxy API)
- API destino: `https://nap.transportes.gob.es/api` (NAP Transportes)

## Estructura en el servidor

```
/persist/nap-dashboard/
├── server.cjs          # Servidor Express (puerto 3000)
├── dist/               # Frontend compilado
├── src/                # Código fuente React
├── api/nap/            # Proxy API (original para Vercel)
└── package.json
```

## Server (server.cjs)
```javascript
- Express en puerto 3000
- Sirve /dist como estático
- Proxy /api/nap/* → nap.transportes.gob.es/api
- Inyecta NAP_API_KEY del environment
- SPA fallback: todo lo no-API va a index.html
```

## Pasos para desplegar

### En el servidor (ya hecho)
```bash
cd /persist
git clone https://github.com/Ntizar/nap-dashboard.git
cd nap-dashboard
npm install
npm install express http-proxy-middleware
npm run build
```

### Para arrancar
```bash
cd /persist/nap-dashboard
NAP_API_KEY=valor node server.cjs
```

### Para producción (con systemd o similar)
```bash
# Crear servicio para que arranque solo
# NAP_API_KEY debe estar en el environment
```

## Pendiente (lo hace el usuario)
1. Entrar en cloud.nan.builders
2. HTTP Exposure → puerto 3000 → `nap.apps.nan.builders`
3. Env tab → NAP_API_KEY + GITHUB_TOKEN
4. Yo arranco el servidor

## Credenciales
- `NAP_API_KEY` → environment variable (no está en el repo)
- Vía Vercel: `process.env.NAP_API_KEY`
- Vía NaN: `process.env.NAP_API_KEY` (en el server.cjs)