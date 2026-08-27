---
name: chatterbox-tts
description: Chatterbox (Resemble AI) — TTS de alta calidad con clonación de voz y control emocional.
category: media
---

# Chatterbox — TTS de Resemble AI

## Qué es

Chatterbox es un sistema TTS de Resemble AI que ofrece:
- **Clonación de voz** — zero-shot cloning de alta fidelidad
- **Control emocional** — ajustar tono emocional de la voz
- **Alta calidad** — audio natural para producción
- **API REST** — fácil integración

## Instalación

```bash
pip install chatterbox
# O usar directamente la API
```

## Uso básico

```python
from chatterbox import TTS

tts = TTS()

# Clonar voz y sintetizar
tts.load_voice("reference.wav")
tts.synthesize("Texto a sintetizar", "output.wav", emotion="happy")
```

## Casos de uso

- **Producción de audio** — contenido profesional
- **Doblaje** — mantener voz consistente
- **Accesibilidad** — TTS personalizado

## Pitfalls

- Requiere API key de Resemble AI para uso completo
- Modelo grande, requiere buen hardware
- La calidad del cloning depende de la referencia
- Algunos features requieren plan de pago

## Referencias

- Repo: `github.com/resemble-ai/chatterbox` (25K⭐)
- Docs: `https://docs.resemble.ai`
