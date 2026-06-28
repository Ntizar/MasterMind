# Referencia: Nominatim en CIAF-visor

## Caso de uso: Geocodificar ~200 estaciones de tren españolas

### Datos extraídos
- 270 informes de accidentes ferroviarios (2007-2025)
- ~200 estaciones únicas (muchas repetidas entre informes)
- Solo ~50-60 con nombres válidos (resto son oraciones basura del PDF)

### Nombres basura típicos de extraer de PDFs
```
Getafe Industrial observa que una persona va caminando
Medina del Campo donde no tenía prescrita parada
Guillarei en condiciones normales a la circulación
Córdoba desde donde se
```
**Solución:** `extract_estacion()` con stop phrases y max 35 chars.

### Patrones de éxito para queries
| Query | Resultado |
|-------|-----------|
| `Madrid Chamartín España` | ✅ Estación (40.4725, -3.6825) |
| `Cuenca-Fernando España` | ✅ Estación (39.3522, -2.3260) |
| `Salou España` | ✅ Municipio (41.0768, 1.1440) |
| `estacion Chamartin Madrid` | ❌ 403 o no encontrado |

### Datos hardcodeados (328 estaciones)
Archivo: `data/station-coords.json` (29.7KB)
- 173 de informes CIAF
- 155 adicionales (capitales de provincia + nudos ferroviarios)
- Maneja normalización: acentos, guiones, case, whitespace

### Workflow completo
1. `scripts/parse_all.py` → extrae texto de PDFs, genera `data/reports/YYYY.json`
2. `scripts/build-station-map.py` → genera `data/station-coords.json`
3. `scripts/geocode_all.py` → aplica coords del JSON a los informes (con Nominatim para las que faltan)
4. `scripts/sync.py` → detecta nuevos PDFs y repite el proceso
