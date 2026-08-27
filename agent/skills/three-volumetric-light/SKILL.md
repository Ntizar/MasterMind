---
name: three-volumetric-light
description: Three.js Volumetric Light — efecto de luz volumétrica/crepuscular con Three.js y shaders custom.
category: creative
---

# Three.js Volumetric Light — Efecto de Luz Volumétrica

## Qué es

Three.js Volumetric Light es una implementación de efectos de luz volumétrica (god rays, crepuscular rays) en Three.js:
- **Volumetric lighting** — efecto de rayos de luz en 3D
- **Post-processing** — implementado como post-process effect
- **Shader-based** — usa custom shaders para rendimiento
- **Real-time** — corre en tiempo real en navegador

## Instalación

```bash
git clone https://github.com/cullenwebber/three-volumetric-light.git
cd three-volumetric-light
npm install
```

## Casos de uso para David

- **Visualización urbana** — luz solar en renders de ciudades 3D
- **Geospatial 3D** — simular iluminación solar sobre terreno
- **Three.js effects** — efectos visuales avanzados
- **Dashboard visual** — mejorar estética de dashboards 3D

## Pitfalls

- Efecto computacionalmente pesado en GPU
- Depende de Three.js post-processing API
- Puede ser lento en dispositivos móviles
- No es un sistema de iluminación completo — solo un efecto

## Referencias

- Repo: `github.com/cullenwebber/three-volumetric-light` (32⭐)
