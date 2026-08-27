---
name: boe-borme-api
version: "1.0.0"
description: "API oficial del BOE/BORME: datos abiertos del Boletín Oficial del Estado y Registro Mercantil. Sumarios diarios, XML de actos mercantiles, legislación consolidada, datos auxiliares. 52 provincias, sin autenticación."
tags: [boe, borme, datos-abiertos, gobierno, registro-mercantil, legislacion]
---

# API BOE/BORME — Datos Abiertos del Estado

## Resumen

API REST pública, gratuita, sin API key. Ofrecida por la Agencia Estatal Boletín Oficial del Estado.

**Base URL:** `https://www.boe.es/datosabiertos/api/`

**Formatos:** JSON y XML (indicar con header `Accept: application/json` o `Accept: application/xml`)

**Método:** Solo GET. POST/PUT devuelven 403.

**Publicación:** Todos los días laborables (lunes-viernes). No publica sábados, domingos ni festivos de Madrid.

## Endpoints disponibles

### 1. Sumario BORME (Registro Mercantil)

```
GET /datosabiertos/api/borme/sumario/{fecha}
```

- **Parámetro:** `fecha` — formato ISO 8601 `AAAAMMDD` (obligatorio)
- **Devuelve:** Sumario diario con todas las provincias
- **Ejemplo:** `curl -H "Accept: application/json" "https://www.boe.es/datosabiertos/api/borme/sumario/20260629"`

**Estructura de respuesta:**
```json
{
  "status": {"code": "200", "text": "ok"},
  "data": {
    "sumario": {
      "metadatos": {
        "publicacion": "BORME",
        "fecha_publicacion": "20260629"
      },
      "diario": [{
        "numero": "122",
        "sumario_diario": {
          "identificador": "BORME-S-2026-122",
          "url_pdf": {"szBytes": "227852", "szKBytes": "223", "texto": "https://www.boe.es/borme/dias/2026/06/29/pdfs/BORME-S-2026-122.pdf"}
        },
        "seccion": [{
          "codigo": "A",
          "nombre": "SECCIÓN PRIMERA. Empresarios. Actos inscritos",
          "item": [
            {
              "identificador": "BORME-A-2026-122-33",
              "titulo": "ASTURIAS",
              "url_pdf": {"szBytes": "...", "szKBytes": "...", "pagina_inicial": "32169", "pagina_final": "32171", "texto": "..."},
              "url_html": "https://www.boe.es/diario_borme/txt.php?id=BORME-A-2026-122-33",
              "url_xml": "https://www.boe.es/diario_borme/xml.php?id=BORME-A-2026-122-33"
            }
          ]
        }]
      }]
    }
  }
}
```

**Secciones del BORME:**
- **Sección A** (código "A"): SECCIÓN PRIMERA — Empresarios. Actos inscritos (una entrada por provincia)
- **Sección B** (código "B"): SECCIÓN PRIMERA — Otros actos publicados en el Registro Mercantil
- **Sección C** (código "C"): SEGUNDA — Anuncios y avisos legales (tiene sub-apartados)

### 2. XML de actos mercantiles por provincia

```
https://www.boe.es/diario_borme/xml.php?id={identificador}
```

- **Parámetro:** `id` — identificador del item (ej: `BORME-A-2026-122-33`)
- **Devuelve:** XML con cada acto mercantil estructurado
- **NO necesita header Accept** — siempre devuelve XML

**Estructura del XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<documento fecha_actualizacion="20260629T071725Z">
  <metadatos>
    <identificador>BORME-A-2026-122-33</identificador>
    <titulo>ASTURIAS</titulo>
    <diario>Boletín Oficial del Registro Mercantil</diario>
    <diario_numero>122</diario_numero>
    <seccion codigo="A">SECCIÓN PRIMERA. Empresarios. Actos inscritos</seccion>
    <fecha_publicacion>20260629</fecha_publicacion>
    <pagina_inicial>32169</pagina_inicial>
    <pagina_final>32171</pagina_final>
    <url_pdf>https://www.boe.es/borme/dias/2026/06/29/pdfs/BORME-A-2026-122-33.pdf</url_pdf>
  </metadatos>
  <texto>
    <p class="articulo">306100 - MAR DE ROCHEL SL.</p>
    <p class="parrafo">Reducción de capital. Importe reducción: 1.197.000,00 Euros...</p>
    <p class="articulo">306103 - MARCONIX23 SOCIEDAD LIMITADA.</p>
    <p class="parrafo">Constitución. Comienzo de operaciones: 10.06.26. Objeto social: CNAE: 6421...</p>
  </texto>
</documento>
```

**Tipos de acto en el XML (clases CSS):**
- `class="articulo"` → Nombre de la sociedad (formato: `NOMBRE - TIPO SOCIEDAD`)
- `class="parrafo"` → Descripción del acto mercantil

**Actos mercantiles más comunes:**
- **Constitución** → nueva empresa (incluye CNAE, domicilio, capital, administrador)
- **Disolución** → cierre de empresa (voluntaria/forzosa)
- **Nombramientos** → cargo de persona (administrador, consejero, liquidador)
- **Ceses/Dimisiones** → baja de persona
- **Modificaciones estatutarias** → cambio de capital, estatutos
- **Reducción/Ampliación de capital** → cambios financieros
- **Otros conceptos** → aprobación de reglamentos, etc.

### 3. HTML de actos mercantiles

```
https://www.boe.es/diario_borme/txt.php?id={identificador}
```

- Misma información que XML pero en formato HTML legible

### 4. PDF de actos mercantiles

```
https://www.boe.es/borme/dias/{AAAA}/{MM}/{DD}/pdfs/{identificador}.pdf
```

- PDF firmado electrónicamente (único formato oficial y auténtico)

### 5. Sumario BOE (Boletín Oficial del Estado)

```
GET /datosabiertos/api/boe/sumario/{fecha}
```

- Misma estructura que BORME pero para legislación
- Secciones: Disposiciones generales, Autoridades, Otras disposiciones, Administración de Justicia, Anuncios

### 6. Legislación consolidada

```
GET /datosabiertos/api/legislacion-consolidada/estado/{id}
```

- Acceso a texto consolidado de leyes
- Documentación: `https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf`

### 7. Datos auxiliares

```
GET /datosabiertos/api/datos-auxiliares/materias
GET /datosabiertos/api/datos-auxiliares/ambitos
GET /datosabiertos/api/datos-auxiliares/departamentos
GET /datosabiertos/api/datos-auxiliares/rangos
GET /datosabiertos/api/datos-auxiliares/estado-consolidacion
```

- Tablas de referencia: materias (temas jurídicos), ámbitos geográficos, departamentos ministeriales, rangos normativos

## Mapeo de provincias → identificadores BORME

Las provincias se identifican por su posición en el sumario diario. El `titulo` del item contiene el nombre de la provincia. Ejemplos verificados:

| Provincia | Ejemplo identificador |
|---|---|
| Albacete | BORME-A-2026-122-02 |
| Almería | BORME-A-2026-122-04 |
| Asturias | BORME-A-2026-122-33 |
| Barcelona | BORME-A-2026-122-08 |
| Madrid | BORME-A-2026-122-28 |
| Cantabria | BORME-A-2026-122-39 |

**Para obtener tu provincia:** Llamar al sumario diario y buscar por `titulo` el nombre de la provincia.

## Cómo funciona DatoAsturias con el BORME

DatoAsturias (datoasturias.com) usa el BORME para mostrar:
1. **Constituciones** de nuevas empresas por día
2. **Disoluciones** de empresas
3. **Capital movilizado** (suma de capitales de constituciones)
4. **Nombramientos/Ceses** de cargos
5. **Modificaciones estatutarias**
6. **Gráfico de evolución histórica** (borme-historico)

**Su endpoint:** `https://datoasturias.com/api/dashboard.php?action=borme`

**Proceso:** Scrapea el XML del BOE → parsea los `<p class="articulo">` y `<p class="parrafo">` → extrae tipo de acto, nombre empresa, domicilio, capital, CNAE → sirve JSON normalizado.

## Código Python de ejemplo

```python
import requests
import xml.etree.ElementTree as ET
from datetime import date

def get_borme_provincia(fecha: str, provincia: str) -> dict:
    """Obtiene el BORME de una provincia para una fecha dada."""
    # 1. Obtener sumario diario
    url = f"https://www.boe.es/datosabiertos/api/borme/sumario/{fecha}"
    resp = requests.get(url, headers={"Accept": "application/json"})
    data = resp.json()
    
    diario = data["data"]["sumario"]["diario"][0]
    
    # 2. Buscar la provincia en la sección A
    for sec in diario["seccion"]:
        if sec["codigo"] == "A":
            items = sec.get("item", [])
            if isinstance(items, dict):
                items = [items]
            for item in items:
                if provincia.upper() in item["titulo"].upper():
                    # 3. Obtener XML detallado
                    xml_url = item["url_xml"]
                    xml_resp = requests.get(xml_url)
                    root = ET.fromstring(xml_resp.content)
                    
                    # 4. Parsear actos
                    actos = []
                    for p in root.findall(".//texto/p"):
                        if p.get("class") == "articulo":
                            actos.append({"empresa": p.text})
                        elif p.get("class") == "parrafo" and actos:
                            actos[-1]["detalle"] = p.text
                    
                    return {
                        "provincia": item["titulo"],
                        "fecha": fecha,
                        "identificador": item["identificador"],
                        "pdf": item["url_pdf"]["texto"],
                        "actos": actos
                    }
    return None

# Ejemplo: BORME de Asturias hoy
resultado = get_borme_provincia("20260629", "ASTURIAS")
print(f"Actos: {len(resultado['actos'])}")
for acto in resultado["actos"][:5]:
    print(f"  {acto['empresa']}: {acto.get('detalle', '')[:80]}")
```

## Pitfalls

- **Sin header Accept** → devuelve XML por defecto (no JSON). SIEMPRE usar `-H "Accept: application/json"` para JSON.
- **Días sin publicación** → sábados, domingos y festivos de Madrid. La API devuelve 404 para esas fechas.
- **Provincia no encontrada** → puede ser que no haya actos mercantiles ese día para esa provincia (devuelve sección vacía).
- **XML con encoding UTF-8** → asegurar que el parser maneje `<?xml version="1.0" encoding="UTF-8"?>`.
- **Formato de fecha** → SOLO `AAAAMMDD` (ej: `20260629`). No acepta guiones ni barras.
- **Las URLs de XML/HTML/PDF cambian con la fecha** → siempre obtener del sumario diario, no hardcodear.
- **Sección C tiene apartados** → la sección de anuncios legales tiene sub-apartados (apartado), no items directos.

## Documentación oficial

- **PDF BORME:** `https://www.boe.es/datosabiertos/documentos/APIsumarioBORME.pdf`
- **PDF BOE:** `https://www.boe.es/datosabiertos/documentos/APIsumarioBOE.pdf`
- **PDF Legislación:** `https://www.boe.es/datosabiertos/documentos/APIconsolidada.pdf`
- **FAQ BORME:** `https://www.boe.es/datosabiertos/faq/borme.php`
- **FAQ BOE:** `https://www.boe.es/datosabiertos/faq/boe.php`
- **XSD Sumario BORME:** `https://www.boe.es/datosabiertos/definitions/download_schema.php?id=diario-borme-sumario` (ZIP con sumario-borme.xsd + tipos.xsd)
- **XSD Sumario BOE:** `https://www.boe.es/datosabiertos/definitions/download_schema.php?id=diario-boe-sumario`

## Reutilización

Condiciones de reutilización: `https://www.boe.es/informacion/aviso_legal/index.php#reutilizacion`

La información es de libre reutilización para fines comerciales y no comerciales, citando la fuente.
