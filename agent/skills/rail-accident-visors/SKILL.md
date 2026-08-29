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
- Algoritmo: normalizar PK (`368+925`, `P.K. 429,825`) y línea (`100 Hendaya a
  Madrid`) → tramos del mismo `cod_eje` cuyo rango pki-pkd contenga el PK →
  interpolar sobre la geometría. Cadena: PKTeoricos exacto → interpolación → Nominatim.
- **Pitfall:** `id_provinc` llega como número (2, no "02") → `str(v).zfill(2)`
  antes de cruzar con el catálogo INE, o el matching de provincia falla al 100%.
- Resultado ES: 215/318 informes clavados en el trazado; auditoría: 250 bien,
  31 duda, 23 mal — los malos son informes sin PK interpolable ("CIM-Aguja km 337,1").

## Datos del dominio

- Excel eRAIL (~4.000 inv × 64 cols): la columna "Investigation report" está vacía
  (4.033/4.067) — los PDFs viven en la web, no en el Excel.
- ES: 374 PDFs 2006-2025, 269 informes CIAF verificados (importables como base rica).
- PK de informes: `20+350`, `P.K. 429,825`, `5/350`, `11,907`. Líneas: `010 Madrid
  Puerta de Atocha - Sevilla Santa Justa`.

## Diseño del visor (preferencias duras de David)

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

## Lecciones de proceso

- Un solo proceso background a la vez (dos LLM estructuradores colisionan en escrituras).
- La API de NaN da errores 524: reintentar 3 veces con sleep; es tiempo, no fallo.
- Cuando el usuario dice "no están bien localizados", no retocar casos sueltos:
  construir el auditor (distancia a vía + provincia) y corregir por clase de fallo.
- Todo proyecto necesita README con estructura, pipeline ordenado, schema y reglas —
  el usuario lo pide explícitamente para que el vibe-coding no se pierda.
