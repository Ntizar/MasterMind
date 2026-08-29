# Extracción v3 profunda — schema y pitfalls de API

## Trigger (feedback del usuario)

Al revisar el visor: fichas desiguales — unas ricas, otras con el ÍNDICE del PDF
dentro del campo descripción ("HECHOS INMEDIATOS DEL SUCESO ........ 6") y títulos
en inglés sin tratar. Respuesta: pipeline v3 que extrae TODO lo posible de cada PDF.

## Schema v3 (json/{pais}/v3/{id}.json)

- `titulo_normalizado` (es, breve) · `idioma_original` · `resumen` (3-5 frases)
- `hechos` — narrativa del suceso, NUNCA el índice (validador: rechazar si contiene
  `\.{4,}` o >40 líneas)
- `lugar` {tipo: plena_via|estacion|apartado|taller, estacion, pk, linea, provincia, descripcion_lugar}
- `cronologia` [{hora, evento}] — minuto a minuto cuando el informe lo da
- `trenes` [{numero, tipo, operador, danos}] · `personal` [{rol, implicacion}]
- `infraestructura` {senalizacion, tipo_via, velocidad_maxima, ancho, electrificacion, estado_via, otro}
- `material_rodante` {series, averia, mantenimiento} · `clima`
- `causas` {directa, contribuyentes[], sistemicas[]}
- `consecuencias` {fallecidos, heridos_graves, heridos_leves, danos_materiales, afectacion_servicio}
- `lecciones[]` · `recomendaciones` [{texto, destinatario}] · `tags[]` (5-12, minúsculas)
- Anti-invención: dato no presente en el texto → null / []. Reanudable: salta v3 existentes.

## Limpieza del .md (antes del LLM)

Regex índice: `\.{4,}\s*\d{0,4}\s*$` fuera; páginas sueltas `^\s*\d{1,3}\s*$` fuera;
colapsar 3+ vacías. Ventana de texto: cabeza 18k + cola 6k chars.

## Pitfalls NaN API con qwen3.8-flash y schemas JSON grandes (los 3 fallos reales)

1. **`PROMPT.format()` + schema con llaves = KeyError** (`'\n "titulo_normalizado"'`).
   Si el prompt lleva el schema JSON literal, NO usar `.format()`: usar
   `PROMPT.replace("{texto}", ...).replace("{pista}", ...)`. El error no menciona
   "format" — parece un fallo del LLM; es de la plantilla.
2. **Tokens de razonamiento**: qwen3.8-flash gasta 800-1900 tokens "pensando"
   (`reasoning_tokens`) antes del JSON y lo corta a mitad de clave. Poner
   `/no_think` al inicio del prompt y `max_tokens: 8000`.
3. **Parseo tolerante**: quitar `<think>...</think>`, fence ```json, y si
   `json.loads` falla reintentar con `strict=False` (saltos de línea sin escapar).

## Limpieza de coordenadas heredadas (auditoría → corrección)

Cuando `revisar_localizacion.py` marca informes como "mal" y son coordenadas viejas
de Nominatim/LLM (fallan mejor que un error de red: p.ej. "Madrid" → cae en León),
el re-geo no los toca porque respeta coords previas. Procedimiento: limpiar
`lat/lng/metodo_geo` de los json fuente con veredicto "mal" que NO tengan
`metodo_geo` empezando por `via_`, luego re-geolocalizar y consolidar.
Resultado real: 23 mal → 1.

## Cifras de la corrida ES (2026-08-29)

426 informes en DB · 316 bien localizados · 372/374 enriquecidos v2 · revisor IA:
2.413 correcciones en 370 JSON · 1 informe sin md por OCR pendiente
(`ID_230507_140907`).

## Corrida v3 completa y fusión en DB (2026-08-29, cierre)

- Resultado: **364/374 v3 generados**; 6 fallos (mezcla de HTTP 524 y parseo) —
  **reanudable**: relanzar el mismo comando regenera solo los que faltan.
- Los "omitidos" (~270) son jsons base sin .md propio: duplicados CIAF ya cubiertos
  por otro nombre de fichero; su v3 llega vía fusión en consolidar, no hay que
  forzarlos.
- **Fusión en `consolidar.py`**: cada registro base recibe `resumen` (fallback al
  de v3), `hechos` y el objeto `v3` completo; en el dedupe por expediente la
  fusión CIAF-gana también arrastra el `v3`. Resultado: **346/426 registros con
  análisis v3 en DB** (los CIAF duplicados heredan el v3 del json del mismo
  expediente).
- **Peso de la DB**: con los textos v3 la DB pasó de 2,0 MB → 4,9 MB. GitHub
  Pages aún lo traga; si al añadir países (DE = 452 PDFs) se dispara, mover los
  textos largos (hechos/cronología) a ficheros `.md` por informe y servirlos bajo
  demanda — la DB plana guarda solo el resto.