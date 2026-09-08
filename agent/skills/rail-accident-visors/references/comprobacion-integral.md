# Sistema de limpieza y comprobación (PDFs ↔ md ↔ json ↔ DB)

Verificaciones deterministas para "asegurarse de que todo sea correcto" en un visor
de informes. Cada una detectó un bug real en era-visor (2026-09). Implementadas como
script fija `scripts/verificar_todo.py` (stdlib, exit ≠ 0 si hay ERROR, `--limpiar`
archiva dupes md5 a `_duplicados_descartados/`). Correr en este orden.

**Lección clave:** convertir la comprobación en SCRIPT reutilizable, no en lista ad hoc.
La 1ª pasada del script encontró 3 duplicados (mismo md5 con stems `*_0`/`_ES-2901`) que
la limpieza manual de sesiones previas dejó pasar — la mirada humana reusa categorías,
el script agrupa por hash y no se cansa.

## 1. Integridad 1:1 de la cadena (pdfs ↔ md ↔ json ↔ DB)

```python
pdfs = {splitext(f)[0] for f in listdir(f'pdfs/{cod}')}
mds  = {splitext(f)[0] for f in listdir(f'md/{cod}')}
jsons= {splitext(f)[0] for f in listdir(f'json/{cod}') if no _duplicados}
# huérfanos en cada dirección: pdfs-mds, mds-jsons, jsons-vs-DB
```
- PDF sin json+md: puede ser escaneado pendiente OCR — comprobar si es duplicado por
  hash (ver 2) antes de darlo por pérdida.
- Comparar STEMS, no rutas completas, y excluir directorios `_duplicados_descartados/`
  (helper `vivo(path, dir_base)` = "el path no cae bajo la carpeta de archivo").
- Los stems de los duplicados suelen llevar sufijo (`IF_x_0`, `IF_x_ES-2901`): antes de
  alarmarse por un .md sin json, buscar su twin en la DB por CONTENIDO (título del .md
  dentro de titulo/resumen) — suele ser duplicado ya consolidado, no pérdida.

## 2. Duplicados por hash de contenido (md5 de los PDFs)

Descargas repetidas con sufijos ` (1)`, `[1]` etc. crean entradas gemelas que
el dedupe por expediente no ve si difieren en stem. Agrupar por `md5(bytes)` → si un
grupo tiene >1 stem vivo, archivar los sobrantes (NUNCA borrar) y reconsolidar.
Caso real: 3 grupos `*_0` con su original aún vivo en json/.

## 3. Salud de los PDFs

Por fichero: magic bytes `%PDF-` (los bloqueos de transportes.gob.es llegan como 200 +
HTML), tamaño >10 KB, y que PyMuPDF devuelva >200 chars de texto (si no → OCR
pendiente, etiquetar, no inventar).

## 4. Salud de la DB (fantasmas, duplicados, gemelas, víctimas)

```python
ids_idx = [x['id'] for x in index]
assert len(ids_idx) == len(set(ids_idx))     # duplicados
fantasmas = set(ids_idx) - set(ids_reports)  # → 270 en producción (bug merge)
```
- El frontend lee el índice: un fantasma renderiza fichas con 'None'. Tras cualquier
  limpieza de colección, `consolidar` debe REEMPLAZAR el país en el índice, no hacer
  overlay sobre el index previo (ver pitfall index-fantasma en SKILL.md).
- **1 registro por expediente** en la DB final (comprobación hermética del dedupe).
- **Coords gemelas con criterio PK:** dos registros de expedientes distintos en la misma
  coordenada son LEGÍTIMOS si comparten PK (varios accidentes en el mismo paso a nivel)
  o ambos son `estacion_ign` sin PK; SOSPECHOSOS si los PK difieren >50 m. Parsear el PK
  con `(\d+)[+,.](\d{1,3})` → km flotante. En ES: 6 grupos legítimos + 1 sospechoso
  real detectado (0006/2012 PK 378+049 ≡ 0013/2009 PK 378,130 — la interpolación los
  calcó). Sin el criterio PK, el check gritaba en los 7 grupos y nadie mira la lista.
- **Víctimas v3→DB:** `r['fallecidos'] == v3.consecuencias.fallecidos` en todos los
  registros (el gráfico de víctimas depende de la propagación).

## 5. Auditoría geográfica — los `mal` SIEMPRE a la vista

- Cada registro con coords: distancia al tramo PK de su línea; cruce PK↔línea (la
  distancia sola es ciega al cross-line — bug Caleyo).
- **Motivo legible obligatorio** en cada `mal`/`duda`: no solo la distancia —
  "cae sobre OTRA vía: a 0 m del tramo X (línea 200), la declarada 622 está a 21884 m".
  El usuario no puede actuar sobre un `d_ref=414891` a secas.
- **Propagar `geo_veredicto` + `geo_motivo` del auditor a cada registro de la DB**
  (consolidar los lee de `data/revision/`) y exponerlos en el frontend (filtro + badge
  + banner ficha + contorno rojo discontinuo en mapa). "Que salgan en informes"
  incluye el visor público, no solo el .md interno.
- **Pitfall `id_provinc="00"`:** los tramos ADIF sin provincia llegan como "00"; si
  `coinciden_provincia` los trata como comparables, devuelve None/False masivamente y
  contamina el veredicto. Tratar "00" como "no comparable" (abstener), como campo vacío.
- Agrupar fallos por patrón (misma línea, mismo método_geo, mismo tramo) y corregir
  la CLASE en el geocodificador, nunca el registro suelto.

## 6. Orden de regeneración (pipeline completo) — CICLO, no línea

```bash
python scripts/geocodificar_via.py ES       # → json/ES/*.json (ubicacion.lat/lng)
python scripts/geocodificar_estacion.py ES  # → los aún sin resolver por estación
python scripts/consolidar.py ES             # → data/db/ (index+reports+recs)
python scripts/revisar_localizacion.py ES   # AUDITA LA DB (lee coords de data/db)
python scripts/consolidar.py ES             # RE-PROPAGA veredictos a la DB
python scripts/revisar_localizacion.py ES   # re-auditar sobre DB final (estable)
python scripts/verificar_todo.py ES         # gate integral → XX-verificacion.md
# bump VERSION_DATOS en frontend + verificar visualmente antes de desplegar
```
Circularidad real: el auditor lee la DB y consolidar propaga el veredicto del auditor.
Una sola pasada deja `geo_veredicto` desfasado en la DB; dos pasadas consolidar↔auditar
convergen (las coords no cambian, solo el etiquetado).

## 7. Patrón de código del verificador

- `check(nombre)` devuelve un closure registrador: `check("md5")("OK", detalle)` —
  evita repetir el nombre en 3 ramas. Cuidado al parchear: introducir la forma
  `check(nombre, nivel, detalle)` cuando ya se usa la closure → TypeError en cascada.
- Importar `defaultdict`/`Counter` desde el principio — los checks nuevos que los usen
  mueren con NameError si no (bug real esta sesión).
- Secciones numeradas con `section()`; conteo global `_stats`; veredicto final
  APTO/NO APTO + `sys.exit(1)` si `ERROR>0` (gate para cron).

## 8. Truco terminal (Windows git-bash)

Expresiones Python con `&`/`|` (intersección/unión de sets) dentro de heredocs
`python - <<'EOF'` pueden devolver exit -1 con queja del shell wrapper; usar
`.intersection()`/`.union()` explícitos o execute_code.

## Nota de proceso

Sesiones de arreglo de pipeline con trabajo bueno sin commitear → **commit de
seguridad PRIMERO** (el auditor de localización se perdió ya dos veces por cortes de
sesión y hubo que regenerarlo). El repo es la fuente de verdad: nada "en progreso"
sobrevive sin él.
