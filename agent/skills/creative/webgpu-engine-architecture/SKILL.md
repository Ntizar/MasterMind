---
name: webgpu-engine-architecture
version: "1.0.0"
description: "Usa para construir motores WebGPU extendibles y juegos."
tags: [webgpu, engine, games, rendering, ecs]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [webgpu, engine, games, rendering, ecs]
    related_skills: [threejs-awesome-graphics-agent-skills, webgpu-onnx-detection]
---
# Sundown Engine — Motor WebGPU extendible

## Resumen
`Sundown` es un motor WebGPU de juegos y simulación, extendible, para diversión, juegos e investigación. Incluye abstracciones de render, render graph flexible, sistema de materiales, capa de simulación de gameplay, ECS (fragment framework + TypedArrays), sistema de input por contexto, shaders PBR incluidos, instanciación e incluso un framework ML simple para experimentos IA en tiempo real.

## Uso (comandos reales del README)

```bash
# Instalación
git clone git@github.com:Sunset-Studio/Sundown.git
cd Sundown
npm install

# Desarrollo en navegador
npm run dev

# Desarrollo en instancia electron
npm run devtop
```

## Patrones / Arquitectura
- Renderable abstractions WebGPU; render graph flexible para pipelines de render y compute.
- Sistema de materiales expresivo (shaders y materiales custom).
- Sistema de capas de simulación de gameplay (funcionalidad modular por capas).
- ECS eficiente con fragment framework y TypedArrays.
- Input por contexto (diferentes esquemas y contextos); shaders PBR built-in; instanciación entity-first y auto-instancing con mesh task queue.
- Compute task queue para trabajo de compute shaders; MSDF text rendering; post-process stack configurable; UI inmediata screen-space; AABB tree dinámico para ray casting; helpers para GTLFs, performance scopes, named IDs y frames.
- Framework ML: gradient tape para backprop, DAG subnet API por capas, librería de activaciones/losses/optimizadores, y clase **MasterMind** para orquestar weight sharing, adaptación y retraining en tiempo real de múltiples modelos.

## Pitfalls
- Requiere la última versión de NodeJS instalada antes de `npm install`.
- Puede empaquetarse para web o desktop con Electron Forge.
- El ejemplo `app.js` se incluye desde el `index.html` top-level; reemplazarlo con tus propios experimentos/entry points.

## Verificación
- `npm run dev` abre el navegador con el ejemplo app.js.
- Confirmar que el render graph, ECS y el gradient tape funcionan ejecutando el demo.

## Referencia
README de https://github.com/Sunset-Studios/Sundown. Repo de clone: Sunset-Studio/Sundown.
