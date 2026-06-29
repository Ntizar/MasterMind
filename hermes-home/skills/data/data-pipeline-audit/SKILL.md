---
name: data-pipeline-audit
version: "1.0.0"
category: data
description: >
  Procedimiento sistemático para auditar pipelines de datos: comparar fuente original
  (Excel, CSV, BD) contra datos extraídos/transformados (JSONs, CSVs procesados).
  Detecta gaps de cobertura, inconsistencias taxonómicas, campos vacíos y problemas
  de geolocalización. Aplicable a cualquier proyecto donde un PDF/scrape se transforma
  en datos estructurados.
triggers:
  - Auditoría de datos extraídos vs fuente
  - Comparar JSONs generados contra Excel/CSV original
  - Verificar cobertura de datos de un pipeline
  - Detectar inconsistencias en taxonomía de datos
  - Revisar calidad de geolocalización
  - "Los datos no coinciden con el Excel"
  - "Faltan informes/datos"
---

# Auditoría de Pipeline de Datos

## Flujo estándar

### Fase 1: Inventario de fuentes
1. **Fuente original** (Excel/CSV/BD): contar registros únicos, identificar campo clave (ID, n_exp, etc.)
2. **Datos extraídos** (JSONs/CSVs): contar archivos, extraer IDs, mapear nomenclatura
3. **Archivos originales** (PDFs/imágenes): contar para verificar que TODO fue procesado
4. Calcular: `faltantes = fuente_original - datos_extraídos`

### Fase 2: Comparación por cobertura
- Contar por año/período/categoría en ambas fuentes
- Identificar gaps concretos (ej: "2008: Excel=57, JSON=53, faltan 4")
- Buscar extras en el destino que no existen en la fuente
- Usar `Counter` de Python para análisis por dimensiones

### Fase 3: Comparación campo a campo
- Para registros que coinciden por ID, comparar valores de campos clave
- Clasificar discrepancias por campo (tipo, ubicación, víctimas, etc.)
- Contar frecuencia de discrepancias por campo para priorizar

### Fase 4: Taxonomía y normalización
- Extraer valores únicos del campo categórico en AMBAS fuentes
- Comparar granularidad: ¿la fuente original tiene más categorías que los datos extraídos?
- Verificar alineación con marco normativo/regulatorio aplicable
- Proponer taxonomía normalizada si hay inconsistencias

### Fase 5: Campos de calidad
- **Coordenadas:** % de nulls en lat/lng
- **Formatos:** verificar consistencia de formatos (PKs, fechas, etc.)
- **Textos largos:** detectar si campos de referencia contienen descripciones completas en vez de valores normalizados

### Fase 6: Informe de resultados
Estructura del informe:
1. **Cubierta de datos** — tabla por período con fuente vs destino
2. **Informes faltantes** — lista concreta de IDs ausentes
3. **Taxonomía** — tabla de discrepancias con frecuencias
4. **Geolocalización** — % completitud y propuesta de mejora
5. **Acciones** — priorizadas por impacto (🔴 crítico, 🟡 importante, 🟢 mejora)

## Pitfalls

### Matching por nombres de archivo caóticos
**Problema:** Cuando los archivos extraídos no tienen nomenclatura consistente (ej: `IF220608240209CIAF.json`, `0011_09_CIAF.json`, `2024-64-0625-if.json`), el matching por nombre es imposible directamente.

**Solución:** Usar campos internos del JSON (ID, año, estación, fecha) para hacer matching fuzzy contra la fuente original. Priorizar: año + número de expediente → fecha + estación → texto del título.

### Extracción de taxonomía simplificada en exceso
**Problema:** Un pipeline de PDF→JSON que solo extrae categorías groseras ("accidente" vs "incidente") pierde información crucial que la fuente original sí tiene.

**Solución:** Siempre comparar la taxonomía del JSON extraído contra la del Excel/fuente. Si el JSON tiene menos categorías que la fuente, el pipeline de extracción necesita re-parseo.

### Severidad/magnitud mal clasificada
**Problema:** Clasificar "grave" todo lo que tiene daños, sin distinguir entre fallecidos y solo heridos. La normativa (RD 929/2022, Directiva 2016/798) exige: muy grave / grave / menor.

**Solución:** Derivar severidad de datos de víctimas (muertos → muy grave, heridos graves → grave, leves/sin víctimas → menor), NO del texto libre del informe.

### Limpieza de texto que destruye datos
**Problema:** Una función de limpieza de nombres que elimina paréntesis, provincias, números PK y textos entre comas PUEDE eliminar el nombre real. Ejemplo: "Sama de Langreo (Asturias)" → la limpieza elimina "(Asturias)" OK, pero si el nombre viene del PDF como "La Serna" y la limpieza elimina "La" por ser genérico, queda vacío.

**Solución:** (1) NUNCA limpiar un nombre completo sin tener un fallback, (2) extraer nombre del resumen ANTES de limpiar, (3) si el resultado de limpiar es <4 chars, descartar y usar el extraído del resumen, (4) SIEMPRE verificar que el nombre limpiado geolocaliza a la provincia correcta — si no, el nombre está mal.

### Geolocalización por municipio en vez de posición real
**Problema:** Guardar solo el nombre del municipio/estación en vez de las coordenadas reales del punto kilométrico.

**Solución:** Si la fuente tiene línea + PK, geocodificar usando APIs de infraestructura (IGN WMTS, Adif) para obtener lat/lng reales del punto en la vía.

### Coordenadas por defecto que contaminan el dataset
**Problema:** Cuando el parsing falla, muchos registros quedan con las mismas coordenadas por defecto (ej: 43.336, -8.3953 = A Coruña para registros de toda España). Estas coordenadas "pasan el filtro" de `lat != null` pero son completamente incorrectas.

**Detección:** Contar frecuencia de coordenadas. Si >5 registros tienen las mismas coords (redondeadas a 1 decimal), es seguro que son por defecto.

```python
from collections import Counter
coord_counts = Counter()
for r in records:
    lat, lng = r.get('lat'), r.get('lng')
    if lat and lng:
        key = (round(lat, 1), round(lng, 1))
        coord_counts[key] += 1
suspicious = {k: v for k, v in coord_counts.items() if v > 5}
```

**Solución:** Marcar esas coords como null, re-geolocalizar desde nombre de estación + resumen del informe. Ver `references/post-extraction-cleanup.md` en skill `government-data-pipelines`.

### Archivos sin procesar (gap entre PDFs y JSONs)
**Problema:** El pipeline no procesó todos los PDFs originales.

**Solución:** Contar PDFs por directorio/año, comparar con JSONs generados. Los faltantes suelen ser PDFs con nombres no estándar o en directorios inesperados.

## Referencias
- `references/rd929-taxonomia.md` — Taxonomía de severidad y tipología según normativa ferroviaria española
