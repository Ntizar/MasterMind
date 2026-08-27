# Scraping de transportes.gob.es — CIAF (Comisión de Investigación de Accidentes Ferroviarios)

## Problema

La web del Ministerio de Transportes (transportes.gob.es) bloquea browser tools con 403 ("PÁGINA WEB BLOQUEADA"). El HTML de curl contiene solo el menú de navegación en páginas que cargan contenido vía AJAX/JavaScript (Views). Pero muchas páginas sí tienen el contenido embebido en HTML estático.

## Solución general

```bash
curl -sL 'https://www.transportes.gob.es/organos-colegiados/ciaf' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
  | grep -oP 'href="[^"]*\.pdf"' | sort -u
```

## Patrones de URL por tipo de contenido

### Informes finales de sucesos investigados (~219 PDFs, 2007-2025)

| Rango | Patrón URL | Ejemplo | PDFs |
|---|---|---|---|
| 2007-2016 | `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/YYYY/` | `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/2009/` | ~181 |
| 2017-2025 | `/informes-finales-de-sucesos-investigados/infofin-YYYY` | `/infofin-2025` | ~38 |
| **Total** | | | **~219** |

**⚠️ NOTA:** Los patrones anteriores (`informes-accidentes-ferroviarios-YYYY`) NO funcionan. La URL real para 2007-2016 es la ruta `/MFOM/LANG_CASTELLANO/...`

**⚠️ 2007-2014 es el patrón más importante:** `informes-accidentes-ferroviarios-AÑO`
- Cada año tiene una subpágina con la tabla de informes
- Los PDFs están en el HTML estático (no AJAX)
- Los enlaces usan comillas simples: `href='/recursos_mfom/...'`
- Regex correcto: `href=(['"])(/recursos_mfom/pdf/[^'"]+?\.pdf)\1`
- En 2008 hay 53 PDFs en una sola página

### Memorias anuales (17 PDFs, 2008-2024)

- **URL:** `/organos-colegiados/ciaf/memorias-anuales/memoriasanuales`
- Contenido en HTML estático (no AJAX)
- Los enlaces usan comillas simples
- Regex: `href='(/recursos_mfom/[^']+\.pdf)'`
- Guardados en `/root/workspace/CIAF/memorias/`

## Patrones de PDFs en transportes.gob.es

Los PDFs usan múltiples rutas según el año de publicación:

1. **`/recursos_mfom/paginabasica/recursos/XXXX-YY-ZZZZ-if-*.pdf`** (2017-2025)
2. **`/recursos_mfom/pdf/UUID-UUID/FILENAME.pdf`** (2015-2016, memorias)
3. **`/recursos_mfom/FILENAME.pdf`** (algunos antiguos)
4. **`/recursos_mfom/listado/recursos/FILENAME.pdf`** (memorias recientes)
5. **`/recursos_mfom/comodin/recursos/FILENAME.pdf`** (2016)

**Siempre usar múltiples patrones regex simultáneamente.**

## Navegación de la web (Drupal)

La web usa Drupal con navegación por menús desplegables. Los enlaces importantes:

| Ruta | Descripción |
|---|---|
| `/organos-colegiados/ciaf` | Página principal CIAF |
| `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados` | Lista principal |
| `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/AÑO` | Página por año (2015-2016) |
| `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/AÑO/informes-accidentes-ferroviarios-AÑO` | Subpágina con PDFs (2007-2014) |
| `/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/infofin-AÑO` | Página por año (2017-2025) |
| `/organos-colegiados/ciaf/memorias-anuales/memoriasanuales` | Memorias anuales |
| `/organos-colegiados/ciaf/normativa` | Normativa |
| `/organos-colegiados/ciaf/presentacion` | Presentación |

## Distribución de PDFs

### Informes finales (~219 PDFs, ~200 MB)

| Año | PDFs | Año | PDFs |
|---|---|---|---|
| 2007 | 0 | 2016 | 11 |
| 2008 | 0 | 2017 | 12 |
| 2009 | 43 | 2018 | 2 |
| 2010 | 28 | 2019 | 3 |
| 2011 | 24 | 2020 | 3 |
| 2012 | 23 | 2021 | 6 |
| 2013 | 23 | 2022 | 5 |
| 2014 | 14 | 2023 | 3 |
| 2015 | 15 | 2024 | 3 |
| | | 2025 | 1 |

**Nota:** 2007 y 2008 están vacíos en la web (no hay PDFs publicados).

### Memorias anuales (17 PDFs, ~41 MB)

| Año | Archivo |
|---|---|
| 2008 | CIAFMemoriaAnual2008300909.pdf |
| 2009 | CIAF_informe_anual_2009.pdf |
| 2010 | CIAF_Informe_Anual_2010.pdf |
| 2011 | MemoriaAnual2011.pdf |
| 2012 | CIAFMemoriaAnual2012_260912.pdf |
| 2013 | CIAFMemoriaAnual2013.pdf |
| 2014 | 20150923_Memoria_Anual_2014.pdf |
| 2015 | CIAFMemoria_Anual_2015.pdf |
| 2016 | memoriaanualciaf2016.pdf |
| 2017 | memoriaanualciaf2017.pdf |
| 2018 | ciaf_memoriaanual2018.pdf |
| 2019 | ciaf_memoriaanual2019.pdf |
| 2020 | ciaf_memoriaanual2020.pdf |
| 2021 | ciaf_memoriaanual2021.pdf |
| 2022 | ciaf_memoriaanual2022.pdf |
| 2023 | ciaf_memoriaanual2023.pdf |
| 2024 | ciaf_memoriaanual2024.pdf |

## Scripts de ejemplo

### Extraer PDFs de una página de informes (2007-2014)

```bash
# La subpágina de 2008 tiene 53 PDFs
curl -s "https://www.transportes.gob.es/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/2008/informes-accidentes-ferroviarios-2008" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  | grep -oP "href=(['\"])(/recursos_mfom/[^'\"]+?\.pdf)\1" \
  | sed -E "s/href=['\"]([^'\"]+)['\"].*/https:\/\/www.transportes.gob.es\1/" \
  | sort -u
```

### Extraer memorias anuales

```bash
curl -s "https://www.transportes.gob.es/organos-colegiados/ciaf/memorias-anuales/memoriasanuales" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  | grep -oP "href='(/recursos_mfom/[^']+\.pdf)'" \
  | sed -E "s/href='([^']+)'.*/https:\/\/www.transportes.gob.es\1/" \
  | sort -u
```

### Descargar todos los PDFs de un año

```bash
python3 << 'EOF'
import re, urllib.request, os

BASE = "https://www.transportes.gob.es"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

url = f"{BASE}/organos-colegiados/ciaf/informes-finales-de-sucesos-investigados/2008/informes-accidentes-ferroviarios-2008"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode("utf-8")

# Regex con grupos de comillas (simple o double)
pdfs = re.findall(r"href=(['\"])(/recursos_mfom/pdf/[^'\"]+?\.pdf)\1", html)
pdfs = sorted(set([p[1] for p in pdfs]))

for pdf in pdfs:
    full = BASE + pdf
    fname = os.path.basename(pdf)
    req = urllib.request.Request(full, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    with open(f"/root/workspace/CIAF/2008/{fname}", "wb") as out:
        out.write(data)
    print(f"✓ {fname} ({len(data)/1024/1024:.2f} MB)")
EOF
```

## Pitfalls

- **Browser tool → 403:** Siempre usar curl con User-Agent para esta web.
- **Comillas simples vs dobles:** Los PDFs de 2007-2014 usan `href='...'` (comillas simples), no `href="..."`. El regex debe manejar ambos con grupos: `href=(['"])(URL)\1`
- **Solo grep de `.pdf` falla:** Buscar solo `href=".*\.pdf"` ignora las comillas simples. Siempre usar múltiples patrones.
- **No asumir 404 sin probar subpáginas:** 2007-2014 dan 404 en `/infofin-AÑO` pero SÍ existen en `/AÑO/informes-accidentes-ferroviarios-AÑO`. **Siempre probar el patrón de subpágina primero.**
- **Filtros GET no funcionan:** `?field_ciaf_anyo_value=2008` no devuelve resultados. Solo URLs de año directas.
- **Contenido dinámico:** Si la página no tiene PDFs en el HTML de curl, el contenido puede estar en AJAX (Views). Intentar encontrar el endpoint AJAX o probar otras URLs.
- **Memorias: verificar siempre el conteo:** El script de descarga puede saltarse un PDF (ej: 2011 se perdió la primera vez). Verificar con `grep` del HTML original.
- **Rate limiting:** Poner `sleep 0.2-0.5` entre peticiones para no ser bloqueado.
- **PDFs duplicados:** Algunos PDFs aparecen dos veces en el HTML (diferentes enlaces al mismo archivo). Usar `set()` para deduplicar.
- **No hay API pública:** Todo el scraping es por parsing de HTML estático.

## Escalabilidad

Este patrón puede extenderse a otros órganos colegiados:
- **CIAIAC** (aviación): misma web, misma técnica, diferentes URLs
- **CIAIM** (marítimo): misma web, mismas técnicas, diferentes URLs
- **DGT** (tráfico): web diferente, adaptar técnicas

## Actualizaciones

- **2026-06-26 (v2):** Corrección importante: los patrones URL para 2007-2016 eran incorrectos. La URL real es `/MFOM/LANG_CASTELLANO/ORGANOS_COLEGIADOS/CIAF/INFORMES/YYYY/` (no `informes-accidentes-ferroviarios-YYYY`). Total corregido de 270 a ~219 PDFs. 2007 y 2008 vacíos.
- **2026-06-26 (v1):** Descubrimiento de patrón 2007-2014. Total inicial: 270 PDFs + 17 memorias anuales.
