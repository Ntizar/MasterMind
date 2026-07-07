---
name: openpose-pose-estimation
version: "1.0.0"
description: "OpenPose — Detección en tiempo real de keypoints corporales (cuerpo, cara, manos, pies). Biblioteca C++/Python para pose estimation multi-persona."
tags: [pose-estimation, computer-vision, keypoints, real-time, deep-learning, C++, body-tracking]
---

# OpenPose — Detección de Pose Corporal en Tiempo Real

## Resumen

[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose) (⭐34K) de CMU es la biblioteca de referencia para detección de keypoints corporales en tiempo real. Detecta cuerpo, cara, manos y pies simultáneamente en múltiples personas.

## Cuándo usar

- Análisis de movimiento/gestos en video
- Detección de postura corporal en tiempo real
- Visualización de pose en dashboards interactivos
- Análisis de ergonomía o biomecánica

## Patrón de uso

```bash
# Build desde source
cd build
cmake -DWITH_INF_ENGINE=OFF -DWITH_CUDA=ON -DCPU_MODE=ON ..
make -j4
```

```python
# Python API
import cv2
import openpose

# Inicializar detector
detector = openpose.PoseDetector()
detector.set_model("BODY_25")  # 25 puntos corporales
detector.set_output_format("json")

# Procesar frame
result = detector.process(frame)
# result: {pose: [[x,y,conf],...], face: [...], hands: [...]}
```

```javascript
// En navegador con WASM (alternativa)
// Para web, usar MediaPipe Pose como alternativa más ligera
```

## Features clave

| Feature | Descripción |
|---------|-------------|
| Multi-persona | Detecta hasta 30 personas simultáneamente |
| 135 keypoints | 25 cuerpo + 70 cara + 40 manos |
| Real-time | 30fps en GPU, 5fps en CPU |
| Multi-plataforma | C++, Python, MATLAB, Android |
| OpenPose 2.0 | Versión más nueva con mejor precisión |

## Integración con otros skills

- **gaze-tracking**: Complementa con detección de mirada
- **roboflow-supervision**: Visualización de keypoints en imágenes
- **manim-video**: Animaciones de pose para contenido educativo

## Pitfalls

- **Build complejo**: OpenPose requiere CMake, Boost, OpenCV. El build puede fallar en distribuciones nuevas
- **GPU recomendada**: Sin GPU, el rendimiento cae drásticamente
- **Alternativa web**: Para el navegador, MediaPipe Pose es más práctico (WebAssembly, no requiere build)
- **Mantenimiento**: El repo principal tiene commits esporádicos. Considerar forks activos como OpenPose2

## Referencias
- Paper: https://arxiv.org/abs/1812.08430
- Website: https://github.com/CMU-Perceptual-Computing-Lab/openpose
- OpenPose2: https://github.com/CMU-Perceptual-Computing-Lab/OpenPose2

---

**Hecho con ❤️ por David Antizar**