---
name: sam3d-cpp-body-objects
description: "SAM 3D en C++/GGML: cuerpo y objetos desde vídeo."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [sam3d, ggml, 3d, cuerpo-humano, video, vulkan, cpu, mesh, mhr]
    related_skills: [trellis2-img-to-3d, depth-anything-3, segment-anything-model]
---

# SAM 3D en C++/GGML (cuerpo y objetos)

Port **C++23/GGML** del SAM 3D Body de Meta + runtime experimental de SAM 3D Objects: inferencia nativa en **CPU o Vulkan**, sin Python, PyTorch, CUDA ni llama.cpp.

## When to Use (cuándo usarlo)

- Recuperar **malla y pose de cuerpo humano (MHR)** desde imagen o vídeo, sin entorno Python.
- Extraer **objetos 3D** desde imagen + máscara binaria pintada a mano.
- Necesitas un ejemplo de build CMake por presets con sanitizers y backends GGML dinámicos.

## Build verificado

```bash
git submodule update --init --recursive
cmake --preset debug
cmake --build --preset debug -j2
ctest --preset debug
cmake --install build/debug --prefix /tu/prefix
```

Presets: `release`, `optimized-sanitizers`, `vulkan-optimized`, `vulkan-bf16-production` (este aplica parches GGML a una **copia** en `build/`, dejando el submódulo público intacto; decodificador y geometría siguen en F32). `debug` activa ASan/UBSan. Los backends GGML se cargan dinámicamente: **un fallo de Vulkan no cae silenciosamente a CPU**.

## Modelos (GGUF locales, F32)

`body-dinov3-f32.gguf` (encoder de imagen) · `body-pose-branch-f32.gguf` (decoder + pose heads) · `mhr-lod1-f32.gguf` (geometría MHR). Los pesos convertidos **aún no están publicados** en HuggingFace: la vía es `reference/GGUF.md`. No usar cuantizaciones de baja precisión.

## Salidas

- **Body**: imagen + bounding box → malla MHR, joints, pose y cámara (GLB/OBJ estáticos en metros, Y-up) y export de esqueleto GLB con jerarquía MHR de **127 joints**, en pose estática o animación desde vídeo/webcam.
- **Objects**: imagen de escena + máscara pintada → geometría con color por vértice (GLB) vía FlexiCubes indexado (ejemplo del README: 488.564 vértices / 977.232 caras, IoU de silueta >0,9999 frente al oráculo CUDA en 3 vistas).

## Rendimiento y pitfalls

- 85,8 ms por inferencia BF16 nativa en GPU NVIDIA (vs 81,6-84,5 ms de la referencia CUDA upstream); ~8,1 Hz en pipeline en vivo.
- **Sin detección automática de personas** ni estimación de cámara (focal por defecto = diagonal de la imagen) — hay que dar el bounding box.
- Estimaciones **independientes por frame**: no hay modelo temporal aprendido (jitter entre frames).
- Refinado de manos y texturas PBR fuera de alcance.
- La **C API es opaca** (`include/sam3d_model.h`, `include/sam3d.h`); la demo Go no tiene autenticación (solo detrás de despliegue confiable).
- Vídeo: procesado offline de MP4/WebM con frames muestreados; el vídeo no sale del navegador (solo se suben JPEG muestreados).

## Referencia

- Repo: `localai-org/sam3d.cpp` (~46 ⭐, C++, push 2026-09-14, consultado 2026-09-15). Apache-2.0 con excepciones para los pesos.
