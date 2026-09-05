---
name: plateau-3d-city-mcp
description: "Usa a conectar datos 3D city de PLATEAU vía MCP."
version: "2.0.0"
tags: [plateau, 3d-city, mcp, glb, modelos, japan, server]
related_skills: [plateau-3d-city-mcp, native-mcp, cesium-3d-tiles-vector-data]
---

# PLATEAU 3D City MCP — datos 3D urbanos vía MCP

> ⚠️ Corrección 2026-09-05 (auditoría): el paquete real es **`@yodolabs/plateau-creative-mcp`** (no `@pixelx/plateau-mcp`); las herramientas reales son `download_area`/`load_area`/`filter_buildings`/`delete_buildings`/`extrude_buildings`/`compose_scene`/`export_glb`/`link_buildings_to_pois`/`get_attribution`/`render_via_blender`; el export es **.glb** (no .gltf/.obj).

**Repo:** `https://github.com/pixelx-jp/plateau-creative-mcp` (TypeScript, ~31⭐).

## When to Use

- Cuando quieras traer **datos 3D de ciudades (Project PLATEAU, Japón)** a tu agente/herramienta vía MCP y trabajar con buildings/escena.

## Uso

```bash
npx -y @yodolabs/plateau-creative-mcp       # paquete real (no @pixelx/plateau-mcp)
```

Herramientas (reales): `download_area`, `load_area`, `filter_buildings`, `delete_buildings`, `extrude_buildings`, `compose_scene`, `export_glb`, `link_buildings_to_pois`, `get_attribution`, `render_via_blender`.

## Pitfalls

- Paquete npx: **`@yodolabs/plateau-creative-mcp`** (no `@pixelx/plateau-mcp`).
- Tools: las de arriba (no `load_city`/`query_buildings`/`export_gltf`/`export_obj`/`get_terrain`/`get_roads`).
- Export: **.glb** (single_glb), no .gltf/.obj.

## Verificación

- Conectar el server MCP y llamar `download_area`/`export_glb` sobre un area de PLATEAU.
