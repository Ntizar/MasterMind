# Patrones de extracción CIAF — Informes finales

## Estructura del PDF tipo

```
Página 1:  Portada — "INFORME FINAL DE LA CIAF (IFC) 111/2024" + título descriptivo
Página 2:  Índice — "1. RESUMEN ........... 5" (puntos = TOC, filtrar)
Página 5:  1. RESUMEN\n — Párrafo empezando con fecha del suceso
Página 6+: 2. LA INVESTIGACIÓN — Análisis detallado
Página 30+: 5.1. RESUMEN DEL ANÁLISIS Y CONCLUSIONES — Factores causales (viñetas •)
Página 32: RECOMENDACIONES FINALES — Tabla bilingüe ES/EN
Página 34: 7. APPENDIX: ENGLISH SUMMARY — Versión inglesa (filtrar)
```

## Regex por campo

### Expediente
```python
# Formato: IF 111/2024, IF-0111-2024, (IFC) 19/2020, Nº 0017/2015
r'IF[-\s]*(\d{4,5})[-\s](\d{4})'     # → "111/2024"
r'IF\s+(\d+/\d{4})'                   # fallback
r'\(IFC\)\s+(\d+/\d{4})'             # formato 2014-2019
r'[nN][ºo]?\s*(\d{1,4}/\d{4})'       # formato 2007-2013
```

### Fecha del suceso
```python
# "ocurrido el 29 de octubre de 2024" → 2024-10-29
r'ocurrido\s+el\s+(.+?)(?:\n|$)'     # capturar frase de fecha
# Luego parse_date() con meses en español:
# enero=1 ... diciembre=12
```

### Estación y provincia
```python
# "en Álora (Málaga) el" → estacion="Álora", provincia="Málaga"
r'en\s+(\w+(?:\s+\w+){0,2})\s+\((\w+)\)\s+el'
# Validar: 2-25 chars, no palabras descriptivas (colisión, choque, etc.)
```

### Resumen (filtrar TOC)
```python
# Buscar "RESUMEN\n" (con salto de línea) seguido de 200-4000 chars
r'(?:\d+\.\s+)?RESUMEN\s*\n\s*([A-ZÁÉÍÓÚÑa-záéíóúñ][\s\S]{199,3999})'
# Validar: word_count > 20, dot_ratio < 0.15
# Cortar al encontrar "2. LA INVESTIGACIÓN"
```

### Conclusiones (factores causales)
```python
# Buscar "FACTORES CAUSALES" o "CONCLUSIONES"
# Extraer viñetas: r'•\s+([^\n]+(?:\n(?!\s*•\s)[^\n]+){0,2})'
# Stop: "FACTORES CONTRIBUYENTES", "RECOMENDACIONES"
```

### Recomendaciones (tabla bilingüe)
```python
# Header: "Destinatario ... Implementador ... Número ... Recomendación"
# Anchor: r'^\s*\d{3}/\d{4}-\d+\s*$'  (ej: "111/2024-1")
# Destinatario: línea N-2, Implementador: línea N-1
# Texto: líneas N+1 hasta siguiente anchor o "AESF" sola
# Filtrar inglés: contexto tiene "(NSA-ES)" en vez de "AESF"
```

## Campos extraídos

| Campo | Función | Notas |
|-------|---------|-------|
| expediente | extract_expediente_id | Formato XXX/YYYY |
| year | extract_year_from_id | Priorizar fecha suceso si diff > 2 años |
| titulo | extract_title_and_date | De portada, líneas tras "INFORME FINAL" |
| tipo | extract_type | accidente/incidente/avería |
| gravedad | extract_gravedad | fatal/grave/menor/desconocido |
| fecha_suceso | parse_date | ISO YYYY-MM-DD |
| estacion | extract_station_and_province | Nombre corto, no descriptivo |
| provincia | extract_station_and_province | Entre paréntesis |
| victimas_mortales | extract_consequences | Regex: `(\d+)\s+fallecid[os]` |
| heridos | extract_consequences | Regex: `(\d+)\s+heridos?\s+graves?` |
| danos_materiales | extract_consequences | Bool: "daños materiales" en texto |
| resumen | extract_summary | 200-1000 chars, filtrar TOC |
| conclusiones | extract_conclusions | Lista de viñetas • |
| recomendaciones | extract_recommendations | Lista de dicts {numero, dest, impl, texto} |
| entidades | extract_entities | Lista hardcodeada (ADIF, Renfe, etc.) |
| tags | extract_tags | Keywords en texto (vía, ERTMS, clima...) |

## CSV — 59 columnas

```
id, year, expediente, titulo, tipo, tipo_suceso, gravedad,
fecha_suceso, estacion, provincia,
victimas_mortales, heridos, danos_materiales,
resumen, conclusiones, entidades, tags,
num_conclusiones, num_recomendaciones,
rec_1_numero, rec_1_destinatario, rec_1_implementador, rec_1_texto,
rec_2_numero, ... rec_10_texto
```

## Bug histórico encontrado en auditoría

`extract_csv.py` línea 50 tenía `r'(\\d{4})'` (doble escape) en raw string.
En Python, `r'\\d'` = literal `\d`, NO dígito. Las fechas con puntos (29.07.2024) nunca se detectaban.
Causa: código copiado de extract.py donde el escape era correcto, pero se corrompió al duplicar.
**Lección**: nunca duplicar funciones extractoras — importar siempre.
