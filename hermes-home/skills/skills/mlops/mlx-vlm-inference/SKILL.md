---
name: mlx-vlm-inference
version: "1.0.0"
description: >
  MLX-VLM — Inference y fine-tuning de Vision Language Models en Mac 
  usando MLX. Soporta LLaVA, Pixtral, Florence2, Molmo, Paligemma, 
  IDEFICS y más. Incluye server FastAPI, chat UI, y distributed inference.
license: MIT
tags: [mlops, MLX, VLM, vision-language, inference]

---

# MLX-VLM — Vision Language Models en Mac

## Visión General

[MLX-VLM](https://github.com/Blaizzy/mlx-vlm) (4.8k⭐) es un paquete para inference y fine-tuning de Vision Language Models (VLMs) y Omni Models (con audio/video) en Mac usando MLX.

## Modelos Soportados

### Vision-Language
- LLaVA / LLaVA-NeXT
- Pixtral
- Florence2
- Molmo
- Paligemma
- IDEFICS / IDEFICS2
- DeepSeek-OCR / DeepSeek-OCR-2
- DOTS-OCR / DOTS-MOCR
- Qwen2.5-VL
- Gemma 3

### Omni (Vision + Audio + Video)
- Modelos con soporte multimodal completo

## Instalación

```bash
pip install mlx-vlm
```

## Uso CLI

```bash
# Chat con imagen
mlx_vlm.chat --model llava-next-llama3-8b --image photo.jpg

# Chat con múltiples imágenes
mlx_vlm.chat --model llava-next-llama3-8b --image img1.jpg --image img2.jpg

# Modelo específico
mlx_vlm.chat --model Florence-2-Large
```

## Server FastAPI

```bash
# Iniciar servidor con continuous batching
mlx_vlm.server --model llava-next-llama3-8b --continuous-batching

# Con APC (Automatic Prefix Caching)
mlx_vlm.server --model llava-next-llama3-8b --apc

# Con KV Cache Quantization
mlx_vlm.server --model llava-next-llama3-8b --kv-cache-quantization
```

## Python API

```python
from mlx_vlm import load, generate

model, processor = load("llava-next-llama3-8b")
output = generate(
    model, 
    processor, 
    "Describe this image", 
    "photo.jpg",
    verbose=True
)
```

## Características Avanzadas

### Speculative Decoding
- DFlash (Qwen3.5)
- Gemma 4 MTP

### Vision Feature Caching
- Cache de features visuales para chat multi-imagen
- Acelera respuestas con imágenes similares

### TurboQuant KV Cache
- Cuantización de KV cache para más contexto

### Distributed Inference
- Inference distribuido en múltiples GPUs

### Fine-tuning
- Fine-tuning incluido para modelos soportados

## Chat UI

```bash
# Interfaz Gradio
mlx_vlm.gradio --model llava-next-llama3-8b
```

## Referencias
- [MLX-VLM GitHub](https://github.com/Blaizzy/mlx-vlm)
- [Apple MLX](https://github.com/apple/mlx)
