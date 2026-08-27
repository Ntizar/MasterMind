# NapMaps — Auditoría Completa y Patrones Derivados

## Caso 1: Strings truncados con *** (Causa de "se queda cargando")

### Síntoma
Loading spinner infinito, nada se renderiza, consola vacía o error de sintaxis no visible.

### Causa
Las URLs de Stadia Maps tenían `***` como placeholder de API key y les faltaba la comilla de cierre. El JS ni siquiera se parsea → `DOMContentLoaded` nunca se ejecuta → `init()` nunca se llama → loading nunca se oculta.

### Fix
Usar la variable `API_KEY` ya definida en el archivo:
```javascript
// ❌ MALO — string sin cerrar
uri: 'https://tiles.stadiamaps.com/styles/...?api_key=***\n

// ✅ BUENO — variable ya definida en el archivo
uri: 'https://tiles.stadiamaps.com/styles/...?api_key=' + API_KEY,
```

### Detección rápida
```python
with open('src/js/app.js', 'r') as f:
    for i, line in enumerate(f, 1):
        if 'uri:' in line or 'tiles:' in line:
            if line.count("'") % 2 != 0:
                print(f"Línea {i}: string sin cerrar")
```

### Second-Layer Bug
Los patches pueden dejar `***` DENTRO del template literal. Siempre verificar con `repr()` o `node -c` después de patchear.

### Verification
```bash
node -c src/js/app.js
npm run build
curl -s https://tu-app.app.nan.builders/assets/*.js | grep -c 'api_key=***'
# Debe devolver 0
```

---

## Caso 2: Edificios procedurales sin sentido (Math.random())

### Problema
`generateMadridBuildings()` genera edificios con `Math.random()` — cada reload genera una ciudad diferente. No representa nada real de Madrid.

### Impacto
- Imposible de depurar (cada carga es diferente)
- Los edificios no corresponden a la realidad
- Landmarks como "Torre Cepsa" son hardcodeados con alturas arbitrarias

### Fix recomendado
1. Usar datos GeoJSON reales de OSM (Overpass API)
2. O bien, usar un GeoJSON pre-cargado con edificios reales del centro de Madrid
3. Si se mantiene procedural, usar un seed determinístico

---

## Caso 3: Factor de conversión incorrecto (edificios microscópicos)

### Problema
```javascript
const w = 10 + Math.random() * 25;  // 10-35 unidades
const h = 10 + Math.random() * 25;
// ...
[lng, lat],
[lng + w * 0.000015, lat],
```

`25 * 0.000015 = 0.000375 grados ≈ 0.03 km = 30 metros`. Los edificios miden ~30m en un radio de 60 unidades (6.6km). Son microscópicos y se ven como puntos.

### Fix
1 grado lat ≈ 111km. Para 25m: `25 / 111000 ≈ 0.000225`.
El factor correcto es `0.000015` → `0.000225` (×15).

---

## Caso 4: Estilo satélite roto

### Problema
El estilo satélite usa un fallback CartoDB y añade un source raster ESRI encima. El resultado es un mapa CartoDB con tiles de ESRI encima — visualmente roto.

### Fix
Usar un estilo JSON válido de ESRI o implementar satélite correctamente con raster tiles sin fallback CartoDB.

---

## Caso 5: Coordenadas invertidas

### Problema
```javascript
document.getElementById('coord-val').textContent =
  `${c.lat.toFixed(3)}°N ${c.lng.toFixed(3)}°W`;
```
Muestra `°W` hardcoded. Madrid está en 3.7°W pero la lógica no maneja hemisferios.

### Fix
```javascript
const latDir = c.lat >= 0 ? 'N' : 'S';
const lngDir = c.lng >= 0 ? 'E' : 'W';
`${Math.abs(c.lat).toFixed(3)}°${latDir} ${Math.abs(c.lng).toFixed(3)}°${lngDir}`;
```

---

## Caso 6: Arquitectura monolítica

### Problema
836 líneas en un solo archivo `app.js`. No hay separación de responsabilidades.

### Impacto
- Imposible de mantener
- Imposible de reutilizar componentes
- Dificulta el debugging

### Fix
Dividir en módulos: `map.js`, `buildings.js`, `weather.js`, `ui.js`, `solar.js`

---

## Caso 7: MapLibre en bundle propio

### Problema
MapLibre GL JS (~820KB minificado) se incluye en el bundle propio. El cliente descarga 820KB + su código.

### Fix
Usar MapLibre desde CDN con importmap, o separar en chunk separado.

---

## Caso 8: Clima en main thread

### Problema
1000 partículas de clima se ejecutan en cada frame del `requestAnimationFrame` en el main thread, compitiendo con WebGL del mapa.

### Fix
Mover a Web Worker o usar canvas con WebGL en vez de 2D.

---

## Caso 9: Búsqueda inútil

### Problema
La búsqueda solo filtra 14 POIs hardcodeados. No usa geocoding real.

### Fix
Integrar Nominatim (OpenStreetMap, gratuito) o Stadia Geocoding para búsqueda real.

---

## Caso 10: Sin manejo de errores

### Problema
No hay try/catch en `init()`. Si el mapa falla, el loading se queda eterno (timeout de 12s).

### Fix
Manejar errores de carga del mapa, timeout configurable, feedback visual.

---

## Caso 11: Sin atribuciones

### Problema
`attributionControl: false` — no muestra atribuciones de CartoDB, Stadia, ESRI, que son obligatorias.

### Fix
Mostrar atribuciones en footer o panel info.

---

## Caso 12: Sin service worker

### Problema
Sin conexión a internet, no funciona nada.

### Fix
Añadir service worker para cache de tiles y app offline.

---

## Deploy Notes
- NaN.builders: Dockerfile hace npx vite build, rebuild automatico en push
- GitHub Pages: El repo usa modo legacy (branch gh-pages). Usar `peaceiris/actions-gh-pages@v4` en vez de `actions/deploy-pages@v4`.