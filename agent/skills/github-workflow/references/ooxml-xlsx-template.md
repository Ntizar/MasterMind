# Plantilla OOXML XLSX — Generar Excel sin dependencias externas

Genera archivos `.xlsx` válidos usando solo `zipfile` + `xml.sax.saxutils` de la stdlib de Python.

## Estructura del paquete XLSX

Un `.xlsx` es un ZIP con esta estructura:

```
archivo.xlsx (ZIP)
├── [Content_Types].xml        → Descriptor MIME del paquete
├── _rels/
│   └── .rels                  → Relaciones raíz (conecta con workbook.xml)
└── xl/
    ├── workbook.xml           → Definición del libro (nombres de hojas)
    ├── _rels/
    │   └── workbook.xml.rels  → Relaciones del libro (conecta con sheet1.xml)
    └── worksheets/
        └── sheet1.xml         → Datos de la hoja de cálculo
```

## Archivos XML mínimos

### [Content_Types].xml
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
```

### _rels/.rels
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
```

### xl/workbook.xml
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Hoja1" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
```

### xl/_rels/workbook.xml.rels
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
```

### xl/worksheets/sheet1.xml (con inlineStr)
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1"><c r="A1" t="inlineStr"><is><t>Encabezado</t></is></c></row>
    <row r="2"><c r="A2" t="inlineStr"><is><t>Dato 1</t></is></c></row>
    <row r="3"><c r="A3" t="inlineStr"><is><t>Dato 2</t></is></c></row>
  </sheetData>
</worksheet>
```

## Por qué inlineStr y no sharedStrings

- **sharedStrings** requiere un archivo adicional `xl/sharedStrings.xml` con un índice global de todas las cadenas. Más complejo de generar.
- **inlineStr** lleva el texto embebido en la celda. Más directo para archivos simples.
- Para listas grandes (>10K filas), sharedStrings es más eficiente en tamaño. Para uso general, inlineStr es suficiente.

## Escapado XML obligatorio

Caracteres que deben escaparse en contenido XML:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&apos;`

Python: `from xml.sax.saxutils import escape` → `escape("texto & <html>")` → `"texto &amp; &lt;html&gt;"`

## Código Python mínimo

```python
import zipfile
from xml.sax.saxutils import escape

def crear_xlsx(ruta, datos, encabezados=None):
    """Genera XLSX con datos como listas de listas."""
    with zipfile.ZipFile(ruta, 'w', zipfile.ZIP_DEFLATED) as xlsx:
        xlsx.writestr('[Content_Types].xml', CONTENT_TYPES)
        xlsx.writestr('_rels/.rels', RELS)
        xlsx.writestr('xl/workbook.xml', WORKBOOK)
        xlsx.writestr('xl/_rels/workbook.xml.rels', WORKBOOK_RELS)
        
        rows = []
        if encabezados:
            cells = ''.join(
                f'<c r="{chr(65+i)}1" t="inlineStr"><is><t>{escape(h)}</t></is></c>'
                for i, h in enumerate(encabezados)
            )
            rows.append(f'<row r="1">{cells}</row>')
        
        start_row = 2 if encabezados else 1
        for idx, fila in enumerate(datos, start=start_row):
            cells = ''.join(
                f'<c r="{chr(65+i)}{idx}" t="inlineStr"><is><t>{escape(str(c))}</t></is></c>'
                for i, c in enumerate(fila)
            )
            rows.append(f'<row r="{idx}">{cells}</row>')
        
        sheet = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<sheetData>{''.join(rows)}</sheetData>
</worksheet>'''
        xlsx.writestr('xl/worksheets/sheet1.xml', sheet)
```

## Limitaciones conocidas

- Solo genera una hoja (sheet1.xml). Para múltiples hojas, duplicar worksheet.xml y actualizar workbook.xml + workbook.xml.rels.
- No soporta fórmulas, formato de celdas, fusión de celdas, ni gráficos.
- Para esas features, usar openpyxl (pero eso requiere dependencia externa).
- Columnas limitadas a A-Z (26 columnas) con el patrón `chr(65+i)`. Para más columnas, usar lógica de columnas compuestas (AA, AB, etc.).
