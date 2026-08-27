---
name: seed-three
description: SeedThree — generación procedural de escenas 3D con Three.js y WebGPU.
category: geospatial
---

# SeedThree — Escenas 3D Procedurales con Three.js

## Qué es

SeedThree es una librería para generar escenas 3D procedurales usando:
- **Three.js** — motor 3D en navegador
- **Procedural generation** — generar geometría algorítmicamente
- **WebGPU** — acceso a GPU para renderizado avanzado
- **Seed-based** — reproducibilidad con seeds

## Instalación

```bash
git clone https://github.com/SkyeShark/SeedThree.git
cd SeedThree
npm install
```

## Casos de uso para David

- **Terrenos procedurales** — generar terreno desde seed
- **City generation** — generar ciudades procedurales
- **Three.js patterns** — patrones avanzados de Three.js
- **WebGPU experiments** — experimentar con WebGPU

## Pitfalls

- Requiere navegador con soporte WebGPU
- Los shaders custom pueden ser complejos
- Depende de Three.js version específica
- No incluye datos geoespaciales — solo generación procedural

## Referencias

- Repo: `github.com/SkyeShark/SeedThree` (60⭐)
