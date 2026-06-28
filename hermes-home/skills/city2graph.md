# City2Graph

- **URL:** https://github.com/c2g-dev/city2graph
- **Categoría:** GIS / Geoespacial / Graph Neural Networks
- **¿Qué hace?:** Biblioteca Python para convertir datasets geoespaciales en representaciones de grafos, integrada con GeoPandas, NetworkX y PyTorch Geometric. Permite construir grafos a partir de datos urbanos (edificios, calles, uso de suelo, transporte GTFS, flujos de movilidad) para aplicar GNNs y análisis de redes espaciales. Incluye módulos para construcción de grafos, transporte, morfología urbana, proximidad y movilidad.
- **Casos de uso:**
  - Modelado de redes de transporte urbano con GTFS
  - Análisis de accesibilidad y servicios urbanos con GNNs
  - Predicción de tráfico y flujos de movilidad
  - Análisis morfológico de ciudades (edificios vs calles)
  - Graph Neural Networks para GeoAI
  - Análisis de proximidad y contigüidad espacial
  - Modelado de matrices OD (origen-destino)
  - Predicción de uso de suelo
- **Snippets útiles:**
  ```python
  # Instalación básica
  pip install city2graph
  
  # Con PyTorch (CPU)
  pip install "city2graph[cpu]"
  
  # Con CUDA
  pip install "city2graph[cu128]"
  ```
  ```python
  # Construir grafo de transporte desde GTFS
  from city2graph import load_gtfs, travel_summary_graph
  
  # Cargar feed GTFS
  gtfs_data = load_gtfs("path/to/gtfs.zip")
  
  # Obtener pares OD
  od_pairs = get_od_pairs(gtfs_data)
  
  # Crear grafo de resumen de viajes
  graph = travel_summary_graph(gtfs_data)
  ```
  ```python
  # Grafo morfológico (edificios + calles)
  from city2graph import morphological_graph
  
  graph = morphological_graph(
      buildings_gdf=buildings,
      segments_gdf=streets,
      center_point=center,
      distance=500,
      as_nx=False  # True para NetworkX, False para GeoDataFrame dict
  )
  ```
  ```python
  # Convertir a PyTorch Geometric
  from city2graph import gdf_to_pyg, nx_to_pyg
  
  # GeoDataFrame → PyG Data
  pyg_data = gdf_to_pyg(gdf, device='cuda')
  
  # NetworkX → PyG Data
  pyg_data = nx_to_pyg(nx_graph, device='cuda')
  ```
  ```python
  # Grafo de proximidad (KNN, Gabriel, Waxman)
  from city2graph import proximity_graph
  
  graph = proximity_graph(
      gdf,
      method='knn',    # knn, gabriel, relative_neighborhood, waxman
      k=10,            # para knn
      distance=500,    # distancia máxima
      as_nx=True
  )
  ```
- **Cómo integrarlo en proyectos:**
  1. Instalar: `pip install city2graph` (core) o `pip install "city2graph[cpu]"` (con PyTorch)
  2. Para desarrollo con uv: `uv sync --extra cpu --group dev`
  3. Cargar datos geoespaciales con GeoPandas (shapefiles, GeoJSON, Overture Maps)
  4. Elegir módulo según necesidad:
     - `transportation.py` → GTFS y redes de transporte
     - `morphology.py` → edificios y calles
     - `proximity.py` → grafos basados en distancia
     - `mobility.py` → flujos de movilidad
     - `graph.py` → conversión a PyTorch Geometric
  5. Usar `gdf_to_pyg()` para convertir a tensores de GNN
  6. Los grafos resultantes son compatibles con PyTorch Geometric directamente
  7. Ejemplos en docs: `docs/examples/` (notebooks)
  8. Documentación: https://city2graph.net
- **Fecha de aprendizaje:** 2026-05-26
- **Stars:** 1210
- **Licencia:** BSD 3-Clause
