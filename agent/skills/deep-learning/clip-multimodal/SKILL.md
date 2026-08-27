---
name: clip-multimodal
description: "Procedimiento para usar CLIP (Contrastive Language-Image Pretraining) para embedding de imágenes y texto, búsqueda semántica, y clasificación zero-shot"
version: 1.0.0
author: Ntizar
tags: [clip, multimodal, embeddings, imagen-texto, open-clip]

---

# CLIP / Aprendizaje Multimodal

## Instalación

```bash
pip install open-clip-torch torch torchvision
```

## Flujo de Uso

### 1. Cargar Modelo

```python
import open_clip
import torch

model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s32b_b82b')
tokenizer = open_clip.get_tokenizer('ViT-B-32')
model.eval()
```

### 2. Embedding de Imagen

```python
from PIL import Image

image = Image.open("foto.jpg")
image_tensor = preprocess(image).unsqueeze(0)

with torch.no_grad():
    image_emb = model.encode_image(image_tensor)
    image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)
```

### 3. Embedding de Texto

```python
texts = tokenizer(["un gato", "un perro", "un coche"])

with torch.no_grad():
    text_emb = model.encode_text(texts)
    text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
```

### 4. Similaridad

```python
scores = (image_emb @ text_emb.T).squeeze()
top_k = torch.topk(scores, 3)
for idx, score in zip(top_k.indices, top_k.values):
    print(f"  {texts[idx].item()}: {score.item():.4f}")
```

### 5. Búsqueda Semántica con FAISS

```python
import faiss
import numpy as np

d = image_emb.shape[-1]
index = faiss.IndexFlatIP(d)  # inner product (cosine tras normalizar)
index.add(image_emb.cpu().numpy().astype(np.float32))

query_emb = text_emb.cpu().numpy().astype(np.float32)
D, I = index.search(query_emb, k=10)  # top 10 más similares
```

## Modelos Disponibles

| Modelo | Precisión | Velocidad | Uso recomendado |
|--------|-----------|-----------|----------------|
| ViT-B-32 | Media | Rápido | Búsqueda en tiempo real |
| ViT-B-16 | Media-Alta | Media | Balance precisión/velocidad |
| ViT-L-14 | Alta | Lento | Alta precisión |
| RN50 | Media | Muy rápido | Edge devices |

## Modelos Pre-entrenados Disponibles

```
laion2b_s32b_b82k  - Entrenado en 2B pares (laion2b), mejor calidad general
laion400m_s13b_b87k - Entrenado en 400M pares (laion400m)
laion2b-s/32-b-32k  - Versión más ligera
```

## Referencias

- Paper original: https://arxiv.org/abs/2103.00020
- OpenCLIP: https://github.com/mlfoundations/open_clip
- Nota técnica: `notes/deep-learning/2026-06-26-clip-multimodal-learning.md`
