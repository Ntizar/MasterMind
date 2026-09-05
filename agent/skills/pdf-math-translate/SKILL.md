---
name: pdf-math-translate
description: "Usa al traducir PDFs matemáticos con pdf2zh."
version: "2.0.0"
tags: [pdf, traduccion, matematicas, pdf2zh, latex, formula, cli]
related_skills: [pdf-processing, pdf-math-translate, document-conversion, marker-pdf-conversion]
---

# PDF Math Translate (pdf2zh) — traducir PDFs matemáticos

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 usaba `pip install PDFMathTranslate` y el comando `pdf-math-translate ... --lang`. **Falso:** el paquete PyPI es **`pdf2zh`** y el CLI es `pdf2zh`.

**Repo:** `https://github.com/PDFMathTranslate/PDFMathTranslate` (MIT, Python, ~37K⭐). Demo online: `pdf2zh.com`.

## When to Use

- Cuando pidas **traducir un PDF manteniendo las fórmulas matemáticas** (LaTeX), el layout y las referencias entre páginas.
- Para documentos científicos/matemáticos con ecuaciones.

## Uso

```bash
pip install pdf2zh
# CLI: origen (-li) y destino (-lo) de idioma, salida (-o)
pdf2zh document.pdf -li en -lo zh
# GUI interactiva:
pdf2zh -i
```

Servicios de traducción soportados: **Google, DeepL, Ollama, OpenAI, MiniMax, BabelDOC** (+ demodemo online). No se limita a Google/DeepL.

## Pitfalls

- Instalar **`pdf2zh`**, nunca `PDFMathTranslate`. El comando es `pdf2zh`, no `pdf-math-translate`.
- No hay un flag `--lang src->dst`; es `-li`/`-lo`.
- La calidad de la traducción depende del servicio elegido (Ollama/OpenAI para local, Google/DeepL para cloud).

## Verificación

- Traducir un PDF con ecuaciones; comprobar que las fórmulas se conservan como LaTeX legible y el orden del documento no se rompe.
