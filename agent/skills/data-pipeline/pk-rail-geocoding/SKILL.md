---
name: pk-rail-geocoding
version: "1.0.0"
author: "David Antizar (Ntizar) — ejecutado por Mastermind"
license: "MIT"
description: "Geolocalizar puntos por PK sobre la vía ADIF vía WFS."
tags: [railway, geocoding, adif, wfs, pk, interpolation, geojson, leaflet, transport]
created: "2026-08-28"
---

# PK Rail Geocoding — Interpolación de puntos kilométricos sobre la red ADIF

## Cuándo usar

- Dataset ferroviario español con PK (ej: "P.K. 429,825", "368+925") y código/nombre de línea
- El usuario pide que los puntos "estén bien en su sitio sobre las vías del tren que aparecen en el mapa"
- El geocoding por nombre de estación (Nominatim / DB local) deja puntos a cientos de metros o kilómetros del trazado
- Necesitas precisión de metros (los puntos caen EXACTOS sobre la geometría de la vía)

## Fuentes de datos (WFS Tramificación ADIF — público, sin auth)

**URL base:** `https://ideadif.adif.es/gservices/Tramificacion/wfs` (WFS 2.0.0)

| Capa | Features | Uso en la interpolación |
|------|----------|------------------------|
| `Tramificacion:TramosServicio` | 1.178 (verificado 2026-08-28) | Segmentos de vía EN SERVICIO con `cod_eje` (código de línea) + `pki`/`pkd` (rango PK del tramo) + geometría LineString. ES LA CAPA CLAVE. |
| `Tramificacion:PKTeoricos` | 17.200 | Puntos kilométricos teóricos con coordenada SOBRE la vía + `codtramo` + código provincia INE. Fallback cuando el tramo no casa. |

**Descarga completa (guardar en el repo, ~20MB total):**
```bash
# Tramos en servicio (la capa para interpolar)
curl -s -o data/adif-tramos.geojson "https://ideadif.adif.es/gservices/Tramificacion/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=Tramificacion:TramosServicio&outputFormat=application/json&srsName=EPSG:4326&count=2000"

# PK teóricos (fallback)
curl -s -o data/adif-pkteoricos.geojson "https://ideadif.adif.es/gservices/Tramificacion/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=Tramificacion:PKTeoricos&outputFormat=application/json&srsName=EPSG:4326&count=25000"
```

⚠️ Pedir `srsName=EPSG:4326` — el WFS usa EPSG:25830 por defecto (ver también skill `government-data-pipelines` → `references/adif-spatial-data-apis.md` para el resto de capas, LTV FeatureServer, WMS de visualización y pitfalls generales).

## Algoritmo de interpolación (estrategia en cascada)

Para cada informe con PK + línea:

1. **Parsear PK** — formatos vistos: `"P.K. 429,825"` (coma decimal), `"368+925"` (km+m), `"PK 12,3"`. Normalizar siempre a float de km: coma→punto; `368+925` → `368.925`.
2. **Parsear línea** — patrones: código suelto (`"100"`), `"100 Hendaya a Madrid"` (código + nombre), nombre con tramo (`"400 Alcázar de San Juan-Cádiz"`). Extraer el código numérico inicial si existe.
3. **Candidatos por cod_eje** — filtrar `TramosServicio` cuyo `cod_eje` empiece por el código de línea del informe (el cod_eje de ADIF es código de línea + tramo: `"10001003"` casa con línea `"100"`). Si no hay candidatos, probar match por nombre de línea contra atributos de texto del tramo.
4. **Interpolar PK dentro del tramo** — para cada candidato cuyo rango `[pki, pkd]` contenga el PK: posición fraccional `t = (pk - pki) / (pkd - pki)`, y punto = vértice del LineString a distancia proporcional (`t * longitud_geom`). La geometría en EPSG:4326 sirve: el error por usar grados en vez de metros es <1% para tramos cortos.
5. **Fallback PKTeoricos** — si ningún tramo casa: punto PKTeoricos más cercano en PK con `codtramo` compatible. Coordenada ya está sobre la vía.
6. **Fallback geocoding clásico** — estación + Nominatim/DB local (ver skill `government-data-pipelines`). Marcar estos registros como `metodo: "estacion"` para saber que su precisión es menor.

**Resultado con datos reales (era-visor, 2026-08-28):** de 318 informes ES → 215 exactamente sobre la vía (172 interpolados en tramo + 43 PK teórico), el resto por estación. Asturias/Cantabria verificadas en coordenadas correctas.

## Pitfalls

- **🔴 `cod_eje` ≠ código de línea directamente:** el cod_eje incluye el tramo (`10001003` = línea 100, tramo 3). Filtrar por prefijo, no por igualdad. El mismo PK puede existir en varias líneas — el código de línea del informe es el que desambigua.
- **🔴 PK en coma decimal vs formato km+m:** `"P.K. 429,825"` es 429.825 km; `"368+925"` es 368.925 km (m, NO fracción). Ambos → float km antes de comparar con `pki/pkd`.
- **⚠️ Rango de PK puede ir en dirección inversa:** algunos tramos tienen `pki > pkd` (PK decreciente). Comparar con min/max del rango, no asumir orden.
- **⚠️ Vías duplicadas (doble vía):** puede haber 2 tramos solapados para el mismo cod_eje y PK — cualquier punto es válido (están a pocos metros).
- **⚠️ Tramos fuera de servicio:** usar solo `TramosServicio`. `TramosFueraServicio` es capa separada — líneas suprimidas darían falsos positivos.
- **⚠️ Distancias en EPSG:4326:** haversine en grados da errores <1% para tramos de decenas de km — aceptable para visualización. Para precisión topográfica, reproyectar a EPSG:25830.
- **⚠️ PKTeoricos sin filtro de línea:** solo como fallback cuando el match de tramo ha fallado; con varias líneas con mismo PK, requiere código de tramo para desambiguar.
- **WFS count alto:** `count=25000` cubre PKTeoricos completo (17.200). El server acepta; no paginar con startIndex salvo timeouts.

## Script de referencia

Ver `era-visor/scripts/geocodificar_via.py` (repo `Ntizar/era-visor`) — implementación completa: parseo de PK/línea, cascada tramo→PKTeoricos, actualización de JSONs de la DB, stats de método. Patrón replicable para cualquier país/dataset con PK.

## Integración en visor

- Pintar los puntos sobre la capa WMS `TramificacionComun` (visual) + tramos WFS si se quiere clic interactivo.
- Guardar en cada registro el método de geocoding (`metodo: "tramo"|"pkteorico"|"estacion"`) — permite auditar la precisión y filtrar.
- Si el dataset tiene provincia, verificar coherencia: un punto de Asturias no puede caer en Andalucía — si cae, el match de línea es erróneo.

---
"Hecho con ❤️ por David Antizar"

## Comparativa de alternativas

- **[nicolaswurtz/...sncf](https://github.com/nicolaswurtz)** — dataset de infraestructura ferroviaria SNCF con PKs geolocalizados, altitudes, velocidades y posicionamiento en tiempo real; referencia de datos ferroviarios georreferenciados (como el PK sobre vía ADIF de este skill).