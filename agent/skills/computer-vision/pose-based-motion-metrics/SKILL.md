---
name: pose-based-motion-metrics
description: "Usa al medir reps o cadencia desde vídeo con pose."
version: "1.0.0"
author: Mastermind (stars-explorer)
license: Apache-2.0 (código de referencia)
metadata:
  hermes:
    tags: [computer-vision, pose-estimation, biomecanica, video, coco-keypoints, conteo-repeticiones, cadencia, series-temporales]
    related_skills: [openpose-pose-estimation, traffic-digital-twin-cctv, gaze-tracking, roboflow-supervision]
---

# Pose-Based Motion Metrics — Métricas de movimiento desde keypoints

**Repo origen:** https://github.com/jeremyipark/vision-demos (266⭐, Python, Apache-2.0, activo 2026-09-16; verificado contra READMEs y guías `*-explained.md` reales). Cuatro demos: `chin_ups` (conta repeticiones), `running` (cadencia y timing de pisadas), `dance_sync` (% de sincronía entre bailarines), `rock_climbing` (segmenta agarres y secuencia usada).

**Cuándo usarlo:** cuando hay que convertir keypoints por frame (ViTPose, OpenPose, COCO-17 en general) en métricas temporales fiables — repeticiones, cadencia, tiempos de contacto, similitud de pose — sin modelos extra ni marcadores.

## Patrón central (5 pasos)

1. **Pose por frame** → keypoints COCO-17 con confianza. En el repo usan `vitpose-plus-large` vía VLM Run Gateway (API key, sin descargar pesos).
2. **Señal escalar autosuficiente**: una diferencia de alturas relativa a un *punto de referencia del propio cuerpo*, nunca al frame. Ej. dominadas: `hand_y - torso_y` (el torso = media de 2 hombros + 2 caderas: promediar 4 articulaciones cancela el ruido por frame).
3. **Suavizado en dos etapas**: filtro de mediana (picos) → media móvil centrada (jitter). Este orden no desplaza los tiempos de los picos.
4. **Máquina de estados con histéresis** para contar eventos: *armada* en un valle, *confirmada* en un pico, *cerrada* en la bajada. Dos umbrales, no uno — con uno solo, el ruido que cruza repetidamente el umbral cuenta varias veces.
5. **Criterio de validación autocalibrado** por sujeto: el pico debe cumplir un gesto anatómico (ojos por encima de las manos = barbilla sobre la barra), no una amplitud absoluta umbral.

## Calibración por clip (la clave de la robustez)

- **Cero de la señal** = meseta de reposo del propio clip (colgado en dominadas; nivel de apoyo del tobillo). Los ceros NO comparan entre vídeos.
- **Cadencia de carrera**: `height[foot] = (ground[foot] - ankle_y) / leg_length`, donde `ground` = percentil 90 de la altura de ESE tobillo (un valor por pierna — en plano lateral los dos tobillos no proyectan igual) y `leg_length` = mediana muslo + mediana pierna medidas como **segmentos**. Usar `|hip_y - ankle_y|` mide cuánto estaba la rodilla doblada (8–11% de error).
- **Pisada** = cruce hacia abajo de `CONTACT_FRACTION` de la altura TÍPICA de balanceo (mediana de picos, para que un frame malo no mueva el umbral). Oscilaciones que no superan `SWING_PEAK_FRACTION` = tobillo en apoyo; apoyos < `MIN_CONTACT_SECONDS` = recorte del umbral a mitad de balanceo. Ambos se absorben.
- **Cadencia = 120 / media(stride_time)** sobre zancadas (mismo pie → mismo pie), no pasos alternos: el offset de landmark por pierna se cancela dentro de la zancada.
- Timings sobre **mid-stance interpolado**, no sobre el cruce del umbral.

## Pitfalls (verificados en las guías del repo)

- **x va normalizada por el ancho del frame e y por el alto** → no son la misma unidad salvo frame cuadrado. Escalar x por la aspect ratio ANTES de medir ángulos o longitudes: con unidades mezcladas, una pierna inclinada 45° se medía 45% más largo (escalada, ±2%). La cadencia (eje único y) no depende de esto; los números de rodilla sí.
- COCO-17 termina en los tobillos — sin talón ni punta: la "pisada" se detecta varios cm por encima de lo que golpea el suelo.
- Frames donde los pies dejan la barra deben descartarse: toda la señal asume el punto de referencia fijo.
- Una sola persona: la señal lee al sujeto trackeado, un segundo cuerpo se ignora.
- Grabación: plano lateral con ambos tobillos visibles; la cinta es ideal (cámara fija). Con cámara en mano, usar cadera como referencia del pie (`FOOT_REFERENCE = "hip"`).
- No juzga técnica (ángulo de codo, kipping) más allá del criterio de validación.

## Higiene de pipeline (reutilizable en cualquier proyecto de David)

- Un knob por ajuste, todo en `config.py`; cada run se autodocumenta con snapshot de parámetros en `run.json` (procedencia).
- Caché de respuestas de API y conversiones keyed **en el fichero fuente Y en los settings** — un setting cambiado nunca reutiliza un fichero obsoleto.
- Salida por run en directorio timestamped: vídeo con overlay + panel de estadísticas, PNG de la señal con cada evento marcado (para ver *por qué* contó cada uno), JSON por evento, `summary.txt` legible.

## Uso en los proyectos de David

- tráfico/CCTV (`traffic-digital-twin-cctv`): histéresis + doble umbral para estados de vehículos (parado/moviendo) sin parpadeo.
- cualquier métrica deportiva o de rehabilitación en HTML local: el patrón señal→histéresis→evento es puro JS/numpy, sin GPU.

## Verificación

Plot de la señal (ej. `displacement.png`) con cada evento marcado: si la explicación visual del "por qué" no concuerda con el JSON de eventos, el umbral está mal, no el dato.
