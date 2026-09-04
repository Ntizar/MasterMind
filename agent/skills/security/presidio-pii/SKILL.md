---
name: presidio-pii
version: "1.0.0"
description: "Presidio — framework de Microsoft para detección y anonimización de PII (datos personales) en texto e imágenes. 8.6K⭐. Análisis, redacción, masking."
tags: [security, privacy, pii, data-protection, microsoft, ner, anonymization]
---

# Presidio — PII Detection & Anonymization

## Resumen

Presidio (de Microsoft) es un framework open-source para **detectar, redactar, enmascarar y anonimizar datos personales (PII)** en texto e imágenes.

## Componentes

| Componente | Descripción |
|------------|-------------|
| **Analyzer** | Detecta PII (nombres, DNI, emails, teléfonos, IBAN, etc.) |
| **Anonymizer** | Redacta/enmascara/sustituye las PII detectadas |
| **Image Redactor** | Detecta y oculta PII en imágenes (OCR + NER) |

## Instalación

```bash
pip install presidio-analyzer
pip install presidio-anonymizer
pip install presidio-image-redactor
```

## Uso básico

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Análisis
analyzer = AnalyzerEngine()
results = analyzer.analyze(text="Mi email es david@example.com y mi teléfono es +34 612345678", language="es")

# Anonimización
anonymizer = AnonymizerEngine()
anonymized = anonymizer.anonymize(text="Mi email es david@example.com...", analyzer_results=results)
```

## Reconocedores disponibles

- DNI/NIE, NIF, NSS, Pasaporte, IBAN
- Email, Teléfono, URL, IP
- Nombre de persona (NER), Localización
- Tarjetas de crédito, coordenadas bancarias

## Integración con Mastermind

- Para skills que procesen PDFs/documentos (liteparse, markitdown)
- Proteger datos personales antes de logging
- Anonimizar datasets de entrenamiento

## Referencia

- Repo: `microsoft/presidio`
- Docs: https://microsoft.github.io/presidio/

## Comparativa de alternativas

- **[data-privacy-stack/presidio](https://github.com/data-privacy-stack/presidio)** — de-identificación PII multi-idioma tanto sobre texto como sobre imágenes con OCR (este skill solo cubre texto); extiende el caso de uso a documentos escaneados/imágenes.