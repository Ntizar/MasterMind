# Canvas2D Particle Background — Documentos flotantes

## Uso
Fondo animado para landing pages, dashboards, herramientas. Partículas tipo documentos que flotan y reaccionan al mouse.

## Patrón mínimo

```html
<canvas id="bg" style="position:fixed;inset:0;width:100vw;height:100vh;z-index:0;pointer-events:none;"></canvas>
<script>
(() => {
  const c = document.getElementById('bg');
  const ctx = c.getContext('2d');
  let w, h, particles = [], mouse = {x:-999,y:-999};

  function resize() { w = c.width = innerWidth; h = c.height = innerHeight; }
  resize();
  addEventListener('resize', resize);
  addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });

  class P {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random()*w; this.y = Math.random()*h;
      this.size = 8+Math.random()*18;
      this.vx = (Math.random()-0.5)*0.3;
      this.vy = -0.15-Math.random()*0.3;
      this.rot = Math.random()*Math.PI*2;
      this.vr = (Math.random()-0.5)*0.008;
      this.alpha = 0.04+Math.random()*0.08;
      this.type = Math.random()>0.6?'doc':'circle';
    }
    update() {
      this.x += this.vx; this.y += this.vy; this.rot += this.vr;
      const dx=this.x-mouse.x, dy=this.y-mouse.y, d=Math.sqrt(dx*dx+dy*dy);
      if(d<120){const f=(120-d)/120*0.8;this.x+=(dx/d)*f;this.y+=(dy/d)*f;}
      if(this.y<-30){this.y=h+30;this.x=Math.random()*w;}
      if(this.x<-30)this.x=w+30;if(this.x>w+30)this.x=-30;
    }
    draw() {
      ctx.save(); ctx.translate(this.x,this.y); ctx.rotate(this.rot);
      ctx.globalAlpha = this.alpha;
      if(this.type==='doc'){
        const s=this.size;
        ctx.fillStyle='#fff'; ctx.shadowColor='rgba(0,0,0,0.08)'; ctx.shadowBlur=6;
        ctx.beginPath(); ctx.roundRect(-s/2,-s*0.65,s,s*1.3,2); ctx.fill();
        ctx.shadowBlur=0; ctx.fillStyle='#e2e8f0';
        for(let i=0;i<3+Math.floor(Math.random()*3);i++)
          ctx.fillRect(-s/2+s*0.12,-s*0.65+s*0.2+i*s*0.16,s*(0.4+Math.random()*0.35),s*0.06);
      } else {
        ctx.fillStyle=Math.random()>0.5?'#dbeafe':'#ffedd5';
        ctx.beginPath(); ctx.arc(0,0,this.size*0.3,0,Math.PI*2); ctx.fill();
      }
      ctx.restore();
    }
  }

  const count = Math.min(50, Math.floor(w*h/25000));
  for(let i=0;i<count;i++) particles.push(new P());

  function bg() {
    const g1=ctx.createRadialGradient(w*0.2,h*0.3,0,w*0.2,h*0.3,w*0.6);
    g1.addColorStop(0,'rgba(219,234,254,0.5)'); g1.addColorStop(1,'rgba(248,250,252,0)');
    ctx.fillStyle=g1; ctx.fillRect(0,0,w,h);
    // ... añadir más gradientes para colores personalizados
  }

  (function loop(){ctx.clearRect(0,0,w,h);bg();particles.forEach(p=>{p.update();p.draw();});requestAnimationFrame(loop);})();
})();
</script>
```

## Customización

| Variable | Efecto |
|----------|--------|
| `this.size = 8+Math.random()*18` | Tamaño de partículas |
| `this.alpha = 0.04+Math.random()*0.08` | Transparencia (0.02-0.15 recomendado) |
| `count = Math.min(50, Math.floor(w*h/25000))` | Densidad (25000 = ~50 en 1920x1080) |
| `if(d<120)` | Radio de repulsión del mouse |
| `this.vy = -0.15-Math.random()*0.3` | Velocidad vertical (negativo = sube) |
| Colores en `ctx.fillStyle` | Cambiar `#dbeafe`, `#ffedd5`, `#f3e8ff` |

## Pitfalls

- **Canvas necesita `pointer-events: none`** — si no, bloquea clicks en el contenido
- **`z-index: 0` en canvas, `z-index: 1` en contenido** — el contenido debe estar encima
- **`roundRect` no existe en navegadores muy antiguos** — fallback: `ctx.fillRect`
- **Demasiadas partículas (>80) causan lag** — limitar con `Math.min(50, ...)`
- **Mouse tracking en mobile** — `mousemove` no existe, las partículas solo flotan
