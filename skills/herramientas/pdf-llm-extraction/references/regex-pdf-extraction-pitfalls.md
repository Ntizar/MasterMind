# Pitfalls de Extracción con Regex en PyMuPDF

Documentación de errores clásicos al extraer datos de PDFs con regex (alternativa al pipeline LLM).

## Pitfall 1: `[\s\S]` coincide con PUNTOS

**Problema:** El patrón `[\s\S]` significa "cualquier carácter" (incluyendo `.`). Cuando se extrae texto de un TOC con puntos como separadores:

```
1. RESUMEN ................................................................................................................5
```

Un regex como `RESUMEN\s+([\s\S]{200,4000})` captura TODOS los puntos del TOC porque `\s\S` incluye `.`.

**Solución:** Verificar que el primer carácter después de la keyword NO sea un punto:

```python
m = re.search(r'RESUMEN\s+(\S[\s\S]{199,3999})', text)
candidate = m.group(1)
if candidate[0] == '.':
    # Es TOC, saltar
    pass
```

**También filtrar por dot ratio:** si el candidato tiene >50% puntos sobre su longitud, es probablemente TOC.

## Pitfall 2: Distinguir TOC de contenido real

**Patrón de filtrado multi-criterio:**

```python
candidate = m.group(1)
word_count = len(candidate.split())
dot_ratio = candidate.count('.') / max(len(candidate), 1)

# TOC: pocos palabras, muchos puntos
# Real: muchas palabras, pocos puntos
if word_count > 20 and dot_ratio < 0.1:
    # Contenido real
```

**También filtrar títulos de sección:** si el candidato empieza con "DEL ANÁLISIS", "DEL ANÁLISIS Y..." es un título de sección analítica, no un resumen del suceso.

```python
if re.match(r'^\s*DEL\s+(ANÁLISIS|ANALISIS)', candidate, re.I):
    # Es título de sección, saltar
```

## Pitfall 3: Tablas en PyMuPDF — columnas en líneas separadas

**Problema:** PyMuPDF `page.get_text()` no respeta estructura de tabla. Columnas que están al lado en el PDF aparecen en líneas separadas:

```
Destinatario
Implementador
final
Número
Recomendación
AESF
ADIF y ADIF AV
111/2024-1
Reelaborar los procedimientos...
```

**Solución:** Usar números de referencia únicos como anclas:

```python
# 1. Buscar sección
m = re.search(r'RECOMENDACIONES\s+FINALES\s+([\s\S]{0,30000})', text)
rec_section = m.group(1)

# 2. Encontrar todas las instancias de patrón de número
rec_numbers = re.findall(r'(\d{3}/\d{4}-\d+)', rec_section)

# 3. Para cada número, extraer contexto ANTES y DESPUÉS
for rec_num in rec_numbers:
    idx = rec_section.find(rec_num)
    # Destinatario + implementador ANTES del número
    before = rec_section[max(0, idx-500):idx]
    # Texto DESPUÉS del número (hasta el siguiente número)
    after = rec_section[idx + len(rec_num):next_idx]
```

## Pitfall 4: `[\s\S]*?` causa catastrophic backtracking

**Problema:** `[\s\S]*?` (lazy) aplicado a texto grande (50K+ chars) puede colgar el procesador.

**Solución:** Limitar el rango con cuantificadores numéricos:

```python
# ❌ COLGA
re.search(r'RESUMEN\s+([\s\S]*?)SIGUIENTE_SECCION', text)

# ✅ LIMITADO
re.search(r'RESUMEN\s+([\s\S]{300,5000})', text)
```

## Pitfall 5: Duplicación de offsets en bucles

**Problema:** Avanzar `pos = pos + m.start() + m.end()` duplica el offset porque `m.start()` siempre es 0 dentro del slice `text[pos:]`.

**Solución:** Solo sumar `m.end()`:

```python
# ❌ DOBLE OFFSET
pos = pos + m.start() + m.end()

# ✅ CORRECTO
pos += m.end()
```

## Pitfall 6: Distinguir "RESUMEN" de "RESUMEN DEL ANÁLISIS" con salto de línea

**Problema:** Un PDF puede tener múltiples ocurrencias de "RESUMEN":
- TOC: `1. RESUMEN ...........5` (puntos de separación)
- Título de sección: `5.1. RESUMEN DEL ANÁLISIS Y CONCLUSIONES...`
- Contenido real: `1. RESUMEN \nEl 29 de octubre de 2024...`

El regex `RESUMEN\s+([\s\S]{200,4000})` captura tanto TOC como títulos de sección porque `\s+` no coincide con `.` (punto) pero `[\s\S]` SÍ coincide.

**Solución definitiva: buscar salto de línea después de RESUMEN.**

El resumen real SIEMPRE tiene `RESUMEN \nEl...` (salto de línea + texto que empieza con letra). Los otros NO tienen salto de línea:
- TOC: `RESUMEN ...........` (puntos, no `\n`)
- Título: `RESUMEN DEL ANÁLISIS` (espacio + palabra, no `\n`)

```python
# ✅ PATRÓN DEFINITIVO: RESUMEN + salto de línea + texto real
m = re.search(r'(?:\d+\.\s+)?RESUMEN\s*\n\s*([A-ZÁÉÍÓÚÑa-záéíóúñ][\s\S]{199,3999})', text)
```

Este patrón filtra automáticamente:
- TOC (puntos, no `\n`)
- Títulos de sección (sin `\n` después de RESUMEN)
- Solo captura el resumen real

## Pitfall 7: Tablas con cabecera — buscar por columnas, no por título

**Problema:** Un PDF puede tener múltiples menciones de "RECOMENDACIONES FINALES":
- TOC (página 1): `6. RECOMENDACIONES FINALES ...........32`
- Texto narrativo (páginas 6-7): menciones en párrafos
- Tabla real (página 32): la tabla con columnas

`re.search(r'RECOMENDACIONES\s+FINALES...')` coge la PRIMERA ocurrencia (TOC), no la tabla.

**Solución: buscar la cabecera de tabla por sus columnas.**

```python
# Buscar la cabecera que tiene TODAS las columnas juntas
table_m = re.search(
    r'(?:Destinatario|Addressee)[\s\S]{0,500}(?:Implementador|Final Implementer)[\s\S]{0,500}'
    r'(?:Número|Number)[\s\S]{0,500}(?:Recomendación|Recommendation)',
    text, re.I
)
```

Esto solo coincide con la tabla real (página 32), no con TOC ni texto narrativo.

## Pitfall 8: Parsear tablas PyMuPDF por líneas, no por posición

**Problema:** PyMuPDF `get_text()` descompone tablas en líneas individuales:
```
AESF
ADIF y ADIF AV
111/2024-1
Reelaborar los procedimientos...
```

Los regex de posición (`before_num`, `after_num`) fallan porque:
- `[A-Z]+` no captura "ADIF y ADIF AV" (la "y" minúscula corta el match)
- El texto puede tener saltos de línea dentro de una misma recomendación
- No hay forma fiable de saber dónde termina una fila y empieza otra

**Solución: parsear por LÍNEAS, no por posición.**

```python
table_section = text[table_m.start():]
lines = table_section.split('\n')

# 1. Encontrar líneas que son números de recomendación
rec_indices = [i for i, line in enumerate(lines)
               if re.match(r'^\s*\d{3}/\d{4}-\d+\s*$', line)]

# 2. Para cada número:
#    - destinatario = línea N-2
#    - implementador = línea N-1
#    - texto = líneas N+1 hasta siguiente número o "AESF"
for idx in rec_indices:
    rec_num = lines[idx].strip()
    destinatario = lines[idx-2].strip() if idx >= 2 else ''
    implementador = lines[idx-1].strip() if idx >= 1 else ''
    
    # Texto hasta siguiente número o línea "AESF"
    text_lines = []
    for line in lines[idx+1:next_idx]:
        if re.match(r'^AESF\s*$', line.strip()):
            break
        if line.strip():
            text_lines.append(line.strip())
    texto = ' '.join(text_lines)
```

## Pitfall 9: Filtrar versión inglesa de tablas bilingües

**Problema:** Algunos PDFs (como los informes CIAF) incluyen versión en español E inglés de la misma tabla. Ambas tienen el mismo patrón de números (`111/2024-1`).

**Solución:** Filtrar por el contenido de las líneas previas. La versión española usa "AESF" como destinatario; la inglesa usa "(NSA-ES)".

```python
spanish_indices = []
for idx in rec_indices:
    context = '\n'.join(lines[max(0, idx-3):idx])
    if 'AESF' in context and '(NSA-ES)' not in context:
        spanish_indices.append(idx)
```

## Cuándo usar regex vs. LLM

| Criterio | Regex | LLM |
|----------|-------|-----|
| PDFs con formato consistente | ✅ Bien | Overkill |
| PDFs con formato variable | ❌ Frágil | ✅ Robusto |
| Sin acceso a API | ✅ Offline | ❌ Necesita API |
| >100 PDFs masivos | ⚠️ Rápido pero frágil | ✅ Escala bien |
| Conclusión/recomendación estructurada | ⚠️ 50-70% éxito | ✅ 99% éxito |
| Tabla con columnas en líneas separadas | ✅ Patrón por líneas | ✅ Funciona también |
| Secciones con títulos ambigüos (RESUMEN vs RESUMEN DEL ANÁLISIS) | ✅ Patrón con salto de línea | ✅ Funciona también |
