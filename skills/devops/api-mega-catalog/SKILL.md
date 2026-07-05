---
name: api-mega-catalog
version: "1.0.0"
description: "Catálogo masivo de APIs públicas listas para usar — 6000+ APIs organizadas por categoría. Inspirado en cporter202/API-mega-list (⭐7K)."
tags: [api, catalog, reference, resources, public-data]
---

# Catálogo Mega de APIs Públicas

## Resumen

[API-mega-list](https://github.com/cporter202/API-mega-list) (⭐7K) es una colección potente de APIs públicas listas para usar inmediatamente. Organizadas por categoría con ejemplos de uso.

## Categorías principales

| Categoría | APIs | Ejemplos |
|-----------|------|---------|
| Weather | 50+ | Open-Meteo, OpenWeather, WeatherAPI |
| Maps/Geo | 40+ | OSM, Google Maps, Mapbox, IGN, Catastro |
| Transport | 30+ | GTFS, NAP DGT, TfL, TransitLand |
| Government | 20+ | BOE, INE, Catastro, datos.gob.es |
| Finance | 40+ | ECB, Yahoo Finance, Alpha Vantage |
| AI/ML | 30+ | OpenAI, Hugging Face, Replicate |
| Media | 25+ | YouTube, Spotify, Unsplash |
| Science | 20+ | NASA, USGS, NOAA |
| Sports | 15+ | Football-Data, ESPN |
| News | 20+ | NewsAPI, Guardian, NYT |

## Patrón de uso

```javascript
// Estructura del catálogo
const apiCatalog = {
  "weather": {
    "open-meteo": {
      "url": "https://api.open-meteo.com/v1/forecast",
      "auth": "none",
      "free": true,
      "rate_limit": "10000/day",
      "example": "https://api.open-meteo.com/v1/forecast?latitude=40.4&longitude=-3.7&hourly=temperature_2m"
    },
    "ign-wmts": {
      "url": "https://www.ign.es/wmts/mapa-raster",
      "auth": "none",
      "free": true,
      "type": "tiles",
      "skill": "ign-wmts-tiles"
    }
  },
  "government": {
    "boe": {
      "url": "https://www.boe.es/api/boe",
      "auth": "none",
      "free": true,
      "skill": "boe-borme-api"
    },
    "catastro": {
      "url": "https://ovc.catastro.meh.es",
      "auth": "none",
      "free": true,
      "skill": "catastro-api"
    }
  }
};

// Buscar API por keyword
function findAPI(keyword) {
  const results = [];
  for (const [category, apis] of Object.entries(apiCatalog)) {
    for (const [name, info] of Object.entries(apis)) {
      if (name.includes(keyword) || category.includes(keyword)) {
        results.push({ name, category, ...info });
      }
    }
  }
  return results;
}
```

## APIs relevantes para proyectos de David

| API | Categoría | Skill relacionado | Uso |
|-----|---------|-------------------|-----|
| Open-Meteo | Weather | — | Weather, marine, air-quality, flood, soil, pollen |
| IGN WMTS | Maps | `ign-wmts-tiles` | Mapas base España |
| Catastro | Government | `catastro-api` | Datos catastrales |
| BOE/BORME | Government | `boe-borme-api` | Boletín oficial |
| INE | Government | `ineapy-ine-espana` | Estadísticas España |
| NAP DGT | Transport | `nap-dgt` | Movilidad España |
| USGS | Science | — | Terremotos, geología |
| ESIOS | Energy | `esios-complete` | Mercado eléctrico España |

## Pitfalls

- **Rate limits:** Verificar rate limit antes de usar en producción.
- **API keys:** Algunas APIs requieren key gratuita. Registrarse antes.
- **CORS:** Algunas APIs no permiten CORS. Usar proxy si es necesario.
- **Deprecation:** Las APIs pueden cambiar o desaparecer. Verificar status.
- **Data quality:** No todas las APIs tienen datos actualizados o completos.

## Referencias

- API-mega-list: https://github.com/cporter202/API-mega-list
- Public APIs: https://github.com/public-apis/public-apis

---

**Hecho con ❤️ por David Antizar**
