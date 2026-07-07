---
name: hyperframes-html-video
version: "1.0.0"
description: "HyperFrames — Framework open-source de HeyGen para convertir HTML/CSS/animaciones en videos MP4 determinísticos. Built for AI agents."
tags: [video, html, animation, mp4, rendering, agent, ffmpeg, gsap]
---

# HyperFrames — HTML a Video Determinístico

## Resumen

[HyperFrames](https://github.com/heygen-com/hyperframes) (⭐34K) de HeyGen es un framework open-source que convierte HTML, CSS, media y animaciones seekables en videos MP4 determinísticos. Diseñado para ser usado por AI coding agents.

**Diferencia clave**: A diferencia de herramientas de screen-capture, HyperFrames genera videos determinísticos desde código HTML — mismo input = mismo output siempre.

## Cuándo usar

- Generar videos programáticamente desde HTML/CSS
- Crear contenido de video para AI agents
- Animaciones de datos a video (dashboards → video)
- Generación de contenido multimedia automatizado

## Patrón de uso

```bash
# Instalar como paquete npm
npm install hyperframes

# O usar como CLI
npx hyperframes render ./index.html --output output.mp4
```

```javascript
// Como librería Node.js
import { render } from 'hyperframes';

const result = await render({
  html: './index.html',
  css: './styles.css',
  output: 'output.mp4',
  width: 1920,
  height: 1080,
  fps: 30,
  // GSAP animations son soportadas nativamente
});
```

```javascript
// Con GSAP para animaciones
import gsap from 'gsap';

// Las animaciones GSAP se renderizan automáticamente en el video
gsap.to('.element', { duration: 2, x: 100 });
```

## Features clave

| Feature | Descripción |
|---------|-------------|
| HTML → MP4 | Convierte cualquier HTML/CSS a video |
| GSAP nativo | Animaciones GSAP renderizadas automáticamente |
| Determinístico | Mismo input = mismo output siempre |
| AI Agent ready | Diseñado para ser usado por agentes de IA |
| Node.js + CLI | Usar como librería o como herramienta CLI |
| Seekable | Animaciones seekables para control preciso |

## Integración con otros skills

- **claude-design**: Generar diseño en HTML → HyperFrames para video
- **manim-video**: Alternativa para animaciones más complejas
- **baoyu-infographic**: Infografías HTML → video con HyperFrames

## Pitfalls

- **Node.js >= 22**: Requiere versión reciente de Node.js
- **ffmpeg**: Necesita ffmpeg instalado en el sistema para el encoding final
- **Limitaciones CSS**: No todos los efectos CSS son soportados (filter, blend-mode, etc.)
- **Tamaño**: Los videos pueden ser grandes. Usar compresión adecuada

## Referencias
- Docs: https://hyperframes.heygen.com
- Quickstart: https://hyperframes.heygen.com/quickstart
- Catalog: https://hyperframes.heygen.com/catalog/blocks/data-chart

---

**Hecho con ❤️ por David Antizar**