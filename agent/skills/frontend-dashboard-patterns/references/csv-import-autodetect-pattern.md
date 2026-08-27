# CSV Import with Auto-Detection Pattern

**Session:** PLANDEMOVILIDAD Fase 3A (2026-07-14)

## Concept

Robust CSV parser that auto-detects format, maps columns to internal fields, validates data, and provides a preview before import. Used for importing survey data from external forms into the app.

## Key Pattern: Column Mapping

Define known column names and map them to internal field names:

```javascript
const COLUMNAS_CONOCIDAS = {
    // Direct mappings
    'nombre': 'nombre',
    'name': 'nombre',
    'departamento': 'departamento',
    'department': 'departamento',
    'modo_principal': 'modo_principal',
    'modo': 'modo_principal',
    'transport_mode': 'modo_principal',
    'distancia_km': 'distancia_km',
    'distance': 'distancia_km',
    'tiempo_viaje_min': 'tiempo_viaje_min',
    'travel_time': 'tiempo_viaje_min',
    // ... 30+ columns
};

// Auto-detect by matching known names
function detectarFormato(headers) {
    const mapping = {};
    let cobertura = 0;
    
    for (const h of headers) {
        const normalizado = h.toLowerCase().trim().replace(/[^a-z0-9_]/g, '_');
        if (COLUMNAS_CONOCIDAS[normalizado]) {
            mapping[normalizado] = COLUMNAS_CONOCIDAS[normalizado];
            cobertura++;
        }
    }
    
    const porcentaje = Math.round(cobertura / headers.length * 100);
    const tipo = mapping.modo_principal ? 'encuesta_movilidad' : 
                 mapping.departamento ? 'empleados' : 'generico';
    
    return { tipo, mapping, porcentajeCobertura: porcentaje };
}
```

## Key Pattern: Transport Mode Normalization

Spanish transport modes have many aliases. Normalize to canonical values:

```javascript
const NORMALIZAR_MODO = {
    // Walking
    'a pie': 'a_pie', 'pie': 'a_pie', 'andando': 'a_pie', 'walk': 'a_pie',
    'caminando': 'a_pie', 'foot': 'a_pie',
    // Bicycle
    'bicicleta': 'bicicleta', 'bici': 'bicicleta', 'bike': 'bicicleta',
    'bicycle': 'bicicleta', 'cycling': 'bicicleta',
    // Public transport
    'transporte_publico': 'transporte_publico', 'bus': 'transporte_publico',
    'autobús': 'transporte_publico', 'metro': 'transporte_publico',
    'tren': 'transporte_publico', 'tram': 'transporte_publico',
    'cercanías': 'transporte_publico', 'renfe': 'transporte_publico',
    // Car
    'coche_particular': 'coche_particular', 'coche': 'coche_particular',
    'car': 'coche_particular', 'driving': 'coche_particular',
    'coche_compartido': 'coche_compartido', 'carpool': 'coche_compartido',
};
```

## Key Pattern: CSV Parser with BOM + Quoted Fields

```javascript
function parseCSV(texto) {
    // Remove UTF-8 BOM
    if (texto.charCodeAt(0) === 0xFEFF) texto = texto.slice(1);
    
    const lineas = [];
    let actual = '';
    let enComillas = false;
    
    for (let i = 0; i < texto.length; i++) {
        const c = texto[i];
        if (c === '"') {
            if (enComillas && texto[i+1] === '"') {
                actual += '"'; i++; // escaped quote
            } else {
                enComillas = !enComillas;
            }
        } else if (c === ',' && !enComillas) {
            lineas.push(actual); actual = '';
        } else if ((c === '\n' || c === '\r') && !enComillas) {
            if (actual || lineas.length > 0) lineas.push(actual);
            if (lineas.length > 0) result.push(lineas.splice(0));
            actual = '';
        } else {
            actual += c;
        }
    }
    if (actual || lineas.length > 0) { lineas.push(actual); result.push(lineas); }
    return result;
}
```

## Key Pattern: Aggregation on Import

After importing, compute aggregates for the dashboard:

```javascript
function calcularAgregados(datos) {
    const repartoModal = {};
    const porDepto = {};
    const distribucionDistancias = { '<1km': 0, '1-3km': 0, '3-5km': 0, '5-10km': 0, '>10km': 0 };
    
    for (const d of datos) {
        // Modal split
        const modo = d.modo_principal || 'desconocido';
        repartoModal[modo] = (repartoModal[modo] || 0) + 1;
        
        // By department
        const depto = d.departamento || 'Sin departamento';
        if (!porDepto[depto]) porDepto[depto] = { total: 0, modos: {} };
        porDepto[depto].total++;
        porDepto[depto].modos[modo] = (porDepto[depto].modos[modo] || 0) + 1;
        
        // Distance distribution
        const km = parseFloat(d.distancia_km) || 0;
        if (km < 1) distribucionDistancias['<1km']++;
        else if (km < 3) distribucionDistancias['1-3km']++;
        // ... etc
    }
    
    return { repartoModal, porDepto, distribucionDistancias, totalEncuestados: datos.length };
}
```

## Pitfalls

1. **BOM UTF-8:** Excel exports CSV with BOM (`\uFEFF`). Always strip it before parsing.
2. **Quoted fields with commas:** `"Madrid, Spain"` must be parsed as one field.
3. **Newlines in quoted fields:** Some tools put newlines inside quotes.
4. **Encoding:** Always export as UTF-8 with BOM for Excel compatibility.
5. **Import vs Replace:** Give user option to merge with existing data or replace entirely.
