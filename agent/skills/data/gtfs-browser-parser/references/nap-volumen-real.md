# NAP API — Volumen Real de Datos

**Fecha análisis:** 2026-06-23  
**Fuente:** nap.transportes.gob.es (API v2)  
**Autenticación:** ApiKey header

## Resumen Ejecutivo

| Métrica | Valor |
|---|---|
| Conjuntos de datos | 161 (160 activos, 1 obsoleto) |
| Tamaño total actual | **662 MB** |
| Total viajes | 2,000,000+ |
| Total rutas | 24,000+ |
| Total paradas | 191,000+ |
| Actualización | Diaria en datasets principales |
| Delta semanal | ~100-500 MB |

## Distribución por tamaño

| Rango | Cantidad | Ejemplos |
|---|---|---|
| < 1 MB | 102 | Pueblos pequeños |
| 1-5 MB | 35 | Ciudades medianas |
| 5-10 MB | 10 | Ciudades grandes |
| 10-50 MB | 10 | Provincias |
| > 50 MB | 4 | Galicia (136 MB), etc. |

## Top 5 datasets por tamaño

1. **Xunta de Galicia** — 136 MB (24 organizaciones)
2. **Cercanías Renfe** — ~50 MB
3. **FGC Barcelona** — ~30 MB
4. **EMT Madrid** — ~20 MB
5. **TMB Barcelona** — ~15 MB

## Actualización

- **Diaria:** Cataluña, Tenerife, Comunidad Valenciana
- **Semanal:** La mayoría de datasets
- **Mensual:** Datos históricos y metadatos

## Estrategia de descarga recomendada

1. **Descarga completa inicial:** ~662 MB
2. **Delta semanal:** solo datasets actualizados en últimas 24h
3. **Históricos:** solo 3 últimas versiones por dataset (~3 GB total)
4. **Script:** `descargar-nap.py --delta`

## Estructura de directorios

```
data/
├── {id}_{nombre}/
│   └── {nombre}.zip    (GTFS-ZIP)
```

## Ficheros por dataset

Cada conjunto de datos tiene:
- `GTFS-ZIP` — fichero GTFS principal (ZIP)
- `GTFS-RT` — tiempo real (no ZIP, no descargable como ZIP)
- `NetEx` / `SIRI` — formatos alternativos (no GTFS)

Solo los `GTFS-ZIP` son descargables como ZIP y útiles para el visor.

## Referencias

- API: `https://nap.transportes.gob.es/api/v2/conjunto-dato`
- Swagger: `https://nap.transportes.gob.es/api/swagger/v2/swagger.json`
- Script descarga: `descargar-nap.py`
- Script delta: `descargar-nap.py --delta`
