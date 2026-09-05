---
name: document-conversion
description: "Usa a convertir muchos formatos con MarkItDown."
version: "2.0.0"
tags: [documentos, conversion, markitdown, pdf, docx, xlsx, python, llm]
related_skills: [markitdown, document-conversion, pdf-processing, docx, xlsx]
---

# MarkItDown — conversión de documentos a markdown para LLM

> ⚠️ Corrección 2026-09-05 (auditoría): la fuente real es **`microsoft/markitdown`** (el manifest apuntaba a firecrawl/anydoc por error). MarkItDown **no convierte .mp4/.avi**: soporta PDF, Office, imágenes, audio, HTML, CSV/JSON/XML, ZIP, YouTube URLs y EPUB. No requiere poppler (usa pdfminer); solo Python 3.10+.

**Repo:** `https://github.com/microsoft/markitdown` (Python, ~178K⭐).

## When to Use

- Cuando pidas **convertir documentos** (PDF, DOCX, PPTX, XLSX, imágenes, audio, HTML…) a **Markdown** para consumir con un LLM.

## Uso

```bash
pip install "markitdown[all]"        # extras: [pdf,docx,pptx,xlsx,audio-transcription,youtube-transcription]
```

```python
from markitdown import MarkItDown
md = MarkItDown()
result = md.convert("documento.pdf")   # también CLI: `markitdown archivo`
print(result.text_content)
```

## Formatos soportados

PDF, PPTX, DOCX, XLSX, imágenes, audio (transcripción), HTML, CSV/JSON/XML, ZIP, YouTube URLs y EPUB. *(NO vídeo raw .mp4/.avi.)*

## Pitfalls

- **No** convierte vídeo (.mp4/.avi).
- **No** requiere poppler-utils (usa pdfminer); Python 3.10+.
- Fuente: `microsoft/markitdown`.

## Verificación

- `md.convert(doc.pdf)` → `text_content`; probar con DOCX/XLSX.
