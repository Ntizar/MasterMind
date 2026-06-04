#!/bin/bash
# Verify System Script — Ntizar Mastermind v4.0
# Verifies that the Hermes-Native system structure is intact.

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

echo "╔══════════════════════════════════════════╗"
echo "║  Ntizar Mastermind v4.0 — System Verify  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

echo "📦 Core files"
check_file "SOUL.md"
check_file "AGENTS.md"
check_file "README.md"
check_file "CHANGELOG.md"
check_file "LICENSE"
check_file "index.html"
echo ""

echo "📦 Documentation"
check_dir "docs"
check_file "CONTRIBUTING.md"
echo ""

echo "📦 Deploy"
check_file ".nojekyll"
check_file ".github/workflows/pages.yml"
echo ""

echo "📦 Legacy (v3.1 — reference only)"
check_dir "legacy"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ $PASS passed  ❌ $FAIL failed"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "❌ SYSTEM INCOMPLETE — $FAIL files/dirs missing"
    exit 1
else
    echo "✅ SYSTEM READY — All files present"
    echo ""
    echo "Stack: Hermes Agent + NaN.builders + GitHub"
    exit 0
fi
