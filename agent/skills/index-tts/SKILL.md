---
name: index-tts
description: "Usa al clonar voz con Index-TTS V2 (multilenguaje)."
version: "2.0.0"
tags: [tts, index-tts, clonacion-voz, indextts, v2, local, transformadores]
related_skills: [f5-tts, chatterbox-tts, openvoice-voice-cloning, fish-speech-tts, gpt-sovits-tts]
---

# Index-TTS (V2) — TTS de alta fidelidad con clonado + multilenguaje

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 usaba `from index_tts import TTS` y métodos `load_reference/synthesize` **inexistentes**. El paquete se llama **`indextts`** y la API real es la clase `IndexTTS2.infer(...)`.

**Repo:** `https://github.com/index-tts/index-tts` (Python, ~24K⭐). Modelo/hub: IndexTTS-2.5 (multilenguaje: chino, inglés, japonés, español, árabe).

## When to Use

- Cuando pidas **clonar una voz nueva** con TTS de alta fidelidad y **multilenguaje**, sin datos masivos de la voz.
- Cuando necesites TTS más natural que el de edge/whisper para un protagonista o narración.

## Uso

El proyecto se gestiona con `uv`. Instalación:

```bash
uv run webui.py            # interfaz web
# o instalar como tool
uv tool install -e .
```

API en Python (paquete `indextts`):

```python
from indextts.infer_v2_5 import IndexTTS2
tts = IndexTTS2(cfg_path='checkpoints/config.yaml', model_dir='checkpoints', use_bf16=True)
tts.infer(
    spk_audio_prompt='voz.wav',   # voz de referencia
    text='Texto a sintetizar',
    lang='EN',                     # EN / ZH / JA / ES / AR...
    output_path='gen.wav',
    verbose=True,
)
```

*(El nombre del submódulo puede ser `infer_v2_5`, `infer_v2` o `infer` según la versión — comprobar el README del repo.)*

## Pitfalls

- El paquete Python es **`indextts`**, nunca `index_tts`. Un `from index_tts import TTS` es inventado y no compila.
- No existe `load_reference()` ni `synthesize()` — el método es `infer(...)`.
- La doc del repo promociona `uv`; `pip install -e .` no es la vía oficial.

## Verificación

- Clonar con la voz de referencia y `texto` en español; comprobar que el audio de salida mantiene el timbre y suena natural en el idioma elegido.
