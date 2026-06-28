#!/usr/bin/env bash
# Arranca ChromaDB desde el venv del sistema
# Debe ejecutarse tras cada reinicio de la VM
# Datos persistentes en /hermes-home/chromadb-data/

set -e

CHROMADB_DIR="/hermes-home/chromadb-data"
PORT=8000
MAX_ATTEMPTS=3

echo "Arrancando ChromaDB desde venv..."

# Asegurar que el dir de datos existe
mkdir -p "$CHROMADB_DIR"

# Arrancar ChromaDB en background
/hermes-home/chromadb-venv/bin/chromadb run --path "$CHROMADB_DIR" --host 0.0.0.0 --port $PORT > /hermes-home/chromadb-data/chromadb.log 2>&1 &

# Esperar a que responda
for i in $(seq 1 $MAX_ATTEMPTS); do
    sleep 5
    if curl -s "http://localhost:$PORT/api/v1/version" > /dev/null 2>&1; then
        echo "ChromaDB arrancado correctamente en puerto $PORT (intento $i)"
        exit 0
    fi
    echo "Intento $i/$MAX_ATTEMPTS - esperando ChromaDB..."
done

echo "ERROR: ChromaDB no arrancó en $MAX_ATTEMPTS intentos"
cat /hermes-home/chromadb-data/chromadb.log
exit 1
