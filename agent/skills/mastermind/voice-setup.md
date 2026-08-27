---
name: voice-setup
description: "Configuración y gestión de STT (faster-whisper) y TTS (Edge TTS) para audio bidireccional en Mastermind"
version: 1.0.0
author: Mastermind
tags: [audio, stt, tts, voice, telegram]
---

# Voice Setup

## STT (Speech-to-Text) — Escuchar al usuario

### Configuración
```yaml
stt:
  enabled: true
  provider: local
  local:
    model: tiny   # tiny (39MB) | base (142MB) | small | medium | large-v3
```

### Instalación
```bash
source /opt/hermes/.venv/bin/activate
uv pip install faster-whisper
```

### Notas
- Modelo `tiny` es suficiente para 2GB RAM. Primer arranque descarga modelo (~39MB).
- El gateway evaluó `_HAS_FASTER_WHISPER` al arrancar. Si se instala después, **hay que reiniciar**.
- STT es **100% local** — los audios nunca salen del servidor.

## TTS (Text-to-Speech) — Hablar al usuario

### Configuración
```yaml
tts:
  provider: edge
  edge:
    voice: es-ES-AlvaroNeural
```

### Edge TTS — Voces españolas disponibles
| Voz | País | Género |
|-----|------|--------|
| es-ES-AlvaroNeural | España | Masculino ✅ activa |
| es-ES-ElviraNeural | España | Femenino |
| es-MX-JorgeNeural | México | Masculino |
| es-AR-TomasNeural | Argentina | Masculino |
| es-CO-GonzaloNeural | Colombia | Masculino |
| es-CL-LorenzoNeural | Chile | Masculino |
| es-VE-SebastianNeural | Venezuela | Masculino |
| es-US-AlonsoNeural | US Latino | Masculino |

### Cambiar voz
```bash
# Ver todas las voces
source /opt/hermes/.venv/bin/activate && edge-tts --list-voices | grep "es-"

# En config.yaml:
# tts.edge.voice: es-ES-AlvaroNeural
```

## Comportamiento
- `voice.auto_tts: false` → solo responde en audio cuando el usuario lo pide
- El usuario manda un voice message → STT transcribe → respondo con TTS si pide audio

## Reinicio del gateway
```bash
kill -TERM 1   # Kubernetes revive automáticamente
# Después de reinicio, restaurar STT/TTS en config.yaml si se reseteó
```