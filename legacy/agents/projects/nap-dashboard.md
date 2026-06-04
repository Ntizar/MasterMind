---
nombre: NAP Dashboard
alias: nap-dashboard
tipo: proyecto
clusters: [arquitectura-software, datos]
repo_local: C:\Ntizar_Obsidian\Ntizar_Brain\Github\nap-dashboard
repo_remoto: https://github.com/ntizar/nap-dashboard
live_url: https://nap-dashboard.vercel.app
estado: activo
---

# NAP Dashboard

Dashboard de movilidad y transporte público construido sobre la API del NAP (Punto de Acceso Nacional de datos de transporte). Permite explorar operadores, líneas, paradas y archivos GTFS de forma visual.

## Stack
- React + TypeScript + Vite
- Tailwind CSS v4
- Leaflet (mapas)
- Vercel Functions (proxies server-side)
- fflate (parseo ZIP GTFS en browser)

## Decisiones arquitectónicas permanentes
- CORS bloqueado en NAP API y en URLs GTFS externas → dos proxies Vercel separados
- `api/nap/proxy.ts` → proxy REST (JSON/text, headers de auth)
- `api/nap/gtfs-proxy.ts` → proxy descargas binarias (ZIPs) con whitelist de dominios
- API key nunca en repo: vive en `localStorage` del cliente, viaja como header `X-Api-Key` al proxy
- Modal bloqueante `ApiKeyModal` como gate de entrada — el usuario no puede saltárselo
- Ruta de `gtfs-proxy` en `vercel.json` ANTES del catch-all del proxy NAP
- Tailwind CSS 4: usar CSS variables (`--nap-blue`) en lugar de `theme()` config

## Pendientes conocidos
- Test con API key real en producción (Vercel deploy)

## Learnings de este proyecto
- [[2026-03-19-nap-dashboard-ciclo5]]
- [[2026-03-19-nap-dashboard-ciclo6]]
