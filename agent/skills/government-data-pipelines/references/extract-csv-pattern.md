# CIAF Tool CSV Extractor

Extracts structured data from CIAF PDF reports into flat CSV for non-technical users.

## Usage

```bash
python3 scripts/extract_csv.py <archivo.pdf> --output CIAF-datos.csv
python3 scripts/extract_csv.py <directorio_pdfs> --output CIAF-datos.csv
```

## Output CSV columns

- `id` — year-expediente
- `year`, `expediente`, `titulo`, `tipo`, `gravedad`
- `fecha_suceso`, `estacion`, `provincia`
- `resumen` — texto completo
- `conclusiones` — separadas por |
- `entidades`, `tags`
- `num_conclusiones`, `num_recomendaciones`
- `rec_1_numero`..`rec_10_texto` — recomendaciones aplanadas

## Key functions

- `extract_pdf_text()` — full text extraction via PyMuPDF
- `extract_expediente_id()` — expediente number (4 patterns)
- `extract_title_and_date()` — title + incident date
- `extract_station_and_province()` — location
- `extract_summary()` — section 1 RESUMEN
- `extract_conclusions()` — causal/contributing factors
- `extract_recommendations()` — table parsing by anchor number
- `extract_tags()` — common cause tags
- `extract_entities()` — known railway entities

## Verification

After extracting, compare CSV fields against JSON output to ensure data integrity.
Key fields to verify: expediente, fecha_suceso, resumen length, conclusiones count, recomendaciones (all fields match).
