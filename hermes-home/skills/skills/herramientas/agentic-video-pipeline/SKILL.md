---
name: agentic-video-pipeline
version: "1.0.0"
description: >
  Pipeline de procesamiento de vídeo agéntico: raw video → shorts, reels, 
  captions, blog posts, social posts. Usa múltiples agentes LLM (Whisper, 
  Gemini, Copilot SDK) con herramientas de FFmpeg, frame capture, y 
  generación de assets. Inspirado en vidpipe.
license: MIT
tags: [herramientas, video, AI, pipeline]

---

# Pipeline de Vídeo Agéntico

## Visión General

Patrón para construir pipelines de procesamiento de vídeo automatizados 
usando agentes LLM especializados. Inspirado en [htekdev/vidpipe](https://github.com/htekdev/vidpipe) (166⭐).

## Arquitectura de Agentes

```
IdeaDiscoveryAgent  →  ProducerAgent  →  ScheduleAgent
                                           ↓
                                     ChapterAgent
                                           ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
              MediumVideoAgent      ShortsAgent          BlogAgent
                    ↓                      ↓                      ↓
              SummaryAgent      SilenceRemovalAgent    SocialMediaAgent
                    ↓                      ↓                      ↓
              ThumbnailAgent       GraphicsAgent       InterviewAgent
```

## Agentes Principales

| Agente | Responsabilidad | Modelos |
|--------|----------------|---------|
| `IdeaDiscoveryAgent` | Genera ideas de video basadas en tendencias | Gemini |
| `ProducerAgent` | Coordina el pipeline completo | GPT-4 |
| `ScheduleAgent` | Divide el vídeo en capítulos | GPT-4 |
| `ChapterAgent` | Crea estructura de capítulos | GPT-4 |
| `ShortsAgent` | Genera clips cortos virales | GPT-4 |
| `MediumVideoAgent` | Genera vídeos medianos | GPT-4 |
| `BlogAgent` | Convierte vídeo en blog post | Gemini |
| `SocialMediaAgent` | Genera posts para redes | GPT-4 |
| `SummaryAgent` | Crea resúmenes ejecutivos | GPT-4 |
| `SilenceRemovalAgent` | Detecta y elimina silencios | GPT-4 |
| `ThumbnailAgent` | Genera thumbnails | DALL-E |
| `GraphicsAgent` | Crea gráficos y overlays | DALL-E |
| `InterviewAgent` | Genera contenido de entrevistas | GPT-4 |

## Pipeline Specs

Tres perfiles de procesamiento:

- **minimal.yaml** — Solo transcripción + resumen
- **full.yaml** — Pipeline completo (todos los agentes)
- **clean.yaml** — Transcripción + captions + shorts

## Herramientas del Agente

### Frame Capture
```typescript
captureFrame(videoPath, timestamp) → { imagePath: string }
```

### Video Info
```typescript
getVideoInfo(videoPath) → { width, height, duration, fps }
```

### Transcript
```typescript
getTranscript(videoPath, start?, end?) → { text, words: [{word, start, end}] }
```

### FFmpeg
```typescript
execFFmpeg(args) → { success, outputPath?, error? }
```

### Image Generation
```typescript
generateImage(prompt) → { imagePath: string }
```

## Asset Types

Cada agente produce un asset tipado:

- `VideoAsset` — Vídeo completo
- `ShortVideoAsset` — Clip corto (<60s)
- `MainVideoAsset` — Vídeo principal
- `MediumClipAsset` — Clip mediano
- `BlogAsset` — Post de blog
- `SocialPostAsset` — Post de red social
- `SummaryAsset` — Resumen ejecutivo
- `TextAsset` — Texto plano (transcripción, captions)

## Configuración

- `.env.example` — Variables de entorno
- `pipeline-specs/*.yaml` — Definiciones de pipeline
- `brand.json` — Marca y estilo
- `schedule.json` — Programación de publicación

## Referencias
- [htekdev/vidpipe](https://github.com/htekdev/vidpipe) — Implementación completa
- [npm vidpipe](https://www.npmjs.com/package/vidpipe) — Paquete público

## 2. Video Processing Pipeline — vidpipe

Pipeline de procesamiento de vídeo con IA — transcripción, edición automática, captions, shorts y posts para redes sociales. Inspirado en vidpipe.

### Flujo
1. Transcripción con Whisper
2. Edición automática (silence removal, chapters)
3. Generación de captions y subtítulos
4. Creación de shorts/clips virales
5. Generación de posts para redes sociales

### Diferencia con agentic-video-pipeline
`agentic-video-pipeline` es el patrón de arquitectura multi-agente (IdeaDiscovery → Producer → Schedule → Chapter → MediumVideo/Shorts/Blog). `video-processing-pipeline` es el flujo práctico de producción: raw video → shorts, reels, captions, blog posts, social posts.
