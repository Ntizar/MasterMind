# Catálogo de APIs de Datos Abiertos Españolas

**Última actualización:** 2026-06-30
**Origen:** Análisis de DatoAsturias.com + verificación directa de endpoints

## Resumen

Inventario de 35+ fuentes de datos públicas españolas mapeadas desde el dashboard DatoAsturias. Categorizadas por facilidad de acceso.

---

## 1. API BOE — BORME (Registro Mercantil)

**La fuente más valiosa para dashboards regionales de economía.**

### Acceso
- **Base:** `https://www.boe.es/datosabiertos/api/borme/`
- **Auth:** Ninguna (API pública, sin key)
- **Formato:** JSON (sumario) + XML (detalle)
- **Cobertura:** 50 provincias + Ceuta + Melilla

### Endpoints

#### Sumario diario (JSON)
```
GET /datosabiertos/api/borme/sumario/YYYYMMDD
Accept: application/json
```
Devuelve la lista de provincias del día con sus IDs de sección.

#### Detalle por provincia (XML)
```
GET /diario_borme/xml.php?id=BORME-A-YYYY-NNN-XX
```
Donde XX es el código de provincia (33=Asturias, 28=Madrid, 39=Cantabria).

#### PDF completo
```
GET /borme/dias/YYYY/MM/DD/pdfs/BORME-A-YYYY-NNN-XX.pdf
```

### Estructura del XML
```xml
<documento>
  <metadatos>
    <identificador>BORME-A-2026-122-33</identificador>
    <titulo>ASTURIAS</titulo>
    <fecha_publicacion>20260629</fecha_publicacion>
  </metadatos>
  <texto>
    <p class="articulo">306100 - MARCONIX23 SOCIEDAD LIMITADA.</p>
    <p class="parrafo">Constitución. Comienzo de operaciones: 10.06.26.
    Objeto social: CNAE: 6421. Domicilio: C/ FLORENCIO RODRIGUEZ, 27.
    Capital: 10.000,00 Euros. Nombramientos. Adm. Unico: PABLO ABEL.</p>
  </texto>
</documento>
```

### Parseo del XML
- `<p class="articulo">` → Nombre de empresa + número de registro
- `<p class="parrafo">` → Descripción del acto

### Tipos de acto extraíbles
| Tipo | Palabra clave | Datos |
|------|--------------|-------|
| Constitución | "Constitución" | nombre, domicilio, capital, CNAE, administrador |
| Disolución | "Disolución" + "Extinción" | empresa, tipo |
| Nombramiento | "Nombramientos" | cargo, persona |
| Ceses | "Ceses/Dimisiones" | cargo, persona |
| Modificación estatutaria | "Modificaciones estatutarias" | capital, estatutos |

### Código de parseo básico
```python
import xml.etree.ElementTree as ET
import requests
import re

def get_borme_provincia(fecha: str, provincia_nombre: str) -> list:
    """Obtiene el BORME de una provincia para una fecha dada."""
    resp = requests.get(
        f"https://www.boe.es/datosabiertos/api/borme/sumario/{fecha}",
        headers={"Accept": "application/json"}
    )
    sumario = resp.json()
    xml_url = None
    for diario in sumario["data"]["sumario"]["diario"]:
        for seccion in diario["seccion"]:
            for item in seccion.get("item", []):
                if item["titulo"].upper() == provincia_nombre.upper():
                    xml_url = item["url_xml"]
                    break
    if not xml_url:
        return []
    resp = requests.get(xml_url)
    root = ET.fromstring(resp.content)
    actos = []
    nombre = ""
    for p in root.findall(".//p"):
        if p.get("class") == "articulo":
            nombre = (p.text or "").strip()
        elif p.get("class") == "parrafo" and nombre:
            texto = (p.text or "").strip()
            acto = parsear_acto(nombre, texto)
            if acto:
                actos.append(acto)
            nombre = ""
    return actos

def parsear_acto(nombre_empresa: str, texto: str) -> dict | None:
    t = texto.lower()
    emp = nombre_empresa.split(" - ", 1)[-1].strip().rstrip(".")
    if "constitución" in t:
        cap = re.search(r'Capital:\s*([\d.,]+)\s*Euros', texto)
        cnae = re.search(r'CNAE:\s*(\d+)', texto)
        dom = re.search(r'Domicilio:\s*(.+?)(?:\.|Capital)', texto)
        return {"tipo": "constitucion", "empresa": emp,
                "capital": cap.group(1) if cap else None,
                "cnae": cnae.group(1) if cnae else None,
                "domicilio": dom.group(1).strip() if dom else None}
    elif "disolución" in t and "extinción" in t:
        return {"tipo": "disolucion", "empresa": emp}
    elif "nombramientos" in t:
        return {"tipo": "nombramiento", "empresa": emp}
    elif "ceses" in t or "dimisiones" in t:
        return {"tipo": "cese", "empresa": emp}
    return None
```

### ⚠️ Pitfalls BORME
- **IDs de provincia cambian entre días** — siempre obtener del sumario del día
- **Días festivos no publican** — sumario devuelve array vacío
- **Los domingos no publican BORME** — usar el viernes anterior
- **Encoding UTF-8** — asegurar decodificación correcta del XML
- **Número de registro** es orden dentro de sección, NO ID único nacional

---

## 2. AEMET — Meteorología

### API REST (key gratuita)
- **Base:** `https://opendata.aemet.es/opendata/api/`
- **Auth:** API key gratuita en aemet.es

### XML público (sin key) — lo que usa DatoAsturias
```
https://www.aemet.es/xml/municipales/localidades_XX_NNNNN.xml
```

### Áreas de aviso
| Código | Nombre |
|--------|--------|
| 61 | Asturias |
| 07 | Cantabria |
| 13 | Madrid |

---

## 3. REE/ESIOS — Energía

- **API:** `https://api.esios.ree.es` (key gratuita)
- **Demanda tiempo real (sin key):** `https://demanda.ree.es/...`
- **Detalle completo:** Ver skill `esios-complete`

---

## 4. INE — Estadísticas

### API REST (sin key)
```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{id}?tip=AM&nult=N
```

### Tablas útiles
| ID | Contenido |
|----|-----------|
| 4247 | EPA: Paro por provincia y sexo |
| 2852 | EPA: Paro por sector y provincia |
| 66241 | Salarios por decil y provincia |
| 56936 | Población por municipio y sexo |
| 2856 | Afiliación SS por provincia |
| 31304 | Pensiones por tipo y provincia |

---

## 5. Puertos del Estado — Mar

```
https://www.puertos.es/sites/default/files/contenidos/simo/XX.json
```
XX = código puerto (gi=Gijón, av=Avilés).

---

## 6. Confederaciones Hidrográficas — Embalses

| Confederación | URL | CCAA |
|---------------|-----|------|
| Cantábrico | saihcantabrico.es | Asturias, Cantabria |
| Ebro | saihceb.com | Aragón, Cataluña |
| Guadalquivir | saihguadalquivir.es | Andalucía |
| Júcar | saihjucar.com | C. Valenciana |
| Miño-Sil | saihmiñosil.es | Galicia |
| Segura | saisegura.com | Murcia |
| Tajo | saihcuenca | Madrid, C. Mancha |

---

## 7. IGN — Sismicidad

```
https://www.ign.es/web/resources/volcanologia/tproximos/todos_visualizadores.js
```

---

## 8. Calidad del Aire — Redes autonómicas

Cada CCAA tiene su propia red (scraping individual):
- Asturias: AsturAire (asturaire.asturias.es)
- Madrid: REDECAM (redcam.comunidad.madrid)
- Cataluña: XAC
- Andalucía: AAA
- País Vasco: Euskalmet

---

## 9. DGT — Tráfico

```
https://infocar.dgt.es/etraffic/data?
```

---

## 10. Contratación Pública

```
https://contrataciondepa.com/plc/licitaciones
```

---

## 11. BDNS — Subvenciones

```
https://www.infosubvenciones.es/bdnrest/bdn/api/bdnBusqueda
```

---

## 12. Ministerio Industria — Carburantes

```
https://energia.serviciosmin.gob.es
```

---

## 13. Copernicus/Sentinel — Satélite

```
https://land.copernicus.eu/
```

---

## Clasificación por facilidad

### ✅ Fáciles (API REST pública)
- BOE/BORME, INE, IGN, REE, ESIOS, BDNS, AEMET

### ⚠️ Medias (scraping limpio)
- DGT, Puertos del Estado, Carburantes, Contratación Pública

### 🔶 Difíciles (scraping complejo)
- Calidad aire autonómica, SAIH embalses, 112 emergencias, Salud, Seguridad Social
