# BOE HTML Parsing — Leyes y Disposiciones Formales

## Contexto

El BOE ofrece texto plano de leyes y disposiciones en `https://www.boe.es/diario_boe/txt.php?id=BOE-A-XXXX-XXXXX`. Este formato es HTML pero con el texto completo del documento, no un PDF.

## Ejemplo real: ContrataPúblico (Sesión 1)

**Ley:** Ley 9/2017, de 8 de noviembre, de Contratos del Sector Público
**URL BOE:** `https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-12902`
**Tamaño:** ~1.7MB HTML
**Resultado:** 347 artículos parseados → `js/ley-data.js` (733KB) + `data/ley-texto.json` (1MB)

## Patrón de parsing

1. **Descargar:** `curl -s "https://www.boe.es/diario_boe/txt.php?id=BOE-A-2017-12902"`
2. **Extraer `<body>`:** Ignorar `<meta>` tags antes del body
3. **Split por `<p>`:** Cada párrafo es un bloque de texto
4. **Clasificar:** Regex para detectar "Artículo", "Libro", "Título", "Capítulo", "Sección"
5. **Acumular:** Texto entre artículos = contenido del artículo
6. **Generar:** `ley-data.js` (estructura + funciones JS) + `ley-texto.json` (texto completo)

## Entidades HTML a decodificar

```python
text = text.replace('&eacute;', 'é')
text = text.replace('&iacute;', 'í')
text = text.replace('&oacute;', 'ó')
text = text.replace('&uacute;', 'ú')
text = text.replace('&ntilde;', 'ñ')
text = text.replace('&aacute;', 'á')
text = text.replace('&quot;', '"')
text = text.replace('&nbsp;', ' ')
text = text.replace('&amp;', '&')
```

## Regex de detección

```python
# Artículo: "Artículo 1. Objeto y finalidad."
re.search(r'Artículo\s+([\dIIVX]+)\.\s*(.+)', text)

# Libro: "Libro primero."
re.search(r'Libro\s+(primero|segundo|tercero|cuarto|quinto|sexto)', text)

# Título: "Título Preliminar."
re.search(r'Título\s+(\w+)\.', text)

# Capítulo: "Capítulo I."
re.search(r'Capítulo\s+(\w+)\.', text)

# Sección: "Sección 1.ª"
re.search(r'Sección\s+([\w\.]+)\.', text)
```

## Output esperado

- `ley-data.js`: Objeto `LEY_DATA` con estructura navegable + funciones JS (`buscarArticulos()`, `getArticulo()`, etc.)
- `ley-texto.json`: Dict `{articulo_numero: texto_completo}`
