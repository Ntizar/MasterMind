# Mármol Procedural con CanvasTexture (Three.js)

Patrón para crear materiales de mármol realistas sin texturas externas. Usado en ARENA (hourglass griego).

## Concepto

Crear una textura de mármol usando Canvas 2D → `THREE.CanvasTexture`. Venas semi-transparentes + flecks dorados + base blanca.

## Código completo

```javascript
function createMarbleMaterial() {
  const canvas = document.createElement('canvas');
  canvas.width = 512;
  canvas.height = 512;
  const ctx = canvas.getContext('2d');

  // 1. Base blanca
  ctx.fillStyle = '#f5f0eb';
  ctx.fillRect(0, 0, 512, 512);

  // 2. Venas de mármol (líneas curvas semi-transparentes)
  for (let i = 0; i < 12; i++) {
    ctx.beginPath();
    ctx.strokeStyle = `rgba(180, 170, 155, ${0.08 + Math.random() * 0.12})`;
    ctx.lineWidth = 0.5 + Math.random() * 1.5;

    let x = Math.random() * 512;
    let y = Math.random() * 512;
    ctx.moveTo(x, y);

    for (let j = 0; j < 20; j++) {
      x += (Math.random() - 0.5) * 80;
      y += (Math.random() - 0.3) * 60;
      ctx.lineTo(x, y);
    }
    ctx.stroke();
  }

  // 3. Flecks dorados
  for (let i = 0; i < 40; i++) {
    ctx.fillStyle = `rgba(201, 168, 76, ${0.05 + Math.random() * 0.1})`;
    ctx.beginPath();
    ctx.arc(Math.random() * 512, Math.random() * 512, 1 + Math.random() * 2, 0, Math.PI * 2);
    ctx.fill();
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;

  return new THREE.MeshPhysicalMaterial({
    map: texture, color: 0xf5f0eb,
    roughness: 0.15, metalness: 0.02,
    clearcoat: 0.8, clearcoatRoughness: 0.1,
    transparent: true, opacity: 0.88, side: THREE.DoubleSide,
  });
}
```

## Variaciones

- **Mármol negro:** base `#1a1a1a`, venas `rgba(60,60,60)`, sin flecks
- **Verde Alpi:** base `#1a3a2a`, venas `rgba(100,160,120)`
- **Rosa:** base `#f5e0e0`, venas `rgba(180,120,130)`
