---
name: gpt-sovits-tts
description: Clona una voz con 1 min de audio y genera TTS por API.
version: 1.0
tags: [tts, voice-cloning, few-shot, sovits, audio, api]
---

# GPT-SoVITS — TTS few-shot con clonación de voz

## Qué es

Framework TTS de RVC-Boss (61K⭐) que entrena un buen modelo de voz con solo **1 minuto de audio** de referencia. Combina GPT para prosodia + SoVITS para timbre. MIT.

- **Few-shot cloning** — 1 min de audio limpio basta (mejor con 5-10 min)
- **Multi-idioma** — zh, en, ja, ko, yue y **español** soportado
- **WebUI integrada** — entrenamiento (UVR5 → Whisper → dataset → fine-tune) y síntesis
- **API FastAPI** — `api_v2.py` para integración en servicios

## Instalación

```bash
git clone https://github.com/RVC-Boss/GPT-SoVITS
cd GPT-SoVITS
# Windows: descargar el paquete preintegrado (integrated package) de releases
# O desde cero (Python 3.10-3.12):
conda create -n gptsovits python=3.10 && conda activate gptsovits
pip install -r extra-req.txt --no-deps
pip install -r requirements.txt
```

## Uso

### WebUI
```bash
python webui.py   # abre Gradio en :9874
```
Flujo: transcibir muestras con Whisper → listar dataset → SoVITS + GPT fine-tune → inferencia.

### API (inferencia sin reentrenar)
```bash
python api_v2.py -a 0.0.0.0 -p 9880
curl "http://localhost:9880/tts?text=Hola+mundo&text_lang=es&ref_audio_path=ref.wav&prompt_lang=es"
```
POST `/tts` con JSON `{text, text_lang, ref_audio_path, prompt_text, prompt_lang, speed_factor}` → audio WAV streaming.

## Casos de uso

- Voz personalizada para informes TTS (alternativa a Álvaro Neural)
- Doblaje y audiolibros con voz consistente
- Comparativa con otros TTS locales del ecosistema (F5-TTS, Fish Speech, OpenVoice, Index-TTS, Chatterbox, RVC)

## Pitfalls

- **Audio de referencia**: debe ser limpio (sin música/ruido), 3-10 s en inferencia; usar UVR5 para limpiar antes de entrenar
- Modelos base GPT/SoVITS preentrenados se descargan aparte (HuggingFace lj1995/GPT-SoVITS) — la primera ejecución no funciona sin ellos
- GPU recomendada para entrenamiento (fine-tune ~10 min en GPU media); inferencia CPU posible pero lenta
- `text_lang=es` funciona pero la calidad es menor que zh/en/ja — considerar fine-tune con muestras en español
- Windows: usar el paquete integrado evita la mayoría de problemas de dependencias (numba, ctranslate2)

## Verificación

```bash
curl http://localhost:9880/tts?text=prueba&text_lang=es&ref_audio_path=ref.wav&prompt_lang=es -o test.wav
# test.wav debe contener audio WAV reproducible
```

## Referencias

- Repo: github.com/RVC-Boss/GPT-SoVITS
- Guía EN: rentry.co/GPT-SoVITS-guide
- Relacionados: `f5-tts`, `fish-speech-tts`, `openvoice-voice-cloning`, `index-tts`, `chatterbox-tts`, `rvc-voice-conversion`
