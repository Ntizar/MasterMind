# Three.js Particle Background — Template reutilizable

## Patrón completo para fondos animados premium

### Setup básico
```html
<canvas id="three-bg" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none"></canvas>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
```

### Init renderer + scene + camera
```javascript
const canvas = document.getElementById('three-bg');
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.z = 30;
```

### Partículas (600 puntos con colores de paleta)
```javascript
const count = 600;
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);

const palette = [
  new THREE.Color(0x2563eb), // azul
  new THREE.Color(0xf97316), // naranja
  new THREE.Color(0x94a3b8), // gris
  new THREE.Color(0xe2e8f0), // gris claro
];

for (let i = 0; i < count; i++) {
  positions[i*3] = (Math.random()-0.5) * 80;
  positions[i*3+1] = (Math.random()-0.5) * 60;
  positions[i*3+2] = (Math.random()-0.5) * 40;
  const c = palette[Math.floor(Math.random()*palette.length)];
  colors[i*3] = c.r; colors[i*3+1] = c.g; colors[i*3+2] = c.b;
}

const geo = new THREE.BufferGeometry();
geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

const mat = new THREE.PointsMaterial({
  size: 0.15, vertexColors: true, transparent: true,
  opacity: 0.5, blending: THREE.AdditiveBlending, depthWrite: false,
});
scene.add(new THREE.Points(geo, mat));
```

### Formas geométricas wireframe (8 formas flotantes)
```javascript
const shapes = [];
const materials = [
  new THREE.MeshBasicMaterial({ color: 0x2563eb, transparent: true, opacity: 0.04, wireframe: true }),
  new THREE.MeshBasicMaterial({ color: 0xf97316, transparent: true, opacity: 0.03, wireframe: true }),
];

for (let i = 0; i < 8; i++) {
  let geo;
  const r = Math.random();
  if (r < 0.33) geo = new THREE.IcosahedronGeometry(Math.random()*3+1, 0);
  else if (r < 0.66) geo = new THREE.OctahedronGeometry(Math.random()*3+1, 0);
  else geo = new THREE.TetrahedronGeometry(Math.random()*3+1, 0);

  const mesh = new THREE.Mesh(geo, materials[Math.floor(Math.random()*2)]);
  mesh.position.set((Math.random()-0.5)*50, (Math.random()-0.5)*40, (Math.random()-0.5)*20-10);
  mesh.userData = {
    rotSpeed: { x: Math.random()*0.003, y: Math.random()*0.005, z: Math.random()*0.002 },
    floatSpeed: Math.random()*0.3+0.1,
    floatOffset: Math.random()*Math.PI*2,
  };
  scene.add(mesh);
  shapes.push(mesh);
}
```

### Animación + mouse parallax
```javascript
let mouseX = 0, mouseY = 0;
document.addEventListener('mousemove', e => {
  mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
  mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
});

function animate() {
  requestAnimationFrame(animate);
  const t = Date.now() * 0.001;

  // Partículas drift
  const pos = geo.attributes.position.array;
  for (let i = 0; i < count; i++) {
    pos[i*3+1] += Math.sin(t*0.3 + i*0.01) * 0.003;
    pos[i*3] += Math.cos(t*0.2 + i*0.01) * 0.002;
  }
  geo.attributes.position.needsUpdate = true;

  // Shapes rotation + float
  shapes.forEach(s => {
    s.rotation.x += s.userData.rotSpeed.x;
    s.rotation.y += s.userData.rotSpeed.y;
    s.rotation.z += s.userData.rotSpeed.z;
    s.position.y += Math.sin(t * s.userData.floatSpeed + s.userData.floatOffset) * 0.005;
  });

  // Camera parallax
  camera.position.x += (mouseX*2 - camera.position.x) * 0.02;
  camera.position.y += (-mouseY*2 - camera.position.y) * 0.02;
  camera.lookAt(scene.position);

  renderer.render(scene, camera);
}
animate();

// Resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Customización
- **Más partículas:** Cambiar `count` (600 → 1000+). Ojo con rendimiento en móviles.
- **Colores diferentes:** Cambiar el array `palette` con los hex del proyecto.
- **Más sutil:** Reducir `opacity` a 0.3, aumentar `size` a 0.2.
- **Más dinámico:** Aumentar los multiplicadores de drift (0.003 → 0.01).
- **Sin mouse:** Eliminar el bloque de `mousemove` y camera parallax.

## Pitfalls
- **`alpha: true`** en el renderer es obligatorio para que el fondo sea transparente.
- **`depthWrite: false`** en partículas evita que se tapen entre sí.
- **`AdditiveBlending`** da el efecto de brillo sutil. Sin esto, las partículas parecen puntos opacos.
- **Resize handler** es obligatorio — sin él, al cambiar tamaño de ventana se deforma.
- **`pointer-events: none`** en el canvas permite clickear elementos debajo.
