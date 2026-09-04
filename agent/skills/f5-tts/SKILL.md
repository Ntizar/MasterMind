---
name: f5-tts
description: F5-TTS — modelo de texto-a-voz de alta calidad con zero-shot cloning y sin necesidad de fine-tuning.
category: media
---

# F5-TTS — Text-to-Speech de Nueva Generación

## Qué es

F5-TTS es un modelo TTS (Text-to-Speech) que ofrece:
- **Zero-shot cloning** — clonar voz con 3-10 segundos de referencia
- **Alta calidad** — audio natural comparable a modelos comerciales
- **Inference rápida** — más rápido que modelos anteriores
- **Multi-idioma** — soporte para inglés, chino y más

## Instalación

```bash
# Clonar y instalar
git clone https://github.com/SWivid/F5-TTS.git
cd F5-TTS
pip install -e .

# Descargar modelos pre-entrenados
# https://huggingface.co/SWivid/F5-TTS
```

## Uso básico

```python
from f5_tts.infer.api import synthesize

# Sintetizar con referencia de voz
synthesize(
    text="Hola, esto es una prueba de F5-TTS",
    ref_audio="reference.wav",
    ref_text="texto de la referencia",
    output_path="output.wav"
)
```

## Casos de uso

- **Narración automática** — generar voz para videos, podcasts
- **Doblaje** — mantener voz consistente en traducciones
- **Accesibilidad** — TTS personalizado para contenido

## Pitfalls

- Requiere GPU para inference rápida (pero corre en CPU)
- La calidad del cloning depende de la muestra de referencia
- Modelos grandes (~2GB cada uno)
- Requiere Python 3.10+

## Referencias

- Repo: `github.com/SWivid/F5-TTS` (14K⭐)
- HuggingFace: `https://huggingface.co/SWivid/F5-TTS`

## Comparativa de alternativas

- **[SWivid/F5-TTS](https://github.com/SWivid/F5-TTS)** — se puede servir vía *Hugging Face Space* para demo instantánea sin GPU; incluye E2-TTS como variante Flat-UNet, fácil de probar sin montar inferencia local.
