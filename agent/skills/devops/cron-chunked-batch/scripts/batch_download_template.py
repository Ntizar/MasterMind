#!/usr/bin/env python3
"""
Batch download template — Two-phase scraper + downloader for rate-limited sites.

Phase 1: Scrape site to build index {unit: {subgroup: [urls]}}
Phase 2: Download files from index, skipping existing

Features:
  - Incremental index saving (resume after timeout)
  - Dry-run mode (--dry-run) to count before downloading
  - Filter by unit (--unit AT)
  - Retry failed (--reintentar)
  - Configurable delay (--delay=1.5)
  - Magic byte verification for PDFs
  - 429 backoff: 30s, 60s, 90s...

Usage:
  python3 batch_download.py                    # Scrape + download all
  python3 batch_download.py --dry-run           # Count only
  python3 batch_download.py --unit AT            # One unit only
  python3 batch_download.py --delay=2           # Custom delay
  python3 batch_download.py --reintentar        # Retry failed downloads
"""
import json
import re
import sys
import time
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, unquote

import requests

# === Config ===
BASE_URL = "https://example.com"
DATA_DIR = Path("/path/to/Data")
INDEX_FILE = DATA_DIR / "indice.json"
FALLIDOS_FILE = DATA_DIR / "fallidos.json"

# === Arguments ===
DELAY = 1.5
DRY_RUN = False
SOLO_UNIDAD = None
REINTENTAR = False
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == "--dry-run": DRY_RUN = True
    elif args[i] == "--reintentar": REINTENTAR = True
    elif args[i] == "--unit" and i + 1 < len(args): SOLO_UNIDAD = args[i + 1]; i += 1
    elif args[i].startswith("--delay="): DELAY = float(args[i].split("=")[1])
    i += 1

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
})

def fetch_html(url):
    """Fetch HTML with 429 backoff."""
    for intento in range(5):
        try:
            resp = SESSION.get(url, timeout=60, allow_redirects=True)
            if resp.status_code == 200: return resp.text
            elif resp.status_code == 429:
                wait = 30 * (intento + 1)
                print(f"429({wait}s)", end=" ", flush=True)
                time.sleep(wait)
            else: return None
        except Exception as e:
            print(f"err({e})", end=" ")
            time.sleep(10 * (intento + 1))
    return None

def extraer_pdfs(html):
    """Extract ALL pdf links from HTML. Captures any href ending in .pdf."""
    pdfs = set()
    for m in re.finditer(r'href="(/[^"]*\.pdf[^"]*)"', html, re.IGNORECASE):
        href = m.group(1).split("?")[0]
        pdfs.add(urljoin(BASE_URL, href))
    return sorted(pdfs)

def descargar_pdf(url, dest):
    """Download a PDF with retries. New connection each time."""
    for intento in range(8):
        try:
            resp = requests.get(url, timeout=120, allow_redirects=True)
            if resp.status_code == 200 and resp.content[:5] == b"%PDF-":
                dest.write_bytes(resp.content)
                return True
            elif resp.status_code == 429:
                time.sleep(30 * (intento + 1))
            else: return False
        except Exception: time.sleep(10 * (intento + 1))
    return False

def limpiar_nombre(nombre):
    nombre = unquote(nombre)
    nombre = re.sub(r'[<>:"/\\|?*]', '_', nombre)
    return re.sub(r'\s+', ' ', nombre).strip().lstrip(' -')

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    indice = {}
    if INDEX_FILE.exists() and not REINTENTAR:
        try: indice = json.load(open(INDEX_FILE))
        except: pass

    # Phase 1: Scrape
    for unidad in sorted(unidades):
        if unidad in indice and not REINTENTAR: continue
        html = fetch_html(url_unidad(unidad))
        if not html: continue
        subgrupos = extraer_subgrupos(html)
        for sg_url in subgrupos:
            time.sleep(1.0)  # delay between scrape requests
            sg_html = fetch_html(sg_url)
            if sg_html:
                pdfs = extraer_pdfs(sg_html)
                if pdfs: indice.setdefault(unidad, {}).setdefault(sg_key, []).extend(pdfs)
        json.dump(indice, open(INDEX_FILE, "w"))  # save after each unit

    total = sum(len(p) for u in indice.values() for p in u.values())
    print(f"Total: {len(indice)} units, {total} files")

    if DRY_RUN: return

    # Phase 2: Download
    for unidad, subgrupos in sorted(indice.items()):
        for subgrupo, urls in sorted(subgrupos.items()):
            dest_dir = DATA_DIR / unidad / subgrupo
            dest_dir.mkdir(parents=True, exist_ok=True)
            for url in urls:
                fname = limpiar_nombre(url.split("/")[-1])
                if not fname.endswith(".pdf"): fname += ".pdf"
                dest = dest_dir / fname
                if dest.exists() and dest.stat().st_size > 2000: continue
                if descargar_pdf(url, dest): print("✅")
                else: print("❌")
                time.sleep(DELAY)
