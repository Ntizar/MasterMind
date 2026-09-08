---
name: webgl-scene-to-video
description: "Renderiza escena Three.js/WebGL a MP4 (Puppeteer+ffmpeg)."
version: "1.0.0"
tags: [video, threejs, webgl, puppeteer, ffmpeg, seek, shorts, render, headless]
related_skills: [short-form-video-generation, hyperframes-html-to-video, webgl-headless-verification]
author: "Mastermind (Ntizar)"
license: "MIT"
metadata:
  hermes:
    tags: [video, threejs, webgl, puppeteer, ffmpeg, seek, shorts, render, headless]
    related_skills: [short-form-video-generation, hyperframes-html-to-video, webgl-headless-verification]
---

# WebGL / Three.js Scene → MP4 (headless capture)

Convierte una escena **Three.js/WebGL animada** (no un slideshow de fotos) en un **MP4 vertical 9:16** sincronizado con voz. Vía: **Puppeteer (Chrome headless) captura frame a frame + ffmpeg**. Alternativa a `hyperframes-html-to-video` cuando la escena usa Three.js y quieres control total (o HyperFrames no está instalado).

**No** es el pipeline de fotos/slides de `short-form-video-generation`. Aquí la escena es 3D real (objetos, cámara con dolly, partículas) renderizada a vídeo.

## When to Use

- Cuando quieras un **vídeo vertical (Shorts/Reels/TikTok)** a partir de una **escena 3D/animada** (Three.js, WebGL, canvas) en vez de un carrusel de fotos.
- Cuando un slideshow plano te parezca "flojo" y quieras **movimiento real de cámara** (dolly), objetos 3D y un look cinematográfico (p. ej. estética apocalíptica/Mad Max).
- Cuando `hyperframes` no esté instalado o la escena use Three.js y prefieras control directo de la captura (frame a frame).
- Requiere: Node ≥ 22, Chrome del sistema (o `puppeteer` descargado), `ffmpeg` en el PATH, y `edge_tts` (venv Hermes) para la voz.

## El patrón clave: escena SEEKABLE

Para capturar frame a frame de forma determinista, la animación NO puede depender del reloj real (`performance.now` en un bucle). Debe ser una función `draw(t)` que se pueda fijar en un tiempo arbitrario:

```js
function draw(t){
  // TODO el estado depende de t (cámara, objetos, partículas, textos)
  renderer.render(scene, camera);
}
window.seek = t => draw(t);   // fija y dibuja en el tiempo t
window.play = () => {         // para previsualización en vivo
  const s=performance.now();
  (function f(now){ draw((now-s)/1000); requestAnimationFrame(f); })();
};
window.seek(0);               // dibuja el primer frame
```

- Todo lo que se mueva (cámara, rotación de objetos, partículas, opacidad de textos) debe derivarse de `t` **de forma determinista**, nunca acumulativo.
- Partículas: usar posición base + `(t*v % rango)`, NO `y += 0.01` en cada frame (eso se acumula y rompe el `seek`).
- Textos superpuestos: controlar su `opacity`/`transform` desde `draw(t)` en vez de CSS keyframes, para que también sean seekables.

## Captura con Puppeteer

```js
const puppeteer = require('puppeteer-core');           // usar el Chrome del sistema, no descargar otro
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless:'new',
    args:['--no-sandbox','--window-size=1080,1920','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
  const page = await browser.newPage();
  await page.setViewport({ width:1080, height:1920, deviceScaleFactor:1 });
  await page.goto('http://localhost:8123/teaser.html', { waitUntil:'networkidle2', timeout:60000 });
  await page.waitForFunction('typeof window.seek === "function"', { timeout:30000 });
  const DUR=14.2, FPS=15, n=Math.ceil(DUR*FPS);
  for(let i=0;i<n;i++){
    await page.evaluate(tt => window.seek(tt), i/FPS);
    await page.screenshot({ path:`frames/f_${String(i).padStart(4,'0')}.png` });
  }
  await browser.close();
})();
```

Servir el HTML con un `python -m http.server 8123` en el directorio (el importmap/CDN de three.js funciona vía http; `file://` puede fallar para módulos). `npm i puppeteer-core` es suficiente — **no** hace falta `puppeteer` completo ni descargar Chrome.

## Montaje con ffmpeg

```bash
ffmpeg -y -framerate 15 -i frames/f_%04d.png -i voice.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k \
  -shortest -movflags +faststart out/video.mp4
# fades cinematográficos (opcional): duración = duración del audio
ffmpeg -y -i out/video.mp4 \
  -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=<DUR-0.5>:d=0.5" \
  -af "afade=t=in:st=0:d=0.3,afade=t=out:st=<DUR-0.3>:d=0.3" \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart out/final.mp4
```

## Pitfalls (verificados)

- **El bucle `requestAnimationFrame` compite con `seek(t)`.** Si la página arranca un bucle con el reloj real, corre entre `seek(t)` y el screenshot y sobrescribe el estado → todos los frames salen iguales / el timing de los textos no sigue. **No arranques el bucle automáticamente**: deja `seek(t)` y `play()` como funciones, y usa `seek(t)` en la captura.
- **GPU nativa vs SwiftShader:** `--use-angle=gl` (GPU nativa) dio `THREE.WebGLProgram: Shader Error ... VALIDATE_STATUS false` en Chrome headless. Usar **`--use-angle=swiftshader --enable-unsafe-swiftshader`** (software) — compila limpio. El rAF va a ~20 fps bajo SwiftShader, suficiente para la captura (la sincronización la da `seek(t)`, no el fps).
- **Mostrar el fondo CSS detrás del canvas WebGL:** por defecto el canvas WebGL es opaco y tapa el gradiente CSS. Poner `alpha:true` en el `WebGLRenderer` + `renderer.setClearColor(0x000000, 0)` para que el gradiente de fondo se vea a través.
- **Servir por HTTP** (`python -m http.server`), no `file://`, para los imports ES con importmap (CDN) en headless.

## Verificación

- `ffprobe` el MP4: 1080×1920, H.264/AAC, duración ≈ voz.
- Extraer 2-3 frames a distintos `t` (0.5s, mitad, final) y comprobar visualmente que **el timing de los textos cambia** y la **cámara hace dolly** (los objetos se ven más grandes al final). Solo mirar un frame no confirma la animación.

## Voz (edge-tts) — notas para vídeos con narración

- El nombre de voz debe llevar el sufijo `Neural` (ej. `es-US-AlonsoNeural`), no `es-US-Alonso`.
- `rate` y `pitch` requieren signo: `'+0%'`, `'-8Hz'`. `'0%'` falla con `ValueError`.
- `rate='-15%'` alarga la duración (~22s un guion de 220 chars); para un teaser corto usar `rate='+0%'` y acortar el guion.
- Elegir voz "de peli": generar 2-3 candidatas y comparar su **frecuencia fundamental (f0)** — la más baja (más grave) encaja en trailers apocalípticos. Método: ffmpeg a wav 16 kHz + autocorrelación (ver `references/kit72h-teaser-madmax.md`).

## Preferencia de David (no romper)

- **Visual:** espectáculo primero; **NUNCA gradiente azul→naranja**. Usar monocromo ámbar/sepia cálido (fondo oscuro + un solo acento naranja `#f59e0b`-ish) — respetado en la estética Mad Max.
- **Voz:** para TTS general la voz por defecto es `es-ES-AlvaroNeural`; para **spots/promos cinematográficos David está abierto a una voz más grave** (elegida por f0), como `es-US-AlonsoNeural`.

## Referencias
- `references/kit72h-teaser-madmax.md` — receta completa del teaser Mad Max de kit72h: esqueleto `draw(t)`, render.js, ffmpeg, análisis de f0 para elegir voz, y los ajustes de la escena.
