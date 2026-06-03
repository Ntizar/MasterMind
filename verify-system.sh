# Verify System Script

# Cross-platform system verification for Ntizar Mastermind v3
# Works on Linux, macOS, and WSL/Bash on Windows

set -euo pipefail

PASS=0
FAIL=0
WARN=0

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
echo "║  Ntizar Mastermind v3 — System Verify   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

echo "📦 Layer 1: Documentation (agents/)"
check_dir "agents"
check_file "agents/00-orchestrator.md"
check_file "agents/01-classifier.md"
check_file "agents/02-explorer.md"
check_file "agents/03-planner.md"
check_file "agents/04-spec-writer.md"
check_file "agents/05-implementer.md"
check_file "agents/06-reviewer.md"
check_file "agents/07-critic.md"
check_file "agents/08-synthesizer.md"
check_file "agents/09-archiver.md"
check_file "agents/10-librarian.md"
echo ""

echo "📦 Layer 2: Executable (.opencode/agents/)"
check_dir ".opencode/agents"
check_file ".opencode/agents/ntizar-build.md"
check_file ".opencode/agents/ntizar-plan.md"
check_file ".opencode/agents/ntizar-explorer.md"
check_file ".opencode/agents/ntizar-planner.md"
check_file ".opencode/agents/ntizar-spec-writer.md"
check_file ".opencode/agents/ntizar-implementer.md"
check_file ".opencode/agents/ntizar-reviewer.md"
check_file ".opencode/agents/ntizar-critic.md"
check_file ".opencode/agents/ntizar-synthesizer.md"
check_file ".opencode/agents/ntizar-archiver.md"
check_file ".opencode/agents/ntizar-librarian.md"
echo ""

echo "📦 Layer 3: Commands"
check_dir ".opencode/commands"
check_file ".opencode/commands/ntizar-start.md"
check_file ".opencode/commands/ntizar-status.md"
check_file ".opencode/commands/ntizar-models.md"
check_file ".opencode/commands/ntizar-archive.md"
echo ""

echo "📦 Layer 4: State & Config"
check_dir "agents/state"
check_file "agents/state/_system-config.md"
check_file "agents/state/_session-state.md"
echo ""

echo "📦 Layer 5: Skills & Learnings"
check_dir "agents/skills"
check_file "agents/skills/_index.md"
check_file "agents/skills/template-skill.md"
check_dir "agents/learnings"
check_file "agents/learnings/_index.md"
check_file "agents/learnings/template-learning.md"
echo ""

echo "📦 Layer 6: Templates & Projects"
check_dir "agents/templates"
check_file "agents/templates/spec-template.md"
check_file "agents/templates/learning-template.md"
check_file "agents/templates/review-template.md"
check_file "agents/templates/task-intake.md"
check_dir "agents/projects"
check_file "agents/projects/_clusters.md"
echo ""

echo "📦 Layer 7: Root Files"
check_file "AGENTS.md"
check_file "README.md"
check_file "LICENSE"
echo ""

echo "📦 Layer 8: Deploy (GitHub Pages)"
check_file ".nojekyll"
check_file ".github/workflows/pages.yml"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ $PASS passed  ❌ $FAIL failed  ⚠️ $WARN warnings"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "❌ SYSTEM INCOMPLETE — $FAIL files/dirs missing"
    echo "Check the list above and fix before using the system."
    exit 1
else
    echo "✅ SYSTEM READY — All files present"
    echo "OpenCode: opencode → /ntizar-start"
    exit 0
fi
