---
name: chunkr-ai
description: Chunkr — API de procesamiento de documentos con IA para extraer texto, tablas y estructura de PDFs.
category: data-pipeline
---

# Chunkr AI — Procesamiento de Documentos con IA

## Qué es

Chunkr es una API de procesamiento de documentos que usa IA para:
- **Document parsing** — extraer texto, tablas, imágenes de PDFs
- **Intelligent chunking** — dividir documentos en chunks semánticos
- **Structure extraction** — detectar estructura de documentos
- **RAG-ready** — output optimizado para sistemas RAG

## Instalación

```bash
# API REST
# Documentación: https://docs.chunkr.ai

# SDK Python
pip install chunkr
```

## Casos de uso para David

- **RAG pipelines** — procesar documentos para bases de conocimiento
- **PDF processing** — extraer datos de PDFs complejos
- **Document analysis** — analizar estructura de documentos
- **Integration** — usar con Marker para PDF → Markdown

## Pitfalls

- Es una API de pago — verificar precios
- Requiere conexión a internet
- Los documentos grandes pueden tardar
- Límites de tamaño de archivo

## Referencias

- Repo: `github.com/lumina-ai-inc/chunkr` (4K⭐)
- Docs: `https://docs.chunkr.ai`
