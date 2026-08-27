---
name: box3d-renderer
description: Box3D — motor de física 3D para juegos, renderizado de cajas y simulación de colisiones.
---

# Box3D — Motor de Física 3D

## Qué hace

[Box3D](https://github.com/erincatto/box3d) es un motor de física 3D para juegos, escrito en C. Ofrece detección de colisiones, simulación de cuerpos rígidos y restricciones. Alternativa ligera a PhysX o Bullet para proyectos que necesitan física 3D sin la complejidad de motores más grandes.

## Instalación

```bash
git clone https://github.com/erincatto/box3d.git
cd box3d
mkdir build && cd build
cmake ..
make -j$(nproc)
```

## Uso básico

```c
#include "box3d/box3d.h"

// Crear mundo físico
bd3dWorld* world = bd3dCreateWorld();

// Añadir cuerpo rígido
bd3dBody* body = bd3dCreateBoxBody(world, position, size, mass);

// Simular paso de física
bd3dStepWorld(world, timestep);

// Obtener posición actual
bd3dVec3 pos = bd3dGetBodyPosition(body);
```

## Integración con Three.js

```javascript
// Ejemplo conceptual de integración con Three.js
// Box3D calcula la física en C → se exporta a JavaScript vía WASM

import * as THREE from 'three';
import { Box3DPhysics } from 'box3d-wasm';

const physics = new Box3DPhysics();
const scene = new THREE.Scene();

// Sincronizar física → renderizado
function tick() {
  physics.step(1/60);
  
  // Actualizar meshes según posiciones de física
  for (const body of physics.getBodies()) {
    body.mesh.position.set(...body.getPosition());
    body.mesh.quaternion.set(...body.getOrientation());
  }
  
  renderer.render(scene, camera);
  requestAnimationFrame(tick);
}
```

## Pitfalls

- Motor en C puro — requiere bindings para JavaScript/TypeScript
- No incluye rendering, solo física
- Documentación limitada — consultar código fuente y tests
- Mejor para simulaciones simples que para juegos complejos

## Referencias

- Repo: https://github.com/erincatto/box3d
- Relacionado: `threejs-3d-maps`, `fable5-webgpu-procedural`, `seed-three`