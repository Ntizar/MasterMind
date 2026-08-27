---
name: marker-pdf-conversion
version: "1.0.0"
description: "Marker — SOTA open-source para convertir PDF/DOCX/PPTX a markdown con alta precisión. Mantiene tablas, fórmulas, código e imágenes. Funciona en GPU/CPU/MPS."
tags: [pdf, markdown, ai, document-intelligence, conversion, OCR, LLM]
---

# Marker — Conversión PDF a Markdown con IA

## Resumen

[Marker](https://github.com/datalab-to/marker) (⭐37K) es el SOTA open-source para convertir documentos PDF, DOCX, PPTX, XLSX, HTML y EPUB a markdown, JSON, chunks o HTML con alta precisión.

## Cuándo usar

- Extraer texto de PDFs para RAG/knowledge base
- Convertir documentos científicos a markdown estructurado
- Procesar batch de PDFs offline (200M+ páginas/semana en producción)
- Mantener tablas, fórmulas, código e imágenes intactos

## Patrón de uso

```bash
pip install marker-pdf
marker convert archivo.pdf --output_dir ./output
```

```python
from marker.convert import convert_single_pdf

# Conversión básica
markdown, images, metadata = convert_single_pdf("documento.pdf")

# Con LLM boost (más preciso)
markdown, images, metadata = convert_single_pdf("documento.pdf", llm_model="claude")

# Extracción estructurada con schema
markdown, images, metadata = convert_single_pdf("documento.pdf", schema="mi_schema.json")
```

## Integración con otros skills

- **rag-knowledge-base**: Pipeline ideal: Marker → Markdown → Embedding → ChromaDB
- **adaptive-web-scraping**: Complemento para extraer texto de PDFs encontrados en scraping
- **firecrawl-web-scraping**: Alternativa offline a Firecrawl para procesamiento de PDFs

## Pitfalls

- **Tamaño de modelo**: El modelo base necesita ~8GB de VRAM. Para CPU puro, usa `--cpu` pero será lento
- **Idioma**: Soporta todos los idiomas pero el rendimiento óptimo es en inglés/alemán/francés/español
- **PDFs escaneados**: Funciona bien pero la OCR depende del modelo. Para PDFs muy antiguos o de mala calidad, considera añadir `--ocr`
- **Fórmulas LaTeX**: Se convierten a LaTeX. Para MathML necesitas post-procesamiento

## Referencias
- Docs: https://documentation.datalab.to
- Playground: https://www.datalab.to/playground
- Modelo Chandra (SOTA): https://github.com/datalab-to/chandra

---

**Hecho con ❤️ por David Antizar**