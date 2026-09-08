# Variante 2D cinematográfica — short vertical "de peli" (sin Three.js)

Enfoque que David **valida** para kit72h y para "no parecer IA slop/videojuego".
Compone con **fotografía real** + **canvas 2D** para atmósfera, no con geometría low-poly.

## Estructura HTML (video_loco.html)

```
#fondo   -> gradiente cinematográfico (radial rojo/naranja oscuro), Ken Burns con transform:scale
#fx      -> <canvas> para humo + brasas (partículas dependientes de t, seekable)
#flare   -> lens flare (radial-gradient, mix-blend:screen)
#vig     -> viñeta (radial-gradient oscuro)
#grain   -> grano (SVG feTurbulence, mix-blend:overlay)
.slide   -> por categoría: .cat (título amarillo skewed) + .panel (img real + marco+glow) + .desc
.punch   -> textos de impacto (intro/cierre), skewX, amarillo/naranja, text-shadow glow
```

- El `#fondo` es un **gradiente CSS**, no una escena 3D. Para que el canvas 2D de
  `#fx` no lo tape, `#fx` es transparente (canvas con `getContext('2d')`, sin fondo).
- Ken Burns: `fondo.style.transform='scale('+(1.02+t*0.012)+')'` en `draw(t)`.

## `draw(t)` + `seek` (determinista, clave para el render)

```js
const T=[0,4.01,12.36,18.82,23.55,28.49,37.15];   // tiempos acumulados de cada segmento (medidos)
const ventanas=[[el1,0,1],[el2,1,2],[el3,2,3],[el4,3,4],[el5,4,5]];
function draw(t){
  fondo.style.transform='scale('+(1.02+t*0.012)+')';
  g.clearRect(0,0,W,H);
  // humo: círculos radiales grises que suben; y = (base - t*sp) % 1
  // brasas: puntos naranjas, opacity con tw = 0.55+sin(t*9+ph)*0.45
  // slides: op=clamp((t-a)/0.18,0,1); transform scale(1.25-0.25*op)
  // textos punch: op=clamp((t-a)/0.2,0,1)*clamp((b-t)/0.3,0,1); scale zoom
  renderer...  // NO hay Three.js; solo dibujo 2D
}
window.seek=t=>draw(t);      // NUNCA auto-arranques un rAF loop si vas a hacer seek
window.play=()=>{...};       // opcional, para previsualizar en vivo
window.seek(0);
```

> **Pitfall crítico:** no arranques un `requestAnimationFrame` loop con reloj de pared
> además del `seek` — sobrescribe el `seek(t)` y todos los frames salen iguales.

## Voz segmentada (sincroniza cada slide con su narración)

```bash
# genera un mp3 por frase y mide su duración; concatena y usa tiempos acumulados
python -c "import edge_tts,asyncio; asyncio.run(edge_tts.Communicate(texto,'es-US-AlonsoNeural',rate='-3%',pitch='-10Hz').save('seg_N.mp3'))"
{ for i in 0 1 2 3 4 5; do printf "file 'seg_%s.mp3'\n" "$i"; done; } > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy voz_full.mp3
```
Voz grave "de narrador": `es-US-AlonsoNeural` (≈104 Hz, la más grave de las es-*).
`rate`/`pitch` exigen signo (`'-3%'`, `'-10Hz'`).

## Render + montaje

```js
// render.js (puppeteer-core + Chrome del sistema)
await page.goto('http://localhost:8123/video_loco.html',{waitUntil:'networkidle2'});
await page.waitForFunction('typeof window.seek === "function"');
for(let i=0;i<n;i++){ await page.evaluate(t=>window.seek(t), i/FPS); await page.screenshot({path:`frames/f_${i}.png`}); }
```
```bash
ffmpeg -y -framerate 15 -i frames/f_%04d.png -i voz_full.mp3 -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart out/short.mp4
ffmpeg -y -i out/short.mp4 -vf "fade=t=in:st=0:d=0.5,fade=t=out:st=<dur-0.5>:d=0.5" \
  -af "afade=t=in:st=0:d=0.4,afade=t=out:st=<dur-0.4>:d=0.4" -c:v libx264 -pix_fmt yuv420p -c:a aac out/short_final.mp4
```
- Headless: `--no-sandbox` (sin GPU necesaria; canvas 2D va por CPU, no usa WebGL).
- Render largo (>500 frames) puede exceder el timeout de foreground (600s): **trocea** con
  un `START` (índice de frame) y re-abre la página — `seek` es determinista, no duplica trabajo.

## Sourcing de imágenes reales
- **Amazon por ASIN**: `amazon.es/s?k=<query>` con cookie jar + UA; imagen del bloque `data-asin="<ASIN>"`.
  Sustituir `_AC_UL320_` → `_AC_SL1500_` para alta resolución. Si el ASIN no sale en la 1ª
  página, probar queries alternativas o tomar la imagen del primer resultado del tema.
- **Wikimedia Commons** (CC) para fondo/paisajes: `commons.wikimedia.org/w/api.php` con
  `generator=search` + `gsrsearch=filetype:bitmap <tema>` + `prop=imageinfo` + `iiurlwidth`.
  User-Agent obligatorio; filtrar por mime `image/jpeg` y width ≥1400 (la API devuelve
  thumburl None a veces — guarda `or ii.get("url")` y comprueba `None`).

## Coste
Render (Puppeteer+ffmpeg) y voz (edge-tts) = **locales, cero tokens**. Solo el guion LLM
(~50–150K tokens/vídeo). Para 26 vídeos (blog+kits) ≈ $1–3 en LLM + horas de render local.
