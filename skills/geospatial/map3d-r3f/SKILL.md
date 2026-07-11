---
name: map3d-r3f
version: "1.0.0"
description: "map3d — generar mapas 3D de ciudades con React-Three-Fiber, datos OSM y exportación GLB"
---

# map3d — 3D City Maps con R3F

## Descripción

Proyecto que genera mapas 3D de ciudades usando React-Three-Fiber (R3F). Construye edificios y carreteras a partir de datos de OpenStreetMap, con exportación GLB incluida. Soporta digital twin, drone surveying y GPS markers.

## Por qué importa para David

- **3D geográfico con React**: Patrón directo para visualización 3D de edificios en proyectos web
- **R3F + Leaflet**: Combina mapa 2D interactivo con renderizado 3D overlay
- **OSM data**: Reutiliza fuentes de datos que David ya maneja
- **GLB export**: Capaz de exportar el modelo 3D para uso fuera del browser

## Arquitectura

```
OSM Data (buildings, roads)
    ↓
React-Three-Fiber (R3F)
    ↓
3D buildings + roads rendering
    ↓
GLB export / Web viewer
```

Stack: TypeScript, React, @react-three/fiber, @react-three/drei, three.js, Leaflet, Zustand

## Uso básico

```tsx
import { Canvas } from '@react-three/fiber'
import { Building } from './components/Building'

// Datos OSM procesados a posiciones 3D
const buildings = osmData.map(b => ({
  position: [b.lon, b.height, b.lat],
  width: b.width,
  depth: b.depth
}))

function CityMap() {
  return (
    <Canvas>
      {buildings.map((b, i) => (
        <Building key={i} {...b} />
      ))}
    </Canvas>
  )
}
```

## Integración con proyectos de David

- **Time**: Visualización 3D de edificios en rutas
- **España Atlas**: Capa 3D de edificios sobre mapa base
- **Digital twin**: Patrón reusable para cualquier city visualization

## Pitfalls

- OSM data no siempre tiene heights → valores faltantes o incorrectos
- Rendimiento: muchos edificios puede ser pesado, considerar LOD (level of detail)
- three.js requiere WebGL, verificar compatibilidad del dispositivo
- Leaflet + R3F overlay requiere sincronización de coordenadas cuidadosa

## Referencias

- GitHub: https://github.com/cartesiancs/map3d
- Demo: https://map.fleet.im/
- React-Three-Fiber: https://docs.pmnd.rs/react-three-fiber/
