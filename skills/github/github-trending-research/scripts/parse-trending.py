#!/usr/bin/env python3
"""Parse GitHub Trending HTML pages — updated 2026-06-03."""
import re
import json
import sys

def extract_repos(html, source):
    repos = []
    articles = re.findall(r'<article class="Box-row"[^>]*>.*?</article>', html, re.DOTALL)
    
    for article in articles:
        # Skip sponsored repos
        if 'sponsored' in article.lower():
            continue
            
        # Repo name from h2 > a
        repo_match = re.search(r'<h2[^>]*>.*?<a href="(/[^\"]+?)"[^>]*>', article, re.DOTALL)
        if not repo_match:
            continue
        repo = repo_match.group(1).strip('/')
        if '/stargazers' in repo:
            repo = repo.replace('/stargazers', '')
        
        # Description
        desc_match = re.search(r'<p class="col-9[^\"]*"[^>]*>([^<]+)', article, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ''
        
        # Language
        lang_match = re.search(r'data-language="([^"]+)"', article)
        lang = lang_match.group(1) if lang_match else ''
        
        # ⚠️ 2026-06-04: GitHub ELIMINÓ star counts del HTML de Trending.
        # Este campo SIEMPRE será '?'. Usar GitHub API para obtener estrellas.
        stars = '?'
        
        repos.append({
            'repo': repo,
            'stars': stars,
            'description': desc,
            'language': lang,
            'source': source
        })
    
    return repos

if __name__ == '__main__':
    with open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/trending-daily.html', 'r') as f:
        html = f.read()
    
    source = 'daily' if 'daily' in sys.argv[1] else 'weekly' if len(sys.argv) > 1 else 'daily'
    repos = extract_repos(html, source)
    
    for r in repos:
        print(f'{r["repo"]} | {r["stars"]} | {r["language"]} | {r["description"][:80]}')
