---
name: chatterbox-tts
description: "Usa al clonar voz con Chatterbox Turbo de Resemble."
version: "2.0.0"
tags: [tts, chatterbox, clonacion-voz, open-source, local, resemble, turbo]
related_skills: [f5-tts, index-tts, openvoice-voice-cloning, fish-speech-tts, gpt-sovits-tts]
---

# Chatterbox (Resemble AI) — TTS open-source con clonado y emoción

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 decía `pip install chatterbox` + `from chatterbox import TTS` (`load_voice`/`synthesize(emotion=...)`), "API REST" y "requiere API key de Resemble". **Falso.** El paquete PyPI es **`chatterbox-tts`**; la API real es `ChatterboxTurboTTS.generate(...)`; corre **100% en local, sin API key ni REST**.

**Repo:** `https://github.com/resemble-ai/chatterbox` (MIT, Python, ~26K⭐). El servicio comercial de resemble.ai es un producto aparte — el modelo open-source no lo necesita.

## When to Use

- Cuando pidas **clonar una voz** con un TTS open-source de alta calidad que funcione local y produzca emociones/sonidos con tags de paralenguaje.
- Como vía rápida de voz clonada **sin depender de ningún proveedor de pago**.

## Uso

```bash
pip install chatterbox-tts
```

El modelo Turbo (rápido, bueno) es el recomendado:

```python
from chatterbox.tts_turbo import ChatterboxTurboTTS
model = ChatterboxTurboTTS.from_pretrained(device='cuda', nano=...)   # nano usaba modelo 134M
# Generar con voz de referencia
wav = model.generate(
    text='Texto a decir',
    audio_prompt_path='voz.wav',   # voz de referencia (clonado)
)
```

- **Emociones/sonidos** no van por un parámetro `emotion=`: se expresan con **tags de paralenguaje** en el texto (`[laugh]`, `[cough]`, etc.).
- La doc real está en el README del repo, **no** en `docs.resemble.ai` (eso es la API comercial).

## Pitfalls

- Instalar **`chatterbox-tts`**, no `chatterbox`.
- No hay API REST ni embargo de key: es un modelo local. Todo lo que hable de "API key de Resemble para uso completo" es inventado.
- Metadatos/embeddings de voz: `from_pretrained` descarga los checkpoints; `nano` es una variante pequeña.

## Verificación

- Cargar con `device='cuda'`, generar con `audio_prompt_path` de la voz de David y comprobar que el clon mantiene el timbre. Probar un tag `[laugh]` para ver la expresión.
