# Presto Word Extraction — Patrón para tablas rotas

## Problema

Algunos PDFs Presto modernos (ej: GLAM, 2026) tienen tablas donde la fila del capítulo
entero está en una sola celda. `extract_tables()` devuelve:

```
['01 Capítulo MOVIMIENTO DE TIERRAS 1,00 2.041,83 € 2.041,83 €', '', '', '', '', '', '']
```

Las columnas están vacías porque el PDF las fusionó en una sola celda.

## Solución: Coordenadas X con extract_words()

### Columnas conocidas (GLAM-style)

| Columna | X aprox | Descripción |
|---------|---------|-------------|
| Código | ~52 | Número o código del capítulo |
| Nat | ~109 | Naturaleza |
| Ud | ~129 | Unidad |
| Resumen | ~258 | Descripción |
| CanPres | ~409 | Cantidad |
| PrPres | ~453 | Precio unitario |
| ImpPres | ~501 | Importe total |

### Parseo de números españoles

Los números en formato español usan punto como separador de miles y coma como decimal:
- `"2.041,83"` → 2041.83
- `"117,00"` → 117.00
- `"2 0.316,59"` → 20316.59 (dividido en palabras)

Función de parseo:
```python
def parse_es_amount(s):
    """Convertir string español a float"""
    s = s.replace(' ', '')  # Quitar espacios internos
    if ',' in s:
        # Última coma es decimal, puntos son miles
        return float(s.replace('.', '').replace(',', '.'))
    return float(s.replace('.', ''))
```

### Patrón completo

Ver `references/budget-extraction-pattern.py` para script completo.

## Casos reales

### GLAM (mayo 2026)
- 100 páginas
- 97 capítulos detectados (incluyendo subcapítulos)
- Total: 1.640.711 €
- Tablas rotas → usó extract_words() con coordenadas X

### Trevicon (abril 2026)
- 355 páginas
- Tablas funcionales → usó extract_tables()
- Total: 816.075 €

### CYPE Arquimedes (Nogal 9 ref)
- 336 páginas
- Tablas funcionales → usó extract_tables()
- Total: 523.705 €
