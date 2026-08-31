---
name: nichos-afiliacion-web
version: "1.0.0"
description: Use al crear webs de nicho con afiliación y cron autónomo.
author: "Mastermind (David Antizar)"
license: "MIT"
metadata:
  hermes:
    tags: [afiliacion, amazon, nicho, github-pages, cron, seo]
    related_skills: [github-pages-modern-deploy, project-spec-workflow]
---

# Webs de nicho con afiliación — flujo completo

## When to Use
- El usuario pide crear una web para ganar dinero con afiliación (Amazon/Awin/TravelPayouts)
- El usuario trae una idea viral tipo "bot que construye webs y genera ingresos" y hay que aterrizarla
- Existe un proyecto de nicho que quiere actualización autónoma nocturna con informe Telegram

Clase de proyecto: web estática de nicho con contenido basado en **fuentes oficiales citadas**, enlaces de afiliado, deploy a GitHub Pages y cron nocturno de vigilancia que actualiza y reporta por Telegram. Ejemplo real: Kit72h (Ntizar/Kit72h). Detalle del caso: `references/kit72h-caso.md`.

## Flujo validado

1. **Elegir nicho**: priorizar (a) fuente de verdad oficial citable (UE, Protección Civil, BOE...) que blinde contra desindexación de contenido AI, (b) intención de compra rápida (ticket bajo, conversión alta), (c) baja competencia seria en castellano. Evitar pSEO genérico con plantillas — las Core Updates 2026 de Google desindexan contenido sin datos únicos.
2. **Verificar nombre/dominio ANTES de casarse con él**: comprobar disponibilidad por DNS: `nslookup -type=NS dominio.es` → si devuelve nameservers está ocupado; si no, probablemente libre (verificar luego en registrador). Probar 15-30 candidatos en un bucle. El usuario compra el dominio con sus datos; mientras tanto, `usuario.github.io/repo` funciona y se migra a dominio custom después.
3. **SPEC antes que código** (skill `project-spec-workflow`): alcance, pantallas, non-goals, human loop con preguntas estructuradas (nicho, monetización, automatización, nombre).
4. **Contenido en `data/*.json`**: kits/listas/productos como datos, no HTML hardcodeado. Cada producto lleva: nombre, `descripcion` útil (para qué sirve de verdad), `precio_aprox` (rango orientativo en €), `prioridad` (esencial/recomendado/extra), `afiliado` (placeholder `AMAZON-URL-*` hasta que el usuario pase enlaces reales). Enriquecer 85 items en un solo script Python con dict de keyword→info, no a mano.
5. **Diseño**: ver sección de estilo más abajo.
6. **Deploy**: GitHub Pages método moderno (`actions/deploy-pages@v4`, skill `github-pages-modern-deploy`). Verificar con `gh run list` + `curl` al URL público (el JSON puede tardar ~20s más que el HTML en estar disponible).
7. **Cron vigilante nocturno**: revisa las fuentes oficiales, busca novedades normativas, actualiza el JSON (solo modificar/añadir, nunca borrar; siempre citar fuente oficial + fecha), commit+push (se despliega solo) e informe a Telegram (cambios o "sin cambios").
8. **Legal obligatorio**: disclosure de afiliado (texto exacto de Amazon) en cada página, `rel="sponsored nofollow noopener"` en enlaces.

## Estilo según tipo de web (preferencia David)

- **Dashboards/herramientas de datos**: fondo blanco, sombras sutiles, azul #2563eb, tipografía compacta (regla clásica de memoria).
- **Webs públicas de nicho "con estilo"**: David pide diseños temáticos potentes — pidió "Mad Max con cobre oxidado, tierra y petróleo + fondo Three.js". Dark theme y temáticas fuertes SÍ valen aquí; la regla anti-dark era para dashboards. Usar tipografía display con carácter (ej. Rubik Dirt), grano de película con blend overlay, salpicaduras/manchas decorativas, fondo 3D animado sutil (dunas wireframe, partículas, cámara que "respira"). Incluir `prefers-reduced-motion` que oculte el fondo 3D y versión print limpia para checklists.

## Pitfalls

- `cp -r carpeta/archivo1 carpeta/archivo2 destino/` aplana: los archivos caen en la raíz de destino, no en su subcarpeta. Usar `cp -r` por carpeta o `mv` después. Causó un deploy con JS perdido.
- Si el push a Pages falla con "Pages not found", crear el site primero: `gh api repos/ORG/REPO/pages -X POST -F build_type=workflow`, luego rerun del workflow.
- Al crear el repo con `gh repo create --source=.`, el primer run de Pages falla si Pages aún no está habilitado — el POST anterior lo arregla.
- `browser_exec` puede colgar el daemon (timeout incluso en `page_info`): para verificar sitios estáticos, `curl` al URL publicado + `node -e` sobre el JSON es más fiable y rápido.
- Enlaces de afiliado: NO inventar URLs de Amazon; dejar placeholder visible y pedir al usuario los enlaces reales (necesita cuenta Amazon Afiliados aprobada con el sitio ya publicado — el contenido primero, la monetización después).

## Búsqueda masiva de URLs reales de Amazon (flujo Kit72h validado, agosto 2026)

Cuando el usuario ya tiene cuenta de afiliados, se puede resolver el paso de enlaces reales sin esperar a que él los busque: localizar producto real en amazon.es (precio en rango, stock, ≥4★), verificar ficha, y entregar Excel para su revisión; el usuario añade su tag y devuelve.

**Método que funciona** (probado en 83/85 productos):
- **curl directo a amazon.es con cookie jar** es la vía principal: `curl -s --compressed -L -c cookies.txt -b cookies.txt -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36' 'https://www.amazon.es/s?k=<query+url-encode>'`. Claves: `--compressed` (la respuesta viene gzip, sin esto no se parsea), cookie jar persistente, y en 503/captcha → reintentar con jar nuevo o pausa (captchas intermitentes en ~2 fichas por lote).
- Extraer de resultados: ASIN (`dp/XXXXXXXXXX`), título, precio (`a-offscreen`), valoración. Filtrar por rango de precio del producto y ≥4★. **Verificar cada ficha final** con fetch directo a `dp/ASIN`: HTTP 200 + buybox + título/precio extraídos de la página propia. Marcar `verificada: extraccion` (buybox confirmado) vs `verificada: busqueda` (solo vía búsqueda).
- web_search con `site:amazon.es` funciona como descubrimiento alternativo pero es lento; curl es ~15x más eficiente. Un subagente llegó al cap de guardrail con 50 web_search repetidas — indicar límite ~15 en el prompt.
- **Paralelizar por lotes de ~17 productos con delegate_task** (5 lotes = 85 productos, ~12 min total). Rate limit del proveedor puede truncar subagentes: al consolidar, verificar SIEMPRE los ficheros de salida en disco (no confiar solo en los resúmenes) y relanzar los lotes ausentes/truncados.
- Si un subagente falla y no escribió salida, relanzarlo con el **método concreto probado incluido en el contexto** (curl + --compressed + cookie jar) — el genérico "usa web_search" lleva al guardrail.
- Fichas de verificación y HTML temporales del scraping: no commitear; `.gitignore` con patrones `ck_*`, `*.html` de trabajo, cookies.

**Productos N/A razonables**: medicamentos OTC (paracetamol — restricciones Amazon), efectivo, libros genéricos. Marcarlos 'N/A — no aplica' y en la web van como nota informativa sin enlace.

**Excel de handoff**: 2 hojas (Productos con columnas Nº/Kit/Sección/Producto/URL Amazon/Precio real/URL con TU afiliado (rellenar)/Notas + Leyenda con instrucciones), freeze panes, autofilter. El usuario rellena su columna o da el tag y se aplica programáticamente. Guardar el Excel y los lotes en el repo como fuente de verdad del trabajo.

Ver `scripts/scraper-amazon-fichas.py` (patrón reutilizable del scraper).

## Referencias

- Estructura de referencia: `index.html` + `css/styles.css` + `js/{state,ui,main,fondo}.js` + `data/kits.json` — un archivo = una responsabilidad.
- Repos ejemplo del usuario: `~/Projects/kit72h` (Ntizar/Kit72h), fuente de datos UE = Estrategia de Preparación JOIN(2025) 90; ES = proteccioncivil.es/gestion-riesgos/recomendaciones.
- `references/scraper-amazon-fichas.md` — método curl probado para buscar y verificar fichas de amazon.es (ASIN, precio, buybox), cuando hay que resolver URLs de productos reales.
