---
name: solar-shadows-web-workers
description: Patrón de cálculo de sombras solares con Web Workers + Comlink para no bloquear la UI
version: "1.0.0"
created: 2026-06-01
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
- **SunCalc azimut** viene desde sur (0=S), convertir a 0=N CW: `(azFromSouth + 180 + 360) % 360`
- **Optimización**: usar `visitToken` en vez de `Set` para marcar segmentos visitados (evita alloc)

## Referencias

- SolMAD: `src/workers/shadows.worker.ts` (~14KB)
- SolMAD: `src/lib/sun.ts` — utilidad de conversión de azimut
- Comlink: https://github.com/GoogleChromeLabs/comlink
