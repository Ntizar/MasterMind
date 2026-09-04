# NAP API — Datos Reales (verificados 2026-06-23)

## Resumen

**161 conjuntos de datos** (160 activos, 1 obsoleto). **0.65 GB total** (661.9 MB).

| Métrica | Valor |
|---|---|
| Conjuntos | 161 |
| Tamaño total | 0.65 GB |
| Viajes totales | 2,088,524 |
| Rutas totales | 24,252 |
| Paradas totales | 191,065 |
| Organizaciones | 122 |
| Regiones | 4,967 |
| Actualización | Diaria |

## Distribución por tipo de transporte

| Tipo | Conjuntos |
|---|---|
| Autobús | 137 |
| Ferroviario | 28 |
| Marítimo | 3 |
| Aéreo | 1 |

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

## Distribución de tamaños

| Rango | Conjuntos | Tamaño total |
|---|---|---|
| <1 MB | 102 | 22 MB |
| 1-5 MB | 35 | 71 MB |
| 5-10 MB | 10 | 66 MB |
| 10-50 MB | 10 | 164 MB |
| 50-100 MB | 3 | 190 MB |
| >100 MB | 1 | 133 MB |
| **Total** | **161** | **662 MB** |

## Top 20 regiones por número de datasets

| Región | Conjuntos |
|---|---|
| Barcelona | 89 |
| Madrid | 58 |
| Cataluña | 43 |
| País Vasco | 40 |
| Castilla y León | 30 |
| Murcia | 28 |
| Guipúzcoa | 25 |
| Málaga | 25 |
| Bilbao | 25 |
| Zaragoza | 24 |

## Top 10 organizaciones

| Organización | Conjuntos |
|---|---|
| Sagalés | 11 |
| Avanza Grupo | 9 |
| Lurraldebus | 7 |
| CRTM | 5 |
| Vectalia | 3 |
| Gobierno de La Rioja | 3 |
| AISA | 2 |
| ATMB Barcelona | 2 |
| Interbus | 2 |
| RENFE | 2 |

## Frecuencia de actualización (históricos)

| Dataset | Versiones históricas | Frecuencia |
|---|---|---|
| Cataluña completa | 426 | ~1.2/día |
| Cataluña simplificada | 424 | ~1.2/día |
| Tenerife TITSA | 854 | ~2.3/día |
| Comunidad Valenciana interurbano | 1,540 | ~4.2/día |
| Madrid EMT | 513 | ~1.4/día |
| Bizkaibus | 256 | ~0.7/día |
| Xunta de Galicia | 190 | ~0.5/día |
| CRTM Madrid interurbanos | 28 | ~0.1/día |
| CRTM Madrid urbano | 22 | ~0.1/día |

## Estrategia de descarga

```
Semana 1: Full dump → ~0.7 GB
Semanas siguientes: Delta → ~100-500 MB
Históricos (3 últimas versiones): ~2 GB
Total estable: ~3-4 GB
```

## API Key

- **Variable:** `NAP_API_KEY`
- **Ubicación:** `/root/workspace/TimeIneco/.env`
- **Header:** `ApiKey: {api_key}`

## Endpoints clave

```
GET /api/v2/conjunto-dato                          # TODOS los datasets (161)
GET /api/v2/conjunto-dato/{id}                     # Detalle de un conjunto
GET /api/v2/conjunto-dato/{id}/historico           # Versiones anteriores
GET /api/v2/fichero/{id}/descarga                  # Enlace S3 temporal (900s)
GET /api/v2/operador                               # Lista operadores
GET /api/v2/region                                 # Lista regiones
GET /api/v2/tipo-transporte                        # Lista tipos
GET /api/v2/tipo-fichero                           # Lista tipos de fichero
GET /api/v2/organizacion                           # Lista organizaciones
```

## Estructura del histórico

```json
{
  "id": 162343,
  "formato": "gtfs-zip",
  "fecha": "2026-06-23T00:00:00",
  "nombreArchivo": "20260623_040056_Bus_Tren_Catalunya_completa",
  "enlaceDescarga": "fichero/162343/historico/descarga"
}
```

## Pitfalls

1. **Enlaces S3 temporales** — Cada descarga da un enlace que expira en 900s (15 min)
2. **No hay paginación** — `/conjunto-dato` devuelve TODOS los 161 de golpe
3. **Actualización diaria** — Algunos datasets cambian cada día, no cada semana
4. **Históricos sin tamaño** — El metadata del histórico NO tiene campo `tamanio`. Solo el fichero actual lo tiene.
5. **Formato de fecha** — Las fechas del histórico son `YYYY-MM-DDT00:00:00` (sin hora real)
6. **Respuesta envuelta** — Todas las respuestas tienen `{success, message, data, traceId, correlationId}`
