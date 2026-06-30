# Pitfalls para Dashboards HTML Vanillas (DataHub España + similares)

## DOM Nesting en HTML Masivo (>2000 líneas)

Cuando se añaden tab-panels nuevos a un `.tab-content`, DEBEN ser hermanos (no hijos) de los paneles existentes.

**Error típico:** Añadir un `<div class="tab-panel" id="tab-nuevo">` sin cerrar el panel anterior → el nuevo panel queda como hijo del anterior → rompe TODO el layout.

**Verificación obligatoria:**
```bash
python3 -c "
import re
content = open('file.html').read()
tc = content.find('class=\"tab-content\"')
mc = content.find('id=\"map-container\">')
seg = content[tc:mc]
o = len(re.findall(r'<div[ >]', seg))
c = len(re.findall(r'</div>', seg))
print(f'Balance: {o-c}')  # Debe ser -1
"
```

**Patrón correcto de cierre:**
```html
                    </div>  <!-- cierra fuentes -->
                </div>      <!-- cierra tab-panel anterior -->
                <div class="tab-panel" id="tab-nuevo">
                    ...
                </div>      <!-- cierra tab-panel nuevo -->
```

## GitHub Pages CDN Caching

Después de `git push`, GitHub Pages sirve versiones cacheadas durante 2-5 minutos.

**Workarounds (en orden de preferencia):**
1. Verificar con `curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/file.html" | grep "contenido"` que el archivo raw SÍ tiene los cambios
2. Hard refresh: `Ctrl+Shift+R` (Chrome/Firefox) o `Cmd+Shift+R` (Mac)
3. Query param: `https://site.com/?v=timestamp`
4. Si nada funciona, esperar 5 minutos

**No diagnosticar "bugs" hasta verificar que el CDN está sirviendo la versión correcta.**

## Subagentes en Archivos Grandes (>3000 líneas)

`delegate_task` con 50 tool calls máximas no alcanza para editar un HTML monolítico de 3000+ líneas. El subagente se queda sin iteraciones.

**Regla:** 
- Archivos <1500 líneas → subagente OK
- Archivos >1500 líneas → usar `execute_code` o `patch` directamente
- Archivos >3000 líneas → SIEMPRE directo, nunca subagente

## Leaflet Choropleth Toggle

Para hacer toggleable un choropleth existente:

1. Crear `L.layerGroup()` ANTES de `L.control.layers()`
2. Añadirlo a los overlays: `L.control.layers(baseLayers, {...overlays, 'Provincias': provincesOverlay})`
3. Después de `renderChoropleth()`: `geoLayer.addTo(provincesOverlay)`
4. El `geoLayer` debe ser un layer hijo del overlay, NO añadido directamente al mapa

```javascript
let provincesOverlay = L.layerGroup();
L.control.layers(baseLayers, {
    'Provincias': provincesOverlay,
    'Parques': parksOverlay
}).addTo(map);

// Después de crear geoLayer:
function renderChoropleth(data) {
    geoLayer = L.geoJSON(data, {...}).addTo(provincesOverlay);
    // NO: geoLayer.addTo(map);
}
```

## Map Navigation on Click

Para navegar al mapa al hacer click en una lista:

```javascript
function selectItem(item) {
    map.flyTo([item.lat, item.lon], 12, { duration: 1.5 });
    // Cargar datos adicionales...
}
```

Funciona con Leaflet sin API externa. `duration: 1.5` = animación suave de 1.5 segundos.

## Datos Estáticos vs APIs Gobernamentales

Si una API gubernamental devuelve 403/HTML/error:
- Usar datos hardcodeados como fallback (ej: ESIOS renewables → 45.2%)
- NO intentar arreglar la API — el usuario quiere ver datos, no errores
- Documentar la fuente: "Fuente: [API] (datos 2023)" o "Fallback: datos hardcodeados"

## Diseño: Eliminar "Look de IA"

David Antizar rechaza explícitamente:
- **NO:** `border-left: 4px solid color` en cards (se nota IA)
- **NO:** Liquid glass, dark themes, gradientes excesivos
- **NO:** Fuentes grandes (>16px para KPIs)
- **SÍ:** Fondo blanco, sombras sutiles, hover elevación
- **SÍ:** Fuentes compactas (12-14px para labels, 14-17px para values)
- **SÍ:** Datos reales, no mockups

## Subida de Datos por Pantalla

David prefiere pantallas densas con más información visible:
- Tabs en barra horizontal arriba (no sidebar lateral)
- KPIs compactos en fila
- Charts pequeños pero informativos
- Listas clickeables que navegan al mapa
- Cada pestaña debe tener mínimo 4-6 KPIs + 1-2 charts

## Two Functions, Same API, Different DOM Targets

Cuando dos funciones hacen la misma llamada API pero actualizan elementos DOM diferentes, un error en los parámetros de la API puede causar que UNA funcione y la OTRA no — aunque la lógica sea idéntica.

**Síntoma:** "El clima funciona en la pestaña pero no en el panel de detalle"
**Causa real:** `fetchProvinceWeather()` pedía `sunrise,sunset` en `current` (error 400 silencioso), mientras `updateClimateForProvince()` no los pedía.

**Debug:**
```javascript
// Verificar qué función actualiza qué elemento
document.querySelectorAll('[id^="weather-"]').forEach(el => {
    console.log(el.id, '=', el.textContent);
});
document.querySelectorAll('[id^="detail-"]').forEach(el => {
    console.log(el.id, '=', el.textContent);
});
```

**Prevención:** Cuando hay dos funciones con API similar, comparar los parámetros fetch lado a lado antes de asumir que "la API funciona".

## Cron-Based Feature Building

Para dashboards grandes que necesitan muchas features nuevas, usar cron jobs one-shot espaciados 10-15 min. Ver `references/cron-based-dashboard-building.md` para el patrón completo.
