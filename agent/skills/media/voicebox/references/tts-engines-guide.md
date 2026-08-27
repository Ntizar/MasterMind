# Guía de Motores TTS y Voice AI (Descubiertos 2026-07-07)

Motores adicionales descubiertos en GitHub Stars Explorer batch nocturno. No incluidos en Voicebox por defecto.

## OpenVoice (⭐37K)
- **URL:** https://github.com/myshell-ai/OpenVoice
- **Desc:** Voice cloning instantáneo por MIT/MyShell
- **Features:** Tone color cloning, style control (emoción, acento, ritmo), zero-shot cross-lingual
- **V2:** Multi-idioma nativo (EN, ES, FR, CN, JP, KO), MIT License, mejor calidad
- **Uso:** `pip install openvoice-app`
- **Ideal para:** Voice cloning rápido, prototipado, integraciones donde no se necesita desktop app
- **License:** MIT

## Fish Speech (⭐31K)
- **URL:** https://github.com/fishaudio/fish-speech
- **Desc:** TTS SOTA basado en VALL-E/VITS architecture
- **Features:** Voice cloning expresivo, multi-idioma, control de emoción y entonación
- **Uso:** `pip install -e .` desde source
- **Ideal para:** Generación de speech con alta naturalidad, voice cloning expresivo
- **License:** NOASSERTION (verificar antes de uso comercial)
- **GPU:** Necesaria para inferencia práctica

## IndexTTS (⭐22K)
- **URL:** https://github.com/index-tts/index-tts
- **Desc:** TTS industrial de nivel producción
- **Features:** **Control preciso de duración** (único), control emocional, zero-shot
- **Ideal para:** Sincronización audio-video, aplicaciones que requieren timing exacto del audio
- **License:** NOASSERTION (verificar antes de uso comercial)
- **Diferenciador:** Único en control de duración del speech sintetizado

## RVC - Retrieval-based Voice Conversion (⭐36K)
- **URL:** https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
- **Desc:** Conversión de voz (NO TTS) — transforma voz de A en voz de B
- **Features:** Entrenamiento con 10min de audio, webui Gradio, retrieval-based
- **Uso:** `python infer/webui.py`
- **Ideal para:** Dubbing, covers de canciones, voice conversion (no generación desde texto)
- **GPU:** Necesaria (6GB+ VRAM)

## Comparativa Rápida

| Motor | TTS | Voice Conversion | Voice Cloning | Multi-idioma | Diferenciador |
|-------|-----|-----------------|---------------|--------------|---------------|
| Qwen3-TTS (Voicebox) | ✅ | ❌ | ✅ | 10 idiomas | Instruct support |
| Chatterbox (Voicebox) | ✅ | ❌ | ✅ | 23 idiomas | Paralinguistic tags |
| Kokoro (Voicebox) | ✅ | ❌ | Preset | 8 idiomas | CPU realtime |
| OpenVoice | ✅ | ❌ | ✅ | 6 idiomas | Tone color cloning |
| Fish Speech | ✅ | ❌ | ✅ | Multi | VALL-E arch, expresivo |
| IndexTTS | ✅ | ❌ | ✅ | Cross-lingual | **Control de duración** |
| RVC | ❌ | ✅ | ✅ | ❌ | **Voice conversion** |
