# NAP API — Datos reales verificados 2026-06-23

## Volumen total

| Métrica | Valor |
|---|---|
| Conjuntos | 161 (160 activos, 1 obsoleto) |
| Tamaño total | 0.65 GB (661.9 MB) |
| Viajes totales | 2,088,524 |
| Rutas totales | 24,252 |
| Paradas totales | 191,065 |
| Organizaciones | 122 |
| Actualización | Diaria (varios datasets se actualizan TODOS los días) |

## Distribución por tipo

- **Autobús:** 137 conjuntos
- **Ferroviario:** 28 conjuntos
- **Marítimo:** 3 conjuntos
- **Aéreo:** 1 conjunto

## Top 10 por tamaño

| Dataset | Tamaño | ID | Viajes | Rutas | Paradas |
|---|---|---|---|---|---|
| Xunta de Galicia | 136.4 MB | 1386 | 133,153 | 6,584 | 26,004 |
| CRTM Madrid interurbanos | 72.2 MB | 1160 | 55,219 | 354 | 8,402 |
| Cataluña completa | 66.1 MB | 1536 | 210,708 | 2,092 | 29,050 |
| Cataluña simplificada | 56.6 MB | 1535 | 194,727 | 1,605 | 23,246 |
| Cataluña interurbano | 21.9 MB | 1163 | 26,148 | 939 | 8,942 |
| Tenerife TITSA | 21.5 MB | 1130 | 72,653 | 178 | 3,815 |
| Bizkaibus | 20.8 MB | 1061 | 38,042 | 93 | 2,335 |
| CRTM Madrid urbano | 20.0 MB | 934 | 87,005 | 236 | 4,911 |
| Comunidad Valenciana | 17.4 MB | 1325 | 10,646 | 381 | 5,225 |
| EMT Madrid | 16.1 MB | 896 | 81,798 | 236 | 4,924 |

## Frecuencia de actualización (versiones por dataset)

- **Comunidad Valenciana interurbano:** 1,540 versiones (~4.2/día)
- **Tenerife TITSA:** 854 versiones (~2.3/día)
- **Cataluña completa:** 426 versiones (~1.2/día)
- **Media general:** 743 versiones por dataset (muchas duplicadas)

## Estrategia de almacenamiento

Full dump inicial ~0.7 GB + delta semanal ~100-500 MB + históricos recientes ~2 GB = **~3-4 GB total estable**.

## Endpoints clave

- `GET /api/v2/conjunto-dato` → lista TODOS los conjuntos (~9 MB response)
- `GET /api/v2/conjunto-dato/{id}` → metadatos + ficheros
- `GET /api/v2/fichero/{id}/descarga` → JSON con `enlaceDescarga` (S3 temporal 900s)
- `GET {enlaceDescarga}` → descarga el ZIP real

## Filtros importantes

- Solo descargar ficheros con `nombreTipoFichero` conteniendo "GTFS"
- Tipos RT, NetEx, SIRI son datos en tiempo real, NO ZIPs descargables
- Los enlaces S3 caducan en 900 segundos (15 min)

## Operadores de Madrid (IDs reales)

| Operador | NAP dataset ID | Líneas | GTFS |
|---|---|---|---|
| EMT Madrid | 2111 | 217 | ✅ Auto |
| Metro Madrid | 2113 | 13 | ✅ Auto |
| Renfe Cercanías | 1738 | 9 | ✅ Auto |
| CRTM | 286 | 400 | ✅ Auto |
