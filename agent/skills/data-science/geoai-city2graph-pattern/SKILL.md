---
name: geoai-city2graph-pattern
description: "Usa a convertir geoespacial a grafos con City2Graph."
version: "2.0.0"
tags: [geoai, city2graph, grafos, geopandas, pyg, redes, transporte]
related_skills: [geoai-city2graph-pattern, osm-infrastructure-mapping, transit-data-pipelines]
---

# City2Graph — datos geoespaciales → grafos (API real)

> ⚠️ Corrección 2026-09-05 (auditoría): `c2g.build_graph`/`build_proximity_graph`/`build_transit_graph`/`compute_isochrones` **no existen**. La API real usa `knn_graph`/`delaunay_graph`/`waxman_graph` (proximity), `morphological_graph(s)` (morphology), `load_gtfs`/`load_gbfs`/`travel_summary_graph` (transporte), `od_matrix_to_graph` (mobility), `gdf_to_pyg`/`pyg_to_nx` (grafos).

**Repo:** `https://github.com/c2g-dev/city2graph` (Python, ~1.9K⭐).

## When to Use

- Cuando pidas **convertir datos geoespaciales** (geodataframes, GTFS/GBFS) en **grafos** para análisis de redes/IA urbana.

## Uso (API real)

```python
import city2graph as c2g
graph = c2g.knn_graph(gdf, k=... )            # proximity: knn_graph / delaunay_graph / waxman_graph
graph = c2g.morphological_graph(...)          # morphology
graph = c2g.travel_summary_graph(...)          # transporte (load_gtfs / load_gbfs)
graph = c2g.od_matrix_to_graph(...)            # movilidad
gfp = c2g.gdf_to_pyg(gdf, ...)                 # GeoDataFrame → PyG Data
nx_g = c2g.pyg_to_nx(gfp)
```

## Pitfalls

- **No** `build_graph`/`build_proximity_graph`/`build_transit_graph`/`compute_isochrones`.
- Atributos: usa las funciones de arriba; no `graph.node_features`/`edge_index`/`labels` directos.
- DOI real del README no es 10.5281/zenodo.15858845 (verificar en el repo).

## Verificación

- `knn_graph(gdf)` de un dataset y mirar `gdf_to_pyg` para alimentar una GNN.
