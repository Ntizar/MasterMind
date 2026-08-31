# Lecciones de implementación: salidas profesionales + UX de estudio (sesión agosto 2026)

## Informe imprimible a PDF (src/studio/informe.js)
- Patrón: `window.open('', '_blank')` + `w.document.write(html)` + `w.document.close()` → el usuario hace Ctrl+P → PDF. Sin dependencias, sin print CSS complejo (solo `@media print` suave).
- El informe es un CONTRATO de transparencia, no decoración: condiciones de partida con la FUENTE de cada dato (boya con código y fecha GMT, o "usuario"), física con qué test de la biblia avala cada paso, y sección "Procedimiento de validación para el revisor" con las URLs exactas (`poem.puertos.es/portus/StationData?code=...`, `rest.emodnet-bathymetry.eu/depth_sample?geom=POINT(lon+lat)`) para comprobar cualquier número a mano.
- Pitfall: si la función auxiliar del template (`resumenFilas`) no se define, el error solo aparece al PULSAR el botón (no en build) — el E2E debe abrir el popup y verificar el contenido real (`contenido.includes('Estudio de propagación')`), no solo que se abrió.
- En puppeteer, popups: `page.on('popup', p => ...)` y luego `p.evaluate(() => document.body.innerHTML)` (NO `.property('content')` — no existe en esa API).

## Exportación CSV
- `descargar(nombre, contenido, mime)`: Blob + `URL.createObjectURL` + `a.click()` + `revokeObjectURL`. Para interceptar descargas en puppeteer: CDP `Browser.setDownloadBehavior` (opcional; basta verificar que el click no lanza error).
- CSV del transecto: cabecera explícita `x_m,h_m,Hs_m,Ks,Kr,alfa_deg,rompe` — el `rompe` como 1/0 para hojas de cálculo.

## Boya real → simulador 2D (flujo completo)
- `portus.js` (Studio) separa transporte (`descargarPartida`) de parsing (`ultimaPartida`): extrae la última fila con Hm0/Tp válidos rechazando huecos -99.9 y valores imposibles (Hs≥20, Tp fuera 2-30 → null). Testeado en T16 con formato real y formato array.
- Al cargar la boya: escribir en los inputs (`inHs.value`, `inT.value`) + recalcular + guardar `boyaActual = { code, ...partida }` para que el informe cite la fuente exacta.
- Estado compartido UI↔informe vía `window.__ultimarejilla2D` (rejilla EMODnet de la última simulación 2D) — el informe la cita en la sección de batimetría.

## UX de estudio (lo que David llama "software profesional")
- Panel lateral con secciones NUMERADAS en el orden del flujo de trabajo real (1 oleaje → 2 boya real → 3 2D → 4 estructura → 5 salidas → 6 escenarios). Cada acción con botón dedicado y div de estado con feedback vivo ("Consultando…", "✅ Hs=… partida de … GMT", error con la vía alternativa).
- Regla de David: "generar todo y dibujar exactamente lo que un software profesional necesitaría" — cada fase debe terminar con salidas exportables (informe/CSV), no solo visualización.
- Nunca dejar funciones basura ni placeholders en archivos nuevos (escribir la versión final limpia de una vez): dos borradores con stubs (`out_b(out)`, `return null`, funciones duplicadas) costaron patches de limpieza y un bug real (`resumenFilas` faltante) detectado solo por E2E.

## README como estado real
- David pidió explícitamente: "el README con el estado real del proyecto". Estructura que funcionó: qué es (app móvil + Studio) → tabla de tandas de tests → bugs cazados por la biblia → fuentes de datos con APIs → física implementada → cómo usar → cómo validar cualquier número → estructura del repo → desarrollo → documentación. Actualizarlo en cada fase entregada.
