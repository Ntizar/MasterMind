#!/usr/bin/env python3
"""Aurora Design System - Audit HTML against Aurora Design System.

Usage:
  python3 audit-aurora.py <file.html>
  curl -s <url> | python3 audit-aurora.py -
"""
import sys
import re

def audit(html_path):
    if html_path == '-':
        html = sys.stdin.read()
    else:
        with open(html_path) as f:
            html = f.read()

    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    css = style_match.group(1) if style_match else ''
    css_lines = len(css.strip().split('\n')) if css.strip() else 0

    all_classes = re.findall(r'\.([a-zA-Z][a-zA-Z0-9_-]*)', css)
    custom_classes = sorted(set(c for c in all_classes if not c.startswith('nz-')))
    hex_colors = re.findall(r'#[0-9a-fA-F]{3,8}\b', css)
    inline_styles = re.findall(r'style="[^"]*"', html)
    aurora_classes = sorted(set(re.findall(r'nz-[a-zA-Z0-9_-]+', html)))
    css_links = re.findall(r'href="([^"]*ntizar[^"]*)"', html)
    packs = sorted(set(css_links))
    body_match = re.search(r'<body([^>]*)>', html)
    body_attrs = body_match.group(1) if body_match else ''

    premium = {
        'nz-aurora-mesh': 'nz-aurora-mesh' in html,
        'nz-orb': 'nz-orb' in html,
        'nz-anim-fade-in': 'nz-anim-fade-in' in html,
        'nz-hover-lift': 'nz-hover-lift' in html,
        'nz-kpi': 'nz-kpi' in html,
        'nz-chart--glass': 'nz-chart--glass' in html,
        'nz-progress': 'nz-progress' in html,
        'nz-bento-grid': 'nz-bento-grid' in html,
        'nz-table': 'nz-table' in html,
        'nz-modal': 'nz-modal' in html,
        'nz-skeleton': 'nz-skeleton' in html,
        'nz-badge': 'nz-badge' in html,
        'nz-tabs': 'nz-tabs' in html,
        'nz-nav--glass': 'nz-nav--glass' in html,
        'nz-data-card': 'nz-data-card' in html,
        'nz-stats-banner': 'nz-stats-banner' in html,
        'nz-stack': 'nz-stack' in html,
        'nz-divider': 'nz-divider' in html,
        'nz-spinner': 'nz-spinner' in html,
        'nz-search': 'nz-search' in html,
        'nz-callout': 'nz-callout' in html,
    }

    has_nz = 'class="nz"' in html or "class='nz'" in html
    has_theme = 'data-nz-theme=' in body_attrs
    has_skin = 'data-nz-skin=' in body_attrs

    print("AURORA AUDIT REPORT")
    print("=" * 50)
    print(f"CSS custom: {css_lines} lines {'PASS' if css_lines <= 30 else 'FAIL'} (limit: 30)")
    print(f"Custom classes: {len(custom_classes)} {'PASS' if len(custom_classes) <= 5 else 'FAIL'} (ideal: <=5)")
    print(f"Hex hardcodes: {len(hex_colors)} {'PASS' if len(hex_colors) == 0 else 'FAIL'} (ideal: 0)")
    print(f"Inline styles: {len(inline_styles)} {'PASS' if len(inline_styles) <= 3 else 'FAIL'} (ideal: <=3)")
    print(f"Aurora classes: {len(aurora_classes)} {'PASS' if len(aurora_classes) >= 100 else 'FAIL'} (min: 100)")
    print(f"Packs: {len(packs)} loaded")
    print(f"Body nz: {'PASS' if has_nz else 'FAIL'}")
    print(f"Body theme: {'PASS' if has_theme else 'FAIL'}")
    print(f"Body skin: {'PASS' if has_skin else 'FAIL'}")
    used = sum(1 for v in premium.values() if v)
    total = len(premium)
    print(f"Premium components: {used}/{total} used")
    for name, present in premium.items():
        print(f"  {'PASS' if present else 'FAIL'} {name}")
    if css_lines > 30 or len(custom_classes) > 10 or used < total * 0.5:
        print("VERDICT: NOT AURORA - needs redesign")
    elif css_lines <= 30 and len(custom_classes) <= 5 and used >= total * 0.7:
        print("VERDICT: AURORA OK")
    else:
        print("VERDICT: PARTIAL AURORA - improve premium components")

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '-'
    audit(path)
