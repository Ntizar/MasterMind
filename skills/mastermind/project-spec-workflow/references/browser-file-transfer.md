# Browser-to-Local-Server File Transfer

## Problem
When the browser generates large HTML (>100KB) via JavaScript, there's no direct way to save it to disk from the browser context. `browser_console` has serialization limits, and `btoa()` chunking is fragile.

## Solution: Mini Python HTTP Server

### Server (run in terminal, background)
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        with open('output.html', 'wb') as f:
            f.write(data)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'ok')
        print(f"Saved {length} bytes")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

server = HTTPServer(('127.0.0.1', 8091), Handler)
server.handle_request()  # OPTIONS preflight
server.handle_request()  # Actual POST
```

### Client (browser_console)
```javascript
(async () => {
    const resp = await fetch('http://127.0.0.1:8091', {
        method: 'POST',
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: window._generatedHTML
    });
    return { saved: resp.ok, size: window._generatedHTML.length };
})()
```

## Pitfalls
- Must handle CORS: `Access-Control-Allow-Origin: *` on server
- Must handle OPTIONS preflight before POST
- Port must be free (check with `lsof -i :8091`)
- Kill server after transfer (only needs 1-2 requests)
- Browser may block `http://127.0.0.1` if page is on `https://` — use same origin or localhost

## Alternative: write_file from execute_code
For smaller files (<50KB), can use `execute_code` with `write_file()` directly if the content is available as a Python string. But for browser-generated HTML, the server approach is more reliable.
