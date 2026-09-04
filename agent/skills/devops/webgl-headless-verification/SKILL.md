---
name: webgl-headless-verification
version: "1.1.0"
description: "Use al verificar render 3D headless sin GPU (WebGL/Three.js y WebGPU/vgpu). Métodos por runtime: puppeteer+SwiftShader para WebGL, vgpu/node (Dawn)+read() para WebGPU."
tags: [webgl, webgpu, vgpu, threejs, puppeteer, swiftshader, dawn, headless, testing, verificacion, gpu]
---

# Verificación Headless de Apps WebGL/3D

## Resumen

Cómo verificar que una escena Three.js/WebGL renderiza correctamente (relieve, animación, espuma, colores) sin depender de la GPU del usuario ni de aprobaciones de Chrome remoto. Método: puppeteer con Chromium propio + SwiftShader (WebGL por software) + **medición numérica de píxeles** en vez de análisis visual.

## El método en 5 pasos

1. **Setup**: `npm i puppeteer` + `npx puppeteer browsers install chrome`. Lanzar con `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --no-sandbox`.
2. **preserveDrawingBuffer: true** en el `WebGLRenderer` — sin esto `gl.readPixels` devuelve TODO ceros (el buffer se vacía tras el swap). Alternativa sin tocar la app: `Page.captureScreenshot` por CDP.
3. **Medir píxeles, no mirar**: `readPixels` de la franja del agua y calcular min/max/media de luminancia (`0.3R+0.6G+0.1B`). Ver tabla de interpretación abajo.
4. **Animación**: capturar 2 muestras separadas ~2 s; desviación media entre frames >2 = el agua se mueve.
5. **Estado lógico**: verificar HUD/DOM (`window.App.estado`) en paralelo — el estado lógico es la fuente de verdad cuando el render es dudoso.

## Interpretación de rangos de luminancia (franja central)

| Rango min-max | Significado |
|---|---|
| 0–5 | Plano o frame caído (frame viejo/pre-displacement) |
| 10–20 | Degradado suave, sin estructura |
| 60–160 | Relieve/textura presentes |
| >160 | Detalle fuerte (espuma, crestas, horizonte) |

Media constante que coincide con un color conocido de la escena (cielo, disco lejano) = ese objeto llena el cuadro: la cámara está mal encuadrada o el mesh principal no se dibuja.

## Pitfalls críticos (todos verificados en Water3J v2)

- **`MeshPhysicalMaterial` con `transmission` se ve NEGRO en render software y en GPUs débiles** (verificado aurora-prism, 2026-09-03): `transmission`/`ior`/`clearcoat` y las `PointLight` débiles hacen que el prisma salga como una silueta oscura bajo SwiftShader — y ese mismo "cristal negro" es lo que David vio y lo que le hizo reportar "no veo nada". **Arreglo:** usar un material que no dependa de transmisión de rayos ni de luces para el objeto principal: (a) `MeshPhysicalMaterial` con `transmission` BAJO (0.5) + `emissive` de respaldo (`emissiveIntensity ~0.6`) para que nunca quede un hueco negro, y (b) luces potentes (`PointLight` intensidad 150-180, no 26-30) + `AmbientLight` fuerte. Para el haz/objeto que debe verse SIEMPRE, usar `MeshBasicMaterial` + `vertexColors: true` (no depende de luces ni tone mapping → renderiza en cualquier GPU).
- **`gl.readPixels` devuelve TODO ceros si no hay `preserveDrawingBuffer: true`** en el `WebGLRenderer` (el buffer se vacía tras el swap). En un canvas cuyo `context` no preserva el buffer, `readPixels` da 0 en todos los canales aunque la escena renderice — confundido con "no hay luz". Alternativa que no toca la app: `Page.captureScreenshot` por CDP + medir píxeles de la imagen (subir la screenshot a `page.evaluate`, leer con `getImageData` y clasificar).
- **El canvas queda en 300×150 (tamaño por defecto) si el contenedor mide 0 al inicializar**: en headless, `container.clientWidth/clientHeight` puede ser 0 al cargar, y `renderer.setSize(0,0)` deja el canvas sin reescalar. Para tests, fijar el `defaultViewport` y llamar `renderer.setSize` tras un tick, o forzar un tamaño en el setup de la sonda.
- **Medir color vivivo (saturación), no solo luminancia, para validar un objeto de color:** el beam R/G/B tiene `sat = max-min > 60 && max > 90`. Clasificar cada píxel como `color/dim/dark` y contar — así se aísla un haz de colores de un fondo estrellado azul-gris que, con solo luminancia, parece "tener estructura". NOTA: si la sonda se implementa dentro de `page.evaluate`, la función clasificadora debe vivir DENTRO (no fuera, donde `is not defined`).
- **SwiftShader da frames parciales/incompletos**: las screenshots muestran bandas diagonales de color o el frame inicial; el análisis de visión dirá "mar plano" aunque el buffer GL tenga relieve. NUNCA concluir desde una captura — medir píxeles.
- **Coste de vertex shader satura el render software**: umbral estrecho (37k vértices × 48 olas Gerstner satura → solo frames viejos; 12 olas pasa). Reducir componentes visuales, no la física.
- **rAF funciona (~12 fps headless)**: si la app avanza y el HUD cambia, el loop está vivo; el problema es de coste de frame, no de congelación.
- **Detección de GPU software**: `gl.getParameter(gl.RENDERER)` devuelve "WebKit WebGL" en puppeteer — usar `WEBGL_debug_renderer_info` → `UNMASKED_RENDERER_WEBGL`, y/o heurística de fps (si fps<3 tras 4 s → bajar calidad).
- **Swap de geometría en caliente** tras campo grande: SwiftShader pierde el frame y vuelve a mostrar frames viejos. La adaptación de calidad debe decidirse en el ARRANQUE, antes del primer render.
- **Tests mínimos**: si la app es sospechosa, crear una escena mínima (plano + vertex shader con `sin(p.x)` + varying de altura) servida vía el dev server; si el varying llega con rango, el pipeline funciona y el bug está en la app. Aísla shader vs. app en un paso.
- **Loop que reescribe la cámara**: si `actualizarCamara()` corre cada frame, cualquier posición manual en tests se pisa al frame siguiente — exponer setters (`setCamara({angX, dist, auto})`) desde la app para tests.
- **`page.setContent` + `<script type="module">` no resuelve imports** relativos: servir el test mínimo como archivo real vía el dev server (Vite) en vez de contenido inline.

## Diagnóstico típico por síntomas

| Síntoma | Causa probable |
|---|---|
| Todo el canvas = color plano de un objeto secundario | Ese objeto tapa al principal (orden de dibujo/profundidad) o el principal no se dibuja |
| Media 204-222 uniforme | Solo cielo en cuadro → cámara fuera de encuadre o mesh invisible (caras culled: cámara bajo las crestas) |
| Fresnel alto lava todo el relieve en vistas rasantes | Limitar la mezcla del reflejo del cielo (ej. `fresnel * 0.35`) |
| Preset "no se aplica" a los ~14 s | Un director automático está pisando el estado → control manual debe apagarlo |
| Frame de screenshot no cambia nunca | Vertex shader satura el software renderer → reducir vértices × iteraciones |

## Receta de sonda de píxeles

Ver `scripts/sonda-pixeles.mjs` — puppeteer headless, aplica un preset, espera, mide franjas del buffer y reporta rango/media por tercios. Copiar y adaptar los selectores (`window.Water3J.*`) al proyecto.

## WebGPU (vgpu) — vía alternativa

Para **WebGPU con vgpu** NO usar puppeteer+SwiftShader: usar el adapter Dawn de
`vgpu/node` y leer píxeles del target con `target.read()`. Determinista, sin GPU real,
sin aprobación de Chrome. Detalle y umbrales: `references/webgpu-vgpu-headless.md`.

**Pitfall confirmado (repo aurora-prism, 2026-09-03):** en Chrome headless con
`--enable-webgpu`, `navigator.gpu.requestAdapter()` devuelve **`null`** y la consola da
`VGPUError: navigator.gpu.requestAdapter() returned null` / `[warn] No available adapters`.
El adapter WebGPU de software **no** está disponible en Chromium headless (SwiftShader cubre
WebGL, no WebGPU). El `fallback` de la app se muestra correctamente → no es un bug del código.
Verificación siempre por la vía `vgpu/node` (Dawn).

**Pitfall del `.wgsl` en Node ESM (para tests con `vgpu/node`):** `import shader from './x.wgsl'`
falla con `ERR_UNKNOWN_FILE_EXTENSION: Unknown file extension ".wgsl"` porque no hay un
loader-node ESM. Los `.wgsl` solo se importan como módulo con el plugin Vite (navegador).
En tests Node pasar el shader como **string**: `const s = readFileSync('./x.wgsl', 'utf8')` y
`draw(gpu, { shader: s })`.

**Umbral verificable de la sonda WebGPU:** renderizar a un `target` de 256×256, leer con
`read()` y medir min/max/media de luminancia por tercios. El veredicto "OK — hay estructura de
luz" se da cuando al menos un tercio alcanza `max >= 20`. Todo-cero (`min=max=0`) = pipeline
compila pero la cámara/geometría no encuadra (en `vgpu/node` el `viewProjection` ya viene
combinado — no pongas `proj` y `view` por separado).

## Referencias Cruzadas

- `software-development` → debugging sistemático, TDD (la biblia de tests antes que el render)
- `browser-use-ai` / `data-pipeline` → automatización de navegador general
- Proyecto de referencia: Water3J (repo Ntizar/Water3J), commit 87f1780 — todos los valores de umbral salen de ahí.
