# Receta solmad — fase 2 (corrección de terrazas + sombras limpias, sesión 2026-09-03)

Corrige la fase 1 (receta-solmad-huellas.md). Tres lecciones centrales: el
punto del censo ES la terraza, el origen de edificios por ArcGIS paginado puede
romper la app, y las sombras de edificios hay que limitarlas por distancia.

## 1. CORRECCIÓN CLAVE: el punto del censo ES la terraza (no se desplaza)

El algoritmo de fase 1 (offset `semiancho_calzada 4,5 m + retroceso 0,5 m`
desde el **eje de la vía**) es **incorrecto**. Desplaza la terraza a la zona de
coches y, en calles anchas, apila las del lado opuesto en un mismo punto.

Regla correcta en `prepare-huellas.mjs`:
- Si `coordenada_x_local/y` es válida (NO `(0,0)`): **el punto ES la terraza**.
  Usarlo como centro, solo empuje de ~0,3 m hacia la fachada.
- Solo los POIs con coords `(0,0)` (dato faltante) se estiman desde la vía
  cercana, y se colocan a ~1,5 m del eje (no 5 m).
- Ancho ACOTADO A LA ACERA: 2,0 m (techo 2,4 m). `longitud = superficie/ancho`,
  techo 45 m, suelo 2,5 m. Nunca subir el ancho >2,4 m.
- POIs sin coords: distribuirlos a lo largo del eje con variación determinista
  por id (`((id % 40) - 20) * longitud * 1.1`) — no apilarlos en el mismo offset.

Resultado real: 6276 huellas, **solo 22 solapes reales** (0.35%), y esos son
mesas contiguas legítimas del mismo bar. Sanity: pares con centroides <3 m —
deben ser pocos; los que se apilan sin GPS son el error.

### La trampa de validar coords (0,0)
No filtrar por rango tipo `abs(y) > 4e6` → descarta TODAS (Madrid y~4.47e6).
Solo filtrar `x===0 && y===0` exacto (o No-Finito). Contar por celda de 15 m:
74 filas (0,0) caen en la misma celda = señal de dato faltante, no de solape.

## 2. ORIGEN DE EDIFICIOS: ArcGIS paginado ROBE (no usar en runtime)

`sigma.madrid.es .../EDIFICIOS_ALTURAS/MapServer/0/query` devuelve edificios +
altura oficial, pero **maxRecord=2000 y `exceededTransferLimit:true`** por tile
de 1,2 km. Paginarlo en el cliente (resultOffset/resultRecordCount) puede
quedarse en bucle → el worker satura → Safari "ha generado problemas
repetidamente" y la app se rompe al mover la hora.

Lección: para datos tan masivos (~492k edificios), NO paginar un ArcGIS en el
runtime. Usar Overpass (estable, aunque lento) o un dataset descargado y
pre-procesado. Dato útil: el bbox del ArcGIS se manda en **WGS84** directamente
(`geometry=w,s,e,n`, `inSR=4326`, `outSR=4326`); una conversión UTM manual está
desfasada ~1,5 km y rompe el matching.

## 3. SOMBRAS LIMPIAS (el "maraña" a sol bajo)

Síntoma: a las 20:28 (sol bajísimo) el mapa se llena de sombras negras
superpuestas. Causa: el render dibujaba TODAS las sombras visibles (hasta 1400)
con borde oscuro y opacidad alta; a sol bajo cada sombra se alarga muchísimo.

Fix en `MapView.tsx` (efecto de sombras):
- **Limitar por distancia al centro**: solo edificios a <260-420 m del centro.
  Filtrar + ordenar por distancia, slice a 220 (móvil) / 900 (desktop).
- **Sin borde negro** (`stroke:false`) — el borde crea la textura de rejilla.
- **Opacidad dependiente del sol**: `duskFactor = clamp((alt-2)/20, 0, 1)`
  (0 al atardecer, 1 mediodía); `opacity = 0.06 + 0.16*duskFactor*(1-d/maxDist)`.
- Helper `centroidDist(ring, center)}` en metros planos

## 4. CACHE SOLAR por ángulo cuantizado y por slot (rendimiento)

Los días son casi iguales (sol se mueve ~1°/día) → NO recalcular raycasts.
- En el worker: `sunlitCached(x,y,az,al)` memoiza `isSunlit` con az/al
  cuantizados a 0,5°. Aplica a quick/compute/ribbon.
- En la app: cache persistente del quick en localStorage por
  `q|terrazaId|slot30min` (independiente del día) → 2ª vez que se mira una hora,
  respuesta instantánea. Solo calcula los que faltan.

## Verificación
`npx tsc -p tsconfig.json --noEmit` EXIT 0 · `node scripts/test-huellas.mjs`
TEST OK · `npm run build` OK · CI Pages success. JSON 1,5 MB válido.
