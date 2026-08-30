---
name: video-use-agentic-editing
description: "Usa al editar vídeo por agente con ffmpeg (video-use)."
version: 1.0.0
tags: [video, ffmpeg, agent, edicion, subtitles]
---

# video-use — Edición de vídeo dirigida por agente (21K⭐)

## Qué es

Repo `browser-use/video-use`: dropas footage crudo en una carpeta, hablas con un agente CLI (Claude Code, Codex, Hermes...) y recibes `final.mp4`. Sin presets ni menús — el agente ejecuta scripts ffmpeg de `helpers/`.

## Capacidades

- **Corta muletillas** (`umm`, `uh`, falsos arranques) y espacio muerto entre tomas
- **Color grading automático** por segmento (cadenas ffmpeg custom)
- **Fades de audio de 30ms** en cada corte (evita pops)
- **Subtítulos quemados** estilo custom (por defecto chunks de 2 palabras en MAYÚSCULAS)
- **Overlays de animación** vía HyperFrames, Remotion, Manim o PIL — sub-agentes paralelos, uno por animación
- **Auto-evaluación** del render en cada corte antes de mostrar nada
- **Memoria de sesión** en `project.md` — retoma donde lo dejaste

## Setup

```bash
git clone https://github.com/browser-use/video-use.git
cd video-use
# leer install.md: configura ffmpeg, registra skill, pide API key de ElevenLabs
# leer helpers/ — ahí viven los scripts de edición
```

Dependencias Python: librosa, matplotlib, numpy, pillow, requests (pyproject.toml). Requiere ffmpeg instalado y un agente CLI con acceso a shell.

## Flujo de uso

1. Instalar y dejar listo (no transcribir nada por cuenta propia)
2. El usuario dropa footage en la carpeta
3. Instruir al agente por chat: "corta los silencios y quema subtítulos"
4. El agente ejecuta scripts de helpers/, auto-evalúa cortes, produce final.mp4

## Cuándo usarlo

- Talking heads, tutoriales, entrevistas, montajes de viaje
- Cuando el usuario pide "editar este vídeo" sin decirle qué software
- Pipeline agéntico: compleméntalo con `video-processing` para transcodificación y `hyperframes-html-to-video` para overlays HTML→MP4

## Pitfalls

- Necesita ElevenLabs API key para transcripción/voz — pedirla al usuario, nunca inventar
- No transcribir por cuenta propia antes del install; dejar que el agente use sus helpers
- Los scripts viven en `helpers/`, no en la raíz — siempre leer esa carpeta
- La auto-evaluación de cortes añade tiempo de render; no desactivarla para material largo

## Verificación

```bash
ls final.mp4 && ffprobe -v error -show_entries format=duration final.mp4
```

## Referencias

- Repo: github.com/browser-use/video-use (MIT)
