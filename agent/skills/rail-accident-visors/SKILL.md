---
name: rail-accident-visors
description: "Use when building train-accident visors (ERA/eRAIL, CIAF)."
version: "1.0.0"
tags: [railways, accidents, era, erail, adif, geolocation, visor, pipeline]
---

# Rail Accident Visors — pipeline y diseño de visores de accidentes ferroviarios

Patrones verificados en CIAF-visor y era-visor (Ntizar). Para scraping de fuentes
gubernamentales españolas en general y parsing PDF ver el skill
`government-data-pipelines` (user-owned: leer, no editar) — este skill añade lo
específico del dominio ferroviario europeo y las preferencias de diseño del usuario.

## Pipeline por país (reanudable, un comando por fase)

1. `scrape_pais.py` — descubre informes en ERA. Listado: `https://www.era.europa.eu/era-folder/{COD}-investigations`; páginas de año `/era-folder/{YYYY}-{N}`. **Nunca `rel=next`** (el book Drupal global cuela otros países).
2. `descargar_pdfs.py` — cortesía 8s; ante 429 backoff 120s×intento. 374 PDFs ES, 0 fallos.
3. `extraer_pais.py` — PDF→md con PyMuPDF; los escaneados quedan "pendiente OCR" y se contabilizan (no se inventa texto).
4. `estructurar_pais.py` — md→json con qwen (NaN API): prompt anti-invención, víctimas SIEMPRE del Excel eRAIL.
5. `enriquecer_ia.py` — segunda pasada LLM añade taxonomía v2 (subsistema, ATP ASFA/ERTMS/LZB, tipo_red, explotación, precursores, mitigaciones, factores humanos, meteorología). Lee el .md completo (cabeza 8000+cola 8000).
6. `geocodificar_via.py` — PK+línea → punto SOBRE la vía (ver abajo).
7. `revisar_localizacion.py` — auditoría: distancia al PK ADIF más cercano (bien <500m / duda <2km / mal) + provincia declarada vs INE del PK cercano. Salida `data/revision/`.
8. `revisar_json.py` — revisor IA: revalida cada json contra su .md y corrige campos mal interpretados en sitio, con log de cambios. Determinista primero (fechas vacías, formatos), LLM después.
9. `consolidar.py` — json/*→data/db/ con dedupe por expediente: **CIAF (verificado) gana, pero los campos v2 del LLM se FUSIONAN** si faltan en el CIAF. Propagar `metodo_geo` al registro final.
10. `extraer_completo.py` — **extracción v3 profunda** (ver `references/extraccion-v3.md`): análisis IA de TODO el informe → cronología minuto a minuto, infraestructura, personal, causas (directa/contribuyentes/sistémicas), lecciones, recomendaciones con destinatario, idioma_original. Antes: `limpiar_md()` elimina el índice del .md (líneas con puntos de relleno `..... 12`) — sin esto el índice acaba colado en el campo "descripción" y el usuario lo detecta al instante.

## Profundidad uniforme (feedback duro del usuario)

"Hay incidentes con mucha información y otros con muy poca o desordenada. Si no somos
capaces de hacerlo bien para España no seremos capaces para Europa." El schema mínimo
(tipo/fecha/pk/resumen) NO basta: cada registro debe llevar la extracción v3 completa.
Títulos en inglés sin normalizar también rechazados → `titulo_normalizado` en castellano
+ `idioma_original`. Ver `references/extraccion-v3.md` para el schema y los pitfalls de
la API (formato vs llaves, tokens de razonamiento, parseo tolerante).

## Geolocalización sobre la vía (la clave de la calidad)

- WFS IDEADIF: `https://ideadif.adif.es/gservices/Tramificacion/wfs` — capas
  `Tramificacion:PKTeoricos` (~17.200 puntos sobre vía, con `codtramo`, `pk`,
  `id_provinc`) y `Tramificacion:TramosServicio` (1.178 tramos: `cod_eje`,
  `pki`/`pkd`, geometría). Descargar ambos a disco (~20 MB), trabajar local.
- Algoritmo: normalizar PK y línea → tramos del mismo `cod_eje` cuyo rango
  pki-pkd contenga el PK → interpolar sobre la geometría. Cadena: PKTeoricos
  exacto → interpolación → estación IGN → Nominatim.
- **Pitfall parse PK:** cubrir TODAS las notaciones en una sola regex con
  separadores `[+,./]` — la barra `/` es notación CIAF (`124/573` = 124,573 km)
  y sin ella ~14 informes por tanda se quedan sin geocodificar. Anclar con
  `(?!\d)` tras los decimales, no con `$` (los PK suelen llevar texto detrás).
- **Geocodificación por estación IGN** (`geocodificar_estacion.py`): dataset
  `RedFerrocarrilesIGN` FeatureServer (services1.arcgis.com/nCKYwcSONQTkPA4K,
  ~3.000 estaciones, CC-BY) para informes sin PK casable pero con estación.
  **Pitfall matcher:** NO casar por contención de substring (`n_est in e["norm"]`)
  ni elegir el primer candidato — "León" cae dentro de nombres ajenos y todo el
  lote acaba en un mismo punto falso. Reglas: coincidencia exacta, o contención
  de PALABRA COMPLETA (`len>=4`, todas las palabras presentes), desempate por
  provincia INE, y ABSTENERSE si queda más de un candidato (mejor sin coordenada
  que mal puesta; `metodo_geo="estacion_ign"` para poder deshacer por clase).
- **Pitfall verificación:** tras cada pasada nueva, releer la auditoría completa
  — una corrección por clase puede introducir una clase de error nueva (la 1ª
  pasada de estaciones metió 45 "mal" antes de detectarse).
- Resultado ES final: 361 bien / 29 duda / 1 mal / 35 sin coords (sobre 426);
  los "sin coords" son informes que no mencionan ni PK ni estación — no inventar.

## Datos del dominio

- Excel eRAIL (~4.000 inv × 64 cols): la columna "Investigation report" está vacía
  (4.033/4.067) — los PDFs viven en la web, no en el Excel.
- ES: 374 PDFs 2006-2025, 269 informes CIAF verificados (importables como base rica).
- PK de informes: `20+350`, `P.K. 429,825`, `5/350`, `11,907`. Líneas: `010 Madrid
  Puerta de Atocha - Sevilla Santa Justa`.

## Diseño del visor (preferencias duras de David)

- **Mapa base IGN WMTS, NUNCA tiles OSM/CARTO** en proyectos públicos: "hay que usar
  mapas públicos en cosas públicas" (petición literal, 2026-09). IGN base vía
  `https://www.ign.es/wmts/ign-base?...LAYER=IGNBase-gris...&FORMAT=image/jpeg`
  (FORMAT obligatorio o 400) con selector gris/topográfico/ortofoto y atribución
  "© IGN — Instituto Geográfico Nacional (CC BY 4.0)". Detalle en el skill
  `ign-wmts-tiles` (verificado: tile de prueba con curl `file` antes de pushear).
- **Tipos de suceso = las 6 categorías oficiales** (Directiva UE 2016/79 / ERA):
  colisiones, descarrilamientos, accidentes en pasos a nivel, daños a personas por
  material rodante en movimiento, incendios, otros. Los tipos crudos del LLM se
  MAPEAN a categoría (tabla `TIPO_A_CATEGORIA`) y el tipo fino queda como subtipo
  mostrado "Categoría — Subtipo" en ficha; el filtro y el dashboard van por
  categoría. Subdividir está permitido SOLO cumpliendo las 6.
- **Título siempre `IF <código>`** (del expediente, sin ceros: `0041/2014` →
  `IF 41/2014`), con el título descriptivo como subtítulo debajo. El usuario lo
  pidió explícitamente: los títulos largos crudos del parser no valen.
- **Chips/secciones de lista SIEMPRE con su CSS definido**: si renderizas spans
  dentro de un contenedor, verifica que la clase exista en el `<style>` — una clase
  `.detail-tag` sin CSS produce "accidente colisión descarrilamiento" todo pegado
  y "ADIFADIF" (bug visto en producción; patrón: `display:flex;flex-wrap:wrap;gap:6px`
  + spans con border-radius:999px). Al añadir cualquier lista de etiquetas, verificar
  en navegador real, no solo que el JS no falle.
- **Cache-busting en los fetch de la DB**: const `VERSION_DATOS` + `?v=` en cada
  fetch de `data/db/*.json` y hacer bump en cada despliegue de datos. Sin esto el
  usuario ve fichas con datos viejos (navegador cachea el JSON de MBs aunque el
  HTML sea nuevo) y lo reporta como "sigue teniendo errores" — costoso de diagnosticar.
- **Rango de años: DOS tiradores sobre UNA sola barra** (dual-range con fill azul).
  Ni slider único "hasta X" ni dos sliders separados — las dos variantes anteriores
  fueron rechazadas explícitamente.
- Blanco, azul #2563eb, tarjetas con sombra sutil + hover elevación, tipografía
  compacta (labels 10-12px, valores 14-17px). SIN gradientes, SIN border-left en
  KPIs, SIN dark theme, SIN emojis grandes.
- Paleta de charts unificada con el UI (#1e40af→#93c5fd, rojo #dc2626, ámbar #d97706).
- Filtros de la taxonomía IA en el sidebar + búsqueda que cubra precursores
  ("somnolencia", "alcoholemia") + export Excel siempre visible.
- **Ficha de detalle v3**: organizar por bloques del schema profundo (cronología
  minuto a minuto, infraestructura, personal, causas en 3 niveles, lecciones) —
  el usuario espera "toda la información posible dentro de un PDF" por ficha.
  Detalle en `references/extraccion-v3.md`.
- Validación sin navegador: node `new Function` sobre los scripts inline + check de
  ids + `grep` de restos de paleta vieja tras reemplazar el `<style>` (los estilos
  inline del body sobreviven al reemplazo). Detalle completo del sistema de diseño
  y el dual-slider en `references/visor-frontend-design.md`.

## Publicación (GitHub Pages, estructura CIAF-visor)

El usuario publica los visores como CIAF-visor: workflow moderno en
`.github/workflows/pages.yml` (deploy-pages@v4 desde main) + `index.html` en la raíz
del repo con `<meta http-equiv="refresh">` hacia `frontend/index.html`. La DB JSON
estática (`data/db/`, varios MB) se sirve tal cual por Pages.

- **Repo nuevo sin Pages**: el 1er run falla en `configure-pages@v5` con
  "Get Pages site failed... Not Found". `enablement: true` NO sirve (GITHUB_TOKEN sin
  permiso: "Resource not accessible by integration"). Fix validado: `gh api repos/<o>/<r>/pages -X POST -f "source[branch]=main" -f "source[path]=/"`, luego
  `gh api ... -X PUT -f "build_type=workflow"`, y push vacío para relanzar.
- Verificar tras deploy con curl las 4 piezas (raíz, frontend, index.json, reports/XX.json)
  y abrir la URL publicada (read_preview) antes de darla por buena.
- Nota: el skill `github-pages-modern-deploy` es user-owned (leer, no editar) — si esta
  lección debe vivir ahí, pedir `hermes curator adopt github-pages-modern-deploy`.

## Lecciones de proceso

- Un solo proceso background a la vez (dos LLM estructuradores colisionan en escrituras).
- La API de NaN da errores 524: reintentar 3 veces con sleep; es tiempo, no fallo.
- Cuando el usuario dice "no están bien localizados", no retocar casos sueltos:
  construir el auditor (distancia a vía + provincia) y corregir por clase de fallo.
- Antes de diagnosticar un "sigue mal" del usuario, comparar contra la FUENTE: la DB
  desplegada puede estar bien y ser caché del navegador (ver cache-busting arriba).
  Verificación: curl del JSON publicado + mirar el campo concreto — si el servidor
  ya lo trae bien, el fix es de cacheo, no de datos.
- **Derivar v2 desde v3 sin LLM** antes de relanzar enriquecedores: v3 ya lleva
  clima (`clima` → meteorologia) y `causas.contribuyentes` → precursores; con un
  script determinista 103 informes ganaron campos v2 en 0,3s y 0 tokens. El LLM
  (enriquecer_ia) solo para lo que v3 no cubre (ATP, subsistema fino).
- Conservar `metodo_geo` por registro permite DESHACER una pasada entera por
  clase (borrar lat/lng/metodo_geo de todos los `estacion_ign` y rehacer) sin
  tocar el resto — diseñar cada geocodificador con su marca propia.
- Pitfall INE: `id_provinc` del GeoJSON llega como número (2, no "02") →
  `str(v).zfill(2)` antes de cruzar con catálogos, o el matching falla al 100%.
- Confundir repos homónimos (era-visor vs ERAVisor, dos proyectos reales del
  usuario): verificar `git remote -v` y fechas de push antes de asumir cuál es
  "este proyecto" cuando el usuario pega una URL.
- Todo proyecto necesita README con estructura, pipeline ordenado, schema y reglas —
  el usuario lo pide explícitamente para que el vibe-coding no se pierda.
