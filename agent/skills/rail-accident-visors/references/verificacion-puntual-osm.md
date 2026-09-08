# Verificación puntual de residuos 'mal' con OSM/Overpass (sesión era-visor 07/09/2026)

Receta para la ronda final de casos geolocalizados mal cuando quedan pocos y el usuario
exige evidencia por registro (zona, origen/destino, PK) antes de cerrar.

## Paso 1 — fuente textual
- JSON: `json/ES/*.json` (buscar por grep de contenido: `grep -il "villanueva de g" json/ES/*.json`;
  el stem del fichero NO siempre contiene el expediente).
- PDF: `pdfs/ES/*.pdf`. `pypdf` falla en algunos CIAF → usar PyMuPDF (`fitz`) con el
  python del sistema `C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe`.
- Sacar literal del informe: municipio(s), origen→destino del tren, línea, PK con su
  notación (25+100, 25/100, 25,100), estación.

## Paso 2 — nodo exacto en Overpass (OpenData ADIF sobre OSM, CC BY 4.0)
Desde Python (curl puede salir bloqueado por filtros del entorno; urllib funciona):

```python
import json, urllib.request, urllib.parse
q = '[out:json][timeout:25];nwr["railway"~"station|halt"]["name"~"Mataró",i](41.49,2.39,41.55,2.46);out body center 15;'
u = 'https://overpass-api.de/api/interpreter?data=' + urllib.parse.quote(q)
req = urllib.request.Request(u, headers={'User-Agent': 'era-visor-corrector/1.0'})
d = json.load(urllib.request.urlopen(req, timeout=60))
for el in d['elements']:
    lat = el.get('lat') or el.get('center',{}).get('lat')
    print(el['type'], el['id'], lat, el.get('lon') or el['center']['lon'], repr(el['tags'].get('name')), el['tags'].get('operator'))
```

- Hosts de respaldo: `overpass.kumi.systems`, `z.overpass-api.de` (intentar en cadena, ~3s de cortesía entre peticiones).
- La consulta-union con varias líneas `(a;b;);out;` a veces da 400 — mejor una bbox por petición.
- Si el nombre no sale con filtro `railway`: quitar el filtro (las estaciones de
  clasificación/mercaderías a veces son yard sin tag station) y ensanchar bbox; para
  localidades usar Nominatim `search?q=...&format=json` (UA propia obligatoria).
- **El `name` devuelto ES la verificación**: no escribir ninguna coord que no haya
  aparecido en la respuesta. Citar `OSM node/<id> '<name>'` en `fuente_geo`.

## Paso 3 — escribir en el JSON
`ubicacion.update(lat, lng, estacion, metodo_geo="estacion_adif", fuente_geo="OSM node/… (OpenData ADIF, CC BY 4.0) …")` —
`metodo_geo` propio por clase permite deshacer la tanda entera. Ojo: `glob` con
corchetes literales en el stem (`...-CIAF[1].json`) no casa; usar listdir+substring.

## Paso 4 — cadena y respuesta
`python scripts/geocodificar_via.py ES && geocodificar_estacion.py ES && revisar_localizacion.py ES && consolidar.py ES && verificar_todo.py ES`
(cadena larga → terminal background=True). Verificar que la coord objetivo CAMBIÓ y el
registro salió de la lista residual; bump `VERSION_DATOS`; commit. Contestar AL USUARIO
por caso: zona real (municipio/provincia correctos), origen–destino, PK, coordenada y
por qué saltaba el aviso (p.ej. CIAF declaró Huesca donde es Zaragoza: 64/2012).

## Hallazgos de esta tanda (para no repetir investigación)
- 64/2012 Villanueva de Gállego–Zuera: provincia del CIAF errónea (dice Huesca, es
  Zaragoza); PK 25,100 de la 200 resuelto interpolando SIN filtro provincial.
- Zaragoza Delicias (44/2013 y gemelo 27/2011): cambiador real 41.658683,-0.910775;
  a 11 m del recodo de la 200; ramal 060 sin geometría ADIF → 'OTRA vía' es artefacto.
- Nodos OSM confirmados: Tarragona Clasificación 41.13260,1.22954 (node 2272953656);
  Salou (estación actual 'Salou-Port Aventura' en la 600); Carmonita 38.70051,-6.15301
  (node 5436494761 — NO confundir con el pueblo, que está a ~1.7 km de la vía 510);
  Mataró 41.53584,2.44428; Vilassar de Mar estación 41.50049,2.38983 (26/2008 PK
  26,100); Elx Parc/Sant Vincent 41.5712,2.0900 ya era correcto (el PK raíz 657,718
  del LLM era erróneo: es el km 0 del desvío a la 700; el bueno 435,900 de la 336).
