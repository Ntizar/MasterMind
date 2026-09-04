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

## Comparativa de alternativas

- **[fishaudio/fish-speech](https://github.com/fishaudio/fish-speech)** — Fish Speech 1.5 (Apache-2.0) es la referencia de TTS con clonación expresiva *zero-shot* en ~0.5 s de audio y salida en tiempo real; frente a otros clones de voz, destaca por calidad expresiva con muy poco audio de referencia.
