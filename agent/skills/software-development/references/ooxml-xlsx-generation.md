# Generación manual de archivos XLSX (OOXML puro)

Generar archivos Excel sin openpyxl, pandas ni xlsxwriter. Solo `zipfile` + `xml.sax.saxutils`.

## Por qué funciona

Un `.xlsx` es un archivo ZIP que contiene archivos XML siguiendo la especificación OOXML. Python puede crearlo directamente con `zipfile.ZipFile`.

## Estructura del paquete XLSX

```
archivo.xlsx (ZIP)
├── [Content_Types].xml            ← Descriptor MIME del paquete
├── _rels/
│   └── .rels                      ← Relaciones raíz (conecta con workbook)
└── xl/
    ├── workbook.xml               ← Define hojas del libro
    ├── _rels/
    │   └── workbook.xml.rels      ← Relaciones del libro → hojas
    ├── sharedStrings.xml          ← (Opcional) Cadenas compartidas
    └── worksheets/
        └── sheet1.xml             ← Datos de la hoja
```

## Decisiones clave

### inlineStr vs sharedStrings

- **sharedStrings.xml**: Archivo global con índice de todas las cadenas. Más eficiente para libros con muchas celdas repetidas, pero requiere generar un archivo adicional y mantener un mapa de índices.
- **inlineStr**: Cada celda lleva su texto embebido (`<c t="inlineStr"><is><t>texto</t></is></c>`). Más simple, ideal para listas simples donde cada celda es única.
- **Recomendación para listados**: Usar inlineStr. Menos complejidad, menos archivos, mismo resultado.

### Escape de caracteres XML

Caracteres que deben escaparse con `xml.sax.saxutils.escape()`:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`

Sin escape, nombres como "informe&2.pdf" o "datos < 2024.pdf" corrompen el XML y Excel no puede abrir el archivo.

## Template mínimo funcional

```python
import zipfile
from xml.sax.saxutils import escape

def crear_xlsx(ruta_salida, datos):
    """
    datos: lista de diccionarios. Cada dict = una fila.
    Claves del primer dict = columnas.
    """
    columnas = list(datos[0].keys()) if datos else []

    def content_types():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '</Types>'
        )

    def rels():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'
        )

    def workbook():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Datos" sheetId="1" r:id="rId1"/></sheets>'
            '</workbook>'
        )

    def workbook_rels():
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '</Relationships>'
        )

    def sheet(datos, columnas):
        lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
            '<sheetData>',
        ]
        # Fila de encabezados
        header_cells = ''.join(
            f'<c r="{chr(65+i)}1" t="inlineStr"><is><t>{escape(col)}</t></is></c>'
            for i, col in enumerate(columnas)
        )
        lines.append(f'<row r="1">{header_cells}</row>')
        # Filas de datos
        for row_idx, fila in enumerate(datos, start=2):
            cells = ''.join(
                f'<c r="{chr(65+i)}{row_idx}" t="inlineStr"><is><t>{escape(str(fila.get(col, "")))}</t></is></c>'
                for i, col in enumerate(columnas)
            )
            lines.append(f'<row r="{row_idx}">{cells}</row>')
        lines.append('</sheetData></worksheet>')
        return '\n'.join(lines)

    with zipfile.ZipFile(ruta_salida, 'w', zipfile.ZIP_DEFLATED) as xlsx:
        xlsx.writestr('[Content_Types].xml', content_types())
        xlsx.writestr('_rels/.rels', rels())
        xlsx.writestr('xl/workbook.xml', workbook())
        xlsx.writestr('xl/_rels/workbook.xml.rels', workbook_rels())
        xlsx.writestr('xl/worksheets/sheet1.xml', sheet(datos, columnas))
```

## Limitaciones conocidas

- **Solo 26 columnas** (A-Z) con el mapeo `chr(65+i)`. Para más columnas, generar columnas de 2 letras: `AA, AB, ...`.
- **Sin formato** (colores, bordes, anchos de columna). Para eso se necesitan atributos adicionales en los `<c>` y `<row>`.
- **Sin fórmulas**. Solo valores literales en inlineStr.
- **Sin merge de celdas**. Cada celda es independiente.

## Verificación

Para validar que el XLSX generado es válido:
1. Abrirlo en Excel / LibreOffice Calc
2. Verificar con: `python -c "import zipfile; z=zipfile.ZipFile('test.xlsx'); print(z.namelist())"`
3. Inspeccionar el XML: `python -c "import zipfile; print(zipfile.ZipFile('test.xlsx').read('xl/worksheets/sheet1.xml').decode()[:500])"`
