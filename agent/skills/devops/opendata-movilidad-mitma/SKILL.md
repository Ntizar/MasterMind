---
name: opendata-movilidad-mitma
version: "1.0.0"
description: >
  Open Data Movilidad del Ministerio de Transportes (MITMA). Datos reales de movilidad en España
  basados en posicionamiento de móviles Orange. Desde enero 2022 hasta la actualidad.
  Bucket S3 público con matrices OD, rutas por carretera, pernoctaciones y personas.
---

# Open Data Movilidad — MITMA

## Qué es

Datos abiertos de movilidad del Ministerio de Transportes y Movilidad Sostenible.
Fuente: posicionamiento de teléfonos móviles (Orange), con cumplimiento LO 3/2018.
Periodo: enero 2022 → actualidad (3-4 días de decalaje para procesamiento).

## Acceso

- **Bucket S3 público:** `https://movilidad-opendata.mitma.es/`
- **Nombre bucket:** `mitma-movilidad-v2`
- **Explorador web:** `https://movilidad-opendata.mitma.es/index.html`
- **RSS (listado completo):** `https://movilidad-opendata.mitma.es/RSS.xml` (7 MB)
- **Paquete R alternativo:** https://ropenspain.github.io/spanishoddata/
- **Licencia:** Datos abiertos MITMA (PDF en el bucket)
- **Metodología:** PDF + XLSX de especificaciones en la raíz del bucket

## Estructura del bucket

```
/
├── LEEME_CambioMetodología_IndicadoresBigdata_posteriores_a_20250701.pdf
├── LEEME_Especificaciones_indicadores_OpenDataMovilidad.xlsx
├── LICENCIA de datos abiertos del MITMA 20201203.pdf
├── RSS.xml / index.html
│
├── estudios_basicos/              ← DIARIO desde 2022
│   ├── calidad/                   ← CSVs de distritos descartados por día
│   ├── estadisticos/
│   ├── movilidad_agregada_mensual/
│   ├── por-GAU/                   ← Grandes Áreas Urbanas
│   ├── por-distritos/             ← Distritos censales
│   ├── por-municipios/            ← MUNICIPAL (el principal)
│   │   ├── viajes/                ← Matrices OD
│   │   ├── pernoctaciones/
│   │   └── personas/
│   └── cambio_metodológico_2025/
│
├── estudios_completos/            ← MENSUAL, indicadores avanzados
│   ├── por-municipios/
│   │   ├── frecuencia/            ← Recurrencia de viajes (14 días/mes)
│   │   ├── etapas-sin-medio-modo/
│   │   └── viajes-sin-medio-modo/
│   └── tiempos de viaje/
│
├── estudios_rutas/                ← RUTAS POR CARRETERA
│   ├── od_rutas/                  ← Rutas OD completas
│   ├── tramo_ruta/                ← Tramos de carretera
│   ├── informacion_tramo/         ← Info por tramo
│   ├── geometria/                 ← Geometrías de rutas
│   └── calidad/
│
└── zonificacion/                  ← Geometrías y metadatos
    ├── poblacion.csv
    ├── relacion_ine_zonificacionMitma.csv
    ├── zonificacion_GAU/          ← Shapefiles (.shp/.dbf/.prj/.shx/.qpj)
    └── zonificacion_distritos/    ← Shapefiles distritos censales
```

## Formato de datos

**Delimiter:** `|` (pipe)
**Compresión:** `.csv.gz`
**Codificación municipios:** Códigos INE

### Columnas (viajes municipales)

```
fecha|periodo|origen|destino|distancia|actividad_origen|actividad_destino|
estudio_origen_posible|estudio_destino_posible|residencia|renta|edad|sexo|
viajes|viajes_km
```

| Columna | Valores |
|---------|---------|
| fecha | YYYYMMDD |
| periodo | 00-23 (franja horaria) |
| origen/destino | Código INE municipio |
| distancia | 2-10, 10-50, >50 km |
| actividad_* | casa, trabajo_estudio, frecuente, no_frecuente |
| renta | 10-15, >15 (rango) |
| edad | 0-25, 25-45, 45-65, NA |
| sexo | hombre, mujer, NA |
| viajes | Número estimado de viajes |
| viajes_km | Kilómetros totales |

## Cómo descargar un fichero

```bash
curl -sL "https://movilidad-opendata.mitma.es/estudios_basicos/por-municipios/viajes/ficheros-diarios/2024-09/20240901_Viajes_municipios.csv.gz" | gunzip
```

## Listar ficheros disponibles

```bash
# Por prefijo
curl -sL "https://movilidad-opendata.mitma.es/?prefix=estudios_basicos/por-municipios/viajes/ficheros-diarios/2024-09/&max-keys=10"

# Con delimitador (solo carpetas)
curl -sL "https://movilidad-opendata.mitma.es/?prefix=estudios_basicos/&delimiter=/&max-keys=20"
```

## Incidencias conocidas

- **DANA Valencia 2024:** 29-31 oct 2024 — anomalías en antenas Orange Levante
- **Incidencias Orange 2023:** 26,27,30,31 oct + 1,2,3 nov 2023
- **Incidencias Orange 2024:** 4,18,19 abr + 10,11 nov 2024
- **Cambio metodología jul  2025:** Ver PDF `LEEME_CambioMetodología_IndicadoresBigdata_posteriores_a_20250701.pdf`

## Potencial de uso

- **TimeIneco2:** Matrices OD reales, rutas carretera, análisis DANA, patrones renta vs movilidad
- **GBFSSpain:** Flujos reales vs cobertura bicicletas, patrones horarios
- **Dashboards/mapas:** Heatmaps, flujos OD, análisis equidad territorial
- **Cruces:** INE (población/renta), ESIOS (energía), Idealista (vivienda)

## Dashboard PowerBI (datos transportes.gob.es)

- **URL:** https://data.transportes.gob.es/public/mov-diaria-mensual
- Es un **Power BI embebido** con datos de movilidad diaria y mensual
- **Fuente de datos:** El mismo S3 de MITMA (`movilidad-opendata.mitma.es`)
- **Acceso:** Solo vía navegador web (Power BI no expone API REST directa)
- La URL `data.transportes.gob.es` sirve como portal público de visualización

## Visualización en Visor Hermes (Fomento)

Los datos de movilidad big data también se visualizan en el **Visor Hermes** del Ministerio:
- URL: https://mapas.fomento.gob.es/VisorHermes/
- Capa ArcGIS REST: `BigData/Movilidad_Big_Data_2/MapServer`
- Capas: Viajes OD, viajeros/día, viajes por distancia, entradas/salidas
- Ver skill `visor-hermes-fomento` para detalles de las capas REST

## Nota

Guardado 2026-06-30. Pendiente de integración cuando David lo solicite.
Nota completa en: `/root/workspace/notes/2026-06-30-opendata-movilidad-mitma.md`
