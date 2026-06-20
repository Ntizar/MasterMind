---
name: threejs-audit-checklist
version: "1.0.0"
description: Procedimiento sistemático para auditar aplicaciones Three.js — memory leaks, disposal, event listeners, renderizado, composición de shaders
---

# Three.js WebGL App Audit Checklist

Procedimiento sistemático para auditar aplicaciones Three.js en producción, detectar bugs, memory leaks y problemas de rendimiento.

## 1. Revisión de Código General

- [ ] **Variables globales** — buscar `var`, asignaciones sin declaración, `window.xxx`
- [ ] **Console errors/warnings** — `console.error`, `console.warn` sin manejo
- [ ] **Imports rotos** — referencias a módulos inexistentes
- [ ] **Código duplicado** — lógica repetida en múltiples archivos
- [ ] **Nombres inconsistentes** — mezclas camelCase/snake_case, nombres ambigüos

## 2. Memory Leaks (Crítico en Three.js)

### Geometrías y Materiales
- [ ] Al cambiar de escena/escenario: `geometry.dispose()`, `material.dispose()`
- [ ] Al destruir el renderer: `renderer.dispose()`
- [ ] Texturas: `texture.dispose()` al cambiar textura
- [ ] RenderTargets: `rt.dispose()` al destruir comparador/efectos

### Event Listeners
- [ ] **Cada `addEventListener` debe tener su `removeEventListener`** en cleanup/unmount/dispose
- [ ] Listeners en `document` son los más peligrosos (nunca se limpian con el componente)
- [ ] Handlers inline (arrow functions) NO se pueden remover — guardar referencia en `this._handler`
- [ ] Patrones comunes de leak:
  - `document.addEventListener('click', (e) => { ... })` sin cleanup
  - `window.addEventListener('resize', ...)` en SPAs multi-montaje
  - Event listeners en UI temporales (modals, overlays) que no se limpian al cerrar

### Animaciones y Loops
- [ ] `requestAnimationFrame` — guardar ID y cancelar en cleanup
- [ ] `setInterval` / `setTimeout` — guardar ID y limpiar
- [ ] Animaciones CSS con `animationend` listeners que no se remueven

### Three.js Objects
- [ ] Al remover de escena: `scene.remove(obj)` + `obj.traverse(child => child.dispose?.())`
- [ ] Grupos: `group.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); })`
- [ ] Meshes creados dinámicamente (shaders temporales, planos de composición)

## 3. Three.js Específico

### Renderer
- [ ] `setPixelRatio` se actualiza en resize
- [ ] `preserveDrawingBuffer: true` solo si se necesita (saca screenshot, export PNG)
- [ ] Shadow map size razonable (2048 es alto para móvil)

### Scenarios/Modos
- [ ] Al cambiar de modo (Gerstner ↔ Espectral): dispose del océano anterior
- [ ] Al cargar nuevo escenario: dispose del anterior
- [ ] Render targets del comparador: dispose al desactivar

### Shaders
- [ ] `ShaderMaterial` temporales: dispose al destruir
- [ ] `PlaneGeometry` temporales: dispose al destruir
- [ ] Verificar que fragment shader use ambas texturas cuando hay composición

## 4. Renderizado

- [ ] **Split view**: ambos lados renderizados en sus render targets antes de composición
- [ ] **Crossfade**: interpolación visual funciona, no solo slider
- [ ] **Export PNG**: leer canvas actual, NO llamar renderer.render() de nuevo (doble render)
- [ ] Océano visible con batimetría correcta
- [ ] Espuma/spray se actualizan independientemente de visibilidad de estructuras

## 5. UI

- [ ] Sliders actualizan escena en tiempo real (input event, no change)
- [ ] Selector de escenarios funciona y carga datos
- [ ] FPS counter se muestra correctamente
- [ ] Diseño responsive (resize actualiza cámara y renderer)
- [ ] Keyboard shortcuts no interfieren con inputs

## 6. Pitfalls Específicos

### Float32Array Shared Views
```js
// ❌ MALO — vista compartida, corrupción de datos
prev = new Float32Array(current);

// ✅ BUENO — copia explícita
prev = new Float32Array(current.length);
prev.set(current);
```

### Division by Zero
```js
// ❌ MALO
Tp = 1 / frequency;  // Infinity si frequency === 0

// ✅ BUENO
if (frequency > 0) Tp = 1 / frequency;
```

### Shader Composition
```glsl
// ❌ MALO — solo muestra textureA
gl_FragColor = texture2D(textureA, uv);

// ✅ BUENO — composición split correcta
vec4 color = uv.x < splitPos ? texture2D(textureA, uv) : texture2D(textureB, uv);
gl_FragColor = color;
```

### Double Render
```js
// ❌ MALO — el loop principal ya renderiza
renderer.render(scene, camera);  // en export PNG → doble render

// ✅ BUENO — solo leer canvas
const canvas = renderer.domElement;
```

### Event Listener Cleanup Pattern
```js
// ❌ MALO — arrow function inline, no se puede remover
document.addEventListener('click', (e) => { ... });

// ✅ BUENO — guardar referencia
this._handler = (e) => { ... };
document.addEventListener('click', this._handler);
// Luego en cleanup:
document.removeEventListener('click', this._handler);
```

## 7. Verificación Post-Auditoría

- [ ] `npm run build` pasa sin errores
- [ ] No hay console.error en DevTools
- [ ] Memory usage estable tras 5 minutos de uso
- [ ] No hay leaks en Chrome DevTools → Memory → Heap snapshot
- [ ] FPS estable en modo Gerstner (>55) y Espectral (>25)
