# ERA — Scraping de Accident Investigation Reports

## Sitio

- **URL base:** `https://www.era.europa.eu`
- **Plataforma:** Drupal (server-side rendered — curl funciona sin JS)
- **Rate limiting:** Agresivo, 429 tras ~50 requests rápidas. Backoff: 30s, 60s, 90s...

## Estructura de navegación

```
era-folder/accident-investigation-reports  (índice de países)
  └── era-folder/investigations             (AT — sin prefijo de país en URL)
  └── era-folder/be-investigations           (BE)
  └── era-folder/bg-investigations           (BG)
  ...                                        (29 países total)
      └── era-folder/2024-13                 (año — sufijo numérico variable)
          └── tabla con enlaces a PDFs
```

### URLs de los 29 países

```python
PAISES_URLS = {
    "AT": f"{BASE_URL}/era-folder/investigations",      # AT sin prefijo
    "BE": f"{BASE_URL}/era-folder/be-investigations",
    "BG": f"{BASE_URL}/era-folder/bg-investigations",
    "CH": f"{BASE_URL}/era-folder/ch-investigations",
    "CZ": f"{BASE_URL}/era-folder/cz-investigations",
    "DE": f"{BASE_URL}/era-folder/de-investigations",
    "DK": f"{BASE_URL}/era-folder/dk-investigations",
    "EE": f"{BASE_URL}/era-folder/ee-investigations",
    "EL": f"{BASE_URL}/era-folder/el-investigations",
    "ES": f"{BASE_URL}/era-folder/es-investigations",
    "FI": f"{BASE_URL}/era-folder/fi-investigations",
    "FR": f"{BASE_URL}/era-folder/fr-investigations",
    "HR": f"{BASE_URL}/era-folder/hr-investigations",
    "HU": f"{BASE_URL}/era-folder/hu-investigations",
    "IE": f"{BASE_URL}/era-folder/ie-investigations",
    "IT": f"{BASE_URL}/era-folder/it-investigations",
    "LT": f"{BASE_URL}/era-folder/lt-investigations",
    "LU": f"{BASE_URL}/era-folder/lu-investigations",
    "LV": f"{BASE_URL}/era-folder/lv-investigations",
    "NL": f"{BASE_URL}/era-folder/nl-investigations",
    "NO": f"{BASE_URL}/era-folder/no-investigations",
    "PL": f"{BASE_URL}/era-folder/pl-investigations",
    "PT": f"{BASE_URL}/era-folder/pt-investigations",
    "RO": f"{BASE_URL}/era-folder/ro-investigations",
    "SE": f"{BASE_URL}/era-folder/se-investigations",
    "SI": f"{BASE_URL}/era-folder/si-investigations",
    "SK": f"{BASE_URL}/era-folder/sk-investigations",
    "Serbia": f"{BASE_URL}/era-folder/serbia-investigations",
    "UK": f"{BASE_URL}/era-folder/uk-investigations",
}
```

## Patrones de URL de PDFs (CRÍTICO)

ERA usa **dos rutas diferentes** para servir PDFs:

- `/sites/default/files/` — Drupal 8+ (PDFs más recientes)
- `/system/files/` — Drupal 7 y migrados (PDFs antiguos)

### Regex que captura AMBOS patrones

```python
# ❌ INCORRECTO — solo captura /sites/default/files/
pdf_links = re.findall(r'href="(/sites/default/files/[^"]*\.pdf)"', html)

# ✅ CORRECTO — captura cualquier path que termine en .pdf
pdf_links = re.findall(r'href="(/[^"]*\.pdf[^"]*)"', html, re.IGNORECASE)
```

Con el patrón amplio, AT pasó de 4 PDFs (solo recientes) a 185 PDFs (todos los años).

## Patrones de URL de años

Los años tienen sufijos numéricos variables que cambian entre países:

```
/era-folder/2005          (AT — sin sufijo)
/era-folder/2024-13      (AT — con sufijo)
/era-folder/2007-0       (BE — sufijo -0)
/era-folder/2023-2       (CZ — sufijo variable)
```

### Regex para extraer años

```python
year_links = re.findall(r'href="(/era-folder/\d{4}[-\d]*)"', html)
# Limpiar sufijo: "2024-13" → "2024"
año_clean = re.match(r'(\d{4})', año).group(1)
```

## Distribución de PDFs por país (2026-07-08)

| País | PDFs | País | PDFs | País | PDFs |
|------|------|------|------|------|------|
| CZ | 601 | RO | 563 | HU | 508 |
| UK | 375 | DE | 407 | ES | 376 |
| FI | 314 | NO | 170 | AT | 185 |
| PL | 128 | DK | 149 | BE | 111 |
| HR | 111 | FR | 119 | IT | 101 |
| SE | 109 | PT | 61 | BG | 57 |
| IE | 53 | SK | 43 | LV | 24 |
| NL | 22 | EE | 19 | SI | 14 |
| Serbia | 65 | LT | 8 | LU | 5 |
| EL | 4 | CH | 13 | | |

**Total: 4.715 PDFs en 29 países, 429 carpetas de año (2002-2025)**

## Script de referencia

`/root/workspace/ERAVisor/scripts/descargar_todos_era.py`

Features:
- Scrapeo incremental con guardado tras cada país
- Resume desde índice previo (`indice_era.json`)
- Dry-run (`--dry-run`) para contar sin descargar
- Filtrar por país (`--pais AT`)
- Reintentar fallidos (`--reintentar`)
- Delay configurable (`--delay=1.5`)
- Estructura: `Data/PAIS/AÑO/archivo.pdf`
