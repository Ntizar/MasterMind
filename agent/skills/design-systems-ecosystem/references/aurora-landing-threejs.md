# Aurora Landing — Three.js Pattern

Patrón completo de la landing page de Ntizar Aurora con Three.js. Reutilizable para cualquier design system landing que necesite un hero 3D único.

## Arquitectura

```
hero (position: relative, min-height: 100vh)
├── canvas#aurora-canvas (position: absolute, inset: 0, z-index: 0)
├── hero__content (position: relative, z-index: 2)
│   ├── badge, title, subtitle, CTA buttons
└── hero__scroll (position: absolute, bottom: 2rem)
```

## Three.js Scene Components

### 1. Icosaedro wireframe central

```javascript
const icoGeo = new THREE.IcosahedronGeometry(4.5, 1);
const icoEdges = new THREE.EdgesGeometry(icoGeo);
const icoMat = new THREE.LineBasicMaterial({
  color: new THREE.Color('#2563eb'),
  transparent: true,
  opacity: 0.35
});
const icoWire = new THREE.LineSegments(icoEdges, icoMat);
scene.add(icoWire);

// Shell sólido translúcido
const icoSolid = new THREE.Mesh(icoGeo, new THREE.MeshBasicMaterial({
  color: new THREE.Color('#2563eb'),
  transparent: true,
  opacity: 0.03,
  side: THREE.DoubleSide
}));
scene.add(icoSolid);
```

### 2. Partículas con shader custom (1200 puntos)

Distribución en toroide + esfera para efecto aurora boreal:

```javascript
// ShaderMaterial para puntos circulares suaves
const pMat = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 },
    uPixelRatio: { value: Math.min(window.devicePixelRatio, 2) }
  },
  vertexShader: `
    attribute float size;
    attribute vec3 color;
    varying vec3 vColor;
    uniform float uTime;
    uniform float uPixelRatio;
    void main() {
      vColor = color;
      vec3 pos = position;
      float pulse = sin(uTime * 0.5 + length(pos) * 0.3) * 0.15;
      pos *= 1.0 + pulse;
      vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
      gl_PointSize = size * 300.0 * uPixelRatio / -mvPosition.z;
      gl_Position = projectionMatrix * mvPosition;
    }
  `,
  fragmentShader: `
    varying vec3 vColor;
    void main() {
      vec2 uv = gl_PointCoord - 0.5;
      float dist = length(uv);
      if (dist > 0.5) discard;
      float alpha = smoothstep(0.5, 0.0, dist);
      alpha = pow(alpha, 1.5);
      gl_FragColor = vec4(vColor, alpha * 0.85);
    }
  `,
  transparent: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending
});
```

**Paleta estricta (sin morado):**
```javascript
const COLOR_BLUE = new THREE.Color('#2563eb');
const COLOR_BLUE_SOFT = new THREE.Color('#60a5fa');
const COLOR_ORANGE = new THREE.Color('#f97316');
const COLOR_ORANGE_SOFT = new THREE.Color('#fdba74');
// NUNCA: new THREE.Color('#7c3aed') — violeta prohibido
```

### 3. Constelación dinámica (líneas entre partículas cercanas)

```javascript
function updateConstellation() {
  const threshold = 2.5;
  let lineIdx = 0;
  const step = 4; // Samplear subconjunto para performance
  for (let i = 0; i < N_PARTICLES && lineIdx < MAX_LINES; i += step) {
    for (let j = i + step; j < N_PARTICLES && lineIdx < MAX_LINES; j += step) {
      const dist = /* distancia 3D */;
      if (dist < threshold) {
        // Escribir posiciones y colores en linePositions/lineColors
        lineIdx++;
      }
    }
  }
  lineGeo.setDrawRange(0, lineIdx * 2);
  linePosAttr.needsUpdate = true;
}
// Llamar cada 3 frames (no cada frame) para performance
```

### 4. Anillos orbitales

```javascript
for (let i = 0; i < 3; i++) {
  const ringGeo = new THREE.TorusGeometry(6 + i * 1.5, 0.015, 8, 80);
  const ringCol = i % 2 === 0 ? COLOR_BLUE : COLOR_ORANGE;
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({
    color: ringCol, transparent: true, opacity: 0.15
  }));
  ring.rotation.x = Math.PI / 2 + (i * 0.3);
  ring.rotation.y = i * 0.4;
  ringGroup.add(ring);
}
```

### 5. Parallax mouse suave

```javascript
const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
window.addEventListener('mousemove', (e) => {
  mouse.tx = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.ty = -(e.clientY / window.innerHeight) * 2 + 1;
});

// En animation loop:
mouse.x += (mouse.tx - mouse.x) * 0.05;  // lerp factor
mouse.y += (mouse.ty - mouse.y) * 0.05;
camera.position.x = mouse.x * 2;
camera.position.y = mouse.y * 2;
camera.lookAt(0, 0, 0);
```

## WebGL Context Fix (crítico)

Algunos navegadores headless crean un contexto 2D por defecto. Fix:

```javascript
const gl = canvas.getContext('webgl2', { alpha: true, antialias: true, powerPreference: 'high-performance' })
        || canvas.getContext('webgl', { alpha: true, antialias: true, powerPreference: 'high-performance' });
const renderer = new THREE.WebGLRenderer({ context: gl, canvas, alpha: true, antialias: true });
```

## Verificación sin visión

Si el modelo no soporta `browser_vision`/`vision_analyze`, verificar via `browser_console`:

```javascript
// ✅ Correcto — no toca el contexto del canvas
canvas.width > 0 && canvas.height > 0  // renderer resizeó el canvas
getComputedStyle(document.body).backgroundColor  // fondo blanco

// ❌ Incorrecto — consume el contexto WebGL y rompe el renderer
canvas.getContext('webgl2')  // NUNCA hacer esto si Three.js ya está usando el canvas
```

## Reduced Motion

```javascript
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  renderer.render(scene, camera);  // una sola vez
} else {
  animate();  // loop completo
}
```

## Liquid Glass CSS (4 capas)

```css
.glass {
  background: linear-gradient(135deg,
    rgba(255,255,255,0.72) 0%, rgba(241,245,249,0.55) 50%, rgba(255,255,255,0.62) 100%);
  backdrop-filter: blur(24px) saturate(180%);
  box-shadow:
    inset 0 1px 0 0 rgba(255,255,255,0.9),   /* highlight superior */
    inset 0 -1px 0 0 rgba(0,0,0,0.04),        /* sombra inferior */
    0 8px 32px rgba(37,99,235,0.06),          /* sombra azul exterior */
    0 2px 8px rgba(249,115,22,0.04);           /* sombra naranja exterior */
  border: 1px solid rgba(255,255,255,0.6);
}
.glass::before {  /* specular highlight */
  background: linear-gradient(180deg, rgba(255,255,255,0.45) 0%, transparent 60%);
}
.glass::after {   /* borde cromático (azul+naranja, sin morado) */
  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.35),
    inset 0 0 20px rgba(37,99,235,0.04),
    inset 0 0 40px rgba(249,115,22,0.03);
}
```

## Bento Grid Responsive

```css
.bento { grid-template-columns: repeat(4, 1fr); }
@media (max-width: 900px) { .bento { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 560px) { .bento { grid-template-columns: 1fr; } }
```

Cells asimétricas: `.bento__cell--lg` (span 2x2), `--wide` (span 2 col), `--tall` (span 2 row).
