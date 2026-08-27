// server-spa-esm.mjs — Servidor HTTP ESM para SPA Vite en NaN.builders
// Compatible con "type": "module" en package.json
// Copiar como server-spa-esm.mjs en el repo y referenciar en Dockerfile:
//   COPY --chown=appuser:appgroup server-spa-esm.mjs ./
//   CMD ["node", "server-spa-esm.mjs"]

import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DIST = path.join(__dirname, "dist");

const MIME = {
  ".html": "text/html",
  ".css": "text/css",
  ".js": "application/javascript",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

const server = http.createServer((req, res) => {
  // Health check para NaN
  if (req.url === "/healthz") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", uptime: process.uptime() }));
    return;
  }

  // SPA fallback: cualquier ruta no encontrada → index.html
  const filePath = path.join(DIST, req.url === "/" ? "index.html" : req.url);
  const ext = path.extname(filePath);

  fs.readFile(filePath, (err, data) => {
    if (err) {
      fs.readFile(path.join(DIST, "index.html"), (e2, d2) => {
        if (e2) {
          res.writeHead(500);
          res.end("Error");
          return;
        }
        res.writeHead(200, { "Content-Type": "text/html" });
        res.end(d2);
      });
    } else {
      res.writeHead(200, {
        "Content-Type": MIME[ext] || "application/octet-stream",
      });
      res.end(data);
    }
  });
});

const PORT = process.env.PORT || 3030;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`App en puerto ${PORT}`);
});
