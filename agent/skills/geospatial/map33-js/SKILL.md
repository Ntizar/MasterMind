---
name: map33-js
description: "Usa a hacer mapas 3D con map33 (Three.js Pearson)."
version: "2.0.0"
tags: [mapa-3d, map33, threejs, terrain, tiles, geospatial, npm]
related_skills: [map33-js, threejs-3d-maps, map3d-r3f]
---

# map33 — mapa 3D desde tilesets XYZ (Three.js)

> ⚠️ Corrección 2026-09-05 (auditoría): el paquete npm es **`map33`** (no `map33.js`); la API es `import { Map, Source, MapPicker }` + `new Map(scene, camera, source, position, { nTiles, zoom })`. **No** inventar `new Map33({container})`/`addLayer()`/`setPitch/setBearing`.

**Repo:** `https://github.com/jccf/map33` (JavaScript, ~505⭐, inactivo desde 2023).

## When to Use

- Cuando pidas un **mapa 3D de terreno** construido desde tilesets XYZ/OGC en Three.js (alternativa a maptalks.three).

## Uso (API real)

```bash
npm install map33
```

```js
import { Map, Source, MapPicker } from 'map33';
const m = new Map(scene, camera, source, position, { nTiles: 3, zoom: 12 });
```

## Pitfalls

- Paquete: **`map33`**, no `map33.js`.
- API: `new Map(scene, camera, source, position, opts)`; no `new Map33({container})`/`addLayer`/`setPitch`/`setBearing`.
- No es un drop-in de maptalks.three (construye terreno 3D desde tilesets XYZ).

## Verificación

- Instalar `map33`, crear un `Map` con scene+camera+source y ver el terreno.
