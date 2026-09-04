---
name: mapcn
description: MapCN — componentes de mapa React listos para usar (MapLibre GL + Tailwind + shadcn/ui), de AnmolSaini16/mapcn.
version: "2.0.0"
category: mapcn
tags: [mapas, react, maplibre, shadcn, componentes, frontend]
---

# MapCN (AnmolSaini16/mapcn — 11.9k⭐, MIT, TypeScript)

> CORRECCIÓN 2026-08-31: el skill anterior describía otra librería "MapCN" de mapeo en China — ERROR. El repo real es una librería de **componentes de mapa para React**.

## Qué es

Componentes de mapa React copy-paste (modelo shadcn): zero config, un comando de setup, construidos sobre **MapLibre GL**, estilizados con Tailwind, compatibles con shadcn/ui. Docs: https://mapcn.dev/docs

- 🎨 Theme-aware (claro/oscuro automático)
- 📍 Markers & popups con tooltips y labels
- 🛤️ Rutas y paths declarativos
- 🎮 Controles: zoom, compass, locate, fullscreen
- 🧩 Componible: UIs complejas con componentes simples

## Instalación

```bash
# setup en un proyecto Next.js/React (shadcn CLI)
npx shadcn@latest add "https://mapcn.dev/r/..."   # ver docs/installation
```
Stack: maplibre-gl, tailwindcss, radix-ui, recharts, lucide-react.

## Basemap (ATENCIÓN licencia)

Usa **CARTO Basemaps** por defecto:
- Uso comercial → requiere licencia CARTO Enterprise
- No comercial → gratis
- Alternativa → tiles OSM u otro proveedor MapLibre-compatible (MapTiler, Stadia)

Para proyectos de David (España, dashboards públicos): usar tiles OSM/IGN (ver skill ign-wmts-tiles) para evitar restricciones CARTO.

## Casos de uso para David

- Dashboards con mapa en React (DataHub España, visores)
- Patrones declarativos para markers/rutas que se pueden portar a vanilla
- Theme-aware maps sin CSS custom

## Pitfalls

- Está pensado para React/Tailwind/shadcn — en proyectos vanilla (p.ej. visores HTML puros) conviene usar maplibre-gl directo y solo copiar patrones
- CARTO basemaps: comprobar licencia si el proyecto es comercial
- Proyecto joven (2025-12) — API aún puede cambiar
