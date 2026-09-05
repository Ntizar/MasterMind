---
name: depth-anything-3
description: "Usa a estimar profundidad con Depth Anything V3."
version: "2.0.0"
tags: [profundidad, depth-anything, vision, monocular, transformers, v3]
related_skills: [depth-anything-3, threejs-webgpu-relighting, mlx-vlm-inference]
---

# Depth Anything V3 — profundidad monocular

> ⚠️ Corrección 2026-09-05 (auditoría): la API real es `depth_anything_3.api.DepthAnything3` + `from_pretrained` + `model.inference()`; **no** `depth_anything_v3.dpt.DepthAnythingV3`/`predict()`. El checkpoint HF es el del repo (ByteDance-Seed).

**Repo:** `https://github.com/ByteDance-Seed/Depth-Anything-3` (Python, ~6.3K⭐).

## When to Use

- Cuando pidas **estimar profundidad monocolar** de una imagen (relieve, 3D, reframes) con el modelo V3 de ByteDance.

## Uso (API real)

```python
from depth_anything_3.api import DepthAnything3
model = DepthAnything3.from_pretrained("ByteDance-Seed/Depth-Anything-3", device=...)
depth = model.inference(image_path)   # método inference (no predict)
```

## Pitfalls

- Import: **`depth_anything_3.api.DepthAnything3`**; no `depth_anything_v3.dpt.DepthAnythingV3`.
- Método: **`model.inference(...)`**, no `predict()`.

## Verificación

- `DepthAnything3.from_pretrained(...)` → `model.inference(img)` y comprobar el mapa de profundidad.
