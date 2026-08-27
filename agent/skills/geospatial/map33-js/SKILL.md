---
name: map33-js
description: Visualización 3D de mapas con Three.js — alternative a maptalks.three para mapas 3D interactivos.
version: "1.0.0"
tags: [three.js, 3D, maps, visualization, WebGL]
---

# map33.js — Mapas 3D con Three.js

## Resumen

Visualización 3D de mapas con Three.js — alternativa ligera a maptalks.three. 500⭐.

## Repo de referencia

- **GitHub:** `github.com/blaze33/map33.js`
- **Lenguaje:** JavaScript/TypeScript
- **Licencia:** MIT

## Instalación

```bash
npm install map33.js
# o CDN
<script src="https://cdn.jsdelivr.net/npm/map33.js/dist/map33.min.js"></script>
```

## Uso Básico

```javascript
import Map33 from 'map33.js';

const map = new Map33({
  container: 'map-container',
  center: [40.4168, -3.7038],  // Madrid
  zoom: 12,
  style: 'osm',  // 'osm', 'satellite', 'dark'
});

// Añadir capas
map.addLayer({
  type: 'circle',
  coordinates: [[40.4168, -3.7038]],
  radius: 500,
  color: '#2563eb',
  opacity: 0.3,
});

// Rotación 3D
map.setPitch(60);  // Inclinación 60 grados
map.setBearing(45);  // Rotación 45 grados
```

## Patrones Clave

1. **Estilos:** OSM, satellite, dark, custom tiles
2. **Capas:** Círculos, líneas, polígonos, marcadores 3D
3. **Interacción:** Zoom, rotación, inclinación, click events
4. **GeoJSON:** Soporte nativo para GeoJSON features
5. **Performance:** Web Workers para procesamiento pesado

## Integración con Mastermind

- Complementa `maptalks.three` — más ligero, menos dependencias
- Ideal para `threejs-3d-maps` con enfoque en visualización
- Útil para `map3d-r3f` — alternativa vanilla a React
- Perfecto para dashboards con mapas 3D interactivos

## Pitfalls

- **Comunidad:** Menos comunidad que maptalks.three
- **Documentación:** Docs limitados, hay que leer el código
- **Extensiones:** Menos plugins disponibles
- **WebGL:** Requiere soporte WebGL en el navegador

## Referencias

- [GitHub: blaze33/map33.js](https://github.com/blaze33/map33.js)
