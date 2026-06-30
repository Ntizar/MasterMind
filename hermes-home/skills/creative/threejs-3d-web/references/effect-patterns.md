# Effect Implementation Patterns

Concrete patterns extracted from the Blonde Voulain VJ Processor (blonde-vj-processor).

## 01. Neon Tracer — Body Contour with Glow Trail

Traces the body contour with neon glow, leaving fading trails.

```javascript
// Get body contour from landmarks
function getContour(lm) {
  const indices = [11,13,15,17,19,21,19,17,15,13,11,12,14,16,18,20,22,20,18,16,14,12,24,26,28,30,32,30,28,26,24,23,25,27,29,31,29,27,25,23,11];
  return indices.filter(i => i < lm.length && lm[i].visibility > 0.5)
    .map(i => ({ x: lm[i].x, y: lm[i].y }));
}

// Draw smooth neon contour
ctx.beginPath();
ctx.moveTo(contour[0].x * w, contour[0].y * h);
for (let i = 1; i < contour.length; i++) {
  const prev = contour[i - 1], curr = contour[i];
  const cpx = ((prev.x + curr.x) / 2) * w;
  const cpy = ((prev.y + curr.y) / 2) * h;
  ctx.quadraticCurveTo(prev.x * w, prev.y * h, cpx, cpy);
}
ctx.closePath();
ctx.strokeStyle = `hsla(${hue},100%,60%,${alpha})`;
ctx.shadowColor = `hsla(${hue},100%,60%,${alpha})`;
ctx.shadowBlur = 25;
ctx.stroke();
```

## 02. Grid Distortion — Cyberpunk Perspective Grid

Perspective grid that warps around the detected body position.

```javascript
// Body distortion on grid nodes
const cx = body.center.x * w, cy = body.center.y * h;
const bodyRadius = body.height * h * 0.4;

for (let r = 0; r <= rows; r++) {
  for (let c = 0; c <= cols; c++) {
    let x = c * gridSize, y = r * gridSize;
    
    // Perspective warp
    const py = (y / h - 0.5) * 2;
    x = w / 2 + (x - w / 2) * (1 + py * 0.3);
    
    // Body repulsion
    const dx = x - cx, dy = y - cy;
    const dist = Math.sqrt(dx * dx + dy * dy);
    if (dist < bodyRadius * 2) {
      const force = (1 - dist / (bodyRadius * 2)) * 40;
      const angle = Math.atan2(dy, dx);
      x += Math.cos(angle) * force * Math.sin(t * 3 + dist * 0.02);
      y += Math.sin(angle) * force * Math.cos(t * 2 + dist * 0.03);
    }
  }
}
```

## 03. Particle Burst — Explosion from Hands

Particles spawn from hand positions, explode on beat.

```javascript
// Spawn from hands
if (body.hands) {
  for (const side of ['left', 'right']) {
    const hand = body.hands[side];
    if (hand && hand.x > 0 && hand.x < 1) {
      for (let i = 0; i < 2 + audio.volume * 5; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 50 + Math.random() * 150 + audio.volume * 200;
        particles.push({
          x: hand.x, y: hand.y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          gravity: 50,
          life: 0.5 + Math.random() * 1.5,
          size: 2 + Math.random() * 4,
        });
      }
    }
  }
}

// Explosion on beat
if (audio.beat) {
  for (let i = 0; i < 20; i++) {
    // Same spawn logic from body center, higher speed
  }
}
```

## 04. Constellation — Connected Landmarks as Star Map

All 33 landmarks as glowing nodes connected by pulsing lines.

```javascript
const connections = [
  [11, 12], [11, 13], [13, 15], [15, 17], [17, 19], [19, 21],
  [12, 14], [14, 16], [16, 18], [18, 20], [20, 22],
  [11, 23], [12, 24], [23, 24], [23, 25], [24, 26],
  [25, 27], [26, 28], [27, 29], [28, 30], [29, 31], [30, 32],
];

// Draw connections
for (const [a, b] of connections) {
  if (lm[a].visibility < 0.4 || lm[b].visibility < 0.4) continue;
  ctx.beginPath();
  ctx.moveTo(lm[a].x * w, lm[a].y * h);
  ctx.lineTo(lm[b].x * w, lm[b].y * h);
  ctx.strokeStyle = `rgba(0,240,255,${0.3 * pulse * audioMult})`;
  ctx.stroke();
}

// Draw nodes with radial glow
for (let i = 0; i < lm.length; i++) {
  if (lm[i].visibility < 0.4) continue;
  const x = lm[i].x * w, y = lm[i].y * h;
  const grad = ctx.createRadialGradient(x, y, 0, x, y, size * 3);
  grad.addColorStop(0, `rgba(0,240,255,${0.3 * twinkle})`);
  grad.addColorStop(1, 'rgba(0,240,255,0)');
  ctx.fillStyle = grad;
  ctx.fill();
}
```

## 05. Shockwave — Concentric Rings from Body Center

Expanding rings spawned on beat or fast movement.

```javascript
// Spawn condition
if (audio.beat || bodyVelocity > threshold) {
  waves.push({
    x: body.center.x, y: body.center.y,
    radius: 0, maxRadius: 0.8,
    speed: 0.4 + audio.volume * 0.3,
    life: 1, hue: (Date.now() * 0.1) % 360,
  });
}

// Render
for (const wave of waves) {
  const r = wave.radius * Math.min(w, h);
  ctx.beginPath();
  ctx.arc(wave.x * w, wave.y * h, r, 0, Math.PI * 2);
  ctx.strokeStyle = `hsla(${hue},100%,60%,${wave.life * 0.6})`;
  ctx.lineWidth = 3;
  ctx.shadowBlur = 20;
  ctx.stroke();
}
```

## 06. Synthwave Sunset — Retro Horizon + Sun

Horizon line, gradient sun with scan lines, perspective grid.

```javascript
// Sun with horizontal scan lines
ctx.save();
ctx.beginPath();
ctx.arc(w / 2, sunY, sunRadius, 0, Math.PI * 2);
ctx.clip();
// Draw gradient sun, then horizontal gaps
for (let i = 0; i < 10; i++) {
  const lineY = sunY - sunRadius + (sunRadius * 2 / 10) * i;
  ctx.fillStyle = 'rgba(10,5,30,0.6)';
  ctx.fillRect(w / 2 - sunRadius, lineY, sunRadius * 2, 2 + i * 1.5);
}
ctx.restore();

// Perspective grid (scrolling)
gridOffset = (gridOffset + dt * 60 * speed) % 40;
for (let i = 0; i < 20; i++) {
  const progress = (i * 40 + gridOffset) / (20 * 40);
  const y = horizonY + Math.pow(progress, 2) * (h - horizonY);
  ctx.strokeStyle = `rgba(255,0,255,${progress * 0.3})`;
  ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
}
```

## 07. Portal Vortex — Spiral Galaxy Behind Body

Orbiting stars + spiral arms around body center.

```javascript
// Spiral arms
for (let arm = 0; arm < 4; arm++) {
  ctx.beginPath();
  for (let i = 0; i < 100; i++) {
    const progress = i / 100;
    const angle = armOffset + progress * Math.PI * 4 + t * 2;
    const r = progress * portalRadius;
    const x = cx + Math.cos(angle) * r;
    const y = cy + Math.sin(angle) * r;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.strokeStyle = `hsla(${280 + arm * 30},80%,60%,0.15)`;
  ctx.stroke();
}

// Orbiting stars
for (const star of stars) {
  star.angle += star.speed * dt;
  const x = cx + Math.cos(star.angle) * star.radius * portalRadius;
  const y = cy + Math.sin(star.angle) * star.radius * portalRadius;
  ctx.arc(x, y, star.size, 0, Math.PI * 2);
  ctx.fill();
}
```

## 08. Energy Field — Rays from Hands + Body Aura

Wavy energy lines emanating from each hand, plus body outline glow.

```javascript
// Rays from hands
for (const hand of [lm[15], lm[16]]) {
  if (!hand || hand.visibility < 0.4) continue;
  for (let i = 0; i < 8; i++) {
    const angle = (i / 8) * Math.PI * 2 + t * 2;
    const length = 100 + audioMult * 200;
    ctx.beginPath();
    ctx.moveTo(hand.x * w, hand.y * h);
    // Wavy line with sine offset perpendicular to direction
    for (let s = 1; s <= segments; s++) {
      const px = hx + Math.cos(angle) * length * (s / segments);
      const py = hy + Math.sin(angle) * length * (s / segments);
      const offset = Math.sin(t * 8 + s * 2) * 10 * audioMult;
      ctx.lineTo(px + perpX * offset, py + perpY * offset);
    }
    ctx.stroke();
  }
}
```

## Color Palette Reference (Cyberpunk)

```javascript
const PALETTE = {
  cyan: '#00f0ff',
  magenta: '#ff00ff',
  yellow: '#ffe033',
  green: '#00ff41',
  red: '#ff0040',
  blue: '#4060ff',
  purple: '#c471f5',
  orange: '#ff6b35',
  white: '#ffffff',
};
```

## HSL Helper

```javascript
hsl(h, s, l, a) { return `hsla(${h},${s}%,${l}%,${a || 1})`; }
// Usage: hue cycling for rainbow effects
const hue = (Date.now() * 0.05) % 360;
ctx.strokeStyle = this.hsl(hue, 100, 60, alpha);
```
