---
name: deep-live-cam-face-swap
version: "1.0.0"
description: "Face swap y deepfake de video en tiempo real con una imagen."
tags: [deepfake, face-swap, realtime, computer-vision, media]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [deepfake, face-swap, realtime, cv]
    related_skills: [openpose-pose-estimation, fast-alpr, gpt-sovits-tts]
---
# Deep-Live-Cam — Face Swap en Tiempo Real

## Resumen
Sistema de face swap y deepfake de video en tiempo real con un solo clic y una única imagen. Pensado para la industria de media generada por IA (animar personajes, contenido, diseño de moda). Incluye controles éticos y de contenido.

## Uso (del README)
- Repo: `hacksider/Deep-Live-Cam`, versión `2.1.6`.
- **Prebuilds optimizados por hardware** (Windows, Mac Silicon, CPU, NVIDIA, AMD) disponibles en https://deeplivecam.net/index.php/quickstart; "Ultimate" incluye 30+ extras exclusivos.
- Demo GIF: `media/demo.gif`.

## Patrones / Arquitectura
- Real-time face swap + video deepfake con una sola imagen de origen.
- Builds precompilados según hardware (CPU/NVIDIA/AMD/Mac Silicon).

## Pitfalls
- **Uso ético obligatorio**: con cara real se requiere consentimiento y etiquetar la salida como deepfake al compartir.
- **Restricciones de contenido**: check incorporado impide procesar material inapropiado (desnudos, contenido gráfico, sensible como metraje de guerra). Puede restringirse o añadir watermark si la ley lo exige.
- No hay garantía: el proyecto puede cerrarse; el usuario es responsable de su uso legal.

## Verificación
- Verificar que la imagen de origen carga y el face swap se aplica; confirmar que no salta el filtro de contenido.

## Referencia
- Repo: https://github.com/hacksider/Deep-Live-Cam
