#!/bin/bash
# System Health Dashboard — Ntizar Mastermind v4.0
# Muestra el estado de salud del sistema en formato legible.

set -uo pipefail

echo "╔══════════════════════════════════════════════════╗"
echo "║  Ntizar Mastermind v4.0 — System Health         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ═══ Git ═══
echo "━━━ 📦 Repositorio ━━━"
branch=$(git branch --show-current 2>/dev/null || echo "unknown")
commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
last_commit=$(git log -1 --format="%h %s" 2>/dev/null || echo "unknown")
dirty=$(git status --porcelain 2>/dev/null | wc -l)

echo "  Branch: $branch"
echo "  Commits: $commits"
echo "  Último: $last_commit"
if [ "$dirty" -eq 0 ]; then
    echo "  Estado: ✅ Limpio (sin cambios pendientes)"
else
    echo "  Estado: ⚠️  $dirty archivos modificados"
fi
echo ""

# ═══ Archivos ═══
echo "━━━ 📁 Archivos ━━━"
file_count=$(find . -not -path './.git/*' -not -path './node_modules/*' -type f 2>/dev/null | wc -l)
dir_count=$(find . -not -path './.git/*' -not -path './node_modules/*' -type d 2>/dev/null | wc -l)
total_size=$(du -sh --exclude=.git . 2>/dev/null | cut -f1)
code_size=$(find . -name "*.html" -o -name "*.md" -o -name "*.sh" -o -name "*.json" -o -name "*.yml" -o -name "*.css" 2>/dev/null | grep -v ".git" | xargs wc -c 2>/dev/null | tail -1 | awk '{print $1}')

echo "  Archivos: $file_count"
echo "  Directorios: $dir_count"
echo "  Tamaño total: $total_size"
echo "  Código fuente: $((code_size / 1024))KB"
echo ""

# ═══ Documentación ═══
echo "━━─ 📝 Documentación ━━━"
for f in SOUL.md AGENTS.md README.md README_EN.md CHANGELOG.md CONTRIBUTING.md; do
    if [ -f "$f" ]; then
        lines=$(wc -l < "$f")
        echo "  ✅ $f ($lines líneas)"
    else
        echo "  ❌ $f MISSING"
    fi
done
echo ""

# ═══ Landing Page ═══
echo "━━─ 🌐 Landing Page ━━━"
if [ -f "index.html" ]; then
    lines=$(wc -l < "index.html")
    has_og=$(grep -c "og:" index.html 2>/dev/null || echo 0)
    has_twitter=$(grep -c "twitter:" index.html 2>/dev/null || echo 0)
    has_aurora=$(grep -c "Ntizar-Aurora@" index.html 2>/dev/null || echo 0)
    echo "  ✅ index.html ($lines líneas)"
    echo "  OG tags: $has_og | Twitter: $has_twitter | Aurora: $has_aurora refs"
else
    echo "  ❌ index.html MISSING"
fi
echo ""

# ═══ Tokens ═══
echo "━━─ 📊 Token Tracking ━━━"
if [ -f "tokens/tokens-log.json" ]; then
    entries=$(python3 -c "import json; print(len(json.load(open('tokens/tokens-log.json'))))" 2>/dev/null || echo 0)
    total=$(python3 -c "import json; d=json.load(open('tokens/tokens-log.json')); print(sum(e.get('total_tokens',0) for e in d))" 2>/dev/null || echo 0)
    cost=$(python3 -c "import json; d=json.load(open('tokens/tokens-log.json')); print(f'\${sum(e.get(\"cost_estimate_usd\",0) for e in d):.3f}')" 2>/dev/null || echo "unknown")
    echo "  ✅ tokens-log.json ($entries sesiones)"
    echo "  Total tokens: $total"
    echo "  Coste estimado: $cost"
else
    echo "  ❌ tokens-log.json MISSING"
fi
echo ""

# ═══ Tests ═══
echo "━━─ 🧪 Tests ━━━"
if [ -f "test-suite.sh" ]; then
    result=$(bash test-suite.sh 2>&1 | tail -3)
    echo "$result"
else
    echo "  ⚠️  test-suite.sh no encontrado"
fi
echo ""

# ═══ Legacy ═══
echo "━━─ 🗄️ Legacy ━━━"
if [ -d "legacy" ]; then
    legacy_size=$(du -sh legacy/ 2>/dev/null | cut -f1)
    echo "  ✅ legacy/ ($legacy_size)"
fi
if [ -f "legacy-v3.1.tar.gz" ]; then
    tar_size=$(ls -lh legacy-v3.1.tar.gz | awk '{print $5}')
    echo "  ✅ legacy-v3.1.tar.gz ($tar_size)"
fi
echo ""

# ═══ Notas ═══
echo "━━─ 📒 Notas de Aprendizaje ━━━"
note_count=$(ls notes/*.md 2>/dev/null | wc -l)
echo "  $note_count notas"
ls -1 notes/*.md 2>/dev/null | while read f; do
    name=$(basename "$f" .md)
    echo "  • $name"
done
echo ""

# ═══ Disk ═══
echo "━━─ 💾 Disco ━━━"
disk_used=$(df -h . | tail -1 | awk '{print $5}')
disk_avail=$(df -h . | tail -1 | awk '{print $4}')
echo "  Usado: $disk_used | Disponible: $disk_avail"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Stack: Hermes Agent + NaN.builders + GitHub"
echo "Hecho con ❤️ por David Antizar"
