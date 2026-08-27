# Dashboard TimeIneco2 — Referencia Técnica

**Fecha:** 2026-06-22
**Repositorio:** Ntizar/TimeIneco2
**Archivos:** `dashboard.html`, `css/dashboard.css`, `js/dashboard.js`

## Estructura

```
TimeIneco2/
├── dashboard.html          # Entry point autocontenido
├── css/
│   └── dashboard.css       # Aurora light theme completo
├── js/
│   └── dashboard.js        # Vanilla JS, sin framework
├── data/
│   ├── ciudades-gtfs.json  # 7 ciudades con coordenadas
│   └── poblacion-cp.json   # Datos INE 2025 por CP
├── index.html              # TimeIneco original (v1)
└── server.mjs              # Backend Node.js
```

## Patrones de código clave

### 1. Cálculo de isocronas simuladas

```javascript
function calcularIsocronaSimulada(lat, lng, minutos, modo) {
  const speedKmh = MODOS[modo].speed;
  const radioKm = (speedKmh / 3.6) * minutos * 60 / 1000;
  const numPoints = 64;
  const coords = [];
  
  for (let i = 0; i < numPoints; i++) {
    const angle = (i / numPoints) * Math.PI * 2;
    const noise = calcularRuidoOrgánico(angle, modo);
    const factorForma = MODOS[modo].shapeFactor;
    const r = radioKm * (0.7 + 0.3 * noise) * factorForma;
    coords.push([
      lat + (r * Math.cos(angle)) / 111,
      lng + (r * Math.sin(angle)) / (111 * Math.cos(lat * Math.PI / 180))
    ]);
  }
  return coords;
}
```

### 2. Motor de ruido orgánico

```javascript
function calcularRuidoOrgánico(angle, modo) {
  const base = 0.5 + 0.5 * Math.sin(angle * 3 + 0.5) * Math.cos(angle * 5 + 1.2);
  const layer1 = 0.15 * Math.sin(angle * 7 + 2.1);
  const layer2 = 0.1 * Math.cos(angle * 11 + 0.8);
  const layer3 = 0.05 * Math.sin(angle * 13 + 3.4);
  const layer4 = 0.03 * Math.cos(angle * 17 + 1.5);
  return Math.max(0, Math.min(1, base + layer1 + layer2 + layer3 + layer4));
}
```

### 3. KPIs calculados por modo

```javascript
function calcularKPIs(ciudad, modo, minutos) {
  const speedKmh = MODOS[modo].speed;
  const radioKm = (speedKmh / 3.6) * minutos * 60 / 1000;
  const areaTotal = Math.PI * radioKm * radioKm;
  const densidad = CIUDAD_DATA[ciudad].poblacion / (Math.PI * 30 * 30);
  const poblacionAccesible = Math.round(densidad * areaTotal);
  const factorAccesibilidad = Math.min(1, radioKm / 30);
  const salarioMedio = Math.round(CIUDAD_DATA[ciudad].salario * factorAccesibilidad);
  const precioM2 = Math.round(CIUDAD_DATA[ciudad].alquiler_m2 * (1 - radioKm * 0.05) * 100) / 100;
  const distanciaKm = 2 * radioKm;
  const co2Anual = Math.round(distanciaKm * MODOS[modo].co2_per_km * 230);
  let costeMensual = 0;
  switch (modo) {
    case 'car': costeMensual = Math.round(distanciaKm * 0.20 * 2 * 22); break;
    case 'bus': case 'metro': costeMensual = CIUDAD_DATA[ciudad].transporte_mensual; break;
  }
  return { poblacionAccesible, salarioMedio, precioM2, co2Anual, costeMensual };
}
```

### 4. Gráfico de barras vanilla JS

```javascript
function renderizarGraficoBarras(kpis) {
  const container = document.getElementById('chart-container');
  const maxPoblacion = Math.max(...Object.values(kpis).map(k => k.poblacionAccesible));
  const colores = { car: '#2563eb', bike: '#f97316', foot: '#22c55e', bus: '#a855f7', metro: '#ef4444' };
  const html = Object.entries(kpis).map(([modo, kpi]) => {
    const height = (kpi.poblacionAccesible / maxPoblacion * 200).toFixed(1);
    const nombre = MODOS[modo].emoji + ' ' + MODOS[modo].label;
    return `<div class="bar-item" style="height:${height}px">
      <div class="bar-label">${nombre}</div>
      <div class="bar-value">${formatNum(kpi.poblacionAccesible)}</div>
    </div>`;
  }).join('');
  container.innerHTML = html;
}
```

### 5. Mapa Leaflet con isocronas

```javascript
function renderizarMapa(lat, lng, isocronas) {
  if (!map) {
    map = L.map('map').setView([lat, lng], 12);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '© OpenStreetMap, © CartoDB'
    }).addTo(map);
  } else {
    map.setView([lat, lng], 12);
  }
  // Limpiar capas anteriores
  map.eachLayer(l => { if (l !== map._tileLayer) map.removeLayer(l); });
  // Marcador origen
  L.marker([lat, lng], { icon: L.divIcon({ className: 'origin-marker', html: '📍' }) }).addTo(map);
  // Isocronas
  isocronas.forEach(({ coords, color }) => {
    L.polygon(coords, { color, fillColor: color, fillOpacity: 0.25 }).addTo(map);
  });
}
```

## Diferencias clave con TimeIneco v1

| Aspecto | TimeIneco v1 | TimeIneco2 Dashboard |
|---|---|---|
| **Módulos** | ES modules (`import/export`) | `<script>` vanilla, sin modules |
| **Servidor** | server.mjs necesario | Autocontenido, funciona solo con archivo HTML |
| **Isocronas** | ORS real + simulación v2.1 (72pts, Overpass, SRTM) | Simulación simplificada (64pts, ruido orgánico) |
| **Datos** | Demográficos reales (299 CPs, INE) | Datos demo por ciudad (7 ciudades) |
| **Complejidad** | DOCX, GTFS, NAP, informes | Foco en visualización rápida |
| **Tamaño** | ~15 archivos JS | 3 archivos (HTML, CSS, JS) |
| **Responsive** | Sidebar lateral | Top/bottom en móvil |
| **KPIs** | En informe DOCX | En dashboard interactivo |

## Notas de implementación

- No usar `import/export` en `dashboard.js` — funciona con `<script>` tag
- Leaflet se carga por CDN en `dashboard.html`
- El mapa se inicializa al cargar la página, se actualiza al cambiar filtros
- Los datos demo están hardcodeados en `dashboard.js` (CIUDAD_DATA, MODOS)
- Para producción con datos reales, reemplazar `calcularKPIs()` con llamadas al backend
