---
name: threejs-procedural-dungeon
description: "Usa a generar mazmorras 3D procedurales en Three.js."
version: "2.0.0"
tags: [threejs, dungeon, procedural, generacion, dungeon-generator, 3d]
related_skills: [threejs-procedural-dungeon, seed-three, ecctrl]
---

# Three.js Procedural Dungeon — mazmorras 3D procedurales

> ⚠️ Corrección 2026-09-05 (auditoría): el comando es `npm run dev` (no `npm start`) y es **pan/orbit** (no first-person). Stars ~495.

**Repo:** `https://github.com/.../threejs-procedural-dungeon` (TypeScript, ~495⭐).

## When to Use

- Cuando pidas **generar una mazmorra 3D procedural** (salas, pasillos, mapa aleatorio) en Three.js.

## Uso

```bash
npm install
npm run dev        # (no npm start) — abre el viewer
```

- Navegación: **pan/orbit** de la escena, no first-person.

## Pitfalls

- Comando de desarrollo: **`npm run dev`**, no `npm start`.
- Cámara: **pan/orbit**, no first-person.

## Verificación

- `npm run dev` y comprobar que genera una mazmorra distinta en cada reload.
