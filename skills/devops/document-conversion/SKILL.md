---
name: document-conversion
description: Convertir cualquier documento (PDF, DOCX, PPTX, HTML, imágenes, audio) a Markdown limpio con IA — ingestión de documentos para pipelines LLM.
version: "1.0.0"
tags: [document, pdf, docx, markdown, conversion, OCR, AI]
---

# Document Conversion — Microsoft MarkItDown

## Resumen

Convierte cualquier documento (PDF, DOCX, PPTX, HTML, imágenes, audio, video) a Markdown limpio con IA. 154k⭐.

## Repo de referencia

- **GitHub:** `github.com/microsoft/markitdown`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install markitdown
```

## Uso Básico

```python
import markitdown

converter = markitdown.MarkItDown()

# PDF → Markdown
result = converter.convert("documento.pdf")
print(result.text_content)

# DOCX → Markdown
result = converter.convert("informe.docx")

# PPTX → Markdown
result = converter.convert("presentacion.pptx")

# Imagen → Markdown (con OCR)
result = converter.convert("foto.png")

# Audio → Transcripción
result = converter.convert("grabacion.mp3")
```

## Pipeline de Ingestión

```python
from pathlib import Path
import markitdown

converter = markitdown.MarkItDown()
SUPPORTED = {'.pdf', '.docx', '.pptx', '.xlsx', '.html', '.htm',
             '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff',
             '.mp3', '.wav', '.mp4', '.avi'}

def process_document(filepath):
    ext = Path(filepath).suffix.lower()
    if ext not in SUPPORTED:
        raise ValueError(f"Formato no soportado: {ext}")
    result = converter.convert(filepath)
    return result.text_content

# Batch processing
for doc in Path("/docs").glob("*"):
    if doc.suffix.lower() in SUPPORTED:
        md = process_document(doc)
        # Guardar o insertar en vector DB
```

## Pitfalls

- **PDFs escaneados:** Requiere OCR. Las imágenes sin texto no se convierten bien.
- **Tablas complejas:** Las tablas con celdas combinadas pueden perder estructura.
- **Tamaño:** Documentos >50MB pueden consumir mucha memoria.
- **Formatos antiguos:** `.doc` y `.ppt` pueden no soportarse.
- **Dependencias:** Requiere `poppler-utils` para PDFs.

## Referencias

- [GitHub: microsoft/markitdown](https://github.com/microsoft/markitdown)
