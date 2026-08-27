# Inyección de Variables de Entorno al Frontend

Patrón para servir API keys al frontend sin hardcodearlas en el HTML.

## Problema

El frontend necesita llamar a ORS API, pero la key no puede estar en el HTML (visible en DevTools). Sin embargo, el frontend ES modules no tiene `process.env`.

## Solución: Inyección en el servidor

### Servidor (server.mjs)

```javascript
// Inyectar variables de entorno en el HTML
let body = data.toString();
const orsKey = process.env.ORS_API_KEY || '';
if (orsKey && body.includes('<script type="module"')) {
    const envScript = `<script>window.__ENV = { ORS_API_KEY: "${orsKey}" };</script>`;
    body = body.replace('<script type="module"', envScript + '\n  <script type="module"');
}
res.end(body);
```

### Frontend (config.js)

```javascript
const key = typeof process !== 'undefined' && process.env?.ORS_API_KEY
    ? process.env.ORS_API_KEY
    : (typeof window !== 'undefined' ? window.__ENV?.ORS_API_KEY : '');
```

## Reglas

- **NUNCA hardcodear API keys en el HTML**
- **NUNCA subir .env a Git**
- **SIEMPRE inyectar en el servidor** antes de servir el HTML
- **SIEMPRE fallback a `process.env`** para el caso de SSR/Node.js

## Caso real: TimeIneco

- `.env` contiene `ORS_API_KEY=eyJvcmciOi...`
- `server.mjs` inyecta `window.__ENV.ORS_API_KEY` en cada request HTML
- `js/config.js` lee `window.__ENV.ORS_API_KEY` en el navegador
- El servidor NaN pasa `ORS_API_KEY` como env var al contenedor
