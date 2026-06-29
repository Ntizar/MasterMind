---
name: ciaf-data-pipeline
description: "Pipeline completo CIAF: PDF → JSON individual → cruzar con Excel → visor web. Geolocalización, limpieza, taxonomía RD 929/2022."
version: "1.0.0"
tags: [ciaf, pipeline, data, geocoding, railroad, spain]
---

# CIAF Data Pipeline

Pipeline de datos para el visor de informes CIAF (Comisión de Investigación de Accidentes Ferroviarios).

## Arquitectura de datos

```
PDFs originales → JSON individuales (pdf_to_jsonv2) → Cruzar con Excel → reports/YYYY.json (visor)
                  /root/workspace/ciaf-data/           /root/workspace/CIAF-visor/data/reports/
                  data/individual/                     
```

**Fuentes de verdad (en orden de fiabilidad):**
1. **JSON individuales** (`ciaf-data/data/individual/`) — generados directamente del PDF, contienen el resumen correcto
2. **Excel** (`260218_Base_Datos_CIAF_1.xlsx`) — metadatos estructurados (fecha, tipo, víctimas, pk, línea)
3. **JSONs del visor** (`CIAF-visor/data/reports/YYYY.json`) — targets de visualización, se rellenan desde fuentes 1+2

## ⚠️ Pitfall crítico: Cross-reference por expediente incompleto

**El error más grave descubierto:** cruzar por número de expediente **sin el año** causa corrupción masiva de datos.

```
# MAL — el mismo resumen se copia a 5 registros:
exp = "50"  # ← matching parcial
# Resultado: 50/2008, 50/2009, 50/2010, 50/2011, 50/2012 → todos con el texto de 50/2009

# BIEN — matching completo:
exp = "0050/2009"  # ← número + año
```

**Síntomas:** múltiples registros mostrando el mismo "Resumen del análisis" en el visor, con fechas/lugares que no coinciden con el expediente.

**Detección:** buscar resúmenes duplicados:
```python
from collections import Counter
resumen_map = {}
for r in all_records:
    res = r['analisis']['resumen'][:80]
    resumen_map.setdefault(res, []).append(r['expediente'])
duplicates = {k: v for k, v in resumen_map.items() if len(v) > 1}
```

**Corrección:** re-cruzar usando expediente normalizado (número con ceros + `/` + año):
```python
# Normalizar: "50/2009" → "0050/2009"
parts = exp.split('/')
norm_exp = f"{parts[0].zfill(4)}/{parts[1]}"
```

## Geolocalización

### Estrategia en orden de preferencia
1. **Coords del JSON individual** — el parser extrae lat/lng cuando aparecen en el PDF. Son las más precisas (~100m)
2. **PK + línea** del Excel → interpolación con ADIF LTV FeatureServer (~500m)
3. **Nombre de estación** → lookup en `data/station-coords.json` (355 entries)
4. **Nominatim** → fallback con nombre + provincia (~2km)
5. **Coords manuales** → para registros sin datos suficientes

**Pitfall crítico:** la interpolación por PK puede dar.coords muy alejadas del punto real (diferencias > 0.1 grado). SIEMPRE verificar coords del JSON individual antes de usar LTV. Si el individual tiene coords válidas, usarlas aunque el LTV dé otras.

### Pitfall: Nominatim rate limiting
Nominatim bloquea con HTTP 429 tras ~20 peticiones. Soluciones:
- Acumular geocodificaciones y hacerlas en batch con 1.1s entre peticiones
- Usar coordenadas hardcodeadas para estaciones conocidas
- La DB de estaciones (`station-coords.json`) es la fuente principal

### Pitfall: Nombres de estación genéricos
Nombres como "La", "San", "Los", "Sant" son resultados de parsing truncado. **Nunca geolocalizar con estos nombres** — siempre extraer el nombre completo del resumen del informe.

Patrón de extracción:
```python
# Buscar en resumen: "estación de X (Provincia)"
m = re.search(r'estaci[oó]n\s+de\s+(\w[\w\s]+)\((\w[\w\s]+)\)', resumen)
station, province = m.group(1), m.group(2)
```

## Limpieza de nombres de estación

**Problema:** el parsing original deja nombres con:
- Provincia entre paréntesis: "Tolosa (Guipúzcoa)" → "Tolosa"
- Mayúsculas: "TRASONA" → "Trasona"
- Puntos finales: "Atocha." → "Atocha"
- Nombres truncados por limpieza agresiva: "Vila-real" → "Vila"

**Regla:** la limpieza NUNCA debe eliminar partes del nombre que no sean provincia entre paréntesis.

## Taxonomía de severidad (RD 929/2022)

| Categoría | Definición |
|-----------|-----------|
| **Muy grave** | Al menos 1 fallecido O lesiones muy graves |
| **Grave** | Lesiones graves sin fallecidos, evacuación significativa, daños materiales importantes |
| **Menor** | Sin víctimas ni daños significativos |

**Mapping desde Excel:** columna `muertos` (>0 → muy grave), `heridos_graves` (>0 → grave), resto → menor.

## Tipología de sucesos (RD 929/2022)

Categorías normalizadas:
- Accidente (colisión, descarrilamiento, atropello)
- Incidente (conato, rebasamiento de señal, fallo infraestructura)
- Sin categorizar

El Excel tiene ~58 categorías que se agrupan en ~18 normalizadas.

## Scripts del pipeline

| Script | Función |
|--------|---------|
| `scripts/cruce_datos.py` | Cruza JSON individuales con Excel |
| `scripts/fix_visor_complete.py` | Fix completo: nombres, provincias, geocoding |
| `scripts/geocode_visor.py` | Geocodificación agresiva con Nominatim |
| `scripts/fix_visor_data.py` | Fix de gravedad y tipología |

## Restauración de datos originales tras cross-reference

**Pitfall crítico:** el cross-reference script sobreescribe campos con contenido generado por IA o datos de otros años. SIEMPRE restaurar desde JSON individuales después del cruce.

### Campos a restaurar (en orden de prioridad)

1. **Título** — usar `titulo` del JSON individual (formato original del PDF: "INFORME FINAL SOBRE EL ACCIDENTE FERROVIARIO Nº 0033/2009..."). NUNCA usar el formato generado por IA ("IF 0033/2009 — El día...")

2. **Conclusiones** — usar `conclusiones` del JSON individual (texto real extraído del PDF). El campo del visor frecuentemente tiene texto diferente inventado.

3. **Recomendaciones** — usar `recomendaciones` del JSON individual.

4. **Estación y provincia** — usar del JSON individual cuando el campo del visor tiene valores incorrectos (fragmentos como "clase C" o datos de otros años).

5. **PK y tramo** — restaurar desde JSON individual si el visor no los tiene.

6. **Tipo de suceso** — usar `tipo_suceso_normalizado` del JSON individual.

### Patrón de restauración

```python
# Normalizar expediente para matching
parts = exp.split('/')
norm_exp = f"{parts[0].zfill(4)}/{parts[1]}"

# Restaurar desde individual
if norm_exp in ind_index:
    ind = ind_index[norm_exp]
    r['titulo'] = ind.get('titulo', r['titulo'])
    r['conclusiones'] = ind.get('conclusiones', r['conclusiones'])
    r['ubicacion']['estacion'] = ind.get('estacion') or r['ubicacion']['estacion']
    r['ubicacion']['provincia'] = ind.get('provincia') or r['ubicacion']['provincia']
```

## Extracción de estación desde Excel "lugar"

El campo `lugar` del Excel contiene descripciones largas como:
- "Paso a nivel clase C en la población de Monforte de Lemos, carretera..."
- "P.K. 104,857, entre Salamanca y Babilafuente"

**Pitfall:** extracciones regex pueden devolver fragmentos como "clase C" o "clase A" en vez del nombre real de la estación.

**Solución:** usar el JSON individual como fuente primaria para estación. Solo usar Excel como fallback cuando el individual no tiene estación.

```python
# Orden de preferencia para estación:
# 1. JSON individual (si tiene nombre > 3 chars y no es fragmento)
# 2. Excel lugar (con extracción limpia)
# 3. Coordenadas geolocalizadas

fragments = {'clase A', 'clase B', 'clase C', 'clase P', 'plena vía'}
if ind_est and len(ind_est) > 3 and ind_est not in fragments:
    station = ind_est
```

## Corrección de provincias

**Pitfall:** los JSON individuales pueden tener provincias incorrectas heredadas del parser. El Excel también puede tener errores (ej: Ponferrada → Barcelona).

**Estrategia (en orden de fiabilidad):**
1. **Resumen del informe** — si menciona "en Asturias", la provincia debe ser Asturias
2. **Excel** — más fiable que el parser para ubicaciones
3. **JSON individual** — fallback cuando no hay Excel

**Verificación obligatoria:** después de cruzar, comparar provincia del Excel vs provincia del JSON individual. Si difieren, investigar cuál es correcta mirando el resumen.

```python
# Verificar consistencia provincia
for exp, ind in ind_index.items():
    if exp in excel_data:
        ex_prov = excel_data[exp]['provincia']
        ind_prov = ind.get('provincia', '')
        if ex_prov and ind_prov and ex_prov.lower() != ind_prov.lower():
            print(f"MISMATCH: {exp} | Excel: {ex_prov} | Individual: {ind_prov}")
```

## Documentación del proyecto (README)

Para que el proyecto sea mantenible sin su autor, el README debe incluir:

### Estructura mínima requerida
1. **¿Qué es?** — una frase clara + lista de capacidades
2. **Fuentes de datos** — tabla con fuente, cantidad, período, enlace
3. **Estructura del proyecto** — árbol de carpetas con comentarios
4. **Flujo de datos** — diagrama ASCII del pipeline completo
5. **Fuentes de verdad** — tabla de qué campo viene de dónde
6. **Scripts** — tabla de cada script con función, entrada, salida
7. **Cómo añadir datos** — paso a paso para nuevos informes
8. **Errores conocidos** — lo que se descubrió y cómo se resolvió
9. **Normativa** — marco legal aplicable
10. **Licencia** — datos públicos + código MIT

### Ejemplo de sección "Fuentes de verdad"

```markdown
| Campo | Fuente | Notas |
|-------|--------|-------|
| Título | JSON individual | Título original del PDF |
| Conclusiones | JSON individual | Texto literal del informe |
| Severidad | Excel + RD 929/2022 | "fatal" → "muy grave" |
| Provincia | Excel + resumen | Verificar consistencia |
| Coordenadas | JSON individual | Más precisas que LTV |
```

### Pitfall: README genérico
Un README con solo "instalación" y "uso" no sirve para mantener el proyecto. Debe explicar el **porqué** de las decisiones de diseño y los **errores descubiertos** para que el siguiente desarrollador no los repita.

## Verificación post-fix

```python
# Checklist obligatorio después de cualquier fix:
# 1. Sin resúmenes duplicados (excepto legítimos)
# 2. Sin nombres de estación <= 3 caracteres
# 3. Sin coordenadas por defecto (A Coruña: 43.336, -8.3953)
# 4. Provincia consistente con el resumen
# 5. Total registros = total en Excel (≈278-280)
# 6. Títulos en formato original del PDF (no formato IA)
# 7. Conclusiones extraídas del PDF (no generadas por IA)
# 8. Estaciones > 3 caracteres, sin fragmentos ("clase C", etc.)
```

## Estructura de archivos

```
ciaf-data/
  data/individual/       # JSONs originales del parser (fuente de verdad para resúmenes)
  data/individual_backup_*/  # Backups antes de fixes
  
CIAF-visor/
  data/reports/YYYY.json  # Datos para el visor (targets de fixes)
  data/station-coords.json  # DB de coordenadas de estaciones
  scripts/                # Scripts del pipeline
  ltv_lookup.json         # Lookup PK → coords del ADIF
```
