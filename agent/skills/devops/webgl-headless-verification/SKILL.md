---
name: webgl-headless-verification
version: "1.0.0"
description: "Use al verificar WebGL/Three.js headless sin GPU."
tags: [webgl, threejs, puppeteer, swiftshader, headless, testing, verificacion, gpu]
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

## Referencias Cruzadas

- `software-development` → debugging sistemático, TDD (la biblia de tests antes que el render)
- `browser-use-ai` / `data-pipeline` → automatización de navegador general
- Proyecto de referencia: Water3J (repo Ntizar/Water3J), commit 87f1780 — todos los valores de umbral salen de ahí.
