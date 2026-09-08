# Escena Three.js seekable → MP4 (Puppeteer frame-by-frame + ffmpeg)

Cómo renderizar una escena Three.js animada a un MP4 vertical determinista, en local sin GPU de pago.
Stack: **puppeteer-core** (Chrome del sistema, SwiftShader) + **ffmpeg** + **edge-tts**. Verificado en kit72h (teaser 13.9s y vídeo explicativo 66s).

## El bug que casi lo tira todo (LEER PRIMERO)
Si la página arranca un loop `requestAnimationFrame`, ese loop corre con el **reloj de pared** y **sobrescribe** el `window.seek(t)` que llamas desde Puppeteer justo antes de cada screenshot. Resultado: todos los frames salen con el mismo tiempo (el de la página), los textos no siguen el timing y el vídeo parece congelado.

**Fix:** que la escena sea **seekable** — un único `draw(t)` que dibuja el estado en tiempo `t` — y **NO auto-arranques el loop**:
```js
window.seek = t => draw(t);
window.play = () => { const s=performance.now(); (function f(now){ draw((now-s)/1000); requestAnimationFrame(f); })(); };
window.seek(0);   // dibuja el primer frame al cargar
```
Para previsualizar en vivo, llama `play()`; para capturar, usa `seek(t)` y nada más.

## Escena con fondo CSS (que el cielo se vea)
Si el cielo es un gradiente CSS en un `div` detrás del canvas:
```js
const renderer = new THREE.WebGLRenderer({canvas:c, antialias:true, alpha:true});
renderer.setClearColor(0x000000, 0);   // SIN esto el canvas limpia a negro y tapa el gradiente
```
Materiales que renderizan en SwiftShader (software): `MeshStandardMaterial` / `MeshBasicMaterial` con luces potentes (`DirectionalLight` intensidad ~4, `AmbientLight` ~1.5). Evitar `MeshPhysicalMaterial` con `transmission` (sale negro).

## Sincronizar slides con la narración
1. Guion segmentado: `[(clave, texto), ...]` (intro, cada categoría, outro).
2. Genera **un mp3 por segmento** con edge-tts.
3. Mide cada duración con `ffprobe -v error -show_entries format=duration -of csv=p=0`.
4. Concatena con el demuxer: `ffmpeg -f concat -safe 0 -i list.txt -c copy voice_full.mp3`.
5. En `draw(t)`, usa los tiempos **acumulados** como ventanas de visibilidad de cada slide, con fade de ~0.45s:
```js
const T=[0,6.46,15.36,25.08,31.99,39.12,46.75,53.69,60.39,66.36]; // acumulados
for(let i=0;i<slides.length;i++){
  const a=T[i], b=T[i+1];
  let op = (t>=a && t<b) ? Math.min(1,(t-a)/0.45,(b-t)/0.45) : 0;
  slides[i].style.opacity = Math.max(0,Math.min(1,op));
}
```

## Captura con Puppeteer (render.js)
```js
const puppeteer=require('puppeteer-core');
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
(async()=>{
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',
    args:['--no-sandbox','--window-size=1080,1920','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
  const page=await browser.newPage();
  await page.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  await page.goto('http://localhost:8123/video_explica.html',{waitUntil:'networkidle2',timeout:60000});
  await page.waitForFunction('typeof window.seek==="function"',{timeout:30000});
  const DUR=66.6, FPS=15, n=Math.ceil(DUR*FPS);
  const START=parseInt(process.env.START||'0',10);   // reanudar render
  for(let i=START;i<n;i++){ await page.evaluate(t=>window.seek(t), i/FPS);
    await page.screenshot({path:`frames2/f_${String(i).padStart(4,'0')}.png`}); }
  await browser.close();
})();
```
- Sirve la página con `python -m http.server 8123` en el dir (los módulos ES + importmap con CDN funcionan sobre http; `file://` puede fallar por CORS de imports).
- **SwiftShader** = ~21 fps rAF; el `seek(t)` usa tiempo real, así que el vídeo es fluido a 15 fps aunque el render software sea lento. La GPU nativa (`--use-angle=gl`) daba errores de shader; SwiftShader no.
- **Render largo = reiniciable**: si el timeout corta a mitad, ejecuta `START=<ultimo_frame> node render.js` (el `seek` es determinista → no duplica ni se desincroniza).
- El audio se monta con `-shortest` para recortar al audio.

## Montaje + acabado
```bash
ffmpeg -y -framerate 15 -i frames2/f_%04d.png -i voice_full.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out/video.mp4
# fades de entrada/salida
ffmpeg -y -i out/video.mp4 \
  -vf "fade=t=in:st=0:d=0.6,fade=t=out:st=<dur-0.6>:d=0.6" \
  -af "afade=t=in:st=0:d=0.4,afade=t=out:st=<dur-0.4>:d=0.4" \
  -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart out/video_final.mp4
```
Verificar: `ffprobe` 1080×1920, H.264/AAC; `ffmpeg ... -af volumedetect` → mean ≈ −20 dB (hay voz, no silencio).
