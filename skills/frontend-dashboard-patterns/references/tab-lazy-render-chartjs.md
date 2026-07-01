# Tab Lazy-Render con Chart.js — DataHub España

## Problema

Charts.js no redimensiona correctamente cuando se renderizan en un panel oculto (`display: none`). Si las funciones de renderizado se ejecutan en `init()` antes de que el usuario navegue a la pestaña, los gráficos aparecen como cajas vacías o con tamaño 0.

## Síntomas

- Pestaña con KPIs visibles pero canvas en blanco
- No hay errores en la consola
- Al redimensionar ventana o cambiar pestaña, el gráfico aparece

## Causa

Chart.js lee el tamaño del canvas en el momento de `new Chart()`. Si el canvas está dentro de un `display: none` (panel de tab oculto), el tamaño es 0 → gráfico invisible.

## Solución: Lazy-Render con Flag

### 1. Tab click handler con lazy render

```javascript
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        const tab = btn.getAttribute('data-tab');
        document.getElementById('tab-' + tab).classList.add('active');
        
        // Lazy render: solo renderizar la primera vez que se abre la pestaña
        if (tab === 'ambiente' && !window.__ambienteRendered) { window.__ambienteRendered = true; renderParks(); }
        if (tab === 'catastro' && !window.__catastroRendered) { window.__catastroRendered = true; renderCatastro(); }
        if (tab === 'poblacion' && !window.__poblacionRendered) { window.__poblacionRendered = true; renderPopulation(); }
        if (tab === 'economia-det' && !window.__economiaDetRendered) { window.__economiaDetRendered = true; renderEconomyDetail(); }
        if (tab === 'calidad-aire' && !window.__calidadAireRendered) { window.__calidadAireRendered = true; fetchAirQuality(); }
        
        // Resize charts after tab becomes visible
        setTimeout(() => {
            Object.values(charts).forEach(c => { if (c && c.resize) c.resize(); });
        }, 100);
    });
});
```

### 2. Eliminar llamadas de init()

Quitar de `init()` todas las llamadas que dependen de tabs visibles:

```javascript
// ❌ ANTES (rompe charts en tabs ocultos)
renderParks();
renderPopulation();
renderEconomyDetail();
fetchAirQuality();

// ✅ DESPUÉS (lazy render en tab click)
// renderPopulation, renderEconomyDetail, renderParks, fetchAirQuality son lazy-rendered
```

### 3. Función de lazy render mínima

```javascript
function renderCatastro() {
    // Catastro card se llena en province click handler.
    // Esta función solo asegura visibilidad al abrir tab.
    const card = document.getElementById('catastro-card');
    if (card) card.style.display = 'block';
}
```

## Reglas

1. **NUNCA** llamar funciones de renderizado de gráficos en `init()` si el canvas está dentro de un tab-panel oculto
2. **SIEMPRE** usar flags `window.__xxxRendered` para evitar doble renderizado
3. **SIEMPRE** hacer `resize()` después de cambiar de tab (setTimeout 100ms)
4. **Verificar** que cada función lazy-render existe antes de añadirla al tab handler — de lo contrario `TypeError` silencioso

## Verificación Pre-Commit

```python
content = open('index.html').read()
# 1. DOM balance
opens = content.count('<div')
closes = content.count('</div>')
assert opens == closes, f'DOM BROKEN: {opens} vs {closes}'

# 2. Todas las funciones lazy-render existen
lazy_funcs = ['renderParks', 'renderCatastro', 'renderPopulation', 'renderEconomyDetail', 'fetchAirQuality']
for f in lazy_funcs:
    assert f'function {f}' in content, f'{f}() no definida'

# 3. No hay llamadas a funciones lazy en init()
init_match = re.search(r'async function init\(\)\s*\{(.*?)\n    \}', content, re.DOTALL)
if init_match:
    init_body = init_match.group(1)
    for f in lazy_funcs:
        assert f'{f}()' not in init_body, f'{f}() llamada en init() — debe ser lazy'
```

## Referencias

- `references/switchtab-pattern.md` — patrón switchTab + lazy load
- `references/threejs-lazy-tab-loading.md` — lazy loading con Three.js
- `references/pitfalls-datahub-2026.md` — pitfalls DataHub
