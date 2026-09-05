---
name: openvoice-voice-cloning
description: "Usa al clonar voz con OpenVoice V2 y tono color."
version: "2.0.0"
tags: [tts, openvoice, clonacion-voz, tone-color, melotts, voice, local]
related_skills: [f5-tts, index-tts, chatterbox-tts, fish-speech-tts, gpt-sovits-tts, vibe-voice]
---

# OpenVoice (V2) — clonado por transferencia de timbre

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): stars y docs desfasadas, la afirmación "corre en CPU, sin GPU" era matizable y la firma del `ToneColorConverter` estaba imprecisa. Corregido.

**Repo:** `https://github.com/myshell-ai/OpenVoice` (MIT, Python, ~37K⭐). Docs: `https://research.myshell.ai/open-voice`.

## When to Use

- Cuando pidas **clonar un timbre** ("tone color") sin entrenar: con OpenVoice transfieres el color de voz a un TTS base.
- Para cambiar el timbre de un texto ya sintetizado sin re-entrenar.

## Qué es

Sistema de **conversión de color de voz** (V2): no genera el texto tú mismo, sino que re-colorea la voz de un TTS base. La cadena V2 usa **MeloTTS** como TTS base (instalar aparte) y el **tone-color converter** para el timbre.

- En la práctica el pipeline completo **se usa con GPU** (MeloTTS + converter); el converter en sí es ligero, pero no es estrictamente CPU-only para uso normal.
- **No necesita API key** — es open-source local.

## Uso

```python
from openvoice.api import ToneColorConverter
from openvoice.se_extractor import se_extractor  # según versiones

# Firma real del converter (checkpoints V2)
converter = ToneColorConverter(
    'checkpoints_v2/converter.pth',
    config_path='checkpoints_v2/config.json'
)
# extraer embed de la voz de referencia y convertir
```

*(Instalar MeloTTS aparte: `pip install -q MeloTTS` — es la dependencia base de V2.)*

## Pitfalls

- La doc NO está en `docs.myshell.com`; la referencia es `research.myshell.ai/open-voice`.
- `ToneColorConverter('checkpoint_v1')` es impreciso: firma completa `('checkpoints_v2/converter.pth', config_path='checkpoints_v2/config.json')`.
- No confundir con un TTS end-to-end: OpenVoice **recolorea** una voz; el texto lo sintetiza el TTS base.

## Verificación

- Cargar `ToneColorConverter` con la ruta V2, extraer embed de una voz y convertir un clip; comprobar que el timbre cambia manteniendo texto y prosodia.
