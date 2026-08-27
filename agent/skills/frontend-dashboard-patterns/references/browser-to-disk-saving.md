# Browser-to-Disk Saving — Guardar contenido generado en disco

Cuando necesitas guardar contenido generado en el navegador (HTML, JSON, CSV) a un archivo en disco local, y no tienes un endpoint de servidor disponible.

## Patrón: Receiver HTTP temporal

```python
# receiver.py — Ejecutar en background
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        with open('/ruta/archivo.html', 'wb') as f:
            f.write(data)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'ok')
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

server = HTTPServer(('127.0.0.1', 8091), Handler)
server.handle_request()  # OPTIONS
server.handle_request()  # POST
```

```javascript
// Desde el navegador
const html = window._generatedHTML;
await fetch('http://127.0.0.1:8091', {
    method: 'POST',
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
    body: html
});
```

## Alternativas

1. **Blob + download link** — El browser descarga el archivo (funciona pero no lo guarda automáticamente)
2. **Data URL + navigation** — `window.location.href = 'data:text/html;base64,...'` (limitado a ~2MB)
3. **Base64 chunks** — Para HTMLs grandes, dividir en chunks de 40KB de base64 y reensamblar en Python

## Cuándo usar

- Generar informes HTML grandes (>100KB) desde el navegador
- Exportar datos procesados a archivos locales
- Testing de generación de contenido sin servidor backend
- Prototipado rápido de pipelines de datos
