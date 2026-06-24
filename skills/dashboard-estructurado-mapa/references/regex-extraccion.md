# Regex para extracción de datos de documentos oficiales

## Patrones comunes para informes oficiales (CIAF y similares)

### ID del informe
```python
# Patrón principal: IF-XX-YYYY o IF XX/YYYY
re.search(r'IF[-/](\d+)[-/](\d{4})', text)
re.search(r'IF\s+(\d+)\s*/\s*(\d{4})', text)
```

### Coordenadas (frontmatter YAML)
```python
# Leer bloque completo
re.search(r'^ubicacion:\s*\n((?:\s+.+\n)*)', fm, re.MULTILINE)
# Extraer array [lat, lng]
re.search(r'\s+coordenadas:\s*\[([^\]]+)\]', block)
parts = [p.strip() for p in match.group(1).split(',')]
```

### Estación y ubicación
```python
# Estación
re.search(r'estación\s+de\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]+?)', text)
# Provincia
re.search(r'provincia\s+[:=]?\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)', text)
# Comunidad
re.search(r'comunidad\s+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s]+?)', text)
```

### Datos técnicos
```python
# PK (punto kilométrico)
re.search(r'PK\s+([\d,]+\+[\d,]+)', text)
# Expediente
re.search(r'(\d{2,3})\s*/\s*(\d{4})', text)
# Fecha completa
re.search(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', text)
```

## Pitfall: IDs duplicados

El bug más común: la regex `IF\s*[-/]?\d+` captura el año en vez del número del informe.

**Incorrecto:** `IF 2025` → ID = "2025" (sobrescribe otros informes del mismo año)
**Correcto:** `IF[-/](\d+)[-/](\d{4})` → ID = "41" del patrón "IF-41-2025"

Si no se encuentra el patrón, fallback al expediente: `(\d{2,3})\s*/\s*(\d{4})`.
