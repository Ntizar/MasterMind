#!/usr/bin/env python3
"""Lectura del inventario de APIs desde estado.json.

Fuente de verdad: /tmp/inventario-apis/estado.json
Produce un resumen estructurado por categorías y progreso.
"""
import json
import sys
from datetime import datetime

INVENTORY_PATH = "/tmp/inventario-apis/estado.json"

def load_state(path=INVENTORY_PATH):
    with open(path, "r") as f:
        return json.load(f)

def classify_categories(state):
    """Clasifica categorías en completadas, en avance, en progreso, pendientes."""
    completadas = []
    casi_completas = []
    en_progreso = []
    pendientes = []

    for cat_id, cat in state["categorias"].items():
        if cat["total"] == 0:
            continue
        pct = cat["procesadas"] / cat["total"] * 100
        entry = (cat_id, cat, pct)
        if pct >= 90:
            completadas.append(entry)
        elif pct >= 50:
            casi_completas.append(entry)
        elif pct > 0:
            en_progreso.append(entry)
        else:
            pendientes.append(entry)

    completadas.sort(key=lambda x: x[2], reverse=True)
    casi_completas.sort(key=lambda x: x[2], reverse=True)
    en_progreso.sort(key=lambda x: x[2], reverse=True)
    pendientes.sort(key=lambda x: x[1]["total"], reverse=True)

    return completadas, casi_completas, en_progreso, pendientes

def get_today_activity(state, date=None):
    """Categorías actualizadas en la fecha dada."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return [
        (k, v) for k, v in state["categorias"].items()
        if v["ultima_actualizacion"] and v["ultima_actualizacion"].startswith(date)
    ]

def main():
    state = load_state()
    total = state["total_estimado"]
    processed = state["procesadas"]
    pct = processed / total * 100 if total > 0 else 0

    completadas, casi_completas, en_progreso, pendientes = classify_categories(state)

    print(f"Total APIs: {total:,}")
    print(f"Procesadas: {processed:,} ({pct:.1f}%)")
    print(f"Completadas (>90%): {len(completadas)}")
    print(f"En avance (50-90%): {len(casi_completas)}")
    print(f"En progreso (1-50%): {len(en_progreso)}")
    print(f"Pendientes (0%): {len(pendientes)}")
    if pendientes:
        total_pend = sum(v["total"] for _, v in pendientes)
        print(f"APIs pendientes: {total_pend:,}")

    # Actividad de hoy
    hoy = get_today_activity(state)
    if hoy:
        print(f"\nActividad hoy ({datetime.now().strftime('%Y-%m-%d')}):")
        for k, v in hoy:
            print(f"  {v['nombre']}: {v['procesadas']:,} APIs | {v['ultima_actualizacion']}")

if __name__ == "__main__":
    main()
