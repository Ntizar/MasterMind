---
name: liteparse
description: Parseo inteligente de páginas web y documentos para pipelines LLM con estructura semántica — extracción de contenido estructurado.
version: "1.0.0"
tags: [parsing, LLM, web, document, structure, extraction]
---

# LiteParse — Parseo Inteligente para LLMs

## Resumen

Herramienta de parseo inteligente de páginas web y documentos para pipelines LLM con estructura semántica. 10k⭐.

## Repo de referencia

- **GitHub:** `github.com/run-llama/liteparse`
- **Lenguaje:** Python/JavaScript
- **Licencia:** Apache 2.0

## Instalación

```bash
pip install liteparse
# o
npm install @run-llama/liteparse
```

## Uso Básico

```python
from liteparse import LiteParse

parser = LiteParse()

# Parsear HTML → estructura semántica
doc = parser.parse("<html>...")
structured = doc.to_dict()  # Extrae títulos, párrafos, listas, tablas

# Parsear documento
with open("documento.pdf", "rb") as f:
    doc = parser.parse(f.read(), format="pdf")
    md = doc.to_markdown()
```

## Patrones Clave

1. **HTML semántico:** Convierte HTML plano a estructura con jerarquía clara
2. **Multi-formato:** Soporta HTML, PDF, DOCX, texto plano
3. **Estructura jerárquica:** Títulos, secciones, párrafos, listas, tablas
4. **LLM-ready:** Output optimizado para embedding y retrieval
5. **Ligero:** Sin dependencias pesadas, rápido

## Integración con Mastermind

- Complementa `marker-pdf-conversion` (parseo semántico vs conversión a MD)
- Ideal para pipelines de ingestión de documentos
- Útil para `llm-friendly-web-crawler` preprocessing
- Rápido y ligero para batch processing

## Pitfalls

- **HTML mal formado:** Puede perder estructura con HTML muy sucio
- **Tablas complejas:** Solo parsea tablas simples
- **JavaScript:** No ejecuta JS, solo parsea HTML estático
- **Idioma:** Optimizado para inglés, puede perder matices en español

## Referencias

- [GitHub: run-llama/liteparse](https://github.com/run-llama/liteparse)
