---
name: short-form-video-generation
description: "Usa a hacer shorts verticales con voz y fotos reales."
version: "1.0.0"
tags: [video, shorts, reels, tiktok, tts, ffmpeg, slides, monetizacion, product-images]
related_skills: [video-gen-from-topic, video-processing, hyperframes-html-video, manim-video]
author: "Mastermind (Ntizar)"
license: "MIT"
metadata:
  hermes:
    tags: [video, shorts, reels, tiktok, tts, ffmpeg, slides, monetizacion, product-images]
    related_skills: [video-gen-from-topic, video-processing, hyperframes-html-video, manim-video]
---

# Short-Form Video Generation (9:16 vertical)

Pipeline programático para producir un **short vertical** (Shorts/Reels/TikTok) con voz + slides + imágenes reales, sin GPU ni claves de pago. Stack: **edge-tts** (voz) + **Pillow** (slides) + **ffmpeg** (composición) + **imágenes reales** (Wikimedia CC o Amazon por ASIN).

**No** es `moneyprinterturbo`/stock random: es el montaje con imágenes **reales y variadas** del tema (clave para que no parezca un vídeo de bot).

## When to Use

- Cuando pidas **generar un short/vídeo vertical** (Shorts, Reels, TikTok) a partir de un tema/producto, con voz, slides y **imágenes reales**.
- Para contenido de **afiliación** (productos Amazon) o de marca, donde "una foto fija de stock" o "texto plano" queda flojo.
- Cuando no haya GPU ni claves de pago para texto-a-vídeo (se compone con stock/imágenes, no se genera con modelos).

## Preferencias de David (embebidas — NO romper)
- **Voz:** `es-ES-AlvaroNeural` (edge-tts). Nunca voz genérica/femenina por defecto.
- **Estilo visual:** espectáculo primero; pero **NUNCA gradiente azul→naranja** (lo odia). Usar fondo **sólido oscuro** + **un solo acento** (p.ej. ámbar `#f59e0b`) + texto blanco gordo.
- **No hagas un solo plano estático:** **varía la imagen por ítem** (cada producto/idea con su foto real). Texto plano sobre fondo = "muy flojo".
- Si el producto/servicio está en Amazon, usa **imágenes reales del producto** (por ASIN), no stock genérico.
- **NO escena 3D low-poly + texto superpuesto = «IA slop»/«videojuego» — David lo rechazó explícitamente.** El look que David **valida** para kit72h es: **fotos reales de producto** (por ASIN) en panel con marco+glow + **grading cinematográfico** (contraste/saturate/sepia, grano, viñeta, lens flare) + **humo/brasas en canvas-2D** + **Ken Burns** (zoom) + **texto punch** skewed amarillo/naranja + **guion con punch** (frases cortas épicas/desesperadas, guiños a Mad Max). Usa la **variante 2D cinematográfica**, no la 3D, salvo que David pida explícitamente 3D.

## Pipeline (comandos que funcionan)

```bash
# 1) VOZ (en el venv de Hermes, tiene edge_tts)
python -c "import edge_tts,asyncio; asyncio.run(edge_tts.Communicate(open('guion.txt',encoding='utf-8').read().strip(),'es-ES-AlvaroNeural').save('voice.mp3'))"
# medir duracion: ffprobe -v error -show_entries format=duration -of csv=p=0 voice.mp3

# 2) SLIDES (Python312, tiene Pillow): foto + scrim + titulo gordo + acento -> slides/slide_0N.png
python build_slides.py

# 3) COMPOSICION — slideshow RAPIDO (loop 1 + concat + audio). OJO: NO usar zoompan, es lentisimo.
for i in 01 02 03 04 05; do ffmpeg -y -loglevel error -loop 1 -t 5 -i slides/slide_$i.png \
  -vf "fps=30,scale=1080:1920" -c:v libx264 -pix_fmt yuv420p segs/seg_$i.mp4; done
{ for i in 01 02 03 04 05; do printf "file 'C:/.../segs/seg_%s.mp4'\n" "$i"; done; } > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -i voice.mp3 -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart out/short.mp4
```

- **Duración por slide** = `duracion_voz / n_slides` (redondea a entero; `-shortest` recorta al audio).
- Resolución 1080×1920 (9:16). H.264 + AAC.

## Variante 3D cinematográfica (Three.js → MP4, para el "salto de nivel")
Cuando David quiere el vídeo **más espectacular/realista** que un slideshow, renderiza una escena **Three.js** a MP4 con **Puppeteer frame-by-frame** (no `zoompan`, no HyperFrames). Receta completa en `references/threejs-video-render.md`. Claves (todas verificadas):
- **Escena seekable**: exponer `window.seek(t)` que dibuja el estado en tiempo `t`. **NUNCA auto-arranques el loop `requestAnimationFrame`** si vas a hacer `seek` — el loop corre con reloj de pared y **sobrescribe** el `seek(t)` justo antes de cada screenshot (bug real: todos los frames salen iguales y los textos no siguen el timing). Exponer `window.play()`/`stop()` y llamar `window.seek(0)` al cargar.
- **Sincronizar slides con la narración**: genera el audio **por segmento** (una frase = un slide) con edge-tts, mide cada duración con `ffprobe`, concatena con el demuxer de ffmpeg, y usa los tiempos **acumulados** como ventanas de visibilidad de cada slide en `draw(t)`.
- **Fondo que se vea**: si el cielo es un gradiente CSS detrás del canvas, el `WebGLRenderer` necesita `alpha:true` + `renderer.setClearColor(0x000000, 0)` — sin eso el canvas limpia a negro y **tapa** el gradiente.
- **Render largo = reiniciable**: `seek(t)` es determinista, así que renderiza en trozos; acepta un `START` (índice de frame) y re-abre la página para continuar sin duplicar trabajo.
- **Acabado**: fades de entrada/salida con `ffmpeg -vf "fade=t=in...,fade=t=out..." -af "afade=..."`.

## Variante 2D cinematográfica (CANVAS 2D — la que David VALIDA para kit72h)

Cuando David pide que **NO** parezca "IA slop"/"videojuego", usa esta variante (sin Three.js): **fondo gradiente cinematográfico** (Ken Burns con `transform:scale`) + **canvas 2D** para humo y brasas (partículas dependientes de `t`, seekable) + **fotos reales de producto** en panel con marco+glow + **texto punch** skewed + **guion loco** narrado por segmento. Receta completa (HTML + render.js + ffmpeg) en `references/canvas2d-cinematic-short.md`.

**Coste (clave para escalar a muchos vídeos):** el render (Puppeteer+ffmpeg) y la voz (edge-tts) son **locales y gratis — cero tokens**; solo el guion LLM cuesta (~50–150K tokens/vídeo). El trabajo "caro" de desarrollo del pipeline se paga una vez.

## Imágenes reales (sourcing)
- **Wikimedia Commons** (CC, gratis, sin key): `commons.wikimedia.org/w/api.php` con `generator=search` + `gsrsearch=filetype:bitmap <tema>` + `prop=imageinfo` + `iiurlwidth`. **Obligatorio User-Agent** (403 sin él) y **filtrar resultados** (la query "agua" devolvió un **mono bebiendo** — excluir títulos con `monkey|maca|animal|museum|collection`...). Preferir `image/jpeg` >1000px.
- **Amazon por ASIN**: las páginas de producto (`/dp/<ASIN>`) devuelven **vacío a curl sin cookies** (bloqueo). La vía fiable es **buscar** `amazon.es/s?k=<query>` con **cookie jar + UA** (patrón de `kit72h/scripts/buscar-amazon.py`) y extraer la imagen del bloque `data-asin="<ASIN>"` (`<img ... src="https://m.media-amazon.com/images/I/...">`). Detalle en `references/imagenes-producto-amazon.md`.
- **PA-API** de Amazon (GetItems → imagen+precio) es la vía 100% compliant y estable si se tienen keys de Associates; la scraping funciona pero falla a veces (ASIN no en 1ª página → 4/6).

## Pitfalls (verificados)
- **`zoompan` de ffmpeg es un cuello de botella enorme** (re-encodifica cada frame; ~60-100s/segmento en 1080×1920; un vídeo de 6 planos se quedó a 4/6 a los 400s). **Usa slideshow estático** (`-loop 1` + concat) para velocidad; si quieres movimiento, mételo en los slides o usa `xfade` (más rápido que zoompan).
- `pip install` no trae Pillow en el venv de Hermes; usar el **Python del sistema** (`C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe`, tiene Pillow). `edge_tts` vive en el **venv de Hermes**, no en el del sistema.
- Windows: rutas nativas a ffmpeg/curl (no `/tmp`); `-o` a un path nativo.
- **Disclosure de afiliación** si usas imágenes de Amazon + enlace afiliado (guías de Associates).
- **edge-tts**: los nombres de voz llevan sufijo `Neural` (`es-US-AlonsoNeural`, no `es-US-Alonso`) y `rate`/`pitch` **exigen signo** (`'+0%'`, no `'0%'`; `'-8Hz'`). Para elegir la voz más cinematográfica, medir la **frecuencia fundamental** (autocorrelación sobre el wav) y quedarse con la más grave (ej. `es-US-AlonsoNeural` ≈104 Hz vs `es-ES-AlvaroNeural` ≈110 Hz).

## Verificación
- `ffprobe` el mp4: 1080×1920, H.264/AAC, duración ≈ voz. Reproducir y comprobar que **cambia de imagen por ítem** y la voz es Álvaro.

## Referencias
- `references/imagenes-producto-amazon.md` — receta completa de extracción de imagen por ASIN (search + cookie jar + data-asin).
- `references/threejs-video-render.md` — receta de escena Three.js seekable → MP4 (Puppeteer frame-by-frame + ffmpeg), con el fix del loop rAF.
