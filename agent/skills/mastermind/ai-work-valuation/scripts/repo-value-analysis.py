#!/usr/bin/env python3
"""
Repo Value Analysis — Cuantifica el valor de trabajo IA vs equipo humano.

Uso:
  python repo-value-analysis.py <github_user> [--repos repo1,repo2,...] [--rate 100]

Requiere:
  - GITHUB_TOKEN en entorno
  - requests (o usar urllib de stdlib)

Output:
  - Métricas por repo (archivos, líneas, commits)
  - Estimación de horas de equipo humano
  - Tabla de asimetría IA vs humano
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
API_BASE = "https://api.github.com"

# ─── GitHub API helpers ───────────────────────────────────────────────

def gh_api(path):
    """Llama a la API de GitHub con autenticación."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ⚠️  HTTP {e.code} en {path}", file=sys.stderr)
        return None

def get_repos(user):
    """Lista repos del usuario."""
    repos = []
    page = 1
    while True:
        data = gh_api(f"/users/{user}/repos?per_page=100&page={page}&sort=updated&type=all")
        if not data:
            # try /user/repos for private
            data = gh_api(f"/user/repos?per_page=100&page={page}&sort=updated&type=all")
        if not data or len(data) == 0:
            break
        repos.extend(data)
        if len(data) < 100:
            break
        page += 1
    return repos

def get_default_branch(owner, repo):
    """Obtiene la rama por defecto."""
    data = gh_api(f"/repos/{owner}/{repo}")
    if data:
        return data.get("default_branch", "main")
    return "main"

def get_tree(owner, repo, branch):
    """Obtiene el árbol de archivos recursivo."""
    data = gh_api(f"/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    if not data:
        return []
    return [t for t in data.get("tree", []) if t["type"] == "blob"]

def get_commits(owner, repo):
    """Cuenta commits."""
    page = 1
    total = 0
    while True:
        data = gh_api(f"/repos/{owner}/{repo}/commits?per_page=100&page={page}")
        if not data or len(data) == 0:
            break
        total += len(data)
        if len(data) < 100:
            break
        page += 1
    return total

def get_commit_dates(owner, repo, limit=15):
    """Obtiene fechas de los últimos commits."""
    data = gh_api(f"/repos/{owner}/{repo}/commits?per_page={limit}")
    if not data:
        return []
    dates = []
    for c in data:
        date_str = c["commit"]["author"]["date"][:19]
        msg = c["commit"]["message"].split("\n")[0][:80]
        dates.append((date_str, msg))
    return dates

# ─── Análisis ─────────────────────────────────────────────────────────

# Aproximación de líneas por tipo de archivo (bytes / factor)
LINE_FACTORS = {
    ".py": 35,
    ".md": 45,
    ".xml": 40,
    ".json": 25,
    ".yaml": 35,
    ".yml": 35,
    ".js": 35,
    ".html": 40,
    ".css": 30,
}

def analyze_repo(owner, repo_name):
    """Analiza un repo y devuelve métricas."""
    branch = get_default_branch(owner, repo_name)
    tree = get_tree(owner, repo_name, branch)
    commits = get_commits(owner, repo_name)
    commit_dates = get_commit_dates(owner, repo_name)

    # Contar por tipo
    by_ext = {}
    test_files = 0
    total_size = 0
    total_lines_est = 0

    for f in tree:
        path = f["path"]
        size = f.get("size", 0)
        total_size += size

        # Detectar tests
        if "test" in path.lower():
            test_files += 1

        # Por extensión
        ext = "." + path.rsplit(".", 1)[-1] if "." in path else "other"
        if ext not in by_ext:
            by_ext[ext] = {"files": 0, "bytes": 0, "lines_est": 0}
        by_ext[ext]["files"] += 1
        by_ext[ext]["bytes"] += size
        if ext in LINE_FACTORS:
            lines_est = size // LINE_FACTORS[ext]
            by_ext[ext]["lines_est"] += lines_est
            total_lines_est += lines_est

    return {
        "name": repo_name,
        "branch": branch,
        "total_files": len(tree),
        "total_bytes": total_size,
        "total_lines_est": total_lines_est,
        "test_files": test_files,
        "commits": commits,
        "by_extension": by_ext,
        "commit_dates": commit_dates,
    }

def estimate_human_hours(analysis_results):
    """Estima horas de equipo humano basándose en métricas."""
    total_py_lines = sum(
        r["by_extension"].get(".py", {}).get("lines_est", 0)
        for r in analysis_results
    )
    total_tests = sum(r["test_files"] for r in analysis_results)
    total_files = sum(r["total_files"] for r in analysis_results)

    # Heurísticas conservadoras
    # Validador: ~2 devs × 3-4 meses (1000-1300h) por cada 200+ reglas
    # Conversor: ~2-3 devs × 3-4 meses (1300-1600h) por cada 10K líneas
    # Spec: ~1-2 personas × 3-4 semanas (120-320h)
    # Tests: ~1-2 testers × 2-3 meses (320-520h)
    # Docs: ~1-2 personas × 2-4 semanas (80-320h)

    base_hours = {
        "investigacion": (320, 480),      # 2-3 expertos × 4-6 sem
        "spec": (120, 320),               # 1-2 personas × 3-4 sem
        "validador": (1000, 1300),        # 2 devs × 3-4 meses
        "conversor": (1300, 1600),        # 2-3 devs × 3-4 meses
        "conversor_inverso": (320, 520),  # 1-2 devs × 2-3 meses
        "tests": (320, 520),              # 1-2 testers × 2-3 meses
        "docs": (80, 320),               # 1-2 personas × 2-4 sem
    }

    total_low = sum(v[0] for v in base_hours.values())
    total_high = sum(v[1] for v in base_hours.values())

    return {
        "phases": base_hours,
        "total_low": total_low,
        "total_high": total_high,
        "team_size": "3-5 personas",
        "duration": "1.5-2.5 años",
    }

def print_report(owner, results, human_est, rate=100):
    """Imprime el informe completo."""
    print(f"\n{'='*60}")
    print(f"  ANÁLISIS DE VALOR — {owner}")
    print(f"{'='*60}\n")

    # Por repo
    for r in results:
        print(f"  📦 {r['name']} ({r['branch']})")
        print(f"     Archivos: {r['total_files']}")
        print(f"     Bytes: {r['total_bytes']:,}")
        print(f"     Líneas (est): {r['total_lines_est']:,}")
        print(f"     Tests: {r['test_files']}")
        print(f"     Commits: {r['commits']}")
        py = r["by_extension"].get(".py", {})
        md = r["by_extension"].get(".md", {})
        xml = r["by_extension"].get(".xml", {})
        if py: print(f"     Python: {py['files']} files, ~{py['lines_est']:,} lines")
        if md: print(f"     Markdown: {md['files']} files, ~{md['lines_est']:,} lines")
        if xml: print(f"     XML: {xml['files']} files, ~{xml['lines_est']:,} lines")
        if r["commit_dates"]:
            first = r["commit_dates"][-1][0]
            last = r["commit_dates"][0][0]
            print(f"     Timeline: {first} → {last}")
        print()

    # Totales
    total_files = sum(r["total_files"] for r in results)
    total_lines = sum(r["total_lines_est"] for r in results)
    total_tests = sum(r["test_files"] for r in results)
    print(f"  📊 TOTALES")
    print(f"     Repos: {len(results)}")
    print(f"     Archivos: {total_files}")
    print(f"     Líneas (est): {total_lines:,}")
    print(f"     Tests: {total_tests}")
    print()

    # Estimación humano
    print(f"  👥 ESTIMACIÓN EQUIPO HUMANO")
    for phase, (low, high) in human_est["phases"].items():
        print(f"     {phase}: {low}-{high}h")
    print(f"     TOTAL: {human_est['total_low']:,}-{human_est['total_high']:,}h")
    print(f"     Equipo: {human_est['team_size']}")
    print(f"     Duración: {human_est['duration']}")
    print()

    # Valor monetario
    val_low = human_est["total_low"] * rate
    val_high = human_est["total_high"] * rate
    print(f"  💰 VALOR MONETARIO (a {rate}€/h)")
    print(f"     {val_low:,}€ - {val_high:,}€")
    print()

    # Tabla de asimetría
    print(f"  ⚡ TABLA DE ASIMETRÍA")
    print(f"     {'':30s} {'Equipo tradicional':>20s}  {'IA + juicio':>20s}")
    print(f"     {'Tiempo':30s} {human_est['duration']:>20s}  {'horas':>20s}")
    print(f"     {'Coste':30s} {f'{val_low//1000}K-{val_high//1000}K€':>20s}  {'Tiempo + IA':>20s}")
    print(f"     {'Margen':30s} {'30-40%':>20s}  {'90%+':>20s}")
    print()

if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN no configurado", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Uso: python repo-value-analysis.py <github_user> [--repos repo1,repo2] [--rate 100]")
        sys.exit(1)

    owner = sys.argv[1]
    repo_filter = None
    rate = 100

    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--repos" and i + 1 < len(sys.argv):
            repo_filter = sys.argv[i + 1].split(",")
        elif arg == "--rate" and i + 1 < len(sys.argv):
            rate = int(sys.argv[i + 1])

    # Obtener repos
    all_repos = get_repos(owner)
    if repo_filter:
        all_repos = [r for r in all_repos if r["name"] in repo_filter]

    if not all_repos:
        print(f"No se encontraron repos para {owner}", file=sys.stderr)
        sys.exit(1)

    # Analizar cada repo
    results = []
    for repo in all_repos:
        print(f"Analizando {repo['name']}...", file=sys.stderr)
        analysis = analyze_repo(owner, repo["name"])
        results.append(analysis)

    # Estimar horas humanas
    human_est = estimate_human_hours(results)

    # Imprimir informe
    print_report(owner, results, human_est, rate)
