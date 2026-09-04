---
name: madrid-solar-shadow-geodata
description: Usa al construir webs de sombras solares de Madrid.
version: "1.0.0"
author: "Hermes curator"
license: "CC BY 4.0"
tags: [madrid, sombras, solmad, geodata, leaflet, arcgis, open-data, rendimiento]
related_skills: [ign-wmts-tiles, shademap-competidor-madrid, solar-shadows-web-workers]
---

# Webs de sombras solares de Madrid con datos abiertos

## When to Use

- Al construir u optimizar una web que calcula sol/sombra por terraza o punto en Madrid (tipo SolMAD).
- Al cruzar datos de terrazas/edificios del Ayto. de Madrid con OSM/IGN para un mapa Leaflet/MapLibre.
- Al optimizar el rendimiento de un raycast de sombras en Web Worker (cache por slot, "los días son iguales").

Clase de trabajo: construir/optimizar mapas que calculan sol/sombra por terraza o punto en Madrid, usando datos abiertos del Ayto. de Madrid + OSM + IGN, render Leaflet/MapLibre con Web Worker para el raycast. Proyecto referencia: SolMAD (`Ntizar/solmad`).

## Fuentes de datos oficiales (verificadas)

| Fuente | Qué da | Acceso |
|---|---|---|
| **Censo de terrazas del Ayto.** | 6.2k terrazas abiertas, coords EPSG:25830, `Superficie_ES/RA`, `mesas_es`, `superficie`, `id_terraza` | `datos.madrid.es` (dataset terrazas) |
| **Alturas de edificios** | altura por polígono + geometría (rings WGS84), CC BY 4.0 | `sigma.madrid.es/hosted/rest/services/CARTOGRAFIA/EDIFICIOS_ALTURAS/MapServer/0/query` |
| **Modelo 3D LOD2** | edificios extruidos 1:1000, SLPK/OBJ por distritos | Geoportal Madrid (dataset "Modelo tridimensional") |
| **IGN WMTS** | mapa base gratuito CC BY 4.0 | `ign.es/wmts/ign-base` (ver skill `ign-wmts-tiles`) |
| **OSM Overpass** | edificios/viario en vivo | `overpass-api.de` |

## Pitfall #1 — El punto del censo NO es la acera

`coordenada_x_local/y` de una terraza del Ayto. (EPSG:25830) está en la **fachada del edificio**, NO sobre la acera. Usarlo como centro de la huella deja las terrazas **DENTRO de los edificios** (el usuario lo detecta al instante: "La has liado con las terrazas").

- Para poner la huella en la acera: proyectar el rectángulo perpendicular a la calle, O ponerla a ~1.5 m del eje de la vía (offset de acera). **NO a 5 m del eje** (cae en la zona de coches).
- El crudo trae `id_terraza` pero `terrazas.min.json` expone `id`. Revisar el campo real antes de cruzar con huellas.

## Pitfall #2 — Bucle de paginación del ArcGIS

El servicio de alturas pagina a **2000** (`exceededTransferLimit`). Un tile de ~1.3 km tiene >2000 edificios → 2+ páginas. Si `fetchTile` no corta el loop (con tope de páginas + timeout + abort), satura el worker y **Safari se cuelga** ("ha generado problemas repetidamente"). Para fetch en vivo es más estable **Overpass**; usar el ArcGIS solo paginando con tope/retry/timeout, o precomputar en build.

- **bbox del ArcGIS en WGS84 directo**: `inSR=4326&outSR=4326`, geometry `"w,s,e,n"`. NO convertir a EPSG:25830 a mano → desfase ~1.5 km y el matching nunca acierta.
- **User-Agent custom obligatorio** en la petición (403 sin él).
- Madrid capital tiene **~492k edificios**; descargar todo en runtime (246 requests) es inviable → precomputar en build o por tiles de zona, simplificando geometría a ~8 vértices (basta para la sombra).

## Rendimiento — cache por slot horario ("los días son iguales")

El sol se mueve ~1°/día, así que el mismo slot de días cercanos da el mismo sol/sombra. Cachear el estado por `(terrazaId, ymd, slot de 30 min)`:

- Computar **solo el slot pedido** (4 raycasts la 1ª vez), guardar en `Map<terrazaId, {ymd, states: Uint8Array[48]}>`. Al mover el slider → **lookup O(1)**.
- **Medido en SolMAD: 1ª llamada 1.13ms → 2ª (mismo slot) 0.01ms (100x)**.
- **Sentinel "no computado" = 255, NUNCA 3** (3 es un estado válido: pendiente). Si usas 3 como K crees que sigue pendiente y recalculas forever.
- **Invalidar cache en `setBuildings`** (al cambiar edificios los raycasts quedan obsoletos, sobre todo los marcados pendiente).
- Cache por ángulo cuantizado a 0.5° solo "pega" si se repite exacta la combinación az/al — al mover el slider casi nunca pasa. La cache **por slot** es la que hace instantáneo el drag.

## Workflow — verificación visual ANTES de desplegar

Cambiar geometría de terrazas/sombras a ciegas y desplegar solo con `tsc`+build **NO es suficiente**: rompe la UX y el usuario lo ve al vuelo.

1. Validar con **verificación visual real** (captura de navegador / screenshot) y/o **script de medición de solapes sobre el JSON real** ANTES de commitear.
2. Guarda el SHA del estado estable. Para revertir solo lo que se lió conservando lo bueno: `git checkout <sha> -- <archivos>`. SolMAD estable = commit `07e6ad6`.
3. Los "solapes" de terrazas casi nunca son un error: son **clusters** (`leaflet.markercluster`, círculos con nº) que agrupan terrazas del mismo bloque; se separan al hacer zoom. Con datos reales, la mayoría de pares <3 m son mesas contiguas legítimas — no moverlas.
4. Atribución básica: `Hecho con ♥ por David Antizar · datos OSM · Madrid Abierto`; licencias CC BY 4.0 → atribución obligatoria.

## Estados del estado solar (convención)

`0=sombra · 1=sol · 2=noche · 3=pendiente (sin edificios) · 255=sin dato`. Mantener esta convención en todo el pipeline (motor, cache, UI) para no mezclar "pendiente" con "sin dato".

## Referencias

- `references/solmad-detalle-sesion.md` — detalle de la sesión SolMAD: qué se rompió y por qué, red de datos de terrazas (74 con (0,0), rangos válidos), medición de la cache por slot, SHA estable `07e6ad6`.
