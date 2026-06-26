# Proxy ORS + Nominatim — Servidor Node.js completo

Implementación completa de un servidor proxy Node.js que:
- Sirve archivos estáticos (HTML, CSS, JS)
- Proxea ORS isochrones (POST) con API key oculta
- Proxea Nominatim geocoding (GET) sin API key
- Health check endpoint

## server.mjs (completo)

```javascript
import http from 'node:http';
import https from 'node:https';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = parseInt(process.env.PORT || '4000');
const DIST = path.join(__dirname);

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.geojson': 'application/geo+json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
};

const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');

  // === HEALTH ===
  if (req.url === '/healthz') {
    const ORS_KEY = process.env.ORS_API_KEY;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ready',
      uptime: process.uptime(),
      checks: {
        ors_api: typeof ORS_KEY === 'string' && ORS_KEY.length > 20
      }
    }));
    return;
  }

  // === PROXY ORS ISOCHRONE ===
  if (req.method === 'POST' && req.url.startsWith('/isochrone')) {
    const ORS_KEY = process.env.ORS_API_KEY;
    if (!ORS_KEY) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'ORS_API_KEY no configurada', fallback: true }));
      return;
    }

    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { profile, locations, range } = JSON.parse(body);
        const bodyObj = {
          locations: [locations],
          range,
          range_type: 'time',
          attributes: ['area']
        };

        const proxyReq = https.request({
          hostname: 'api.openrouteservice.org',
          path: `/v2/isochrones/${profile}`,
          method: 'POST',
          headers: {
            'Authorization': ORS_KEY,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json, application/geo+json'
          }
        }, (proxyRes) => {
          let data = '';
          proxyRes.on('data', chunk => data += chunk);
          proxyRes.on('end', () => {
            res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
            res.end(data);
          });
        });
        proxyReq.on('error', (err) => {
          res.writeHead(502);
          res.end(JSON.stringify({ error: err.message, fallback: true }));
        });
        proxyReq.write(JSON.stringify(bodyObj));
        proxyReq.end();
      } catch (err) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: err.message }));
      }
    });
    return;
  }

  // === PROXY NOMINATIM ===
  if (req.url.startsWith('/geocode')) {
    const url = new URL(req.url, 'http://localhost');
    const query = url.searchParams.get('q');
    const type = url.searchParams.get('type') || 'search';

    let nominatimUrl;
    if (type === 'reverse') {
      const [lat, lon] = query.split(',').map(Number);
      nominatimUrl = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=es`;
    } else {
      nominatimUrl = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=5&accept-language=es`;
    }

    https.get(nominatimUrl, {
      headers: { 'User-Agent': 'TimeIneco/1.0 (timeineco@antizar.es)' }
    }, (proxyRes) => {
      let data = '';
      proxyRes.on('data', chunk => data += chunk);
      proxyRes.on('end', () => {
        res.writeHead(proxyRes.statusCode, { 'Content-Type': 'application/json' });
        res.end(data);
      });
    }).on('error', (err) => {
      res.writeHead(502);
      res.end(JSON.stringify({ error: err.message }));
    });
    return;
  }

  // === ARCHIVOS ESTÁTICOS ===
  let filePath = path.join(DIST, req.url.split('?')[0]);
  if (filePath === DIST + '/') filePath = path.join(DIST, 'index.html');
  if (!filePath.startsWith(DIST)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      // SPA fallback
      fs.readFile(path.join(DIST, 'index.html'), (e2, d2) => {
        if (e2) { res.writeHead(500); res.end('Error'); return; }
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(d2);
      });
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache, no-store, must-revalidate'
    });
    res.end(data);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Servidor → http://0.0.0.0:${PORT}`);
});
```

## .env

```
ORS_API_KEY=eyJvcmciOiI1YjNj...
NAP_API_KEY=
PORT=4000
```

## Arranque (IMPORTANTE)

```bash
node --env-file=.env server.mjs
```

## Dockerfile

```dockerfile
FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=4000
COPY . .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
RUN chown -R appuser:appgroup /app
USER appuser
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:4000/healthz || exit 1
EXPOSE 4000
CMD ["node", "--env-file=.env", "server.mjs"]
```

## Debugging checklist

1. `node --env-file=.env server.mjs` ✅
2. `curl http://localhost:4000/healthz` → `ors_api: true`
3. `curl -X POST http://localhost:4000/isochrone -H 'Content-Type: application/json' -d '{"profile":"foot-walking","locations":[-3.7038,40.4167],"range":[900]}'` → FeatureCollection
4. Si recibe `{"error":"ORS_API_KEY no configurada","fallback":true}`:
   - Revisar que el servidor se arrancó con `--env-file`
   - Verificar que la key no está truncada: `node --env-file=.env -e 'console.log(process.env.ORS_API_KEY.length)'` debe ser ~120