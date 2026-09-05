---
name: video-gen-from-topic
description: "Usa a generar short-videos desde un tema con MoneyPrinterTurbo."
version: "2.0.0"
tags: [video, ai, automation, tts, moviepy, short-video, monetizacion]
related_skills: [video-gen-from-topic, video-processing, browser-local-tools, product-price-monitor]
---

# Video Generation from Topic — MoneyPrinterTurbo Pattern

> ⚠️ Actualizado 2026-09-05: stars reales **120.8K⭐** (no 88K), repo activo (push 2026-09-05), MIT. Llama a guion vía LLM(L): además de OpenAI/Claude/Gemini/Azure/DashScope/G4F, el README actual integra **Kimi K3**, **volcengine GLM-5.3 / DeepSeek / MiniMax / Doubao**. Tema/keyword → guion → stock → voz → subtítulos → BGM → HD short en un clic.

**Repo:** `https://github.com/harry0703/MoneyPrinterTurbo` (Python, MIT, ~120.8K⭐, activo).

## Qué aporta

- Flujo 100% automático: **tema → guion (LLM) → material (Pexels/Pixabay stock) → voz (edge-tts gratis) → subtítulos → BGM → vídeo HD corto**.
- Web UI (Streamlit) + API REST (FastAPI). Docker + Redis (cola de tareas) para escalar.
- Composición con MoviePy. Sin API keys de pago obligatorias (edge-tts); solo el LLM de guion puede necesitar una (o servicio local/NaN).

## Patrones clave

1. **Topic-driven generation** — el input es un tema/keyword; el sistema produce todo.
2. **Multi-LLM fallback chain** — intenta el LLM principal, si falla pasa al siguiente; añade los del README (Kimi K3 / GLM-5.3 / DeepSeek).
3. **Edge TTS gratis** — `edge-tts` en lugar de APIs de pago (ideal sin presupuesto).
4. **MoviePy composition** — clips + imágenes + texto superpuesto + audio.
5. **Web UI + API dual** — Streamlit para interactuar, FastAPI para automatizar en lote.

## 🪙 MONETIZACIÓN (el ángel)

El poder real de MoneyPrinterTurbo **no es el vídeo, es el alcance barato**. Guion con reserva: el RPM de YouTube/TikTok Shorts es bajo (~$0,05–0,15/1000 views), así que **no monetiza el vídeo, monetiza lo que está alrededor**:

- **A. Afiliación** (encaja con **Kit72h**): shorts de "gadget/amazon finds" + link afiliado en descripción/CTR. El short hace de gancho de reach, Kit72h hace la conversión. Requiere **disclosure** del enlace afiliado y cumplir políticas de la plataforma.
- **B. Funnel a producto propio**: shorts de nicho → newsletter/web/lead magnet. Monetiza por lista, no por views.
- **C. Agencia (vender el servicio)**: "te hago N shorts/mes para tu marca" — vendes el *producto*, no tu tiempo. Esto es lo que deja dinero real.
- **D. Nichos con RPM decente**: finanzas, tech, b2b → más RPM y patrocinios que el entretenimiento genérico.

**Estrategia recomendada para David:** nicho de gadgets/tech utility → shorts virales de Amazon finds → **funnel a Kit72h** (afiliación) + ofrecer el servicio a marcas. Mass-produce con MoneyPrinterTurbo, cura/concilia el guion con la voz de Álvaro (`es-ES-AlvaroNeural`) para no sonar a bot.

## Comparativa de alternativas

- **hradec/ComfyUI-HR-Endless-Sampler** — muestreo por chunks de latents + LLM que planifica; vídeo "infinito" coherente (nodo de generación).
- **mutonby/openshorts** — recorte vertical de podcast (apilar speakers + captions, crop con face-tracking) en Docker; útil para pulir/reencuadrar.
- **shorts automáticos de plataforma** (YouTube "Shorts/Script IA") — menos control, pero cero código.

## Pitfalls

- El LLM de guion puede costar si no se usa uno local/grátis; usa edge-tts para voz (gratis) y un LLM barato.
- Vídeo genérico de stock + voz de bot = contenido "muy fácil de ignorar". La voz de Álvaro y un guion curado son lo que diferencia.
- Licencias: el stock (Pexels/Pixabay) permite uso comercial; respetar términos (sin reclamo de patrocinio).

## Verificación

- Tema → config LLM → generar short HD; comprobar voz (Álvaro), subtítulos y que el montaje rinde en vertical (9:16) para Shorts/Reels/TikTok.
