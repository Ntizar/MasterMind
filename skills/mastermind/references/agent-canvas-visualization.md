# Visualización de Agentes con Canvas

Patrón para mostrar agentes comunicándose en un dashboard usando Canvas 2D nativo (sin librerías externas).

## Estructura básica

```javascript
const AGENTS = [
  { id: 'mastermind', name: 'Mastermind', color: '#2563eb', x: 0.5, y: 0.15, r: 22 },
  { id: 'explorer',  name: 'Explorer',  color: '#10b981', x: 0.15, y: 0.55, r: 16 },
  { id: 'planner',   name: 'Planner',   color: '#f59e0b', x: 0.38, y: 0.55, r: 16 },
  { id: 'implementer', name: 'Implementer', color: '#f97316', x: 0.62, y: 0.55, r: 16 },
  { id: 'reviewer',  name: 'Reviewer',  color: '#8b5cf6', x: 0.85, y: 0.55, r: 16 },
  { id: 'critic',    name: 'Critic',    color: '#ef4444', x: 0.5,  y: 0.85, r: 16 },
];
```

## Elementos visuales

### 1. Glow exterior
```javascript
const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 3);
grad.addColorStop(0, a.color + '40');
grad.addColorStop(1, a.color + '00');
ctx.fillStyle = grad;
ctx.beginPath();
ctx.arc(cx, cy, r * 3, 0, Math.PI * 2);
ctx.fill();
```

### 2. Círculo con borde
```javascript
ctx.beginPath();
ctx.arc(cx, cy, r, 0, Math.PI * 2);
ctx.fillStyle = a.color + '30';
ctx.fill();
ctx.strokeStyle = a.color;
ctx.lineWidth = 2;
ctx.stroke();
```

### 3. Inner glow (efecto 3D)
```javascript
const ig = ctx.createRadialGradient(cx - r*0.3, cy - r*0.3, 0, cx, cy, r);
ig.addColorStop(0, a.color + '80');
ig.addColorStop(1, a.color + '10');
ctx.fillStyle = ig;
ctx.beginPath();
ctx.arc(cx, cy, r * 0.7, 0, Math.PI * 2);
ctx.fill();
```

### 4. Pulsación suave
```javascript
const r = a.r + Math.sin(time * 0.002 + a.id.length) * 2;
```

## Animación de mensajes entre agentes

### Partícula viajera
```javascript
function drawMessage(msg, time) {
  const progress = Math.min(1, (time - msg.start) / msg.duration);
  if (progress >= 1) return;

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
}
```

### Easing cúbico para movimiento natural
```javascript
const ease = 1 - Math.pow(1 - progress, 3);
```

## Conexiones estáticas (líneas punteadas del centro a los hijos)
```javascript
animAgents.forEach(a => {
  if (a.id === 'mastermind') return;
  ctx.beginPath();
  ctx.moveTo(mx, my);
  ctx.lineTo(ax, ay);
  ctx.strokeStyle = 'rgba(255,255,255,0.04)';
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 6]);
  ctx.stroke();
  ctx.setLineDash([]);
});
```

## High DPI (Retina)
```javascript
canvas.width = rect.width * (window.devicePixelRatio || 1);
canvas.height = rect.height * (window.devicePixelRatio || 1);
ctx.scale(window.devicePixelRatio || 1, window.devicePixelRatio || 1);
```

## Activity log (texto)

Patrón de items con animación slideIn:
```css
@keyframes slideIn {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}
```

Cada item muestra: `[from] → [to] [acción] [timestamp]` con colores por agente.

## Referencia completa

Ver `public/dashboard.html` en el repo `github.com/Ntizar/Mastermind-Dashboard` para la implementación completa (~400 líneas de JS de canvas + animación).