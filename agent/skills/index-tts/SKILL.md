---
name: index-tts
description: Index-TTS — sistema de texto-a-voz de alta fidelidad con clonación de voz y control de prosodia.
category: media
---

# Index-TTS — Text-to-Speech de Alta Fidelidad

## Qué es

Index-TTS es un sistema TTS de última generación que ofrece:
- **Clonación de voz ultra-realista** — calidad comparable a soluciones comerciales
- **Control de prosodia** — ajustar ritmo, entonación, énfasis
- **Zero-shot** — clonar con muestras cortas (3-5 segundos)
- **Multi-idioma** — soporte para varios idiomas

## Instalación

```bash
git clone https://github.com/index-tts/index-tts.git
cd index-tts
pip install -e .
```

## Uso básico

```python
from index_tts import TTS

tts = TTS()

# Clonar voz y sintetizar
tts.load_reference("reference.wav", "reference_text.txt")
tts.synthesize("Texto a sintetizar con la voz clonada", "output.wav")
```

## Casos de uso

- **Voz personalizada** para narraciones de David
- **Doblaje automatizado** manteniendo timbre consistente
- **Accesibilidad** TTS natural y personalizable

## Pitfalls

- Modelo grande, requiere buen hardware para inference rápida
- La calidad del cloning depende de la muestra de referencia
- Audio limpio sin ruido de fondo es obligatorio
- Requiere Python 3.9+

## Referencias

- Repo: `github.com/index-tts/index-tts` (21K⭐)
