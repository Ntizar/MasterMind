---
name: hyperframes-html-to-video
description: Genera vídeo MP4 desde HTML con HyperFrames si piden vídeo.
version: 1.0.0
tags: [video, html, ffmpeg, puppeteer, agentes, gsap]
---

# HyperFrames — HTML a vídeo (43k★, TypeScript, Apache-2.0, activo)

Framework open-source de HeyGen que convierte HTML + CSS + media + animaciones "seekables" en MP4 deterministas. Diseñado específicamente para agentes IA: escribes HTML, renderiza vídeo con CLI, skills para agentes, o como núcleo de renderizado en servidores.

## Por qué es útil
- Determinista: mismo HTML → mismo frame a frame (a diferencia de screen-capture).
- Usa Puppeteer para capturar frames y FFmpeg para ensamblar; GSAP para animaciones seekables (scrub por timestamp, no reloj real).
- Bloques listos (catálogo): data-charts, textos animados, etc.
- MCP server incluido para integración con agentes.

## Instalación y uso básico
```bash
npm install -g hyperframes        # requiere Node >= 22
hyperframes render comp.html --out video.mp4
```
Estructura: compones una página HTML con timeline (animaciones declaradas en tiempo, ej. GSAP con seek), HyperFrames recorre frame a frame y renderiza.

## Pasos recomendados
1. Escribir el componente HTML/CSS con animaciones basadas en timeline (no setTimeout/RAF — no son seekables).
2. Previsualizar en el Playground (hyperframes.dev) o con `hyperframes preview`.
3. Renderizar CLI: `hyperframes render` (resolución, fps configurables).
4. Para agentes: instalar el skill/MCP de HyperFrames y generar HTML directamente.

## Pitfalls
- Animaciones imperativas (requestAnimationFrame, reloj de pared) NO funcionan: el render seeka el tiempo; usar timeline declarativa (GSAP, Web Animations API).
- Node >= 22 obligatorio; FFmpeg necesario en el PATH.
- Fuentes/woff2 deben estar referenciadas localmente para render reproducible.
- Vídeos largos = mucho tiempo de render; segmentar.

## Verificación
- El MP4 resultante: comprobar duración con `ffprobe video.mp4`.
- Determinismo: renderizar dos veces y comparar hashes si es crítico.

Repo: https://github.com/heygen-com/hyperframes · Docs: https://hyperframes.heygen.com/introduction
