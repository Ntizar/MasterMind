---
name: agent-canvas-visualization
description: "Visualización de agentes IA en Canvas 2D — grafo radial con partículas animadas que simulan comunicación entre agentes. Para dashboards de control y monitorización multi-agente."
version: 1.0.0
tags: [mastermind, visualization, canvas, agents, dashboard, animation]
---

# Agent Canvas Visualization

Patrón para visualizar agentes IA comunicándose en un Canvas 2D. Usado en el Mastermind Dashboard para mostrar Mastermind, Explorer, Planner, Implementer, Reviewer y Critic.

## Arquitectura del canvas

```
Mastermind (centro-arriba)
  ├── Explorer (izquierda-media)
  ├── Planner (centro-izquierda)
  ├── Implementer (centro-derecha)
  ├── Reviewer (derecha-media)
  └── Critic (centro-abajo)
```

Cada agente se conecta con Mastermind mediante líneas punteadas. Las partículas vuelan entre agentes simulando comunicación.

## Estructura de datos

```javascript
const AGENTS = [
  { id: 'mastermind', name: 'Mastermind', color: '#2563eb', x: 0.5, y: 0.15, r: 22 },
  { id: 'explorer', name: 'Explorer', color: '#10b981', x: 0.15, y: 0.55, r: 16 },
  { id: 'planner', name: 'Planner', color: '#f59e0b', x: 0.38, y: 0.55, r: 16 },
  { id: 'implementer', name: 'Implementer', color: '#f97316', x: 0.62, y: 0.55, r: 16 },
  { id: 'reviewer', name: 'Reviewer', color: '#8b5cf6', x: 0.85, y: 0.55, r: 16 },
  { id: 'critic', name: 'Critic', color: '#ef4444', x: 0.5, y: 0.85, r: 16 },
];
```

- `x`, `y` son proporciones (0-1) del ancho/alto del canvas
- `r` es el radio del círculo en píxeles
- `color` en hex

## Técnicas de renderizado

### 1. Glow de agente
```javascript
const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 3);
grad.addColorStop(0, color + '40');
grad.addColorStop(1, color + '00');
ctx.fillStyle = grad;
ctx.beginPath();
ctx.arc(cx, cy, r * 3, 0, Math.PI * 2);
ctx.fill();
```

### 2. Círculo con borde
```javascript
ctx.beginPath();
ctx.arc(cx, cy, r, 0, Math.PI * 2);
ctx.fillStyle = color + '30';
ctx.fill();
ctx.strokeStyle = color;
ctx.lineWidth = 2;
ctx.stroke();
```

### 3. Inner glow (efecto 3D)
```javascript
const ig = ctx.createRadialGradient(cx - r*0.3, cy - r*0.3, 0, cx, cy, r);
ig.addColorStop(0, color + '80');
ig.addColorStop(1, color + '10');
ctx.fillStyle = ig;
ctx.beginPath();
ctx.arc(cx, cy, r * 0.7, 0, Math.PI * 2);
ctx.fill();
```

### 4. Partícula voladora entre agentes
```javascript
const fx = from.x * w, fy = from.y * h;
const tx = to.x * w, ty = to.y * h;
const progress = Math.min(1, (time - msg.start) / msg.duration);
const ease = 1 - Math.pow(1 - progress, 3);
const cx = fx + (tx - fx) * ease;
const cy = fy + (ty - fy) * ease;

// Trail punteado
ctx.beginPath();
ctx.moveTo(fx, fy);
ctx.lineTo(cx, cy);
ctx.strokeStyle = from.color + '40';
ctx.lineWidth = 2;
ctx.setLineDash([4, 4]);
ctx.stroke();
ctx.setLineDash([]);

// Partícula
ctx.beginPath();
ctx.arc(cx, cy, 4 + Math.sin(time * 0.01) * 2, 0, Math.PI * 2);
ctx.fillStyle = from.color;
ctx.fill();
```

### 5. Conexiones estáticas (líneas punteadas)
```javascript
ctx.beginPath();
ctx.moveTo(mx, my);
ctx.lineTo(ax, ay);
ctx.strokeStyle = 'rgba(255,255,255,0.04)';
ctx.lineWidth = 1;
ctx.setLineDash([3, 6]);
ctx.stroke();
ctx.setLineDash([]);
```

## Loop de animación

```javascript
function animate(time) {
  resizeCanvas(); // Ajustar al tamaño del contenedor
  ctx.clearRect(0, 0, w, h);

  // 1. Dibujar conexiones estáticas
  // 2. Dibujar partículas voladoras
  // 3. Dibujar agentes (con glow pulsante)

  requestAnimationFrame(animate);
}
```

## Simulación de actividad

```javascript
const patterns = [
  { from: 'mastermind', to: 'planner', action: 'Delegó planificación' },
  { from: 'planner', to: 'mastermind', action: 'Plan completado' },
  // ...
];

let activityIdx = 0;
function simulateActivity() {
  const a = patterns[activityIdx % patterns.length];
  activityIdx++;
  sendMessage(a.from, a.to);
}
setInterval(simulateActivity, 3000);
```

## Leyenda

```html
<div class="agent-legend">
  <div class="agent-legend-item">
    <span class="agent-legend-dot" style="background:#2563eb"></span>
    Mastermind
  </div>
  <!-- ... -->
</div>
```

## Pitfalls

1. **Resize en cada frame** — necesario para que el canvas se adapte al contenedor. Usar `window.devicePixelRatio` para retina.
2. **No usar `const` para el canvas** — usar `var charts = window.charts = {}` si hay múltiples canvases en la página.
3. **Partículas con duración fija** — 1500ms es buen default. Limpiar mensajes viejos: `messages = messages.filter(m => (time - m.start) < m.duration)`.
4. **Easing cúbico** para movimiento natural: `1 - Math.pow(1 - progress, 3)`.
5. **Fondo del canvas** debe coincidir con el fondo de la página para que los glows se vean bien.