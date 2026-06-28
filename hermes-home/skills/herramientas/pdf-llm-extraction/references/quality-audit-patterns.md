# Quality Audit Patterns — PDF Data Extraction

## Audit Results (CIAF 270 PDFs)

### Initial State (before re-extract)
| Metric | Value |
|--------|-------|
| Total reports | 270 |
| Good resúmenes (executive) | 16/270 (5%) |
| Descriptions (bad) | 254/270 (94%) |
| With conclusiones | 270/270 (100%) |
| With recomendaciones | 218/270 (80%) |
| Total conclusiones | 713 |
| Total recomendaciones | 438 |

### After Re-extract
| Metric | Value |
|--------|-------|
| Good resúmenes | 245/270 (90%) |
| Descriptions (bad) | 25/270 (9%) |
| Time | 21m52s |
| Success rate | 94% (250/267) |
| Errors (empty LLM response) | 17 |

### Re-extract Prompt Used
```
Eres un analista de seguridad ferroviaria de la CIAF.

Extrae un RESUMEN EJECUTIVO del siguiente informe. El resumen debe:
1. Tener MÁXIMO 3 oraciones
2. Empezar con el tipo de suceso (accidente, incidente, etc.)
3. Incluir la ubicación y fecha
4. Mencionar las consecuencias (víctimas, daños)
5. Indicar la causa principal si se menciona
6. Ser conciso y profesional

CONTEXTO: {context}
TEXTO: {truncated}

Devuelve SOLO el resumen ejecutivo, sin comillas ni formato adicional.
```

### Cross-Repo Matching Pitfall
- CIAF-visor IDs: `2008-0022/2008`
- ciaf-data IDs: `IF-0022-2008`
- Matching by expediente number alone: 118/269 errors (44%)
- Matching by year + station + date: reliable but slow
- Lesson: NEVER assume IDs match across repos

### Scripts Created
- `reextract-resumenes.py` — Batch re-extraction of deficient resúmenes
- `batch-final.py` — Original batch processing (270 PDFs)
