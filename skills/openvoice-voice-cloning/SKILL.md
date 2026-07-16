---
name: openvoice-voice-cloning
description: OpenVoice — cloning de voz instantánea con transferencia de habla multi-idioma y control granular del estilo.
category: media
---

# OpenVoice — Voice Cloning Instantáneo

## Qué es

OpenVoice de MyShell es un sistema de voice cloning que permite:
- **Clonación instantánea** — una muestra de audio de 3 segundos es suficiente
- **Transferencia multi-idioma** — clonar voz y hablar en idiomas diferentes
- **Control granular** — ajustar acento, entonación, estilo emocional
- **Ligero** — corre en CPU, no necesita GPU

## Instalación

```bash
# Clonar y instalar
git clone https://github.com/myshell-ai/OpenVoice.git
cd OpenVoice
pip install -e .

# Descargar modelos de checkpoint
# https://huggingface.co/myshell-audio/OpenVoice
```

## Uso básico

```python
from openvoice import se_extractor
from openvoice.api import ToneColorConverter

# 1. Extraer speaker embedding de la referencia
se = se_extractor.get_se("reference.wav", save_path="embedded.pt")

# 2. Convertir voz
converter = ToneColorConverter('checkpoint_v1')
converter.to("source.wav", "output.wav", se_path="embedded.pt")
```

## Control de estilo

```python
# Cambiar tono, velocidad, emoción
# Usar tone color checkpoints predefinidos
# https://github.com/myshell-ai/OpenVoice/tree/main/checkpoints_v2
```

## Casos de uso para David

- **TTS personalizado** — clonar su propia voz para narraciones
- **Accesibilidad** — generar voz con su timbre para contenido
- **Doblaje** — mantener la voz del actor en traducciones
- **Contenido multimodal** — audio + video con voz consistente

## Pitfalls

- La calidad depende de la muestra de referencia (audio limpio, sin ruido)
- No funciona bien con voces con acento muy fuerte en la referencia
- Los checkpoints v2 son mejores que v1
- Requiere Python 3.9+
- El proceso de clonación es ~10-30 segundos por muestra de 5 segundos

## Referencias

- Repo: `github.com/myshell-ai/OpenVoice` (36K⭐)
- Docs: `https://docs.myshell.com`
- Modelos: `https://huggingface.co/myshell-audio/OpenVoice`
