# Pitfalls Críticos — DataHub España (junio 2026)

## 1. DOM Nesting de Tab Panels
**REGLA:** Los `div.tab-panel` deben ser **HERMANOS**, no hijos unos de otros.

```html
<!-- ✅ CORRECTO -->
<div class="tab-content">
    <div class="tab-panel" id="tab-clima">...</div>
    <div class="tab-panel" id="tab-agua">...</div>
</div>

<!-- ❌ INCORRECTO — si falta un </div>, todos los paneles quedan anidados -->
```

**Verificación pre-commit:**
```python
import re
content = open('index.html').read()
tc = content.find('class="tab-content"')
mc = content.find('id="map-container">')
seg = content[tc:mc]
o = len(re.findall(r'<div[ >]', seg))
c = len(re.findall(r'</div>', seg))
print(f'DOM balance: {o-c}')  # Debe ser -1
```

## 2. Open-Meteo: Parámetros current vs daily
`sunrise` y `sunset` **NO** son válidos en `current=`. Solo en `daily=`. Falla silenciosa.

```javascript
// ❌ FALLA
`?current=temperature_2m,sunrise,sunset`
// ✅ CORRECTO
`?current=temperature_2m&daily=sunrise,sunset`
```

**Parámetros current válidos:** temperature_2m, relative_humidity_2m, apparent_temperature, precipitation, rain, snowfall, snow_depth, weather_code, cloud_cover, pressure_msl, surface_pressure, wind_speed_10m, wind_direction_10m, wind_gusts_10m

## 3. Unidades Open-Meteo
- `snow_depth` → **metros** (×100 para cm)
- `wind_speed_10m` → km/h
- `precipitation` → mm

## 4. Tabs Responsive (35+ pestañas)
```css
.tabs-row { display: flex; flex-wrap: wrap; gap: 4px; }
.tab-btn { font-size: 10px; padding: 3px 8px; }
/* NO flex-shrink: 0 — eso causa scroll horizontal invisible */
```
Tres breakpoints: Desktop (>1024px), Tablet (768-1024px, sidebar 45% + mapa), Mobile (<768px, vertical).

## 4b. Wave7 Revert (junio 2026)
Commit wave7 (Térmica, Mareas, Eólica, Nubosidad, Aire Ext.) corrompió el HTML con 3+ líneas fusionadas/truncadas. Se intentó fix incremental y falló. **Se revirtió el commit completo.**

Lección: cuando un commit tiene múltiples corrupciones estructurales en un monolito, **revert > parchear individualmente**. Ver `references/pitfalls-html-dashboards.md#commits-corruptos` para el patrón.

Para re-aplicar wave7 features: hacerlo **incrementalmente**, un feature a la vez, con validación `vm.Script()` tras cada cambio.

## 5. GitHub Pages CDN Cache
Archivo raw correcto pero CDN sirve versión vieja. Usuario debe hard refresh `Ctrl+Shift+R`.

## 6. Datos absurdos
- Nieve en ciudades en verano → filtrar, mostrar solo estaciones de esquí
- Nieve en cm, no metros (snow_depth × 100)
- Al seleccionar provincia → actualizar TODAS las pestañas (no solo clima)

## 7. Naming mismatch de funciones
Cuando se renombra una función (ej: `fetchFlood` → `fetchFloods`), SIEMPRE buscar TODAS las referencias. Un mismatch causa `ReferenceError` silencioso en init() que rompe la pestaña entera.

**Verificación pre-commit:**
```bash
grep -n 'fetchNOMBRE\|fetchNOMBRE[^s]' index.html
# O completo:
python3 -c "
import re; c=open('index.html').read()
init=re.search(r'async function init\(\)\s*\{(.*?)\n    \}',c,re.DOTALL)
calls=set(re.findall(r'(\w+)\(\)',init.group(1)))
for f in calls:
    if f not in ['now','sort','init','parseInt'] and f'function {f}' not in c:
        print(f'❌ {f}() called but NOT defined')
"
```

## 8. ESIOS API — Auth variable por indicador
La API de ESIOS/REE no requiere auth para TODOS los indicadores. Algunos funcionan sin token, otros devuelven 403.

| Indicador | Funciona sin auth | Notas |
|---|---|---|
| 1001 (PVPC) | ✅ Sí | 120 values/día |
| 600 (Pool OMIE) | ✅ Sí | 288 values/día |
| 1293 (Demanda real) | ❌ No | Requiere `x-api-key` |
| 1294 (Renovables) | ❌ No | Requiere `x-api-key` |
| 2052 (Demanda prevista) | ❌ No | Requiere `x-api-key` |

**Patrón de diagnóstico:**
```bash
curl -s "https://api.esios.ree.es/indicators/ID" -H "Accept: application/json" | python3 -c "
import json,sys; d=json.load(sys.stdin)
if 'Status' in d: print(f'AUTH REQUIRED: {d[\"Status\"]}')
else: print(f'OK: {len(d.get(\"indicator\",{}).get(\"values\",[]))} values')
"
```

**Para indicadores que requieren auth:** necesitar token ESIOS configurado en el dashboard. Sin él, mostrar fallback o "N/D" es comportamiento esperado.

## 9. Init-time data fetching para panel KPIs
Si un fetch solo se llama en交互 del usuario (ej: clickear provincia), los KPIs del panel principal quedan vacíos.

```javascript
// ❌ MAL — AQI solo se carga al clickear provincia
if (centroid) fetchAirQuality(centroid[0], centroid[1]);

// ✅ BIEN — también en init() con coordenadas por defecto
async function init() {
    // ... otros fetches ...
    fetchAirQuality(40.4168, -3.7038); // Madrid como default
}
```

**Regla:** Todo KPI visible en el panel principal debe tener un fetch durante `init()`, no solo en交互.

## 10. Panel vacío sin contenido
Si un panel tiene `<div class="tab-panel" id="tab-X">` pero no tiene KPIs, canvas ni selects, está vacío y el usuario lo detecta al instante. Verificar que cada panel tiene al menos 500 bytes de contenido HTML.
