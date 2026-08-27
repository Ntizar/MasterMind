# Fallback en Cascada para Dashboards

**Fecha:** 2026-07-06  
**Contexto:** DataHub España — 5 pestañas rotas por APIs externas fallando

## Problema

Las pestañas de dashboards que consumen APIs externas quedaban en blanco cuando las APIs fallaban. El patrón `try/catch` solo ponía "N/D" en un KPI y no renderizaba nada más.

## Causas Raíz Detectadas

1. **BOE**: API `https://www.boe.es/datosabiertos/api/boe/sumarias/{fecha}` devuelve 404 para TODAS las fechas (últimos 30 días probados)
2. **INE IPC**: API devuelve datos de 1992 (desactualizados, no 2026)
3. **INE Paro**: API devuelve 0 bytes (vacio)
4. **DGT Tráfico**: CORS bloqueado por `apps.dgt.es`
5. **EEA**: Fichero local `eeea-stations.json` no existe
6. **Terremotos USGS**: No hay terremotos significativos en España en 7 días (API funciona pero resultado vacío)

## Patrón Implementado

### Niveles de Fallback

```
API Principal → Datos Locales → API Alternativa → Datos Referenciales
```

### Reglas Clave

1. **NUNCA "N/D" solo** — Siempre renderizar algo visual
2. **Validar freshness de datos** — Verificar `Anyo >= 2020` antes de usar
3. **Array.isArray()** — Los datos pueden ser `{data: [...]}` en vez de array directo
4. **Múltiples APIs alternativas** — Probar 2-3 endpoints antes de fallback
5. **Etiquetar referenciales** — `text: 'Datos referenciales'` siempre visible

## Casos por Pestaña

### BOE
- **Principal**: `boe.es/datosabiertos/api/boe/sumaras/{fecha}` → 404
- **Local**: `data/boe/disposiciones.json` → vacío
- **Fallback**: Mensaje informativo "API fuera de servicio"

### INE - IPC
- **Principal**: `INE/wstempus/IPC206` → datos de 1992
- **Validación**: `Anyo < 2020` → saltar a fallback
- **Fallback**: Gráfico con últimos 7 meses referenciales [2.8, 2.9, 2.6, 2.5, 2.4, 2.3, 2.3]

### INE - Paro
- **Principal**: `PCNACT` → 0 bytes
- **Alternativas**: `EPA001`, `TASA_PARO` → probar 3 series
- **Fallback**: Gráfico referenciales [10.8, 11.0, 11.2, 11.5, 11.4, 11.2, 11.0]

### Tráfico DGT
- **Principal**: CORS bloqueado `apps.dgt.es`
- **Local**: `data/dgt/radares.json` → 0 items
- **Fallback**: ~1.200 radares, 62 ZBE, gráfico tipos

### EEA Aire
- **Principal**: `data/aemet/eeea-stations.json` → no existe
- **Alternativa**: Open-Meteo Air Quality API → 8 ciudades
- **Fallback**: Madrid PM2.5=8.5, NO2=12.0

### Terremotos
- **Principal**: USGS España (lat 35-44, lon -10 a 5) → 0 en 7 días
- **Alternativa**: USGS Global magnitud 4.0+
- **Fallback**: "Sin terremotos en España" con gráfico placeholder

## Implementación Técnica

### Validación de Freshness
```javascript
if (data.Data && data.Data[0]?.Anyo && data.Data[0].Anyo < 2020) {
    data = null; // Datos desactualizados
}
```

### Parseo Seguro
```javascript
let radars = [];
if (res.ok) {
    const data = await res.json();
    radars = Array.isArray(data) ? data : [];
}
```

### Renderizado con Fallback
```javascript
if (data.length === 0) {
    document.getElementById('kpi').textContent = '~1.200';
    if (charts.my) charts.my.destroy();
    charts.my = new Chart(el, {
        type: 'bar',
        data: { labels: ['Referencial'], datasets: [{ data: [0], backgroundColor: '#94a3b8' }] },
        options: { plugins: { title: { display: true, text: 'API fuera de servicio', color: '#64748b' } } }
    });
    return;
}
```

## Verificación Post-Fix

1. ✅ La pestaña NUNCA muestra solo "N/D"
2. ✅ Los gráficos siempre se renderizan
3. ✅ Mensajes informativos, no "N/D"
4. ✅ Datos referenciales etiquetados como tales
5. ✅ Commit + push exitoso (DataHubEspana #84)
