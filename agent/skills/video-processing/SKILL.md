---
name: video-processing
version: "1.0.0"
description: "Ecosistema completo de procesamiento de vídeo: pipelines agénticos multi-LLM, generación automática desde topic, edición, transcripción, shorts, captions y posts para redes sociales."
tags: [video, ai, pipeline, automation, tts, short-video, content-generation, ffmpeg, whisper]
---

# Video Processing — Ecosistema Completo

## Resumen

Ecosistema completo de procesamiento de vídeo con IA que cubre todos los patrones de uso:

| Subskill | Cuándo usar | Output |
|----------|-------------|--------|
| **Agentic Pipeline** | Pipeline completo multi-agente desde raw video | Shorts, reels, captions, blog posts, social posts |
| **Video from Topic** | Generación automática desde keyword/simple topic | Video completo con TTS, footage, subtítulos, BGM |

## Sección 1: Agentic Pipeline (vidpipe pattern)

**Para:** Procesamiento de vídeo existente con múltiples agentes LLM especializados.
**Arquitectura:** IdeaDiscovery → Producer → Schedule → Chapter → MediumVideo/Shorts/Blog
**Agentes:** Whisper transcripción, Gemini tendencias, GPT-4 edición, DALL-E thumbnails
**Pipeline specs:** minimal.yaml, full.yaml, clean.yaml
**Herramientas:** Frame capture, transcript, FFmpeg, image generation

## Sección 2: Video from Topic (MoneyPrinterTurbo pattern)

**Para:** Generación automática de videos cortos desde un tema o palabra clave.
**Flujo:** tema → guion → voz → imágenes/video → subtítulos → música → video final
**Tech stack:** FastAPI, Streamlit, MoviePy, edge-tts (gratis), multi-LLM routing
**Web UI:** Streamlit visual + API REST

## Decision Guide

```
¿Tienes un vídeo existente?
├── Sí → Agentic Pipeline (vidpipe)
│        └── ¿Quieres solo transcripción? → minimal.yaml
│        └── ¿Quieres todo (shorts, blog, social)? → full.yaml
│        └── ¿Quieres transcripción + shorts? → clean.yaml
│
└── ¿Quieres generar un vídeo desde cero?
    └── Sí → Video from Topic (MoneyPrinterTurbo)
             └── ¿Presupuesto limitado? → edge-tts gratis
             └── ¿Necesitas multi-LLM? → OpenAI/Claude/Gemini routing
```

## Referencias

- [htekdev/vidpipe](https://github.com/htekdev/vidpipe) — Pipeline agéntico multi-agente
- [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) — Generación automática desde topic (88K⭐)
