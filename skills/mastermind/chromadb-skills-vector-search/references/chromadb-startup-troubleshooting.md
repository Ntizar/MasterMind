# ChromaDB Startup Troubleshooting

## Problema: ChromaDB tarda 60-120s en arrancar

ChromaDB 1.5.5+ (backend Rust) tarda mucho en cargar datos persistentes desde disco. El servidor se queda "listening" pero no atiende peticiones HTTP hasta que termina de reconstruir el índice.

### Síntomas
- `chroma run` muestra "Frontend server listening on address" pero no responde a `/api/v1/heartbeat`
- `subprocess.run()` con timeout corto se queda pegado
- `nohup` + `subprocess.run()` NO desapeña el proceso — se queda en el padre

### Diagnóstico
```bash
pgrep -fa chroma
tail -20 /tmp/chromadb.log
curl -s http://localhost:8000/api/v1/heartbeat
```

### Solución correcta
```bash
bash /hermes-home/scripts/start-chromadb.sh
```

O desde Python:
```python
import subprocess, time, requests
subprocess.run(['pkill', '-9', '-f', 'chroma'], capture_output=True)
time.sleep(3)
subprocess.Popen(['nohup', 'chroma', 'run', '--path', '/hermes-home/chromadb-data',
                  '--host', '0.0.0.0', '--port', '8000'],
                 stdout=open('/tmp/chromadb.log', 'w'), stderr=subprocess.STDOUT)
for i in range(120):
    try:
        r = requests.get('http://localhost:8000/api/v1/heartbeat', timeout=3)
        if r.status_code == 200: break
    except: pass
    time.sleep(1)
```

### API v1 vs v2
- ChromaDB 1.5.5+ solo soporta API v2
- `/api/v1/collections` → 410 Unimplemented
- Usar cliente Python: `chromadb.HttpClient(host="localhost", port=8000)`