#!/bin/bash
# Test Suite — Ntizar Mastermind v4.0
# Tests funcionales: estructura + contenido + consistencia + comportamiento

set -uo pipefail

PASS=0
FAIL=0
WARN=0

# ═══ Helpers ═══

pass() {
    echo "  ✅ $1"
    PASS=$((PASS + 1))
}

fail() {
    echo "  ❌ $1"
    FAIL=$((FAIL + 1))
}

warn() {
    echo "  ⚠️  $1"
    WARN=$((WARN + 1))
}

check_file() {
    if [ -f "$1" ]; then pass "$1 existe"; else fail "$1 MISSING"; fi
}

check_dir() {
    if [ -d "$1" ]; then pass "$1/ existe"; else fail "$1/ MISSING"; fi
}

check_contains() {
    if grep -q "$2" "$1" 2>/dev/null; then
        pass "$1 contiene '$2'"
    else
        fail "$1 NO contiene '$2'"
    fi
}

check_not_contains() {
    if grep -q "$2" "$1" 2>/dev/null; then
        fail "$1 contiene '$2' (NO debería)"
    else
        pass "$1 sin '$2'"
    fi
}

check_min_lines() {
    local lines
    lines=$(wc -l < "$1" 2>/dev/null || echo 0)
    if [ "$lines" -ge "$2" ]; then
        pass "$1 tiene $lines líneas (>= $2)"
    else
        fail "$1 solo tiene $lines líneas (necesita >= $2)"
    fi
}

check_max_lines() {
    local lines
    lines=$(wc -l < "$1" 2>/dev/null || echo 0)
    if [ "$lines" -le "$2" ]; then
        pass "$1 tiene $lines líneas (<= $2)"
    else
        warn "$1 tiene $lines líneas (> $2, considerar reducir)"
    fi
}

echo "╔══════════════════════════════════════════════════╗"
echo "║  Ntizar Mastermind v4.0 — Test Suite            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# ═══ 1. ESTRUCTURA ═══
echo "━━━ 1. ESTRUCTURA ━━━"

echo "  Archivos core:"
check_file "SOUL.md"
check_file "AGENTS.md"
check_file "README.md"
check_file "README_EN.md"
check_file "CHANGELOG.md"
check_file "CONTRIBUTING.md"
check_file "LICENSE"
check_file "index.html"
check_file ".nojekyll"
check_file ".gitignore"
echo ""

echo "  Directorios:"
check_dir "legacy"
check_dir "notes"
check_dir "tokens"
check_dir "assets"
check_dir ".github/workflows"
echo ""

echo "  Assets:"
check_file "assets/banner.svg"
check_file "tokens/index.html"
check_file "tokens/tokens-log.json"
check_file "legacy-v3.1.tar.gz"
echo ""

# ═══ 2. CONTENIDO — SOUL.md ═══
echo "━━━ 2. CONTENIDO — SOUL.md (fuente de verdad) ━━━"

check_contains "SOUL.md" "Mastermind"
check_contains "SOUL.md" "Hermes Agent"
check_contains "SOUL.md" "NaN.builders"
check_contains "SOUL.md" "David Antizar"
check_contains "SOUL.md" "12 Reglas"
check_contains "SOUL.md" "Human Loop"
check_contains "SOUL.md" "Niveles de Ejecución"
check_not_contains "SOUL.md" "Ebbinghaus"
check_not_contains "SOUL.md" "docs/"
check_min_lines "SOUL.md" 70
check_max_lines "SOUL.md" 120
echo ""

# ═══ 3. CONTENIDO — AGENTS.md ═══
echo "━━━ 3. CONTENIDO — AGENTS.md (referencia rápida) ━━━"

check_contains "AGENTS.md" "Mastermind"
check_contains "AGENTS.md" "delegate_task"
check_contains "AGENTS.md" "skill_view"
check_contains "AGENTS.md" "SOUL.md"
check_not_contains "AGENTS.md" "Ebbinghaus"
check_min_lines "AGENTS.md" 50
check_max_lines "AGENTS.md" 80
echo ""

# ═══ 4. CONTENIDO — README.md ═══
echo "━━━ 4. CONTENIDO — README.md (vista usuario) ━━━"

check_contains "README.md" "Ntizar Mastermind"
check_contains "README.md" "143 skills"
check_contains "README.md" "git clone"
check_contains "README.md" "MIT License"
check_contains "README.md" "David Antizar"
check_not_contains "README.md" "## Principios"  # No duplicar secciones de SOUL.md
check_min_lines "README.md" 100
check_max_lines "README.md" 200
echo ""

# ═══ 5. CONTENIDO — index.html ═══
echo "━━━ 5. CONTENIDO — index.html (landing) ━━━"

check_contains "index.html" "nz-btn"
check_contains "index.html" "og:title"
check_contains "index.html" "og:image"
check_contains "index.html" "og:description"
check_contains "index.html" "twitter:card"
check_contains "index.html" "Ntizar-Aurora@latest"
check_contains "index.html" 'rel="icon"'
check_contains "index.html" "anim-fade-in"
check_not_contains "index.html" "innerHTML"
check_min_lines "index.html" 400
echo ""

# ═══ 6. CONSISTENCIA ═══
echo "━━━ 6. CONSISTENCIA ━━━"

# Aurora CDN version consistente
aurora_count=$(grep -c "Ntizar-Aurora@" index.html 2>/dev/null || echo 0)
if [ "$aurora_count" -ge 6 ]; then
    pass "Aurora CDN: $aurora_count referencias consistentes"
else
    fail "Aurora CDN: solo $aurora_count referencias (esperaba >= 6)"
fi

# No archivos fantasma en pages.yml
check_not_contains ".github/workflows/pages.yml" "verify-system.bat"
check_not_contains ".github/workflows/pages.yml" "docs/"

# JSON válido
if python3 -c "import json; json.load(open('tokens/tokens-log.json'))" 2>/dev/null; then
    pass "tokens-log.json es JSON válido"
else
    fail "tokens-log.json es JSON inválido"
fi

# Verificar estructura del JSON
entries=$(python3 -c "import json; d=json.load(open('tokens/tokens-log.json')); print(len(d))" 2>/dev/null || echo 0)
if [ "$entries" -ge 3 ]; then
    pass "tokens-log.json tiene $entries entradas (>= 3)"
else
    fail "tokens-log.json solo tiene $entries entradas (necesita >= 3)"
fi
echo ""

# ═══ 7. SEGURIDAD ═══
echo "━━━ 7. SEGURIDAD ━━━"

check_not_contains "index.html" "innerHTML"
check_not_contains "index.html" "eval("

# No secrets en el repo (patrones específicos, no genéricos)
secret_count=$(grep -rl "sk-[a-zA-Z0-9]\{20,\}" . --include="*.md" --include="*.json" --include="*.html" --include="*.sh" --include="*.yml" 2>/dev/null | grep -v ".git" | wc -l)
ghp_count=$(grep -rl "ghp_[a-zA-Z0-9]\{36,\}" . --include="*.md" --include="*.json" --include="*.html" --include="*.sh" --include="*.yml" 2>/dev/null | grep -v ".git" | wc -l)
aws_count=$(grep -rl "AKIA[A-Z0-9]\{16,\}" . --include="*.md" --include="*.json" --include="*.html" --include="*.sh" --include="*.yml" 2>/dev/null | grep -v ".git" | wc -l)
total_secrets=$((secret_count + ghp_count + aws_count))
if [ "$total_secrets" -eq 0 ]; then
    pass "No secrets detectados (AWS keys, GitHub tokens, API keys)"
else
    fail "$total_secrets archivos contienen posibles secrets reales"
fi
echo ""

# ═══ 8. LINKS ═══
echo "━━━ 8. LINKS INTERNOS ━━━"

# Verificar que archivos referenciados existen
if grep -q 'href="CONTRIBUTING.md"' README.md 2>/dev/null; then
    check_file "CONTRIBUTING.md"
fi
if grep -q 'href="CHANGELOG.md"' SOUL.md 2>/dev/null; then
    check_file "CHANGELOG.md"
fi
if grep -q 'href="LICENSE"' README.md 2>/dev/null; then
    check_file "LICENSE"
fi
if grep -q 'href="tokens/' index.html 2>/dev/null; then
    check_file "tokens/index.html"
fi
echo ""

# ═══ 9. LEGACY ═══
echo "━━━ 9. LEGACY ━━━"

check_file "legacy/README.md"
check_contains "legacy/README.md" "NUNCA ejecutar"
check_contains "legacy/README.md" "v3.1"
echo ""

# ═══ 10. NOTAS ═══
echo "━━━ 10. NOTAS DE APRENDIZAJE ━━━"

note_count=$(ls notes/*.md 2>/dev/null | wc -l || echo 0)
if [ "$note_count" -ge 3 ]; then
    pass "$note_count notas de aprendizaje (>= 3)"
else
    warn "Solo $note_count notas (recomendado >= 3)"
fi
echo ""

# ═══ RESULTADO ═══
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ $PASS passed  ❌ $FAIL failed  ⚠️  $WARN warnings"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "❌ TESTS FAILED — $FAIL checks failed"
    exit 1
else
    echo "✅ ALL TESTS PASSED — $PASS checks, $WARN warnings"
    echo ""
    echo "Stack: Hermes Agent + NaN.builders + GitHub"
    exit 0
fi
