---
name: point-to-footprint-geometry
description: "Use al convertir POIs puntuales en huellas de acera."
version: "1.0.0"
tags: [gis, huellas, footprints, overpass, geometria, web-workers]
---

# Point-to-Footprint Geometry — de puntos a polígonos sobre la calle

## Descripcion

Patron para convertir un dataset de **puntos** (terrazas, locales, kioskos, cualquier POI con direccion + superficie) en **huellas poligonales** dibujadas sobre la acera real. Resuelve el problema clasico de los puntos: un POI de 30 m² tratado como 1 punto produce errores groseros de sol/sombra/ruido (la esquina sur puede tener sol mientras la norte esta en sombra).

Origen: fase 1 de [solmad](https://github.com/Ntizar/solmad) (6.154 huellas del censo de terrazas de Madrid, 98% de cobertura).

## Algoritmo (5 pasos)

1. **Punto oficial -> metros locales.** Proyectar el punto (p.ej. EPSG:25830 -> WGS84 con proj4) y a coordenadas metricas locales (`x = (lng-originLng)*mPerDegLng`, `y = (lat-originLat)*111320`).
2. **Via mas cercana.** Indexar segmentos del viario OSM (`way[highway][name]`, `out body geom`) en un grid espacial de celdas de 100 m. Buscar el segmento mas cercano dentro de un radio de ~60 m.
3. **Orientacion por eje de via.** Promediar la direccion de los segmentos cercanos al punto de cruce usando el truco del **angulo doble** (`sin(2a)`/`cos(2a)`, luego `atan2/2`): evita el wrap 180° y descarta esquinas.
4. **El punto del censo ES la terraza.** El tipo de dato georreferenciado correcto es la **coordenada real del POI** (`coordenada_x_local/y`, no un punto del edificio). Si tiene dato válido (no `0,0`), **NO se desplaza desde el eje de la vía** — se usa directamente como centro de la huella, porque el censo ya la colocó en su acera. Solo los POIs con coordenada faltante (`0,0`) se estiman desde la vía más cercana.
5. **Dimensionado superficie/ancho, con ancho ACOTADO A LA ACERA.** `longitud = superficie / ancho`. En Madrid el ancho de acera típico es **2,0 m** (techo 2,4 m): así la terraza no invade la calzada. Las terrazas grandes reparten la superficie a lo largo de la fachada (`longitud = sup/ancho`, techo 45 m, suelo 2,5 m).

**⚠️ El error clásico (corregido en esta fase):** el enfoque de "offset desde el eje de la vía" (`semiancho_calzada ~4,5 m + retroceso`) es **incorrecto** para POIs con coordenada real. Empuja la terraza a la zona de coches y, en calles anchas, apila las del lado opuesto en el mismo punto. La regla correcta: **con coordenada real, el punto ES la huella** (solo un empuje de ~0,3 m hacia la fachada). Solo los POIs sin coordenada se colocan en el borde de acera (~1,5 m del eje, no 5 m).

Cada huella lleva ademas **muestras interiores** (grid 2x2 = centros de cuadrantes) para motores que evaluan por superficie y no por punto.

## Motor por superficie (v2)

Con huellas, el estado por punto pasa a **% de superficie**: evaluar las 4 muestras por huella en el worker (`isSunlit` por muestra), estado = pct >= 25. `minutesLeft` usa el mismo umbral: el POI "conserva" la condicion mientras >=25% de su huella la cumpla. Anadir `pct?: number` al tipo de estado y mantener el booleano anterior por compatibilidad. (En solmad: `computeForHuellas` / `quickForHuellas` en `shadows.worker.ts`, umbral 25%.)

## Test de un Comlink worker en Node (sin navegador)

Patron verificado para testear la logica de un Web Worker fuera del navegador:

1. Empaquetar el worker con **esbuild** (`bundle: true, format: 'esm', platform: 'browser'`, `absWorkingDir` apuntando a la raiz del proyecto para que resuelva node_modules).
2. **Shim de comlink** con `alias` de esbuild: un modulo propio cuyo `expose(api)` hace `globalThis.__testAPI = api` (ver `templates/comlink-shim.mjs`). En Node no hay MessagePort y `expose` real revienta con `ep.addEventListener is not a function`.
3. Tras importar el bundle, leer `globalThis.__testAPI` y llamar a los metodos directamente (son funciones normales; Comlink solo envuelve el transporte).
4. Test fisico minimo: edificio sintetico (anillo WGS84 + altura), huella al este y al oeste, sol de manana (azimut ~82deg) -> este=100% sol, oeste=0% sombra. Si sale al reves, la matematica de azimut esta invertida.

## Parametros usados en solmad (madrid, probados)

- Radio busqueda via (solo POIs sin coords): 55 m · radio promedio de direccion: 35 m
- Celdas del grid espacial: 100 m
- Ancho de acera: 2,0 m (techo 2,4 m), longitud 2,5-45 m
- Viario completo de Madrid (52131 ways): query Overpass `way[highway][name](40.312,-3.842,40.568,-3.508);out body geom;` = **41 MB / ~3 min**
- Salida: `public/<datos>-huellas.json`, ~1,5 MB para 6276 huellas (ring 4 esquinas + 4 samples)
- Sanity: contar huellas con diagonal >35 m (deben ser pocas) y **pares con centroides a <3 m** (son los que se apilan — con coordenada real deben ser pocos; los legítimos son mesas contiguas del mismo bar).

## Pitfalls

- **Overpass grande en background con `curl`**: capturar `HTTP %{http_code}`; un timeout de conexion devuelve exito aparente con codigo 000 y 0 bytes. Verificar codigo y tamano antes de parsear. Si un mirror falla, probar overpass.kumi.systems (el principal puede colgar 21 s y morir en silencio).
- **Proyeccion local para geometria**: 111320 m/deg lat y `cos(lat)` para longitud dan error <0,1% a escala de ciudad. No usar proj4 para el paso metrico local, solo para la reproyeccion de origen.
- **Coordenadas (0,0) en el censo**: muchas filas del dataset municipal vienen con `coordenada_x_local/y = (0,0)` (dato faltante, no un punto real). Contarlas por separado ANTES de generar: si son pocas (~1%), se estiman desde la vía más cercana; si son muchas, el dataset no tiene posición fiable y hay que buscar otra fuente. Agruparlas por celda de 15 m revela la basura: 74 filas (0,0) caen en la MISMA celda.
- **Coordenada (0,0) es dato faltante, no coordenada**: `x===0 && y===0` es inválido — no validar contra rangos "razonables" como `abs(y)>4e6` (Madrid tiene y~4.47e6, TODAS las válidas las descartarías). Solo filtrar el exacto (0,0) o No-Finito.
- **Solape = NO apilar**. Distribuir los POIs sin coordenada a lo largo del eje de la calle con una **variación determinista** basada en el id (`((id % 40) - 20) * longitud*1.1`) en vez de apilarlos todos en el mismo offset. Los "solapes" residuales con datos reales casi nunca son error: son mesas contiguas del mismo bar (en Madrid: 22 solapes reales de 6276 = 0.35%).
- **Ancho imposible**: si `superficie/ancho_acera` da longitudes >45 m (POIs enormes), recortar la longitud (techo 45 m) en vez de dibujar un tren infinito. Nunca subir el ancho por encima del ancho de acera real (2,4 m) o invadirá la calzada.
- **Zoom de render**: los poligonos de 4-10 m solo se leen desde zoom >=15-16. Por encima de ~500 huellas visibles, recortar por bbox del viewport y renderizar en rAF con `moveend/zoomend`.
- **Campos del censo**: tras filtrar "Abierto", campos como `ubicacion`/`periodo` pueden ser null en TODAS las filas — no apoyar la geometria en ellos; `Superficie_ES` y `ref_catastral` (92%) si existen.

## Referencias

- `references/receta-solmad-huellas.md` — implementación concreta en solmad: archivos, firmas, decisiones y verificación (fase 1).
- `references/receta-solmad-fase2.md` — corrección de fase 2: el punto del censo ES la terraza, fallo del ArcGIS paginado, sombras limpias por distancia, cache solar por ángulo.
- `templates/comlink-shim.mjs` — shim para testear workers Comlink en Node.
