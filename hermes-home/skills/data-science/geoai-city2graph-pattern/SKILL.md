---
name: geoai-city2graph-pattern
description: "Patrón GeoAI con City2Graph: convertir datos geoespaciales en grafos para Graph Neural Networks y análisis de redes urbanas. Integración GeoPandas → NetworkX → PyTorch Geometric. Modelado de transporte, proximidad, flujo de movilidad."
version: "1.0.0"
category: data-science
tags: [data-science, geoai, city2graph, GNN]

---

# GeoAI City2Graph Pattern

Patrón para convertir datos geoespaciales en grafos para Graph Neural Networks (GNNs) y análisis de redes urbanas usando City2Graph.

**Referencia:** https://github.com/c2g-dev/city2graph (1.2k⭐, DOI: 10.5281/zenodo.15858845)

## ¿Qué es City2Graph?

Biblioteca Python que transforma datasets geoespaciales en representaciones graph, proporcionando una interfaz integrada entre GeoPandas, NetworkX y PyTorch Geometric.

```bash
pip install city2graph
pip install city2graph[cpu]  # Con PyTorch y PyG
```

## Casos de Uso Principales

### 1. Graph Construction for GeoAI
Construir grafos a partir de datos urbanos (edificios, calles, uso de suelo) para aplicaciones GeoAI y GNN.

### 2. Transportation Network Modeling
Consultar feeds GTFS a través de DuckDB y construir grafos de transporte detallados para análisis de accesibilidad.

### 3. Proximity and Contiguity Analysis
Crear grafos basados en proximidad espacial y adyacencia, incluyendo filtrado de distancia multi-centro y isocronas.

### 4. Mobility Flow Analysis
Modelar y analizar patrones de movilidad urbana desde bike-sharing, migración y flujos peatonales.

## Pipeline Típico

```python
import city2graph as c2g
import geopandas as gpd

# 1. Cargar datos geoespaciales
streets = gpd.read_file("streets.geojson")
buildings = gpd.read_file("buildings.geojson")
poi = gpd.read_file("poi.geojson")

# 2. Construir grafo
graph = c2g.build_graph(
    streets=streets,
    buildings=buildings,
    poi=poi,
    method="projected"  # o "geographic"
)

# 3. Extraer features para GNN
node_features = graph.node_features
edge_index = graph.edge_index
y = graph.labels

# 4. Entrenar GNN con PyTorch Geometric
from torch_geometric.data import Data
data = Data(x=node_features, edge_index=edge_index, y=y)
```

## Integración con Datos de Transporte (Ntizar)

Este patrón es directamente aplicable a los proyectos de transporte de Ntizar:

### NAP Dashboard (Transportes de España)
- GTFS feeds de todos los operadores de transporte españoles
- Construir grafos de rutas, paradas y conexiones
- Análisis de accesibilidad y cobertura
- Isocronas de tiempo de viaje

### Bicimad Integration
- Estaciones de bicimad como nodos del grafo
- Conexiones físicas como aristas
- Análisis de red de movilidad

### Faros España
- Rutas marítimas como grafos
- Análisis de conectividad portuaria

## Patrones Avanzados

### Isochrone Graphs
```python
# Isocronas multi-centro para análisis de accesibilidad
isochrones = c2g.compute_isochrones(
    network=graph,
    origins=stations,
    max_time=1800,  # 30 minutos
    steps=60
)
```

### POI Proximity Graphs
```python
# Grafos de proximidad basados en POIs
poi_graph = c2g.build_proximity_graph(
    points=poi,
    method="knn",
    k=10,
    weights="distance"
)
```

### GTFS Transit Graph
```python
# Grafo de transporte público desde GTFS
transit_graph = c2g.build_transit_graph(
    gtfs_dir="/path/to/gtfs",
    duckdb_path="transit.db"
)
```

## Aplicación al Sistema Eléctrico

El patrón GeoAI puede extenderse al SistemaEléctricoFuturo:
- Subestaciones como nodos
- Líneas de transmisión como aristas
- Análisis de estrés de red con GNNs
- Predicción de fallos con graph convolution

## Beneficios del Patrón

1. **Unificación:** GeoPandas → NetworkX → PyG en una sola API
2. **Escalabilidad:** Soporta datasets grandes con optimizaciones
3. **Multi-dominio:** Calles, transporte, edificios, POIs, movilidad
4. **GNN-ready:** Salida directa en formato PyTorch Geometric
5. **Reproductible:** DOI zenodo, tests, CI/CD

## Limitaciones Conocidas

- Requiere datos geoespaciales en formatos compatibles (GeoJSON, Shapefile, etc.)
- El procesamiento de grafos grandes puede ser intensivo en memoria
- Las isocronas requieren un grafo de red de transporte pre-construido