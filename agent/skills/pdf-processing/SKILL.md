---
name: pdf-processing
version: "1.0.0"
description: "Ecosistema completo de procesamiento de PDFs: extracción de texto, OCR, extracción de datos estructurados, conversión a Markdown, generación de artefactos, y análisis de diseño. Cubre desde PDFs simples hasta pipelines de 1000+ documentos."
tags: [pdf, ocr, extraction, markdown, landing, artifacts, pymupdf, fitz, markitdown, liteparse]
---

# PDF Processing — Ecosistema Completo

## Resumen

Ecosistema completo de procesamiento de PDFs que cubre todos los patrones de uso:

| Subskill | Cuándo usar | Output |
|----------|-------------|--------|
| **PDF → Structured Data (LLM)** | PDFs digitales con texto seleccionable, necesitas datos JSON/CSV | JSON validado con schema |
| **PDF → Structured Data (Regex)** | Formato predecible, sin LLM/cloud, volumen alto | CSV plano + JSON |
| **OCR Quirúrgico** | PDFs escaneados/imágenes, necesitas preservar layout | Markdown/HTML con posición exacta |
| **PDF → Landing Page** | PDF de propuesta de diseño → landing HTML generada | HTML responsive |
| **PDF → 3 Artifacts** | Informe técnico → HTML resumen + LinkedIn post + nota | 3 artefactos con branding |
| **Markitdown** | Conversión genérica multi-formato a Markdown | Markdown limpio |
| **LiteParse (Rust)** | PDF rápido con OCR + bounding boxes + layout | JSON con spatial data |
| **LiteParse (AI)** | Extracción con LLM + auto-learn schema | JSON/CSV con schema aprendido |

## Decision Guide

```
¿El PDF tiene texto seleccionable?
├── NO → OCR Quirúrgico (si necesitas preservar layout)
│        └── ¿Necesitas datos estructurados? → PDF → Structured Data (LLM)
│        └── ¿Necesitas Markdown navegable? → OCR Quirúrgico
│
├── SÍ → ¿Necesitas datos estructurados (JSON/CSV)?
│        ├── Sí, sin LLM → PDF → Structured Data (Regex)
│        └── Sí, con LLM → PDF → Structured Data (LLM)
│
└── ¿Necesitas generar contenido a partir del PDF?
    ├── Landing page → PDF → Landing Page
    ├── Informe → artefactos → PDF → 3 Artifacts
    ├── Conversión genérica → Markitdown
    └── OCR rápido con layout → LiteParse (Rust)
```

## Sección 1: PDF → Structured Data (LLM)

**Para:** Extracción de datos estructurados de PDFs digitales usando PyMuPDF + LLM.
**Validado:** 270+ informes CIAF → 99.6% éxito.
**Pipeline:** Font analysis → section detection → LLM schema filling → JSON validation.
**Pitfalls clave:** `span["text"]` puede ser None, text limit analizar antes, directory search recursivo, rate limiting en batch.

## Sección 2: PDF → Structured Data (Regex)

**Para:** Formato predecible, sin LLM/cloud, volumen alto, precisión determinística.
**Pipeline:** PyMuPDF → regex por campo → CSV/JSON aplanado.
**Pitfalls clave:** Backtracking catastrófico, doble escape, TOC confusión, year≠suceso, bilingüe duplicado.

## Sección 3: OCR Quirúrgico

**Para:** PDFs escaneados/imágenes, necesitas preservar layout con precisión absoluta.
**Pipeline:** Corte página → clasificación → OCR fallback → ensamblado → vectorización ChromaDB.
**Pitfalls clave:** poppler no funciona en contenedores, render es caro (solo fallback), Tesseract necesita preprocesado.

## Sección 4: PDF → Landing Page

**Para:** PDF de propuesta de diseño → landing page HTML generada por IA.
**Pipeline:** Extracción visual de colores (Median Cut) → análisis IA → generación HTML.
**Pitfalls clave:** pdf-parse v2.x rompe API, ESM + createRequire, .env en .dockerignore, colores genéricos sin extracción visual.

## Sección 5: PDF → 3 Artifacts

**Para:** Informe técnico → HTML resumen + LinkedIn post + nota de auditoría.
**Pipeline:** Extracción texto → análisis contenido → generación HTML (Aurora) → LinkedIn post → nota.
**Pitfalls clave:** Atribución literal exacta, colores reales del PDF, fallback chain para extracción.

## Sección 6: Markitdown

**Para:** Conversión genérica multi-formato a Markdown. Soporta 15+ formatos.
**Pipeline:** Plugin-based converter architecture → Markdown limpio.
**Pitfalls clave:** PDF tracking artifacts, \b\d+\.\s regex come años, header stripping difiere por formato.

## Sección 7: LiteParse (Rust)

**Para:** OCR rápido con bounding boxes, spatial extraction, multi-formato (PDF, DOCX, XLSX, PPTX, imágenes).
**Pipeline:** Rust core → PDFium → OCR selectivo → Grid Projection → JSON con layout.
**Decision:** Markitdown para conversión genérica, LiteParse para OCR rápido con layout.

## Sección 8: LiteParse (AI)

**Para:** Extracción con LLM integrado, auto-learn schema desde análisis de fuentes PDF.
**Pipeline:** Rust parser → LLM extraction → JSON/CSV con schema aprendido.
**Casos de uso:** Informes oficiales (CIAF), facturas, contratos.

## Referencias Cruzadas

- `ocr-quirurgico-pdf-md` → Para PDFs escaneados con layout preservation
- `pdf-to-landing` → Para conversión PDF → landing page
- `pdf-to-artifacts-david-antizar` → Para generar artefactos de contenido
- `markitdown` → Para conversión genérica multi-formato
- `liteparse-rust-pdf-ocr` → Para OCR rápido con Rust
- `liteparse-document-ai-parsing` → Para extracción con LLM integrado
- `pdf-llm-extraction` → Para datos estructurados con LLM
- `pdf-regex-structured-extraction` → Para datos estructurados con regex
