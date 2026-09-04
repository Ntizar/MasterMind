---
name: trellis2-img-to-3d
version: "1.0.0"
description: "Usa para imagen a 3D con TRELLIS.2 en C++/ggml y GLB."
tags: [3d, image-to-3d, ggml, trellis, glb]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [3d, image-to-3d, ggml, trellis, glb]
    related_skills: [colmap-view, img2threejs]
---
# trellis2.cpp — Image-to-3D con TRELLIS.2

## Resumen
`trellis2.cpp` (RobertBeckebans fork) es una implementación C++/ggml del pipeline TRELLIS.2 imagen→3D: entra una imagen, sale un mesh 3D con texturas PBR por vértice, toda la inferencia en C++/ggml (sin PyTorch en runtime). El demo exporta a GLB con color de vértice interpolado y atributos PBR. Librería single-file (`src/trellis2.h`/`.cpp`), ggml como submodule, ABI C plana (`src/trellis2_capi.h`) para un servidor demo en Go con visor de mesh en navegador. Pipeline: DINOv3 encoder, shape-SLAT, PBR texturing, CGAL print wrap.

## Uso (comandos reales del README)

Windows AMD (ROCm) — sin contenedor:
```sh
git clone --recursive https://github.com/RobertBeckebans/AI_trellis2cpp.git
cd AI_trellis2cpp
scripts/download_ggufs.sh          # GGUFs f16 -> ggufs/ (~14 GB)
cmake-ninja-win64-rocm.bat         # HIP + Vulkan en una librería
start_server.bat
# abrir http://localhost:8742 y soltar una imagen
```

Windows NVIDIA (CUDA):
```sh
git clone --recursive https://github.com/RobertBeckebans/AI_trellis2cpp.git
cd AI_trellis2cpp
scripts/download_ggufs.sh          # GGUFs f16 -> ggufs/ (~14 GB)
cmake-msbuild-win64-cuda.bat       # CUDA + Vulkan en build-cuda\
start_server.bat build-cuda
# abrir http://localhost:8742 y soltar una imagen
```

## Patrones / Arquitectura
- Backends conmutables en runtime via `TRELLIS2_DEVICE=cpu|rocm|vulkan`, sin segundo build tree. El backend queda registrado en el manifest de cada generación.
- Cascade tier 1536³ con presupuesto de tokens que baja la resolución si el scaffold la excedería.
- Retopología quad + normal-map bake (AutoRemesher vendored sin Qt/TBB; MikkTSpace via `meshopt_generateTangents`).
- Superficie GPL menor: proyección PBR de closest-surface movida de CGAL a tinybvh (default MIT); la ruta low-poly aún usa CGAL Alpha Wrap.
- Referencia PyTorch reproducible nativa vía `uv` (incluye wheels ROCm de AMD en Windows) — `scripts/ref_generate.py` produce una generación completa en el visor junto a los runs de backend.

## Pitfalls
- `download_ggufs.sh` es script shell: ejecutarla desde **Git Bash**, no `cmd`.
- `cmake-ninja-win64-rocm.bat` necesita ROCm SDK y Vulkan SDK (se niega sin `VULKAN_SDK`). Para saltar Vulkan: `-DGGML_VULKAN=OFF` o `cmake-ninja-win64-cpu.bat` / `cmake-ninja-win64-vulkan.bat`. **Borra `build/`** (es configure, no rebuild).
- CUDA: CUDA Toolkit 12.8+, Visual Studio 2019/2022 o Build Tools, vcpkg con `eigen3` y `cgal` en `C:\vcpkg`; sin vcpkg el print wrap y quad stage se configuran como no disponibles (leer output de configure). CUDA graphs desactivados por defecto (`TRELLIS2_CUDA_GRAPHS=1` re-activa).
- `start_server.bat` reconstruye lo stale y pone DLL + ROCm runtime en `PATH`; ese `PATH` importa para `ctest`.
- Cartografía de `CUDA_ARCHS`: 120 Blackwell/80 default, 89 (RTX 40xx), 86 (30xx), 75 (20xx).
- Vigilar el decoder de subdivision (divergencia o colapso); el peor fallo pasado superó el check unilateral en silencio.

## Verificación
- Verificar generaciones y export GLB full-density en términos MIT; la ruta low-poly requiere CGAL Alpha Wrap (ver sección licencia).
- Números de paridad: `docs/VERIFICATION.md`; arquitectura: `docs/architecture/README.md`; bugs documentados en `docs/bugs/`.

## Referencia
README de https://github.com/RobertBeckebans/AI_trellis2cpp. Modeled after sam3.cpp; stage-1 port por rms80, pipeline completo image→mesh por richiejp.
