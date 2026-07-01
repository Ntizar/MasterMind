# MITMA Open Data Movilidad — Referencia completa

**Fuente:** Ministerio de Transportes y Movilidad Sostenible
**URL:** https://www.transportes.gob.es/ministerio/proyectos-singulares/estudios-de-movilidad-con-big-data/opendata-movilidad
**Bucket S3:** https://movilidad-opendata.mitma.es/
**Bucket name:** `mitma-movilidad-v2`
**Datos desde:** Enero 2022 hasta la actualidad (3-4 días de decalaje)
**Fuente:** Posicionamiento de teléfonos móviles (Orange), LO 3/2018
**Licencia:** Datos abiertos MITMA
**Paquete R:** https://ropenspain.github.io/spanishoddata/

## Exploración del bucket (técnica S3)

El bucket es S3-compatible y se explora con curl + parámetros query:

```bash
# Listar prefijos de nivel superior
curl -sL "https://movilidad-opendata.mitma.es/?delimiter=/&max-keys=200"

# Listar subcarpetas de un prefijo
curl -sL "https://movilidad-opendata.mitma.es/?prefix=estudios_basicos/&delimiter=/&max-keys=20"

# Listar ficheros concretos
curl -sL "https://movilidad-opendata.mitma.es/?prefix=estudios_basicos/por-municipios/viajes/ficheros-diarios/2024-09/&max-keys=5"
```

**Extraer keys/prefixes del XML:**
```bash
# Keys (ficheros)
curl -sL "URL" | grep -oP '<Key>[^<]+</Key>'
# Prefixes (carpetas)
curl -sL "URL" | grep -oP '<Prefix>[^<]+</Prefix>'
```

## Estructura del bucket

```
/
├── LEEME_CambioMetodología_IndicadoresBigdata_posteriores_a_20250701.pdf
├── LEEME_Especificaciones_indicadores_OpenDataMovilidad.xlsx
├── LICENCIA de datos abiertos del MITMA 20201203.pdf
├── RSS.xml                          ← Listado completo de ficheros (~7MB)
├── index.html                       ← Explorador web
│
├── estudios_basicos/                ← DIARIO, desde 2022
│   ├── calidad/                     ← Metadatos de calidad por día
│   │   └── ficheros-diarios/YYYY-MM/YYYYMMDD_distritos_descartados.csv
│   ├── estadisticos/
│   ├── movilidad_agregada_mensual/
│   ├── por-GAU/                     ← Grandes Áreas Urbanas
│   ├── por-distritos/               ← Distritos censales
│   ├── por-municipios/              ← Municipal (PRINCIPAL)
│   │   ├── pernoctaciones/
│   │   ├── personas/
│   │   └── viajes/
│   │       ├── ficheros-diarios/YYYY-MM/YYYYMMDD_Viajes_municipios.csv.gz
│   │       └── meses-completos/
│   └── cambio_metodológico_2025/
│
├── estudios_completos/              ← MENSUAL, indicadores avanzados
│   ├── por-GAU/
│   ├── por-distritos/
│   ├── por-municipios/
│   │   ├── etapas-sin-medio-modo/
│   │   ├── frecuencia/              ← Recurrencia de viajes (14 días/mes)
│   │   └── viajes-sin-medio-modo/
│   └── tiempos de viaje/
│
├── estudios_rutas/                  ← RUTAS POR CARRETERA
│   ├── calidad/
│   ├── geometria/                   ← Geometrías de rutas
│   ├── informacion_tramo/           ← Info por tramo de carretera
│   ├── od_rutas/                    ← Rutas OD (origin-destination)
│   └── tramo_ruta/                  ← Tramos de ruta
│
└── zonificacion/                    ← Geometrías de zonificación
    ├── poblacion.csv
    ├── relacion_ine_zonificacionMitma.csv
    ├── zonificacion_GAU/            ← Shapefiles GAUS
    └── zonificacion_distritos/      ← Shapefiles distritos censales
```

## Formato de datos — Viajes municipales

**Delimiter:** `|` (pipe)
**Compresión:** `.csv.gz`
**URL ejemplo:** `https://movilidad-opendata.mitma.es/estudios_basicos/por-municipios/viajes/ficheros-diarios/2024-09/20240901_Viajes_municipios.csv.gz`

| Columna | Tipo | Valores ejemplo |
|---------|------|----------------|
| fecha | int | 20240901 |
| periodo | str | 00-23 (franja horaria) |
| origen | str | Código municipio INE (ej: 01001) |
| destino | str | Código municipio INE (ej: 01009_AM) |
| distancia | str | 2-10, 10-50, >50 km |
| actividad_origen | str | casa, trabajo_estudio, frecuente, no_frecuente |
| actividad_destino | str | casa, trabajo_estudio, frecuente, no_frecuente |
| estudio_origen_posible | str | si/no |
| estudio_destino_posible | str | si/no |
| residencia | str | Código INE residencia |
| renta | str | 10-15, >15 (rangos de renta media) |
| edad | str | 0-25, 25-45, 45-65, NA |
| sexo | str | hombre/mujer/NA |
| viajes | float | Número estimado de viajes (con decimales) |
| viajes_km | float | Kilómetros totales |

## Incidencias conocidas

- **DANA Valencia 2024:** 29-31 oct 2024 — anomalías en antenas Orange Levante
- **Incidencias Orange 2023:** 26,27,30,31 oct + 1,2,3 nov 2023
- **Incidencias Orange 2024:** 4,18,19 abr + 10,11 nov 2024

## Volumen estimado

- Datos diarios desde enero 2022 → ~1,300 días de datos
- Cada día: un CSV gzipped por zonificación × tipo (viajes, personas, pernoctaciones)
- Total estimado: varios GB de CSVs comprimidos
- RSS.xml tiene 7MB → miles de ficheros listados

## Integración con proyectos TimeIneco

### Datos OD (Origin-Destination) → Matrices de viajes reales
- Cruzar con 161 datasets NAP (transporte público)
- Cruzar con 74 redes GBFS (bicicletas compartidas)
- Las matrices OD dan la demanda real de movilidad → dónde va la gente

### Rutas por carretera → Geometrías reales
- Las geometrías en `estudios_rutas/geometria/` son las rutas que la gente USA realmente
- Comparar con rutas calculadas por ORS/Valhalla
- Datos disponibles para semanas tipo: agosto/oct 2022, oct 2023

### Datos de calidad → Fiabilidad
- CSVs `distritos_descartados.csv` por día → qué distritos NO son fiables
- Incidencias Orange → qué días tienen datos incompletos

### Dimensiones de análisis
- **Temporal:** 24 franjas horarias × 365 días × 4 años
- **Espacial:** Municipal, distritos censales, GAUS
- **Demográfico:** Renta (2 niveles), edad (4 rangos), sexo
- **Funcional:** Actividad origen/destino (casa, trabajo, frecuente, no frecuente)
- **Distancia:** 3 bandas (2-10, 10-50, >50 km)

## Integración con proyectos GBFSSpain

### Demanda real vs oferta de bicicletas
- Flujos OD por municipio → qué municipios generan más viajes
- Franja horaria → picos de movilidad (coincide con disponibilidad bicis?)
- Distancia 2-10 km → rango donde la bicicleta es competitiva
- Actividad "casa→trabajo" → movilidad laboral que podría ser en bici
