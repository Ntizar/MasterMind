# Kit72h Teaser Mad Max — receta completa (sesión 2026-09-06)

Resultado: un teaser 9:16 de ~14s, escena Three.js postapocalíptica (atardecer ámbar, sol bajo, dunas, polvo, objetos del kit levitando) + voz `es-US-AlonsoNeural`. Reproducible con el patrón `webgl-scene-to-video`.

## 1) Escena seekable (`teaser.html`)

Esqueleto del bloque `<script type="module">` (three.js r160 vía importmap CDN):

```js
import * as THREE from 'three';
const c = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas:c, antialias:true, alpha:true});
const W=innerWidth, H=innerHeight;
renderer.setSize(W,H);
renderer.setClearColor(0x000000, 0);   // << clave: deja ver el gradiente CSS de fondo
renderer.setPixelRatio(1);
// ... luces, sol, terreno duna, objetos, partículas ...
function draw(t){
  // cámara dolly: camera.position.set(sin(t*.25)*.7, 3.1 - t*.06, 9 - t*.35); camera.lookAt(0,1.1,0);
  // objetos levitan: o.position.y = 0.9 + sin(t*.8 + i*1.3)*.12
  // partículas deterministas: dp.setY(i, base[i*3+1] + ((t*1.1) % 6));
  // textos (NO CSS keyframes): topEl.style.opacity = clamp((t-0.4)/0.8,0,1); ...
  renderer.render(scene, camera);
}
window.seek = t => draw(t);
window.play = () => { const s=performance.now(); (function f(now){ draw((now-s)/1000); requestAnimationFrame(f); })(); };
window.seek(0);
```

Detalles de la escena Mad Max:
- **Fondo CSS** (el canvas se hace transparente): `linear-gradient(180deg,#120806 0%,#3a1a09 30%,#b85a1c 58%,#e08a2e 66%,#7a3d12 78%,#241008 100%)` — monocromo ámbar, SIN azul.
- **Sol** como esfera `MeshBasicMaterial({color:0xffb347})` + halo transparente `0xff8a1e` opacity .28.
- **Luces:** `AmbientLight(0xffd9a0, 1.5)` + `DirectionalLight(0xff9a3c, 4.0)` (potentes para que los objetos metálicos no salgan siluetas negras) + fill débil.
- **Terreno:** `PlaneGeometry(40,22,90,50)` rotado a plano, altura `sin(x*.35)*.7+cos(z*.5)*.6+sin((x+z)*.2)*.5` * 0.9, `position.y=-0.7`.
- **Objetos del kit** (grupo): radio (caja + antena), botella (cilindro), linterna (cilindro con tapa `emissive`), botiquín (caja + cruz).
- **Polvo:** `THREE.Points` 900 partículas, color `0xd9a45a`, size 0.06, opacity .55; `y = base + (t*1.1 % 6)`.
- **Textos:** `.txt` con `opacity:0` por defecto; `draw(t)` los controla (top a t≈0.4, "KIT 72h" a t≈4.6, subtítulo a t≈5.6).

## 2) Voz (edge-tts) — elegir la más grave

```python
import edge_tts, asyncio
GUION = open('guion.txt', encoding='utf-8').read().strip()
async def main():
    await edge_tts.Communicate(GUION, 'es-US-AlonsoNeural', rate='+0%', pitch='-8Hz').save('voice.mp3')
asyncio.run(main())
```

- Nombre de voz con sufijo `Neural`. `rate`/`pitch` con signo (`'+0%'`, `'-8Hz'`).
- `rate='-15%'` alargó a 22s; con `'+0%'` y guion corto → 13.9s.
- **Selección por f0** (autocorrelación): convertir a wav 16kHz, media de la frecuencia fundamental en frames de 40ms. Candidatas → `alonso` 104.6 Hz (la más grave, elegida), `jorge` 107.4, `alvaro` 109.6. La más grave encaja en trailers.

## 3) Captura (`render.js`)

`npm i puppeteer-core`, `python -m http.server 8123`, Chrome del sistema con SwiftShader:
```js
const puppeteer = require('puppeteer-core');
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
// launch: args ['--no-sandbox','--window-size=1080,1920','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']
// goto http://localhost:8123/teaser.html ; waitForFunction('typeof window.seek==="function"')
// loop i: page.evaluate(tt=>window.seek(tt), i/15); page.screenshot({path:`frames/f_${pad4}.png`});
```
213 frames a 15fps durante 14.2s.

## 4) Montaje

```bash
ffmpeg -y -framerate 15 -i frames/f_%04d.png -i voice.mp3 -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/teaser.mp4
ffmpeg -y -i out/teaser.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=13.4:d=0.5" -af "afade=t=in:st=0:d=0.3,afade=t=out:st=13.62:d=0.3" -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart out/teaser_final.mp4
```
Resultado: 1080×1920, H.264, 15fps, 13.92s, ~1.5 MB.

## 5) Verificación

Extraer frames a t=0.5 / 5 / 13.5 del MP4 y comprobar con visión:
- t=0.5: solo "CUANDO TODO SE APAGUE" (baja opacidad); "KIT 72h" NO visible.
- t=5: "KIT 72h" apareciendo (semi-visible); subtítulo aún no.
- t=13.5: "KIT 72h" grande abajo + subtítulo; cámara más cerca (dolly).
Si todos los frames se ven iguales → el bucle `requestAnimationFrame` compitió con `seek(t)` (ver pitfall en SKILL.md).

## Notas del proyecto
- Ruta: `C:/Users/d_ant/Projects/kit72h/videos/teaser/` (`teaser.html`, `guion.txt`, `voice.mp3`, `render.js`, `out/teaser_final.mp4`).
- Cuando David conecte la cuenta de YouTube del proyecto, subir estos shorts con el pipeline.
