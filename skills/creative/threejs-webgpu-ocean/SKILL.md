---
name: threejs-webgpu-ocean
version: "1.0.0"
description: "Simulación de océano FFT en tiempo real GPU-driven con three.js + WebGPU/TSL. Inspirado en owenyuwono/poseidon (⭐56). Olas realistas con FFT spectrum, normal mapping y foam."
tags: [threejs, webgpu, ocean, fft, shader, simulation, water]
---

# Océano WebGPU con Three.js

## Resumen

Simulación de superficie de océano en tiempo real usando FFT (Fast Fourier Transform) en GPU con WebGPU/TSL. Genera olas realistas con spectrum de Phillips, normal mapping y foam.

## Cuándo usar

- Escena 3D con agua/oceáno realista
- Simulación marítima con olas dinámicas
- Visualización de costa con mareas
- Visor 3D con entorno marino

## Patrón de uso

```javascript
import * as THREE from 'three';
import * as TSL from 'three/tsl';

// Configuración WebGPU
const renderer = new THREE.WebGPURenderer({ antialias: true });
await renderer.init();

// Geometry del océano (plano subdividido)
const oceanGeom = new THREE.PlaneGeometry(1000, 1000, 256, 256);
oceanGeom.rotateX(-Math.PI / 2);

// Shader TSL para FFT ocean
const time = TSL.uniform(0);
const windDirection = TSL.uniform(new THREE.Vector2(1, 1));
const windSpeed = TSL.uniform(30);

// Height displacement basado en FFT spectrum
const displacement = TSL.Fn(([uv]) => {
  const k = TSL.vec2(uv.mul(2).sub(1)); // wave vector
  const kMag = k.length();
  const Phillips = k.normalize().dot(windDirection).pow(2)
    .div(kMag.pow(4).add(0.001))
    .mul(TSL.exp(kMag.pow(2).mul(windSpeed.pow(2)).neg()));
  return TSL.sqrt(Phillips).mul(TSL.cos(k.dot(time)));
});

const oceanMaterial = new THREE.MeshStandardNodeMaterial({
  color: 0x006994,
  metalness: 0.9,
  roughness: 0.2,
});

// Vertex displacement
oceanMaterial.positionNode = TSL.vertexPosition
  .add(TSL.vec3(0, displacement(TSL.uv()), 0));

// Normal calculation
oceanMaterial.normalNode = TSL.normalize(TSL.vec3(
  displacement(TSL.uv().sub(TSL.vec2(0.01, 0))).sub(displacement(TSL.uv())),
  1.0,
  displacement(TSL.uv().sub(TSL.vec2(0, 0.01))).sub(displacement(TSL.uv()))
));

const ocean = new THREE.Mesh(oceanGeom, oceanMaterial);
scene.add(ocean);

// Animation loop
renderer.setAnimationLoop(() => {
  time.value += 0.016;
  renderer.render(scene, camera);
});
```

## Pitfalls

- **WebGPU support:** Solo Chrome/Edge 113+ y Safari 18+. Fallback a WebGL con vertex shader FFT.
- **FFT size:** 256x256 es bueno para real-time. 512x512 = más calidad pero más costoso.
- **Tiling:** El océano FFT se repite. Usar múltiples spectrums con diferentes direcciones de viento para variación.
- **Foam:** Añadir foam donde la altura supera un threshold. Usar textura de ruido.
- **Underwater:** Para vista submarina, invertir normals y ajustar color de agua.

## Referencias

- poseidon: https://github.com/owenyuwono/poseidon
- Three.js WebGPU: https://threejs.org/docs/#api/en/renderers/WebGPURenderer
- TSL (Three Shading Language): https://threejs.org/docs/#api/en/tsl
- FFT Ocean shader: https://developer.download.nvidia.com/assets/gamedev/files/siggraph2005/OceanSimulation.pdf

---

**Hecho con ❤️ por David Antizar**
