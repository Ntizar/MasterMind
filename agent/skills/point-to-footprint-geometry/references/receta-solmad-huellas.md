# Receta solmad — generación de huellas de terrazas (fase 1, sesión 2026-09-03)

Implementación concreta del patrón point-to-footprint en el repo
[Ntizar/solmad](https://github.com/Ntizar/solmad) (clon local: `~/Projects/solmad`).

## Archivos

| Archivo | Rol |
|---|---|
| `scripts/prepare-huellas.mjs` | Generador: lee `data/terrazas.json` (crudo Ayuntamiento, EPSG:25830) + `data/vias-madrid.json` (Overpass) → `public/terrazas-huellas.json` |
| `scripts/test-huellas.mjs` | Test del motor: esbuild + shim comlink, edificio sintético |
| `scripts/comlink-shim.mjs` | Shim de comlink para el test (`expose` captura en `globalThis.__solmadTestAPI`) |
| `src/lib/huellas.ts` | Loader cliente: fetch `/terrazas-huellas.json`, tolerante a fallo (devuelve null → motor v1) |
| `src/lib/types.ts` | `Huella { ring, samples, orientacion? }` + `SunState.sunNowPct?` |
| `src/workers/shadows.worker.ts` | `setHuellas`, `quickForHuellas` (4 muestras, umbral 25%), `computeForHuellas` (con sunNowPct + minutesLeft por umbral) |
| `src/store/useAppStore.ts` | `huellas` + `setHuellas`; `introDone` acepta `?nointro` por URL |
| `src/App.tsx` | Carga terrazas+huellas en paralelo; registra huellas en worker; quick usa `quickForHuellas` con try/catch y fallback a `facadeQuickFor` |
| `src/components/MapView.tsx` | Capa `huellaLayerRef` (LayerGroup): polígonos coloreados por estado (naranja sol / gris sombra / azul noche / gris claro pendiente), zoom>=15, cap 500, bbox pad 0.15, rAF en moveend/zoomend, click → setSelectedId |
| `package.json` | `prepare:huellas` añadido a `dev` y `build` |

## Formato de salida (`public/terrazas-huellas.json`)

```json
{ "8": {
  "ring": [[lng,lat],[lng,lat],[lng,lat],[lng,lat]],
  "samples": [[lng,lat],[lng,lat],[lng,lat],[lng,lat]],
  "orientacion": 0 } }
```
Clave = `id_terraza` (string). Ring en orden: (-1,-1),(-1,1),(1,1),(1,-1) sobre
(eje vía × normal). Samples = centros de los 4 cuadrantes.

## Decisiones y porqués

- **Viario completo de una vez** (41 MB) y no por tile: el generador corre en
  build, no en el cliente. Query: `way[highway][name](40.312,-3.842,40.568,-3.508);out body geom;`
  → 52.131 ways. Descarga con `curl --data-urlencode` al mirror `overpass.kumi.systems`
  (el principal devolvió HTTP 000 tras 21 s; kumi tardó ~3 min).
- **Lado de acera por signo**, no por paridad de portal: el censo ya coloca el
  punto en su acera; paridad + cruce perpendicular daba errores en glorietas.
- **Grid 2×2 de muestras**, no centroide único: permite % de superficie soleada
  y casar "medio soleada" en vez del SÍ/NO grosero del punto.
- **Umbral 25%** para `sunNow`: con 4 muestras, 1 muestra soleada = 25% = sol.
  Es el compromiso entre "toda la mesa al sol" y "algún rincón al sol".
- **Zoom mínimo 15** para la capa de huellas (16 las ocultaba en vista de barrio;
  a 15 se ve el efecto 'terrazas en la acera' que pidió David).
- **Filtro idéntico a prepare-data.mjs** (situacion_local=Abierto y terraza
  Abierta/null) para que huellas y marcadores hablen de los mismos ids.

## Verificación realizada

- `node --check scripts/prepare-huellas.mjs` OK; ejecución: `6154 huellas, 122
  sin via cercana`; sanity diagonal: 30/6154 > 35 m.
- `npx tsc -b` EXIT 0 tras todos los cambios.
- Test físico (`node scripts/test-huellas.mjs`): edificio 20 m alto, sol
  azimut 82°/alt 28.5° → huella este `[1, 100%, 516 min]`, oeste `[0, 0%, 0 min]`.
  **TEST OK** — la física (sombra al oeste por la mañana) sale correcta.
- Smoke test en `http://localhost:5199/?nointro` (preview Hermes): app carga,
  terrazas y TimeWheel visibles. Verificación visual de rectángulos pendiente
  de confirmar a zoom alto (se cortó por límite de sesión); el overlay SVG no
  apareció en los intentos por DOM (headless se quedaba en intro sin `?nointro`).

## Siguientes fases acordadas con David

- Fase 2: DetailPanel mostrando `sunNowPct` ("% de la terraza al sol"), ribbon
  por huella.
- Fase 3: precalculo nocturno de mapa de sombras por hora (GitHub Action),
  vista 3D Three.js con arco solar sobre la huella del bar seleccionado,
  filtros toldos/sombrillas/estufas (campos ya presentes en el censo: 242 con
  toldo, `anclaje` 778).
- Mejora geométrica: semiancho de calzada real (tags `lanes`, `sidewalk`) y
  Catastro (Consulta_CPMRC proyecta el portal a la fachada; 92% de terrazas
  tienen `ref_catastral`).
