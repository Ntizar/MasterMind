# Referencia: API NAP (Nodo de Acceso al Transporte Público)

## Fuente

- **URL base:** `https://nap.transportes.gob.es/api/v2/`
- **Swagger:** `https://nap.transportes.gob.es/api/swagger/v2/swagger.json`
- **Autenticación:** Header `Api-key: <tu_api_key>`
- **Key en:** `/root/workspace/TimeIneco/.env` (variable `NAP_API_KEY`)

## Estructura de la API

- **31 endpoints** (26 GET, 5 POST)
- **42 schemas** de datos
- **161 conjuntos de datos** (160 activos, 1 obsoleto)

## Endpoints principales

| Endpoint | Método | Descripción |
|---|---|---|
| `/conjunto-dato` | GET | Listar todos los conjuntos de datos |
| `/conjunto-dato/{id}` | GET | Detalles de un conjunto específico |
| `/conjunto-dato/{id}/fichero` | GET | Listar ficheros de un conjunto |
| `/conjunto-dato/{id}/historico` | GET | Historial de versiones |
| `/descargar/{id}` | GET | Descargar fichero GTFS (ZIP) |

## Tipos de transporte (route_type)

| Value | Tipo |
|---|---|
| 0 | Tranvía |
| 1 | Metro |
| 2 | Subterráneo |
| 3 | Autobús |
| 4 | Ferrocarril |
| 5 | Funicular |
| 6 | Barco |
| 7 | Teleférico |
| 11 | Tren ligero |
| 12 | Autobús exprés |

## Volumen de datos (junio 2026)

- **Total actual:** 650-673 MB (162 ZIPs)
- **Total con históricos:** ~3 GB conservador
- **2M+ viajes**, **24K rutas**, **191K paradas**
- **102 datasets** < 1 MB
- **35 datasets** entre 1-5 MB
- **10 datasets** entre 5-10 MB
- **10 datasets** entre 10-50 MB
- **4 datasets** > 50 MB (Xunta Galicia lidera con 136 MB)

## Frecuencia de actualización

- **Diaria** para la mayoría de datasets grandes
- **Semanal** para datasets pequeños
- **Delta semanal:** ~100-500 MB (solo actualizados en últimas 24h)

## Scripts disponibles

- `descargar-nap.py` — Descarga completa o delta
- `descargar-faltantes.py` — Descarga forzada de datasets faltantes
- `cron-update.sh` — Script para crontab (domingo 06:00 UTC)

## Estructura del repositorio GTFSSpain

```
GTFSSpain/
├── data/              # ZIPs GTFS (673 MB, no en git)
├── metadata/          # JSON metadatos (en git)
├── visor/
│   └── index.html     # Visor interactivo autocontenido
├── descargar-nap.py   # Script de descarga
├── descargar-faltantes.py
├── cron-update.sh     # Actualización semanal
└── README.md
```

## Pitfalls

- Los enlaces S3 de descarga son temporales (900s)
- Algunos datasets tienen ficheros de 0 MB (vacíos en la API)
- GTFS RT (tiempo real) no es ZIP descargable — solo GTFS estático
- NetEx/SIRI son formatos diferentes, no compatibles con JSZip
- El repo GitHub es privado (Ntizar/GTFSSpain)
