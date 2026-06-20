# Pre-Implementation Audit — MasterFit v4.0.2 (2026-06-14)

## Session Context

Task: Iterative improvement of MasterFit (dieta-masterfit) — a Node.js/Express + HTML/JS/CSS fitness dashboard deployed on NaN.builders.

## Automated Checks Performed

### 1. Syntax Validation
- `node -c server.js` → ✅ OK
- HTML brace/paren balance → ✅ 293/293 braces, 825/825 parens
- File size: 82KB dashboard.html (under 100KB threshold for safe patching)

### 2. Variable Scope Analysis
**BUG FOUND:** `renderResumen` function used `perfil && perfil.altura_cm` but `perfil` was never declared in the function scope.
- **Impact:** TDEE calculation always fell back to 174cm regardless of user config
- **Fix:** Changed to `datos.perfil || {}`

### 3. Field Name Consistency
**BUG FOUND:** `saveConfig()` sent `objetivo_peso_kg` but server.js expects `peso_objetivo_kg`
- **Impact:** Weight objective never saved from config page
- **Fix:** Renamed field to `peso_objetivo_kg`

### 4. API Endpoint Verification
- All 18 API calls from frontend verified against backend endpoints
- Water POST endpoint ✅, generic DELETE/PUT ✅, CSV export ✅

### 5. Chart.js Memory Management
- 2 `.destroy()` calls found vs. 2 `new Chart()` calls → balanced ✅
- Pattern: `appState.charts.peso` / `appState.charts.macros` used correctly

### 6. XSS Risk Assessment
- 25 `innerHTML` assignments in dashboard.html
- User input escaped via `escapeHtml()` and `formatMarkdown()` in chat messages ✅
- Form inputs use `value="..."` with template literals (safe for config values)

## Real-World Bugs Found

| Bug | Severity | Root Cause | Fix |
|-----|----------|-----------|-----|
| `perfil` undefined in renderResumen | HIGH | Variable referenced but never declared in scope | Use `datos.perfil` |
| `objetivo_peso_kg` vs `peso_objetivo_kg` | HIGH | Frontend/backend field name mismatch | Rename field |
| No moving average on weight chart | LOW | Missing UX feature | Add 7-day MA line |
| No visual macro progress | LOW | Text-only display | Add colored progress bars |

## Key Takeaway

Phase 0 audit took ~5 minutes but found 2 real bugs that would have been missed by "just implementing features." The variable scope bug (`perfil && perfil.altura_cm`) is a classic JavaScript gotcha — the `&&` short-circuit makes it look safe but the variable is always undefined in scope.
