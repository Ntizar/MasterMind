---
name: vibe-voice
description: Voice AI de Microsoft — síntesis y clonación de voz con IA de última generación.
version: "1.0.0"
tags: [voice, TTS, AI, cloning, Microsoft, synthesis]
---

# VibeVoice — Voice AI de Microsoft

## Resumen

Voice AI de Microsoft para síntesis y clonación de voz con IA de última generación. 49k⭐.

## Repo de referencia

- **GitHub:** `github.com/microsoft/VibeVoice`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install vibe-voice
# o clonar y configurar entorno
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice && pip install -r requirements.txt
```

## Uso Básico

```python
from vibe_voice import VibeVoice

# Síntesis de voz
vibe = VibeVoice()
audio = vibe.synthesize("Hola, ¿cómo estás?", voice="es-ES-Alvaro")
audio.save("saludo.mp3")

# Clonación de voz
vibe.clone_voice("referencia.wav", voice_id="mi_voz")
audio = vibe.synthesize("Texto con voz clonada", voice="mi_voz")
```

## Patrones Clave

1. **Síntesis natural:** Voz humana con entonación realista
2. **Clonación:** Clonar voz con pocos segundos de audio
3. **Multi-idioma:** Soporte para español, inglés y más
4. **Control emocional:** Ajustar tono y emoción de la voz
5. **Low latency:** Síntesis en tiempo real posible

## Integración con Mastermind

- Complementa `edge-tts` (más natural, más lento)
- Útil para TTS de alta calidad en dashboards
- Reemplaza `coqui-ai/TTS` para síntesis más natural
- Ideal para voicebox workflow

## Pitfalls

- **Recursos:** Requiere GPU para clonación en tiempo real
- **Latencia:** Más lento que edge-tts para síntesis simple
- **Calidad de referencia:** La clonación requiere audio limpio
- **Dependencias:** PyTorch pesado para instalar

## Referencias

- [GitHub: microsoft/VibeVoice](https://github.com/microsoft/VibeVoice)
