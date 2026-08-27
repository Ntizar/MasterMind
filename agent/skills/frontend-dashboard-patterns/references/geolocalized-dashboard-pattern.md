# Patrón de Dashboard Geolocalizado

## Concepto
Al seleccionar una entidad geográfica (provincia, ciudad, puerto), TODAS las pestañas del dashboard deben actualizarse con datos relevantes para esa ubicación. No solo la pestaña activa.

## Componentes

### 1. Barra de contexto
Muestra la entidad seleccionada y permite limpiar la selección.

```html
<div id="province-context" class="province-context hidden">
    <div class="context-info">
        <span class="context-label">📍</span>
        <span class="context-name" id="context-province-name">-</span>
        <span class="context-code" id="context-province-code">-</span>
    </div>
    <button class="context-clear" id="context-clear">✕ Restaurar vista nacional</button>
</div>
```

```css
.province-context {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border-bottom: 1px solid #bfdbfe;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: slideDown 0.3s ease;
}
.province-context.hidden { display: none; }
.context-name { font-weight: 600; color: #1e40af; }
.context-code { color: #64748b; font-size: 0.9em; margin-left: 8px; }
.context-clear {
    background: #1e40af; color: white; border: none;
    padding: 6px 14px; border-radius: 6px; cursor: pointer;
    font-size: 0.85em; transition: background 0.2s;
}
.context-clear:hover { background: #1e3a8a; }
@keyframes slideDown { from { max-height: 0; opacity: 0; } to { max-height: 60px; opacity: 1; } }
```

### 2. Sincronización de pestañas
Al seleccionar entidad → llamar a funciones de actualización de cada pestaña.

```javascript
function selectProvince(code) {
    selectedProvince = code;
    const data = provinces[code];
    
    // 1. Actualizar barra de contexto
    showContextBar(data.nombre, code);
    
    // 2. Actualizar panel detalle
    updateProvinceDetail(data);
    
    // 3. Sincronizar TODAS las pestañas
    updateClimateForProvince(code);
    updateEconomyForProvince(code);
    updatePopulationForProvince(code);
    updatePortsForProvince(code);
    updateWaterForProvince(code);
    updateTransportForProvince(code);
    
    // 4. Zoom en mapa
    map.flyTo(provinceCentroids[code], 8);
}
```

### 3. Restaurar vista nacional
Al limpiar selección → restaurar datos nacionales en todas las pestañas.

```javascript
function restoreDefaultTabValues() {
    // Restaurar KPIs nacionales
    updateKPIs(nationalData);
    
    // Restaurar gráficos con datos nacionales
    renderPopulation();      // Datos INE nacionales
    renderEconomyDetail();   // Datos BOE/BORME nacionales
    renderPorts();           // Todos los puertos
    renderWater();           // Todas las cuencas
}
```

### 4. Coordenadas de centroides
Para hacer API calls por ubicación:

```javascript
const provinceCentroids = {
    '01': [37.39, -5.99],   // Sevilla
    '02': [41.65, -0.88],   // Zaragoza
    '03': [43.36, -8.40],   // A Coruña (Galicia)
    '04': [39.57, 2.65],    // Palma (Baleares)
    '05': [28.12, -15.43],  // Las Palmas (Canarias)
    '06': [43.46, -3.81],   // Santander
    // ... 52 provincias
};
```

## APIs geolocalizadas

### Clima (Open-Meteo)
```javascript
async function fetchClimate(lat, lon) {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}` +
        `&current=temperature_2m,wind_speed_10m,relative_humidity_2m,weather_code` +
        `&daily=sunrise,sunset&timezone=Europe/Madrid`;
    const res = await fetch(url);
    return await res.json();
}
```

### Marina (Open-Meteo Marine)
```javascript
async function fetchMarine(lat, lon) {
    const url = `https://marine-api.open-meteo.com/v1/marine?latitude=${lat}&longitude=${lon}` +
        `&current=wave_height,wave_direction,wave_period,swell_wave_height` +
        `&timezone=Europe/Madrid`;
    const res = await fetch(url);
    return await res.json();
}
```

### Cascada de APIs (Weather + Marine)
```javascript
async function fetchLocationData(lat, lon) {
    const [weather, marine] = await Promise.allSettled([
        fetchClimate(lat, lon),
        fetchMarine(lat, lon)
    ]);
    
    return {
        climate: weather.status === 'fulfilled' ? weather.value : null,
        marine: marine.status === 'fulfilled' ? marine.value : null
    };
}
```

## Pitfalls

1. **No solo pestaña activa:** David verifica que al cambiar de pestaña, los datos de la provincia sigan ahí. Si solo actualizas la pestaña activa, al volver a otra verás datos nacionales.

2. **APIs solo para costas:** Marine API falla para coordenadas terrestres. Verificar si la provincia tiene costa antes de llamar.

3. **Cache por provincia:** Si el usuario navega rápido entre provincias, cachear resultados para evitar llamadas duplicadas.

4. **Loading states:** Mostrar spinner mientras se cargan datos de la provincia seleccionada. No dejar la UI con datos viejos.

5. **Coordenadas correctas:** Usar coordenadas de la capital/provincia, no del centroide del polígono GeoJSON (que puede estar en el mar para islas).

6. **setTxt() helper para updates seguros:** Al actualizar DOM desde APIs, usar helper que verifica que el elemento existe antes de escribir. Evita errores silenciosos cuando un ID no existe:
   ```javascript
   const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; else console.warn('Element not found:', id); };
   ```

7. **showToast en errores de API:** Cuando una API falla al cargar datos de provincia, mostrar toast de error + valores fallback en vez de dejar la UI con "—" eterno:
   ```javascript
   } catch (err) {
       showToast(`Error cargando datos de ${nombre}: ${err.message}`, 'error', 3000);
       setTxt('weather-temp', 'No disponible');
   }
   ```

## Ejemplo completo: DataHub España

- **Repo:** `Ntizar/DataHubEspana`
- **Pestañas:** 16 (Panel, Energía, Clima, Agua, Economía, Transporte, Medio Ambiente, Catastro, Población, Economía detallada, Calidad Aire, Demografía, Puertos, Polen, Inundaciones, Suelo)
- **Layout v2.5:** Tabs horizontales en `#tab-navbar` (no en sidebar)
- **APIs:** Open-Meteo (weather/marine/air-quality/flood/soil/pollen), INE, USGS, ESIOS
- **Mapa:** Leaflet + Layer Control (carreteras, ferrocarriles) + GeoJSON provincias choropleth
- **Gráficos:** Chart.js (barras, doughnuts, líneas)
- **Error handling:** setTxt() helper + showToast en errores API + fallback values
