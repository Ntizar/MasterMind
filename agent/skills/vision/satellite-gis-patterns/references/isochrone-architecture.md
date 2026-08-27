# Isocronas — Arquitectura híbrida ORS + NAP

## Resumen

Patrón de arquitectura para herramientas de isocronas de movilidad:
motor de routing público (OpenRouteService) + datos GTFS locales (NAP)
para transporte público. Todo en el navegador, sin backend.

## Arquitectura

```
Frontend (HTML único)
├── Leaflet (Canvas renderer)
├── OpenRouteService API → isocronas 🚗🚲🚶
├── NAP/GTFS → paradas TP cercanas
├── jsPDF → informe PDF
└── Nominatim → geocodificación inversa
```

## OpenRouteService

- **Endpoint:** `GET https://api.openrouteservice.org/v2/isochrones/{lon},{lat}`
- **Params:** `profile`, `range[0]`, `range_type=time`, `attributes=area,total_pop`
- **Perfiles:** `driving-car`, `cycling-regular`, `cycling-mountain`, `foot-walking`
- **Gratis:** 2.000 requests/día con API key
- **Desnivel:** Ya considerado internamente en `cycling-*` y `foot-walking`

## NAP (Transporte Público España)

- **Catálogo GTFS** — no routing
- **Autenticación:** Header `ApiKey: <key>`
- **Flujo:** listar datasets → filtrar región → descargar GTFS → parsear stops → calcular cercanía
- **Solo España**

## Limitaciones del patrón

- ORS gratis tiene límite de 2.000 req/día
- NAP solo cubre España
- Sin backend, no se puede cachear ni batch requests
- Para producción escalable → self-host Valhalla o GraphHopper

## Proyectos de referencia

- TimeIneco: `/root/workspace/TimeIneco/PLAN.md`
