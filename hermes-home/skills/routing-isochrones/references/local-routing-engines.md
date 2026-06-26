# Motores de Routing Locales — Notas de Sesión (2026-06-25)

## Contexto
David preguntó sobre alternativas a ORS API para calcular isócronas sin dependencia externa. La key de ORS en el proyecto Time no tenía permisos de isócronas (`403: Access to this API has been disallowed`).

## Valhalla — La opción más completa

**Why Valhalla wins:**
- Isochoronas nativas (`/isochrones/{profile}`)
- Profiles: `auto`, `bicycle`, `pedestrian` con velocidades reales por tipo de vía OSM
- Docker: un `docker run` y listo
- Sin API key, sin límites, sin internet tras descarga
- Soporta GTFS para transit routing

**Docker setup:**
```bash
docker run -d --name valhalla \
  -p 8002:8002 \
  -v ./data:/data \
  -e tile_extract=/data/valhalla.tar \
  -e build=true \
  ghcr.io/gis-ops/valhalla:latest
```

**Isochrone endpoint:**
```
GET /isochrones/{profile}?json={"locations":[{"lat":40.4167,"lon":-3.7038}],"costing":"auto","contours":[{"time":15}]}
```

**Profiles:** `auto`, `bicycle`, `pedestrian`

**Size:** Spain PBF ~200MB, Europe ~2GB
**RAM:** 2-4GB for tiles
**Build time:** 30-60 min for full Europe

## OSMnx + NetworkX — Python script approach

```python
import osmnx as ox
import networkx as nx
from shapely.geometry import MultiPoint

G = ox.graph_from_place("Madrid, Spain", network_type='drive')
center = ox.geocode("Plaza Mayor, Madrid")
origin_node = ox.distance.nearest_nodes(G, center[1], center[0])

cutoff = 900  # 15 min in seconds
costs, paths = nx.single_source_dijkstra(G, origin_node, weight='length')
speed_ms = 13.8  # ~50 km/h for driving
reachable = {n: d/speed_ms for n, d in costs.items() if d/speed_ms <= cutoff}

reachable_nodes = [G.nodes[n] for n in reachable]
polygon = MultiPoint([(n['x'], n['y']) for n in reachable_nodes]).convex_hull
```

**Advantage:** No server needed. Script generates GeoJSON for frontend.
**Disadvantage:** Only works for pre-downloaded cities. Graph cached in `~/.cache/osmnx/`.

## Architecture proposal for Time

```
NaN.builders (Node.js frontend)
  └── Proxy to Valhalla (Docker on VPS)
       └── OSM data (spain-latest.osm.pbf)

Alternative: OSMnx pre-calculated GeoJSON per city
  └── Served as static JSON from /data/isochrones/{city}.json
```

## Key decision: ORS API key permissions

The ORS key was returning `403: Access to this API has been disallowed` for isochrone endpoint. This means:
- The key exists and is valid format
- But it lacks isochrone scope (only has routing)
- Some ORS keys from v1 era don't have isochrone permissions
- Fix: create new key at openrouteservice.org (free tier includes isochrones)

**Diagnostic:** Check healthz `ors_api` field. If `false`, key is invalid or lacks permissions.
