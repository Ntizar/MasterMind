---
name: f5-tts
description: "Usa al hacer TTS clonado con F5-TTS (src layout)."
version: "2.0.0"
tags: [tts, f5-tts, clonacion-voz, src, huggingface, local, zero-shot]
related_skills: [index-tts, chatterbox-tts, openvoice-voice-cloning, fish-speech-tts, gpt-sovits-tts]
---

# F5-TTS — texto-a-voz con clonado (zero-shot)

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 usaba `from f5_tts.infer.api import synthesize` — **inexistente**. El paquete vive en `src/`; la API real es la clase `F5TTS.infer(...)` (o el CLI).

**Repo:** `https://github.com/SWivid/F5-TTS` (MIT, Python, ~15K⭐). Modelo en HF: `SWivid/F5-TTS`.

## When to Use

- Cuando pidas **clonar una voz** con un TTS open-source de alta calidad y velocidad (zero-shot, con una sola referencia de audio).
- Como alternativa ligera y rápida en la cadena de voces de David.

## Uso

El repo usa **layout `src/`** (`src/f5_tts/`). Instalación válida: `pip install -e .` (pyproject.toml en raíz).

API Python:

```python
from f5_tts.api import F5TTS        # clase, no función de módulo
tts = F5TTS()
tts.infer(...)                       # parámetros por el README real
```

CLI:

```bash
python -m f5_tts.infer.infer_cli     # o el binario f5-tts-infer tras instalar -e .
```

*(No existe `f5_tts/infer/api.py` — `f5_tts/infer/` contiene `infer_cli.py`, `infer_gradio.py`, `utils_infer.py`, `speech_edit.py`.)*

## Pitfalls

- Import correcto: `from f5_tts.api import F5TTS`; **no** `from f5_tts.infer.api import synthesize`.
- El paquete no está en la raíz: está en `src/f5_tts/`.
- Parámetros de `F5TTS.infer(...)`: ver el README — no coinciden con `ref_audio/ref_text` de la v1.

## Verificación

- Instalar con `pip install -e .`, llamar `F5TTS().infer(...)` con una referencia de audio y comprobar el clon.
