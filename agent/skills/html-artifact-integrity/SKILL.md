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
4. **Verificación final programática** (no a ojo) — balance de etiquetas y contenido:
   ```python
   h = open(fichero, encoding='utf-8').read()
   for tag in ['section','div','table','tbody','thead','html','body']:
       assert h.count(f'<{tag}') == h.count(f'</{tag}>'), tag
   assert h.rstrip().endswith('</html>')
   ```
5. **Verificación visual**: abrir con `open_preview` y leer con `read_preview` para confirmar que el texto renderizado es coherente (detecta corrupción que el balance de etiquetas no ve).
6. Limpiar los temporales de `$LOCALAPPDATA/Temp`.

## Pitfalls

- **No confiar en el `verified: true` del write**: verifica hash on-disk vs lo enviado, pero si el stream se corrompió antes de llegar, "verifica" contenido corrupto.
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

## Verificación headless con Chrome en Windows (alternativa a browser_exec)

Cuando el navegador de automatización no esté disponible (pide permiso de depuración remota en Chrome), verificar por terminal:

```bash
"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --dump-dom --virtual-time-budget=12000 "file:///C:/ruta/absoluta/archivo.html" > dump.html
```

- **SIEMPRE `file:///` con ruta absoluta en barras** — pasar la ruta cruda (`gallery.html`) hace que Chrome la trate como dominio → DNS error y el dump es la página de error.
- Aserciones por grep sobre el dump: nº de secciones/anclas presentes, ausencia de mojibake, `<canvas>` creados por Three.js, 0 clases gate.
- WebGL/Three.js: añadir `--enable-unsafe-swiftshader --use-gl=angle`. Errores de consola: `--enable-logging=stderr` y filtrar `uncaught|error` (excluir ruido GPU/Fontconfig).
- Screenshot para cortes: `--screenshot=out.png --window-size=1440,2400` (el output del comando corta el path en el log, pero el PNG se guarda).
- Deploy GitHub Pages: `gh api repos/O/R/pages/builds/latest --jq '{status,commit}'` + byte-exactitud `curl -s URL | wc -c` vs `wc -c fichero`. La caché de Pages puede tardar ~1 min extra tras `built`.

## Pitfall: `patch` difuso puede borrar el bloque equivocado

En HTML grandes, un `patch` cuyo `old_string` coincide ambiguamente puede aplicar el reemplazo en otra zona y eliminar contenido hermano (pasó al insertar una tabla duplicando un cierre `</section>`). **SIEMPRE leer el diff devuelto línea a línea y releer la zona tocada tras cada patch**; si borró de más, restaurar el bloque en el siguiente paso antes de continuar. Con secuencias repetidas (`</table>\n</div>\n</section>`), incluir contexto único (un `<h4>` o comentario) en `old_string` para anclar el sitio.