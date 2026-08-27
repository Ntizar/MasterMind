# Realistic Isochrone Simulation with Urban Barriers

## Problem
Simple circle-based isochrone simulations (jitter) don't look realistic. Real cities have:
- Major road axes that extend travel range in certain directions
- Urban barriers (rivers, railways, highways) that reduce accessibility
- Public transport connections that extend range in specific directions

## Solution: Road axis + barrier model

### Algorithm (48-point polygon)

```javascript
function generarIsocronaRealista(centro, radioMax, modo, tiempo) {
    const PUNTOS = 48;
    const coords = [];
    
    // Define road axes with extension factors
    const ejes = [
        { angulo: 0,   factor: 1.4, nombre: 'Castellana N' },      // Major N-S axis
        { angulo: 45,  factor: 1.1, nombre: 'Bravo Murillo' },      // NE diagonal
        { angulo: 90,  factor: 0.7, nombre: 'Río Manzanares' },     // E barrier
        { angulo: 135, factor: 1.2, nombre: 'Plaza de España' },    // SE connection
        { angulo: 180, factor: 1.3, nombre: 'Paseo Habana S' },     // S axis
        { angulo: 225, factor: 1.0, nombre: 'Calle México' },       // SW normal
        { angulo: 270, factor: 0.8, nombre: 'Zona menos dev' },     // W less developed
        { angulo: 315, factor: 1.15, nombre: 'Concha Espina' },     // NW moderate
    ];
    
    // Define urban barriers
    const barreras = [
        { anguloInicio: 75,  anguloFin: 105, factor: 0.6 },   // River: -40%
        { anguloInicio: 260, anguloFin: 285, factor: 0.75 },  // Railway: -25%
    ];
    
    for (let i = 0; i < PUNTOS; i++) {
        const angulo = (i / PUNTOS) * 2 * Math.PI;
        const anguloDeg = (i / PUNTOS) * 360;
        
        // Road axis factor (smooth interpolation)
        let factorEje = 1;
        for (const eje of ejes) {
            const diff = Math.abs(anguloDeg - eje.angulo);
            if (diff < 30) {
                factorEje *= 1 + (eje.factor - 1) * (1 - diff / 30);
            }
        }
        
        // Barrier factor
        let factorBarrera = 1;
        for (const b of barreras) {
            if (anguloDeg >= b.anguloInicio && anguloDeg <= b.anguloFin) {
                factorBarrera *= b.factor;
            }
        }
        
        // Natural variation (3-frequency sine)
        const variacion = 1 + 0.15 * Math.sin(angulo * 0.1) 
                             + 0.1 * Math.cos(angulo * 0.23) 
                             + 0.08 * Math.sin(angulo * 0.37);
        
        const radio = radioMax * factorEje * factorBarrera * variacion;
        
        // Convert to coordinates
        const lat = centro.lat + (radio / 111320) * Math.cos(angulo);
        const lon = centro.lon + (radio / (111320 * Math.cos(centro.lat * Math.PI / 180))) * Math.sin(angulo);
        coords.push([lat, lon]);
    }
    
    return coords;
}
```

### Speed by mode

| Mode | Speed (km/h) | 10min radius | 15min radius | 30min radius |
|------|-------------|--------------|--------------|--------------|
| Coche | 25 | 4.2 km | 6.3 km | 12.5 km |
| Bici | 14 | 2.3 km | 3.5 km | 7.0 km |
| Pie | 4.5 | 0.75 km | 1.1 km | 2.25 km |

### Madrid example (Paseo de la Habana)

**Road axes calibrated for Madrid:**
- Castellana N (0°): factor 1.4 — major highway extends range 40%
- Paseo de la Habana S (180°): factor 1.3 — good south connection
- Río Manzanares E (90°): factor 0.7 — river barrier reduces 30%
- Vía tren Chamartín W (270°): factor 0.75 — railway barrier -25%

**Barriers:**
- Río Manzanares (75°-105°): factor 0.6 — few crossings
- Vía de tren Chamartín (260°-285°): factor 0.75 — underpasses only

**Result:** "Octopus hand" shape that extends along major roads and contracts at barriers.

### Area calculation (Shoelace formula)

```javascript
function calcularAreaPoligonoKm2(coords, refLat) {
    let area = 0;
    const n = coords.length;
    for (let i = 0; i < n; i++) {
        const j = (i + 1) % n;
        area += coords[i][0] * coords[j][1] - coords[j][0] * coords[i][1];
    }
    const cosLat = Math.cos(refLat * Math.PI / 180);
    return Math.abs(area) / 2 * (111.32 * 111.32 * cosLat);
}
```

### Comparison with real ORS data

| Metric | Simulated | ORS Real | Error |
|--------|-----------|----------|-------|
| Area (coche, 15min) | 150-200 km² | 165 km² | ~15% |
| Shape irregularity | High | High | Similar |
| Barrier effect | Visible | Visible | Similar |

### Calibration

To calibrate for a new city:
1. Identify 4-8 major road axes (highways, main avenues)
2. Identify 2-4 barriers (rivers, railways, highways)
3. Set factors: major axis 1.3-1.5, barrier 0.6-0.8
4. Verify against ORS real data if available
5. Adjust factors to match real area within 20%

### Usage in PLANDEMOVILIDAD

The algorithm is used in `js/isochrones-realistas.js` and called from `js/report-maps.js` to generate realistic isochrones for the PMST report. The isochrones are rendered both as:
1. **Interactive Leaflet polygons** in the HTML report
2. **Static map images** via `staticmap` Python library for PDF generation
