# Dockerfile para SPA estáticas en NaN.builders

## Patrón Node.js (recomendado — mismo stack que esios-dashboard)

Para proyectos Vite/React/Vanilla JS que generan `dist/` y necesitan SPA fallback.

```dockerfile
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3700

# 1. Dependencias
COPY package.json package-lock.json ./
RUN npm ci

# 2. Código fuente
COPY index.html vite.config.js ./
COPY public/ ./public/
COPY src/ ./src/

# 3. Build
RUN npx vite build

# 4. Usuario no-root (REQUISITO NaN — sin esto el pod se queda Pending)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 5. Servidor Node.js embebido con SPA fallback + multi-puerto
#    Escucha en PORT (3700) + 80 para healthchecks internos de NaN
RUN echo 'const http = require("http"); \
const fs = require("fs"); \
const path = require("path"); \
const DIST = path.join(__dirname, "dist"); \
const MIME = { \
  ".html": "text/html", ".css": "text/css", \
  ".js": "application/javascript", ".json": "application/json", \
  ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", \
  ".ico": "image/x-icon", ".woff2": "font/woff2" \
}; \
function handler(req, res) { \
  let filePath = path.join(DIST, req.url === "/" ? "index.html" : req.url); \
  const ext = path.extname(filePath); \
  fs.readFile(filePath, (err, data) => { \
    if (err) { \
      fs.readFile(path.join(DIST, "index.html"), (e2, d2) => { \
        if (e2) { res.writeHead(500); res.end("Error"); return; } \
        res.writeHead(200, {"Content-Type": "text/html"}); \
        res.end(d2); \
      }); \
    } else { \
      res.writeHead(200, {"Content-Type": MIME[ext] || "application/octet-stream"}); \
      res.end(data); \
    } \
  }); \
} \
const ports = [process.env.PORT || 3700, 80]; \
ports.forEach(p => http.createServer(handler).listen(p, "0.0.0.0", () => console.log("NapMaps en puerto " + p)));' > server.js

# 6. Permisos y usuario no-root
RUN chown -R appuser:appgroup /app
USER appuser

# 7. Healthcheck en puerto 80 (NaN lo sondea)
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1

EXPOSE 3700
EXPOSE 80
CMD ["node", "server.js"]
```

## Patrón Nginx (alternativa, más complejo)

Para proyectos que ya tienen nginx configurado. Requiere multi-etapa y nginx.conf personalizado.

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY index.html vite.config.js ./
COPY public/ ./public/
COPY src/ ./src/
RUN npx vite build

FROM nginx:alpine
# Puerto debe coincidir con espacio NaN
RUN echo 'server { \
  listen 3700; \
  server_name _; \
  root /usr/share/nginx/html; \
  index index.html; \
  gzip on; \
  gzip_types text/css application/javascript image/svg+xml; \
  gzip_min_length 256; \
  location /assets/ { \
    expires 1y; \
    add_header Cache-Control "public, immutable"; \
  } \
  location / { \
    try_files $uri $uri/ /index.html; \
  } \
}' > /etc/nginx/conf.d/default.conf && rm -f /etc/nginx/conf.d/80.conf 2>/dev/null; \
true

COPY --from=builder /build/dist/ /usr/share/nginx/html/
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3700/ || exit 1
EXPOSE 3700
CMD ["nginx", "-g", "daemon off;"]
```

> ⚠️ **Problema común con nginx**: si el healthcheck falla porque `wget` no está en `nginx:alpine` (algunas versiones lo omiten), el pod se queda en Pending. Usar `busybox-extras` o cambiar a Node.js.

## Diagnóstico de SPA desplegada

```bash
# Verificar que la página principal carga
curl -s https://<app>.apps.nan.builders/ | head -5

# Verificar assets (deben devolver 200)
curl -sI https://<app>.apps.nan.builders/assets/index.js
curl -sI https://<app>.apps.nan.builders/assets/index.css

# Verificar healthcheck
curl -s https://<app>.apps.nan.builders/healthz

# Si todo da 404 → el pod no está corriendo → build falló o contenedor root
```