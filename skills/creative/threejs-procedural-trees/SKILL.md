---
name: threejs-procedural-trees
version: "1.0.0"
description: "Generación procedural de árboles 3D con three.js — L-systems, recursive branching, procedural geometry. Inspirado en dgreenheck/ez-tree (⭐1.5K)."
tags: [threejs, procedural, trees, 3d, l-system, geometry, nature]
---

# Árboles Procedurales con Three.js

## Resumen

Genera árboles 3D realistas proceduralmente usando three.js. Implementa L-systems para branching recursivo, con control de parámetros: profundidad, ángulo, longitud, grosor, color de hojas.

## Cuándo usar

- Visor 3D con vegetación procedural
- Visualización urbana con árboles
- Escenas naturales generativas
- Decoración de mapas 3D con árboles

## Patrón de uso

```javascript
import * as THREE from 'three';

// Generar árbol procedural con L-system
function generateTree(params = {}) {
  const {
    maxDepth = 5,
    branchAngle = 25,
    lengthRatio = 0.75,
    radiusRatio = 0.65,
    leafSize = 0.3,
    leafColor = 0x4a7c3a,
    barkColor = 0x6b4f3a
  } = params;

  const tree = new THREE.Group();
  
  function branch(depth, length, radius, direction, position) {
    if (depth <= 0 || length < 0.1) {
      // Hoja
      const leafGeom = new THREE.IcosahedronGeometry(leafSize, 0);
      const leafMesh = new THREE.Mesh(leafGeom, new THREE.MeshLambertMaterial({ color: leafColor }));
      leafMesh.position.copy(position);
      tree.add(leafMesh);
      return;
    }
    
    // Tronco/rama
    const geom = new THREE.CylinderGeometry(radius * radiusRatio, radius, length, 6);
    const mesh = new THREE.Mesh(geom, new THREE.MeshLambertMaterial({ color: barkColor }));
    mesh.position.copy(position);
    mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction);
    tree.add(mesh);
    
    // Posición final de la rama
    const endPos = position.clone().add(direction.clone().multiplyScalar(length));
    
    // Ramas hijas (2-3 ramas por nodo)
    const numBranches = 2 + Math.floor(Math.random() * 2);
    for (let i = 0; i < numBranches; i++) {
      const newDir = direction.clone();
      newDir.applyAxisAngle(
        new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize(),
        THREE.MathUtils.degToRad(branchAngle * (0.5 + Math.random() * 0.5))
      );
      branch(depth - 1, length * lengthRatio, radius * radiusRatio, newDir, endPos);
    }
  }
  
  branch(maxDepth, 2.0, 0.3, new THREE.Vector3(0, 1, 0), new THREE.Vector3(0, 0, 0));
  return tree;
}

// Añadir árbol a la escena
const tree = generateTree({ maxDepth: 6, leafColor: 0x2d8a4e });
scene.add(tree);
```

## Parámetros clave

| Parámetro | Default | Efecto |
|-----------|---------|--------|
| maxDepth | 5 | Profundidad de recursión (más = más ramas) |
| branchAngle | 25° | Ángulo de bifurcación |
| lengthRatio | 0.75 | Ratio de longitud rama hija/padre |
| radiusRatio | 0.65 | Ratio de grosor rama hija/padre |
| leafSize | 0.3 | Tamaño de hojas |
| numBranches | 2-3 | Ramas por nodo |

## Pitfalls

- **Performance:** maxDepth > 7 = miles de meshes. Usar InstancedMesh para hojas.
- **Geometría:** CylinderGeometry con pocos segmentos (6) para optimizar.
- **Seed:** Usar PRNG con seed para árboles reproducibles.
- **Wind animation:** Animar hojas con shader de vertex displacement para efecto viento.
- **LOD:** Simplificar árboles lejanos (reducir maxDepth según distancia).

## Referencias

- ez-tree: https://github.com/dgreenheck/ez-tree (demo: https://ez-tree.dgreenheck.com)
- L-systems: https://en.wikipedia.org/wiki/L-system
- Three.js InstancedMesh: https://threejs.org/docs/#api/en/objects/InstancedMesh

---

**Hecho con ❤️ por David Antizar**
