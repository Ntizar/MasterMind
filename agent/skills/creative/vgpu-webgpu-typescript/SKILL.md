---
name: vgpu-webgpu-typescript
description: "Use cuando crear efectos WebGPU en TypeScript con WGSL."
version: "1.0.0"
author: "Mastermind (stars-explorer)"
license: "MIT"
tags: [webgpu, typescript, wgsl, shaders, gpu, browser, headless, testing]
---

# vgpu — Librería WebGPU de TypeScript (Vercel Labs)

## Cuándo usar

- Efectos fullscreen, visualizaciones o pipelines compute con WebGPU desde TypeScript en una web estática.
- Tests/CI de shaders en máquina sin GPU (adapter mock determinista).
- Alternativa ligera (25 KB) a Three.js cuando no necesitas scene graph ni loaders.

## Qué es

`vgpu` (github.com/vercel-labs/vgpu, ~1.500⭐, MIT, muy activa) es una librería TypeScript para WebGPU con un enfoque distinto al de Three.js: **sin grafo de escena, frames explícitos, shaders como módulos tipados, y el mismo código corriendo en navegador, Node headless y tests**. Relevante para las herramientas HTML de David (efectos GPU en navegador, visualizaciones, CI sin GPU).

Patrones clave:

1. **Imports WGSL tipados** — los `.wgsl` se importan/exportan como módulos TypeScript; la reflexión mantiene nombres, tipos y layouts de bindings correctos sin declaraciones escritas a mano ni codegen.
2. **Un único contexto `Gpu`** — `init()` devuelve el handle; todo entry point (`draw`, `effect`, `frame`, `surface`, `target`, `compute`, `bundle`, `uniforms`) lo recibe como primer argumento. Sin estado global oculto.
3. **Multi-runtime con la misma API** — navegador (`vgpu`), Node headless respaldado por Dawn (`vgpu/node`), y mock determinista de software (`vgpu/mock`) para tests y CI sin GPU.
4. **Frames explícitos** — `frame(gpu, (f) => f.pass(target, effect))`: passes, clears y draws son llamadas explícitas.
5. **Presupuesto de bundle** — un efecto fullscreen completo pesa 25 KB gzip, con declaraciones no usadas podadas y presupuesto enforced en CI.
6. **Agent-ready** — docs, galería de ejemplos y validación de shaders desde CLI; publica `agents.md`, `llms.txt` y servidor MCP.

## Instalación

```bash
pnpm add vgpu
pnpm add -D @webgpu/types
```

## Uso básico — efecto fullscreen en navegador

```ts
import { clock, init, effect, frameLoop, surface } from "vgpu";
import waveShader from "./wave.wgsl";

const gpu = await init();                          // adapter + device
const canvasSurface = surface(gpu, canvas, { dpr: [1, 2] });
const wave = effect(gpu, waveShader, { set: { speed: 2 } });

const time = clock(gpu);
frameLoop(gpu, (frame) => {
  wave.set({ time: time.time });                   // uniforms por nombre WGSL, escritura inmediata
  frame.pass(canvasSurface, wave);
});
```

## Uso headless en Node (render + lectura de píxeles)

```ts
import { draw, frame, init, target } from "vgpu/node";
import triangleShader from "./triangle.wgsl";

const gpu = await init();
const colorTarget = target(gpu, { size: [256, 256], format: "rgba8unorm" });
const triangle = draw(gpu, { shader: triangleShader });

frame(gpu, (f) => f.pass(colorTarget, triangle));
const pixels = await colorTarget.read();
gpu.dispose();
```

En tests, sustituir `vgpu/node` por `vgpu/mock`: mismo código, adapter de software determinista, no necesita GPU real. Ideal para CI.

## Módulos WGSL reutilizables

`@vgpu/wgsl-std` trae utilidades (hash, noise, color, sampling, math) como exports con nombre; cualquier `.wgsl` propio puede exportar `fn`/`struct`/`const`:

```wgsl
// grain.wgsl
import { hash2 } from "@vgpu/wgsl-std/hash";

export fn grain(uv: vec2f, time: f32) -> f32 {
  return hash2(uv * time).x;
}
```

Los imports se resuelven en build por reflexión WGSL tipada — sin paso de codegen.

## CLI y recursos para agentes

```bash
npx vgpu docs cat getting-started.md     # docs offline dentro del paquete
npx vgpu docs find effect
npx vgpu examples search "raymarching"   # galería buscable
npx vgpu examples pull <id> --out ./example
npx vgpu check                            # valida shaders
npx vgpu mcp                              # MCP stdio local
```

- Docs y guía de rendimiento: https://vgpu.sh (performance playbook: bundles, target pre-warm, `set()` in-place, instancing, ping-pong, MSAA/depth).
- `https://vgpu.sh/llms.txt` y `agents.md` para consumo LLM; endpoint MCP público read-only en `https://vgpu.sh/api/mcp`.

## Paquetes del monorepo

| Paquete | Qué es |
| --- | --- |
| `vgpu` | API pública: `init`, `draw`, `compute`, `effect`, `frame`, `bundle`, `target`, `uniforms` + subpaths `scene` y `core` |
| `@vgpu/cli` | Binario `vgpu`: docs, `check`, `doctor`, setup Dawn/software |
| `@vgpu/core` | Wrappers WebGPU de bajo nivel (Device, Buffer, Texture, bind groups) |
| `@vgpu/wgsl` | Convierte `.wgsl` en módulos JS y resuelve imports WGSL↔WGSL |
| `@vgpu/wgsl-std` | Módulos estándar WGSL (math, color, sampling, noise, hash) |
| `@vgpu/adapter-node` | Adapter Dawn para `vgpu/node` |
| `@vgpu/adapter-mock` | Adapter mock determinista para `vgpu/mock` |
| `@vgpu/render` | Helpers edit/inspect/utils/perf |

## Cuándo usar vgpu vs alternativas

- **vgpu**: efectos/visualizaciones GPU con lógica propia, tests de shaders en CI sin GPU, pipelines compute, control fino sin peso de scene graph.
- **Three.js** (`threejs-*`, `webgl-scene-wow`): escenas 3D con cámara/luces/modelos y ecosistema de loaders — allí Three sigue ganando.
- **WebGPU ONNX** (`webgpu-onnx-detection`): inferencia ML — propósito distinto.

## Caso de estudio — Hero "prism" de Vercel (refracción de luz en malla)

Desmonta cómo construir un hero GPU "smoke & mirrors" sin simular la física real. Fuente: [Codrops, 2026-09-03](https://tympanus.net/codrops/2026/09/03/from-rays-to-meshes-building-vercels-prism-with-vgpu/). Regla general: **no hace falta simular la realidad perfectamente, solo que el resultado sea convincente y funcione fluido.**

### El paso clave: de rayos a malla (de-light → de-mesh)

1. El enfoque naíf es lanzar rayos por píxel y acumular (16 samples + jitter temporal). Caro y borroso → **descartar**.
2. La alternativa ganadora: **dibujar la luz como un mesh**. Se calcula cómo se refracta cada longitud de onda al entrar/salir del prisma; cada path es una línea; se conectan los paths vecinos formando caras triangulares → un beam sólido, más suave y **mucho más barato** (deja de depender de la resolución de píxeles).
3. Así se evita el raymarching caro: la geometría se construye en CPU/GPU una vez y el shader solo sombrea la superficie.

### Composición típica del efecto

- **Glass shader con cubemap**: env-map de 6 direcciones para falsificar reflejos del entorno (adaptado del hero de eve.dev). Habilita fake reflections baratas.
- **Bloom + partículas flotantes** para el dark-mode.
- **Light-mode**: como añadir luz a fondo blanco no tiene sentido (todo se lava), se **oscurece el fondo** para dejar sitio a la "luz".

### Técnicas de cabeceo de coste (light-mode / detalle)

- **Sombra de un objeto estático** → no se calcula en tiempo real: se **pega como textura** sobre la pared (el prisma no se mueve).
- **Normal map de ruido** para los "bumps" de la pared: se **renderiza una vez a imagen estática** en startup — el cálculo de noise caro solo ocurre una vez.
- **Composición de capas**: sombra texturizada + normal map estático + imagen AI de fondo, cada una con controles para afinar.

### Editor de pipeline visual (debug)

- Se construyó un **visualizador del grafo de nodos** del shader (mezcla de imágenes/matemáticas). Útil para entender y depurar composiciones complejas; exposible vía `?debug`.

### Calidad adaptativa (adaptive quality)

- Se crean **versiones ligeras** de cada shader (menos samples, menos detalle) manteniendo el resultado visualmente similar.
- Regla: **empezar en alta calidad y bajar cuando sea necesario** usando 3 señales de dispositivo (capacidad/carga). "The rule is simple: start at high quality, then switch to low quality when necessary."

## Pitfalls

- **`.wgsl` se importa como módulo en Vite, NO en Node ESM**: `import shader from './x.wgsl'` usa el plugin `wgslVitePlugin` de `@vgpu/wgsl/loader-vite`. En Node (para tests) NO existe loader-node ESM → pasar el shader como **string** (leer el archivo con `readFileSync`) o no se importa.
- **VGpu `init()` sin GPU**: en tests usar `vgpu/node` (Dawn) y pasar shaders como strings; compila el draw, renderiza a un `target` y lee píxeles con `target.read()`.
- **Las matrices de la cámara de `vgpu/scene` ya vienen combinadas**: `perspectiveCamera({...}).viewProjection` es proj×view column-major. En WGSL usa `mat4x4f viewProj` y multiplica `viewProj * world`. NO pongas `proj` y `view` separadas (duplicarías la vista).
- **Los uniforms se direccionan por CAMPO del struct, no por nombre libre**: `draw.set({ viewProj: ..., time: t })` setea los campos del bind group. Si un shader no declara un campo (p.ej. `camPos` solo en glass), no le pases a los demás o falla con `Binding 'X' does not exist in 'draw'`.
- **Geometría: un atributo por buffer** — `geometry(gpu, { buffers: [{ attributes: { position: 'float32x3' }, data }, ...], indices })`. Si declaras `position+color+intensity` en un solo buffer pero solo pasas posición, falla `VGPU-MESH-DATA-MISALIGNED` (stride no divisible). Separa cada atributo en su propio buffer.
- **`final` es palabra reservada en WGSL** (no usable como identificador). Renombrar a `result`.
- **`npx vgpu check` valida los shaders en el build** vía el plugin Vite — un WGSL inválido falla el build. Úsalo como gate.
- **`effect` = fullscreen fragment-only** (genera el fullscreen triangle); `draw` = con geometría (VR/prisma). `frame(gpu, f => f.pass(target, drawable))` para render a target.
- Subpaths distintas según runtime: `vgpu` (navegador), `vgpu/node` (Dawn), `vgpu/mock` (tests). Importar de la equivocada falla en build o pide GPU.
- `effect`/`draw` direccionan uniforms **por su nombre WGSL** vía `set()` — si el shader renombra un uniform, deja de actualizarse silenciosamente; pasar `npx vgpu check` en CI.
- `set()` escribe inmediatamente: en el loop solo hay que poner lo que cambia cada frame (no re-setear constantes).
- `surface` clampa el device-pixel-ratio a [1, 2] salvo configuración explícita.
- Proyecto joven (creado 2026-05, Vercel Labs): la API puede moverse entre versiones — fijar versión en `package.json`.
- Sin ecosistema de loaders 3D: para importar GLTF/mallas pesadas, Three.js u otro.

## Verificación

1. `npx vgpu doctor` — comprueba adapter Dawn/software disponibles.
2. `npx vgpu check` — valida shaders del proyecto.
3. En CI con mock: `import { init } from "vgpu/mock"` y ejecutar el pipeline de render completo sobre `target` + `read()` para asserts de píxeles deterministas.

## Referencias

- Repo: https://github.com/vercel-labs/vgpu · Docs: https://vgpu.sh
- Registry: `vercel-labs/vgpu` (1.532⭐, explorado 2026-09-03)
