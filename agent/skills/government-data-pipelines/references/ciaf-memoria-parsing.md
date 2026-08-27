# CIAF — Parseo de Memorias Anuales

## Diferencia con informes individuales

Las memorias anuales CIAF son documentos de **resumen estadístico** (NO investigaciones individuales). Contienen:
- Totales de accidentes/incidentes del año
- Estadísticas de víctimas
- Principales causas
- Entidades más involucradas
- Comparativas con años anteriores

**Alcance:** Las memorias cubren TODOS los incidentes ferroviarios del año, los informes JSON solo los INVESTIGADOS por la CIAF. Por eso los números son diferentes (ej: memoria 2024 dice 97 accidentes, pero solo 3 informes individuales).

## Fuentes

- PDFs en: `pdfs/memorias/CIAF_Memoria_YYYY.pdf`
- Años disponibles: 2008-2024 (17 memorias)
- **NO existe memoria 2007** (aunque hay 4 informes de ese año)
- **NO existe memoria 2025** (año incompleto)

## Schema de salida

```json
{
  "year": 2024,
  "title": "Memoria Anual CIAF 2024",
  "summary": "Resumen de 2-3 oraciones...",
  "total_accidents": 97,
  "total_incidents": 29,
  "total_fatal": 18,
  "total_victims": 33,
  "total_heridos": 24,
  "total_material_damage_eur": null,
  "top_causes": [{"cause": "Factor humano", "count": 45}],
  "top_entities": [{"entity": "ADIF", "count": 30}],
  "highlights": "..."
}
```

## Campos que pueden quedar null

- `total_material_damage_eur`: No siempre está en el PDF
- `total_fatal` / `total_victims` / `total_heridos`: En memorias antiguas (2009, 2011-2013) el formato no permite extraer estos números
- **Usar null, NUNCA fabricar datos**

## Extracción con PyMuPDF

```python
import fitz

doc = fitz.open(f"pdfs/memorias/CIAF_Memoria_{year}.pdf")
text = "\n".join(page.get_text() for page in doc)
doc.close()

# Buscar tabla de saldos estadísticos
# Secciones típicas: "ACCIDENTES E INCIDENTES", "SALDOS ESTADÍSTICOS"
# La info suele estar en las primeras 10-15 páginas
```

## Validación post-parseo

```python
# 1. Verificar que cada JSON tiene un PDF correspondiente
import os
for year in range(2008, 2025):
    pdf = f"pdfs/memorias/CIAF_Memoria_{year}.pdf"
    json_f = f"data/memorias/{year}.json"
    if not os.path.exists(pdf):
        print(f"⚠️ {year}: sin PDF fuente — eliminar JSON si existe")
    elif os.path.exists(json_f):
        with open(json_f) as f:
            m = json.load(f)
        if m.get('total_accidents') is None:
            print(f"⚠️ {year}: total_accidents es null — verificar parseo")

# 2. Rangos razonables
# Accidentes: 40-120/año
# Víctimas fatales: 0-25/año
# Si un número está fuera de rango, revisar el parseo
```

## Frontend: selector de años

El selector de memorias SOLO debe mostrar años con PDF real:
```javascript
const MEMORIA_YEARS = [2024, 2023, ..., 2008]; // NO incluir 2025 ni 2007
```

## Relación memorias ↔ informes

Las memorias e informes individuales son **complementarios**, no contradictorios:
- Memoria = resumen anual de TODOS los incidentes (más numeros)
- Informes = investigaciones individuales de incidentes seleccionados (menos numeros)
- No intentar "reconciliar" los números — son alcances diferentes
