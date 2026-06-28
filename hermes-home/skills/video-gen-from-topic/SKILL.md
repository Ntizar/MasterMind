---
name: video-gen-from-topic
version: "1.0.0"
description: "Pipeline de generación automática de videos cortos desde un tema o keyword — texto → TTS → footage → subtítulos → BGM → output"
tags: [video, ai, automation, tts, moviepy, short-video, content-generation]
---

# Video Generation from Topic — MoneyPrinterTurbo Pattern

## Resumen

Patrón para construir un pipeline de generación automática de videos cortos a partir de un simple tema o palabra clave. Inspirado en [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (88K⭐).

## Qué aporta

- Flujo completo automatizado: tema → guion → voz → imágenes/video → subtítulos → música → video final
- Multi-LLM routing: soporta OpenAI, Anthropic, Gemini, Azure, DashScope, G4F
- TTS gratuito con edge-tts (no requiere API key de pago)
- Composición de video con MoviePy (superposición de texto, imágenes, audio)
- Web UI con Streamlit + API REST con FastAPI

## Patrones clave

1. **Topic-driven generation:** El input es un tema simple, el sistema genera todo el contenido
2. **Multi-LLM fallback chain:** Intenta con el LLM principal, si falla prueba con el siguiente
3. **Edge TTS gratis:** Usa edge-tts (Microsoft Edge TTS gratuito) en lugar de APIs de pago
4. **MoviePy composition pipeline:** Combina clips de video/imágenes con texto superpuesto y audio
5. **Web UI + API dual:** Streamlit para interfaz visual + FastAPI para integración programática

## Tech stack
- **Backend:** Python, FastAPI, Streamlit
- **LLMs:** OpenAI, Anthropic Claude, Google Gemini, Azure OpenAI, DashScope, G4F
- **TTS:** edge-tts (gratuito), Azure Speech SDK
- **Video:** MoviePy, pydub
- **Audio:** faster-whisper (transcripción), pydub (manipulación)
- **Infra:** Docker, Docker Compose, Redis (cola de tareas)

## Cuándo usarlo
- Cuando necesitas generar videos explicativos o informativos automáticamente
- Para crear contenido de redes sociales a escala
- Cuando se requiere generación de video sin intervención humana
- Para prototipar productos de contenido AI-generated
- Cuando edge-tts es suficiente (presupuesto limitado, sin API keys de pago)

## Referencias
- Repo: https://github.com/harry0703/MoneyPrinterTurbo
- Stars: 88572
- License: MIT
