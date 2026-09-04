#!/usr/bin/env python3
"""Aurora Design System - Audit HTML against Aurora Design System.

Usage:
  python3 audit-aurora.py <file.html>
  curl -s <url> | python3 audit-aurora.py -

v2 (Aurora v6): whitelist de prefijos de shell, inline styles con tokens
no penalizan, componentes premium v6, perfil landing (umbral 60 clases).
"""
import sys
import re

# Prefijos de shell permitidos (patrón "shell + componentes", ERROR #13):
# el shell aporta layout/espaciado, los componentes Aurora el resto.
SHELL_PREFIXES = ('nz-', 'u-nz-', 'mm-', 'demo-', 'login-', 'dash-', 'app-',
                  'nav-', 'hero-', 'footer-', 'section-', 'bento-', 'stat-')

# Inline styles que solo usan var(--nz-*) o spacing simple no penalizan.
INLINE_PERMITIDO = re.compile(r'^(var\(--nz-[^)]+\)|[-0-9a-z%. ]+)$', re.I)

# Componentes premium v5 + v6
PREMIUM_BASE = [
    'nz-anim-fade-in', 'nz-kpi', 'nz-bento-grid', 'nz-table', 'nz-badge',
    'nz-nav--glass', 'nz-stats-banner', 'nz-stack',
    'nz-chart--glass', 'nz-progress', 'nz-modal', 'nz-skeleton', 'nz-tabs',
    'nz-data-card', 'nz-divider', 'nz-spinner', 'nz-search', 'nz-callout',
]
PREMIUM_V6 = [
    'nz-glass-liquid-live', 'nz-three', 'data-nz-three',
]

def audit(html_path):
    if html_path == '-':
        html = sys.stdin.read()
    else:
        with open(html_path, encoding='utf-8') as f:
            html = f.read()

    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    css = style_match.group(1) if style_match else ''
    css_lines = len(css.strip().split('\n')) if css.strip() else 0

    all_classes = re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', css)
    custom_classes = sorted(set(c for c in all_classes if not c.startswith(SHELL_PREFIXES)))
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}\b', css)
    inline_styles = [s for s in re.findall(r'style="([^"]*)"', html)
                     if any(tok not in s and 'var(--nz-' not in s for tok in [s])
                     and not INLINE_PERMITIDO.match(s.strip())]
    aurora_classes = sorted(set(re.findall(r'nz-[a-zA-Z0-9_-]+', html)))
    css_links = re.findall(r'href="([^"]*ntizar[^"]*)"', html)
    packs = sorted(set(css_links))
    body_match = re.search(r'<body([^>]*)>', html)
    body_attrs = body_match.group(1) if body_match else ''

    es_landing = 'nz-hero' in html or '<header' in html
    min_clases = 60 if es_landing else 100

    premium = {n: (n in html) for n in PREMIUM_BASE}
    premium['nz-glass-liquid-live'] = 'nz-glass-liquid-live' in html
    premium['nz-three'] = '.nz-three' in html or 'nz-three nz-three' in html
    premium['data-nz-three'] = 'data-nz-three' in html
    if es_landing:
        premium.pop('nz-modal', None)
        premium.pop('nz-skeleton', None)
        premium.pop('nz-search', None)

    has_nz = 'class="nz"' in html or "class='nz'" in html
    has_theme = 'data-nz-theme=' in body_attrs
    has_skin = 'data-nz-skin=' in body_attrs

    print("AURORA AUDIT REPORT v2")
    print("=" * 50)
    print(f"CSS custom: {css_lines} lines {'PASS' if css_lines <= 40 else 'FAIL'} (limit shell: 40)")
    print(f"Custom classes: {len(custom_classes)} {'PASS' if len(custom_classes) <= 5 else 'FAIL'} (ideal: <=5) {custom_classes if custom_classes else ''}")
    print(f"Hex hardcodes: {len(hex_colors)} {'PASS' if len(hex_colors) == 0 else 'FAIL'} (ideal: 0)")
    print(f"Inline styles: {len(inline_styles)} {'PASS' if len(inline_styles) <= 8 else 'FAIL'} (con tokens: ok) {inline_styles if len(inline_styles) <= 12 else ''}")
    print(f"Aurora classes: {len(aurora_classes)} {'PASS' if len(aurora_classes) >= min_clases else 'FAIL'} (min landing: {min_clases})")
    print(f"Packs: {len(packs)} loaded")
    print(f"Body nz: {'PASS' if has_nz else 'FAIL'}")
    print(f"Body theme: {'PASS' if has_theme else 'FAIL'}")
    print(f"Body skin: {'PASS' if has_skin else 'FAIL'}")
    used = sum(1 for v in premium.values() if v)
    total = len(premium)
    print(f"Premium components: {used}/{total} used (v5 + v6)")
    for name, present in premium.items():
        print(f"  {'PASS' if present else 'FAIL'} {name}")
    if css_lines > 40 or len(custom_classes) > 10 or used < total * 0.5:
        print("VERDICT: NOT AURORA - needs redesign")
    elif css_lines <= 40 and len(custom_classes) <= 5 and used >= total * 0.7:
        print("VERDICT: AURORA OK")
    else:
        print("VERDICT: PARTIAL AURORA - improve premium components")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '-'
    audit(path)
