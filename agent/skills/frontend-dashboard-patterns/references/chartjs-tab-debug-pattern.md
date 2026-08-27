# Chart.js Tab Debug Pattern — Diagnóstico y Fix

## Problema

Charts.js en tabs ocultas de dashboards HTML masivos (>500KB) — diagnósticar por qué no se renderizan y cómo arreglar.

## Diagnóstico Rápido (3 pasos)

### Paso 1: Verificar DOM balance
```bash
python3 -c "c=open('index.html').read();assert c.count('<div')==c.count('</div>'),'BROKEN';print('OK')"
```

### Paso 2: Verificar existencia de canvas y funciones
```python
for tab in ['tab-termica', 'tab-mareas', 'tab-eolica', 'tab-nubosidad', 'tab-aireext']:
    assert f'id="{tab}"' in content, f"{tab} MISSING"
for canvas in ['chart-termica', 'chart-mareas', 'chart-eolica', 'chart-nubosidad', 'chart-aireext-limits', 'chart-aireext-hourly']:
    assert f'id="{canvas}"' in content, f"Canvas #{canvas} MISSING"
for fn in ['fetchTermica', 'fetchMareas', 'fetchEolica', 'fetchNubosidad', 'fetchAireExt']:
    assert f'function {fn}' in content, f"{fn}() MISSING"
```

### Paso 3: Verificar Chart.js versión
```python
assert 'chart.js@4.4.4' in content, "Chart.js version mismatch"
```

## Errores Comunes en Charts de Tabs

### 1. Concatenación de datos de múltiples ciudades en un solo chart
**Síntoma:** Chart con 192+ puntos cuando debería tener 24.
**Causa:** El código itera TODAS las ciudades y concatena sus horas en un solo array.
**Fix:** Usar solo la primera ciudad (principal) para el chart 24h.

```javascript
// ❌ MALO
results.forEach((data, idx) => {
    data.hourly.time.forEach((time, i) => {
        chartLabels.push(time);
        chartData.push(data.hourly.value?.[i]);
    });
});

// ✅ BUENO
const mainData = results[0];
const times = mainData.hourly.time;
const startIdx = Math.max(0, times.length - 24);
for (let i = startIdx; i < times.length; i++) {
    chartLabels.push(formatTime(times[i]));
    chartData.push(mainData.hourly.value[i] ?? null);
}
```

### 2. Demasiados datasets en un chart
**Síntoma:** Chart saturado, ilegible, leyenda infinita.
**Causa:** Un dataset por puerto + sub-dataset por métrica = 20+ datasets.
**Fix:** Limitar a top N (3-5) o agregar datos.

```javascript
const topPorts = results
    .map((data, idx) => ({ data, idx }))
    .filter(x => x.data && x.data.current)
    .sort((a, b) => (b.data.current.wave_height || 0) - (a.data.current.wave_height || 0))
    .slice(0, 3);
```

### 3. Tipo de chart incorrecto
**Síntoma:** Barras apiladas cuando se quieren líneas comparativas.
**Causa:** `type: 'bar'` para datos temporales.
**Fix:** Cambiar a `type: 'line'` y ajustar datasets.

### 4. Tooltip con valores null
**Síntoma:** `Cannot read property 'toFixed' of null`.
**Causa:** Dataset tiene nulls y tooltip llama a `.toFixed()` sin verificar.
**Fix:** `if (ctx.parsed.y == null) return null;`

## Verificación Post-Fix

```python
checks = [
    ("Chart usa datos principales", "mainData" in content or "madridData" in content),
    ("Chart limitado", "slice(0, 3)" in content),
    ("Tooltip null-safe", "parsed.y == null" in content),
    ("Tipo chart correcto", "type: 'line'" in content),
]
```

## Regla de Oro

> **Cada chart debe mostrar máximo 24-48 puntos de datos y 2-5 datasets.**
> Si supera esos límites, el chart es ilegible → limitar datos o dividir en múltiples charts.
