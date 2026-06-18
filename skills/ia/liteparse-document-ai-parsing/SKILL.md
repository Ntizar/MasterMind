---
name: liteparse-document-ai-parsing
version: "1.0.0"
description: "Liteparse — parser de documentos con IA del equipo LlamaIndex (10K⭐). Extrae datos estructurados (JSON/CSV) de PDFs, HTML, markdown, imágenes usando LLMs. Rápido (Rust)."
tags: [document-parsing, llm, extraction, pdf, rust, llamaindex, ai]
---

# Liteparse — Document AI Parsing

## Resumen

Liteparse de LlamaIndex (run-llama) es un parser de documentos **rápido** (Rust) que extrae datos estructurados de documentos no estructurados usando **LLMs**. A diferencia de markitdown (conversión a markdown), liteparse extrae **esquemas específicos** (JSON/CSV con campos definidos).

## Características

- **Rápido:** Escrito en Rust → milisegundos por página
- **Estructurado:** Extrae JSON/CSV según schema que definas
- **Multi-formato:** PDF, HTML, Markdown, imágenes
- **LLM integrado:** Usa modelos locales o API (OpenAI, Claude)
- **Open-source:** Apache 2.0

## Instalación

```bash
pip install liteparse  # Python bindings
# O CLI directa
cargo install liteparse  # Rust
```

## Uso

```python
from liteparse import DocumentParser

# Definir schema de extracción
schema = {
    "company_name": "string",
    "invoice_number": "string",
    "date": "date",
    "total_amount": "number",
    "line_items": [{"description": "string", "amount": "number"}]
}

# Parsear
parser = DocumentParser(model="gpt-4o")
result = parser.parse("factura.pdf", schema=schema)
# → {"company_name": "ACME", "invoice_number": "INV-001", ...}
```

## Integración con Mastermind

- Pipeline `pdf-to-dashboard` (extraer datos de presupuestos de obra)
- Pipeline `pdf-to-landing` (estructurar contenido de PDFs)
- OCR quirúrgico (complementar `ocr-quirurgico-pdf-md`)
- Extracción de datos de facturas, contratos, informes

## Comparativa

| Herramienta | Output | Velocidad | Formato target |
|------------|--------|-----------|----------------|
| **markitdown** | Markdown | Media | Conversión genérica |
| **liteparse** | JSON/CSV | Alta (Rust) | Extracción estructurada |
| **pdfplumber** | Tablas | Baja | PDF-only |
| **Unstructured** | Markdown+JSON | Media | Multi-formato |

## Referencia

- Repo: `run-llama/liteparse