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

### Cross-Repo Matching Pitfall
- CIAF-visor IDs: `2008-0022/2008`
- ciaf-data IDs: `IF-0022-2008`
- Matching by expediente number alone: 118/269 errors (44%)
- Matching by year + station + date: reliable but slow
- Lesson: NEVER assume IDs match across repos

### JSON-to-PDF Verification Audit (Junio 2026)

Auditoría completa de los 270 JSONs contra los 277 PDFs originales en `/root/workspace/CIAF/`.

**Metodología:** Para cada JSON, extraer texto del PDF con PyMuPDF y verificar 6 campos:
1. Título (palabras significativas >5 chars deben aparecer)
2. Fecha (probar formatos YYYY-MM-DD, DD/MM/YYYY, "DD de mes de YYYY")
3. Estación (nombre simple en minúsculas)
4. Víctimas (número o phrase "sin víctimas")
5. Resumen (>50% palabras del resumen en PDF)
6. Conclusiones (>50% palabras en PDF)

**Resultados:**
| Score | Cantidad | % |
|-------|----------|---|
| EXCELENTE (≥80%) | 244 | 92.4% |
| BUENO (60-79%) | 8 | 3.0% |
| REGULAR (40-59%) | 11 | 4.2% |
| MALO (<40%) | 1 | 0.4% |

**Estadísticas:** Media 87.3%, Mediana 88.3%, Mínimo 38.7%, Máximo 100%

**Errores detectados:**
- 6 JSONs sin PDF accesible (todos de 2009, pdf_path apunta a `0056CIAF.pdf` — error de emparejamiento)
- 12 informes de 2010 con calidad regular (posible formato PDF diferente)
- 25 casos de víctimas inconsistentes (suma subcategorías > total)

**Ubicación de PDFs:**
- `/root/workspace/CIAF/` — 277 PDFs (fuente real, organizados por año)
- `/root/workspace/ciaf-data/pdfs/` — solo 38 PDFs (NO usar como fuente)
- `/root/workspace/CIAF-visor/pdfs/` — copia del visor

### CIAF-visor Data Enrichment Pattern

El visor CIAF usa un esquema más rico que ciaf-data:

| Campo Visor | Campo CIAF-data |
|-------------|-----------------|
| `ubicacion.lat/lng` | `lat`, `lng` |
| `ubicacion.estacion` | `estacion` |
| `consecuencias.victimas_mortales` | `victimas_fallecidos` |
| `analisis.resumen` | `resumen` |
| `expediente` | `id` (formato diferente) |

**Matching:** Extraer número de expediente del título con regex `r'Nº?\s*(\d{3,4}/\d{4})'` — funciona para 238/270 informes (88%).

**Enriquecimiento:** Añadir campos detallados de ciaf-data al visor:
- `victimas_fallecidos`, `victimas_graves`, `victimas_leves`, `victimas_heridos`
- `hora`, `pk`, `tramo`, `trenes`
- Coordenadas GPS verificadas

**Resultado:** 269 informes en visor, 238 enriquecidos (88%), 194 con coordenadas (72%).

### Scripts Created
- `reextract-resumenes.py` — Batch re-extraction of deficient resúmenes
- `batch-final.py` — Original batch processing (270 PDFs)
