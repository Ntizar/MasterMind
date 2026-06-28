# Quality Audit — Government Data Pipelines

## Post-Extraction Quality Audit (CIAF verified 2026-06-27)

After batch processing, ALWAYS audit quality before declaring success.

### Audit Checklist

1. **Resúmenes**: Should be executive summaries (2-3 sentences), NOT descriptions ("El día X...")
   - Good: 50-500 chars, starts with event type
   - Bad: >500 chars, starts with "El día"
   - Threshold: 80%+ should be "good"

2. **Conclusiones**: Should have ≥2 per report
   - If many reports have 0-1, the extraction missed the section

3. **Recomendaciones**: Should have ≥1 per report
   - If many are empty, check if the PDF has them (some pre-2014 reports don't)

4. **Fechas**: All should be ISO format (YYYY-MM-DD)
   - Check for empty dates on reports with known dates

5. **Estaciones**: Should be clean names (not full sentences)
   - Flag any >35 chars or containing verbs

### Re-extraction Pattern

When a field has low quality but the PDF has the data:

```python
def reextract_field(reports_dir, pdf_dir, field, classify_fn, llm_fn):
    """Re-extract a specific field for deficient reports."""
    deficient = []
    for f in os.listdir(reports_dir):
        with open(os.path.join(reports_dir, f)) as fh:
            r = json.load(fh)
        if classify_fn(r.get(field, "")) in ("empty", "bad"):
            deficient.append(r)
    
    print(f"Re-extracting {len(deficient)} deficient {field}s...")
    for r in deficient:
        text = extract_pdf_text(r, pdf_dir)
        new_value = llm_fn(text, r)
        r[field] = new_value
        save_report(r)
```

### Cross-Repo Matching Pitfall

When two repos have the same data with different IDs:
- CIAF-visor: `2008-0022/2008`
- ciaf-data: `IF-0022-2008`

**NEVER match by ID alone** (44% error rate). Use multi-criteria scoring:
- Year match: +10
- Expedition number: +20
- Date match: +15
- Station name: +5
- Minimum score for valid match: 10

### Quality Metrics Table

| Field | Metric | Good Threshold |
|-------|--------|---------------|
| resumen | Length | 50-500 chars |
| resumen | Pattern | NOT "El día..." |
| conclusiones | Count | ≥ 2 |
| recomendaciones | Count | ≥ 1 |
| fecha | Format | ISO YYYY-MM-DD |
| victimas | Type | int ≥ 0 |
| estacion | Length | < 35 chars |
