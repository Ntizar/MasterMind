# Three.js — Espuma y Spray de Olas (WaveThree)

Implementación de sistemas de partículas para simular espuma de impacto y salpicadura de olas en un visor oceánico 3D.

## Contexto

Proyecto WaveThree — visor oceánico 3D con ondas Gerstner/espectrales, batimetría 3D y escenarios. Fase 4 añadió estructuras costeras (dique, muelle) con efectos de espuma y spray.

## Implementación Real

### `src/structures/foam.js` — Sistema de Espuma

**Arquitectura:**
- Pool de 4000 partículas recicladas
- BufferGeometry con atributos: position, color, size, alpha
- ShaderMaterial custom con vertex shader (tamaño basado en distancia) y fragment shader (círculo suave con edge fade)
- Emisión basada en altura de ola: `emitCount = floor(2 + waveHeight * 8)`

**Parámetros de espuma:**
- Tamaño: 0.2-0.8 (variable)
- Color: Blanco puro (1,1,1)
- Vida: 1-5 segundos
- Velocidad: Baja hacia arriba y lados
- Gravedad: Mínima (0.1)
- Fricción: Alta (0.97-0.98)
- Alpha máximo: 0.7
- Blending: Additive

### `src/structures/splash.js` — Sistema de Spray

**Arquitectura:**
- Pool de 2000 partículas recicladas
- Partículas más pequeñas y más rápidas que la espuma
- Efecto de explosión radial cuando la ola impacta

**Parámetros de spray:**
- Tamaño: 0.05-0.2 (pequeño)
- Color: Blanco azulado (0.85, 0.9, 0.95)
- Vida: 0.5-1.5 segundos (corta)
- Velocidad: Alta explosiva radial
- Gravedad: Fuerte (2.0)
- Fricción: Media (0.94-0.95)
- Alpha máximo: 0.5
- Blending: Additive

### `src/structures/index.js` — Estructuras Costeras

**`createBreakwater(params)`:**
- Perfil trapezoidal con escollera
- Geometría: `BufferGeometry` con vértices calculados para forma trapezoidal
- Material: `MeshStandardMaterial` con color roca y roughness alto
- Posicionamiento relativo a la escena

**`createSimpleCoastline(points)`:**
- Línea de costa como serie de puntos 3D
- Color arena/verde
- Geometría de `BufferGeometry` con `setFromPoints()`

**`createPier()`:**
- Muelle/espigón simple con cajas
- Geometría de `BoxGeometry` para plataforma
- Pilares con cilindros

### Integración en `main.js`

```javascript
// Crear sistema de espuma y spray
const foamSystem = createFoamSystem(scene);
const splashSystem = createSplashSystem(scene);

// Crear dique de demostración
const breakwater = createBreakwater({
  position: { x: -20, y: 0, z: 0 },
  length: 30,
  width: 5,
  height: 3
});
scene.add(breakwater);

// En el animation loop
function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  const dt = clock.getDelta();

  ocean.update(t);
  foamSystem.update(dt, waveHeight, breakwater.position);
  splashSystem.update(dt, waveHeight, breakwater.position);

  renderer.render(scene, camera);
}
```

### Escenario `port_scene.json`

```json
{
  "id": "port_scene",
  "label": "Puerto con dique",
  "location": "Cantábrico",
  "time": "2026-04-20T10:00:00Z",
  "wave": { "hs": 2.5, "tp": 10.0, "dir": 290 },
  "wind": { "speed": 12.0, "dir": 280 },
  "structure": "breakwater"
}
```

## Lecciones Aprendidas

1. **Pool reciclado > crear/destruir:** Para 4000+ partículas, reciclar es obligatorio. Crear/destruir cada frame causa GC spikes y stuttering.
2. **Shader custom para partículas:** `PointsMaterial` no permite tamaño individual ni alpha individual. ShaderMaterial con attributes es la solución.
3. **`discard` en fragment shader:** Para partículas circulares, `discard` es mejor que alpha 0 — evita cuadrados visibles en las esquinas del punto.
4. **`depthWrite: false`** para partículas transparentes — sin esto, depth sorting se rompe y las partículas se renderizan mal.
5. **`frustumCulled = false`** para sistemas de partículas — las partículas pueden desaparecer al mover la cámara si están cerca del borde del frustum.
6. **Vite build como verificación:** `npx vite build` es la forma de verificar que todo compila sin errores. Si el build pasa, el deploy en NaN funciona.
7. **Añadir escenario requiere actualizar loader:** El nuevo escenario `port_scene` debe añadirse a la lista `knownScenarios` en `src/loaders/index.js` además de crear el archivo JSON.
