# Referencia: Kaizen Movilidad — Sistema de Planes de Movilidad

## Contexto

Proyecto real de David Antizar en Ineco. Objetivo: crear un sistema modular que genere planes de movilidad al trabajo completos en menos de 8 horas, en lugar de los 3-6 meses que tardan las consultoras tradicionales.

## Estructura de 10 secciones

Cada sección es un archivo `.md` independiente en `/root/workspace/kaizen-movilidad/`.

### Secuencia de ejecución

1. **01-introduccion-y-alcance** → Define el estudio, centro de trabajo, alcance legal
2. **02-encuesta-movilidad** → Recopila datos reales de empleados
3. **03-analisis-accesibilidad** → Isocronas reales (ORS + GTFS BFS + fallback)
4. **04-analisis-costes** → Coste por modo, escenarios teletrabajo, fiscalidad
5. **05-datos-demograficos** → Ranking de CPs con datos INE
6. **06-impacto-ambiental** → Emisiones CO₂ IPCC AR6, escenarios reducción
7. **07-escenarios-y-recomendaciones** → Priorización, plan de acción 24 meses
8. **08-informe-final** → DOCX 11 secciones + CSV + GeoJSON + KML + SHP
9. **09-implementacion-y-seguimiento** → KPIs, calendario, dashboard
10. **10-metodologia-y-fuentes** → Fuentes, fórmulas, glosario, limitaciones

## Formato de datos central

```json
{
  "estudio": {},
  "encuesta": {},
  "accesibilidad": {},
  "costes": {},
  "demografia": {},
  "impacto_ambiental": {},
  "recomendaciones": {},
  "implementacion": {},
  "metodologia": {}
}
```

## Orquestación

- 10 cron jobs creados, cada uno con `repeat: 1`
- Programados para ejecutar a las 17:00 UTC (19:00 España)
- Cada cron lee su plantilla → la refina → sobrescribe el archivo
- Los cron jobs se borran tras la ejecución

## Fuentes de datos principales

- **INE:** Padrón 2025, EAES 2024, EHPN 2023
- **NAP API:** 161 datasets GTFS de España
- **ORS:** OpenRouteService para isocronas reales
- **CityBikes API:** 74 redes de bicis en España
- **IPCC AR6:** Factores de emisión CO₂
- **Idealista/Catastro:** Precios vivienda
