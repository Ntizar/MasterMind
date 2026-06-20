#!/bin/bash
# ============================================================
# Mastermind Weekly Maintenance
# Domingo 05:00 UTC
# ============================================================
set -e

export NAN_API="${NAN_API:-sk-oej...4dRg}"
export GITHUB_TOKEN="$(cat /hermes-home/.env 2>/dev/null | grep GITHUB_TOKEN | cut -d= -f2-)"

LOG="/var/log/mastermind-weekly.log"
exec > >(tee -a "$LOG") 2>&1

echo ""
echo "=========================================="
echo "🧠 Mastermind Weekly Maintenance"
echo "   $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "=========================================="

# 1. Reindex ChromaDB
echo ""
echo "[1/7] 🔄 Reindexando ChromaDB..."
cd /hermes-home/scripts && NAN_API="$NAN_API" python3 indexar-skills.py 2>&1 | tail -5

# 2. Ebbinghaus decay
echo ""
echo "[2/7] 🧠 Ejecutando Ebbinghaus decay..."
python3 /hermes-home/scripts/ebbinghaus-decay.py 2>&1 | tail -5

# 3. Knowledge graph
echo ""
echo "[3/7] 🕸️  Actualizando knowledge graph..."
python3 /hermes-home/scripts/knowledge-graph.py 2>&1 | tail -5

# 4. Skill lifecycle
echo ""
echo "[4/7] 📊 Actualizando skill lifecycle..."
python3 /hermes-home/scripts/skill-lifecycle.py 2>&1 | tail -5

# 5. Generate dashboard
echo ""
echo "[5/7] 📈 Actualizando dashboard..."
python3 /hermes-home/scripts/generate-dashboard.py 2>&1 | tail -5

# 6. Health check
echo ""
echo "[6/7] 🏥 Verificando salud del sistema..."
COLLECTIONS=$(curl -s --max-time 10 http://localhost:8000/api/v1/collections 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")
echo "  ChromaDB collections: $COLLECTIONS"

if [ "$COLLECTIONS" = "0" ]; then
    echo "  ⚠️  ChromaDB no responde, iniciando..."
    bash /hermes-home/scripts/start-chromadb.sh 2>&1
    sleep 3
    COLLECTIONS=$(curl -s --max-time 10 http://localhost:8000/api/v1/collections 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d))" 2>/dev/null || echo "0")
    echo "  ChromaDB collections tras restart: $COLLECTIONS"
fi

# 7. Commit y push
echo ""
echo "[7/7] 💾 Commit y push al repo..."
cd /root/workspace/Mastermind
git add -A
if git diff --cached --quiet; then
    echo "  Sin cambios para commit"
else
    git commit -m "chore: mantenimiento semanal Mastermind - $(date +%Y-%m-%d)" 2>&1
    git push 2>&1 | tail -3
    echo "  ✅ Commit y push completados"
fi

echo ""
echo "=========================================="
echo "✅ Mantenimiento completado"
echo "=========================================="
