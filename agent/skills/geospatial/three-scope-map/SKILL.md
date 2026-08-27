---
name: three-scope-map
description: Mapa 3D con Three.js — visualización de datos geoespaciales en tres dimensiones.
version: "1.0.0"
tags: [three.js, 3D, maps, geospatial, visualization, WebGL]
---

# Three-Scope Map — Mapas 3D con Three.js

## Resumen

Mapa 3D con Three.js — visualización de datos geoespaciales en tres dimensiones. 145⭐.

## Repo de referencia

- **GitHub:** `github.com/songsummer920-dazzle/three-scope-map-skill`
- **Lenguaje:** JavaScript/Three.js
- **Licencia:** MIT

## Instalación

```bash
npm install three-scope-map
# o clonar
git clone https://github.com/songsummer920-dazzle/three-scope-map-skill.git
```

## Uso Básico

```javascript
import ThreeScopeMap from 'three-scope-map';

const map = new ThreeScopeMap({
  container: '#map',
  center: [40.4168, -3.7038],  // Madrid
  zoom: 12,
  terrain: true,  // Terreno 3D
  buildings: true,  // Edificios extruidos
});

// Añadir datos
map.addPoints([
  { lat: 40.4168, lng: -3.7038, value: 100, color: '#f97316' },
  { lat: 40.4200, lng: -3.7100, value: 200, color: '#2563eb' },
]);

// Añadir rutas
map.addRoute({
  coordinates: [[40.4168, -3.7038], [40.4200, -3.7100]],
  color: '#10b981',
  width: 3,
});
```

## Funcionalidades

1. **Terreno 3D:** Topografía con elevación real
2. **Edificios:** Extrusión de edificios desde datos OSM
3. **Heatmaps:** Visualización de densidad con mapas de calor
4. **Rutas 3D:** Líneas y rutas en 3D
5. **Interacción:** Zoom, rotación, click, hover

## Integración con Mastermind

- Complementa `map3d-r3f` — Three.js vanilla vs React
- Útil para `threejs-3d-maps` — visualización geoespacial
- Ideal para `transit-3d-realtime` — rutas de transporte en 3D
- Reemplaza Cesium.js para setups más ligeros

## Pitfalls

- **Performance:** Terreno 3D + edificios puede ser pesado
- **Datos:** Necesita datos OSM/terrain para edificios y topografía
- **Mobile:** Puede no funcionar bien en dispositivos móviles
- **Dependencias:** Three.js + loaders adicionales

## Referencias

- [GitHub: songsummer920-dazzle/three-scope-map-skill](https://github.com/songsummer920-dazzle/three-scope-map-skill)
