---
name: threejs-webgpu-relighting
version: "1.0.0"
description: "Luz monocualar web con Three.js WebGPU y Transformers.js."
tags: [threejs, webgpu, depth, relighting, transformers-js, onnx, creative]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [threejs, webgpu, depth, relighting, onnx]
    related_skills: [vgpu-webgpu-typescript, webgl-scene-wow, threejs-3d-maps, depth-anything-3]
---
# Monocular Light Injection — Three.js + Transformers.js

## Resumen
Port independiente con Three.js (WebGPU + TSL) del ejemplo `monocular-light-injection` de TypeGPU: toma un feed de webcam o una foto, estima profundidad pixel a pixel con una red neuronal en el navegador e inyecta una **luz puntual virtual móvil** en la escena, con sombreado difuso/especular dependiente de profundidad, sombras suaves ray-marched y un sprite de bombilla brillante. **Sin dependencia de TypeGPU** (el original usa una red DepthART custom como shaders de compute).

## Uso (nombres reales del código)
- Demo: https://radames.github.io/relight-three-js-transformers-js/ (requiere navegador WebGPU).
- **Render**: `WebGPURenderer` de Three.js + TSL en `src/relight/` (pass temporal de estabilización de profundidad, pass de superficie slope+AO a storage texture, frag de relighting fullscreen: Lambert envuelto, specular tipo Blinn-Phong, sombras ray-marched de 32 pasos, sprite de bombilla, tonemap Reinhard extendido + dither). Bucle único `requestAnimationFrame`.
- **Profundidad**: [Depth Anything V2](https://huggingface.co/onnx-community/depth-anything-v2-small) (small/base/large, seleccionable) en el backend WebGPU de transformers.js, en `fp16` si el dispositivo soporta `shader-f16`. Red corre a la "depth res" seleccionable (252/392/448/518 px). Código en `src/depth/`.
- **Backend/engine** (dropdown en el panel): `webgpu` (default, shared device), `wasm`, y `webnn-gpu`/`webnn-npu` donde el navegador exponga WebNN. El backend reportado (read-only) muestra p. ej. `webgpu · fp16 · shared device`, `wasm · q8`.

## Patrones / Arquitectura
- **`webgpu` (default) — shared device**: ONNX Runtime y Three.js comparten un único `GPUDevice`; el frame nunca sale de la GPU hacia la red: un compute pass muestrea la textura de video y escribe el tensor NCHW normalizado en un storage buffer que la sesión lee *in situ*. Elimina el draw de canvas por-frame, el readback `getImageData` y el rescale/normalize/pack de CPU (~39% menos latencia de profundidad; 245 ms → 150 ms en Depth Anything V2 small, fp16, 448 px, cámara en vivo, Chrome headless en Apple Silicon — figura relativa, no absoluta del hardware).
- Un `GPUBuffer` no cruza el límite de thread, así que este backend corre en el hilo principal.
- ONNX Runtime acepta un adapter pero nunca un device, así que siempre crea el suyo y el renderer lo toma prestado.

## Pitfalls
- Requiere navegador con WebGPU; fallback `wasm` (q8) disponible.
- El coste del relight es ~1–3 ms de GPU por frame; una webcam de 30 fps no limita el framerate (solo se intercambia el último frame de video).

## Verificación
- Cargar el demo con un navegador WebGPU; mover la luz y ver sombreado dependiente de profundidad y sombras; consultar las filas "depth"/"backend".

## Referencia
- Repo: https://github.com/radames/relight-three-js-transformers-js. Original: TypeGPU `monocular-light-injection` (docs.swmansion.com/TypeGPU).
