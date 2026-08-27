# Page-Based PDF Extraction — Patrones Verificados

## Por qué extracción por páginas > regex sobre texto completo

El regex sobre texto completo falla en informes CIAF porque:
1. **TOC se confunde con contenido** — el índice tiene "1. RESUMEN .....5" que matchea como sección
2. **Headers/footers se mezclan** — "Comisión de Investigación de Accidentes Ferroviarios" aparece en cada página
3. **Bilingüismo** — informes 2014+ tienen sección inglesa al final que contamina extracción

## Resultados comparativos (verificado 2026-06-26)

| Métrica | Regex completo | Por páginas |
|---------|---------------|-------------|
| Títulos | ~60% | **100%** |
| Conclusiones | ~30% | **70%** |
| Recomendaciones | ~10% | **54%** |
| Coordenadas | 0% (Nominatim blocked) | **71%** (local coords) |

## Código base

```python
import fitz, re

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = [page.get_text() for page in doc]
    doc.close()
    return pages

def find_section_pages(pages):
    section_pages = {}
    for i, text in enumerate(pages):
        if i < 2: continue  # Skip cover + warning
        if re.search(r'\.{10,}', text): continue  # Skip TOC
        for m in re.finditer(r'(?:^|\n)\s*(\d+)\.\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{5,40})', text):
            num = int(m.group(1))
            if num not in section_pages:
                section_pages[num] = i
    return section_pages

def get_pages_text(pages, start, end):
    text = ""
    for i in range(start, min(end, len(pages))):
        pt = pages[i]
        # Clean per-page headers/footers
        pt = re.sub(r'Comisión de Investigación de\s*Accidentes Ferroviarios', '', pt)
        pt = re.sub(r'Informe Final de la CIAF\s+\d+/\d{4}', '', pt)
        pt = re.sub(r'^\s*\d{1,2}\s*$', '', pt, flags=re.MULTILINE)
        pt = re.sub(r'^.*\.{10,}.*$', '', pt, flags=re.MULTILINE)
        text += pt + "\n"
    return text.strip()
```

## Detección de TOC

Líneas con 10+ puntos consecutivos = entradas de índice:
```python
if re.search(r'\.{10,}', page_text):
    # Skip this page for section detection
    continue
```

## Manejo de bilingüismo

Cortar antes de sección inglesa:
```python
for i in range(start + 1, min(start + 5, len(pages))):
    if re.search(r'SAFETY\s+RECOMMENDATIONS|English\s+summary', pages[i], re.IGNORECASE):
        end = i
        break
```

## Formatos de recomendación por era

| Era | Años | Formato número | Ejemplo |
|-----|------|----------------|---------|
| Pre-RD 810 | 2007-2008 | Libre | Sin recomendaciones formales |
| RD 810 | 2009-2013 | `XX/YY-Z` | `11/09-1` |
| RD 623 | 2014-2025 | `XX/YYYY-Z` | `64/2024-1` |

Regex universal: `\d+/\d{2,4}-\d+`

## Script completo

`/root/workspace/CIAF-visor/scripts/parse_year_v2.py` — parser funcional con:
- Extracción por páginas
- Geocoding local (328 estaciones)
- Manejo de 3 eras
- Detección de bilingüismo
- Province-by-station
