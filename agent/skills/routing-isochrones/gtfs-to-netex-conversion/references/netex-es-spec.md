# Especificación NeTEx-ES — Resumen ejecutivo

## Fuente completa
Para la especificación completa (400+ líneas), ver `../../spec/NeTEx-ES.md` en el repo netex.

## Estructura XML básica

```xml
<PublicationDelivery version="1.14"
  xmlns="http://www.netex.org.uk/netex"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.netex.org.uk/netex 
    http://netex-cen.github.io/netex-schemas/schemas/1.14/neTEx/neTEx_publication.xsd">
  <PublicationTimestamp>2025-01-15T10:00:00Z</PublicationTimestamp>
  <dataDescription>
    <PublisherRef>ES:Publisher:CRTM</PublisherRef>
    <PublicationFormat>application/neTex+xml</PublicationFormat>
  </dataDescription>
  <dataObjects>
    <CompositeFrame id="ES:Frame:CRTM:001" version="1">
      <FrameDefaults>
        <DefaultFrameType>network</DefaultFrameType>
        <DefaultLanguage>es</DefaultLanguage>
        <DefaultCurrency>EUR</DefaultCurrency>
        <DefaultTimezone>Europe/Madrid</DefaultTimezone>
      </FrameDefaults>
      <dataObjects>
        <!-- StopPlaces, Lines, Routes, VJs, Fares... -->
      </dataObjects>
    </CompositeFrame>
  </dataObjects>
</PublicationDelivery>
```

## Jerarquía de paradas (clave NeTEx)

```
StopPlace (estación/intercambiador)
  └── Quays (andenes)
        └── StopPoint (punto exacto de parada)
```

- `location_type=1` en GTFS → StopPlace con Quays hijos
- `location_type=0` en GTFS → StopPoint dentro de un Quay
- Cada StopPlace puede tener múltiples Quays (andenes ida/vuelta)

## IDs NeTEx-ES

Formato: `ES:{Tipo}:{Operador}:{Secuencia}`

| Tipo | Ejemplo |
|---|---|
| Frame | `ES:Frame:CRTM:001` |
| StopPlace | `ES:StopPlace:MTM:28079:001` |
| Quay | `ES:Quay:MTM:28079:001:Q01` |
| StopPoint | `ES:StopPoint:MTM:28079:001:Q01` |
| Line | `ES:Line:MTM:M1` |
| Route | `ES:Route:MTM:M1:N` |
| JourneyPattern | `ES:JP:MTM:M1:N` |
| VehicleJourney | `ES:VJ:MTM:M1:N:001` |
| ServiceFrame | `ES:SF:MTM:Weekday` |
| FareZone | `ES:FareZone:MTM:Z1` |

## Operadores españoles comunes

| Código | Operador |
|---|---|
| MTM | Metro de Madrid |
| EMT | EMT Madrid |
| RENFE | Renfe Operadora |
| TMB | Transports Metropolitans de Barcelona |
| FGC | Ferrocarrils de la Generalitat |
| EUSKOTREN | Euskotren Trena |
| TRAM | Metrovalencia |
| CRTM | Consorcio Regional Transportes Madrid |
