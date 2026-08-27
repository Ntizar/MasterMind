---
name: open-source-voice-studio
version: "1.0.0"
description: "Estudio de voz AI open-source local-first — clonación de voz, dictado, creación. Inspirado en jamiepine/voicebox (⭐38K)."
tags: [voice, tts, stt, ai, audio, open-source, local-first]
---

# Estudio de Voz AI Open-Source

## Resumen

[voicebox](https://github.com/jamiepine/voicebox) (⭐38K) es un estudio de voz AI open-source local-first. Clona voces, dicta texto, y crea contenido de audio sin enviar datos a la nube.

## Cuándo usar

- Clonación de voz con pocos segundos de audio
- Dictado de texto a voz natural
- Creación de contenido de audio local
- Asistente de voz con voz personalizada

## Stack

| Componente | Tecnología | Función |
|-----------|-----------|---------|
| TTS | Coqui TTS / Piper | Texto a voz |
| STT | Whisper / Vosk | Voz a texto |
| Clonación | XTTS / F5-TTS | Clonar voz con audio corto |
| UI | Web (React) | Interfaz de estudio |
| Backend | Node.js/Python | API local |

## Patrón de uso

```python
# Clonación de voz con XTTS (few-shot)
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
# Clonar voz con 3 segundos de audio
tts.tts_to_file(
    text="Hola, soy una voz clonada",
    speaker_wav="reference_voice.wav",
    language="es",
    file_path="output.wav"
)

# STT con Whisper
import whisper
model = whisper.load_model("base")
result = model.transcribe("input.wav", language="es")
print(result["text"])
```

```javascript
// API local para el estudio de voz
const express = require('express');
const app = express();

app.post('/api/tts', async (req, res) => {
  const { text, voiceId } = req.body;
  // Llamar a TTS local
  const audio = await generateTTS(text, voiceId);
  res.json({ audio: audio.toString('base64') });
});

app.post('/api/stt', async (req, res) => {
  const audio = Buffer.from(req.body.audio, 'base64');
  // Llamar a Whisper local
  const text = await transcribe(audio);
  res.json({ text });
});

app.listen(3000);
```

## Pitfalls

- **XTTS vs Piper:** XTTS = mejor calidad, más lento. Piper = más rápido, calidad decente.
- **GPU:** Clonación de voz necesita GPU. Sin GPU, usar Piper (CPU-friendly).
- **Audio reference:** Para clonación, 3-10s de audio limpio sin ruido de fondo.
- **Idioma:** XTTS soporta multi-idioma. Piper necesita modelo por idioma.
- **Latencia:** TTS local tiene latencia < 500ms. Cloud TTS = 1-3s.

## Referencias

- voicebox: https://github.com/jamiepine/voicebox
- Coqui TTS: https://github.com/coqui-ai/TTS
- Whisper: https://github.com/openai/whisper
- Piper: https://github.com/rhasspy/piper

---

**Hecho con ❤️ por David Antizar**
