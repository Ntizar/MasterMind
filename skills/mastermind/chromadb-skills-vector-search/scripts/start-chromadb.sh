#!/bin/bash
# start-chromadb.sh — Arranca ChromaDB local con health check
# Úsalo tras reinicio de la VM o si ChromaDB no responde
# Dependencias: chromadb 1.5.9 instalado en el venv de Hermes

set -e

CHROMA_PORT=8000
CHROMA_DATA="/hermes-home/chromadb-data"
PID_FILE="/tmp/chromadb.pid"
LOG_FILE="/tmp/chromadb.log"
MAX_RETRIES=10

# Verificar si ya está corriendo
if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
    echo "✅ ChromaDB ya está corriendo (PID $(cat $PID_FILE))"
    curl -s http://localhost:$CHROMA_PORT/api/v1/version
    echo
    exit 0
fi

# Limpiar PID file huérfano
rm -f "$PID_FILE"

echo "🚀 Arrancando ChromaDB en puerto $CHROMA_PORT..."

# Arrancar en background
nohup /opt/hermes/.venv/bin/python -c "
from chromadb.server.fastapi import FastAPI
from chromadb.config import Settings
import uvicorn

settings = Settings(
    chroma_server_host='0.0.0.0',
    chroma_server_http_port=$CHROMA_PORT,
    persist_directory='$CHROMA_DATA',
    allow_reset=True,
    is_persistent=True
)
server = FastAPI(settings)
app = server.app()
uvicorn.run(app, host='0.0.0.0', port=$CHROMA_PORT, log_level='info')
" > "$LOG_FILE" 2>&1 &

PID=$!
echo $PID > "$PID_FILE"
echo "   PID: $PID"

# Health check con reintentos
echo -n "   Esperando respuesta..."
for i in $(seq 1 $MAX_RETRIES); do
    sleep 1
    if curl -s http://localhost:$CHROMA_PORT/api/v1/version > /dev/null 2>&1; then
        echo " ✅"
        echo "   Versión: $(curl -s http://localhost:$CHROMA_PORT/api/v1/version)"
        echo "   Skills indexados: $(curl -s http://localhost:$CHROMA_PORT/api/v1/collections/mastermind-skills 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"dimension\",\"?\"))' 2>/dev/null || echo 'colección no encontrada')"
        exit 0
    fi
    echo -n "."
done

echo " ❌"
echo "ERROR: ChromaDB no respondió tras $MAX_RETRIES segundos"
echo "Logs: $LOG_FILE"
tail -5 "$LOG_FILE"
exit 1