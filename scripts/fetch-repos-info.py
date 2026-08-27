#!/usr/bin/env python3
"""Fetch README/content from repos for skill creation."""
import json, os, time, base64, sys, re
from urllib.request import Request, urlopen

TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Mastermind/1.0'
}
API = "https://api.github.com"

repos = [
    "github/spec-kit",
    "microsoft/qlib",
    "google-research/timesfm",
    "microsoft/presidio",
    "hcengineering/platform",
    "nocobase/nocobase",
    "run-llama/liteparse",
    "Panniantong/Agent-Reach",
]

for repo_name in repos:
    # Repo info
    req = Request(f"{API}/repos/{repo_name}", headers=HEADERS)
    resp = urlopen(req, timeout=15)
    repo = json.loads(resp.read())
    
    # README
    req = Request(f"{API}/repos/{repo_name}/readme", headers=HEADERS)
    try:
        resp = urlopen(req, timeout=15)
        readme_data = json.loads(resp.read())
        readme = base64.b64decode(readme_data["content"]).decode("utf-8", errors="replace")
        if len(readme) > 6000:
            readme = readme[:6000] + "\n\n... [truncated]"
    except:
        readme = ""
    
    # Topics & license
    topics = repo.get("topics", [])
    lang = repo.get("language", "")
    desc = repo.get("description", "") or ""
    stars = repo.get("stargazers_count", 0)
    
    # Get key files for tech stack
    key_files_content = {}
    for fname in ["package.json", "requirements.txt", "pyproject.toml", "setup.py", "Cargo.toml", "Dockerfile", "README.md"]:
        try:
            req = Request(f"{API}/repos/{repo_name}/contents/{fname}", headers=HEADERS)
            resp = urlopen(req, timeout=10)
            data = json.loads(resp.read())
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            if len(content) > 2000:
                content = content[:2000] + "\n... truncated"
            key_files_content[fname] = content
        except:
            pass
    
    output = {
        "full_name": repo_name,
        "name": repo_name.split("/")[1],
        "stars": stars,
        "language": lang,
        "description": desc,
        "topics": topics,
        "readme": readme,
        "key_files": key_files_content,
        "url": repo.get("html_url", ""),
        "license": (repo.get("license") or {}).get("spdx_id", ""),
    }
    
    outpath = f"/tmp/repo-{repo_name.replace('/', '-')}.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"[OK] {repo_name} -> {outpath}")
    time.sleep(0.3)