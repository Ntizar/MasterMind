---
name: markitdown
description: Convert various file formats to Markdown for LLM consumption. Supports PDF, DOCX, PPTX, XLSX, images, audio, HTML, CSV, JSON, XML, ZIP, EPUB, YouTube URLs, and more via a plugin-based converter architecture.
version: 0.1.0
author: Adam Fourney (Microsoft)
homepage: https://github.com/microsoft/markitdown
tags: [herramientas, PDF, markdown, conversion]

---

# markitdown

Convert almost any file to Markdown for use with LLMs and text-analysis pipelines. Built by Microsoft's AutoGen team.

## What It Does

MarkItDown reads common file types and converts them into clean Markdown, preserving document structure (headings, lists, tables, links). The output is optimized for LLM consumption — not human readability — making it token-efficient while retaining semantic structure.

## Installation

```bash
# Full installation (all optional dependencies)
pip install 'markitdown[all]'

# Minimal (core only: text, HTML, JSON, XML, ZIP)
pip install markitdown

# Specific format extras
pip install 'markitdown[pdf, docx, pptx, xlsx, audio-transcription, youtube-transcription]'
```

**Core dependencies:** `beautifulsoup4`, `requests`, `markdownify`, `magika` (MIME detection), `charset-normalizer`, `defusedxml`

## Basic Usage

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.markdown)        # or result.text_content (deprecated alias)
print(result.title)           # optional title if detected
```

```bash
# CLI
markitdown path-to-file.pdf > output.md
cat file.pdf | markitdown
```

Supported sources: local paths, URLs, `requests.Response` objects, binary streams, data URIs, file URIs.

## When to Use

- **RAG pipelines** — convert uploaded documents (PDF, DOCX, PPTX, images) into Markdown before embedding
- **LLM context building** — prepare multi-format document collections for chat/completion APIs
- **Content extraction** — bulk convert files to a uniform text format for analysis
- **Bulk document comparison** — extract text from Word/PDF pairs and diff them (see pattern below)
- **Plugin extensibility** — register custom converters via `markitdown.plugin` entry points

## Pattern: Bulk Word vs PDF Comparison

Use markitdown to extract text from both formats, then `difflib.unified_diff` to compare. Works for hundreds of document pairs.

```python
from markitdown import MarkItDown
import difflib, os

md = MarkItDown()

def extract_and_compare(word_path, pdf_path):
    word_text = md.convert(word_path).markdown
    pdf_text = md.convert(pdf_path).markdown

    # Normalize: strip markdown headers ( Word includes #, PDF doesn't)
    def normalize(text):
        return [l.strip().lstrip("#").strip() for l in text.splitlines() if l.strip()]

    diff = list(difflib.unified_diff(
        normalize(word_text), normalize(pdf_text),
        fromfile=f"Word: {os.path.basename(word_path)}",
        tofile=f"PDF: {os.path.basename(pdf_path)}",
        lineterm=""
    ))
    return diff  # empty = identical
```

**Bulk iteration pattern:** Walk subdirectories, match `.docx` + `.pdf` pairs by folder, write `diff_<folder>.txt` per pair.

## Browser-Based Fallback (when Python unavailable)

When user cannot install Python, use **mammoth.js + pdf.js** in a single HTML file — zero installation, works in any browser, 100% local:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mammoth/1.8.0/mammoth.browser.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
  // Word extraction
  const result = await mammoth.extractRawText({ arrayBuffer });
  const wordText = result.value;
  // PDF extraction
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  const page = await pdf.getPage(1);
  const content = await page.getTextContent();
  const pdfText = content.items.map(i => i.str).join(' ');
</script>
```

**Template:** `templates/comparar-legal-docs.html` — full working tool with drag-and-drop UI, includes legal document normalization.

## Pitfalls

1. **Markdown header stripping differs by format** — Word converter outputs `# Title` while PDF converter outputs `Title` (no `#`). Always strip markdown headers before comparing text across formats.
2. **markitdown vs liteparse for PDFs** — markitdown handles DOCX+PDF well for text-based files. For scanned PDFs or OCR-heavy documents, use `liteparse` (Rust-based, faster, better OCR). See `herramientas/liteparse-rust-pdf-ocr`.
3. **PDF tracking/spacing artifacts** — PDFs from designed layouts (e.g., Word→PDF export) extract with letter-spacing artifacts: "A C UER DO", "junio d e 2 026", "DELACOMISIÓN". Fix: normalize by stripping all non-alphanumeric chars after lowercasing.
4. **`\b\d+\.\s` regex eats years in legal texts** — Pattern like `\b\d+\.\s` (intended to strip paragraph numbers) matches inside "2026.\n" → "026.\n" gets consumed, leaving "2" from "2026". **Fix:** Use `(?:^|\n)\d{1,2}\.\s` to only match paragraph numbers at line start. Never use `\b` boundary for paragraph number removal in texts with dates/years.
5. **Legal doc comparison normalization pipeline** — For comparing Word vs PDF of legal documents: (a) strip headers/footers (PASEO, CASTELLANA, page numbers), (b) strip paragraph numbers at line start, (c) strip Markdown formatting from mammoth.js (`*1.`), (d) strip signatures section (from "firman en la fecha" onward — different table layouts between formats), (e) lowercase + strip tildes, (f) remove all non-alphanumeric. This yields content-only comparison that ignores formatting differences.
6. **Paragraph numbering restarts between formats** — Word often restarts numbering per section (1,2,1,1,2,3) while PDF continues (1,2,3,4,5,6). Must strip paragraph numbers for comparison — they're formatting, not content.

## Architecture Highlights

- **Plugin-based converters:** Each file type has its own `DocumentConverter` subclass with `accepts()` and `convert()` methods
- **MIME detection:** Uses `magika` (Google's ML-based file type detector) plus `mimetypes` for layered detection
- **Priority system:** Converters are sorted by priority; more specific formats win over generic ones
- **Optional cloud integrations:** Azure Document Intelligence and Azure Content Understanding for higher-quality extraction

## Security Note

MarkItDown performs I/O with the privileges of the current process. Sanitize inputs in untrusted environments and prefer the narrowest conversion API (`convert_local()`, `convert_stream()`, `convert_response()`) for your use case.
