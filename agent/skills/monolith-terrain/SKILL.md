---
name: monolith-terrain
description: Monolith Terrain — visualización 3D de terreno con Three.js y datos geoespaciales.
category: geospatial
---

# Monolith Terrain — Visualización 3D de Terreno

## Qué es

Monolith Terrain es una herramienta de visualización 3D de terreno que usa:
- **Three.js** — renderizado 3D en navegador
- **Data-driven** — genera terreno desde datos DEM/heightmap
- **Interactive** — navegación interactiva con cámara libre
- **Lightweight** — corre 100% en el cliente

## Instalación

```bash
git clone https://github.com/kaolti/monolith-terrain.git
cd monolith-terrain
npm install
npm start
```

## Casos de uso para David

- **Visualización DEM** — mostrar elevación de terreno español
- **Integración** — usar como referencia para dashboards geoespaciales
- **Three.js patterns** — patrones de malla 3D para terrenos
- **Heightmap processing** — generar heightmaps desde datos satelitales

## Pitfalls

- Depende de Three.js version específica
- Los heightmaps grandes pueden ser lentos en navegador
- Requiere datos DEM/heightmap de entrada
- No incluye datos de terreno — solo visualización

## Referencias

- Repo: `github.com/kaolti/monolith-terrain` (69⭐)

## Comparativa de alternativas

- **[kaolti/monolith-terrain](https://github.com/kaolti/monolith-terrain)** — referencia de terreno 3D topográfico con tint hipsométrico, markers de picos, escaneo radar y tours; la implementación de la que este skill es guía.
