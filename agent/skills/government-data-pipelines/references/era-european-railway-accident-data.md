# ERA — European Union Agency for Railways Accident Investigation Reports

## Fuente
- **URL:** https://www.era.europa.eu/era-folder/accident-investigation-reports
- **Países:** 28 (AT, BE, BG, CH, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT, LT, LU, LV, NL, NO, PL, PT, RO, SE, SI, SK, UK, RS)
- **Años cubiertos:** 2003–2025 (variable por país)
- **Idiomas:** Cada país publica en su lengua oficial (ES → español, FR → francés, DE → alemán, UK → inglés, etc.)

## Estructura del sitio
La página principal lista carpetas por país. Cada carpeta país lista años. Cada año tiene una tabla con los informes.

### URLs por país (verificado)
```
/era-folder/{PAIS_ISO2}-investigations
/era-folder/serbia-investigations      (excepción: Serbia no tiene ISO de 2 letras ERA)
```

### URLs de años dentro de cada país (formato Drupal book)
La URL real se obtiene del href del link. Ejemplos desde el HTML:
```javascript
// Obtener URLs de años desde la página de país:
document.querySelectorAll('nav a[href*="/era-folder/"]').forEach(a => {
  if (a.textContent.trim().match(/^\d{4}$/)) console.log(a.getAttribute('href'))
})
```
Ejemplo ES: `/era-folder/2006-5`, `/era-folder/2007-7`, etc. Los sufijos numéricos varían por país.

### URLs de PDFs
Dos patrones:
1. `https://www.era.europa.eu/system/files/YYYY-MM/{filename}` — informes antiguos
2. `https://www.era.europa.eu/sites/default/files/YYYY-MM/{filename}` — informes recientes

## Indexación por país

### Script de extracción
```python
import requests, json, re, time
from bs4 import BeautifulSoup

ERA_BASE = "https://www.era.europa.eu"
PAIS = "FR"  # ISO del país

def extraer_informes_pais(pais, year_urls):
    """Extrae todos los informes PDF de un país para todos los años."""
    reports = []
    for year, url in year_urls.items():
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        for link in soup.find_all('a', href=re.compile(r'\.pdf$', re.I)):
            href = link.get('href')
            if not href.startswith('http'):
                href = ERA_BASE + href
            reports.append({
                "title": link.text.strip() or href.split('/')[-1],
                "pdf_url": href,
                "year": int(year),
                "country": pais
            })
        time.sleep(1)  # rate limiting
    return reports
```

### Países indexados (a 2026-07-06)
| País | Informes | Rango |
|------|----------|-------|
| ES (España) | 375 | 2006–2025 |
| DE (Alemania) | 392 | 2006–2025 |
| FR (Francia) | 119 | 2004–2023 |
| IT (Italia) | 100 | 2005–2024 |
| NL (Países Bajos) | 21 | 2003–2024 |
| UK (Reino Unido) | 373 | 2005–2020 |
| **TOTAL** | **1.380** | |

### Formato de índice
```json
{
  "source": "ERA",
  "url": "https://www.era.europa.eu/era-folder/{pais}-investigations",
  "total_reports": 375,
  "reports": [
    {
      "title": "ID-011206-130407.pdf",
      "pdf_url": "https://www.era.europa.eu/system/files/2023-07/ID-011206-130407.pdf",
      "year": 2006,
      "country": "ES"
    }
  ]
}
```

## Estructura de los informes PDF (CIAF España)

Los informes españoles (CIAF) siguen una estructura muy consistente con 3 eras:

### Era 1: Pre-RD 810/2007 (2006–2008)
- Formato libre, secciones variables
- Portada escueta: solo número de expediente
- Archivos: `ID-DDMMAA-DDMMAA.pdf` (fechas de suceso y de informe)

### Era 2: RD 810/2007 (2009–2013)
- Secciones 1–5: Resumen, Descripción, Análisis, Conclusiones, Recomendaciones
- Portada con logo Ministerio de Fomento + CIAF
- Archivos: `ID-DDMMAA-DDMMAA.pdf`

### Era 3: RD 623/2014 (2014–2025)
- Secciones 0–6: Abreviaturas, Resumen, Descripción, Análisis, Conclusiones, Recomendaciones, Anexos
- Portada moderna con diseño CIAF
- Incluye English summary al final
- Archivos: `ES-XXXXX - Final Report, YYYY-NN-DDMM-if.pdf` o `ES-XXXXX - YYYYMMDD-IF descripción.pdf`

### Extracción de campos

**Campos extraíbles con regex:**
- `fecha` → patrón `DD/MM/AAAA` o `DD.MM.AAAA` en primeras 5000 chars
- `hora` → `a las HH:MM` o `sobre las HH:MM`
- `provincia` → `provincia de X` o `término municipal de X`
- `pk` → `PK NNN+NNN` o `p.k. NNN+NNN`
- `línea` → `línea NOMBRE (DESDE - HASTA)`
- `fallecidos`, `heridos_graves`, `heridos_leves` → números + palabras clave

**Campos extraíbles con LLM (deepseek-v4-flash):**
- Clasificación Anexo III (código de suceso y causa)
- Causas directas y factores contribuyentes
- Resumen estructurado
- Recomendaciones de seguridad

### Esquema de salida (57 columnas, 6 secciones)
Ver `/root/workspace/ERAVisor/schemas/eravisor-schema.json`

Secciones: datos_generales (16), clasificacion_suceso (4), clasificacion_causa (4), victimas (10), descripcion (5), analisis (12), control_calidad (6)

## Taxonomía de clasificación (Anexo III RD 929/2020)

### Sucesos ferroviarios (79 códigos, 3 niveles)
```
1 = Accidente
  1.1 = Colisión tren con vehículo ferroviario
    1.1.1 = Frontal
    1.1.2 = Alcance
    1.1.3 = Lateral
  1.2 = Colisión con obstáculo en gálibo
    1.2.1 = Elementos de tren
    ...
  1.3 = Descarrilamiento
  1.4 = Accidente en paso a nivel
  1.5 = Accidente a persona por material rodante
  1.6 = Incendio/explosión
  1.7 = Otros accidentes
2 = Incidente
  2.1 = Precursor
  2.2 = Otros precursores
  2.3 = Otros incidentes
3 = Suicidio
  3.1 = Suicidio
  3.2 = Intento de suicidio
```

### Causas directas (53 códigos, 3 niveles)
```
1 = Ferrocarril
  1.1 = Factor humano
    1.1.1 = Señales
    1.1.2 = Bloqueo
    ...
  1.2 = Fallo técnico
    1.2.1 = Fallo material rodante
      1.2.1.1 = Rodadura
      ...
    1.2.2 = Fallo instalaciones
2 = Usuarios/entorno/otros
  2.1 = Usuarios del ferrocarril
  2.2 = Condiciones de entorno
  2.3 = Otros
  2.4 = Sin identificar
```

## Pipeline de extracción

### Script principal
`/root/workspace/ERAVisor/scripts/extract_pipeline.py`

```bash
# Prueba con muestra
python3 extract_pipeline.py --pais ES --samples 3

# Completo (375 PDFs, ~1.5h)
python3 extract_pipeline.py --pais ES
```

### Flujo
1. Cargar índice JSON del país
2. Descargar cada PDF (con retry + rate limiting)
3. Extraer texto con PyPDF2
4. Extraer campos básicos con regex
5. Llamar a LLM (deepseek-v4-flash vía NaN API) para clasificación + análisis
6. Aplanar JSON anidado a CSV
7. Generar CSV + Excel

### NaN API endpoint
```python
NAN_API_URL = "https://api.nan.builders/v1/chat/completions"
NAN_API_KEY = os.environ.get("NAN_API", "")
```

### Pitfalls ERA
- **Rate limiting (429):** ERA devuelve 429 si se descargan más de 3-4 PDFs seguidos. Usar `time.sleep(2)` entre descargas
- **URLs que caducan:** las URLs con `sites/default/files/YYYY-MM/` cambian de prefijo cuando el archivo se mueve. Fallback: probar `system/files/YYYY-MM/` si `sites/default/files/` falla
- **PDFs falsos (404 HTML):** ERA devuelve HTTP 200 con un HTML "Sorry - XXXX" cuando el PDF no existe. Verificar `head -c 5 == "%PDF-"`
- **Nombres de archivo:** Los más antiguos (2006-2013) usan IDs crípticos (`ID-DDMMAA-DDMMAA.pdf`). Los modernos (2014+) usan nombres descriptivos
- **Multi-idioma:** Francia y Alemania publican informes en sus idiomas. El prompt LLM debe ser adaptado al idioma del país

## Proyecto ERAVisor
- **Carpeta:** `/root/workspace/ERAVisor/`
- **Estructura:**
  ```
  ERAVisor/
  ├── data/          → Índices JSON por país + CSVs extraídos
  ├── schemas/       → RD 929/2020, Anexos I y III, esquema 57 cols
  ├── scripts/       → extract_pipeline.py
  ├── pdfs/{PAIS}/   → PDFs descargados
  └── notes/         → Resúmenes de sesión
  ```
- **Roadmap:**
  - Fase 1: España completo (375 PDFs → CSV/Excel)
  - Fase 2: Indexar + extraer resto de países ERA
  - Fase 3: Visor web global (mapa + filtros + estadísticas)
  - Fase 4: Herramienta de planes de riesgo cuantitativos
