---
name: moondream-vlm
version: "1.0.0"
description: "Use al analizar imágenes con un VLM diminuto (Moondream)."
tags: [vision, vlm, cv, captioning, object-detection, edge, api, m87]
---

# Moondream — Vision Language Model diminuto (10k⭐)

## When to Use

Cuando hace falta entender imágenes con consultas en lenguaje natural abierto (VQA, captioning, detección por texto, pointing, OCR) sin entrenar un modelo, y GPT-4o/gemini vision es caro o lento. Encaja con el stack de visión de David (onnx-webgpu-inference, cctv-yolo, satellite-ai-vision): YOLO para clases fijas en tiempo real; Moondream para preguntas abiertas ("¿hay operarios sin casco?").

## Resumen

Moondream (M87 Labs, Apache-2.0) es un VLM de ~2B parámetros (variante destilada 0.5B para edge) "que corre en cualquier sitio".

| Modelo | Params | Uso |
|--------|--------|-----|
| Moondream 2B | 2B | general: caption, VQA, detect |
| Moondream 0.5B | 0.5B | edge/dispositivos restringidos (destilado) |
| moondream3.1-9B-A2B | 9B (MoE A2B) | variante que sirve la API cloud actual |

## API Cloud (la vía rápida — verificado en docs oficiales)

Base: `https://api.moondream.ai/v1` · Auth: header `X-Moondream-Auth: API_KEY` (clave en https://moondream.ai/c/cloud/api-keys)

```bash
# VQA
curl -X POST https://api.moondream.ai/v1/query \
  -H 'Content-Type: application/json' -H 'X-Moondream-Auth: KEY' \
  -d '{"model":"moondream3.1-9B-A2B","image_url":"URL","question":"¿Qué hay en la imagen?"}'
# -> {"answer": "...", "request_id": "..."}
```

Endpoints (todos POST, JSON, imagen por `image_url`):

| Endpoint | Payload extra | Respuesta |
|----------|---------------|-----------|
| `/v1/query` | `question` | `{answer}` |
| `/v1/caption` | `length: "normal"`, `stream` | `{caption, metrics{ttft_ms,...}}` |
| `/v1/detect` | `object: "perro"` | `{objects:[{x_min,y_min,x_max,y_max}]}` **coords normalizadas 0-1** |
| `/v1/point` | `object` | `{points:[{x,y}]}` normalizadas |

**Pitfall clave:** las coordenadas de detect/point vienen normalizadas [0,1] — multiplicar por `width`/`height` de la imagen real antes de dibujar boxes o recortar.

## SDK Python / Node

```python
import moondream as md
from PIL import Image

model = md.vl(api_key="KEY")           # cloud
image = Image.open("foto.jpg")
model.query(image, "¿Qué hace la niña?")     # {"answer": ...}
model.detect(image, "coche")                  # {"objects": [...]}
model.point(image, "semáforo")                # {"points": [...]}
model.caption(image, length="normal")         # {"caption": ...}
```

`pip install moondream` · `npm install moondream` (misma superficie: `new vl({apiKey})`, métodos query/detect/point/caption).

## Uso local

El repo remite a https://moondream.ai/c/docs/quickstart (sección "Running Locally") para inferencia en hardware propio. Históricamente las variantes 0.5B/2B corren en CPU/GPU modestas vía `transformers` con `trust_remote_code=True` desde HuggingFace (`m87-labs/moondream-2b`). Los modelos 3.x usan pesos propios: verificar la variante local exacta en docs antes de integrar en producción.

## Comparativa rápida

- **Vs YOLO (cctv-yolo, onnx-webgpu):** YOLO gana en clases fijas, tiempo real y navegador; Moondream en consultas abiertas y OCR/VQA sin entrenar.
- **Vs GPT-4o vision:** Moondream mucho más barato y rápido (TTFT ~80ms en cloud) con pesos abiertos; menos capaz en razonamiento complejo.
- **Vs CLIP (clip-multimodal):** CLIP solo hace matching texto-imagen; Moondream genera texto y boxes.

## Patrón integrado Mastermind (auditoría de fotos de obra/infra)

```python
import moondream as md
model = md.vl(api_key=KEY)
for path in fotos:
    img = Image.open(path)
    cap = model.caption(img)["caption"]
    boxes = model.detect(img, "persona")["objects"]
    # escalar coords 0-1 → píxeles antes de anotar
```

## Verificación

```bash
python -c "import moondream as md, os; from PIL import Image; m = md.vl(api_key=os.environ['MOONDREAM_API_KEY']); print(m.caption(Image.open('test.jpg'))['caption'][:80])"
```

## Referencia

- Repo: https://github.com/m87-labs/moondream · Web: https://moondream.ai/ · Playground: https://moondream.ai/playground
- Examples: https://github.com/m87-labs/moondream-examples (incluye cómo correr en Modal)
