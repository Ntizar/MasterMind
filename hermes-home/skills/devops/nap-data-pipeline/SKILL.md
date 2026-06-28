---
name: nap-data-pipeline
version: "1.0.0"
description: "Pipeline completo para descargar, almacenar y actualizar datos de transporte público español desde la API NAP (Nodo de Acceso al Transporte Público). Incluye script de descarga, estructura de repositorio, delta semanal y patrón de integración con TimeIneco/GTFS."
author: David Antizar
tags: [nap, gtfs, transporte, data-pipeline, api, descargas, cron, automatización, datos-abiertos]
---

# NAP Data Pipeline — Descarga y Actualización Automática

## Cuándo cargar esta skill

Cuando el usuario pida: descargar datos de transporte público de España, GTFS, NAP transportes, actualizar datos de buses/metros, tener datos de transporte offline, pipeline de datos de APIs gubernamentales.

## Contexto

La **NAP (Nodo de Acceso al Transporte Público)** del Ministerio de Transportes es la fuente oficial de datos GTFS de España:
- **161 conjuntos de datos** (160 activos, 1 obsoleto)
- **0.65 GB** de datos GTFS actuales
- **2M viajes, 24K rutas, 191K paradas**
- **Actualización diaria** (varios datasets se actualizan TODOS los días)

## API Endpoint

- **Base URL:** `https://nap.transportes.gob.es/api/v2/`
- **Autenticación:** Header `ApiKey: <NAP_API_KEY>`
- **API Key:** en `/root/workspace/Time/.env` (variable `NAP_API_KEY`)
- **Swagger:** `https://nap.transportes.gob.es/api/v2/swagger.json`

## Endpoints principales

### 1. Listar TODOS los conjuntos (9 MB response)
```
GET /api/v2/conjunto-dato
```
Devuelve array de 161 conjuntos con: `id`, `nombre`, `tipo`, `regionId`, `tamaño`, `versiones`.

### 2. Metadatos de un conjunto
```
GET /api/v2/conjunto-dato/{id}
```
Devuelve: `nombre`, `descripcion`, `ficheros[]`, `regionId`, `tipo`, `versiones[]`.

### 3. URL de descarga de un fichero
```
GET /api/v2/fichero/{id}/descarga
```
Devuelve: `{"success": true, "data": {"enlaceDescarga": "https://s3.../GTFS.zip?X-Amz-Signed..."}}`

**⚠️ El enlace S3 caduca en 900 segundos (15 min).**

### 4. Descarga directa del ZIP
```
GET {enlaceDescarga}
```
Devuelve el archivo ZIP GTFS real.

## Estructura del repositorio

```
GTFSSpain/
├── .gitignore              # data/ gitignored (GTFS ZIPs)
├── descargar-nap.py        # Script de descarga (full/delta/dry-run)
├── README.md               # Documentación y resumen de datos
├── metadata/
│   ├── conjuntos-datos.json  # Lista completa (en git)
│   ├── ids-actualizados.json # IDs actualizados en últimas 24h (en git)
│   ├── ultima-descarga.txt   # Timestamp última descarga (en git)
│   └── descarga.log        # Log de descargas (en git)
└── data/                   # GTFS ZIPs (NO en git, ~0.65 GB)
    ├── 00896_Autobus_urbano_de_Madrid/
    │   ├── metadata.json
    │   └── 2060_GTFS-ZIP.zip
    ├── 01386_Autobuses_Xunta_Galicia/
    │   ├── metadata.json
    │   └── 2083_GTFS-ZIP.zip
    └── ...
```

## Script de descarga

**Ubicación:** `/root/workspace/GTFSSpain/descargar-nap.py`

### Modos de uso

```bash
# Descarga completa (primera vez o reset)
python3 descargar-nap.py

# Actualización delta (solo datasets actualizados en últimas 24h)
python3 descargar-nap.py --delta

# Preview sin descargar
python3 descargar-nap.py --dry-run
```

### Lógica del script

1. **Cargar metadatos existentes** (si los hay) desde `metadata/conjuntos-datos.json`
2. **GET /api/v2/conjunto-dato** → obtener lista completa
3. **Filtrar datasets** por tipo y región (opcional)
4. **Para cada dataset:**
   - Si `--delta`: solo si se actualizó en últimas 24h
   - GET `/api/v2/conjunto-dato/{id}` → metadatos + ficheros
   - Filtrar ficheros con `nombreTipoFichero` conteniendo "GTFS"
   - GET `/api/v2/fichero/{id}/descarga` → enlace S3
   - GET `{enlaceDescarga}` → descargar ZIP
   - Guardar en `data/{nombre}/`

### Filtrado de tipos de fichero

Solo descargar ficheros con `nombreTipoFichero` conteniendo:
- **GTFS** → ZIP descargable ✅
- **GTFS-RT** → Tiempo real, NO ZIP ❌
- **NetEx** → Formato diferente, NO ZIP ❌
- **SIRI** → Tiempo real, NO ZIP ❌

## Estrategia de almacenamiento

### Opción A: Solo datos actuales (recomendada)
- **0.65 GB** — datos GTFS actuales
- **Delta semanal** ~100-500 MB descargados
- **Total estable:** ~0.7-1 GB

### Opción B: Con históricos
- **0.65 GB** actuales + **2-3 GB** históricos (3 versiones/dataset)
- **Total:** ~3-4 GB

### Opción C: Full dump semanal
- Descargar TODO cada semana
- **Overhead:** 0.65 GB/semana × 52 = 33.8 GB/año
- **No recomendado** — el delta es suficiente

## Integración con TimeIneco

### Opción 1: Datos locales directos
```javascript
// En server.mjs de TimeIneco
app.get('/gtfs-local/:city/:file', (req, res) => {
  const path = `/root/workspace/GTFSSpain/data/${req.params.city}/${req.params.file}`;
  res.sendFile(path);
});
```

### Opción 2: Parser GTFS en navegador
```javascript
// Cargar ZIP local
const zip = await fetch('/gtfs-local/madrid/2060_GTFS-ZIP.zip');
const blob = await zip.blob();
// Parsear con librería GTFS
const gtfs = await parseGTFS(blob);
```

### Opción 3: Servir desde GTFSSpain directamente
Mount `/root/workspace/GTFSSpain/data/` como directorio servible.

## Top datasets por tamaño

| Dataset | Tamaño | ID | Viajes | Rutas | Paradas |
|---|---|---|---|---|---|
| Xunta de Galicia | 136.4 MB | 1386 | 133K | 6.5K | 26K |
| CRTM Madrid interurbanos | 72.2 MB | 1160 | 55K | 354 | 8.4K |
| Cataluña completa | 66.1 MB | 1536 | 210K | 2.1K | 29K |
| Cataluña simplificada | 56.6 MB | 1535 | 194K | 1.6K | 23K |
| Tenerife TITSA | 21.5 MB | 1130 | 72K | 178 | 3.8K |

## Pitfalls

1. **Enlaces S3 caducan en 15 min** — hay que descargar rápido. No hacer muchos `GET /fichero/{id}/descarga` antes de descargar los ZIPs.
2. **Solo GTFS-ZIP son descargables** — GTFS-RT, NetEx, SIRI no son ZIPs. Filtrar por `nombreTipoFichero`.
3. **Algunos datasets tienen ficheros de 0 bytes** — son datasets con GTFS pero la API no devuelve fichero descargable. Ignorarlos.
4. **161 datasets** — la llamada `GET /conjunto-dato` devuelve ~9 MB de JSON. No cachear indefinidamente.
5. **NAP_API_KEY en `/root/workspace/Time/.env`** — NO en `/hermes-home/.env` ni en `/root/workspace/TimeIneco/.env`. El script busca en ese orden: `TimeIneco/.env` → `Time/.env` → `/.env`.
6. **Data directory gitignored** — los ZIPs nunca van a git. Solo metadatos ligeros.
7. **Delta mode** — solo descarga lo actualizado en últimas 24h. Útil para actualizaciones semanales.
8. **Algunos datasets se actualizan varias veces al día** (Tenerife TITSA: 2.3/día, Comunidad Valenciana: 4.2/día). El delta semanal cubre todos.
9. **Log de "fallos" engañoso** — el script cuenta como fallos las descargas de GTFS-RT y SIRI (tamaño 0.0 MB, son streams en vivo, no ZIPs). Un resumen con "41 fallos" es normal y esperado. Solo los GTFS-ZIP son datos reales descargables. Los GTFS-RT/SIRI siempre fallarán en este script.

## Cron job

**Job:** `gtfsspain-update`
**Frecuencia:** domingo 06:00 UTC
**Comando:** `python3 /root/workspace/GTFSSpain/descargar-nap.py --delta`
**Entrega:** al chat actual (origin)
**Repeticiones:** 52 (1 año)

## Referencias

- `references/nap-api-endpoints.md` — Endpoints API NAP con ejemplos de request/response
- `references/disk-space-warning.md` — Alerta de espacio en disco (94% usado, 1.3 GB libres)