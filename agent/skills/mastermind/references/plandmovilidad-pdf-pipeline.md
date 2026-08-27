# PLANDEMOVILIDAD — Pipeline de PDF

Pipeline completo para generar el PDF del informe PMST/PTST (73 páginas, 754KB).

## Pipeline

```
demo-renfe.js (browser) → IndexedDB (3 centros)
    → page reload (app init carga Renfe)
    → import('./js/report.js') → generarInformeCompleto(appState)
    → 164KB HTML (22 capítulos)
    → POST a Python receiver local
    → weasyprint → PDF (73 páginas)
```

## Pasos exactos

### 1. Cargar datos demo en IndexedDB
```js
const r = await fetch('/demo-renfe.js');
const code = await r.text();
await eval(code);           // esperar que termine
await new Promise(r => setTimeout(r, 1500));  // buffer
```

**Pitfall:** `eval(code)` ejecuta una IIFE async. Usar `await eval(code)` para esperar a que termine. Si no se espera, IndexedDB puede quedar con datos parciales (0 centros en `empresas.centros[]`).

### 2. Recargar página con empresa activa
```js
location.href = 'http://localhost:8765/index.html';
```
La app lee `empresas` store y carga la más reciente. Si hay duplicados (ejecuciones múltiples del demo), el selector mostrará empresas repetidas.

**Pitfall:** Si hay duplicados en `empresas` store, limpiar antes:
```js
for (const store of ['empresas', 'datosEmpresa', 'respuestas']) {
    const tx = db.transaction(store, 'readwrite');
    tx.objectStore(store).clear();
    await new Promise(res => { tx.oncomplete = () => res(); });
}
```

### 3. Generar HTML del informe
```js
const m = await import('./js/report.js');
const html = m.generarInformeCompleto(window.pmstApp.appState);
```
Resultado: ~164KB HTML con 22 capítulos.

### 4. Transferir HTML a disco (POST a receiver local)
Montar un servidor Python minimal que escuche POST y guarde el body a archivo:

```python
import http.server, json, threading

class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        with open('/ruta/archivo.html', 'wb') as f:
            f.write(body)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'ok':True}).encode())
        threading.Thread(target=self.server.shutdown).start()
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

s = http.server.HTTPServer(('0.0.0.0', 9876), H)
s.serve_forever()
```

En el navegador:
```js
await fetch('http://localhost:9876', {
    method: 'POST',
    headers: {'Content-Type': 'text/html; charset=utf-8'},
    body: html
});
```

### 5. Convertir a PDF con weasyprint
```bash
weasyprint PMST_Renfe_Completo.html PMST_Renfe_Completo.pdf
```

## Problemas conocidos

### No transferir HTML chunks por consola
NO dividir el HTML en chunks base64 por la consola del navegador. Es lento, frágil y el console puede truncar strings grandes. Usar el receiver HTTP.

### weasyprint NO renderiza JS/Cavas/Leaflet
- Gráficos Canvas2D (reparto modal, huella CO₂e, comparativas) → espacios vacíos
- Mapa Leaflet (isocronas, paradas) → no se renderiza
- `box-shadow`, `grid auto-fit/fill`, `mix-blend-mode` → warnings, ignorados

**Soluciones pendientes:** html2canvas para rasterizar charts a PNG antes de exportar, o generar imágenes SVG estáticas.

### IA texts no conectados al informe
`ia-generativa.js` genera textos para 8 secciones vía qwen3.6 y los guarda en `appState.iaTexts`, pero `report.js` NUNCA los lee. El PDF usa texto de plantilla estática.

## Métricas de referencia
- HTML: 164KB, 22 capítulos
- PDF: 754KB, 73 páginas
- Tiempo: ~5-10s (generación) + ~10-20s (weasyprint)