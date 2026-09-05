---
name: baidu-unlimited-ocr
description: "Usa al parsear documentos largos con el modelo Unlimited-OCR."
version: "2.0.0"
tags: [ocr, documentos, parsing, huggingface, transformers, deepseek-ocr, local]
related_skills: [mineru-pdf-to-markdown, marker-pdf-conversion, pdf-processing, ocr-quirurgico-pdf-md]
---

# Unlimited-OCR (Baidu) — parser de documentos de largo alcance

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 describía esto como un "servicio OCR gratuito sin límites" con endpoint REST `api.unlimitedocr.com/api/ocr`. **Falso.** No hay API REST; es un modelo de investigación de parsing de documentos (sucesor de DeepSeek-OCR, paper arXiv 2606.23050) que corre **en local** con HuggingFace Transformers y requiere GPU/CUDA.

**Repo:** `https://github.com/baidu/Unlimited-OCR` (MIT, Python, ~25K⭐)

## When to Use

- Cuando pidas **extraer/parsear documentos largos** (formato → contenido estructurado) con un modelo de IA en local, sin depender de una nube de pago.
- Cuando necesites un **parser one-shot de largo alcance** (long-horizon) — leer PDFs/páginas largos de una pasada, no trocear a mano.

## Qué es

Modelo de investigación de Baidu para **parsing de documentos de largo alcance**. "Unlimited" NO significa cuota gratuita ilimitada: se refiere al parser de documentos de alcance largo (one-shot long-horizon parsing). Es el sucesor de DeepSeek-OCR.

- **Ejecución:** 100% local con `transformers` (HuggingFace), vía `AutoModel.from_pretrained('baidu/Unlimited-OCR')`.
- **Requisitos:** GPU/CUDA recomendada, Python 3.12+, parámetros grandes.
- **NO expone API REST** — no hay `api.unlimitedocr.com` ni nada que consumir por HTTP.

## Uso

```python
from transformers import AutoModel, AutoTokenizer
# Cargar modelo local
tokenizer = AutoTokenizer.from_pretrained('baidu/Unlimited-OCR')
model = AutoModel.from_pretrained('baidu/Unlimited-OCR').cuda()
# Inferencia sobre el documento
# (la API del repo expone un método de inferencia tipo infer(); ver README de baidu/Unlimited-OCR)
result = model.infer(...)
```

Consultar el README del repo y el paper (arXiv 2606.23050) para la firma exacta de `infer()` y el formato de entrada/salida.

## Pitfalls

- **Nada de REST:** no hay `api.unlimitedocr.com/api/ocr`. Cualquier skill/prompt que mencione un endpoint de este repo está inventado.
- Imagen grande + modelo grande → necesita CUDA y batería de VRAM; no es una tool de CPU ligera.
- Es modelo de **parsing**, no un OCR clásico por caja de texto: para PDFs "en imágenes" quizá te convenga combinarlo con `marker-pdf` / `mineru`.

## Verificación

- Instalar el modelo y correr inferencia sobre un PDF largo; comprobar que la salida mantiene el orden/secciones correctas (ahí es donde destaca sobre OCR por páginas).
