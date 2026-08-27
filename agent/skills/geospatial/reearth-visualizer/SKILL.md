---
name: reearth-visualizer
version: "1.0.0"
description: "Reearth Visualizer — plataforma WebGIS open-source con Cesium, storytelling, plugin system y rendering 3D"
---

# Reearth Visualizer — WebGIS Platform

## Descripción

Plataforma WebGIS gratuita, open-source y altamente extensible para visualizar datos GIS. Usa Cesium como motor de rendering 3D. Soporta dibujo interactivo de geometría, styling condicional de capas, storytelling, plugins y publicación de proyectos.

## Por qué importa para David

- **Cesium para WebGIS**: Alternativa robusta a three.js para visualización geoespacial 3D
- **Storytelling**: Feature de narrativas interactivas página a página con datos GIS
- **Plugin system**: Extensibilidad para custom solutions
- **Digital twin**: Soporte nativo para gemelos digitales

## Arquitectura

```
GIS Data (vector, raster, 3D)
    ↓
Cesium Engine (rendering 3D)
    ↓
Reearth Visualizer (WebGIS frontend)
    ├── Conditional layer styling
    ├── Interactive geometry drawing
    ├── Storytelling (page-by-page narratives)
    └── Plugin system (custom solutions)
    ↓
Publish & Share projects
```

Stack: TypeScript, React, Cesium, GraphQL, MongoDB, Go (backend)

## Instalación

```bash
# Docker compose (oficial)
docker-compose up -d

# O usar el visualizer en cloud:
# https://visualizer.developer.reearth.io/
```

## Uso básico

```javascript
// Cargar datos GIS en Cesium
const viewer = new Cesium.Viewer('cesiumContainer', {
  baseLayer: Cesium.IonImagery.fromAssetId(3957)
});

// Añadir capas condicionales
layer.style = {
  color: {
    conditions: [
      ['property("population") > 1000000', 'red'],
      ['property("population") > 100000', 'orange'],
      ['true', 'green']
    ]
  }
};

// Storytelling feature
story.addPage({
  title: 'Madrid Centro',
  camera: {
    position: Cesium.Cartesian3.fromDegrees(-3.7038, 40.4168, 500),
    orientation: { heading: 0, pitch: -30, roll: 0 }
  },
  layers: ['buildings', 'transport', 'points-of-interest']
});
```

## Integración con proyectos de David

- **España Atlas**: Visualización 3D de infraestructura regional con Cesium
- **Time**: Storytelling de rutas y isocronas
- **Digital twin**: Patrón reusable para gemelos digitales de ciudades
- **3D GIS**: Alternativa a three.js para proyectos geoespaciales 3D

## Pitfalls

- Cesium es pesado (~30-50MB bundle size)
- MongoDB para metadata puede ser overkill para proyectos pequeños
- Go backend requiere compilación si se modifica
- Plugin system potente pero requiere conocimiento de React + Cesium
- Cesium Ion requiere API key para datos premium

## Referencias

- GitHub: https://github.com/reearth/reearth-visualizer
- Docs: https://visualizer.developer.reearth.io/
- Cesium: https://cesium.com/
- Reearth: https://reearth.io/
