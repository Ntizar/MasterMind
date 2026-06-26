# Patrón: Gráfico Sankey con Plotly.js en Sistema Eléctrico Futuro

Implementación de gráfico de flujo energético Sankey en SEF. Añadido como mejora #9 del pipeline 9009 (31/05/2026).

## Estructura de archivos

- `simulator.js` → método `calcularFlujosSankey()` en `SimuladorElectrico`
- `charts.js` → función `plotSankey()` en módulo `SEF.Charts`
- `app.js` → variable `sankeyData`, cálculo en `setResults()`, render en `renderizarGraficos()`
- `index.html` → sección en tab "Análisis" con canvas `plot-sankey`

## Implementación

### 1. simulator.js — `calcularFlujosSankey()`

```javascript
calcularFlujosSankey() {
    const mix = this._ultimoMix;
    if (!mix || !mix.length) return null;
    
    // Sumar generación por tecnología (GWh)
    // Sumar demanda por sector (GWh)
    // Construir nodos: fuentes (tecnologías) + almacenamiento + sectores + pérdidas
    // Construir enlaces: cada fuente → todos los sectores (proporcional)
    // Retornar objeto con nodos[], enlaces[], generacionTotal, demandaTotal, porTecnologia[], porSector[]
}
```

**Importante:** `calcularFlujosSankey()` accede a `this._ultimoMix` y `this._ultimoDetalleDemanda`, que se almacenan en `simular()` tras `R.mix = mix` y `R.detalleDemanda = detalleDemanda`.

### 2. charts.js — `plotSankey()`

```javascript
function plotSankey(divId, sankeyData) {
    const trace = {
        type: 'sankey',
        orientation: 'h',
        direction: 'left',
        node: {
            pad: 12,
            thickness: 18,
            label: nodeLabels,
            color: nodeColors,
            hovertemplate: '<b>%{label}</b><br>Total: %{customdata:.0f} GWh<extra></extra>',
        },
        link: {
            source: enlaces.map(e => e.source),
            target: enlaces.map(e => e.target),
            value: enlaces.map(e => e.value),
            hovertemplate: '%{source.label} → %{target.label}<br>Flujo: %{value:.0f} GWh<extra></extra>',
        },
    };
    plotOrReact(divId, [trace], lyt);
}
```

**Colores:** Tecnologías usan colores del proyecto (`SEF.COLORES`), sectores usan gris suave.

### 3. app.js — integración

```javascript
let sankeyData = null;

function setResults(res) {
    // ...existing code...
    try {
        const sim = new SEF.SimuladorElectrico({ ...params });
        sim._ultimoMix = res.mix;
        sim._ultimoDetalleDemanda = res.detalleDemanda;
        sankeyData = sim.calcularFlujosSankey();
    } catch (e) {
        sankeyData = null;
    }
}

function renderizarGraficos() {
    // ...existing code...
    if (sankeyData) {
        SEF.Charts.plotSankey('plot-sankey', sankeyData);
    }
}
```

### 4. index.html — sección en tab "Análisis"

```html
<article class="nz-card nz-card--glass-soft chart-card chart-card--full">
    <div class="nz-card__header">
        <div>
            <div class="nz-card__title">Flujo energético — Gráfico Sankey</div>
            <div class="nz-card__meta">Visualización de flujos de energía...</div>
        </div>
    </div>
    <div id="plot-sankey" class="chart-host chart-host--xl"></div>
    <div class="chart-explain nz-callout nz-callout--tip">...</div>
</article>
```

## Nodos del Sankey

**Fuentes (izquierda):** Nuclear, Solar FV, Eólica terrestre, Eólica marina, Hidráulica, Gas CCGT, Importaciones, Baterías (descarga), Bombeo (descarga), V2G (descarga)

**Sectores (derecha):** Residencial, Servicios, Industria, Vehículos eléctricos, Bombas de calor, H₂ flexible

**Pérdidas:** Vertido (pérdida)

## Notas

- Plotly.js soporta sankey nativamente desde v2.0
- El gráfico se recalcula tras cada simulación
- Si no hay datos, el gráfico no se renderiza (condicional `if (sankeyData)`)
- Los flujos se distribuyen proporcionalmente entre sectores basándose en la demanda de cada sector
