---
name: solar-shadows-web-workers
description: Patrón de cálculo de sombras solares con Web Workers + Comlink para no bloquear la UI
version: "1.1.0"
created: 2026-06-01
updated: 2026-09-16
source: Ntizar/solmad
status: active
tags: [data-science, solar, sombras, web-workers, solmad]
---

# Patrón: Cálculo de Sombras Solares con Web Workers

**Proyecto origen:** SolMAD (Ntizar/solmad)  
**Clusters:** web-workers, calculo-solar, rendimiento-ui  
**Decay:** lento  

## Descripción

Patrón para realizar cálculos intensivos de sombras solares sin bloquear el hilo principal de la UI, usando Web Workers + Comlink para una API type-safe.

## Cuándo usarlo

- Tienes cálculos que duran >50ms y pueden bloquear la UI
- Necesitas hacer raycasting contra un grid de edificios
- El usuario necesita feedback visual en tiempo real mientras se calcula

## Pasos

### 1. Instalar dependencias

```bash
npm install comlink suncalc
```

### 2. Crear el worker (`src/workers/shadows.worker.ts`)

```typescript
import * as Comlink from 'comlink';
import SunCalc from 'suncalc';

class SegIndex {
  cell = 60; // metros por celda
  grid = new Map<string, Seg[]>();
  
  build(buildings, originLng, originLat) {
    // Indexar segmentos de fachada en grid espacial
  }
  
  forEachAlongRay(ox, oy, dx, dy, len, fn) {
    // Raycasting optimizado con grid spatial
    // Usa visitToken para evitar Set (más rápido)
  }
}
```

### 3. Crear el cliente (`src/workers/shadowsClient.ts`)

```typescript
import * as Comlink from 'comlink';

const workerUrl = new URL('./shadows.worker.ts', import.meta.url);
const worker = new Worker(workerUrl, { type: 'module' });
export const workerApi = Comlink.wrap<ShadowWorker>(worker);
Comlink.release(workerApi);
```

### 4. Usar en el componente

```typescript
import { workerApi } from './workers/shadowsClient';
await workerApi.build(buildings, centerLng, centerLat);
const result = await workerApi.checkShadow(terraceLng, terraceLat, date);
```

## Pitfalls

- **Comlink serializa funciones** — no puedes pasar callbacks arbitrarios, solo funciones serializables
- **No compartas estado mutable** entre llamadas al worker
- **Limpia el worker** con `Comlink.release()` cuando el componente se desmonte
- **SunCalc azimut según versión (CRÍTICO 2026-09)**: en **v1** (≤1.9, la que usa SolMAD: `"suncalc": "^1.9.0"`) viene desde sur (0=S) → convertir con `(azFromSouth + 180 + 360) % 360`; en **v2** ya viene en grados clockwise desde el NORTE (0=N) → usar directo, NO aplicar la conversión o se gira 180° (sombras calculating en dirección opuesta). Ver `## SunCalc v2` abajo.
- **Optimización**: usar `visitToken` en vez de `Set` para marcar segmentos visitados (evita alloc)

## SunCalc v2 (2.0.2, 2026-09-02) — qué cambia al migrar desde v1

Aprendido del repo [mourner/suncalc](https://github.com/mourner/suncalc) (3.471⭐, BSD-2, activo). v2 es una reescritura de precisión: posición solar ~0.43°→~0.08°, salidas/puestas ~75s→~15s, posición lunar ~1.2°→~0.09° (validado contra JPL Horizons y USNO, fórmulas de Jean Meeus).

**Breaking changes (migración SolMAD/shademap u otros proyectos con `suncalc@1.x`):**

1. **ESM-first**: `import * as SunCalc from 'suncalc'` (ya no default `import SunCalc`). Sigue hay build UMD/CJS para `<script>` (global `SunCalc`) y `require()` — jsDelivr: `https://cdn.jsdelivr.net/npm/suncalc/+esm` (módulo) o `/npm/suncalc` (bundle global).
2. **Todos los ángulos en GRADOS** (entrada y salida: altitude, azimuth, parallactic…) — v1 usaba radianes. Un upgrade sin tocar el código = azimuts interpretados 57× fuera de rango, silenciosamente.
3. **Azimut desde el NORTE, CW** (0=N, 90=E, 180=S, 270=W) — v1 era desde el SUR. Eliminar toda conversión propia tipo `(az+180)%360` (ver pitfall arriba).
4. **Altitud aparente** (corregida por refracción atmosférica) — cerca del horizonte coincide con lo observado; con v1 el sol "sale" medido ~3-4 min antes/despes de lo visible.
5. **Fechas = instantes UTC absolutos** sin conversión de zona; `getTimes` resuelve el día solar de la fecha pase la hora que pase (en v1 había que pasar el mediodía para evitar off-by-one). Para MOSTRAR en zona: `toLocaleString`/`Intl` con `timeZone` explícito (el DST se aplica solo).
6. **Eventos inexistentes = `null`** (no `Invalid Date`) + flags `alwaysUp`/`alwaysDown` en latitudes polares. En zonas templadas como Madrid no dispara, pero el código que hace `isNaN(date)` debe pasar a `=== null`.
7. `getMoonTimes` escanea el día UTC; eliminado el argumento `inUTC` — para ventana civil local, pasar fecha a medianoche local. `getMoonIllumination` añade flag `waxing`.

**Para el raytraceo de sombras (uso en este patrón):** `getPosition(date, lat, lng)` → `{altitude, azimuth}` en grados; el check "hay sol" sigue siendo `altitude > obstrucción`; el vector de dirección del rayo se construye YA desde norte (sin el +180). Precisión de ~15s hace innecesario el truco v1 de muestrear a mediodía.

## Referencias

- SunCalc v2: https://github.com/mourner/suncalc (3.471⭐, BSD-2, v2.0.2 — notas de ruptura en la release v2.0.0)
- SolMAD: `src/workers/shadows.worker.ts` (~14KB)
- SolMAD: `src/lib/sun.ts` — utilidad de conversión de azimut
- Comlink: https://github.com/GoogleChromeLabs/comlink
