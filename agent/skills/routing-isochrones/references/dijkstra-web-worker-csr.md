# Dijkstra en Web Worker — Formato CSR Binario + Patrón de Implementación

## Contexto
Implementado en ISOTime (`github.com/Ntizar/ISOTime`, 2026-07-01).
Permite calcular isocronas 100% en el navegador sin API externa ni servidor,
usando grafos viarios OSM pre-calculados y Dijkstra en un Web Worker.

## Formato binario CSR (Compressed Sparse Row)

Serialización compacta del grafo viario. Un grafo de 40K nodos / 78K aristas
ocupa 1.4 MB. El formato está optimizado para carga rápida con `ArrayBuffer`
y `TypedArray` views.

### Estructura del archivo

```
Offset  Tamaño        Campo              Descripción
──────  ────────────  ──────────────────  ──────────────────────────────
0       4 bytes       MAGIC              "ISOG" (identificador)
4       4 bytes       VERSION            u32 LE (actualmente 1)
8       4 bytes       NUM_NODES          u32 LE
12      4 bytes       NUM_EDGES          u32 LE
16      4 bytes       CENTER_LAT         f32 LE (latitud del centro)
20      4 bytes       CENTER_LNG         f32 LE (longitud del centro)
24      4 bytes       RADIUS_KM          f32 LE (radio de cobertura)
28      4 bytes       RESERVED           u32 LE (padding)
32      32 bytes      CITY_NAME          UTF-8 null-padded
64      N×4 bytes     NODE_LATS          f32 LE × NUM_NODES
64+N*4  N×4 bytes     NODE_LNGS          f32 LE × NUM_NODES
64+N*8  (N+1)×4 bytes NODE_OFFSETS       u32 LE × (NUM_NODES+1) — CSR row pointers
...     E×4 bytes     EDGE_TARGETS       u32 LE × NUM_EDGES — nodo destino
...     E×4 bytes     EDGE_LENGTHS       f32 LE × NUM_EDGES — metros
...     E×4 bytes     EDGE_SPEEDS        f32 LE × NUM_EDGES — km/h
```

### Por qué CSR

CSR (Compressed Sparse Row) es el formato estándar para grafos dispersos:
- Los nodos se indexan 0..N-1
- `NODE_OFFSETS[i]` a `NODE_OFFSETS[i+1]` define el rango de aristas salientes del nodo `i`
- Acceso O(1) a las aristas de cualquier nodo
- Sin punteros ni indirección extra — un solo `ArrayBuffer` continuo

### ⚠️ Parseo en JavaScript — CRÍTICO: arrays separados, NO interleaved

**Python escribe lats y lngs como arrays CONTIGUOS separados:**
```python
node_lats.tofile(f)   # [lat0, lat1, ..., latN]
node_lngs.tofile(f)   # [lng0, lng1, ..., lngN]
```

**El error común** es usar zero-copy view que lee como interleaved:
```javascript
// ❌ INCORRECTO — lee [lat0..latN, lng0..lngN] como [lat0,lng0,lat1,lng1,...]
const nodeCoords = new Float32Array(buffer, offset, numNodes * 2);
// nodeCoords[0] = lat0 ✓
// nodeCoords[1] = lat1 ✗ (debería ser lng0)
```

**La corrección** — leer arrays separados e interleavear manualmente:
```javascript
// ✅ CORRECTO
const rawLats = new Float32Array(buffer, latOffset, numNodes);
const rawLngs = new Float32Array(buffer, lngOffset, numNodes);
const nodeCoords = new Float32Array(numNodes * 2);
for (let i = 0; i < numNodes; i++) {
  nodeCoords[i * 2] = rawLats[i];
  nodeCoords[i * 2 + 1] = rawLngs[i];
}
```

**Verificación:** `nodeCoords[0]` = `node_lats[0]`, `nodeCoords[1]` = `node_lngs[0]`. Si `nodeCoords[1]` = `node_lats[1]` → bug interleaved.

### Parseo completo del header

```javascript
function parseGraph(buffer) {
  const view = new DataView(buffer);
  const magic = String.fromCharCode(view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3));
  if (magic !== 'ISOG') throw new Error(`Invalid magic: ${magic}`);
  
  const numNodes = view.getUint32(8, true);
  const numEdges = view.getUint32(12, true);
  const centerLat = view.getFloat32(16, true);
  const centerLng = view.getFloat32(20, true);
  const radiusKm = view.getFloat32(24, true);
  
  let cityName = '';
  for (let i = 32; i < 64 && view.getUint8(i) !== 0; i++) {
    cityName += String.fromCharCode(view.getUint8(i));
  }
  
  // Coords: SEPARATE arrays (NOT interleaved!)
  const latOffset = 64;
  const lngOffset = 64 + numNodes * 4;
  const rawLats = new Float32Array(buffer, latOffset, numNodes);
  const rawLngs = new Float32Array(buffer, lngOffset, numNodes);
  
  const nodeCoords = new Float32Array(numNodes * 2);
  for (let i = 0; i < numNodes; i++) {
    nodeCoords[i * 2] = rawLats[i];
    nodeCoords[i * 2 + 1] = rawLngs[i];
  }
  
  const offsetsOffset = lngOffset + numNodes * 4;
  const nodeOffsets = new Uint32Array(buffer, offsetsOffset, numNodes + 1);
  
  const targetsOffset = offsetsOffset + (numNodes + 1) * 4;
  const edgeTargets = new Uint32Array(buffer, targetsOffset, numEdges);
  
  const lengthsOffset = targetsOffset + numEdges * 4;
  const edgeLengths = new Float32Array(buffer, lengthsOffset, numEdges);
  
  const speedsOffset = lengthsOffset + numEdges * 4;
  const edgeSpeeds = new Float32Array(buffer, speedsOffset, numEdges);
  
  return { numNodes, numEdges, nodeCoords, nodeOffsets, edgeTargets, edgeLengths, edgeSpeeds, centerLat, centerLng, radiusKm, cityName };
}
```

## Script Python de generación

```python
import osmnx as ox
import networkx as nx
import numpy as np
import struct

G = ox.graph_from_point((center_lat, center_lng), dist=radius_km*1000, network_type='drive')
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
G = nx.DiGraph(G)

nodes = list(G.nodes())
G = nx.relabel_nodes(G, {n: i for i, n in enumerate(nodes)})

# ... populate arrays ...

# Escribir binario — lats y lngs como ARRAYS SEPARADOS
with open(f'{city}.bin', 'wb') as f:
    f.write(b'ISOG')
    f.write(struct.pack('<I', 1))
    f.write(struct.pack('<I', num_nodes))
    f.write(struct.pack('<I', num_edges))
    f.write(struct.pack('<f', center_lat))
    f.write(struct.pack('<f', center_lng))
    f.write(struct.pack('<f', radius_km))
    f.write(struct.pack('<I', 0))
    f.write(city_name_bytes.ljust(32, b'\x00'))
    node_lats.tofile(f)    # ← SEPARATE array
    node_lngs.tofile(f)    # ← SEPARATE array
    node_offsets.tofile(f)
    edge_targets.tofile(f)
    edge_lengths.tofile(f)
    edge_speeds.tofile(f)
```

## Web Worker — Dijkstra + Binary Heap + Physical Distance Filter

```javascript
function dijkstra(originNode, cutoffSec, modeSpeed) {
  const n = graph.numNodes;
  const dist = new Float32Array(n).fill(Infinity);
  dist[originNode] = 0;
  const visited = new Uint8Array(n);
  const heap = new MinHeap();
  heap.push(originNode, 0);
  
  const speedMs = modeSpeed > 0 ? modeSpeed / 3.6 : Math.abs(modeSpeed) / 3.6;
  const maxPhysicalDist = cutoffSec * speedMs * 1.3;
  
  const originLat = graph.nodeCoords[originNode * 2];
  const originLng = graph.nodeCoords[originNode * 2 + 1];
  const cosLat = Math.cos(originLat * Math.PI / 180);
  
  const reachable = [];

  while (heap.size > 0) {
    const { node, dist: d } = heap.pop();  // ⚠️ MUST match pop() return shape!
    if (visited[node]) continue;
    visited[node] = 1;
    if (d > cutoffSec) break;
    
    const nLat = graph.nodeCoords[node * 2];
    const nLng = graph.nodeCoords[node * 2 + 1];
    const phyDist = Math.sqrt(
      Math.pow((nLat - originLat) * 111320, 2) +
      Math.pow((nLng - originLng) * 111320 * cosLat, 2)
    );
    if (phyDist > maxPhysicalDist) continue;
    
    reachable.push(node);

    for (let i = graph.nodeOffsets[node]; i < graph.nodeOffsets[node + 1]; i++) {
      const target = graph.edgeTargets[i];
      if (visited[target]) continue;
      const length = graph.edgeLengths[i];
      const edgeSpeed = graph.edgeSpeeds[i] || 50;
      const speed = modeSpeed > 0 ? Math.min(edgeSpeed, modeSpeed) : Math.abs(modeSpeed);
      const time = length / (speed / 3.6);
      const newDist = d + time;
      if (newDist < dist[target]) {
        dist[target] = newDist;
        heap.push(target, newDist);
      }
    }
  }
  return reachable;
}
```

## Velocidades por modo

| Modo | modeSpeed | Significado |
|------|-----------|-------------|
| Coche | 120 | `min(velocidad_vía, 120)` — respeta límites de calle |
| Andando | -5 | 5 km/h fijo |
| Bici | -15 | 15 km/h fijo |

## Métricas reales (ISOTime, 2026-07-01)

| Ciudad | Nodos | Aristas | Tamaño | Tiempo |
|--------|------:|--------:|-------:|-------:|
| Madrid | 40.209 | 78.465 | 1.4 MB | <1s |
| Sevilla | 32.098 | 67.798 | 1.2 MB | <1s |
| Bilbao | 13.643 | 26.661 | 0.5 MB | <0.5s |
| Zaragoza | 13.353 | 25.912 | 0.5 MB | <0.5s |

## Cadena de fallback en el frontend

```javascript
async function calcularIsocrona(lng, lat, modo, minutos, engine = 'auto') {
  if (engine === 'ors') return calcularIsocronaORS(lng, lat, modo, minutos);
  if (engine === 'dijkstra') return calcularIsocronaLocal(lng, lat, modo, minutos);
  if (engine === 'osrm') return calcularIsocronaOSRM(lng, lat, modo, minutos);
  if (engine === 'sim') return calcularIsocronaSim(lng, lat, modo, minutos);

  if (apiKey) try { return await calcularIsocronaORS(...); } catch {}
  if (hasLocalGraph(lat, lng)) try { return await calcularIsocronaLocal(...); } catch {}
  if (['car', 'walk'].includes(modo)) try { return await calcularIsocronaOSRM(...); } catch {}
  return calcularIsocronaSim(...);
}
```

## Pitfalls

1. **OSMnx OOM en VMs pequeñas** — Radio 20km Madrid (40K+ nodos) causa OOM en 2GB RAM. Usar 12km máximo.
2. **Web Worker module loading** — `new Worker(new URL('./worker.js', import.meta.url))` correcto para ES modules.
3. **Transferable objects** — `postMessage(data, [arrayBuffer])` mueve memoria sin copiar.
4. **Float32Array views son zero-copy** — Pero el ArrayBuffer debe mantenerse vivo.
5. **findNearestNode es O(n)** — Brute force. Para 40K nodos <1ms, para más considerar KD-tree.
6. **⚠️ CRÍTICO: Binary format — Python writes SEPARATE arrays, JS must INTERLEAVE** — `node_lats.tofile()` + `node_lngs.tofile()` produce `[lat0..latN][lng0..lngN]`. La view `Float32Array(buffer, off, N*2)` lee como interleaved. **Symptom:** graph loads OK, Dijkstra returns "Muy pocos nodos alcanzables", no JS error. **Verify:** `nodeCoords[0]` vs `node_lats[0]`, `nodeCoords[1]` vs `node_lngs[0]`.
7. **Physical distance filter** — Sin `maxPhysicalDist = cutoffSec * speedMs * 1.3`, Dijkstra a 120km/h alcanza Barcelona desde Madrid → polígono de 9M km².
8. **Web Worker path resolution** — Worker en `js/` resuelve `data/graphs/` relativo a `js/` → 404. Fix: `self.location.href.replace(/js\\/[^/]*$/, '')`.
9. **heap.pop() destructuring** — `pop()` retorna `{node, dist}`. Si desestructuras `{node, d}`, `d` es undefined silencioso.
10. **Web Worker standalone testing** — Para diagnosticar workers sin deploy a Pages, testear directamente en consola:
    ```javascript
    const w = new Worker('./js/dijkstra-worker.js?v=999');
    w.onmessage = (e) => console.log('worker:', JSON.stringify(e.data));
    w.postMessage({cmd:'load', city:'madrid'});
    w.postMessage({cmd:'findNearest', lat:40.4168, lng:-3.7038});
    w.postMessage({cmd:'dijkstra', lat:40.4168, lng:-3.7038, mode:'walking', cutoffSec:1800});
    ```
    Esto es 10x más rápido que push a Pages + hard refresh + cache bust.

## Algoritmos de boundary detection para Dijkstra local

### ❌ NO funciona: Angular sectors (72 direcciones)

El algoritmo original de ISOTime usaba 72 direcciones × N radios, tomando el nodo más lejano alcanzable por dirección. **Resultado: forma de estrella (spiky)** — `ratio = maxDist/avgDist > 20`. Causa: los nodos en la dirección "justo entre" dos sectores quedan fuera del polígono.

### ❌ NO funciona: Marching squares

Algoritmo de contorno para grid numérico. **Falla con isócronas** porque las claves de segmento son floats (``${x1}:${y1}-${x2}:${y2}``) y las precisiones no coinciden → segmentos no se encadenan → boundary rota. Ratio sigue en 21.95.

### ❌ NO funciona: Moore neighborhood boundary walking

Recorre la frontera del grid celda por celda. **No mejora el ratio** porque el grid base (500m) tiene la misma irregularidad angular.

### ✅ Funciona: Convex hull (Andrew's monotone chain)

Toma todos los nodos alcanzables y construye el convex hull. **Resultado suave** — `ratio = 2.11` (casi circular, forma natural). Funciona especialmente bien para Dijkstra walking donde la red de calles es densa y isotrópica.

**Trade-off:** El convex hull sobrestima el área (incluye puntos no alcanzables dentro del hull). Para walking (red densa isotrópica) la sobrestimación es pequeña (~15-20%). Para carreteras con valles encauzados la sobrestimación es mayor.

**Decisión:** Usar convex hull para Dijkstra local. El usuario lo verificó y confirmó que el resultado es "suave y natural" vs las formas de estrella anteriores.
