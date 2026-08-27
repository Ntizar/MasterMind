---
name: voicebox
description: "Voicebox — Estudio de voz AI local-first open-source. 7 motores TTS, clonación de voz, dictado global, transcripción STT, integración MCP. Alternativa local a ElevenLabs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [voice, tts, stt, voice-clone, mcp, audio, elevenlabs-alternative]
    category: media
---

# voicebox — Open-Source AI Voice Studio

Voicebox (28K⭐) es un estudio de voz AI local-first, gratuito y open-source (MIT), alternativo a ElevenLabs + WisprFlow combinados.

## Filosofía
- **Privacidad total**: modelos, datos de voz y capturas nunca salen de tu máquina
- **Stack completo de voz I/O**: clonación, generación TTS, dictado global, transcripción STT, agentes con voz
- **Nativo**: construido con Tauri (Rust), no Electron
- **Multi-plataforma**: macOS (Apple Silicon con MLX/Metal), Windows (CUDA), Linux (AMD ROCm, Intel Arc, CPU), Docker

## Instalación

```bash
# Descarga directa
# macOS ARM: https://voicebox.sh/download/mac-arm
# macOS Intel: https://voicebox.sh/download/mac-intel
# Windows: https://voicebox.sh/download/windows
# Docker: docker compose up

# Desde fuente (desarrollo)
git clone https://github.com/jamiepine/voicebox.git
cd voicebox
just setup   # crea venv, instala deps Python + JS
just dev     # inicia backend + app desktop
```

## 7 Motores TTS

| Motor | Modelos | Clonación | Idiomas | Tamaño | Características |
|-------|---------|-----------|---------|--------|----------------|
| **Qwen3-TTS** | 0.6B / 1.7B | Sí (zero-shot 10s) | 10 (es incluido) | 1.2-3.5 GB | Mayor calidad, cloning de voz |
| **Qwen CustomVoice** | 0.6B / 1.7B | Preset speakers | 10 | 1.2-3.5 GB | **Instruct support** (control de delivery) |
| **LuxTTS** | luxtts | Sí (zero-shot 3s) | Inglés | ~300 MB | CPU-friendly, 48kHz, 150x realtime en CPU |
| **Chatterbox Multilingual** | chatterbox-tts | Sí (zero-shot 5s) | **23 idiomas** | ~3.2 GB | Mayor cobertura lingüística |
| **Chatterbox Turbo** | chatterbox-turbo | Sí (zero-shot 5s) | Inglés | ~1.5 GB | **Paralinguistic tags** ([laugh], [sigh]), baja latencia |
| **HumeAI TADA** | 1B / 3B Multilingual | Sí (zero-shot) | EN (1B), 10 (3B) | 4-8 GB | Modelo speech-language, audio 700s+ |
| **Kokoro** | 82M | Preset (50+ voces) | 8 (es incluido) | **350 MB** | CPU realtime, Apache 2.0 |

## REST API (localhost:17493)

```bash
# Generar speech
curl -X POST http://127.0.0.1:17493/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hola mundo", "profile_id": "abc123", "language": "es"}'

# Agent voice output — cualquier app puede hablar en voz clonada
curl -X POST http://127.0.0.1:17493/speak \
  -H "X-Voicebox-Client-Id: my-script" \
  -d '{"text": "Deploy complete.", "profile": "Morgan"}'

# Transcribir audio
curl -X POST http://127.0.0.1:17493/transcribe \
  -F "audio=@recording.wav" \
  -F "model=whisper-turbo"
```

## MCP Server
4 herramientas: `voicebox.speak`, `voicebox.transcribe`, `voicebox.list_captures`, `voicebox.list_profiles`

```bash
claude mcp add voicebox \
  --transport http \
  --url http://127.0.0.1:17493/mcp \
  --header "X-Voicebox-Client-Id: claude-code"
```

## Post-Processing Effects (8 efectos)
Pitch Shift, Reverb, Delay, Chorus/Flanger, Compressor, Gain, High-Pass Filter, Low-Pass Filter

## Casos de Uso para Mastermind
1. **TTS local** — alternativa a edge-cloud sin límites de API
2. **Voces personalizadas** — clonación de voz para agentes
3. **Integración MCP** — agentes AI hablan con voces clonadas
4. **Dictado global** — hotkey para dictar en cualquier app
5. **CI/CD voice notifications** — notificaciones por voz desde shell scripts
6. **Producción de contenido** — generación masiva de speech

## Stack Tecnológico
- Desktop App: Tauri (Rust)
- Frontend: React, TypeScript, Tailwind CSS, Zustand
- Backend: FastAPI (Python)
- Inference: MLX (Apple Silicon) / PyTorch (CUDA/ROCm/XPU/CPU)
- Database: SQLite

## Recursos
- GitHub: https://github.com/jamiepine/voicebox
- Docs: https://docs.voicebox.sh
- Licencia: MIT
