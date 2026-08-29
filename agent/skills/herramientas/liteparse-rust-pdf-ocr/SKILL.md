---
name: liteparse-rust-pdf-ocr
description: "Parser de PDF rápido en Rust con OCR, extracción espacial con bounding boxes, y bindings multi-lenguaje (Node.js, Python, WASM). 7.4k+ estrellas. Ideal para pipelines de documentos donde velocidad y layout importan."
version: 1.0.0
author: Ntizar (extraído de run-llama/liteparse)
source: https://github.com/run-llama/liteparse
tags: [herramientas, PDF, OCR, Rust]

---

# LiteParse — PDF Parsing Rápido en Rust

Parser de PDF de alto rendimiento con OCR y extracción espacial.
Repositorio: [run-llama/liteparse](https://github.com/run-llama/liteparse) (7.4k+ ⭐)

## Características Clave

- **Rust core** — Máximo rendimiento y seguridad
- **Spatial text extraction** — Bounding boxes precisos para cada texto
- **OCR flexible** — Tesseract integrado o servidor HTTP externo
- **Multi-format** — PDF, DOCX, XLSX, PPTX, imágenes (vía conversión)
- **Multi-language bindings** — Node.js (napi-rs), Python (PyO3), WASM
- **Local-first** — Cero dependencias cloud por defecto

## Arquitectura

```
Input (archivo o bytes)
    ↓
Conversion (LibreOffice/ImageMagick si no es PDF)
    ↓
PDF Loading (PDFium extrae texto, imágenes, metadata)
    ↓
OCR (solo en imágenes donde falló extracción)
    ↓
Grid Projection (reconstrucción layout con anchors)
    ↓
Output (JSON o texto plano)
```

## Instalación

```bash
# Node.js
npm install liteparse

# Python
pip install liteparse

# Rust
cargo add liteparse
```

## Uso Node.js

```typescript
import { LiteParse } from 'liteparse';

const parser = new LiteParse();
const result = await parser.parseFile('documento.pdf');
console.log(result.pages[0].textItems);
// [{ text: "Hello", bbox: {x, y, w, h}, ... }]
```

## Uso Python

```python
from liteparse import LiteParse

parser = LiteParse()
result = parser.parse_file("documento.pdf")
for page in result.pages:
    for item in page.text_items:
        print(f"{item.text} @ {item.bbox}")
```

## OCR Engine Trait

```
OcrEngine (trait)
├── Tesseract (built-in, default)
└── HttpOcrServer (remoto, pluggable)

Ejemplos incluidos:
├── easyocr/ — Wrapper EasyOCR
└── paddleocr/ — Wrapper PaddleOCR
```

## Spatial Grid Projection

El componente más complejo y valioso:
- **Anchor-based layout**: Detecta alineación (izq, der, centro, flotante)
- **Forward anchors**: Mantiene info de alineación entre líneas
- **Column detection**: Identifica layouts multi-columna
- **Rotation handling**: Transforma texto rotado 90°/180°/270°
- **OCR merging**: Combina texto nativo con OCR, preservando confidence

## Configuración

Default-first: solo sobreescribir lo necesario.

```typescript
const parser = new LiteParse({
    ocr: true,                    // Habilitar OCR
    ocrLanguage: 'spa+eng',       // Idiomas
    outputFormat: 'json',         // json | text
    // ... más opciones
});
```

## Casos de Uso

1. **Document pipelines** — Ingestión masiva de PDFs con preservación de layout
2. **RAG systems** — Extracción de documentos con contexto espacial
3. **OCR pipelines** — OCR selectivo solo donde es necesario
4. **Multi-format** — Unificar múltiples formatos a estructura consistente

## Data Flow Detallado

```
1. Input: File path o raw bytes (cualquier formato soportado)
2. Conversion: No-PDF → PDF vía LibreOffice/ImageMagick
3. PDF Loading: PDFium extrae text items, imágenes, metadata
4. OCR: Páginas renderizadas y OCR'd solo donde texto falló
5. Grid Projection: Reconstrucción layout con anchor system
6. Post-processing: Bounding boxes, limpieza texto
7. Output: JSON o texto plano formateado
```

## Decision Guide

| Criterio | markitdown | liteparse |
|----------|-----------|-----------|
| Formatos | 15+ (PDF, DOCX, PPTX, XLSX, images, audio, HTML, ZIP, YouTube, EPUB...) | Solo PDF |
| Velocidad | Moderada (Python) | Muy rápida (Rust/PDFium) |
| Bounding boxes | No | Sí |
| OCR | Básico | Flexible (Tesseract, EasyOCR, PaddleOCR, custom) |
| Screenshots para agentes | No | Sí |

## Data Flow Detallado
