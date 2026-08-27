---
name: mineru-pdf-to-markdown
version: "1.0.0"
description: "Úsalo al convertir PDFs densos a Markdown con layout y OCR."
tags: [pdf, mineru, ocr, markdown, layout-analysis, rag]
---

# MinerU — PDF/Office → Markdown para LLMs

Herramienta de OpenDataLab que transforma documentos complejos (PDFs escaneados, papers, docx/pptx/xlsx) en Markdown o JSON estructurado, apto para pipelines RAG y agentes. Repo: https://github.com/opendatalab/MinerU

## Instalación

```bash
pip install "mineru[core]"        # núcleo CPU
pip install "mineru[all]"         # con soporte GPU (backend vlm)
uv tool install mineru[core]      # alternativa CLI aislada
```

## Uso CLI

```bash
# PDF → Markdown (pipeline estándar)
mineru -i entrada.pdf -o salida/

# Elegir backend: pipeline (rápido, CPU) | vlm (más preciso, requiere GPU/API)
mineru -i entrada.pdf -o salida/ -b vlm

# OCR forzado para escaneos
mineru -i escaneado.pdf -o salida/ -p

# Solo procesar páginas concretas (1-indexado, ej: 1-3,5,8)
mineru -i entrada.pdf -o salida/ -s 1-3,5

# Idioma para OCR (por defecto auto-detección)
mineru -i doc.pdf -o salida/ -l es
```

## Uso en Python

Patrón recomendado: llamar a la CLI en subproceso (más estable entre versiones).

```python
import subprocess
subprocess.run(["mineru", "-i", "doc.pdf", "-o", "out/", "-b", "pipeline"], check=True)
```

## Salida

Por cada documento genera en el directorio de salida:
- `*.md` — contenido en Markdown con tablas y fórmulas (LaTeX)
- contenido JSON estructurado por página (bloques, coordenadas)
- `images/` — figuras extraídas
- `*_middle.json`, `*_model.json` — artefactos intermedios de layout (debug)

## Cuándo usarlo

- RAG/agentes: PDFs densos → Markdown limpio con tablas preservadas
- Papers académicos: fórmulas a LaTeX, referencias intactas
- Escaneos: OCR de calidad con detección de layout (columnas, tablas, cabeceras)
- Alternativas ya disponibles en el ecosistema: `markitdown` (rápido, Office-first, pierde layout), `liteparse` (Rust, velocidad), pipeline `ocr-quirurgico` (página a página con vision). MinerU es el más fuerte en layout complejo + tablas.

## Pitfalls

- Primera ejecución descarga modelos (~1-2 GB) de HuggingFace; puede tardar y fallar offline.
- Backend `vlm` necesita GPU con VRAM suficiente; en CPU usar `-b pipeline`.
- PDFs muy grandes: procesar por rangos de páginas (`-s`) para no agotar RAM.
- Licencia NOASSERTION en el repo — revisar términos antes de uso comercial.
- En Windows, ejecutar desde rutas sin espacios y con Python 3.10-3.13.

## Verificación

```bash
mineru -i ejemplo.pdf -o out/ -b pipeline && ls out/
# Comprobar que out/ contiene .md y JSON de layout, y que el .md incluye las tablas esperadas
```
