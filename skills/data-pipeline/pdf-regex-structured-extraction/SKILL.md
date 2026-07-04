---
name: pdf-regex-structured-extraction
version: "1.0.0"
category: data-pipeline
description: Extrae datos estructurados de informes PDF gubernamentales o técnicos usando PyMuPDF + regex, sin LLM ni cloud. Genera CSV plano y/o JSON anidado para visualización offline.
---

# PDF Regex → Structured Data (CSV/JSON)

Extrae datos estructurados de informes PDF gubernamentales o técnicos usando PyMuPDF + regex, sin LLM ni cloud. Genera CSV plano y/o JSON anidado para visualización offline.

## Cuándo usar este enfoque (vs LLM)

- **Formato predecible**: El PDF tiene estructura repetible (informes oficiales, formularios).
- **Sin dependencias cloud**: Entorno local, sin API keys.
- **Volumen alto**: Cientos de PDFs donde LLM sería caro/lento.
- **Precisión determinística**: Regex produce resultados reproducibles.

Si el PDF no tiene estructura predecible (scans, formatos variables), usar `pdf-llm-extraction` en su lugar.

## Arquitectura canónica

```
scripts/
├── extract.py        # Extractor core: PDF → dict Python (una función por campo)
└── extract_csv.py    # Importa extract.py, añade solo lógica de aplanado CSV
```

**Regla crítica**: NUNCA duplicar funciones extractoras entre scripts. `extract_csv.py` importa de `extract.py`:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract import (
    extract_pdf_text, extract_expediente_id, extract_type,
    extract_summary, extract_conclusions, extract_recommendations,
    # ... una función por campo
)
```

## Pasos del pipeline

1. **Extracción de texto**: `fitz.open(path)` → `page.get_text()` por página → join con `\n`.
2. **Metadatos**: Expediente, año, tipo, gravedad, fecha — regex sobre primeras 5000 chars.
3. **Ubicación**: Estación/provincia — regex sobre título o primeras páginas.
4. **Resumen**: Buscar sección "RESUMEN\n" (con salto de línea) — filtrar TOC por word count y dot ratio.
5. **Conclusiones**: Buscar "FACTORES CAUSALES" o "CONCLUSIONES" — extraer viñetas `•`.
6. **Recomendaciones**: Buscar tabla con header "Destinatario|Implementador|Número|Recomendación" — parsear por líneas ancla (número de rec).
7. **Deduplicación**: Trackear expedientes vistos en un `set()`, saltar duplicados.
8. **Aplanado CSV**: Arrays → columnas prefijadas (`rec_1_numero`, `rec_1_texto`...).
9. **Escritura**: CSV con `utf-8-sig` (BOM para Excel), JSON con `ensure_ascii=False`.

## Aplanado JSON → CSV

Arrays anidados se aplanan en columnas numeradas:

```python
# JSON: recomendaciones: [{numero, destinatario, implementador, texto}, ...]
# CSV:  rec_1_numero, rec_1_destinatario, rec_1_implementador, rec_1_texto
#       rec_2_numero, rec_2_destinatario, ...
```

- Máximo N columnas por array (típicamente 10-20).
- Rellenar con strings vacíos si hay menos elementos.
- Arrays de strings (conclusiones, tags) → join con separador (` | ` o `, `).

## Pitfalls críticos

### P1 — Backtracking catastrófico en regex

`[\s\S]*?` sobre texto completo de PDF (50K+ chars) puede colgar el script indefinidamente.

**Fix**: Limitar el scope de búsqueda:
```python
# MAL: re.search(r'RESUMEN[\s\S]*?RECOMENDACIONES', full_text)
# BIEN: re.search(r'RESUMEN\s*\n\s*([A-Z][\s\S]{199,3999})', text[pos:])
#       con bucle incremental y validación de word_count/dot_ratio
```

### P2 — Doble escape en raw strings

`r'(\\d{4})'` dentro de un raw string matchea literal `\d`, no dígitos. Debe ser `r'(\d{4})'`.

Este bug pasó desapercibido en código duplicado — otro motivo para NO duplicar funciones.

### P3 — file:// bloquea fetch() y CDN

El visor HTML debe funcionar con doble clic (file://). Problemas:
- `fetch('datos.csv')` → bloqueado por CORS en file://
- `<script src="https://cdn...">` → no carga sin internet

**Fix**:
- Descargar libs JS (PapaParse, etc.) localmente y referenciar con ruta relativa.
- Para auto-load en file://, usar `XMLHttpRequest` con check `status === 0 && responseText.length > 0`.
- Siempre tener fallback de upload manual (drag & drop o `<input type="file">`).

### P4 — TOC confunde al extractor

Los informes tienen índices con "1. RESUMEN ........... 5" que matchean patrones de sección.

**Fix**: Validar que el contenido después del header tenga >20 palabras y <15% de puntos (dot ratio).

### P5 — Año del expediente ≠ año del suceso

Informes antiguos reabiertos tienen `expediente: 0055/2017` pero `fecha_suceso: 2024-10-29`.

**Fix**: Si `abs(año_fecha - año_expediente) > 2`, usar año de la fecha.

### P6 — Versión bilingüe duplica recomendaciones

Informes CIAF tienen tabla de recomendaciones en español e inglés con el mismo patrón de número.

**Fix**: Filtrar por contexto — versión española tiene "AESF", inglesa tiene "(NSA-ES)".

## Visor HTML offline

Estructura canónica del visor:
- **PapaParse local** (no CDN) para parsear CSV en el navegador.
- **Auto-load** con XHR + fallback a drag&drop.
- **Tabla con sorting** por columna (data-sort attribute + click handler).
- **Filtros**: búsqueda text, select de tipo, select de año.
- **Modal de detalle**: meta grid + resumen + conclusiones + recomendaciones + tags.
- **Stats bar**: KPIs calculados dinámicamente (total, accidentes, víctimas, recomendaciones).

## Auditoría de proyectos de extracción

Checklist al auditar un pipeline PDF→datos:
- [ ] ¿Hay código duplicado entre extractores? → Unificar con imports.
- [ ] ¿Todos los campos del JSON están en el CSV? → Comparar keys.
- [ ] ¿Funciona offline (file://)? → Bundle JS local, no CDN.
- [ ] ¿Hay deduplicación? → Track de IDs vistos.
- [ ] ¿Regex seguro? → No `[\s\S]*?` sobre texto completo.
- [ ] ¿Encoding correcto? → `utf-8-sig` para CSV (Excel), `utf-8` para JSON.

## Referencias

- `references/ciaf-extraction-patterns.md` — Patrones regex específicos para informes CIAF, estructura de campos, y ejemplos de PDFs reales.
