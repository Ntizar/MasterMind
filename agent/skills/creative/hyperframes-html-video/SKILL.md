---
name: hyperframes-html-video
description: "Usa a convertir HTML a vídeo con HyperFrames CLI."
version: "2.0.0"
tags: [hyperframes, video, html, cli, render, mp4, heygen]
related_skills: [hyperframes-html-to-video, video-processing, hyperframes-html-video, manim-video]
---

# HyperFrames — HTML → vídeo (CLI, no librería)

> ⚠️ Corrección 2026-09-05 (auditoría): el paquete npm `hyperframes` es **CLI-only** (bin `hyperframes`, sin `main`/`exports`); no expone `import { render }`. La vía correcta es el CLI `npx hyperframes render` (o los skills / `@hyperframes/core`).

**Repo:** `https://github.com/heygen-com/hyperframes` (TypeScript, ~44K⭐). Apache-2.0, Node >=22 + FFmpeg.

## When to Use

- Cuando pidas **convertir un HTML animado a vídeo MP4** (render determinista con Chrome headless + FFmpeg). Soporta GSAP/Lottie/Three.js.

## Uso (CLI real)

```bash
npm install hyperframes        # solo CLI
npx hyperframes render entrada.html -o salida.mp4
# o vía los skills del repo (y @hyperframes/core / @hyperframes/engine)
```

## Pitfalls

- **NO** `import { render } from 'hyperframes'` ni `{html, css, output, width, height, fps}` — no hay API exportada; es CLI-only.
- `npm install hyperframes` instala el CLI, no una librería.

## Verificación

- `npx hyperframes render tu.html -o final.mp4` → comprobar el vídeo de salida.
