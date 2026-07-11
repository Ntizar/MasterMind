# Round-trip verificado con feed real Valencia EMT — 2026-07-08

## Feed de prueba

- **Origen:** EMT Valencia (GTFS público)
- **Tamaño:** 1.4 MB ZIP
- **Contenido:** 1 agencia, 214 rutas, 13.566 viajes, 236.134 stop_times, 144 paradas, 900 shapes (20 shape_ids), 9 calendarios, 54 calendar_dates

## Resultados del round-trip GTFS → NeTEx → GTFS

| Categoría | Original | Recuperado | Diff | Estado |
|---|---|---|---|---|
| Agencias | 1 | 1 | 0 | ✅ |
| Paradas | 144 | 144 | 0 | ✅ |
| Rutas | 214 | 214 | 0 | ✅ |
| Viajes | 13.566 | 13.566 | 0 | ✅ |
| Stop times | 236.134 | 236.134 | 0 | ✅ |
| Calendarios | 9 | 9 | 0 | ✅ |
| Calendar dates | 54 | 54 | 0 | ✅ |
| Shapes | 900 | 900 | 0 | ✅ |

**Cero pérdida de información.** Coordenadas de shapes exactas (error < 0.0001).

## Tiempos de ejecución

| Fase | Tiempo |
|---|---|
| Lectura GTFS | 1.1s |
| GTFS → NeTEx (writer) | 81.5s |
| NeTEx → GTFS (reader) | 10.8s |
| Escritura GTFS .txt | 1.5s |
| **Total** | **~95s** |

## XML generado

- Tamaño: 52.7 MB (55.256.539 chars)
- IDs totales: 259.286
- IDs únicos: 259.286
- IDs duplicados: 0

## Bug encontrado y fixeado

### Shapes: Position vs Point

El `netex_writer` genera:
```xml
<LineGeometry id="ES:LineGeometry:ES:1" srsName="EPSG:4326">
  <positions>
    <Position>
      <Latitude>39.6228408813</Latitude>
      <Longitude>-0.590277791</Longitude>
    </Position>
    ...
  </positions>
</LineGeometry>
```

Pero el `netex_reader` buscaba `<Point>` (que no existe). Fix: buscar `<Position>` dentro de `<positions>` y leer `<Latitude>`/`<Longitude>` directamente.

## Comando para reproducir

```python
import sys
sys.path.insert(0, '/root/workspace/netex')

from converter.gtfs_reader import GTFSReader
from converter.netex_writer import NeTExWriter
from converter.netex_reader import NeTExReader
from converter.gtfs_writer import GTFSWriter
from converter.config import Config

# GTFS → NeTEx
reader = GTFSReader('/tmp/valencia-gtfs.zip')
feed = reader.read()
writer = NeTExWriter(feed, Config(publisher_name='EMT Valencia'))
writer.to_file('/tmp/valencia-netex.xml')

# NeTEx → GTFS
reader2 = NeTExReader('/tmp/valencia-netex.xml')
feed_rt = reader2.read()

# Verificar
assert len(feed_rt.routes) == len(feed.routes)          # 214 == 214
assert len(feed_rt.trips) == len(feed.trips)            # 13566 == 13566
assert len(feed_rt.stop_times) == len(feed.stop_times)  # 236134 == 236134
assert len(feed_rt.shapes) == len(feed.shapes)          # 900 == 900
```
