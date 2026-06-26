# GitHub API Enrichment for Trending Research

## Basic enrichment (single repo)
```bash
curl -s "https://api.github.com/repos/OWNER/REPO" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Stars: {data.get('stargazers_count')}\")
print(f\"Forks: {data.get('forks_count')}\")
print(f\"Created: {data.get('created_at', '')[:10]}\")
print(f\"Language: {data.get('language')}\")
print(f\"Topics: {data.get('topics', [])}\")
print(f\"License: {data.get('license', {}).get('spdx_id') if data.get('license') else 'N/A'}\")
print(f\"Description: {data.get('description', '')}\")
print(f\"Size: {data.get('size')} KB\")
"
```

## Batch enrichment (multiple repos)
```bash
# Input: file with one OWNER/REPO per line
while IFS= read -r repo; do
    echo "--- $repo ---"
    curl -s "https://api.github.com/repos/$repo" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Stars: {data.get('stargazers_count')}\")
print(f\"Topics: {data.get('topics', [])}\")
" 2>/dev/null || echo "FAILED"
done < repos.txt
```

## Rate limiting
- Unauthenticated: 60 req/hour
- Authenticated: 5,000 req/hour
- Use `$GITHUB_TOKEN` env var for authenticated requests
- For sessions with 10+ repos, always use token

## README fetching
```bash
# Try branches in order: main → master → develop
for branch in main master develop; do
    code=$(curl -s -o /dev/null -w "%{http_code}" \
        "https://raw.githubusercontent.com/OWNER/REPO/$branch/README.md")
    if [ "$code" = "200" ]; then
        curl -s "https://raw.githubusercontent.com/OWNER/REPO/$branch/README.md" | head -2000
        break
    fi
done
```

## Pitfalls
- Some READMEs are in `docs/README.md` or `README.zh-CN.md`
- API returns 403 for private repos or rate-limited requests
- Use `jq` for cleaner parsing: `curl -s "https://api.github.com/repos/OWNER/REPO" | jq '.stargazers_count'`
