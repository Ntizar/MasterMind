---
fecha: 2026-03-19
tarea: nap-dashboard-ciclo6
tipo: software
complejidad: alta
clusters: [arquitectura-software, datos]
proyecto: nap-dashboard
patron: dual-proxy-cors-pattern
---

# NAP Dashboard — ciclo 6: GTFS Proxy + Viewer v2 + Design System

## Decisión clave
Descargar ZIPs GTFS de URLs externas (mf.transportes.gob.es) también tiene CORS.
Se necesita un segundo proxy dedicado (`api/nap/gtfs-proxy.ts`) separado del proxy NAP,
con whitelist explícita de dominios permitidos para evitar uso como proxy abierto.
En Vite dev, se necesita un middleware local que simule este endpoint porque
las Vercel Functions no corren con `vite dev` (solo con `vercel dev`).

## Patrón reutilizable
sí → **dual-proxy-cors-pattern**
Cuando hay dos fuentes de CORS distintas (API + archivos externos):
1. `api/nap/proxy.ts` — proxy para la API REST (headers de auth, JSON/text)
2. `api/nap/gtfs-proxy.ts` — proxy para descargas binarias (ZIPs) desde URLs externas
3. `vercel.json` — ruta específica para `gtfs-proxy` ANTES del catch-all del proxy NAP
4. `vite.config.ts` — middleware plugin que simula ambos proxies en dev local

## Qué funcionó
- `fflate.unzipSync` en el browser — parseo de ZIP GTFS sin Node.js, sin dependencia pesada
- Limitar `stop_times.txt` a 100k filas — previene crash del browser con archivos grandes
- `availableFiles[]` en el parser — la UI sabe exactamente qué tabs mostrar sin adivinar
- Tailwind CSS 4 con CSS variables — `--nap-blue`, `--nap-orange`, etc. son más robustas
  que `theme()` config que no funciona igual en v4
- `MapBoundsAdjuster` con `useEffect` — evita el loop de re-renders de Leaflet

## Qué evitar
- No poner la ruta de `gtfs-proxy` después del catch-all en `vercel.json` —
  el catch-all la absorbe y nunca llega al handler correcto
- No usar `@import url(...)` después de `@import "tailwindcss"` en CSS —
  Vite lanza warning y el orden importa para la cascada
- No confiar en que `downloadLink` devuelve JSON — devuelve texto plano con la URL;
  el proxy debe pasar `Content-Type: text/plain` y el cliente leer `.text()`

## Skills usados
- software-dev.md
- dashboard-dev.md

## Tests/criterios que validaron esto
REVIEWER PASS — commit 295865e pushed.
Funcionalidad: GTFS ZIP se descarga vía gtfs-proxy, se parsea con fflate,
viewer muestra trips/paradas/calendarios/frecuencias/tarifas.
Design system: NAP colors, Inter font, sidebar blanco, KPI cards con gradiente.

## Dashboard: datos del proyecto
fuente: nap.transportes.gob.es + mf.transportes.gob.es (ZIPs GTFS externos)
encoding_encontrado: UTF-8 (GTFS CSV dentro de ZIP)
problema_principal: CORS en URL de descarga GTFS externa + plain-text downloadLink
solucion_aplicada: gtfs-proxy dedicado con whitelist + dev middleware en vite.config.ts
tipo_artefacto: React SPA + 2 Vercel Functions proxy

## Conexiones
**Clusters:** #arquitectura-software · #datos
**Proyecto:** [[nap-dashboard]]
**Aprendizajes relacionados:** [[2026-03-19-nap-dashboard-ciclo5]] · [[2026-03-19-dashboard-skill-md]]
