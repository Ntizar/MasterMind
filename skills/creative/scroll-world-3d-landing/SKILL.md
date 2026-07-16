---
name: scroll-world-3d-landing
description: Scroll-scrubbed 3D fly-through landing pages — skill de agente que genera mundos inmersivos con scroll continuo, AI art y video generation.
category: creative
---

# Scroll World — Landing Pages 3D con Scroll-Scrubbing

## Qué es

**scroll-world** (oso95/scroll-world, 483⭐) es un skill de agente (compatible con Claude Code, Codex, y cualquier agente que soporte SKILL.md) que genera **landing pages inmersivas 3D** donde la cámara "vuela" a través de escenas conectadas sin cortes, controlado por el scroll del usuario.

## Cómo funciona

1. **Higgsfield CLI** genera el arte visual (escenas diorama isométricas + camera flights)
2. **ffmpeg/ffprobe** extrae frames y codifica el video final
3. **Python + Pillow** hace transparent-scene knockout (opcional)
4. Resultado: landing page HTML con scroll-scrubbing que controla la reproducción del video

## Patrón arquitectónico — Scroll-Scrubbed Video

```javascript
// Sincronizar scroll del usuario con tiempo del video
const video = document.querySelector('video');
window.addEventListener('scroll', () => {
  const progress = window.scrollY / (document.body.scrollHeight - window.innerHeight);
  video.currentTime = progress * video.duration;
});
```

## Casos de uso para proyectos de David

- Landing pages de proyectos (GTFSSpain, DataHubEspana) con intro 3D
- Showcases de visualizaciones con fly-through de mapas
- Storytelling geoespacial — volar sobre un mapa 3D mostrando datos

## Requisitos

- **Higgsfield CLI** autenticado con créditos
- `ffmpeg` / `ffprobe`
- Python 3 con Pillow (opcional)

## Pitfalls

- Higgsfield requiere créditos — cada landing consume créditos de AI generation
- El video puede ser pesado — optimizar con WebM/VP9
- Scroll-scrubbing necesita RAF para suavizar
- Mobile performance puede ser laggy

## Referencias

- Repo: https://github.com/oso95/scroll-world
- Higgsfield: https://higgsfield.ai
