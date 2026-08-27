# APIs de Datos Abiertos Españolas — Estado Verificado (2026-06-30)

## ✅ Funcionan sin autenticación

### BOE/BORME (Registro Mercantil)
- **Sumario diario:** `https://www.boe.es/datosabiertos/api/borme/sumario/YYYYMMDD`
  - Header: `Accept: application/json`
  - Respuesta: JSON con `sumario` → `sumario` → `seccion` → arrays de actos
  - 52 provincias, ~1-5 actos por provincia diario
- **Detalle boletín:** `https://www.boe.es/datosabiertos/api/borme/boletin/BOCM-YYYYMMDD-NN`
- **Código parseo:** ver `scrapers/borme_scraper.py` en DataHubEspana

### INE (Instituto Nacional de Estadística)
- **Tabla por ID:** `https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla_id}?tip=AM&nult=N`
  - Sin key, sin CAPTCHA, sin rate limiting agresivo
  - `tip=AM` = acumulado mensual, `nult=N` = últimos N períodos
  - Tabla 4247 = paro por provincias
  - Tabla 31301 = IPC por provincias
  - Tabla 2852 = salarios medios por provincia
  - Tabla 31304 = precios vivienda por provincias

### Catastro (Dirección General del Catastro)
- **Provincias:** `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc/json/ObtenerProvincias`
- **Municipios:** `...ObtenerMunicipios?Provincia={cod}`
- **Callejero:** `...ObtenerCalles?Municipio={cod}&CodigoMunicipio={cod2}`
- **Búsqueda parcela:** `...Consulta_DNP_ABC_XMCP?Referencia={ref}`
- **⚠️ BOM UTF-8 en respuestas:** usar `utf-8-sig` al decodificar

### ESIOS/REE (Energía)
- **Demanda realtime:** `https://demanda.ree.es/vcc/curva?tun=1&curva=1` (sin auth)
- **Indicadores:** `https://api.esios.ree.es/indicators/{id}/data` (requiere key)
- **Indicator IDs:** 600 (demanda), 602 (eólica), 604 (solar), 606 (hidráulica), 607 (nuclear), 609 (término), 613 (carbono), 614 (intercambios), 10245 (fotovoltaica)
- **Key gratuita:** en `https://aemet.es` o `https://e-sios.org`

### IGN (Instituto Geográfico Nacional)
- **Terremotos último día:** `https://www.ign.es/web/resources/volcanologia/tproximos/consultas_ultimodia/40_30days.js`
- **Catálogo sismicidad:** `https://www.ign.es/web/ign/portal/sis-catalogo` (HTML scraping)
- **WMS terremotos:** `https://www.ign.es/wmts/ign-base/wmts.fcgi` (capas sísmicas)

## ✅ Funcionan con API CKAN (sin auth)

### datos.madrid.es
- **package_search:** `https://datos.madrid.es/api/3/action/package_search?rows=50`
- **package_show:** `https://datos.madrid.es/api/3/action/package_show?id={name}`
- **671 datasets** verificados
- **⚠️ Web catálogo en mantenimiento** — usar solo la API CKAN

### opendata.aragon.es
- **package_search:** `https://opendata.aragon.es/api/3/action/package_search?rows=50`
- **2,430 datasets** verificados
- **CKAN estándar** — mismo patrón que datos.madrid.es

## ⚠️ Requieren key gratuita

### AEMET (Agencia Meteorológica)
- **API:** `https://opendata.aemet.es/opendata/api/`
- **Key gratuita** en `https://aemet.es/api`
- **Endpoints:** predicción, observación, climatología

### NAP Transportes
- **API:** `https://nap.transportes.gob.es/api/v2/`
- **Header:** `ApiKey={key}`
- **161 datasets GTFS** (~0.65 GB total)
- **⚠️ Enlaces S3 caducan en 15 min** — descargar rápido

## ✅ datos.gob.es — Catálogo Nacional (ACTUALIZADO 2026-06-30)

**La portal web está bloqueado por WAF, pero la API de catálogo SÍ funciona:**
- **Endpoint:** `https://datos.gob.es/apidata/catalog/dataset.json?_page={page}`
- **Formato DCAT:** respuestas de 10 datasets por página, paginación por `_page`
- **⚠️ CRÍTICO:** los datos están bajo `data["result"]["items"]`, NO bajo `data["items"]`
- **~5,000+ datasets** del catálogo nacional accesibles vía API
- **Sin auth, sin CAPTCHA** — solo necesita User-Agent estándar
- **Código de parseo:** `scrapers/datos_gob_scraper.py` en DataHubEspana
- **Estructura por dataset:** título (es/en), descripción, territorio, temas, distribuciones (formato + URL)

```python
# Parseo correcto de datos.gob.es
resp = requests.get("https://datos.gob.es/apidata/catalog/dataset.json?_page=0")
data = resp.json()
items = data["result"]["items"]  # ⚠️ NO data["items"]
for item in items:
    titulo = item["title"][0]["_value"]  # Lista de dicts con _lang
    dists = item.get("distribution", [])
    for d in dists:
        formato = d["format"]["value"].split("/")[-1].upper()
        url = d.get("accessURL", "")
```

## ❌ Bloqueados / caídos desde servidor

### Portales CKAN autonómicos — la mayoría caídos (VERIFICADO 2026-06-30)
De 10+ portales testeados, SOLO 2 funcionan:
- ✅ **opendata.aragon.es** — 2,430 datasets
- ✅ **datos.comunidad.madrid** — 2,304 datasets
- ✅ **datos.madrid.es** — 671 datasets (Ayuntamiento)
- ❌ opendata.asturias.es — offline (connection refused)
- ❌ opendata.euskadi.eus — 404
- ❌ abertos.xunta.gal — 404
- ❌ analisi.transparenciacatalunya.cat — 404
- ❌ www.juntadeandalucia.es — 404
- ❌ catalogo.navarra.es — offline
- ❌ www.carm.es — offline
- ❌ datosabiertos.jcyl.es — offline

### Portales internacionales CKAN
- ✅ **datos.gob.cl** (Chile) — 3,114 datasets
- ✅ **datos.gob.ar** (Argentina) — 1,236 datasets (500+ pág 1, errores en paginación)

### IDEE WMS — todos bloqueados (VERIFICADO 2026-06-30)
- servicios.ign.es — ConnectionResetError
- wms.mapa.ign.es — timeout
- www.ign.es/wms — 404
- **Solución:** usar datos IGN descargados directamente (JSON terremotos funciona)

### BDNS Subvenciones — offline (VERIFICADO 2026-06-30)
- subvenciones.mrrf.es — offline
- subvenciones.inclusion.gob.es — offline
- **Solución:** usar BOE secciones D/E para subvenciones (cuando la API funcione)

### BOE API — estructura funciona pero vacía (VERIFICADO 2026-06-30)
- Endpoint `https://www.boe.es/datosabiertos/api/boe/sumario/YYYYMMDD` devuelve 200 + JSON
- Pero las secciones tienen `items: []` vacíos para todas las fechas testeadas
- **Posible causa:** API nueva sin datos históricos, o cambio de formato
- **El BORME SÍ funciona** con datos completos

## Patrón de descubrimiento rápido

```bash
# Test CKAN:
curl -s "https://PORTAL/api/3/action/package_list" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('result',[])))"

# Listar datasets de un CKAN:
curl -s "https://PORTAL/api/3/action/package_search?rows=1000" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for r in d['result']['results']:
    print(f\"{r['name']}: {r['title']}\")
"
```
