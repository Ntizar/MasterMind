---
name: eubucco-building-stock
description: "Huellas de edificios de la UE con altura y plantas."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [edificios, huellas, altura, parquet, duckdb, 3d, sombras, nuts]
    related_skills: [catastro-api, madrid-solar-shadow-geodata, solar-shadow-computation]
---

# EUBUCCO — stock de edificios europeo

Base de datos científica con **322+ millones de huellas de edificios** (UE-27 + Noruega, Suiza y UK), armonizando 55 datasets abiertos: 62,2 % registros gubernamentales, 20,4 % Microsoft building footprints, 17,4 % OpenStreetMap. DOI Zenodo `10.5281/zenodo.6524780`.

## When to Use (cuándo usarlo)

- Necesitas **altura y nº de plantas** de edificios para 3D de ciudades o **cálculo de sombras solares** fuera de Madrid.
- Quieres datos de edificios de varios países con la **misma estructura** (no un acuerdo por país).
- Buscas acceso a datos vía **Parquet remoto** sin montar infraestructura.

## Acceso verificado

```bash
# Descarga por región NUTS
curl -o CH04.parquet "https://s3.eubucco.com/eubucco/v0.2/buildings/parquet/nuts_id=CH04/CH04.parquet"

# Alternativa con AWS CLI anónimo
aws s3 cp s3://eubucco/v0.2/buildings/parquet/nuts_id=CH04/CH04.parquet . \
    --endpoint-url https://s3.eubucco.com --no-sign-request
```

Lectura directa sin descargar:

```python
# GeoPandas
gdf = gpd.read_parquet(s3_path, storage_options={'anon': True,
        'client_kwargs': {'endpoint_url': 'https://s3.eubucco.com'}})
```

```sql
-- DuckDB
INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial;
SET s3_endpoint='s3.eubucco.com'; SET s3_url_style='path'; SET s3_region='eu';
-- geometría WKB -> ST_AsWKT ; CRS del dataset: EPSG:3035
```

## Atributos y trazabilidad (clave)

Cada atributo lleva su origen: **Ground Truth / Merged / ML Estimated**.

| Atributo | Cobertura | Ground truth |
|---|---|---|
| type | 100 % | 38,1 % |
| subtype | 100 % | 17,3 % |
| height | 100 % | 43,2 % |
| floors | 100 % | 16,6 % |
| construction year | 15,9 % | 15,6 % |

**No tratar los atributos ML-estimated como datos reales**: etiquetarlos o filtrarlos según el uso.

## Pipeline reproducible (9 pasos)

0-downloading → 1-parsing (`.gml/.xml/.shp/.dxf/.pbf`) → 2-db-set-up (partición NUTS/LAU) → 3-attrib-cleaning → 4-conflation (rubbersheeting geométrico + matching ML con XGBoost, repo `ai4up/eubucco-conflation`) → features (`ai4up/eubucco-features`) → predicción (`ai4up/ufo-prediction`) → 5-release → 6-upload. Orquestado en clusters HPC Slurm (`ai4up/slurm-pipeline`) con configs YAML en `database/preprocessing/`.

Arranque: `tutorials/getting-started.ipynb` (descarga, filtro por ciudad, conversión a GeoDataFrame); esquema en `docs.eubucco.com`.

## Referencia

- Repo: `ai4up/eubucco` (~122 ⭐, consultado 2026-09-15). Licencia MIT.
