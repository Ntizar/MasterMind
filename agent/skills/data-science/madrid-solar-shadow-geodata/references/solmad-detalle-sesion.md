# Referencia — SolMAD: trampas y mediciones verificadas

Detalle de la sesión de optimización de SolMAD (`github.com/Ntizar/solmad`). Notes que refuerzan el SKILL.md sin inflarlo.

## Estado estable y revert

- El commit `07e6ad6` es el estado ESTABLE que funciona (Overpass para edificios + huellas originales en acera + render de sombras original + cache de slots en el worker).
- Para revertir solo lo que se lió conservando lo bueno:
  `git checkout 07e6ad6 -- scripts/prepare-huellas.mjs public/terrazas-huellas.json src/components/MapView.tsx`
- El worker (`src/workers/shadows.worker.ts`) con `sunlitCached` + cache de slots vivía en `07e6ad6` y se conservó; NO se revierte.

## Qué se rompió y por qué

1. **Terrazas dentro de edificios.** Se usó `coordenada_x_local/y` del censo como centro de la huella. El punto está en la fachada → las huellas quedaron dentro del polígono del edificio. El usuario: "La has liado con las terrazas".
2. **Crash al mover el slider en móvil.** El origen de edificios se cambió a ArcGIS del Ayto. Paginaba a 2000 por tile; un tile de 1.3 km tiene >2000 edificios → el `fetchTile` podía entrar en bucle; al mover la hora el worker se saturaba y Safari mostraba "ha generado problemas repetidamente".

## Red de datos de terrazas (verificada al inspeccionar el dataset)

- `data/terrazas.json` (crudo Ayto.): 6488 registros, 6307 abiertos (según `desc_situacion_local == 'Abierto'` y `desc_situacion_terraza` vacío o `'Abierta'`).
- **74 terrazas tienen `coordenada_x_local=0, y=0`** (sin dato) → se agrupan en la misma celda y parecen "solapadas". No es un solape real; hay que estimarlas desde la vía cercana.
- Rangos válidos EPSG:25830 de Madrid: X 432k-453k, Y 4465k-4487k. No filtrar por `abs(y)>4_000_000` (todas lo superan).
- Lo que el vision/mapa muestra como "círculos con número" son **clusters** de `leaflet.markercluster`, no terrazas mal puestas.

## Datos que SÍ ayudan a colocar bien la terraza

- `Superficie_ES` / `Superficie_RA` (m²) y `mesas_es`/`mesas_ra` del censo.
- `viaDir`: dirección media de la acera cerca de un punto, promediando los ángulos de segmentos con `2*theta` (para evitar el wrap de ±180°).
- Solape legítimo: **centroides a <3 m** = mesas contiguas. Moverlo solo si centroides >3 m y polígonos superpuestos (malo). Con datos reales quedan ~22 de 6276 (0.35%).

## Medición de rendimiento de la cache de slots

En `scripts/test-huellas.mjs` se añadió una medición con `performance.now()`:

```js
const t0 = performance.now();
const quick = api.quickForHuellas(terrazas, when);
const t1 = performance.now();
api.quickForHuellas(terrazas, when);
const t2 = performance.now();
console.log(`1ª ${t1-t0}ms | 2ª ${t2-t1}ms`);
```

Resultado real: **1ª llamada 1.13ms → 2ª (mismo slot) 0.01ms (~100x)**.

## Convención de estados

`0=sombra · 1=sol · 2=noche · 3=pendiente (sin edificios) · 255=sin dato`.
En la cache de slots el sentinel de "no computado" es **255**; `3` es un resultado VÁLIDO (pendiente). No usar `3` como centinela o el slot "pendiente" se recomputa siempre.
