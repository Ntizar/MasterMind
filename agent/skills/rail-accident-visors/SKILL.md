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
7. `revisar_localizacion.py` — auditoría estricta: (a) **distancia GEOMÉTRICA a las
   polilíneas de los tramos ADIF** (no al marcador PKTeoricos más cercano — los
   marcadores son escasos: portal de túnel, tramo largo… y provocan falsos dudosos;
   caso real Álora 111/2024: coord a 0 m de la línea 030 declarada pero a 501 m del
   marcador de su tramo → "duda" falsa; el proxy de marcadores se conserva solo como
   diagnóstico `dist_via_m`) Y (b) **cruce PK↔línea**: el veredicto lo manda la
   distancia geométrica a la línea DECLARADA — si cae sobre otra vía, será grande.
   (c) **nodo de estación ≠ otra vía**: la geometría de tramos solo tiene el EJE en
   línea, no el manojo de vías del recinto. `metodo_geo=estacion_ign` + vía más
   cercana = línea declarada + d ≤ ESTACION_RADIO (1200 m) → 'bien' (caso Manresa
   70/2022: 604 m de SU línea 220, dg == dgl — el motivo 'OTRA vía' era mentira).
   Señal de falsos positivos del auditor: `dist_via_geo_m == dist_linea_geo_m`. Solo (a) es ciego al peor bug posible — Caleyo
   (Oviedo) caía sobre otra vía lejana y el auditor lo marcaba "bien" durante ciclos
   enteros. Además: provincia declarada vs INE (con alias de cabecera Oviedo→Asturias,
   Santander→Cantabria y denominaciones antiguas Gerona→Girona, Lerida→Lleida; y
   candidatas múltiples si raíz y ubicacion declaran líneas distintas). Salida
   `data/revision/`.
   **PITFALL "misma_linea" demasiado estricto (2026-09):** un punto por ESTACIÓN puede ser
   correcto estando sobre la red, aunque la distancia a la línea DECLARADA sea grande. Si la
   línea declarada es un ramal interno o se trunca en ADIF, `dgl` engaña: Salou (pk 263 línea
   600 — ADIF la trunca en pk 254) o Zaragoza-Delicias (ramal 060 sin geometría) se marcaban
   "duda" con el punto correcto a 11 m de la vía real. Regla fijada: **si `metodo_geo` es
   `estacion_*` y `dg` (dist a la vía real MÁS CERCANA) ≤ ESTACION_RADIO → "bien"**, aunque
   `dgl` sea grande. El matcher estricto de estación garantiza que el punto por estación es el
   correcto por construcción; el cruce de línea declarado pasa a ser una etiqueta, no un error.
8. `revisar_json.py` — revisor IA: revalida cada json contra su .md y corrige campos mal interpretados en sitio, con log de cambios. Determinista primero (fechas vacías, formatos), LLM después.
9. `consolidar.py` — json/*→data/db/ con **dedupe BIDIRECCIONAL por expediente**: un solo
   registro por expediente; gana quien tenga análisis (v3/hechos), empate → CIAF; el
   perdedor aporta los campos que falten (lista amplia: v2, resumen, causa, tags, trenes,
   entidades, geo...). El dedupe de un solo sentido ("CIAF gana si llega después") deja
   duplicados cuando el orden de ficheros varía — 71 duplicados en producción.
   Propagar `metodo_geo` al registro final. **CRÍTICO — orden de escritura:** cualquier
   normalización de campos DEBE ejecutarse ANTES de `write_text(reports/XX.json)`;
   normalizar después de escribir no cambia nada en disco (bug real que costó varias
   rondas de debugging).
   **CRÍTICO — index fantasma:** el merge del `index.json` NO puede ser acumulativo
   (`merged = index` + overlay). Tras archivar duplicados, el país re-consolidado hay
   que REEMPLAZARLO entero (conservar solo claves de OTROS países) o el índice conserva
   registros muertos — 619 entradas para 349 informes en producción, y el frontend los
   renderiza con strings 'None'. Verificar siempre `len(index)` == nº de informes.
   **Autoridad de campos:** las `consecuencias` del análisis v3 MANDAN sobre el JSON
   base (`fallecidos`, `heridos_graves`, `heridos_leves`) para TODOS los registros —
   la primera pasada sistemáticamente deja víctimas a 0 en informes recientes y el
   usuario lo detecta en el gráfico de evolución ("seguro que no hay fallecidos desde
   2014?"). Igual criterio: `fecha` = fecha del SUCESO, no del informe ni del
   expediente ("lo importante de la fecha es cuando ocurre el siniestro").
   **Prioridad geo:** en `pk`/`linea`/`provincia`, el bloque `ubicacion` verificado por
   el geocodificador MANDA sobre los campos raíz del LLM (raíz tenía '244' erróneo y
   ubicacion '422' correcto en Pedrera; al revés que las víctimas, donde v3 manda).
10. `extraer_completo.py` — **extracción v3 profunda** (ver `references/extraccion-v3.md`): análisis IA de TODO el informe → cronología minuto a minuto, infraestructura, personal, causas (directa/contribuyentes/sistémicas), lecciones, recomendaciones con destinatario, idioma_original. Antes: `limpiar_md()` elimina el índice del .md (líneas con puntos de relleno `..... 12`) — sin esto el índice acaba colado en el campo "descripción" y el usuario lo detecta al instante.
11. `verificar_todo.py` — **comprobación integral reutilizable** (pdfs↔md↔json↔DB, dupes md5, magic bytes, fantasmas, 1-registro-por-expediente, coords gemelas, veredictos del auditor, cache-busting) → `data/revision/XX-verificacion.md`. `--limpiar` archiva duplicados md5 a `_duplicados_descartados/`; exit ≠ 0 si hay ERROR (apto como gate en cron). Su 1ª pasada encontró **3 duplicados que la limpieza manual previa dejó pasar** — la comprobación debe ser script fija, no lista ad hoc por sesión. Ver `references/comprobacion-integral.md`.

**ORDEN crítico de la fase 8-11 (ida y vuelta obligatoria):** el auditor `revisar_localizacion.py` lee las coords de la DB generada → debe correr DESPUÉS de `consolidar.py`; y `consolidar.py` propaga `geo_veredicto`/`geo_motivo` del auditor a cada registro → tras consolidar hay que **re-auditar y re-consolidar** hasta que las cifras del verificador cuadren. Secuencia estable: geocodificar → consolidar → auditar → consolidar → verificar_todo.

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
- **CAUSA RAÍZ del bug Caleyo (estructura codtramo):** el `codtramo` ADIF es
  `eje(2)+línea(3)+seq(4)` (9 dígitos) — el código de línea CIAF vive en
  `codtramo[2:5]`, NUNCA en `codtramo[:3]`. Indexar tramos/pk por `[:3]` hace que
  la línea 130 (Gijón–Venta de Baños) case con el eje '061' (Teruel–Sagunt) y
  accidentes asturianos aterricen en Guadalajara. Al buscar por línea, usar el
  prefijo numérico de `cod_linea` ('130-Gijón...' → '130') Y `codtramo[2:5]` como
  claves del índice (un tramo puede pertenecer a ambas vistas).
- **id_provinc del GeoJSON ADIF = código INE** (verificado: Guipúzcoa→20, Cuenca→16,
  Jaén→23, Palencia→34). Cualquier mapa propio IDP→provincia hay que validarlo contra
  un tramo conocido ANTES de fiarse — el que había estaba desplazado y filtraba por
  provincias equivocadas en silencio. 93 tramos tienen `idp=0`: resolver su provincia
  vía texto `provincia` del tramo (con alias) o, en PKTeoricos, vía su `codtramo` →
  tramo → provincia.
- **La ruta PK-sin-línea no debe depender de la coord previa** para elegir match:
  una coordenada previa errónea se auto-perpetúa (el filtro de cercanía descarta el
  candidato correcto). Filtrar por pk+línea+provincia primero y solo usar la coord
  vieja como desempate entre varios matches válidos.
- **El reintento SIN la provincia declarada debe ejecutarse de verdad**: en
  `geocodificar_via.py` el fallback «línea+PK ignorando provincia» vive en una cadena
  `if/elif` y, si queda detrás del `elif` que consume el fallo con provincia, es
  INALCANZABLE — el script sale 0 y la coord ni se mueve (silencioso). Después de
  tocar la cadena, verificar que la coord del registro objetivo CAMBIÓ, no solo el
  exit code. Caso real 64/2012: el CIAF declara «Huesca» pero Villanueva de Gállego
  es ZARAGOZA; los tramos 200 de Huesca no cubren el PK 25 y solo el match sin
  provincia clava el punto correcto (interpolación sobre el tramo de la 200).
  La provincia de un informe CIAF puede ser simplemente errónea: ante conflicto
  provincia-vs-geometría, manda la línea+PK.
- **parse_linea:** tolerar prefijo 'Línea ' de los CIAF ('Línea 130 ...' — sin ello
  el registro cae a la ruta buggy), códigos LV de 4 dígitos ('9502' alta velocidad),
  y zfill solo para ≤3 dígitos (no corromper los LV). **PROBLEMA+fix (2026-09):** muchos
  informes escriben la línea SIN código numérico ('Valencia - San Vicente de Calders')
  y `parse_linea` devuelve None → el geocodificador no puede casar por línea y caía al
  fallback por provincia, aterrizando en OTRA línea (caso 34/2007 → pk 244,350 cruzado
  a la línea 200 en Zaragoza). Fix: si `parse_linea` no da código, **recuperarlo del
  texto del informe** (erail `Location name`/título/resumen) con regex
  `\(\s*(\d{3})\s*[A-Za-z]` ('(600 Valencia-... railway line)') → interpolación por
  línea correcta.
- **PROBLEMA id_provinc=0 en PKTeoricos (bug de clase, 2026-09):** los PKTeoricos de
  líneas correctas a menudo traen `id_provinc=0` (provincia sin resolver en INE). El
  filtro `if idps and to_int(idp) not in idps: continue` los EXCLUÍa TODOS → match
  vacío → se conservaba la coord previa stale/errónea (34/2007 en Zaragoza). Fix:
  **solo excluir provincias CONOCIDAS distintas** — `if idp not in (None,0) and idp not in idps: continue`.
  Así `id_provinc=0` (válido) deja de ser descartado y el PK correcto de la línea entra.
- **Directiva del usuario (2026-09): snap a estación/población nombrada — PERO con matiz de
  precisión.** Si el título/ubicación nombra la estación, David quiere el pin en ella ("si el
  título tiene el nombre de la estación ponlo en la estación... no es tan difícil. O si aparece
  la población"). Para la clase, snap a la estación cuando la ubica CLARAMENTE.
  **PELIGRO — no hacer auto-snap masivo por nombre desde el TÍTULO:** los títulos llevan la
  ruta completa del tren ("Madrid Chamartín", "Intermodal Abando Indalecio", "San Vicente",
  "Sevilla-Santa Justa") → un match por substring devuelve cientos de falsos positivos
  (barrido real: 248 de 276 candidatos eran espúreos). Implementación SEGURA: snap SOLO desde
  el campo `estacion` explícito o el patrón de ubicación oficial del eRail `Location name`
  ("in the vicinity of X" / "en la estación de X"), con match estricto por PALABRA COMPLETA
  (no substring) y desempate por el patrón de ubicación, no por longitud del nombre.
  **Matiz de precisión:** cuando el informe tiene PK+línea resoluble, la interpolación sobre
  la vía GANA — David eligió "precisión sobre la vía" para el 34/2007 aun estando el punto a
  ~17 km de la estación nombrada; el snap a estación es el fallback/cuando la ubica claramente.
- **`metodo_geo="poblacion"` es legítimo → hay que enseñárselo al AUDITOR (2026-09).** Cuando
  la línea declarada NO existe en la geometría ADIF (p.ej. la CIAF escribe "510 Aljucén-Cáceres"
  pero ADIF solo conserva 1 tramo de esa línea en otra zona, pk 140-142) y la estación no está
  mapeada (Carmonita ni en el cache IGN de 2.000 ni en OSM), el punto correcto es la POBLACIÓN
  declarada (regla de David): geocodificar el municipio vía Nominatim y escribir
  `metodo_geo="poblacion"`. OJO: el auditor `revisar_localizacion.py` mide distancia a la línea
  y marca esos puntos como "mal" porque un centro urbano no cae sobre un raíl — hay que añadir una
  regla al auditor (`if metodo_geo.startswith("poblacion"): veredicto="bien"`, con `motivo`
  "ubicación por población declarada; sin geometría de línea en ADIF"). Sin eso, el informe de
  verificación listará la población como error indefinidamente. **NO "snap a la línea ADIF más
  cercana"** — junto a Carmonita la ADIF más cercana es la 026 Plasencia, NO la 510: el pin dejaría
  de estar en la localidad declarada y seguiría "mal" (además en la vía equivocada). Errores cross
  reales fijados así esta sesión: 49/2010→Carmonita (estaba en Zafra a ~55 km) y 4/2016→Elx-Parc
  (estaba en Sabadell-Parc del Nord/Barcelona por falso match de substring "Parc").
- **Pitfall reproducción del geocodificador (diagnóstico):** `idps_de` y `puntos_pk` están
  ANIDADAS en `main()` — al importar `geocodificar_via` no se exponen; `g.idps_de(...)`
  devuelve `None` y enmascara que `idps` en realidad es `[43]` (Perdí 2 rondas de repro por
  esto). Para reproducir la lógica hay que replicar `idps_de` inline. El observador DEFINITIVO
  de un cross-line es inspeccionar los PKT (o tramos) candidatos con `pk±tol` y ver su
  `id_provinc`/`codtramo[2:5]` — un punto de la línea correcta puede venir con `id_provinc=0`
  y es justo el que el filtro excluía (caso 34/2007).
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
  **Cache del dataset:** copiar las 2 páginas del FeatureServer a `data/ign-estaciones*.json`
  y leer de ahí — si solo viven en `Temp`, se pierden entre sesiones y el script
  muere (el arreglo de Caleyo se bloqueó una sesión entera por esto).
- **Sistema de comprobación integral** (pdfs↔md↔json↔DB, fantasmas, hash dupes):
  ver `references/comprobacion-integral.md`.
- **Pitfall verificación:** tras cada pasada nueva, releer la auditoría completa
  — una corrección por clase puede introducir una clase de error nueva (la 1ª
  pasada de estaciones metió 45 "mal" antes de detectarse).
- **Los `mal` del auditor se clasifican solos**: coord fuera de vía real vs "pegado a
  vía pero línea no cuadra" (PK ambiguo entre líneas / error de dígito del LLM en la
  línea raíz). Para cada `mal`, mirar las líneas de los tramos a <1 km de la coord —
  si una es pariente de la declarada (244 vs 422 Pedrera: transposición), es ruido del
  auditor o del parser, no un re-geocodificado. No re-geocodificar a ciegas.
- **Recintos sin geometría propia (cambiadores de ancho, clasificaciones)**: ramales
  de servicio como `060 Bifurcación Cambiador Zaragoza-Delicias…` a veces NO tienen
  tramo en `adif-tramos.geojson`; el punto correcto (el cambiador, a 11 m del recodo
  enlazado a la 200) sale como 'OTRA vía' porque la línea declarada está a 1.4 km.
  Señal: distancia global tiny (≤50 m) y la línea cercana es la matriz de la declarada
  → ubicación BUENA; documentarlo en `fuente_geo` del JSON, no mover la coord.
- **Ronda final de residuos = uno a uno con evidencia, no otra pasada de pipeline.**
  Cuando quedan pocos casos (`son pocos, puedes comprobarlo` — el usuario lo exige así):
  por registro (1) abrir su JSON y el PDF fuente (PyMuPDF `fitz` si pypdf falla) y sacar
  textualmente municipio, origen-destino del tren y PK; (2) localizar el punto EXACTO en
  OpenStreetMap vía Overpass (`nwr["railway"~"station|halt"]["name"~"…",i](bbox)` con
  urllib POST, o Nominatim para localidades) — el `name` del nodo confirmado en la
  respuesta cuenta como verificación; (3) escribir lat/lng en el JSON con
  `metodo_geo="estacion_adif"` y `fuente_geo` citando el `node/<id>` OSM (trazable,
  CC BY 4.0); (4) relanzar revisar→consolidar→verificar y contestar con
  zona+origen/destino+PK+coordenada POR CASO, no con estadísticas del lote. NUNCA
  escribir una coord de memoria sin haberla visto en la respuesta del servidor.
  Si Overpass no devuelve el nombre exacto (clasificaciones/yards sin etiquetar),
  ensanchar bbox y quitar el filtro `railway`, y como último recurso usar el punto del
  eje ADIF interpolado por PK y declararlo en `fuente_geo`. Receta completa con consultas
  Overpass/Nominatim y nodos ya verificados: `references/verificacion-puntual-osm.md`.
- **Pitfall al corregir JSON en lote por nombre de fichero:** `glob.glob('json/ES/*.json')`
  con stems que llevan corchetes literales (`ID-211207-290408-CIAF[1].json`) no casa —
  `[1]` es una clase de caracteres del glob. Usar `os.listdir` + substring del basename,
  o `glob.escape`.
- Resultado ES con auditor estricto sobre 349 limpios (post-dedupe): ~294 bien, 0 mal
  tipo Caleyo, ~47 sin geo legítimos (informes sin PK ni estación). Las cifras exactas
  cambian por pasada — lo que importa es que ningún `bien` sea un cross-line.

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
- Filtros de la taxonomía IA en el sidebar + **filtro por entidad implicada** (ADIF,
  Renfe, FEVE... — petición literal: "quiero que las entidades también sean un filtro";
  select aparte que combina con el resto de filtros) + búsqueda que cubra precursores
  ("somnolencia", "alcoholemia") + export Excel siempre visible.
- **Los mal geolocalizados deben ser VISIBLES en el visor, no solo en informes internos**
  (petición literal: "ES importante que en informes salgan los que no están bien
  geolocalizados"). Patrón verificado: el auditor emite `geo_veredicto` + `geo_motivo`
  legible ("cae sobre OTRA vía: la declarada 622 está a 21884 m"), `consolidar.py` los
  propaga a cada registro DB, y el frontend los expone por triple vía: select de filtro
  (mal/duda/sin coords/bien), badge `⚠ ubicación` en la tabla + banner en la ficha, y
  `dashArray` con contorno rojo `#dc2626` en el circleMarker del mapa.
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
- **Auditar los residuos ANTES de darlos por perdidos**: los registros "sin análisis"
  resultaron ser 3 duplicados mal cruzados de un import viejo (títulos/resúmenes de
  OTRO suceso: expediente 402/2013 con resumen de 2008), 1 fallo transitorio de API
  (el HTTP 400 "persistente" pasó al reintentar con `--solo`), y 1 PDF no descargado
  (re-scrape pendiente). Nunca borrarlos del repo: moverlos a `json/ES/_duplicados_descartados/`.
  Para reintentar un único informe, flag `--solo <stem>` en extraer_completo (mejor que
  hacks de `exec()` que rompen indentación).
- Cuando los totales no cuadran con lo esperado (ej. 0 fallecidos post-2014 en un
  gráfico), cruzar SIEMPRE el campo DB contra el texto fuente (hechos/resumen) con un
  extractor determinista; si el texto dice una cifra y la DB otra, el análisis v3
  profundo suele tener la razón — propagarlo, no re-extraer.
- **"¿Y después de X no hay nada?" (vacíos en series temporales):** verificar contra
  la FUENTE OFICIAL completa, no solo contra los informes que ya tienes. Las tablas
  oficiales por año de la web del CIAF (`infofin-AAAA`) listan expediente/fecha/provincia/
  tipo y son el listado maestro para cruzar cobertura: la DB debe tener EXACTAMENTE los
  mismos expedientes que la web, ni uno menos (un faltante real ahí = PDF publicado
  después del último scrape; su link directo está en la tabla oficial, no en el scrape
  de ERA). La conclusión "0 fallecidos" puede ser verdad — demostrarla con el cruce,
  no asumirla.
- **Limpieza de la colección json/* (cuando el usuario pide "limpiar y quedarnos
  con los buenos"):** clasificar por (a) con v3 = buenos, (b) sin v3 = candidatos a
  residuo. Antes de archivar cualquier grupo, verificación programática de 0 pérdidas:
  para cada candidato, contrastar TODOS sus campos no vacíos contra el registro DB de
  su expediente y abortar si el ganador carece de alguno. Solo entonces mover a
  `json/ES/_duplicados_descartados/` (NUNCA borrar). Resultado esperado: colección
  base == nº de informes con v3 (uno a uno, sin humedad).
- **Descarga de PDFs de transportes.gob.es:** el User-Agent simple tipo pipeline
  recibe un HTML "Página web bloqueada" (200 + HTML, NO un PDF). Fix validado:
  UA de navegador completo (`Mozilla/5.0 (Windows NT 10.0... Chrome/126.0 Safari/537.36`)
  + header `Referer: https://www.transportes.gob.es/`. Verificar SIEMPRE el primer
  byte (`%PDF-`) tras descargar: los bloqueos llegan con código 200.
- **PDFs publicados tarde:** un suceso antiguo (2023) puede tener informe publicado
  años después (114/2023 → 09/02/2026). Revisar las tablas `infofin-AAAA` oficiales
  con fecha de publicación, no fiarse solo del año de suceso al buscar novedades.
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
  el usuario lo pide explícitamente para que el vibe-coding no se pierda. **Formato de README
  que funciona (cuando se prepara para escalar a OTROS PAÍSES — 2026-09):** (1) tabla de estado
  ACTUAL con cifras del país (informes, v3, localización auditada, VERSION_DATOS) — no los
  totales de un reporte viejo; (2) árbol del repo con el pipeline EN ORDEN numerado; (3) tabla
  de `metodo_geo` con su fiabilidad; (4) lecciones de geolocalización (los bugs de clase ya
  resueltos); (5) hoja de ruta multi-país y **traducción** — un informe llega en el idioma del
  país y hay que emitir `titulo_normalizado` (es) + `idioma_original`; y (6) **aviso de que la red
  ADIF es SOLO España**: ERA/eRAIL no da coordenadas y cada país nuevo necesita descargar su red
  ferrovia para interpolar, o el matcher de geolocalización no funcionará fuera de ES.
  **Limpieza antes de escalar:** quitar scripts superados (el geocodificador Nominatim
  `geocodificar.py` quedó obsoleto al aparecer `geocodificar_via.py`+`geocodificar_estacion.py`),
  deduplicar docs del repo raíz, mover notas de análisis a `docs/`, renombrar scripts `_archivo.py`
  a nombres claros (`_corrige_estaciones.py` → `corregir_ubicaciones.py`), ampliar `.gitignore`
  (.DS_Store, *.tmp, *.bak, *.log). Verificar con `grep` que nadie referencie los nombres viejos.
  No borrar jamás `_duplicados_descartados/` (evidencia de que no se pierden datos).
