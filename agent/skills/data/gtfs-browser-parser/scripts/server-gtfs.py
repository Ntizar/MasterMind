#!/usr/bin/env python3
"""
Servidor mínimo para GTFSSpain — sirve visor + ZIPs + /api/zips
Uso: python server.py (desde la carpeta raiz del proyecto)
"""

import http.server
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PORT = 8080

class GTFSServer(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/api/zips' or self.path == '/api/zips/':
            self.serve_zips_list()
            return
        super().do_GET()
    
    def serve_zips_list(self):
        if not DATA_DIR.exists():
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "data/ no encontrado"}).encode())
            return
        
        zips = []
        for root, dirs, files in os.walk(DATA_DIR):
            for f in files:
                if f.endswith('.zip'):
                    full_path = Path(root) / f
                    rel_path = full_path.relative_to(BASE_DIR)
                    zips.append({
                        "name": f,
                        "path": str(rel_path).replace("\\", "/"),
                        "size": full_path.stat().st_size,
                        "size_human": f"{full_path.stat().st_size / 1024 / 1024:.1f} MB"
                    })
        
        zips.sort(key=lambda x: x["name"])
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(zips, indent=2).encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    os.chdir(BASE_DIR)
    server = http.server.HTTPServer(("0.0.0.0", PORT), GTFSServer)
    print(f"🚌 GTFSSpain server running at http://localhost:{PORT}")
    print(f"   Visor: http://localhost:{PORT}/visor/index.html")
    print(f"   API zips: http://localhost:{PORT}/api/zips")
    print(f"   Data: {len(list(DATA_DIR.rglob('*.zip')))} ZIPs")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado.")
        server.server_close()
