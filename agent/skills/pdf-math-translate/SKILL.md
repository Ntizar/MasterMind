---
name: pdf-math-translate
description: PDF Math Translate — traducción de PDFs matemáticos/académicos manteniendo fórmulas y formato.
category: data-pipeline
---

# PDF Math Translate — Traducción de PDFs Académicos

## Qué es

PDF Math Translate es una herramienta para traducir PDFs académicos manteniendo fórmulas:
- **Formula preservation** — las fórmulas matemáticas se mantienen intactas
- **Layout preservation** — el formato original se conserva
- **Academic-focused** — optimizado para papers académicos
- **Multi-idioma** — traducción entre múltiples idiomas

## Instalación

```bash
pip install PDFMathTranslate
# O usar CLI
pdf-math-translate input.pdf output.pdf --lang src->dst
```

## Casos de uso para David

- **Paper translation** — traducir papers académicos
- **Learning** — leer papers en otros idiomas
- **Documentation** — traducir documentación técnica
- **Research** — acceder a papers en chino/otros idiomas

## Pitfalls

- Lento para PDFs grandes
- Requiere conexión a API de traducción (Google/DeepL)
- Las fórmulas complejas pueden no traducirse bien
- Output puede necesitar revisión manual

## Referencias

- Repo: `github.com/PDFMathTranslate/PDFMathTranslate` (35K⭐)
