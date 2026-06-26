#!/bin/bash
# ChromaDB auto-start para Mastermind v3
# Usa el venv dedicado para evitar conflictos con el sistema

VENV_PYTHON="/hermes-home/chromadb-venv/bin/python"
CHROMA_PERSIST_DIR="/hermes-home/chromadb-data"
CHROMA_LOG="/tmp/chromadb.log"

# Crear directorio persistente si no existe
mkdir -p "$CHROMA_PERSIST_DIR"

# Verificar si ya está corriendo
if curl -s http://localhost:8000/api/v1/collections > /dev/null 2>&1; then
    echo "ChromaDB ya está corriendo en puerto 8000"
    exit 0
fi

echo "Arrancando ChromaDB desde venv..."

# Arrancar ChromaDB server con persistencia (v1.5+ usa CLI 'chroma run')
nohup /hermes-home/chromadb-venv/bin/chroma run \
    --path "$CHROMA_PERSIST_DIR" \
    --host 0.0.0.0 \
    --port 8000 \
    > "$CHROMA_LOG" 2>&1 &

# Esperar a que arranque
for i in $(seq 1 15); do
    if curl -s http://localhost:8000/api/v1/collections > /dev/null 2>&1; then
        echo "ChromaDB arrancado correctamente en puerto 8000 (intento $i)"
        exit 0
    fi
    sleep 1
done

echo "ERROR: ChromaDB no respondió tras 15 segundos"
echo "Últimas líneas del log:"
tail -20 "$CHROMA_LOG"
exit 1