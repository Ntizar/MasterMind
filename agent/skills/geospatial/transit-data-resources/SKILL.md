---
name: transit-data-resources
version: "1.0.0"
description: "Catálogo de APIs, datasets, apps y software de transporte público mundial. Inspirado en MobilityData/awesome-transit (⭐1.8K). Recursos GTFS, GTFS-realtime, APIs de tránsito, datasets abiertos."
tags: [transit, gtfs, api, dataset, catalog, transport, mobility]
---

# Recursos de Datos de Tránsito Mundial

## Resumen

Catálogo comunitario de recursos para transporte público: APIs, datasets, apps, software y research. Mantenido por MobilityData (organización detrás del estándar GTFS).

## Recursos clave

### APIs de tránsito por país

| País | API | Formato | Notas |
|------|-----|---------|-------|
| España | NAP DGT | GTFS-rt | nap.transportes.gob.es — ver skill `nap-dgt` |
| UK | Transport for London | GTFS-rt, REST | API gratuita con key |
| USA | TransitLand | REST, GTFS-rt | Aggregate de 2000+ agencias |
| Suiza | swisstrains.ch | GTFS-rt | Trenes en tiempo real |
| Global | OpenTripPlanner | REST | Multi-modal routing |

### Datasets GTFS estáticos

- **Mobility Database:** https://database.mobilitydata.org/ — 3000+ feeds GTFS de todo el mundo
- **TransitFeeds:** https://transitfeeds.com/ — catálogo histórico de feeds
- **GTFS Schedule spec:** https://gtfs.org/schedule/

### GTFS-realtime

- **Vehicle positions:** Posición GPS de vehículos en tiempo real
- **Trip updates:** Retrasos y cambios de horario
- **Alerts:** Avisos de servicio (obras, cancelaciones)

### Software open-source

| Herramienta | Función | Skill relacionado |
|------------|---------|-------------------|
| gtfs-to-html | Horarios HTML/PDF desde GTFS | — |
| static-GTFS-manager | Editor GUI de GTFS | — |
| OpenTripPlanner | Routing multi-modal | — |
| Valhalla | Routing con tiles | — |
| GTFS-Validator | Validar feeds GTFS | — |

## Patrón de uso

```javascript
// Descargar y parsear GTFS estático
const response = await fetch('https://nap.transportes.gob.es/gtfs.zip');
const zip = await JSZip.loadAsync(await response.arrayBuffer());

// Parsear stops.txt
const stopsCSV = zip.file('stops.txt').async('text');
const stops = parseCSV(stopsCSV); // [{stop_id, stop_name, stop_lat, stop_lon}]

// Fetch GTFS-realtime vehicle positions
const rtResponse = await fetch('https://nap.transportes.gob.es/gtfs-rt/vehicles');
const vehicles = await rtResponse.json();
```

## Pitfalls

- **Rate limits:** La mayoría de APIs tienen rate limits. Cachear respuestas.
- **GTFS vs GTFS-rt:** GTFS es estático (rutas, horarios). GTFS-rt es dinámico (posiciones, retrasos).
- **Timezones:** GTFS usa timezone por agencia. Convertir a UTC para comparar.
- **Frequencies vs stop_times:** Algunos feeds usan frequencies.txt en vez de stop_times.txt.
- **Dataset quality:** No todos los feeds son válidos. Usar GTFS-Validator antes de procesar.

## Referencias

- MobilityData/awesome-transit: https://github.com/MobilityData/awesome-transit
- GTFS spec: https://gtfs.org/
- Mobility Database: https://database.mobilitydata.org/

---

**Hecho con ❤️ por David Antizar**
