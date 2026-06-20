# Canvas 2D Fallback — Patrón para entornos sin scripts externos

## Cuándo usar

- **Hermes browser tool:** NO ejecuta `<script src>`, importmap, ni ES modules
- **Sandbox sin red:** No puede descargar Three.js
- **Entornos restringidos:** CSP bloquea scripts externos
- **Performance:** Canvas 2D carga instantáneamente (30KB vs 600KB+)

## Patrón base

```javascript
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
    requestAnimationFrame(render);
}
requestAnimationFrame(render);
```

## Simulación 3D con Canvas 2D

### Esfera con gradiente radial (efecto 3D)
```javascript
function drawSphere3D(ctx, cx, cy, radius, baseColor, lightOffset) {
    const grad = ctx.createRadialGradient(
        cx + radius * (lightOffset || -0.3),
        cy + radius * (lightOffset || -0.3),
        radius * 0.1, cx, cy, radius
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

### Glow / halo alrededor de objetos
```javascript
function drawGlow(ctx, cx, cy, radius, color, glowSize) {
    const glow = ctx.createRadialGradient(cx, cy, radius * 0.5, cx, cy, radius * glowSize);
    const c = parseInt(color.slice(1), 16);
    const cr = (c >> 16) & 0xff, cg = (c >> 8) & 0xff, cb = c & 0xff;
    glow.addColorStop(0, `rgba(${cr},${cg},${cb},0.2)`);
    glow.addColorStop(1, `rgba(${cr},${cg},${cb},0)`);
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(cx, cy, radius * glowSize, 0, Math.PI * 2);
    ctx.fill();
}
```

### Órbita elíptica
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

### Campo estelar con twinkle
```javascript
function drawStars(ctx, w, h, stars, cameraOffset, time) {
    for (const star of stars) {
        const sx = ((star.x - cameraOffset.x * 0.05) + w/2) + w/2;
        const sy = ((star.y - cameraOffset.y * 0.05) + h/2) + h/2;
        if (sx < -10 || sx > w + 10 || sy < -10 || sy > h + 10) continue;
        const twinkle = star.brightness + 0.15 * Math.sin(time / 1000 * star.twinkleSpeed);
        ctx.fillStyle = `rgba(255,255,255,${Math.max(0, Math.min(1, twinkle))})`;
        ctx.beginPath();
        ctx.arc(sx, sy, star.size, 0, Math.PI * 2);
        ctx.fill();
    }
}
```

### Interacción: detección de click en esfera
```javascript
function hitTestSphere(mx, my, cx, cy, radius) {
    const dx = mx - cx, dy = my - cy;
    return dx * dx + dy * dy <= radius * radius;
}
```

### Zoom suave con interpolación
```javascript
let camX = 0, camY = 0, zoom = 1;
let targetX = 0, targetY = 0, targetZoom = 1;
camX += (targetX - camX) * 0.05;
camY += (targetY - camY) * 0.05;
zoom += (targetZoom - zoom) * 0.05;
```

## Ejemplo completo: Sistema Solar Canvas 2D

Ver `/root/workspace/sistema-solar/index.html` — ~30KB autocontenido con:
- Sol con glow multicapa y corona pulsante
- 9 planetas con gradientes 3D y detalles específicos
- 2000 estrellas con twinkle
- Órbitas elípticas keplerianas reales
- Click en planeta = zoom suave automático
- Arrastrar para mover, scroll para zoom
- Panel de datos con info de cada planeta
- Touch support

## Comparativa: Canvas 2D vs Three.js

| | Canvas 2D | Three.js |
|---|---|---|
| Tamaño | ~30KB | ~600KB |
| Dependencias | Ninguna | CDN o embebido |
| Entornos | Todos | Requiere scripts externos |
| 3D real | No (simulado) | Sí (WebGL) |
| Iluminación | Gradientes | Phong, PBR, shaders |
| Carga | Instantánea | Depende de CDN |

## Cuándo NO usar Canvas 2D

- El usuario necesita WebGL real (sombras dinámicas, iluminación física)
- Se requiere renderizado de modelos 3D complejos (GLTF/GLB)
- La escena tiene miles de objetos con intersecciones complejas
- Se necesita post-procesado avanzado (bloom, SSAO, DOF)
