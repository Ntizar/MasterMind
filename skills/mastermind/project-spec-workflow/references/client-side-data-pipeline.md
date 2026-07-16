# Client-Side Data Pipeline Architecture

Patrón completo para SPAs que ingieren datos, los procesan y generan informes. Extraído de PLANDEMOVILIDAD v2.0.

## Pipeline completo

```
Formulario HTML → CSV → Parser → State (IndexedDB) → Diagnóstico → APIs externas → Informe HTML con mapas
```

## Módulos requeridos

| Módulo | Responsabilidad | Fichero ejemplo |
|--------|----------------|-----------------|
| **Formulario** | Input de datos por usuario | `encuesta.html` |
| **CSV Parser** | Detectar formato, mapear columnas, validar | `csv-import.js` |
| **State** | Estado centralizado + persistencia IndexedDB | `state.js` |
| **APIs externas** | GBFS, ORS, Nominatim con fallback | `api-gbfs.js`, `api-ors.js`, `api-nominatim.js` |
| **Diagnóstico** | Cálculos sobre datos | `diagnostico.js` |
| **Informe** | Generación HTML con 22+ capítulos | `report.js` |
| **Mapas embebidos** | Leaflet en informe estático | `report-maps.js` |
| **Enriquecimiento** | Carga datos API antes de informe | `report-enrich.js` |

## Orden de creación recomendado

1. **State** (state.js) — Fundamento de todo
2. **CSV Parser** (csv-import.js) — Para tener datos reales rápido
3. **APIs** (api-*.js) — Con fallback para que siempre funcione
4. **Diagnóstico** — Usa state + APIs
5. **Informe** — Usa todo lo anterior
6. **Mapas embebidos** — Leaflet en informe

## CSV Parser — Pattern

```javascript
// Detección automática de formato
function detectarFormato(headers) {
    if (headers.includes('modo_principal')) return 'encuesta';
    if (headers.includes('departamento') && headers.includes('puesto')) return 'empleados';
    return 'generico';
}

// Normalización de valores (crítico para datos de usuarios)
const NORMALIZACION = {
    'bus': 'transporte_publico',
    'metro': 'transporte_publico',
    'bici': 'bicicleta',
    'coche solo': 'coche_conductor',
};
```

## API Integration — Fallback Pattern

```javascript
export async function calcularIsocrona(lon, lat, modo, minutos) {
    const apiKey = localStorage.getItem('ors_api_key');
    if (apiKey) {
        try {
            const resp = await fetch(ORS_URL + modo, { ... });
            if (resp.ok) return { geojson: await resp.json(), real: true };
        } catch(e) { /* fall through */ }
    }
    return simulateIsochrone(lat, lon, modo, minutos);
}
```

## Leaflet Maps in Static HTML

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map-tp" style="height:400px"></div>
<script type="module">
import { initReportMaps } from './js/report-maps.js';
document.addEventListener('DOMContentLoaded', () => setTimeout(() => initReportMaps(app), 800));
</script>
```

## Pitfalls

- **CSV BOM:** Excel exporta CSV con BOM UTF-8. Parser debe strippear al inicio.
- **IndexedDB async:** `initState()` es async. No llamar funciones de state antes de que termine.
- **API rate limits:** Nominatim = 1 req/s. ORS free = 2000 req/day. Stagger entre requests.
- **Leaflet en PDF:** Mapas NO se renderizan en Ctrl+P. Solo preview web. Para PDF, html2canvas.
- **Window.pmstApp timing:** Módulos ES ejecutan antes del inline script. No asignar en módulo si inline sobreescribe.
- **Overpass API:** Fuente más fiable para paradas TP. Query: `node["highway"="bus_stop"](bbox);out body 50;`.
- **Browser-to-disk:** Para HTML >100KB generado en browser, usar mini-servidor Python + POST. Ver `references/browser-file-transfer.md`.
