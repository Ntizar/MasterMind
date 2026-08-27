---
name: rvc-voice-conversion
description: RVC (Retrieval-based Voice Conversion) — conversión de voz en tiempo real con cloning de baja latencia y alta calidad.
category: media
---

# RVC — Retrieval-based Voice Conversion

## Qué es

RVC es un sistema de conversión de voz (voice conversion) que permite:
- **RVC v2** — última versión con mejor calidad y velocidad
- **Inference en tiempo real** — latencia <500ms
- **Zero-shot** — clones de voz sin fine-tuning
- **Comunidad enorme** — miles de modelos pre-entrenados disponibles

## Instalación

```bash
# Clonar y usar el launcher
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
cd Retrieval-based-Voice-Conversion-WebUI

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar WebUI
python infer.py
```

## Casos de uso para David

- **Voice cloning** — clonar su voz para narraciones
- **Doblaje** — mantener timbre consistente
- **Accesibilidad** — TTS con su voz
- **Streaming** — conversión en tiempo real para calls/live

## Pitfalls

- **GPU recomendada** — corre en CPU pero es lento
- Las muestras de referencia deben ser limpias
- Modelos grandes (100MB-1GB cada uno)
- La interfaz WebUI es la forma principal de uso
- Versiones incompatibles entre v1 y v2

## Referencias

- Repo: `github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI` (36K⭐)
- Docs: `https://github.com/RVC-Project`
- Modelos HuggingFace: búsqueda "RVC model" en HF
