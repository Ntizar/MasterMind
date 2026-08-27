# Yahoo Finance para frontend — Patrón de integración

**Fecha:** 2026-05-31  
**Contexto:** Proyecto frontend puro (sin backend Node.js) que necesita datos de mercado en tiempo real.

## Problema

La API de ESIOS/REE requiere autenticación (`x-api-key`) y no soporta CORS desde el navegador.

## Solución

Usar Yahoo Finance query1 API como alternativa:
- Sin API key
- Soporta CORS (funciona desde navegador)
- JSON parseable
- Datos actualizados diariamente

## Implementación completa

### 1. Caché en localStorage con TTL

```javascript
const CACHE_TTL_MS = 60 * 60 * 1000;
const CACHE_KEY = 'sef_ree_api_cache';

function cacheGet(key) {
    try {
        const raw = localStorage.getItem(CACHE_KEY);
        if (!raw) return null;
        const cache = JSON.parse(raw);
        if (cache[key] && (Date.now() - cache[key].ts < CACHE_TTL_MS)) return cache[key].data;
        return null;
    } catch (e) { return null; }
}
```

### 2. Fetch Yahoo Finance

```javascript
function fetchYahooFinance(ticker) {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(ticker)}?range=1d&interval=1d`;
    return fetch(url, { headers: { 'Accept': 'application/json' } })
        .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
        .then(data => {
            const result = data.chart?.result?.[0];
            if (!result) return null;
            const quotes = result.indicators?.quote?.[0];
            const meta = result.meta;
            if (!quotes || !meta) return null;
            return { precio: quotes.close[0], meta };
        })
        .catch(() => null);
}
```

## Reglas de oro

1. **Siempre tener fallback:** Yahoo Finance puede fallar. Mantener datos estáticos de REE como respaldo.
2. **Caché con TTL:** 1 hora es un buen balance entre frescura y evitar llamadas excesivas.
3. **No confundir unidades:** Yahoo devuelve precios en la moneda del ticker (EUR para TTF, USD para CO2).
4. **No es datos en tiempo real puro:** Actualiza una vez al día. Para datos intradiarios reales, se necesita backend con API key de ESIOS.
5. **No usar para generación/demanda:** Solo tiene datos de mercado (precios).

## Tickers de energía útiles

| Ticker | Nombre | Moneda | Uso |
|--------|--------|--------|-----|
| `TTF=F` | Gas Natural TTF | EUR | Precio gas natural Europa |
| `EURO0=DXX` | EU ETS CO2 | EUR | Precio carbono UE |
| `CL=F` | Crude Oil WTI | USD | Petróleo crudo USA |
| `BZ=F` | Crude Oil Brent | USD | Petróleo crudo Europa |
