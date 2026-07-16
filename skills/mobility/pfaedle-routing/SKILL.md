---
name: pfaedle-routing
description: pfaedle — map-matching preciso para feeds GTFS. Genera shapes de alta calidad a partir de datos de tránsito.
---

# pfaedle — Map-Matching para GTFS

## Qué hace

[pfaedle](https://github.com/ad-freiburg/pfaedle) es un motor de map-matching de alta precisión para feeds de transporte público. Genera shapes de ruta de alta calidad a partir de datos GPS de vehículos, ideal para corregir shapes GTFS incorrectos o incompletos.

## Instalación

```bash
# pfaedle es una herramienta C++ que se compila desde fuente
git clone https://github.com/ad-freiburg/pfaedle.git
cd pfaedle
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

## Uso básico

```bash
# Map-match tracks GPS a una ruta GTFS
pfaedle --gtfs feed.zip --tracks tracks.csv --output matched.zip

# Validar shapes existentes
pfaedle --gtfs feed.zip --validate-shapes
```

## Integración con pipelines GTFS

```python
# Ejemplo de integración con node-gtfs o gtfstidy
# 1. Validar con gtfstidy
# 2. Corregir shapes con pfaedle
# 3. Exportar resultado
```

## Pitfalls

- Requiere datos GPS de alta calidad (frecuencia ≥ 1 Hz)
- Necesita un archivo OSM del área de interés para el map-matching
- El rendimiento depende del tamaño del área y la cantidad de tracks
- Compatible con Linux principalmente

## Referencias

- Repo: https://github.com/ad-freiburg/pfaedle
- Relacionado: `gtfs-tidy`, `node-gtfs`, `graphhopper-routing`, `valhalla-routing`
- Paper: "pfaedle: Precise Map-Matching for Public Transit Feeds" (Freiburg University)