# Lecciones de implementación Water3J (v1, 14/14 tests)

## Arquitectura validada

`estado.js` (estado puro serializable, canonicalizado a 9 decimales, round-trip idéntico)
→ `campoOlas.js` (componentes Gerstner CPU, uniformes GPU)
→ `shaders.js` (GLSL océano/cielo/fondo con caústicas) → `main.js` (bootstrap + UI).

Regla de oro: la UI solo ESCRIBE estado; el render solo lo LEE. Nada de Three.js en estado.js.

## Física: reparto espectral que conserva Hs

- Reparto cuadrático EXACTO: `a_i = (Hs/2)·forma_i·norm` con `Σ forma_i² = 1` ⇒ `2·sqrt(Σa²) = Hs` por diseño (verificado Σa²·2 = 6.0000 con Hs=6).
- Escalar longitudes con Hs (ley de Toba: L ∝ Hs^0.4, coef 1.25 calibrado). Sin esto, el clamp de steepness (0.9) corta amplitudes y el Hs visual cae a la mitad. Si Σ steepness > clamp, estirar L, nunca debilitar el criterio del test.

## Pitfalls Three.js / GLSL (costaron horas)

1. `String.replace()` solo cambia la PRIMERA ocurrencia: en shaders con constantes tipo `MAX_OLAS` usar `replaceAll()` (aparece en declaración y en el bucle).
2. Three APLANA arrays de uniformes `vec4`: rellenar SIEMPRE hasta MAX_OLAS con ceros aunque haya menos olas activas (`Cannot read properties of undefined (reading 'toArray')`).
3. Exponer estado al runner (`window.Water3J`) con GETTER si la variable local se reasigna internamente (`comps = generarCampo(...)` invalida referencias capturadas).
4. `geoAgua.dispose()` al regenerar geometría por cambio de calidad.

## Bugs del solver SWE (pipes) que la biblia cazó

- Advección: donante PIERDE, receptor GANA (`dh[i-1] -= f; dh[i] += f` para f>0). Invertir = agua congelada.
- Fricción por unidad de TIEMPO: `f *= exp(-friccion·dt)`, nunca `(1-f)` por paso (deja 98% del flujo vivo ×8000 pasos ⇒ oscilación estacionaria con gradiente).
- El frente de la presa rota sobreestima velocidad sin flujo de momento (llega al borde vs Stoker 2.89): validar con vasos comunicantes (±0.36%) y anotar T15 (solver HLL) como extensión.

## Testing: biblia + navegador headless SIN depender del PC del usuario

- `tests/runner-navegador.mjs`: puppeteer + `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --no-sandbox`. Descargar Chrome con `npx puppeteer browsers install chrome` (y aprobar postinstall con `npm install-scripts approve puppeteer`).
- npm aprovisiona scripts: `npm install-scripts approve esbuild` para el postinstall de vite.
- Verificación de build/Pages: servidor http propio que mapee `/Water3J/` → `dist/` (la base de vite) antes de pushear. Script: `tests/verificar-build.mjs` y `tests/verificar-pages.mjs` en el repo.
- Umbrales honestos: SwiftShader rinde ~27 fps en calidad baja; en GPU real >60. Medir y documentar el contexto del número.

## Deploy GitHub Pages

- vite.config.js con `base: '/Water3J/'` + rollupOptions input multipage (landing index.html + demo.html).
- Si Pages no está habilitado: `gh api -X POST repos/Ntizar/Water3J/pages -f "build_type=workflow"` y relanzar el run (configure-pages falla con "Get Pages site failed... Not Found").
- Workflow moderno: actions/configure-pages@v5 + upload-pages-artifact + deploy-pages@v4 (skill github-pages-modern-deploy).

## Landing comercial (https://ntizar.github.io/Water3J/)

Patrón que funcionó (valorado 8.5/10): hero con degradado océano + titular degradado con background-clip:text, badge pulsante, CTAs con glow, stats glassmorphism con cifras doradas, grid de capacidades, bloque de precisión con chips de referencias (Stoker 1946, Goda 1985...), olas SVG animadas. Excepción visual aprobada por David: aquí SÍ es dark/océano (él lo pidió explícitamente: "tonos preciosos y llamativos"), a pesar de su preferencia general anti-dark para dashboards.

## Sesiones v2-v3: datos reales + Studio PC (lecciones nuevas)

### API de Puertos del Estado (Portus)
- Descubrir endpoints reales leyendo el JS de los widgets oficiales de portus.puertos.es (grep de URLs en el HTML/js de la web): el endpoint operativo es `https://poem.puertos.es/portus/StationData?code=<CODIGO>&params=Hm0,Tp` → JSON con timestamp GMT, valor y flag de calidad validada.
- SIMAR (descargas históricas): CSV tab-separado, huecos = **-99.9**. Filtrar con `valor <= -90`, NO solo `isFinite` (bug cazado por test T12 en su primer run).
- CORS abierto NO garantizado: ofrecer siempre vía manual (cargar JSON/CSV descargado) y documentarla; nunca fingir datos si la red falla.
- Guía completa para el usuario: `docs/10-guia-datos-puertos.md` en el repo.

### Studio (motor de estudios, PC)
- Motor 100% Node-testable y puro (`src/studio/motor.js`), UI solo consume: mismo patrón que estado.js de la app. Reutilizar la física ya validada de `src/fisica/` (coeficienteShoaling, presionGoda...) por composición, no reescribir.
- `presionGoda` devuelve la fuerza en la clave `F` (no `fuerzaTotal`): crear alias en el motor.
- Si el motor devuelve `generado: new Date().toISOString()`, los tests de reproducibilidad deben excluir ese campo del JSON comparado (timestamp legítimo ≠ falta de determinismo).
- Transparencia radical (exigida por David): cada paso del cálculo muestra fórmula + qué test de la biblia la avala + "ejemplo con tus números" con los valores reales del usuario, comprobable a mano con calculadora. Exigencia de producto, no opcional.
- Biblioteca local con IndexedDB (`db.js`): verificar persistencia con reload en puppeteer, no solo con la escritura.
- Cada HTML nuevo en un deploy multipage de vite: añadirlo a `input` de `vite.config.js` (mirar el archivo antes de patchear por memoria — el nombre de la clave puede no ser el esperado).
- Verificación puppeteer del Studio: `tests/ver-studio.mjs` (carga, métricas, recálculo en vivo con dispatchEvent) y `tests/ver-db.mjs` (guardar + reload). Dialogs de `prompt()` en puppeteer: `page.on('dialog', d => d.accept(nombre))`.
- **Rate de llamadas**: David pidió explícitamente máximo ~5 llamadas de red/sondeo por exploración externa ("Usa 5 llamadas como máximo"); planear 1-3 llamadas decisivas (grep de URLs + curl del endpoint + captura real) en vez de probar endpoints uno a uno.
