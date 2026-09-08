#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valida la integridad de un HTML contra el design system Aurora (sin navegador).

Comprueba, por código, tres cosas que el ojo no ve y que el audit-aurora.py NO
valida (el audit cuenta clases únicas pero no verifica que existan):

  1. Que toda clase `nz-*` usada en el HTML exista como selector en algún .css
     del repo (caza clases inventadas / typos).
  2. Que todo `var(--nz-*)` usado exista como token definido (caza renders rotos
     por variables inexistentes).
  3. Que las llaves de cada .css del repo estén balanceadas.

Uso:
  python validate-aurora-css.py <archivo.html> [dir_repo]
    dir_repo por defecto: C:\\Users\\d_ant\\Projects\\Ntizar-Aurora

PITFALL (regex BEM): al extraer selectores NO usar `\\.([a-z0-9-]+)` — el guion
bajo `_` de `nz-card__body` y el doble guion `--` de `nz-btn--primary` quedan
fuera y reportan falsos "faltantes". Usar `\\.(nz-[a-zA-Z0-9_\\-]+)`.
"""
import os, re, sys

DEFAULT_REPO = r"C:\Users\d_ant\Projects\Ntizar-Aurora"

def defined_classes(repo):
    """Selector de clase: incluye _ y -- (BEM)."""
    out = set()
    for fn in os.listdir(repo):
        if fn.endswith(".css"):
            css = open(os.path.join(repo, fn), encoding="utf-8").read()
            out |= set(re.findall(r"\.(nz-[a-zA-Z0-9_\-]+)", css))
    return out

def defined_tokens(repo):
    out = set()
    for fn in os.listdir(repo):
        if fn.endswith(".css"):
            css = open(os.path.join(repo, fn), encoding="utf-8").read()
            out |= set(re.findall(r"(--[a-z0-9-]+):", css))
    return out

def main():
    if len(sys.argv) < 2:
        print("Uso: python validate-aurora-css.py <archivo.html> [dir_repo]"); return 1
    html_path = sys.argv[1]
    repo = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_REPO
    html = open(html_path, encoding="utf-8").read()

    used = set()
    for m in re.findall(r'\bclass="([^"]+)"', html):
        used |= set(m.split())
    nz_used = {c for c in used if c.startswith("nz-")}
    ai_defs = defined_classes(repo)
    missing_classes = sorted(nz_used - ai_defs)
    print(f"clases nz- usadas: {len(nz_used)}")

    tok_used = set(re.findall(r"var\((--[a-z0-9-]+)", html))
    tok_defs = defined_tokens(repo)
    missing_tokens = sorted(tok_used - tok_defs)
    print(f"tokens usados: {len(tok_used)}")

    brace_issues = []
    for fn in os.listdir(repo):
        if fn.endswith(".css"):
            css = open(os.path.join(repo, fn), encoding="utf-8").read()
            if css.count("{") != css.count("}"):
                brace_issues.append(fn)

    ok = True
    if missing_classes:
        ok = False
        print("=== CLASES FALTANTES (posibles typos/inventadas) ===")
        for c in missing_classes:
            print("  ?", c)
    if missing_tokens:
        ok = False
        print("=== TOKENS FALTANTES (var(--nz-*) no definido) ===")
        for t in missing_tokens:
            print("  ?", t)
    if brace_issues:
        ok = False
        print("=== LLABES DESBALANCEADAS ===", brace_issues)

    if ok:
        print("OK: 0 clases inventadas, 0 tokens indefinidos, llaves balanceadas.")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
