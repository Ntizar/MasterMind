# Auditoría de Calidad JSON vs PDF — Pipeline CIAF

## Ubicaciones de datos

| Tipo | Ruta | Cantidad |
|------|------|----------|
| **JSONs extraídos** | `/root/workspace/ciaf-data/data/individual/*.json` | 270 |
| **PDFs originales** | `/root/workspace/CIAF/{YYYY}/*.pdf` | 277 |
| **PDFs backup (pocos)** | `/root/workspace/ciaf-data/pdfs/{YYYY}/*.pdf` | 38 |

**⚠️ PITFALL CRÍTICO:** No confundir `/root/workspace/ciaf-data/pdfs/` (solo 38 PDFs viejos) con `/root/workspace/CIAF/` (270 PDFs completos organizados por año). Siempre usar `/root/workspace/CIAF/` como fuente.

## Metodología de auditoría

### Emparejamiento JSON → PDF

```python
import re, os

def find_pdf_for_json(json_data, filename):
    """Estrategias de emparejamiento (en orden de prioridad):"""
    
    # 1. Campo pdf_path en el JSON
    pdf_path = json_data.get('pdf_path', '')
    if pdf_path:
        full = os.path.join("/root/workspace/ciaf-data", pdf_path.lstrip('./'))
        if os.path.exists(full):
            return full
    
    # 2. Búsqueda por año + números del filename
    json_año = json_data.get('año', 0)
    numbers = re.findall(r'\d+', filename)
    
    year_pdfs = [f for f in os.listdir(f"/root/workspace/CIAF/{json_año}")
                 if f.endswith('.pdf')]
    
    for pdf in year_pdfs:
        for num in numbers:
            if len(num) >= 3 and num in pdf.lower().replace('.pdf', ''):
                return f"/root/workspace/CIAF/{json_año}/{pdf}"
    
    return None
```

### Comparación campo por campo

```python
import fitz  # PyMuPDF

def audit_json_vs_pdf(json_data, pdf_path):
    """Compara cada campo del JSON contra el texto del PDF"""
    
    doc = fitz.open(pdf_path)
    pdf_text = "\n".join(page.get_text() for page in doc)
    doc.close()
    pdf_lower = pdf_text.lower()
    
    results = {}
    
    # 1. TÍTULO: buscar palabras significativas (>4 chars) del título
    titulo_words = [w.lower() for w in json_data['titulo'].split() if len(w) > 4][:8]
    matches = sum(1 for w in titulo_words if w in pdf_lower)
    results['titulo'] = matches / len(titulo_words)
    
    # 2. FECHA: probar múltiples formatos ISO vs español
    fecha = json_data.get('fecha', '')
    parts = fecha.split('-')  # YYYY-MM-DD
    formats = [
        fecha,  # 2021-08-11
        f"{parts[2]}/{parts[1]}/{parts[0]}",  # 11/08/2021
        f"{parts[2]}.{parts[1]}.{parts[0]}",  # 11.08.2021
    ]
    # También: "11 de agosto de 2021"
    month_map = {'01':'enero','02':'febrero',...,'12':'diciembre'}
    text_date = f"{int(parts[2])} de {month_map[parts[1]]} de {parts[0]}"
    
    # 3. VÍCTIMAS: verificar números en PDF
    victimas = json_data.get('victimas', 0)
    if victimas > 0:
        check = str(victimas) in pdf_text
    else:
        check = any(p in pdf_lower for p in ['sin víctimas', 'sin fallecidos'])
    
    # 4. RESUMEN/CONCLUSIONES: cobertura de palabras clave
    resumen_words = [w.lower() for w in json_data['resumen'].split() if len(w) > 5][:25]
    coverage = sum(1 for w in resumen_words if w in pdf_lower) / len(resumen_words)
    
    return results
```

## Resultados de auditoría (ejecutada 2026-06-28)

### Estadísticas generales

| Métrica | Valor |
|---------|-------|
| JSONs auditados | 264 de 270 (98%) |
| Media de calidad | **87.3%** |
| Mediana | 88.3% |
| Rango | 38.7% - 100% |

### Distribución

| Categoría | Cantidad | % |
|-----------|----------|---|
| EXCELENTE (≥80%) | 244 | 92.4% |
| BUENO (60-79%) | 8 | 3.0% |
| REGULAR (40-59%) | 11 | 4.2% |
| MALO (<40%) | 1 | 0.4% |

### Conclusión

El pipeline de extracción funciona **muy bien**. El 92.4% de los JSONs tiene calidad excelente (≥80% de match contra el PDF original).

## Problemas detectados

### 6 JSONs sin emparejamiento (error de `pdf_path`)

Todos de 2009, apuntan al mismo PDF `0056CIAF.pdf`. Error de naming en el campo `pdf_path`:

```
IF_N_65_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
IF_N_56_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
IF_N_63_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
IF_N_62_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
IF_N_54_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
IF_N_57_CIAF.json  → pdf_path: /root/workspace/CIAF/2009/0056CIAF.pdf  (incorrecto)
```

**Fix:** Emparejar por número de informe (regex del título) en vez de por `pdf_path`.

### 12 informes con calidad regular/malo

La mayoría son de **2010** — posible formato de PDF diferente ese año. Requieren revisión manual puntual.

### Issues de consistencia interna (sin PDF)

| Problema | Casos |
|----------|-------|
| Sin coordenadas GPS | 262 (97%) |
| Sin tags | 39 (14%) |
| Víctimas inconsistentes (suma sub > total) | 25 (9%) |

## Pitfalls

- **Recomendaciones son `dict[]`**, no `string[]`. Formato: `{'numero': '...', 'destinatario': '...', 'texto': '...'}`. Acceder a `rec['texto']`, no `rec.lower()`.
- **Fechas en múltiples formatos:** ISO (YYYY-MM-DD), DD/MM/YYYY, texto español. Siempre probar todos.
- **Campo estación puede ser largo:** A veces incluye PK + tramo completo. Usar solo la primera parte (antes de coma) para matching.
- **PyMuPDF puede fallar con PDFs corruptos:** Envolver en try/except y registrar fallos.
