---
name: presidio-pii
description: "Usa a anonimizar PII con Presidio (texto e imágenes)."
version: "2.0.0"
tags: [presidio, pii, anonimizacion, privacidad, ner, imagen, python]
related_skills: [presidio-pii, llm-guardrails-policy, security]
---

# Presidio — anonimización de PII (texto e imágenes)

> ⚠️ Corrección 2026-09-05 (auditoría): el repo se movió a **`data-privacy-stack/presidio`** (microsoft/presidio redirige; mismo proyecto, nuevo hogar). Presidio **NO es solo texto** — incluye **Image Redactor** (PII en imágenes vía OCR+NER). Stars ~10.7K.

**Repo:** `https://github.com/data-privacy-stack/presidio` (Python, ~10.7K⭐).

## When to Use

- Cuando pidas **detectar y anonimizar PII** (NLP/NER + Image Redactor) en texto, imágenes o documentos.

## Qué es

Framework de Microsoft (ahora en data-privacy-stack) para **anonimización de datos personales**: análisis NER con `presidio-analyzer`, anonimización con `presidio-anonymizer`, y **presidio-image-redactor** para PII en imágenes.

## Uso

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
results = AnalyzerEngine().analyze(text=text, language='es')
anonymized = AnonymizerEngine().anonymize(text=text, analyzer_results=results)
```

## Pitfalls

- Repo actual: **data-privacy-stack/presidio** (no lo dupliques como "alternativa").
- Cubre **texto E imágenes** (Image Redactor) — no solo texto.

## Verificación

- Analizar/anonimizar un texto con NER y probar una imagen con `presidio-image-redactor`.
