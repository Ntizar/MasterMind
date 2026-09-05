---
name: ez-tree
description: "Usa a generar árboles 3D procedurales con Three.js."
version: "2.0.0"
tags: [ez-tree, arboles, procedural, threejs, 3d, glb, png]
related_skills: [threejs-3d-maps, ecctrl, seed-three, threejs-procedural-dungeon]
---

# EzTree — generador procedural de árboles 3D (Three.js)

> ⚠️ Corrección 2026-09-05 (auditoría): la v1 lo describía como "visualizador de grafos" con `new EzTree({container, data, layout})`, `tree.render()` y export SVG — **no existe**. EzTree es un **generador procedural de árboles 3D** para Three.js (paquete `@dgreenheck/ez-tree`).

**Repo:** `https://github.com/dgreenheck/ez-tree` (JavaScript, ~1.6K⭐).

## When to Use

- Cuando pidas **generar árboles 3D procedurales** (tronco, ramas, hojas) para una escena Three.js, con semilla reproducible y export.

## Uso (API real)

```bash
npm install @dgreenheck/ez-tree
```

```js
import * as THREE from 'three';
import { Tree } from '@dgreenheck/ez-tree';   // clase Tree, no EzTree

const tree = new Tree();
tree.options.seed = 42;                        // o tree.options.* (trunk, branch, leaves)
tree.generate();                               // genera la geometría
// export: PNG / GLB
```

## Pitfalls

- Paquete: **`@dgreenheck/ez-tree`**, no `ez-tree`; clase **`Tree`**, no `EzTree`.
- Proposito: **árboles procedurales 3D**, no visualización de grafos/mapas de decisión.
- **No** hay `tree.render()`, `tree.on('click')`, `layout` de grafo ni export SVG.

## Verificación

- `new Tree()` + `tree.generate()` y comprobar la geometría de árbol en la escena; exportar GLB.
