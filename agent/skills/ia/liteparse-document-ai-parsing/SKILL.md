---
name: liteparse-document-ai-parsing
description: "Usa a parsear documentos en local con LiteParse."
version: "2.0.0"
tags: [parseo, liteparse, ocr, pdfium, pdf, local, rust]
related_skills: [liteparse, pdf-processing, marker-pdf-conversion, mineru-pdf-to-markdown]
---

# LiteParse — parser de documentos LOCAL (v2)

> ⚠️ Corrección 2026-09-05 (auditoría): la v1 usaba `from liteparse import DocumentParser` con `model='gpt-4o'` y `schema=...` — **no existe**. LiteParse (v2) es un parser **local** (PDFium + Tesseract OCR) con API `LiteParse().parse(...)`, sin LLM ni cloud ni output CSV.

**Repo:** `https://github.com/run-llama/liteparse` (Rust, ~12K⭐).

## When to Use

- Cuando pidas **parsear documentos a Markdown/JSON/texto** en local, sin depender de un LLM/cloud. Parser de PDF con OCR.

## Uso (API real)

```python
from liteparse import LiteParse
parser = LiteParse()
result = parser.parse("documento.pdf")   # parser local (PDFium + Tesseract OCR)
# formatos de salida: json | text | markdown  (NO csv)
```

También vía CLI (crate Rust): `cargo install liteparse`.

## Pitfalls

- **NO** `DocumentParser(model="gpt-4o", schema=...)` — esa clase/params no existen.
- Es un parser local, explícitamente "sin features LLM propietarias ni dependencias cloud".
- Salidas: **json / text / markdown**; **no hay CSV**.

## Verificación

- `LiteParse().parse(doc.pdf)` → comprobar que produce markdown/texto con bounding boxes correctos.
