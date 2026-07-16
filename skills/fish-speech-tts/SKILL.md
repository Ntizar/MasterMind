---
name: fish-speech-tts
description: Fish Speech — modelo TTS de última generación con clonación de voz zero-shot y alta calidad.
category: media
---

# Fish Speech — TTS de Nueva Generación

## Qué es

Fish Speech de Fish Audio es un sistema TTS que ofrece:
- **Zero-shot cloning** — clonar voz con muestras cortas
- **Alta calidad** — audio natural y expresivo
- **Multilingüe** — soporte para múltiples idiomas
- **Open source** — completamente abierto

## Instalación

```bash
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech
pip install -e .
```

## Uso básico

```python
# Generar audio con voz clonada
# Usar el CLI o API proporcionada
fish-speech --text "Texto a sintetizar" --reference "reference.wav" --output "output.wav"
```

## Casos de uso

- **Narración personalizada** — voz de David para contenido
- **Doblaje** — mantener timbre consistente
- **Prototipado rápido** — generar audio para tests

## Pitfalls

- Requiere GPU para inference rápida
- Modelos grandes (varios GB)
- La configuración inicial puede ser compleja
- Depende de modelos pre-entrenados de HuggingFace

## Referencias

- Repo: `github.com/fishaudio/fish-speech` (31K⭐)
- HuggingFace: `https://huggingface.co/fishaudio`
