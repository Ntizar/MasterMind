# Query Params en path.extname() — Bug de Content-Type

## El Problema

`path.extname()` no ignora query strings:

```js
const path = require('path');
path.extname('css/style.css?v=2');  // → '.css?v=2' ❌
path.extname('css/style.css');      // → '.css' ✅
```

Cuando un servidor estático usa `path.extname()` para determinar el `Content-Type`, las URLs con query params (`?v=2`, `?t=12345`) reciben `application/octet-stream` en vez del tipo correcto.

## La Solución

Limpiar el path antes de `path.extname()`:

```js
let filePath = path.join(DIST, req.url);
filePath = filePath.split('?')[0];  // Limpiar query params
const ext = path.extname(filePath);
const contentType = MIME[ext] || 'application/octet-stream';
```

## Cuándo Ocurre
- Servidores estáticos en Node.js (express.static, http.createServer)
- CDN o reverse proxy que añade query params para cache-busting
- Herramientas de build que inyectan hashes en URLs

## Verificación

```bash
# Sin fix — devuelve application/octet-stream
curl -I http://localhost:4000/css/style.css?v=2
Content-Type: application/octet-stream

# Con fix — devuelve text/css
curl -I http://localhost:4000/css/style.css?v=2
Content-Type: text/css
```
