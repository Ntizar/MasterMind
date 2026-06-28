---
name: threejs-3d-web
description: "Crear escenas 3D interactivas en el navegador con Three.js o Canvas 2D puro — gemelos digitales, visualizaciones, partículas. Autocontenido sin build step. Incluye patrón mármol procedural."
version: "3.0.0"
author: David Antizar
tags: [threejs, webgl, 3d, browser, visualization, interactive, gemelo-digital, canvas2d]
---

# Three.js / Canvas 2D — 3D en el Navegador

Crear escenas 3D interactivas en el navegador. Three.js vía CDN O Canvas 2D puro como fallback universal.

## Cuándo cargar esta skill

Cuando el usuario pida: escena 3D, visualización 3D, modelo 3D, WebGL, gemelo digital, simulación 3D, renderizado 3D, partículas, animación 3D, sistema solar, visualización de datos espaciales, etc.

## ⚠️ CRÍTICO: Entorno de ejecución

**Si el entorno NO ejecuta scripts externos** (Hermes browser tool, sandbox sin red, entorno restringido):
→ **Usar Canvas 2D puro** en vez de Three.js. Ver `references/canvas2d-fallback.md` para el patrón completo.
- Canvas 2D funciona en TODOS los entornos, carga instantáneamente, cero dependencias
- Para visualizaciones tipo sistema solar, datos espaciales, gráficos interactivos: Canvas 2D es suficiente y superior en compatibilidad
- Three.js solo si el usuario insiste en WebGL real Y el entorno lo permite

**Si el entorno SÍ permite scripts externos:**
→ Usar Three.js vía importmap CDN. Ver patrón base abajo.

**Si el entorno NO permite scripts externos PERO se necesita WebGL real:**
→ Usar mini WebGL engine desde cero. Ver `references/mini-webgl-engine.md` para el patrón completo.
- ~33KB autocontenido con shaders custom (Phong, rim light, emisividad)
- Esferas 3D reales con iluminación direccional
- Anillos texturizados, estrellas con point sprites
- Cámara esférica con interpolación suave
- Ideal para gemelos digitales, visualizaciones espaciales, simulaciones

## Patrón Canvas 2D (fallback universal)

```javascript
// Patrón: todo autocontenido, sin dependencias externas
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

function render(time) {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // Dibujar aquí...
    requestAnimationFrame(render);
}
requestAnimationFrame(render);
```

**Ventajas Canvas 2D:**
- Cero dependencias, archivo autocontenido
- Funciona en cualquier entorno (Hermes, sandbox, sin red)
- Carga instantánea (30KB vs 600KB+ de Three.js)
- Suficiente para visualizaciones 2D/2.5D (órbitas, gráficos, mapas)
- Simular 3D con gradientes radiales (`ctx.createRadialGradient`)

**Cuándo usar Three.js real:**
- El usuario necesita WebGL real (sombras, iluminación física, shaders)
- El entorno permite cargar scripts externos
- Se aceptan los ~600KB de Three.js

## Patrón base (Three.js vía CDN)

```html
<script type="importmap">
{
    "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.163.0/build/three.module.js",
        "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.163.0/examples/jsm/"
    }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// 1. Scene + Camera + Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.001, 10000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

// 2. Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// 3. Lights
scene.add(new THREE.AmbientLight(0x404040));
const dirLight = new THREE.DirectionalLight(0xffffff, 2);
dirLight.position.set(5, 10, 5);
scene.add(dirLight);

// 4. Objects — MeshStandardMaterial para reacción a luz
const geo = new THREE.SphereGeometry(1, 32, 32);
const mat = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geo, mat);
scene.add(mesh);

// 5. Animation loop
function animate() {
    requestAnimationFrame(animate);
    mesh.rotation.y += 0.01;
    controls.update();
    renderer.render(scene, camera);
}
animate();

// 6. Resize handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
```

## Capas de complejidad (de simple a avanzado)

### Nivel 1 — Canvas 2D básico
Rectángulos, círculos, líneas, texto. Ideal para dashboards, gráficos, visualizaciones de datos.

### Nivel 2 — Canvas 2D con simulación 3D
Gradientes radiales para esferas, perspectiva forzada, sombras simuladas. Suficiente para gemelos digitales 2.5D.

### Nivel 2.5 — Mini WebGL engine desde cero
WebGL puro con shaders custom (~33KB). Esferas reales con iluminación Phong, rim light, emisividad. Sin dependencias externas. Ver `references/mini-webgl-engine.md`.

### Nivel 3 — Three.js básico
Scene, camera, renderer, geometría básica, materiales estándar.

### Nivel 4 — Texturas procedurales
Crear texturas con Canvas 2D → `THREE.CanvasTexture`. Planetas con continentes, bandas de Júpiter, superficies detalladas.
- Ver `references/marmol-procedural-threejs.md` para patrón de mármol griego (venas + flecks dorados)

### Nivel 5 — Iluminación avanzada
`PointLight`, `DirectionalLight`, `AmbientLight`, `SpotLight`.

### Nivel 6 — Shaders custom
`ShaderMaterial` para glow, bloom, atmospheric scattering.

### Nivel 7 — Post-procesado
`EffectComposer` + `UnrealBloomPass` / `SSAOPass`.

### Nivel 8 — Modelos externos
Cargar GLTF/GLB con `GLTFLoader`.

### Nivel 9 — Partículas y efectos
`Points` con `BufferGeometry` para campos estelares, lluvia, fuego.

### Nivel 10 — Datos en 3D
Visualizar datos reales: órbitas keplerianas, datos geográficos, redes.

## Componentes reutilizables

### Campo estelar (Canvas 2D)
```javascript
function drawStars(ctx, w, h, count, cameraOffset) {
    for (let i = 0; i < count; i++) {
        const seed = i * 7919; // prime for distribution
        const x = ((seed * 13) % 4000) - 2000 - (cameraOffset.x * 0.05);
        const y = ((seed * 17) % 4000) - 2000 - (cameraOffset.y * 0.05);
        const sx = (x + w/2) + w/2;
        const sy = (y + h/2) + h/2;
        if (sx < 0 || sx > w || sy < 0 || sy > h) continue;
        const brightness = 0.3 + 0.4 * Math.sin(Date.now() / 1000 + i);
        ctx.fillStyle = `rgba(255,255,255,${Math.max(0, Math.min(1, brightness))})`;
        ctx.beginPath();
        ctx.arc(sx, sy, 0.5 + Math.random() * 1, 0, Math.PI * 2);
        ctx.fill();
    }
}
```

### Esfera 3D simulada (Canvas 2D)
```javascript
function drawSphere3D(ctx, cx, cy, radius, baseColor, lightOffset) {
    const grad = ctx.createRadialGradient(
        cx + radius * (lightOffset || -0.3),
        cy + radius * (lightOffset || -0.3),
        radius * 0.1,
        cx, cy, radius
    );
    const c = parseInt(baseColor.slice(1), 16);
    const r = Math.min(255, ((c >> 16) & 0xff) + 40);
    const g = Math.min(255, ((c >> 8) & 0xff) + 40);
    const b = Math.min(255, (c & 0xff) + 40);
    grad.addColorStop(0, `rgb(${r},${g},${b})`);
    grad.addColorStop(0.7, baseColor);
    const dr = Math.max(0, ((c >> 16) & 0xff) - 60);
    const dg = Math.max(0, ((c >> 8) & 0xff) - 60);
    const db = Math.max(0, (c & 0xff) - 60);
    grad.addColorStop(1, `rgb(${dr},${dg},${db})`);
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.fill();
}
```

### Órbita elíptica (Canvas 2D)
```javascript
function drawOrbit(ctx, cx, cy, semiMajorAxis, eccentricity, inclination, scale, color) {
    const a = semiMajorAxis * scale;
    const b = a * Math.sqrt(1 - eccentricity * eccentricity);
    const inc = inclination * Math.PI / 180;
    ctx.strokeStyle = color || 'rgba(255,255,255,0.12)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let i = 0; i <= 256; i++) {
        const theta = (i / 256) * Math.PI * 2;
        const r = semiMajorAxis * (1 - eccentricity**2) / (1 + eccentricity * Math.cos(theta));
        const x = r * Math.cos(theta) * scale;
        const z = r * Math.sin(theta) * scale;
        const y = z * Math.sin(inc);
        if (i === 0) ctx.moveTo(cx + x, cy + y);
        else ctx.lineTo(cx + x, cy + y);
    }
    ctx.closePath();
    ctx.stroke();
}
```

### Ecuación de Kepler (posiciones reales)
```javascript
function solveKepler(M, e, tol) {
    if (tol === undefined) tol = 1e-10;
    let E = M;
    for (let i = 0; i < 50; i++) {
        const dE = (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
        E -= dE;
        if (Math.abs(dE) < tol) break;
    }
    return E;
}

function getKeplerPosition(semiMajorAxis, eccentricity, period, M0, date) {
    const JD = date.getTime() / 86400000 + 2440587.5;
    const J2000 = 2451545.0;
    const n = (2 * Math.PI) / period;
    const M = (M0 + n * (JD - J2000)) % (2 * Math.PI);
    const E = solveKepler(M, eccentricity);
    const nu = 2 * Math.atan2(
        Math.sqrt(1 + eccentricity) * Math.sin(E / 2),
        Math.sqrt(1 - eccentricity) * Math.cos(E / 2)
    );
    const r = semiMajorAxis * (1 - eccentricity * Math.cos(E));
    return { x: r * Math.cos(nu), z: r * Math.sin(nu) };
}
```

## Pitfalls

- **⚠️ ENTORNO HERMES:** El browser tool de Hermes NO ejecuta scripts externos (`<script src>`, importmap, ES modules). **Siempre usar Canvas 2D puro** como primer enfoque. Three.js solo si el entorno lo permite explícitamente.
- **Scripts inline grandes (600KB+):** El browser de Hermes puede timeout al ejecutar scripts inline enormes. Three.js embebido NO funciona en el browser de Hermes — usar mini WebGL engine (~33KB) o Canvas 2D.
- **Unpkg 404 en examples/js/:** Three.js 0.160.1 eliminó la carpeta `examples/js/` legacy. Solo existe `examples/jsm/` (ES modules). La ruta `examples/js/controls/OrbitControls.js` devuelve 404.
- **Renderer sin `setPixelRatio`** → puede ser demasiado pesado en pantallas retina. Limitar a `Math.min(devicePixelRatio, 2)`.
- **MeshBasicMaterial + luz** → `MeshBasicMaterial` NO reacciona a luces. Usar `MeshStandardMaterial` para objetos que necesiten iluminación.
- **OrbitControls damping** → si no se llama `controls.update()` en el loop, el damping no funciona. Durante animación de cámara, desactivar temporalmente `controls.enableDamping = false`.
- **Textura Canvas no se repite** → `texture.wrapS = THREE.RepeatWrapping` para que se repita en U.
- **Importmap CDN** → usar jsdelivr con versión concreta (`@0.163.0`), NUNCA `@latest` en producción.
- **Tamaño de escena** → Three.js no escala por defecto. Los planetas reales son demasiado pequeños relativos a las distancias. Usar escala arbitraria pero proporcional.
- **Raycaster con objetos anidados** → si un planeta tiene hijos (anillos), el raycast puede hitting el hijo. Verificar `object.parent` o usar `recursive: true`.
- **`MeshPhysicalMaterial` vs versión Three.js** → propiedades como `thickness`, `transmission`, `ior` solo existen desde Three.js r136+. En r128 (cdnjs por defecto) dan warning silencioso y se ignoran. **Usar importmap con `@0.163.0`** o eliminar esas propiedades si se usa r128. Patrón seguro: `MeshStandardMaterial` + `clearcoat` si se necesita transparencia parcial.
- **GitHub Pages cache** → añadir `?nocache=N` a la URL para forzar refresh.
- **Replace-all en patch** → NUNCA usar `replace_all=true` para cambios en Three.js — cadenas genéricas aparecen en múltiples contextos.

## 3. ExportPanel — Captura PNG + Compartir URL

**2026-06-18 (WaveThree Fase 5):** Patrón para capturar escena Three.js como PNG con watermark y compartir URL con estado.

### ExportPanel API

```javascript
const exportPanel = new ExportPanel({ renderer, getState, scenarioMeta, baseURL });
exportPanel.mount();           // Montar en el DOM
exportPanel.updateScenarioMeta(meta);
exportPanel.unmount();
```

**Pitfalls:**
- **Llamar `renderer.render()` antes de `toDataURL()`** — el canvas no tiene el frame actual
- **Watermark dibujado en canvas** — no usar overlay DOM, dibujar directamente en canvas exportado
- **navigator.clipboard puede fallar** — tener fallback con `document.execCommand('copy')`

### Comparador de Escenas

**2026-06-18 (WaveThree Fase 5):** Comparar dos escenarios lado a lado con modos split, crossfade y toggle.

```javascript
const comparador = new Comparador({ scene, camera, renderer, controls, selectScenario });
comparador.enable();
comparador.selectA('scenario_a');
comparador.selectB('scenario_b');
comparador.setMode('split');   // 'split' | 'crossfade' | 'toggle'
comparador.render(time);       // En el animation loop
comparador.dispose();
```

**Pitfalls:**
- **WebGLRenderTarget debe tener mismo tamaño que canvas** — crear con `renderer.domElement.width/height`
- **Llamar `comparador.render(time)` en el animation loop** — es el único modo que actualiza visualización
- **No compartir geometría entre escenas clonadas** — cada escena clonada necesita materiales independientes

### Atajos de teclado para visores 3D

**2026-06-18 (WaveThree Fase 5):** Atajos de teclado en visores 3D interactivos.

```javascript
document.addEventListener('keydown', (e) => {
  const tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
  // e.key === 'r' → reset cámara
  // e.key === 'e' → exportar
  // e.key === '1'-'9' → seleccionar escenario
});
```

**Pitfalls:**
- **Siempre verificar `e.target.tagName`** — los atajos se disparan al escribir en inputs/sliders
- **Event listener global** — no vincular a elementos específicos

## Integración con UI

- Canvas ocupa `position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0`
- UI overlay con `z-index: 10` y `pointer-events: none` en el contenedor, `pointer-events: auto` en los elementos
- Glassmorphism con `backdrop-filter: blur(20px)` y bordes semitransparentes

## Deploy

Ver skill `github-workflow` → sección 7.1b (branch gh-pages) para deploy ultra-rápido de HTML autocontenido.

## Referencias

- `references/sistema-solar.md` — Patrón de gemelo digital del sistema solar con efemérides keplerianas
- `references/canvas2d-fallback.md` — Patrón Canvas 2D puro como alternativa a Three.js
- `references/mini-webgl-engine.md` — Mini motor WebGL desde cero para entornos sin scripts externos
- `references/threejs-export-scene-comparator.md` — ExportPanel (captura PNG con watermark + compartir URL), Comparador (split/crossfade/toggle), atajos de teclado para visores 3D
- `references/canvas2d-particle-background.md` — Fondo de partículas Canvas2D (documentos flotantes con repulsión mouse). Para landing pages, dashboards, herramientas.

## 2. Sistemas de Partículas (absorbido de `threejs-particle-systems`)

### Pool Reciclado de Partículas
Cada sistema usa `THREE.Points` con buffer pools reciclados y `ShaderMaterial` custom. Patrón: `MAX_PARTICLES` → `findDeadParticle()` → `emit()` → `update(dt)` con fade-out.

### Tipos de partículas
- **Espuma (Foam):** 0.2-0.8 size, blanco puro, vida 1-5s, gravedad mínima, additive blending
- **Spray (Salpicadura):** 0.05-0.2 size, blanco azulado, vida 0.5-1.5s, gravedad fuerte, additive blending
- **Humo:** 0.5-2.0 size, gris oscuro, vida 3-8s, flota, normal blending

### Pitfalls de partículas
- `depthWrite: false` siempre en partículas transparentes
- `frustumCulled = false` para sistemas de partículas
- `discard` en fragment shader para círculos suaves (evitar cuadrados)
- `geometry.attributes.position.needsUpdate = true` en cada frame

## 3. Three.js Audit Checklist (absorbido de `threejs-audit-checklist`)

### Memory Leaks
- `geometry.dispose()`, `material.dispose()`, `texture.dispose()` al cambiar escena
- `renderer.dispose()` al destruir
- Cada `addEventListener` → `removeEventListener` en cleanup
- `requestAnimationFrame` ID → `cancelAnimationFrame`
- `scene.remove(obj)` + `obj.traverse(child => child.dispose?.())`

### Event Listener Cleanup Pattern
```js
// ❌ MALO — arrow function inline
document.addEventListener('click', (e) => { ... });
// ✅ BUENO — guardar referencia
this._handler = (e) => { ... };
document.addEventListener('click', this._handler);
document.removeEventListener('click', this._handler); // en cleanup
```

### Float32Array Shared Views
```js
// ❌ MALO — vista compartida, corrupción
prev = new Float32Array(current);
// ✅ BUENO — copia explícita
prev = new Float32Array(current.length);
prev.set(current);
```

## 4. Visualizaciones 3D — Madrid, InBody, Ciudades

### Madrid Visualization
Visualización de la ciudad de Madrid con isometric pixel art (Madrid3Pixel), mapas 3D WebGL (NapMaps), y renderizadores procedurales. Incluye guías de decisión: Canvas 2D vs MapLibre GL JS vs Three.js.

### Render 3D Isométrico de Ciudades
Render 3D isométrico de ciudades en Canvas 2D — edificios con 3 caras (frontal/lateral/tejado), depth sorting, ciclo día/noche, clima y datos de coordenadas reales.

### InBody 3D Visualization
Visualización 3D del cuerpo humano con Three.js basada en datos reales de composición corporal. Modelo procedural con segmentos escalables por grasa y músculo.