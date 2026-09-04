# Verificación headless de WebGPU / vgpu (distinto de WebGL)

Este skill cubre WebGL/Three.js (puppeteer + SwiftShader). Para **WebGPU con vgpu** el
camino es distinto y más fiable: usar el runtime nativo `vgpu/node` (Dawn) y **leer
píxeles del target** — no hace falta Chrome/puppeteer/SwiftShader ni la aprobación
remota de debugging.

Herramientas y umbrales validados construyendo `aurora-prism` (2026-09).

## Por qué no puppeteer+SwiftShader

WebGPU no corre bien sobre SwiftShader software; y la captura remota de Chrome exige
aprobar el debugging. Para verificar el **render real** de un pipeline vgpu, el camino
determinista es el adapter Dawn de `vgpu/node`.

## El método (vgpu/node + lectura de píxeles)

1. **Shaders como strings, no imports `.wgsl`**: en Node ESM no hay loader-node para
   `.wgsl`. Leer el archivo con `readFileSync` y pasarlo como string.
   ```js
   const beamWgsl = readFileSync('src/shaders/beam.wgsl', 'utf8');
   ```
2. `init()` de `vgpu/node`, crea `target(gpu, { size, format })`, monta `draw`/`effect`,
   y renderiza con `frame(gpu, f => f.pass({ target }, (p) => { p.draw(x); }))`.
3. Lee píxeles `await target.read()` y mide luminancia por tercios
   (`0.3R + 0.6G + 0.1B`).

## Umbrales (para assert de render)

| Tercio | Interpretación |
|---|---|
| max < 20 en los tres | PLANO — shader no dibuja (geometría/cámara fuera de encuadre) |
| max >= 20–60 en alguna zona | Estructura presente, luz visible |
| max > 100-160 | Detalle fuerte (beam/glass nítido) |

En `aurora-prism` el render del beam+glass dio `mid max 255, bot max 166` → `VEREDICTO:
OK`. Antes de fijar la geometría correcta, con una cámara identidad manual salió todo
0 (plano) — **un "PLANO" en la sonda casi siempre es cámara/encuadre, no shader roto**;
usa la `perspectiveCamera` real (viewProjection combinado) antes de concluir.

## Diferencia clave vs WebGL

- WebGL/Three.js → puppeteer + SwiftShader + (`gl.readPixels` o `captureScreenshot`).
- WebGPU/vgpu → `vgpu/node` (Dawn) + `target.read()` — determinista, sin GPU real, sin
  aprobación de Chrome.
- En CI el adapter `vgpu/mock` da el mismo pipeline con software determinista
  (`import { init } from 'vgpu/mock'`).
