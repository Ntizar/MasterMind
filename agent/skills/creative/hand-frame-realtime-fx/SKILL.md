---
name: hand-frame-realtime-fx
version: "1.0.0"
description: "Use al crear demos de cámara y manos IA en tiempo real."
tags: [mediapipe, hand-tracking, webcam, realtime, fal, webrtc, canvas, browser-demo]
---

# Hand-Frame Realtime FX — Ventana IA en tiempo real con las manos

> Patrón destilado de `blendi-remade/finger-frame-effect-fal` (27⭐, JS, agosto 2026).

## Qué es

Página estática **sin build y sin backend**: al hacer el gesto "marco" con dos manos ante
la webcam, el área entre los dedos se convierte en una ventana a un mundo IA generado
**en tiempo real** (modelos: Decart Lucy 2.5 / FLUX.2 klein vía fal, BYO API key).

El valor no es la demo — es la **arquitectura de dos velocidades** y el pipeline de
tracking robusto, ambos reutilizables para cualquier tool de navegador con cámara
(preference de David: espectáculo visual primero).

## El patrón central: tracking local rápido + generación remota lenta

- El tracking de manos, la máscara del quad y el contorno animado corren **locales a
  framerate de pantalla**. La generación IA va a su ritmo (5-8 fps o menos).
- **Compositing:** la salida de la IA se dibuja alineada a pantalla y se revela SOLO a
  través del quad tracked con `canvas clip` + outline discontinuo y puntos de esquina.
- Clave conceptual: **el modelo nunca sabe que existen los dedos** — no recorta, no
  enmascara, restiliza todo el frame. La costura son los dedos tracked localmente →
  el efecto sigue siendo impecable aunque el modelo vaya por debajo del framerate.
- Sin key de fal: fallback a filtro local hue-shift (la demo nunca queda muerta).

## Pipeline de tracking de quad con manos (audited, del README original)

1. MediaPipe **Hand Landmarker**, dos manos por frame.
2. Esquinas ordenadas **anatómicamente** (dedos cruzados → render "corbata", no quad roto).
3. Gates de **spread y área con histéresis** (evita flapping gesto/no-gesto).
4. **Rechazo de teletransporte** (saltos > umbral se descartan).
5. **Suavizado adaptativo a velocidad** + **dropout hold** (mantiene última pose unos
   frames si la mano se pierde) + **presence fade** (aparición/desaparición suave).

Este pipeline vale igual para cualquier gesto→máscara en Canvas 2D sin IA.

## Integración con fal realtime (dos backends, dos modos)

- **Lucy 2.5 (v2v true realtime):** sesión WebRTC — sube la cámara, devuelve el stream
  restilizado motion-locked. Cambio de estilo = mensaje de prompt por el WebSocket de
  signaling (SIN reconectar). Retry con backoff si hay capacidad arriba.
- **FLUX.2 klein (edición por frames):** JPEG espejado 768×768 cada 125 ms con
  `output_feedback_strength: 0.9` + seed fijo → **coherencia temporal** (cada frame se
  siembra con un poco del output anterior). El 16:9 se **aplasta a cuadrado** (no
  recorta): la distorsión se cancela en pantalla y el marco puede estar en cualquier sitio del plano.
- Facturación: Lucy se cobra por sesión conectada, klein por frame. **Nunca dejar una
  sesión Lucy abierta** — desconectar al cambiar de estilo o cerrar tab.
- Prompts redactados por backend (Lucy: "Change the style of the video to…" con
  detalles visuales concretos; klein: "Turn this into…").

## Truco de testabilidad que copiar SIEMPRE

`?demo` → feed sintético con landmarks falsos: ejercita tracking + compositing **sin
cámara y sin llamadas API**. Para cualquier herramienta de webcam: modo demo de datos
sintéticos + coste cero.

## Familia finger-frame (4 generaciones, por latencia)

| Variante | Técnica | Latencia |
|---|---|---|
| finger-frame-effect (sophiamyang) | Canvas 2D local (Van Gogh, glitch) | ninguna |
| …-effect-ai | Gemini (offline video edit), vídeo grabado | minutos |
| …-effect-lucy | Decart Lucy vía API directa | casi realtime |
| este repo | Lucy + klein vía `@fal-ai/client` | casi realtime |

## Pitfalls

- Repo sin licencia definida → usar como REFERENCIA de patrón, no copiar código.
- La key de fal vive solo en el navegador (localStorage opcional) y se canjea por
  session tokens de corta vida — patrón BYOK correcto, respetarlo en tools propias.
- Hand tracking con dos manos se degrada con oclusión/luces malas: los gates con
  histéresis + dropout hold existen precisamente por eso — no quitarlos al podar código.
- klein es frame-por-frame: la geometría "sueña" (dreamy). Para motion-lock real (que
  el parpadeo del usuario aparezca dentro de la ventana) hace falta Lucy/WebRTC.

## Verificación

1. Con `?demo`: el quad sigue las landmarks sintéticas a framerate de pantalla, sin latencia.
2. Cambiar de estilo no reconecta la sesión (DevTools → el WebSocket sigue abierto).
3. Al cerrar la pestaña no queda sesión Lucy facturando (ver dashboard de fal).
4. Ocluir una mano 1 s → el marco debe mantenerse (dropout hold) y desvanecer tras el umbral.

## Referencias

- Repo: https://github.com/blendi-remade/finger-frame-effect-fal
- Docs modelos: fal.ai/models/decart/lucy-2-5/realtime · fal.ai/models/fal-ai/flux-2-klein-realtime/realtime
- Explorado por stars-explorer: 2026-09-03
- Relacionados: `tools/browser-local-tools`, `computer-vision/openpose-pose-estimation`, `vision/onnx-webgpu-inference`
