#!/usr/bin/env bash
# Re-dispatch GitHub Pages deploy for DataHub España
# Usage: bash gh-pages-retry.sh [repo]
#   repo: Ntizar/DataHubEspana (default)

set -euo pipefail

REPO="${1:-Ntizar/DataHubEspana}"
TOKEN="${GITHUB_TOKEN:-$(grep GITHUB_TOKEN .env | cut -d= -f2-)}"

echo "🚀 Re-dispatching GitHub Pages deploy for $REPO..."

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$REPO/actions/workflows/pages.yml/dispatches" \
  -d '{"ref":"main"}')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Deploy dispatched successfully!"
    echo "⏳ Espera 2-3 minutos y verifica con:"
    echo "   curl -s -H \"Authorization: token \$GITHUB_TOKEN\" \\"
    echo "     \"https://api.github.com/repos/$REPO/actions/runs?per_page=3\" \\"
    echo "     -H \"Accept: application/vnd.github+json\" | python3 -c \"import json,sys; [print(f\\\"#{r['run_number']}: {r['status']} {r.get('conclusion','N/A')}\\\") for r in json.load(sys.stdin).get('workflow_runs',[])]\""
else
    echo "❌ Failed (HTTP $HTTP_CODE): $BODY"
    exit 1
fi
