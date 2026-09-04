---
name: catastro-api
version: "1.0.0"
description: "API pública del Catastro español (DGC). Callejero, datos catastrales no protegidos, conversión de coordenadas. SOAP/REST/JSON. 48 provincias (excepto País Vasco y Navarra). Sin autenticación."
tags: [catastro, catastro-api, catastro-spain, parcelas, coordenadas, callejero, inmuebles, government-data]
---

# API Catastro — Datos Catastrales No Protegidos

## Resumen

La **Dirección General del Catastro (DGC)** ofrece servicios web gratuitos con información catastral no protegida (todo excepto titularidad y valor catastral).

**Dominio:** `https://ovc.catastro.meh.es`

**Formatos:** JSON y XML

**Método:** GET (REST) y SOAP

**Autenticación:** NO requerida para datos no protegidos

**Cobertura:** 48 provincias (excepto País Vasco y Navarra)

## Endpoints JSON

Base URL: `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc/json/`

### 1. ObtenerProvincias
```
GET /ObtenerProvincias
```
Devuelve listado de todas las provincias con código INE.

**Estructura:**
```json
{
  "consulta_provincieroResult": {
    "control": {"cuprov": 48},
    "provinciero": {
      "prov": [
        {"cpine": "39", "np": "CANTABRIA"},
        {"cpine": "28", "np": "MADRID"}
      ]
    }
  }
}
```

### 2. ObtenerMunicipios
```
GET /ObtenerMunicipios?Provincia={PROVINCIA}
```
- `Provincia`: nombre de la provincia (obligatorio)

**Estructura:**
```json
{
  "consulta_municipieroResult": {
    "municipiero": {
      "muni": [
        {
          "nm": "SANTANDER",
          "carto": "U",
          "locat": {"cd": "39", "cmc": "190"},
          "loine": {"cp": "39", "cm": "75"}
        }
      ]
    }
  }
}
```

### 3. ObtenerCallejero
```
GET /ObtenerCallejero?Provincia={PROVINCIA}&Municipio={MUNICIPIO}&TipoVia={TIPOVIA}&NomVia={NOMVIA}
```
- `Provincia`: nombre (obligatorio)
- `Municipio`: nombre (obligatorio)
- `TipoVia`: abreviatura tipo vía (CL=CL, AV=AVENIDA, etc.)
- `NomVia`: nombre de la vía (opcional)

### 4. ObtenerNumerero
```
GET /ObtenerNumerero?Provincia={PROVINCIA}&Municipio={MUNICIPIO}&TipoVia={TIPOVIA}&NomVia={NOMVIA}&Numero={NUMERO}
```
Devuelve referencia catastral de un número concreto.

### 5. Consulta_DNPLOC — Datos por localización
```
GET /Consulta_DNPLOC?Provincia={PROVINCIA}&Municipio={MUNICIPIO}&Sigla={SIGLA}&Calle={CALLE}&Numero={NUMERO}&Bloque={BLOQUE}&Escalera={ESCALERA}&Planta={PLANTA}&Puerta={PUERTA}
```
- `Sigla`: tipo de vía (CL, AV, PL, etc.)

**Datos devueltos (inmueble único):**
- Tipo: urbano (UR) o rústico (RU)
- Referencia catastral
- Domicilio tributario
- Uso (Residencial, Agrario, etc.)
- Superficie (m²)
- Coeficiente de participación
- Antigüedad
- Unidades constructivas
- Subparcelas (cultivos)

### 6. Consulta_DNPRC — Datos por referencia catastral
```
GET /Consulta_DNPRC?RefCat={REFCAT}
```
- `RefCat`: referencia catastral de 14, 18 o 20 caracteres

### 7. Consulta_DNPPP — Datos por polígono-parcela
```
GET /Consulta_DNPPP?Provincia={PROVINCIA}&Municipio={MUNICIPIO}&Poligono={POLIGONO}&Parcela={PARCELA}
```

**Ejemplo respuesta (Santander, polígono 1, parcela 1):**
```json
{
  "bico": {
    "bi": {
      "idbi": {"cn": "RU", "rc": {"pc1": "39900A0", "pc2": "0100001"}},
      "dt": {
        "np": "CANTABRIA",
        "nm": "SANTANDER",
        "locs": {"lors": {"lorus": {"npa": "VIRGEN DEL MAR"}}}
      },
      "ldt": "CL VIRGEN DEL MAR 161 Polígono 1 Parcela 1...",
      "debi": {"luso": "Agrario", "sfc": "539", "ant": "1920"}
    },
    "finca": {
      "dff": {"ss": "33692"},
      "infgraf": {"igraf": "https://www1.sedecatastro.gob.es/Cartografia/mapa.aspx?..."}
    }
  }
}
```

## Servicio de Coordenadas

Base URL: `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json/`

### Consulta_RCCOOR — Referencia catastral por coordenadas
```
GET /Consulta_RCCOOR?SRS={SRS}&Coordenada_X={X}&Coordenada_Y={Y}
```

### Consulta_CPMRC — Coordenadas por referencia catastral
```
GET /Consulta_CPMRC?SRS={SRS}&Provincia={PROVINCIA}&Municipio={MUNICIPIO}&RefCat={REFCAT}
```

### Consulta_RCCOOR_Distancia — Referencias por proximidad
```
GET /Consulta_RCCOOR_Distancia?SRS={SRS}&Coordenada_X={X}&Coordenada_Y={Y}
```

**Sistemas de referencia soportados:**
- `EPSG:4230` — Geográficas ED50
- `EPSG:4326` — Geográficas WGS84
- `EPSG:4258` — Geográficas ETRS89
- `EPSG:32630` — UTM 30N WGS84
- `EPSG:25830` — UTM 30N ETRS89
- `EPSG:23030` — UTM 30N ED50

## Tipos de vía (abreviaturas)

| Código | Tipo | Código | Tipo |
|--------|------|--------|------|
| CL | Calle | AV | Avenida |
| PL | Plaza | PS | Paseo |
| CR | Carretera | CT | Cuesta |
| PJ | Pasaje | TR | Travesía |
| BL | Bloque | PZ | Plazuela |
| CM | Camino | CA | Cañada |
| RD | Ronda | RB | Rambla |
| GL | Glorieta | SL | Solar |

## Ejemplo JavaScript/Leaflet

```javascript
// Buscar referencia catastral por coordenadas
async function getCatastroRef(lat, lng) {
  const url = `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json/Consulta_RCCOOR?SRS=EPSG:4326&Coordenada_X=${lng}&Coordenada_Y=${lat}`;
  const resp = await fetch(url);
  const data = await resp.json();
  const result = data.Consulta_RCCOORResult;
  if (result.control.cuerr > 0) return null;
  return result.coordenadas.coord[0]; // {pc: {pc1, pc2}, ldt: "dirección"}
}

// Obtener datos de un inmueble por referencia catastral
async function getCatastroData(refCat) {
  const url = `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc/json/Consulta_DNPRC?RefCat=${refCat}`;
  const resp = await fetch(url);
  const data = await resp.json();
  const result = data.consulta_dnprcResult;
  if (result.control.cuerr > 0) return null;
  return result.bico; // datos completos del inmueble
}

// Obtener coordenadas de una referencia catastral
async function getCatastroCoords(refCat) {
  const url = `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json/Consulta_CPMRC?SRS=EPSG:4326&RefCat=${refCat}`;
  const resp = await fetch(url);
  const data = await resp.json();
  const result = data.Consulta_CPMRCResult;
  if (result.control.cuerr > 0) return null;
  return result.coordenadas.coord[0].geo; // {xcen, ycen, srs}
}
```

## Datos descargables (requieren certificado/Cl@ve)

La Sede Electrónica del Catastro (`https://www.sedecatastro.gob.es/Accesos/SECAccDescargaDatos.aspx`) ofrece:

1. **Información alfanumérica por provincia (formato CAT)** — todos los inmuebles excepto titularidad y valor
2. **Cartografía vectorial por provincia (formato Shapefile)** — polígonos de parcelas
3. **Ficheros de Redes Topo-Geodésicas Catastrales**
4. **Cartografía Histórica catastral**

**Estos requieren:** certificado electrónico o Cl@ve + aceptación de licencia de uso

**URL descarga shapefiles:** `https://www.catastro.hacienda.gob.es/web/DescargaCartografia.html`

## Pitfalls

- **JSON BOM** → las respuestas JSON tienen BOM UTF-8 (`\ufeff`). Usar `utf-8-sig` al decodificar.
- **Nombres de endpoints** → en JSON se llaman `ObtenerProvincias`, `ObtenerMunicipios`, etc. (no `ConsultaProvincia`).
- **Provincia por nombre** → usar nombres como "CANTABRIA", "MADRID", "SANTANDER" (no códigos).
- **Referencia catastral** → puede tener 14 (finca), 18 o 20 (inmueble) caracteres. Validar longitud.
- **Sin País Vasco ni Navarra** → estos territorios tienen su propio catastro.
- **Rate limiting** → no hay límites documentados, pero ser razonable (máx ~1 req/seg).
- **WSDL/SOAP** → también disponible en `https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc?singleWsdl`

## Documentación oficial

- **Web services libres:** `https://www.catastro.hacienda.gob.es/ws/Webservices_Libres.pdf`
- **Consulta masiva:** `https://www.catastro.hacienda.gob.es/ayuda/masiva/Descripcion_consulta_masiva_datos_Catastrales_tit.pdf`
- **Esquemas XML:** `http://www.catastro.hacienda.gob.es/ws/esquemas.htm`
- **Sede Electrónica:** `https://www.sedecatastro.gob.es/`

## Uso para dashboard regional

Para un dashboard como DatoAsturias:

1. **Parcelas por zona** → `Consulta_RCCOOR_Distancia` con coordenadas del centro de la ciudad
2. **Datos de inmueble al hacer click** → `Consulta_DNPRC` con la referencia catastral
3. **Callejero interactivo** → `ObtenerCallejero` para autocompletado de direcciones
4. **Mapa catastral** → usar el servicio WMS del Catastro o los shapefiles descargados

## Comparativa de alternativas

- **[miguelfreb/ATOMCPDownloader](https://github.com/miguelfreb/ATOMCPDownloader)** — downloader ATOM INSPIRE del Catastro que maneja feeds especiales, salta los ya descargados y convierte GML→GeoParquet por CRS; automatiza la descarga masiva de parcelas que este skill prepara a mano.
