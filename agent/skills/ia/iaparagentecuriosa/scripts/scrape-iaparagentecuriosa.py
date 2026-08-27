#!/usr/bin/env python3
"""Extrae estructura completa de iaparagentecuriosa.dev fascículo por fascículo.
Usar: python scrape_iaparagentecuriosa_final.py
Output: /root/workspace/iaparagentecuriosa_final.json
"""
import json, re, subprocess, sys

BASE = "https://www.iaparagentecuriosa.686f6c61.dev"

def fetch(url):
    result = subprocess.run(["curl", "-s", url], capture_output=True, text=True, timeout=30)
    return result.stdout

def extract_numbered_chapters(html):
    """Extrae capítulos reales: h2 numerados (1. Título, 2. Título, etc.)."""
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    chapters = []
    for h in h2s:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        num_match = re.match(r'^(\d+)\.\s+(.+)$', clean)
        if num_match:
            chapters.append({"num": int(num_match.group(1)), "title": num_match.group(2).strip()})
    return chapters

def extract_notebooks(html):
    """Extrae cuadernos de Colab con descripciones completas."""
    notebooks = []
    for block in re.split(r'<article[^>]*>', html):
        title_m = re.search(r'<h4[^>]*>(.*?)</h4>', block, re.DOTALL)
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', block, re.DOTALL)
        colab_m = re.search(r'href="([^"]*colab[^"]*)"', block)
        if title_m:
            title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()
            descs = [re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs if re.sub(r'<[^>]+>', '', p).strip() and len(re.sub(r'<[^>]+>', '', p).strip()) > 50]
            desc = max(descs, key=len) if descs else ""
            if title and len(title) > 10:
                notebooks.append({"title": title, "description": desc[:500], "colab_url": colab_m.group(1) if colab_m else ""})
    return notebooks

# Extraer fascículos
fascicles = []
for i in range(1, 13):
    fid = f"{i:02d}"
    url = f"{BASE}/fasciculo-{fid}/"
    html = fetch(url)
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    title = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else ""
    desc_m = re.findall(r'<p[^>]*class="[^"]*lead[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    desc = re.sub(r'<[^>]+>', '', desc_m[0]).strip() if desc_m else ""
    chapters = extract_numbered_chapters(html)
    fascicles.append({"id": i, "number": fid, "title": title, "description": desc, "chapters": chapters, "chapter_count": len(chapters), "url": url})

# Cuadernos
cuadernos = extract_notebooks(fetch(f"{BASE}/cuadernos/"))

# Glosario
glosario_terms = [re.sub(r'<[^>]+>', '', t).strip() for t in re.findall(r'<dt[^>]*>(.*?)</dt>', fetch(f"{BASE}/glosario/"), re.DOTALL) if re.sub(r'<[^>]+>', '', t).strip()]

output = {"fascicles": fascicles, "cuadernos": cuadernos, "glosario_terms_sample": glosario_terms[:50], "glosario_total": len(glosario_terms)}

with open("/root/workspace/iaparagentecuriosa_final.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Capturado: {len(fascicles)} fascículos, {sum(f['chapter_count'] for f in fascicles)} capítulos, {len(cuadernos)} cuadernos, {len(glosario_terms)} términos")