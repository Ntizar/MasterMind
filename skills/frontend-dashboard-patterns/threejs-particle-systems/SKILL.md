---
name: threejs-particle-systems
description: "Sistemas de partículas con Three.js — emitters con pool reciclado, shaders custom, partículas con vida limitada, espuma, spray, humo, fuego. Patrón de arquitectura reutilizable."
version: "1.0.0"
author: Hermes Agent
tags: [threejs, particles, shaders, foam, spray, particle-system, gpu, points]
---

# Three.js — Sistemas de Partículas con Shaders Custom

Patrones para crear sistemas de partículas con Three.js usando `THREE.Points`, buffer pools reciclados, y shaders GLSL custom. Basado en WaveThree (espuma de impacto, spray de olas).

## Arquitectura Base

Cada sistema de partículas sigue este patrón:

```
1. BufferGeometry con atributos: position, color, size, alpha
2. ShaderMaterial custom (vertex + fragment)
3. Pool de partículas recicladas (dead/alive states)
4. Función update(dt, params) que mueve, fade-out y re-emite
```

## Patrón 1: Pool Reciclado de Partículas

En vez de crear/destruir partículas cada frame, usar un pool fijo con estados:

```javascript
const MAX_PARTICLES = 4000;
const positions = new Float32Array(MAX_PARTICLES * 3);
const colors = new Float32Array(MAX_PARTICLES * 4); // RGBA
const sizes = new Float32Array(MAX_PARTICLES);
const alphas = new Float32Array(MAX_PARTICLES);
const lifetimes = new Float32Array(MAX_PARTICLES);
const velocities = new Float32Array(MAX_PARTICLES * 3);
const states = new Uint8Array(MAX_PARTICLES); // 0=dead, 1=alive

function findDeadParticle() {
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (states[i] === 0) return i;
  }
  // Pool lleno: reciclar la más vieja
  let oldest = 0;
  for (let i = 1; i < MAX_PARTICLES; i++) {
    if (lifetimes[i] < lifetimes[oldest]) oldest = i;
  }
  return oldest;
}

function emit(x, y, z, intensity) {
  const idx = findDeadParticle();
  positions[idx*3] = x + (Math.random()-0.5)*0.5;
  positions[idx*3+1] = y + Math.random()*0.3;
  positions[idx*3+2] = z + (Math.random()-0.5)*0.5;
  velocities[idx*3] = (Math.random()-0.5)*2;
  velocities[idx*3+1] = 0.5 + Math.random()*1.5*intensity;
  velocities[idx*3+2] = (Math.random()-0.5)*2;
  lifetimes[idx] = 1.0 + Math.random()*2.0*intensity;
  colors[idx*4] = 1.0; colors[idx*4+1] = 1.0; colors[idx*4+2] = 1.0; colors[idx*4+3] = 1.0;
  sizes[idx] = 0.4 * (0.5 + Math.random()*1.5) * (0.5 + intensity);
  states[idx] = 1;
}
```

## Patrón 2: Shader de Partículas Circulares

Para partículas redondas con bordes suaves (espuma, spray, humo):

```javascript
// Vertex shader — tamaño basado en distancia a cámara
const vertexShader = `
  attribute float size;
  attribute float alpha;
  attribute vec4 color;
  uniform float uPixelRatio;
  varying float vAlpha;
  varying vec4 vColor;
  void main() {
    vAlpha = alpha;
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * uPixelRatio * (200.0 / -mvPosition.z);
    gl_PointSize = max(gl_PointSize, 1.0);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

// Fragment shader — círculo suave con edge fade
const fragmentShader = `
  varying float vAlpha;
  varying vec4 vColor;
  void main() {
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);
    if (dist > 0.5) discard;
    float edge = 1.0 - smoothstep(0.2, 0.5, dist);
    float brightness = 0.85 + 0.15 * (1.0 - dist * 2.0);
    gl_FragColor = vec4(vColor.rgb * brightness, vAlpha * edge);
  }
`;
```

## Patrón 3: Update Loop con Fade-Out

```javascript
function update(dt, waveHeight, structurePos) {
  if (dt > 0.1) dt = 0.1;

  // Emitir nuevas partículas basado en parámetro
  let emitCount = Math.floor(2 + waveHeight * 8);
  for (let i = 0; i < emitCount; i++) {
    let ex, ey, ez;
    if (structurePos) {
      ex = structurePos.x + (Math.random()-0.5)*3;
      ey = Math.max(0, waveHeight*0.3);
      ez = structurePos.z + (Math.random()-0.5)*2;
    } else {
      ex = (Math.random()-0.5)*60;
      ey = Math.max(0, waveHeight*0.2);
      ez = (Math.random()-0.5)*60;
    }
    emit(ex, ey, ez, Math.min(waveHeight/4.0, 1.0));
  }

  // Actualizar partículas existentes
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (states[i] !== 1) continue;
    lifetimes[i] -= dt;
    if (lifetimes[i] <= 0) {
      states[i] = 0; sizes[i] = 0; alphas[i] = 0; continue;
    }
    // Mover
    positions[i*3]   += velocities[i*3]   * dt;
    positions[i*3+1] += velocities[i*3+1] * dt;
    positions[i*3+2] += velocities[i*3+2] * dt;
    // Fricción
    velocities[i*3]   *= 0.98;
    velocities[i*3+1] *= 0.97;
    velocities[i*3+2] *= 0.98;
    // Gravedad reducida
    velocities[i*3+1] -= 0.1 * dt;
    // Fade out
    alphas[i] = Math.pow(lifetimes[i]/2.0, 0.5) * 0.7;
    sizes[i] *= (1.0 + dt * 0.3); // dispersión
  }

  geometry.attributes.position.needsUpdate = true;
  geometry.attributes.alpha.needsUpdate = true;
  geometry.attributes.size.needsUpdate = true;
}
```

## Tipos de Partículas

### Espuma (Foam)
- **Tamaño:** 0.2-0.8 (variable)
- **Color:** Blanco puro (1,1,1)
- **Vida:** 1-5 segundos (larga)
- **Velocidad:** Baja hacia arriba y lados
- **Gravedad:** Mínima (0.1)
- **Fricción:** Alta (0.97-0.98)
- **Alpha:** 0.7 máximo
- **Blending:** Additive

### Spray (Salpicadura)
- **Tamaño:** 0.05-0.2 (pequeño)
- **Color:** Blanco azulado (0.85, 0.9, 0.95)
- **Vida:** 0.5-1.5 segundos (corta)
- **Velocidad:** Alta explosiva radial
- **Gravedad:** Fuerte (2.0)
- **Fricción:** Media (0.94-0.95)
- **Alpha:** 0.5 máximo
- **Blending:** Additive

### Humo
- **Tamaño:** 0.5-2.0 (grande, crece rápido)
- **Color:** Gris oscuro con transparencia
- **Vida:** 3-8 segundos (muy larga)
- **Velocidad:** Lenta hacia arriba
- **Gravedad:** Negativa (flota)
- **Fricción:** Muy alta (0.99)
- **Alpha:** 0.3 máximo
- **Blending:** Normal (no additive)

## Pitfalls

- **`needsUpdate` en cada frame:** Olvidar poner `geometry.attributes.position.needsUpdate = true` es el error más común. Las partículas se quedan quietas.
- **`depthWrite: false`:** Siempre desactivarlo en partículas transparentes o se renderizan mal con depth sorting.
- **`frustumCulled = false`:** Para sistemas de partículas, desactivar frustum culling o las partículas desaparecerán al mover la cámara.
- **Buffer size fijo:** El `Float32Array` debe tener tamaño fijo (`MAX_PARTICLES * 3`). No usar `push()` en attributes.
- **Additive blending:** Para partículas brillantes (espuma, fuego), usar `AdditiveBlending`. Para partículas oscuras (humo), usar `NormalBlending`.
- **Tamaño de partícula:** `gl_PointSize` se calcula en el vertex shader. Si es 0 o negativo, la partícula no se ve. Siempre `max(gl_PointSize, 1.0)`.
- **`discard` en fragment shader:** Para partículas circulares, usar `if (dist > 0.5) discard` en vez de alpha 0 — evita que las partículas cuadradas se vean como cuadrados.
- **Pixel ratio:** Multiplicar el tamaño por `uPixelRatio` para que las partículas se vean nítidas en pantallas retina.

## Integración con Océano

Para que la espuma se genere donde las olas tocan el agua:

```javascript
// En el animation loop
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  const dt = clock.getDelta();

  // Actualizar océano
  ocean.update(t);

  // Actualizar espuma basada en altura de ola
  const waveHeight = state.params.amplitude || 3.2;
  foamSystem.update(dt, waveHeight, structurePos);
  spraySystem.update(dt, waveHeight, structurePos);

  renderer.render(scene, camera);
}
```

## Referencias

- `references/threejs-particle-foam-spray.md` — Implementación completa de espuma y spray de WaveThree (estructuras costeras, dique, partículas con pool reciclado, shaders custom).
