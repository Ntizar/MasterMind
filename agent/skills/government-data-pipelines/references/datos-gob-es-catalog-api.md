# datos.gob.es — Catálogo Nacional de Datos Abiertos (DESCUBIERTO 2026-06-30)

## Hallazgo clave

**La portal web (datos.gob.es) está bloqueada por WAF Incapsula**, pero **la API de catálogo SÍ funciona** sin autenticación.

## Endpoint

```
GET https://datos.gob.es/apidata/catalog/dataset.json?_page={page}
```

- Sin auth, sin CAPTCHA, sin rate limiting agresivo
- Responde JSON DCAT (Data Catalog Vocabulary)
- 10 datasets por página
- ~5,000+ datasets accesibles

## Estructura de respuesta

```json
{
  "result": {
    "items": [...],
    "itemsPerPage": 10,
    "page": 0
  }
}
```

## ⚠️ PITFALL CRÍTICO

Los datos están bajo `data["result"]["items"]`, NO bajo `data["items"]`.

```python
# ❌ INCORRECTO
items = data.get("items", [])  # → []

# ✅ CORRECTO
items = data["result"]["items"]  # → [10 datasets]
```

## Código de parseo

```python
import requests

def fetch_page(page=0):
    url = f"https://datos.gob.es/apidata/catalog/dataset.json?_page={page}"
    resp = requests.get(url, timeout=30, headers={"Accept": "application/json"})
    return resp.json()["result"]["items"]

def parse_dataset(item):
    titulo = ""
    for t in item.get("title", []):
        if isinstance(t, dict) and t.get("_lang") == "es":
            titulo = t["_value"]
            break
    
    dists = []
    for d in item.get("distribution", []):
        fmt = d.get("format", {})
        formato = fmt.get("value", "").split("/")[-1].upper() if isinstance(fmt, dict) else ""
        dists.append({"formato": formato, "url": d.get("accessURL", "")})
    
    return {
        "id": item.get("identifier", "").split("/")[-1],
        "titulo": titulo,
        "distribuciones": dists,
        "total_recursos": len(dists)
    }
```

## Scrapers existentes

- `scrapers/datos_gob_scraper.py` — scraper completo con paginación
- `scrapers/ckan_multi_portal.py` — multi-portal CKAN (Aragón + Madrid)
