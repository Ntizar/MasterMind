---
name: fable5-webgpu-procedural
version: "1.0.0"
description: "LAAS — mundo 3D procedural 4x4km con three.js WebGPU, TSL materials y WGSL compute, generado íntegramente por código"
---

# LAAS — Procedural Open World con WebGPU + three.js

## Descripción

Mundo abierto procedural de 4x4 km renderizado en el browser usando three.js WebGPURenderer con TSL materials y raw WGSL compute. Cada mesh, textura y luz es generado por código en boot — el repositorio no contiene assets de imagen, modelo o audio. Reproducible desde un único seed URL parameter.

## Por qué importa para David

- **WebGPU + three.js**: Demo de referencia del estado del arte en rendering 3D procedural
- **Zero assets**: Todo generado proceduralmente → patrón para generación de mundos/terrenos
- **WGSL compute**: Shaders compute para generative algorithms
- **Procedural generation**: Patrón reusable para terrain, vegetation, buildings

## Arquitectura

```
Seed Parameter (?seed=N)
    ↓
Procedural Generation (boot)
    ├── Terrain mesh
    ├── Vegetation (trees, grass)
    ├── Water bodies
    ├── Clouds & lighting
    └── Textures (procedural)
    ↓
WebGPURenderer + TSL Materials
    ↓
Raw WGSL compute shaders
```

Stack: TypeScript, three.js (WebGPURenderer), WebGPU, WGSL, Vite, Playwright (headless QA)

## Uso básico

```tsx
// Acceso directo a la demo
// https://laas-demo.example.com/?seed=42
// (cargar URL con seed para reproducibilidad)
```

## Integración con proyectos de David

- **3D visualization**: Patrón de rendering avanzado para cualquier visualización 3D
- **Procedural terrain**: Generar terrenos para proyectos geográficos
- **Performance**: Pattern de WebGPU compute para processing pesado del lado cliente

## Pitfalls

- WebGPU requiere browser moderno (Chrome 113+, Edge 113+, Opera 99+)
- No hay fallback a WebGL → dispositivos viejos no funcionan
- three.js WebGPURenderer es experimental → API puede cambiar
- Procedural generation heavy: requiere GPU decente (mínimo integrated modern)
- Demo fue generada por IA (Claude Fable 5) → código puede no seguir mejores prácticas

## Referencias

- GitHub: https://github.com/Braffolk/fable5-world-demo
- Brief: PROJECT_LAAS_v2.md (brief humano que guió la generación)
- three.js WebGPU: https://threejs.org/docs/#manual/en/introduction/WebGPU
- WGSL: https://www.w3.org/WGSL/
