---
name: ecctrl
description: Epic Controls for Three.js — sistema de controles FPS/TPS para Three.js con movimiento, cámara y físicas.
version: "1.0.0"
tags: [three.js, controls, FPS, TPS, game, movement, camera]
---

# ECCTRL — Epic Controls for Three.js

## Resumen

Sistema de controles FPS/TPS para Three.js con movimiento, cámara y físicas. 741⭐.

## Repo de referencia

- **GitHub:** `github.com/pmndrs/ecctrl`
- **Lenguaje:** TypeScript
- **Licencia:** MIT
- **Ecosistema:** pmndrs (React Three Fiber)

## Instalación

```bash
npm install @ecctrl/core
# o
yarn add @ecctrl/core
```

## Uso Básico

```javascript
import { EcctrlControls } from '@ecctrl/core';

// Crear controles
const controls = new EcctrlControls(camera, domElement);

// Configuración
controls.set({
  speed: 5,
  jumpForce: 8,
  friction: 0.8,
  camera: {
    mode: 'fps',  // 'fps' | 'tps'
    distance: 5,
    minPolarAngle: 0,
    maxPolarAngle: Math.PI,
  }
});

// Loop de animación
function animate() {
  controls.update(delta);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

## Patrones Clave

1. **FPS mode:** Cámara en primera persona con WASD + ratón
2. **TPS mode:** Cámara en tercera persona con seguimiento
3. **Físicas:** Gravedad, saltos, fricción, colisiones
4. **Rigging:** Integración con modelos 3D animados
5. **State machine:** Transiciones entre caminar, correr, saltar

## Integración con Mastermind

- Complementa `three.js` para experiencias interactivas 3D
- Ideal para visores de mapas en 3D estilo "exploración"
- Útil para `threejs-3d-maps` con navegación peatonal
- Reemplaza controles manuales de cámara

## Pitfalls

- **React:** Diseñado para React Three Fiber, uso vanilla requiere adaptación
- **Dependencias:** Requiere Three.js y React
- **Documentación:** Docs limitados, hay que leer el código fuente
- **Performance:** Puede ser pesado en móviles

## Referencias

- [GitHub: pmndrs/ecctrl](https://github.com/pmndrs/ecctrl)
