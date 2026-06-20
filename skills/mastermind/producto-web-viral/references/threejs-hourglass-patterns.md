# Three.js Hourglass Patterns

Patrones reutilizables para escenas 3D con Three.js, extraídos del proyecto ARENA.

## Hourglass con LatheGeometry

En vez de conos (ConeGeometry), usar LatheGeometry para formas suaves:

```javascript
const points = [];
for (let i = 0; i <= 20; i++) {
  const t = i / 20;
  const y = 0.3 + t * 2.5;
  const r = t < 0.1
    ? NECK_RADIUS + t * (BULB_RADIUS - NECK_RADIUS) * 10
    : BULB_RADIUS * Math.sin(t * Math.PI * 0.85) * (1 - t * 0.1);
  points.push(new THREE.Vector2(Math.max(r, 0.05), y));
}
const geo = new THREE.LatheGeometry(points, 48);
```

## Instanced Particles (5000+ partículas)

NO usar un mesh por partícula. Usar BufferGeometry + PointsMaterial:

```javascript
const COUNT = 5000;
const positions = new Float32Array(COUNT * 3);
const colors = new Float32Array(COUNT * 3);
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
const material = new THREE.PointsMaterial({ size: 0.06, vertexColors: true, sizeAttenuation: true });
const mesh = new THREE.Points(geometry, material);
```

Actualizar con `needsUpdate = true` tras modificar positions/colors.

## Marble Material procedural

Crear textura de mármol con Canvas:
1. Base color claro (#f0ebe5)
2. Líneas semi-transparentes para vetas (15-20 iteraciones con bezier random)
3. Puntos dorados sutiles (30-40)
4. CanvasTexture → MeshPhysicalMaterial con clearcoat

```javascript
const material = new THREE.MeshPhysicalMaterial({
  map: texture, color: 0xf0ebe5,
  roughness: 0.12, metalness: 0.02,
  clearcoat: 0.9, clearcoatRoughness: 0.08,
  transparent: true, opacity: 0.82,
});
```

## Gold Band Material

```javascript
new THREE.MeshPhysicalMaterial({
  color: 0xc9a84c, roughness: 0.15,
  metalness: 0.8, clearcoat: 0.5,
});
```

## Mouse Parallax

```javascript
container.addEventListener('mousemove', (e) => {
  const r = container.getBoundingClientRect();
  mouseX = ((e.clientX - r.left) / r.width - 0.5) * 2;
  mouseY = ((e.clientY - r.top) / r.height - 0.5) * 2;
});
// En animate():
hourglassGroup.rotation.y += (mouseX * 0.12 - hourglassGroup.rotation.y) * 0.025;
camera.position.y += (0.5 + mouseY * -0.4 - camera.position.y) * 0.02;
```

## Spin Animation con Easing

```javascript
function spin(duration, rotations, callback) {
  const start = Date.now();
  const startRot = group.rotation.z;
  const total = rotations * Math.PI * 2;
  function tick() {
    const p = Math.min((Date.now() - start) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3); // ease-out cubic
    group.rotation.z = startRot + total * ease;
    if (p < 1) requestAnimationFrame(tick);
    else if (callback) callback();
  }
  tick();
}
```

## Pitfalls Three.js

- `thickness` NO existe en MeshPhysicalMaterial r128 — no usarlo
- `var charts = window.charts = {}` (NO `const`) para globales en frontend
- GitHub Pages CDN cache → usar `?v=N` para bust cache
- Three.js CDN: `cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`
- Pixel ratio: `Math.min(window.devicePixelRatio, 2)` para no matar performance
