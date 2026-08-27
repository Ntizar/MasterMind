#!/usr/bin/env python3
"""
Scraper CKAN Genérico Multi-Portal — Template reutilizable
Adapta PORTALES para nuevos portales. Output: data/{portal}/catalogo.json + index.json

Uso:
  python3 ckan-multi-portal-scraper.py --all            # Todos los portales
  python3 ckan-multi-portal-scraper.py --portal aragon   # Uno específico
  python3 ckan-multi-portal-scraper.py --test            # Testear qué responden
"""
import json
import time
import requests
from pathlib import Path

DATA_DIR = Path("data") / "ckan"

# ═══════════════════════════════════════════════
# CONFIGURACIÓN: Añadir/portales aquí
# ═══════════════════════════════════════════════
PORTALES = {
    "aragon": {
        "nombre": "Aragón Open Data",
        "base": "https://opendata.aragon.es/api/3/action",
        "web": "https://opendata.aragon.es",
        "ccaa": "Aragón"
    },
    "madrid_ayunt": {
        "nombre": "Ayuntamiento de Madrid",
        "base": "https://datos.madrid.es/api/3/action",
        "web": "https://datos.madrid.es",
        "ccaa": "C. de Madrid"
    },
    "madrid_ccaa": {
        "nombre": "Comunidad de Madrid",
        "base": "https://datos.comunidad.madrid/api/3/action",
        "web": "https://datos.comunidad.madrid",
        "ccaa": "C. de Madrid"
    },
    # Añadir más portales:
    # "mi_portal": {
    #     "nombre": "Mi Portal",
    #     "base": "https://miportal.org/api/3/action",
    #     "web": "https://miportal.org",
    #     "ccaa": "CCAA"
    # },
}


def test_portal(portal_id, config):
    """Testea si un portal CKAN responde."""
    try:
        resp = requests.get(f"{config['base']}/package_search?rows=1", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("success"):
                return {"status": "ok", "datasets": data.get("result", {}).get("count", 0)}
    except:
        pass
    return {"status": "offline"}


def scrape_portal(portal_id, config, max_datasets=200):
    """Scrapea un portal CKAN completo."""
    portal_dir = DATA_DIR / portal_id
    portal_dir.mkdir(parents=True, exist_ok=True)
    base = config["base"]

    print(f"\n🌐 {config['nombre']} ({config['ccaa']})")

    # Organizaciones
    orgs = []
    try:
        resp = requests.get(f"{base}/organization_list", params={"all_fields": "true"}, timeout=30)
        orgs = resp.json().get("result", [])
    except:
        pass
    print(f"  📁 Organizaciones: {len(orgs)}")

    # Tags
    tags = []
    try:
        resp = requests.get(f"{base}/tag_list", params={"all_fields": "true"}, timeout=30)
        tags = resp.json().get("result", [])
    except:
        pass
    print(f"  🏷️ Etiquetas: {len(tags)}")

    # Datasets paginados
    all_datasets = []
    start = 0
    while start < max_datasets:
        try:
            resp = requests.get(f"{base}/package_search", params={"rows": 50, "start": start}, timeout=30)
            datasets = resp.json().get("result", {}).get("results", [])
            if not datasets:
                break
            all_datasets.extend(datasets)
            start += 50
            print(f"  📊 Datasets: {len(all_datasets)}...", end="\r")
            time.sleep(0.3)
        except:
            break

    print(f"  📊 Total datasets: {len(all_datasets)}")

    # Parsear catálogo
    catalogo = []
    for ds in all_datasets:
        recursos = []
        for r in ds.get("resources", []):
            recursos.append({
                "nombre": r.get("name", ""),
                "formato": r.get("format", ""),
                "url": r.get("url", ""),
                "tamaño": r.get("size", 0)
            })
        catalogo.append({
            "id": ds.get("name", ""),
            "titulo": ds.get("title", ""),
            "descripcion": (ds.get("notes", "") or "")[:500],
            "organizacion": ds.get("organization", {}).get("title", "") if ds.get("organization") else "",
            "etiquetas": [t.get("name", "") for t in ds.get("tags", [])],
            "fecha_creacion": ds.get("metadata_created", ""),
            "fecha_modificacion": ds.get("metadata_modified", ""),
            "recursos": recursos,
            "total_recursos": len(recursos)
        })

    # Guardar
    with open(portal_dir / "catalogo.json", "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)

    formatos = {}
    for ds in catalogo:
        for r in ds["recursos"]:
            fmt = r["formato"].upper()
            if fmt:
                formatos[fmt] = formatos.get(fmt, 0) + 1

    index = {
        "portal": portal_id, "nombre": config["nombre"], "ccaa": config["ccaa"],
        "web": config["web"], "total_datasets": len(catalogo),
        "total_recursos": sum(d["total_recursos"] for d in catalogo),
        "organizaciones": len(orgs), "etiquetas": len(tags),
        "formatos": dict(sorted(formatos.items(), key=lambda x: -x[1])[:20])
    }
    with open(portal_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"  ✅ {len(catalogo)} datasets, {index['total_recursos']} recursos")
    return index


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--portal", help="Portal específico")
    parser.add_argument("--max", type=int, default=200)
    args = parser.parse_args()

    if args.test:
        for pid, cfg in PORTALES.items():
            r = test_portal(pid, cfg)
            print(f"  {'✅' if r['status']=='ok' else '❌'} {cfg['nombre']}: {r.get('datasets',0)} datasets")
    elif args.portal and args.portal in PORTALES:
        scrape_portal(args.portal, PORTALES[args.portal], args.max)
    else:
        for pid, cfg in PORTALES.items():
            try:
                scrape_portal(pid, cfg, args.max)
            except Exception as e:
                print(f"  ❌ {pid}: {e}")
            time.sleep(0.5)
