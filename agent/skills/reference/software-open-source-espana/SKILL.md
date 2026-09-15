---
name: software-open-source-espana
description: "Catálogo de software open source específico de España."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: CC0-1.0
metadata:
  hermes:
    tags: [espana, catalogo, open-source, catastro, ign, datos-abiertos, librerias]
    related_skills: [catastro-api, ineapy-ine-espana, ign-wmts-tiles, government-data-pipelines]
---

# Software open source de España (awesome-spain)

Catálogo curado (CC0-1.0, ~339 ⭐, consultado 2026-09-15) de **software open source que da soporte específico a España**: 37 categorías que van de cartografía y catastro a facturación electrónica, firma digital o datos abiertos.

## When to Use (cuándo usarlo)

- **Antes de escribir un conector desde cero**: puede existir ya una librería española mantenida para ese organismo/portal.
- Buscas alternativa open source a un servicio de pago para datos españoles (Catastro, IGN, INE, DGT, AEAT…).
- Quieres saber qué existe en un dominio concreto (energía, meteorología, movilidad, salud) antes de decidir stack.

## Categorías (37)

Agricultura · Alarmas y Seguridad del Hogar · Blockchain e Identidad Digital · **Cartografía y Catastro** · Cine y Entretenimiento · Combustible y Estaciones de Servicio · **Comunidades Autónomas y Administración Local** (por CCAA: Andalucía…País Vasco) · **Datos Abiertos y Estadísticas** · Deportes · **DGT y Vehículos** · Educación y Oposiciones · Empleo y Trabajo Remoto · **Energía y Electricidad** · ERP y Contabilidad · Extranjería y Visados · **Facturación Electrónica** (Facturae, SII y modelos AEAT, TicketBAI, VeriFactu) · **Firma Electrónica y Administración Pública** (AutoFirma, @firma) · Formatos Bancarios · Inmobiliaria y Mercados · Lengua Española y Diccionarios · Logística y Mensajería · Meteorología · Música y Flamenco · Participación Ciudadana · Pasarelas de Pago · Procesamiento de Lenguaje Natural · Salud y Medicamentos · **Servidores MCP** · Smart Cities e IoT · Supermercados · Telecomunicaciones · Televisión, Radio y Podcasts · Transparencia y Legal Tech · **Transporte y Movilidad** · Validación de Documentos.

## Selección verificada de las categorías clave

**Cartografía y Catastro** (lo más denso del catálogo):

- `IGN-CNIG/API-CNIG` — API del CNIG para visualizadores cartográficos web.
- `Desarrollos-IDEE/API-IDEE` — API JS de la IDE de España (visualizadores con datos IDE).
- `dieghernan/leaflet-providersESP` — proveedores de teselas y capas WMS de España (IGN, Catastro, CCAA) para Leaflet.
- `sigdeletras/Leaflet.Spain.WMS` — capas WMS (PNOA, IGN base, Catastro) para Leaflet.
- `sperea/catastro-lib-python`, `gisce/pycatastro`, `IvanitiX/ESCatastroLib` — librerías Python del Catastro.
- `oscarfonts/catastro2postgis` — importa datos del Catastro a PostGIS.
- `OSM-es/CatAtom2Osm` — convierte datos INSPIRE del Catastro a OpenStreetMap.
- `geomatico/cidownloader` — descargador de datos INSPIRE del Catastro.
- `martgnz/bcn-geodata` — shapefiles oficiales de Barcelona en GeoJSON/TopoJSON.
- `rOpenSpain/mapSpain` — límites administrativos de España (CCAA, provincias, municipios) en R.

**Datos Abiertos y Estadísticas**:

- **Datania** (`datania/hub`) — centro logístico de datasets abiertos de España: INE, AEMET, BOE, IPC, Mercadona (demo en `datania.cc`). Repos satélite por fuente (`ine-catalog`, `aemet`, `boe`, `ipc`, `mercadona-catalog`, `datosgobes-catalog`).
- `martgnz/es-atlas` — **TopoJSON preconstruido del IGN** para mapas de España (evita montar el pipeline de conversión).
- `davidgasquez/dine` — librería y CLI para explorar/exportar datos del INE.
- `rOpenSpain/INEbaseR`, `sigdeletras/censosine21` — INE desde R / API del Censo 2021 en Python.
- `inigoflores/ds-codigos-postales-ine-es`, `franciscojuan1974/codigos_postales_spain` — relación códigos postales ↔ municipios (>11.000 CP con coordenadas).
- `datadista/datasets` — datos de los reportajes de investigación de DATADISTA.
- `palmerabollo/egov` — API abierto de datos públicos españoles.

## Cómo usarlo en la práctica

1. Antes de construir un conector para un organismo español, **buscar aquí** (el catálogo enlaza al repo y muestra stars/último commit/idioma/licencia con badges).
2. Si el repo está muerto, usar el catálogo como mapa de alternativas (suelen existir 2-3 implementaciones por fuente).
3. Es CC0-1.0: sus datos de índice se pueden reutilizar libremente; cada herramienta mantiene su licencia.

## Pitfalls

- Es una **lista curada**, no una librería: nada de `pip install`. Copiar el enlace del repo concreto.
- Incluye proyectos de calidad y madurez muy dispares (hay wrappers de una tarde y proyectos de organismos oficiales): mirar stars + último commit antes de adoptar.
- Muchas entradas son de R (rOpenSpain); para el stack Python/Node de David, filtrar por lenguaje.

## Referencia

- Repo: `GeiserX/awesome-spain` (~339 ⭐, CC0-1.0, consultado 2026-09-15). Contribuciones vía PR siguiendo el formato de badges del README.
