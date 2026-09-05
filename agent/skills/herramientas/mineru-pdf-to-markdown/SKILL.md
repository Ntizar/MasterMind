---
name: mineru-pdf-to-markdown
description: "Usa al convertir PDFs densos con MinerU."
version: "2.0.0"
tags: [pdf, mineru, markdown, ocr, layout, extraccion, cli]
related_skills: [marker-pdf-conversion, pdf-llm-extraction, pdf-processing, ocr-quirurgico-pdf-md]
---

# MinerU — PDF → Markdown con layout y OCR

> ⚠️ Corrección 2026-09-05 (auditoría): el flag de entrada es `-p` (no `-i`), licencia "MinerU Open Source License" (Apache 2.0-based, no NOASSERTION) y la salida v2/v3 es `.md`+`images/`. El extra documentado es `mineru[all]`, no `mineru[core]`.

**Repo:** `https://github.com/opendatalab/MinerU` (Python, ~79K⭐) · Licencia: MinerU Open Source License (basada en Apache 2.0).

## When to Use

- Cuando pidas **convertir PDFs densos** (con tablas, fórmulas, imágenes, multi-columna) a **Markdown** con layout correcto, en local.

## Uso

```bash
pip install "mineru[all]"      # extras documentados; mirar módulos de extensión según docs
mineru -p entrada.pdf -o salida/    # -p = path de entrada (NO -i)
```

## Salida (v2/v3)

- `*.md` (texto marcado con layout), JSON por página (`*.json`) y `images/` con las figuras/tablas extraídas.
- *(Los nombres `*_middle.json`/`*_model.json` son de la estructura v1 — obsoletos.)*

## Pitfalls

- Flag de entrada: **`-p`** (path), no `-i`.
- Licencia: **MinerU Open Source License** (no NOASSERTION/AGPL).
- Extras: usa `mineru[all]` (o los módulos de extensión documentados); `mineru[core]` no está documentado.

## Verificación

- `mineru -p doc.pdf -o out/` → comprobar `out/*.md` + `out/images/`; verificar que tablas/fórmulas conservan estructura.
