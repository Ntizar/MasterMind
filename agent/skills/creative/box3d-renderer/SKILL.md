---
name: box3d-renderer
description: "Usa a simular cajas 3D y física con Box3D (b3)."
version: "2.0.0"
tags: [box3d, fisica, 3d, cajas, c, wasm, simulacion]
related_skills: [box3d-renderer, threejs-3d-maps, ecctrl]
---

# Box3D — motor de física de cajas 3D (API `b3*`)

> ⚠️ Corrección 2026-09-05 (auditoría): el prefijo de API es **`b3*`** (`b3CreateWorld`, `b3WorldId`, `b3CreateBody`, `b3Vec3`); **no** `bd3d*` (`bd3dCreateWorld`... no existe ninguna función `bd3d`).

**Repo:** `https://github.com/erincatto/box3d` (C, ~6.3K⭐). Hay wrapper wasm/npm (`box3d-wasm` / `@...`).

## When to Use

- Cuando pidas **simulación física de cajas/rigid bodies** en 3D (motor ligero de Box3D) desde C o desde el navegador vía wasm.

## Uso (API real, C)

```c
b3WorldId world = b3CreateWorld(bbox);      // NO bd3dCreateWorld
b3BodyId body = b3CreateBody(world, ...);
b3Vec3 v = b3Vec3(1, 2, 3);
```

*(Comprobar los nombres exactos en el repo — el prefijo correcto es `b3`, nunca `bd3d`.)*

## Pitfalls

- Prefijo de API: **`b3*`**, no `bd3d*`.
- No existe `bd3dCreateWorld`/`bd3dCreateBoxBody`.

## Verificación

- Enlazar la cabecera y crear un mundo + un body; comprobar que la simulación avanza con `b3`.
