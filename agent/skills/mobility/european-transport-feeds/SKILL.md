---
name: european-transport-feeds
description: Feeds de transporte público europeos en GTFS/NeTEx — datos abiertos para toda Europa.
version: "1.0.0"
tags: [GTFS, NeTEx, transport, Europe, open-data, feeds]
---

# European Transport Feeds

## Resumen

Feeds de transporte público europeos en GTFS/NeTEx — datos abiertos para toda Europa. 58⭐.

## Repo de referencia

- **GitHub:** `github.com/public-transport/european-transport-feeds`
- **Lenguaje:** Markdown (catálogo de URLs)
- **Licencia:** Open Data

## Contenido

Catálogo de feeds GTFS de ciudades europeas:

- **España:** Madrid (EMT), Barcelona (TMB), Valencia, Sevilla
- **Francia:** París (RATP), Lyon, Marsella
- **Alemania:** Berlín (BVG), Múnich (MVV)
- **Reino Unido:** Londres (TfL), Manchester
- **Italia:** Roma (ATAC), Milán (ATM)
- **Portugal:** Lisboa (Carris), Oporto (STCP)

## Uso

```bash
# Clonar para referencia
git clone https://github.com/public-transport/european-transport-feeds.git

# Buscar feed de una ciudad
cat european-transport-feeds/README.md | grep -i spain -A 10
```

## Integración con Mastermind

- Complementa `node-gtfs` — feeds reales para importar
- Fuente para `gtfs-browser-parser` — datasets reales
- Útil para `opentripplanner-otp` — feeds para routing
- Referencia para `gtfs-to-html-timetables` — datos de horarios

## Pitfalls

- **Actualización:** Los feeds pueden caducar o cambiar URL
- **Formato:** Mezcla de GTFS y NeTEx
- **Cobertura:** Mejor para Europa del Norte que del Sur

## Referencias

- [GitHub: public-transport/european-transport-feeds](https://github.com/public-transport/european-transport-feeds)
