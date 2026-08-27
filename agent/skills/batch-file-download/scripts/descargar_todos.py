#!/usr/bin/env python3
"""
ERAVisor — Descargar TODOS los PDFs restantes
Script robusto: un PDF = una nueva conexión. Sin session keep-alive.
Carga los índices y descarga todo lo que falte.

Uso:
    python3 scripts/descargar_todos.py [--delay SEGS] [--dry-run]

Ejemplo:
    python3 scripts/descargar_todos.py --delay 1
    python3 scripts/descargar_todos.py --dry-run  # solo cuenta
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime

import requests

BASE = Path("/root/workspace/ERAVisor")
PDF_DIR = BASE / "pdfs"
DATA_DIR = BASE / "data"

# Parse args
DELAY = 1.0
DRY_RUN = False
for arg in sys.argv[1:]:
    if arg == "--dry-run":
        DRY_RUN = True
    elif arg.startswith("--delay"):
        DELAY = float(arg.split("=")[1] if "=" in arg else sys.argv[sys.argv.index(arg) + 1])

# === Cargar índices ===
def cargar_indices():
    indices = {}
    for idx_file in DATA_DIR.glob("*-investigations-index.json"):
        pais = idx_file.stem.split("-")[0].upper()
        try:
            data = json.load(open(idx_file))
            reports = data.get("reports", [])
            indices[pais] = reports
        except Exception as e:
            print(f"⚠️ Error cargando {idx_file.name}: {e}")
    return indices

# === Descargar un PDF — CONEXIÓN NUEVA POR PDF ===
def descargar_pdf(pdf_url, dest_path):
    """Descarga con conexión nueva cada vez. 8 intentos con backoff."""
    for intento in range(8):
        try:
            # Conexión nueva cada vez — sin session
            resp = requests.get(pdf_url, timeout=120, allow_redirects=True)
            
            if resp.status_code == 200 and resp.content[:5] == b"%PDF-":
                return True
            elif resp.status_code == 429:
                delay = 30 * (intento + 1)
                print(f"⏳ 429, retry en {delay}s...", end=" ", flush=True)
                time.sleep(delay)
            else:
                # Error HTTP — no reintentar
                return False
        except requests.exceptions.ConnectionError:
            delay = 10 * (intento + 1)
            print(f"Conn error, retry en {delay}s...", end=" ", flush=True)
            time.sleep(delay)
        except requests.exceptions.Timeout:
            delay = 15 * (intento + 1)
            print(f"Timeout, retry en {delay}s...", end=" ", flush=True)
            time.sleep(delay)
        except Exception as e:
            print(f"Error: {e}", end=" ", flush=True)
            time.sleep(5)
    return False

# === Main ===
def main():
    print("=" * 70)
    print(f"🚆 ERAVisor — Descarga masiva de PDFs")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Delay entre descargas: {DELAY}s")
    print(f"   Dry-run: {DRY_RUN}")
    print("=" * 70)

    indices = cargar_indices()
    if not indices:
        print("❌ No hay índices disponibles")
        sys.exit(1)

    # Calcular totales
    total_reports = sum(len(r) for r in indices.values())
    
    # Calcular pendientes
    pendientes_info = []
    for pais in sorted(indices.keys()):
        reports = indices[pais]
        pendientes = 0
        for r in reports:
            fname = f"{pais}_{r['year']}_{r['title']}"
            path = PDF_DIR / pais / fname
            if not path.exists() or path.stat().st_size <= 2000:
                pendientes += 1
        pendientes_info.append((pais, len(reports), pendientes))
    
    total_pendientes = sum(p[2] for p in pendientes_info)
    
    print(f"\n📡 {len(indices)} países, {total_reports} informes en total\n")
    
    for pais, total, pend in pendientes_info:
        if pend > 0:
            print(f"  {pais}: {pend}/{total} pendientes")
    
    print(f"\n📊 Total pendientes: {total_pendientes}")
    
    if total_pendientes == 0:
        print("✅ ¡Todos los PDFs ya están descargados!")
        return
    
    if DRY_RUN:
        return

    # === Descarga real ===
    total_exitosos = 0
    total_fallidos = 0
    total_saltados = 0
    inicio = time.time()
    
    for pais in sorted(indices.keys()):
        reports = indices[pais]
        pais_dir = PDF_DIR / pais
        pais_dir.mkdir(parents=True, exist_ok=True)
        
        pais_pendientes = 0
        for r in reports:
            fname = f"{pais}_{r['year']}_{r['title']}"
            path = pais_dir / fname
            if not path.exists() or path.stat().st_size <= 2000:
                pais_pendientes += 1
        
        if pais_pendientes == 0:
            print(f"\n✅ [{pais}] Todos descargados ({len(reports)})")
            continue
        
        print(f"\n{'─' * 70}")
        print(f"📦 [{pais}] {pais_pendientes} pendientes de {len(reports)}")
        print(f"{'─' * 70}")
        
        pais_exitosos = 0
        pais_fallidos = 0
        
        for i, r in enumerate(reports):
            title = r["title"]
            year = r["year"]
            pdf_url = r["pdf_url"]
            
            fname = f"{pais}_{year}_{title}"
            path = pais_dir / fname
            
            # Verificar si ya existe (por si acaso)
            if path.exists() and path.stat().st_size > 2000:
                total_saltados += 1
                continue
            
            name_short = f"{year} - {title[:50]}"
            print(f"  [{i+1}/{len(reports)}] {name_short}", end=" ", flush=True)
            
            if descargar_pdf(pdf_url, path):
                total_exitosos += 1
                pais_exitosos += 1
                print("✅")
            else:
                total_fallidos += 1
                pais_fallidos += 1
                print("❌")
            
            time.sleep(DELAY)
        
        elapsed = time.time() - inicio
        print(f"\n  [{pais}] Resultado: {pais_exitosos}✅ {pais_fallidos}❌ (tiempo: {elapsed/60:.1f}min)")
    
    duration = time.time() - inicio
    
    print(f"\n{'=' * 70}")
    print(f"✅ RESUMEN FINAL")
    print(f"{'=' * 70}")
    print(f"   ⏱️ Duración: {duration/60:.1f} min ({duration:.0f} seg)")
    print(f"   ✅ Exitosos: {total_exitosos}")
    print(f"   ❌ Fallidos: {total_fallidos}")
    print(f"   ⏭️ Saltados (ya existían): {total_saltados}")
    print(f"   📊 Total informes: {total_reports}")
    if total_fallidos > 0:
        print(f"   📦 Restantes no descargados: {total_fallidos}")
    print(f"{'=' * 70}")

    # Guardar log
    stats = {
        "total_pendientes": total_pendientes,
        "exitosos": total_exitosos,
        "fallidos": total_fallidos,
        "saltados": total_saltados,
        "duracion_seg": round(duration, 1),
        "fecha": datetime.now().isoformat()
    }
    log_path = DATA_DIR / "descarga_todos.json"
    json.dump(stats, open(log_path, "w"), indent=2)
    print(f"📄 Log guardado: {log_path}")


if __name__ == "__main__":
    main()
