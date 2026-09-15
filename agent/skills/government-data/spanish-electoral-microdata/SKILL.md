---
name: spanish-electoral-microdata
description: "Microdatos electorales de España: espejo y decodificador."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [elecciones, microdatos, ministerio-interior, datos-espana, descarga-masiva]
    related_skills: [government-data-pipelines, ineapy-ine-espana, boe-borme-api]
---

# Microdatos electorales de España

Espejo + **intérprete** de los microdatos del Ministerio del Interior. La fuente oficial (`infoelectoral.mir.es`) publica formatos propietarios que exigen software ad hoc para decodificarlos; este repo lo hace y redistribuye los datos.

## When to Use (cuándo usarlo)

- Necesitas resultados electorales **a nivel de mesa/sección** o listas de candidatos completas.
- Quieres cruzar **adscripción política de candidatos** con otras bases (adjudicaciones, cargos, sociedades).
- Buscas un patrón de **descarga masiva por listas de URLs** de un portal con desplegables.

## CLI real

```bash
php src/parse.php ruta/al/fichero.DAT     # decodifica y vuelca a stdout en formato legible
```

Usa `src/includes/functions.php` y `src/lists.php`.

## Patrón de descarga masiva (reutilizable)

Las relaciones oficiales de URLs están versionadas en el repo: `assets/congreso.txt`, `senado.txt`, `europeas.txt`, `municipales.txt`, `cabildos.txt`, `referendums.txt` → permite `wget -i municipales.txt` y bajar los **161 ficheros históricos** sin recorrer el portal a mano.

Posprocesado del espejo: cada ZIP se descomprime preservando el nombre (`04199105_TOTA.zip` → `municipales/04199105_TOTA`) y se eliminan `FICHEROS.DOC`/`FICHEROS.rtf` por ser idénticos en todos los ZIP (queda una copia única en `files/`).

## Cobertura

Europeas, Congreso, Senado, municipales y cabildos canarios (miles de agrupaciones, cientos de miles de candidatos) + **4 referéndums desde 1976**. El Ministerio **no** publica elecciones autonómicas (competencia de cada CCAA, según recoge el README).

## Pitfalls

- Datos base del volcado **2019/2020**; no hay API REST (era la idea del autor, quedó pendiente).
- Las tablas de decodificación de municipios/provincias derivan del INE con nombres "embellecidos" (issue #1) → verificar mapeos antes de cruces finos.
- Licencia AGPL-3.0.

## Referencia

- Repo: `JaimeObregon/infoelectoral` (~155 ⭐, PHP, consultado 2026-09-15).
- Contexto jurídico: el README recoge la jurisprudencia del TC que declara pública la adscripción política del candidato.
