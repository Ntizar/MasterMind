---
name: mlx-vlm-inference
description: "Usa a inferir VLM en Apple Silicon con MLX-VLM."
version: "2.0.0"
tags: [mlx, vlm, vision-language, apple-silicon, mlx-vlm, inference]
related_skills: [moondream-vlm, mlx-vlm-inference, huggingface-hub]
---

# MLX-VLM — inference de Vision-Language en Apple Silicon

> ⚠️ Corrección 2026-09-05 (auditoría): los módulos CLI `mlx_vlm.chat`/`mlx_vlm.gradio` **no existen**; el real es `mlx_vlm.generate` / `mlx_vlm.chat_ui`. Flags de server: `APC_ENABLED=1` y `--kv-bits` (no `--apc` ni `--kv-cache-quantization`); batching automático.

**Repo:** `https://github.com/Blaizzy/mlx-vlm` (Python, ~5.5K⭐).

## When to Use

- Cuando pidas **inferir un VLM** (texto+imagen) en Apple Silicon (MLX) de forma local y eficiente.

## Uso (API real)

```bash
pip install mlx-vlm
# CLI de generación:
mlx_vlm.generate --model <modelo> --image img.jpg --prompt "..."
# UI/servidor:
mlx_vlm.chat_ui ...        # (no mlx_vlm.gradio)
# server con APC enable:
APC_ENABLED=1 mlx_vlm.server ... --kv-bits 8   # (no --apc ni --kv-cache-quantization)
```

## Pitfalls

- Módulos: **`mlx_vlm.generate`** / **`mlx_vlm.chat_ui`**, no `chat` / `gradio`.
- Server: `APC_ENABLED=1` y `--kv-bits`, no `--apc`/`--kv-cache-quantization`.
- Modelos en constante evolución (Gemma 3→4); consultar el README.

## Verificación

- `mlx_vlm.generate` con una imagen y un prompt sobre la imagen.
