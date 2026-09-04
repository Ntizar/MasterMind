---
name: openpose-pose-estimation
description: "Usa al detectar pose humana con OpenPose."
version: "1.0.0"
tags: [cv, pose-estimation, keypoints, deep-learning, c++, realtime]
---

# OpenPose — Detección de Pose Humana Multi-persona

## Qué es

OpenPose (CMU Perceptual Computing Lab, CVPR 2017) fue el **primer sistema en tiempo real multi-persona** que detecta conjuntamente 135 keypoints: 25 del cuerpo, 21×2 manos, 70 cara y 6 pies, sobre una sola imagen o vídeo.

- **Output:** coordenadas (x, y, confianza) por keypoint + PAFs (Part Affinity Fields) para asociar extremidades
- **Backends:** Caffe, OpenGL, OpenVINO, TensorRT, CUDA
- **Multi-persona** sin detector previo (bottom-up), a diferencia de enfoques top-down
- **Licencia:** gratuita para uso no comercial (NOASSERTION — revisar antes de uso comercial)

## Instalación (Windows)

```bash
git clone --recursive https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
cd openpose
# Requiere CMake + Visual Studio (Windows) o Make (Linux)
# Modelos se descargan al compilar (baixar_models option) o con scripts/getModels.sh
```

Pitfall: clonar SIEMPRE con `--recursive` (dependencia de submódulos de Caffe/3rdparty).

## Uso básico

```bash
# Imagen con todos los keypoints
bin/OpenPoseDemo.exe --image_path imagen.jpg --face --hand

# Vídeo en directo
bin/OpenPoseDemo.exe --video video.mp4 --net_resolution "-1x368"

# Salida JSON de keypoints
bin/OpenPoseDemo.exe --image_path img.jpg --write_json output/
```

`--net_resolution "-1x368"` mantiene múltiplo de 16 y equilibra velocidad/precisión en GPU modestas.

## Casos de uso para David

- **Base para proyectos CV**: gestos, interacción, análisis de movimiento en webcams o vídeo
- **Complemento de otras skills de visión** (RF-DETR, GazeTracking, ONNX/WebGPU): OpenPose cubre la parte de pose que las otras no
- **Alternativas modernas** si el proyecto lo requiere: MediaPipe Pose, YOLO-Pose, RTMPose — más ligeras y con mejor soporte web, pero OpenPose sigue siendo el benchmark de referencia y el más completo en manos/cara

## Pitfalls

- **Build en Windows es pesado**: CMake + VS 2019/2022, y los modelos (~200MB) se descargan aparte; fallos típicos por versión de CUDA incompatible con la de PyTorch preinstalada
- **Sin desarrollo activo**: último push en 2024 — para producción considerar alternativas; sigue siendo válido como referencia y para experimentos
- **Licencia no comercial**: no usar en proyectos de clientes sin revisarla
- CPU-only es lento (≈1 fps a resolución baja); GPU recomendada para tiempo real

## Verificación

- `bin/OpenPoseDemo.exe --image_path examples/media/COCO_val2014_000000000192.jpg` debe abrir la ventana con el esqueleto dibujado sobre la persona
- El JSON de salida contiene `part_candidates` y `people` con 25+ keypoints por persona detectada

## Referencias

- Repo: `github.com/CMU-Perceptual-Computing-Lab/openpose` (34.4k⭐)
- Paper: CVPR 2017 — "Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields"

## Comparativa de alternativas

- **[bharath5673/3d_human_pose](https://github.com/bharath5673/3d_human_pose)** — saltar de pose 2D a 3D con YOLO + MediaPipe + BodyPose3DNet (workflow 3D y multi-cámara); es el siguiente paso natural tras detectar la pose 2D en 2D.
- **[ronvidev/modelo_lstm_lsp](https://github.com/ronvidev/modelo_lstm_lsp)** — pipeline de reconocimiento de lengua de signos por secuencia: MediaPipe → normalización de frames → keypoints → LSTM → GUI; ejemplo de clasificación de gestos sobre secuencia de pose.
