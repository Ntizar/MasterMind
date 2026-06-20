#!/bin/bash
# Verificar estado de indexación ChromaDB
# Uso: bash scripts/verify-index.sh
# Compara skills en disco vs indexados en ChromaDB

CHROMA_URL="http://localhost:8000"
COLLECTION_NAME="mastermind-skills"
VENV_PYTHON="/opt/hermes/.venv/bin/python3"

echo "=== ChromaDB Index Verification ==="

# 1. Check ChromaDB is running
if ! curl -s "$CHROMA_URL/api/v1/collections" > /dev/null 2>&1; then
    echo "❌ ChromaDB NO está corriendo en $CHROMA_URL"
    echo "   Arrancar con: bash scripts/start-chromadb.sh"
    exit 1
fi
echo "✅ ChromaDB corriendo"

# 2. Count skills in disk
SKILLS_IN_DISK=$($VENV_PYTHON -c "
import glob
files = glob.glob('/hermes-home/skills/**/SKILL.md', recursive=True)
print(len(files))
")
echo "📁 Skills en disco: $SKILLS_IN_DISK"

# 3. Count skills in ChromaDB
SKILLS_IN_CHROMA=$($VENV_PYTHON -c "
import requests
resp = requests.get('$CHROMA_URL/api/v1/collections/$COLLECTION_NAME', timeout=5)
cid = resp.json()['id']
resp2 = requests.post('$CHROMA_URL/api/v1/collections/' + cid + '/query',
    json={'query_embeddings': [[0.0]*4096]], 'n_results': 9999}, timeout=10)
print(len(resp2.json()['ids'][0]))
")
echo "📦 Indexados en ChromaDB: $SKILLS_IN_CHROMA"

# 4. Show missing (by directory name)
echo ""
echo "=== Skills sin indexar (por nombre de directorio) ==="
$VENV_PYTHON -c "
import requests, glob, os
CHROMA_URL = '$CHROMA_URL'
COLLECTION_NAME = '$COLLECTION_NAME'
resp = requests.get(CHROMA_URL + '/api/v1/collections/' + COLLECTION_NAME, timeout=10)
collection_id = resp.json()['id']
payload = {'query_embeddings': [[0.0] * 4096], 'n_results': 9999}
resp2 = requests.post(CHROMA_URL + '/api/v1/collections/' + collection_id + '/query', json=payload, timeout=10)
indexed = set(resp2.json()['ids'][0])
for sf in sorted(glob.glob('/hermes-home/skills/**/SKILL.md', recursive=True)):
    name = os.path.basename(os.path.dirname(sf))
    if name not in indexed:
        print('  MISSING: ' + name)
"

echo ""
echo "=== Done ==="
