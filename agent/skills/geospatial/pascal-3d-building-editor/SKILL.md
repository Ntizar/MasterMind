---
name: pascal-3d-building-editor
version: "1.0.0"
description: "Editor 3D de edificios en navegador con R3F, WebGPU y MCP."
tags: [three, r3f, webgpu, 3d, edificios, gis, city, editor, mcp]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [three, r3f, webgpu, 3d, edificios, gis, mcp]
    related_skills: [photorealistic-3d-tiles-threejs, threejs-3d-maps, map3d-r3f, cesium-3d-tiles-vector-data]
---

# Pascal Editor — Editor 3D de Edificios (Web)

## Resumen

Editor 3D de edificios construido con **React Three Fiber + WebGPU** (repo `pascalorg/editor`, ~21.8K⭐).
Pensado para modelado urbano 3D / CityGIS / BIM web: crear y editar volumetrías de edificios desde el navegador.
Se consume como paquetes npm (`@pascal-app/core`, `@pascal-app/viewer`, `@pascal-app/cli`) y arranca con **un solo comando**.

## Instalación y uso

No hace falta clonar el repo. Node.js **22.13+** crea una instalación local persistente:

```bash
npx @pascal-app/cli editor
```

El CLI arranca el editor **y un servicio MCP autenticado en segundo plano**, elige puertos loopback libres de colisiones
y guarda los proyectos en `~/.pascal/data/pascal.db`.

Para conectar un agente LLM:

```bash
pascal mcp connect
```

Docs: https://editor.pascal.app/docs/developer

## Arquitectura / Patrones reutilizables

- **Stack**: React Three Fiber (R3F) + WebGPU → render de escena 3D urbana en el navegador sin backend pesado.
- **Paquetes modulares**: `@pascal-app/core` (lógica), `@pascal-app/viewer` (render), `@pascal-app/cli` (tooling).
- **MCP server embebido**: el editor se *expone* a agentes vía MCP (`pascal mcp connect`) → edición de edificios
  por prompt, no solo por UI. Patrón potente para herramientas 3D agentic-first.
- **Persistencia local**: SQLite (`~/.pascal/data/pascal.db`), sin servidor externo obligatorio.

## Pitfalls

- Requiere **Node 22.13+** — con versiones viejas falla el CLI.
- La parte WebGPU necesita navegador con soporte WebGPU (Chrome/Edge recientes); en iOS/Safari verificar.
- Los puertos se eligen automáticamente para evitar colisiones con otros servicios — no forzar puertos a mano.

## Verificación

Tras `npx @pascal-app/cli editor` debe abrirse el editor y crearse `~/.pascal/data/pascal.db`.
`pascal mcp connect` debe resolver sin error y exponer las herramientas MCP al agente.

## Referencia

- Repo: https://github.com/pascalorg/editor
- Paquetes npm: `@pascal-app/core`, `@pascal-app/viewer`, `@pascal-app/cli`
- Docs: https://editor.pascal.app/docs/developer
