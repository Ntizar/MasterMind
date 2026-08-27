# Browser→Disco→PDF — Patrones de transferencia y conversión

## Problema

Cuando generas HTML rich (con Canvas charts, Leaflet maps, CSS print) en el navegador y necesitas convertirlo a PDF, hay una brecha: el HTML vive en `window` y el disco está fuera del navegador.

## Patrón 1: Base64 chunks (funciona, lento)

**Browser:**
```js
const html = window.__fullReport; // 164KB+
const chunkSize = 55000;
window.__chunks = [];
for (let i = 0; i < html.length; i += chunkSize) {
    window.__chunks.push(btoa(unescape(encodeURIComponent(html.substring(i, i + chunkSize)))));
}
// Recuperar cada chunk via browser_console y reensamblar
```

**Terminal (por cada chunk):**
```python
import base64
chunk_b64 = "..." # pegar desde browser_console
with open('report.html', 'ab') as f:
    f.write(base64.b64decode(chunk_b64))
```

**Ventaja:** No necesita servidor auxiliar.
**Desventaja:** Muy lento para >100KB (4+ rounds de browser_console → terminal).

## Patrón 2: HTTP receiver (más limpio)

**Levantar receiver ANTES de generar:**
```python
import http.server, threading, sys

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        with open('output.html', 'wb') as f:
            f.write(body)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(f'{{"ok":true,"bytes":{len(body)}}}'.encode())
        threading.Thread(target=self.server.shutdown).start()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

http.server.HTTPServer(('0.0.0.0', 8766), Handler).serve_forever()
```

**Browser:**
```js
fetch('http://localhost:8766', {
    method: 'POST',
    body: window.__fullReport,
    headers: {'Content-Type': 'text/html'}
}).then(r => r.json()).then(d => console.log(d));
```

**PITFALL:** El server en background a veces no arranca a tiempo. Verificar antes:
```bash
curl -s -o /dev/null -w '%{http_code}' http://localhost:8766/
# Debe devolver 000 si no está listo, o error de conexión
```

## Patrón 3: Node.js directo (sin browser)

Si `report.js` NO usa APIs de navegador (DOM, Canvas, Leaflet), se puede ejecutar directamente con Node.js + jsdom. Evita todo el pipeline browser→disco.

## Conversión HTML→PDF con weasyprint

**Instalación:** `pip install weasyprint` (ya disponible en el sistema)

**Comando:**
```bash
weasyprint input.html output.pdf
```

**CSS essential para A4:**
```css
@page {
    size: A4;
    margin: 25mm 20mm 30mm 20mm;
    @bottom-center {
        content: "PLAN DE MOVILIDAD SOSTENIBLE — Hecho con ❤️ por David Antizar";
        font-size: 8pt;
        color: #666;
    }
    @bottom-right { content: counter(page); font-size: 8pt; color: #666; }
}
```

**PITFALL:** weasyprint NO puede renderizar:
- JavaScript (Canvas2D charts, gráficas dinámicas)
- Leaflet maps (necesita tiles de red)
- Contenido lazy-loaded
- Web fonts que dependen de JS

**Solución para charts:** Exportar canvas como PNG antes de la conversión:
```js
// En browser, antes de generar HTML para PDF:
document.querySelectorAll('canvas').forEach(c => {
    const img = document.createElement('img');
    img.src = c.toDataURL('image/png');
    img.style.width = '100%';
    c.parentNode.replaceChild(img, c);
});
```

**Solución para maps:** Usar `exportMapAsImage()` (html2canvas) para rasterizar el mapa como imagen estática.

## Patrón completo: Browser→PDF profesional

```
1. Generar HTML en browser (generarInformeCompleto)
2. Rasterizar charts: canvas → img via toDataURL()
3. Rasterizar maps: Leaflet → img via html2canvas
4. Transferir HTML a disco (HTTP receiver o base64)
5. weasyprint input.html output.pdf
6. Verificar: wc -c output.pdf (debe ser >500KB para doc profesional)
```

## Limitaciones conocidas

| Feature | Browser | weasyprint PDF |
|---------|---------|----------------|
| HTML/CSS layout | ✅ | ✅ |
| Tablas | ✅ | ✅ |
| Canvas2D charts | ✅ | ❌ (necesita PNG) |
| Leaflet maps | ✅ | ❌ (necesita imagen) |
| CSS @page | N/A | ✅ |
| JavaScript | ✅ | ❌ |
| Web fonts | ✅ | ⚠️ (solo si embebidas) |
| Imágenes base64 | ✅ | ✅ |
