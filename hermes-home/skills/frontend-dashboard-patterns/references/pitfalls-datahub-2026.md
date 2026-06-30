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

## 4. Tabs Responsive (15+ pestañas)
```css
.tabs-row { display: flex; flex-wrap: wrap; gap: 4px; }
.tab-btn { font-size: 10px; padding: 3px 8px; flex-shrink: 0; }
```

## 5. GitHub Pages CDN Cache
Archivo raw correcto pero CDN sirve versión vieja. Usuario debe hard refresh `Ctrl+Shift+R`.

## 6. Datos absurdos
- Nieve en ciudades en verano → filtrar, mostrar solo estaciones de esquí
- Nieve en cm, no metros (snow_depth × 100)
- Al seleccionar provincia → actualizar TODAS las pestañas (no solo clima)
