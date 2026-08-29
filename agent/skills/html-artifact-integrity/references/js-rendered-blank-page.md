# Página "en blanco" por contenido renderizado por JS — diagnóstico y rebuild

Caso real: `Ntizar-Aurora/gallery.html` (2026-08-28). Usuario: "está totalmente roto, no se ve prácticamente nada". HTTP 200, CSS íntegro en producción (diff live-vs-repo = solo CRLF), pero página visualmente vacía.

## Causa raíz

La página pintaba su contenido por JS: tokens leídos del CSSOM, KPIs, tipografía y radios vía `innerHTML`, secciones enteras generadas en runtime, `.nz-reveal` con `opacity:0` hasta que un IntersectionObserver añadía `is-visible`. Cualquier fallo del script (o del CDN, o del import map de Three.js) deja la página vacía. Los parches incrementales (encoding, gradientes, enlaces de packs) no tocaban este mecanismo → "sigue roto" tras 3 rondas de fixes.

## Diagnóstico que sí funcionó

1. Confirmar integridad del despliegue: `curl -s URL | wc -c` vs `wc -c fichero` (byte-exactitud), `gh api repos/O/R/pages/builds/latest`.
2. Chrome headless sobre el archivo local:
   ```bash
   "C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
     --dump-dom --virtual-time-budget=12000 \
     "file:///C:/Users/<u>/Projects/<repo>/gallery.html" > dump.html
   ```
   - **Trampa:** ruta cruda o relativa → Chrome la trata como dominio → DNS_PROBE, el dump es la página de error. `file:///` + ruta absoluta con barras SIEMPRE.
   - Grep del dump: nº de secciones esperadas presentes, 0 mojibake, nº de `<canvas>`, `is-visible` (0 con scroll-to-top es normal: el observer no dispara sin scroll).
   - WebGL: `--enable-unsafe-swiftshader --use-gl=angle`. Errores: `--enable-logging=stderr 2>&1 | grep -iE "uncaught|error"` excluyendo ruido GPU/Fontconfig.
3. Conclusión: si el HTML base ya es JS-dependiente en >50% del contenido visible → rebuild, no parches.

## Reglas del rebuild estático

- Todo el contenido visible sale del HTML; el JS solo mejora (scrollspy, botones de tema/skin, selects de ejes, reveals).
- Reveals: nunca `opacity:0` gateado por clase que añade el JS. Gatear con `html.js` que el propio script pone ANTES de observar — sin JS, todo visible.
- Catálogo de API verificado: extraer clases reales de cada CSS con regex antes de escribir ejemplos (generar `classes.json` por pack). Citar solo lo que existe.
- Ensamblar en partes (`parteN.html` → `cat parte1..N > gallery.html`) y validar balance de tags + anchors (`href="#x"` → ids) programáticamente.
- El JS final debe manejar los controles que el HTML realmente declara (botones `data-skin`, selects `data-set`) — reescribir ambos a la vez o sobra el mismísimo bug que se pretendía arreglar.

## Señal de alarma temprana

Usuario dice "no se ve nada" + HTTP 200 + CSS ok → NO diagnosticar por lectura de código a mano; dump-dom primero. Y si el parche incremental no cambia la percepción tras 2 rondas, pasar a rebuild estático.
