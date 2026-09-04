---
name: html-artifact-integrity
description: Use al escribir HTML grande — trozos y verificación previa.
version: "1.0.0"
tags: [html, escritura-ficheros, verificacion, integridad, aurora]
---

# Integridad de artefactos HTML grandes

## Cuándo usar

Al generar o entregar cualquier HTML >5 KB (informes, auditorías, dashboards, landings), y al citar cifras de repos o herramientas en documentos comparativos. Incluye referencia del estado verificado del repo Aurora: `references/aurora-repo-estado.md`.

## Problema observado (2026-08-28)

Los writes de ficheros HTML grandes (>5 KB) con `write_file` pueden **corromperse a mitad de stream**: texto truncado, fragmentos absurdos insertados (`1</ bus`, `< doble tbody`), placeholders sin sentido. Ocurrió 2 veces en la misma sesión. El tool reporta `verified: true` aunque el contenido esté roto — la verificación del tool NO detecta corrupción semántica.

## Flujo fiable (validado)

1. **Partir en trozos de ~2-3 KB máximo.** Escribir el trozo 1 con `write_file` al destino (sobrescribe), y los siguientes a ficheros temporales (`$LOCALAPPDATA/Temp/parteN.html`).
2. **Verificar cada trozo tras escribirlo**: releer o comprobar que el contenido tiene sentido antes de continuar. Si un trozo sale corrupto, reescribir SOLO ese trozo (más pequeño si hace falta).
3. **Ensamblar**: `cat parte2.html parte3.html >> destino.html` en un solo comando de terminal.
4. **Verificación final programática** (no a ojo) — balance de etiquetas y contenido. **SIEMPRE regex con límite `[\s>]`**: un `h.count('<p')` ingenuo también cuenta `<path` (SVG) y `<b` cuenta `<body`/`<br>`, produciendo MISMATCH falsos que obligan a re-verificar (pasó 2026-09-01 con `p 25≠22` que eran 22=22):
   ```python
   import re
   h = open(fichero, encoding='utf-8').read()
   for tag in ['section','div','p','span','table','tbody','thead','html','body']:
       o = len(re.findall(r'<%s(?=[\s>])' % tag, h))
       assert o == h.count('</%s>' % tag), (tag, o)
   # auto-cerrantes (line, circle, path, img, br) se excluyen del balance
   assert h.rstrip().endswith('</html>')
   ```
4b. **Validar la sintaxis del JS antes de la captura visual (2026-09-01).** Tras ensamblar, extraer el `<script>` y pasarlo por `node --check` — caza errores de sintaxis de ensamblaje (un trozo que dejó `cat[...];` sin cerrar, un `rint()` duplicado) que el balance de etiquetas no ve y que de otro modo aparecerían como «página vacía» en la captura:
   ```bash
   python -c "import re,sys; h=open(sys.argv[1],encoding='utf-8').read(); open('tmp.js','w').write(re.search(r'<script>(.*)</script>',h,re.S).group(1))" file.html
   node --check tmp.js && echo OK
   ```
   Verificar que el JS extraído sea **sintácticamente válido por sí mismo**; al dividir por trozos conviene que cada parte empiece/termine en frontera de bloque (p. ej. el array de datos acaba con `];`) para que la unión sea limpia.
5. **Verificación visual**: abrir con `open_preview` y leer con `read_preview` para confirmar que el texto renderizado es coherente (detecta corrupción que el balance de etiquetas no ve).
6. Limpiar los temporales de `$LOCALAPPDATA/Temp`.

## Pitfalls

- **No confiar en el `verified: true` del write**: verifica hash on-disk vs lo enviado, pero si el stream se corrompió antes de llegar, "verifica" contenido corrupto.
- **NO anexar HTML grande con heredoc de bash** (`cat >> destino << 'EOF'`): un bloque de ~30 KB con comillas/apóstrofes del texto falla con `unexpected EOF while looking for matching '''` y se pierde el intento entero. Flujo correcto: escribir cada parte como fichero propio con `write_file` y ensamblar con `cat parte1 parte2 > destino` en un solo comando, luego validar balance (paso 4) y borrar las partes.
- **Reescribir el fichero entero tras detectar corrupción** reintroduce el mismo riesgo: mejor trozos más pequeños.
- Si `execute_code` está bloqueado por consentimiento, el plan B es trozos + `cat` (validado). No insistir con execute_code.
- La corrupción puede insertar texto que **parece** HTML válido: balance de etiquetas + lectura del preview es el mínimo aceptable antes de entregar.

## Verificación de datos antes de citarlos

Cuando el artefacto compara herramientas/repos, verificar cada cifra con el sistema vivo (API GitHub, ficheros locales, DB), nunca con memoria o con lo que diga un README desactualizado. Ejemplos reales (2026-08-28): el README de MasterMind decía "143 skills" y la cuenta real en ChromaDB era 311; el skill de Aurora referenciaba un `CHEATSHEET.md` eliminado del repo (404 verificado por API de GitHub). Para porcentajes (p. ej. barras de lenguajes), calcularlos desde `gh api repos/O/R/languages` con un script — no estimarlos a ojo.

## Rebuild estático cuando "no se ve nada" (2026-08-28, galería Aurora)

Detalle completo del caso: `references/js-rendered-blank-page.md`.

Síntoma: el usuario reporta página en blanco o casi vacía pese a HTTP 200 y CSS íntegro (el diff live-vs-repo era solo CRLF). Causa raíz típica: el contenido se pinta por JS (`innerHTML` de tokens leídos del CSSOM, KPIs, gráficos) — cualquier fallo del script o del CDN deja la página vacía, y los parches incrementales NO lo arreglan. Remedio: rehacer el HTML con contenido **100% estático visible sin JS**, y dejar el JS solo como mejora progresiva (scrollspy, reveals, switchers). Reglas del rebuild:

- Nunca `opacity:0` condicionado a que el JS añada una clase (`is-visible`): si el JS muere, el contenido desaparece. Gatear reveals solo cuando un script haya añadido antes una clase `js` al root.
- Mostrar solo API verificada: extraer las clases reales de cada CSS con regex sobre los ficheros (catálogo `classes.json` por pack) antes de escribir ejemplos — nada de clases recordadas de memoria.
- Ensamblar desde `gallery-parts/parteN.html` con `cat parte1..4 > destino` (mismo flujo de trozos de arriba), y reescribir el JS final para que maneje los controles REALES del HTML (botones `data-skin`, selects) — los anchors huérfanos del sidebar (`api-*`) se cazan con el chequeo `href="#x"` → ids inexistentes.

## Verificación visual de páginas con scroll-reveals (2026-09-01, nantest web)

Una landing narrativa con elementos `.rv{opacity:0}` revelados por IntersectionObserver **miente al capturarla headless**: Chrome pinta antes de que el observer dispare, y `vision_analyze` reporta «página vacía / contraste bajísimo / contenido no cargado» cuando en un navegador real todo está bien. Dos reglas para no perseguir fantasmas:

- **Modo aplanado de prueba.** Añadir al JS: `if (location.hash==='#test') document.body.classList.add('aplanado')` con CSS `body.aplanado .rv{opacity:1!important;transform:none!important;transition:none!important}` (y lo mismo para animaciones de entrada tipo `@keyframes`: `animation:none!important`). Capturar SIEMPRE la URL con `#test` para auditoría visual. Sin esto, cada franja parece rota y se "arregla" contraste que no estaba roto.
- **Altura real antes de recortar.** No adivinar `--window-size=...,7600`: el fondo fijo rellena el hueco y el análisis ve "sección final vacía" (en realidad fuera del documento). Sondear la altura con un script sonda que haga `document.title='ALTO:'+document.documentElement.scrollHeight` + `--dump-dom` + `grep -o "ALTO:[0-9]*"`, y luego recapturar con `--window-size` ≈ esa altura (o recortar el PNG a scrollHeight con PIL). Ojo: la altura cambia con el viewport — medir con el mismo ancho y una altura generosa.
- **Fallback de revelado para usuarios reales:** `setTimeout(()=>document.querySelectorAll('.rv:not(.on)').forEach(el=>el.classList.add('on')),4000)` — si el observer falla o el contenido ya está visible sin scroll, nada queda oculto.
- **Firmas y HUD en `position:absolute` dentro de secciones muy altas** quedan fuera de franjas de captura: verificar el cierre midiendo la última `.act` (`offsetTop+offsetHeight` vía title sonda), no asumiendo que el final de página = final del screenshot.

## Verificación headless con Chrome en Windows (alternativa a browser_exec)

Cuando el navegador de automatización no esté disponible (pide permiso de depuración remota en Chrome), verificar por terminal:

```bash
"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --dump-dom --virtual-time-budget=12000 "file:///C:/ruta/absoluta/archivo.html" > dump.html
```

- **SIEMPRE `file:///` con ruta absoluta en barras** — pasar la ruta cruda (`gallery.html`) hace que Chrome la trate como dominio → DNS error y el dump es la página de error.
- Aserciones por grep sobre el dump: nº de secciones/anclas presentes, ausencia de mojibake, `<canvas>` creados por Three.js, 0 clases gate.
- WebGL/Three.js: añadir `--enable-unsafe-swiftshader --use-gl=angle`. Errores de consola: `--enable-logging=stderr` y filtrar `uncaught|error` (excluir ruido GPU/Fontconfig).
- Screenshot: **ruta absoluta con barras SIEMPRE** (`--screenshot=C:/Users/.../out.png --window-size=1440,2400`). Con ruta relativa (y sobre todo combinada con `--dump-dom` y redirecciones), Chrome la resuelve contra su propio cwd y falla `Failed to write file: Acceso denegado (0x5)` — verificar el PNG con `ls` después.
- **Piezas canvas/generativas** (plexus, partículas, animación JS pura): el grep del dump NO dice nada del render. Flujo validado (2026-09-01, nantest): `--virtual-time-budget≥8000` + `--screenshot` absoluto → `vision_analyze` pidiendo defectos concretos (nodos huérfanos, zonas vacías, contraste de líneas/halos) → corregir → re-capturar → re-verificar. Esperar al menos una ronda de crítica visual; es normal que la primera versión se vea "apagada o a medio dibujar". Truco de densidad: enlaces **k-nearest** (cada nodo enlaza con sus K más cercanos, K≈3) eliminan los puntos huérfanos que el umbral de proximidad deja sueltos; halos con `createRadialGradient` en modo `lighter` para que los nodos brillen.
- Deploy GitHub Pages desde repo nuevo: `gh repo create O/R --public` → push `main` → `gh api repos/O/R/pages -X POST -f "source[branch]=main" -f "source[path]=/"` → poll `curl -s -o /dev/null -w '%{http_code}' URL` cada ~20s (404 durante `building` es normal; ~40s hasta 200, confirmar tamaño con `curl -s URL | wc -c`). Repos ya publicados: `gh api repos/O/R/pages/builds/latest --jq '{status,commit}'` + byte-exactitud vs `wc -c fichero`. La caché de Pages puede tardar ~1 min extra tras `built`.

## Piezas creativas «flipalo»: espectáculo primero, robustez como red de seguridad (2026-09-01, nantest)

Lección de dirección de la sesión completa: el usuario pidió "algo totalmente loco, filosófico, visual". El agente falló POR EXCESO de prudencia: primero pieza de una sola pantalla («quería más web, con historia»), luego web editorial sobrecargada de técnica («has seguido demasiado las normas, más filosófico y menos técnico»), luego un poema calmado con JS de enjambre («está roto»), y por último CSS puro estático («no es lo que buscábamos»). Lo que sí validó: **vórtice canvas hiperactivo + palabras estáticas flotando encima + `<noscript>` de emergencia**. Reglas:

- **El espectáculo es el producto.** Canvas generativo denso (anillos girando, estelas con `rgba` de arrastre, modos `lighter`, reacción al puntero, explosiones al click) + texto estático mínimo por encima (`mix-blend-mode:screen` + glow). La robustez NO debe quitar el show: se añade como capa de seguridad, nunca sustituyendo la pieza.
- **Red de seguridad en 3 capas** (invisible cuando todo funciona): texto HTML/CSS siempre visible sobre el canvas; `<noscript>` con un gradiente de fondo; contadores/reveales nunca ocultan contenido de base.
- **Pedir confirmación creativa con 2-3 opciones de giro antes de iterar más** — iterar a ciegas sobre "esto no es lo que queríamos" quema 4 versiones.

## Verificación de páginas LONG-SCROLL (multi-sección 100vh) (2026-09-01, descenso nantest)

Una página de N secciones de 100vh (≈7000px+) **no se puede verificar con una captura de página completa**: Chrome headless con `--window-size=...,6900` renderiza el canvas fixed y la primera viewport de contenido DOM, y el resto sale vacío aunque la página esté perfecta. Lo que NO funcionó: `scrollTo(0,y)` inyectado en load + `--virtual-time-budget` (captura antes del scroll), ni fragmentos `#id` en `file://`. Método validado, en orden de preferencia:

1. **Verificación estructural por DOM** (barata y suficiente para contenido): `--dump-dom` y contar palabras/`.rv`/`.flot` por `<section>` con regex en Python. Confirma que las 8 secciones tienen su texto completo, que nada se perdió en el ensamblaje.
2. **Modo captura por sección** para auditoría visual puntual: CSS `html.capmode .sec{display:none}` + `html.capmode .sec.activa{display:flex}`, y en el JS `if (location.hash==='#test'){ const n=+(new URLSearchParams(location.search).get('sec')||0); document.querySelectorAll('.sec').forEach((s,i)=>s.classList.toggle('activa',i===n)); }`. Capturar `...?sec=4` una sección por screenshot (100vh normal). El screenshot puede seguir congelando animaciones — juzgar composición estática.
3. Si el canvas es fixed con estela, en modo test dibujar **un solo frame** (`if(test) cuadro(); else requestAnimationFrame(cuadro)`) para que la captura no pille estados intermedios del fade.

No iterar el diseño visual por franjas de una captura larga: las conclusiones serán falsas (vacío = fuera del documento, no sección rota). Verificar el cierre (última sección + firma) capturando la última sección en modo `?sec=N-1`.

## Pitfall: captura headless congela animaciones CSS — estados iniciales `opacity:0` parecen "roto" (2026-09-01)

Chrome headless con `--virtual-time-budget` congela las CSS animations en su primer frame: N capturas con distintos budgets producen PNGs **byte-idénticos** (señal de congelación). Consecuencia: cualquier elemento cuya visibilidad arranque en `opacity:0` dentro de un keyframe («aparece») se captura invisible y `vision_analyze` reporta «página vacía / falta contenido» aunque en un navegador real funcione — y el agente acaba «arreglando» contraste que no estaba roto o degradando la pieza a texto estático soso.

- **Regla de diseño a prueba de captura:** la visibilidad base NUNCA depende del estado inicial de una animación. Escribir `opacity:.9` en la clase y que el keyframe solo module (`@keyframes respira{0%,100%{opacity:.9}50%{opacity:.4}}`), en vez de `opacity:0` + keyframe de entrada.
- **Detección:** si dos screenshots con distinto `--virtual-time-budget` pesan exactamente igual, las animaciones están congeladas — juzgar composición estática, no presencia.
- `prefers-reduced-motion` y `@media print` deben fijar `opacity` visible (`animation:none` + opacity explícita), mismo motivo.

## Pitfall: `patch` difuso puede borrar el bloque equivocado

En HTML grandes, un `patch` cuyo `old_string` coincide ambiguamente puede aplicar el reemplazo en otra zona y eliminar contenido hermano (pasó al insertar una tabla duplicando un cierre `</section>`). **SIEMPRE leer el diff devuelto línea a línea y releer la zona tocada tras cada patch**; si borró de más, restaurar el bloque en el siguiente paso antes de continuar. Con secuencias repetidas (`</table>\n</div>\n</section>`), incluir contexto único (un `<h4>` o comentario) en `old_string` para anclar el sitio.