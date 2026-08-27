#!/bin/bash
# Verify System Script — Ntizar Mastermind v4.0
# Verifica estructura, contenido y consistencia del sistema.

set -euo pipefail

PASS=0
FAIL=0

check_file() {
    if [ -f "$1" ]; then
        echo "  ✅ $1"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $1 (MISSING)"
        FAIL=$((FAIL + 1))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "  ✅ $1/"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $1/ (MISSING)"
        FAIL=$((FAIL + 1))
    fi
}

check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo "  ✅ $1 → contiene '$2'"
        PASS=$((PASS + 1))
    else
        echo "  ❌ $1 → NO contiene '$2'"
        FAIL=$((FAIL + 1))
    fi
}

check_no_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo "  ❌ $1 → contiene '$2' (NO debería)"
        FAIL=$((FAIL + 1))
    else
        echo "  ✅ $1 → sin '$2'"
        PASS=$((PASS + 1))
    fi
}

echo "╔══════════════════════════════════════════════╗"
echo "║  Ntizar Mastermind v4.0 — System Verify     ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ═══ Estructura ═══
echo "📦 Estructura — Archivos core"
check_file "SOUL.md"
check_file "AGENTS.md"
check_file "README.md"
check_file "README_EN.md"
check_file "CHANGELOG.md"
check_file "CONTRIBUTING.md"
check_file "LICENSE"
check_file "index.html"
echo ""

echo "📦 Estructura — Directorios"
check_dir "legacy"
check_dir "notes"
check_dir "tokens"
check_dir "assets"
check_dir ".github/workflows"
echo ""

# ═══ Contenido ═══
echo "📝 Contenido — SOUL.md (fuente de verdad)"
check_content "SOUL.md" "Mastermind"
check_content "SOUL.md" "Hermes Agent"
check_content "SOUL.md" "NaN.builders"
check_content "SOUL.md" "David Antizar"
echo ""

echo "📝 Contenido — README.md (vista usuario)"
check_content "README.md" "Ntizar Mastermind"
check_content "README.md" "143 skills"
check_content "README.md" "git clone"
echo ""

echo "📝 Contenido — index.html (landing)"
check_content "index.html" "nz-btn"
check_content "index.html" "og:title"
check_content "index.html" "og:image"
echo ""

# ═══ Consistencia ═══
echo "🔗 Consistencia — Sin duplicación"
check_no_content "index.html" "innerHTML"
echo ""

echo "🔗 Consistencia — Aurora CDN"
check_content "index.html" "Ntizar-Aurora@latest"
echo ""

echo "🔗 Consistencia — Pages workflow limpio"
check_no_content ".github/workflows/pages.yml" "verify-system.bat"
echo ""

echo "🔗 Consistencia — Token dashboard"
if [ -f "tokens/tokens-log.json" ]; then
    if python3 -c "import json; json.load(open('tokens/tokens-log.json'))" 2>/dev/null; then
        echo "  ✅ tokens/tokens-log.json → JSON válido"
        PASS=$((PASS + 1))
    else
        echo "  ❌ tokens/tokens-log.json → JSON inválido"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  ❌ tokens/tokens-log.json → MISSING"
    FAIL=$((FAIL + 1))
fi
echo ""

# ═══ Resultado ═══
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ $PASS passed  ❌ $FAIL failed"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "❌ SYSTEM INCOMPLETE — $FAIL checks failed"
    exit 1
else
    echo "✅ SYSTEM READY — All $PASS checks passed"
    echo ""
    echo "Stack: Hermes Agent + NaN.builders + GitHub"
    exit 0
fi
