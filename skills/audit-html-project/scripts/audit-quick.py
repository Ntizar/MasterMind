#!/usr/bin/env python3
"""
Quick HTML project health check — run from project root.
Checks: line-number corruption, broken links, CSS brace balance, broken nav.
Usage: python3 audit-quick.py [directory]
"""
import re, os, sys

base = sys.argv[1] if len(sys.argv) > 1 else '.'
html_files = sorted(f for f in os.listdir(base) if f.endswith('.html'))
all_files = set(html_files)

issues = {'critical': [], 'warning': []}

for f in html_files:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        content = fh.read()

    # 1. Line number corruption
    line_nums = len(re.findall(r'^\s*\d+\|', content, re.MULTILINE))
    if line_nums > 0:
        issues['critical'].append(f"❌ {f}: {line_nums} line-number prefixes (N|)")

    # 2. Broken internal links
    hrefs = set(re.findall(r'href="([^"#]+\.html)"', content))
    for href in hrefs:
        if href not in all_files:
            issues['critical'].append(f"❌ {f} → {href} (DOES NOT EXIST)")

    # 3. CSS brace balance
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match:
        css = style_match.group(1)
        if css.count('{') != css.count('}'):
            issues['critical'].append(f"❌ {f}: CSS braces {css.count('{')} open vs {css.count('}')} close")

    # 4. Broken nav (href="#")
    empty_nav = re.findall(r'href="#"[^>]*>[^<]*(?:Anterior|Siguiente)', content)
    if empty_nav:
        issues['warning'].append(f"⚠️  {f}: broken nav link (href='#')")

    # 5. Unclosed style tags
    if content.count('<style>') != content.count('</style>'):
        issues['critical'].append(f"❌ {f}: unclosed <style> tag")

    # 6. Div imbalance > 3
    div_open = len(re.findall(r'<div(?:\s[^>]*)?>', content))
    div_close = content.count('</div>')
    if abs(div_open - div_close) > 3:
        issues['warning'].append(f"⚠️  {f}: div imbalance {div_open} open vs {div_close} close")

print(f"=== HTML Audit: {len(html_files)} files ===\n")
if issues['critical']:
    print(f"❌ CRITICAL ({len(issues['critical'])}):")
    for i in issues['critical']:
        print(f"  {i}")
    print()
if issues['warning']:
    print(f"⚠️  WARNINGS ({len(issues['warning'])}):")
    for w in issues['warning']:
        print(f"  {w}")
    print()
total = len(issues['critical']) + len(issues['warning'])
if total == 0:
    print("✅ All clean!")
else:
    print(f"Total: {len(issues['critical'])} critical, {len(issues['warning'])} warnings")
