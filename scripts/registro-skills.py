#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registro-skills.py — Registro real de uso de skills a partir de state.db.

Hermes guarda cada llamada a skill_view en la tabla `messages` (tool_name='skill_view')
y el RESULTADO (JSON con el campo `name`) en `content`. Este script lee esa tabla
(read-only), extrae el nombre del skill cargado en cada llamada, y agrupa el uso
por semana (lunes a domingo) para ver qué skills se cargan de verdad.

Uso:
  python registro-skills.py                 # resumen de las últimas 8 semanas
  python registro-skills.py --weeks 12      # últimas 12 semanas
  python registro-skills.py --skill foo     # detalle de un skill concreto
  python registro-skills.py --json          # salida JSON (para crons/digest)

No requiere chromadb ni red: solo stdlib (sqlite3, json, datetime, argparse).
"""

import argparse
import json
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, timedelta


def week_start(ts):
    """Devuelve el lunes (00:00) de la semana de ts (float unix)."""
    d = datetime.fromtimestamp(ts)
    monday = d - timedelta(days=d.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def load_usage(db):
    """Lee todas las llamadas a skill_view y devuelve (skill, week, ts)."""
    con = sqlite3.connect("file:" + db + "?mode=ro", uri=True)
    cur = con.cursor()
    rows = cur.execute(
        "SELECT content, timestamp FROM messages "
        "WHERE tool_name='skill_view' AND content LIKE '%\"name\"%'"
    ).fetchall()
    usage = []  # (skill, file_or_None, week_dt, ts)
    bad = 0
    for content, ts in rows:
        if not content:
            continue
        try:
            parsed = json.loads(content)
        except (ValueError, TypeError):
            bad += 1
            continue
        name = parsed.get("name")
        if not name:
            continue
        fpath = parsed.get("file") or parsed.get("file_path")
        try:
            week = week_start(ts)
        except (ValueError, OSError, OverflowError):
            continue
        usage.append((name, fpath, week, ts))
    con.close()
    return usage, bad


def summarize(usage, weeks, skill_filter=None):
    # por semana
    weeks_ordered = sorted({w for _, _, w, _ in usage})
    if weeks:
        cutoff = weeks_ordered[-1] - timedelta(weeks=weeks - 1) if weeks_ordered else None
    else:
        cutoff = None

    # per-skill total
    per_skill = defaultdict(int)
    per_skill_last = {}
    per_skill_weeks = defaultdict(lambda: defaultdict(int))
    file_loads = defaultdict(int)
    for name, fpath, week, ts in usage:
        if skill_filter and skill_filter not in name:
            continue
        if cutoff and week < cutoff:
            continue
        per_skill[name] += 1
        per_skill_last[name] = max(per_skill_last.get(name, 0), ts)
        per_skill_weeks[name][week] += 1
        if fpath:
            file_loads[name] += 1

    # resumen semanal
    weekly = defaultdict(int)
    for _, _, week, _ in usage:
        if skill_filter and skill_filter not in _[0]:
            continue
        if cutoff and week < cutoff:
            continue
        weekly[week] += 1

    return {
        "weeks": sorted({w for _, _, w, _ in usage if not cutoff or w >= cutoff}),
        "weekly_counts": {w.isoformat(): weekly.get(w, 0) for w in sorted(weekly)},
        "per_skill": dict(sorted(per_skill.items(), key=lambda kv: kv[1], reverse=True)),
        "per_skill_last": {k: datetime.fromtimestamp(v).strftime("%Y-%m-%d") for k, v in per_skill_last.items()},
        "file_loads": dict(file_loads),
        "total_loads": sum(per_skill.values()),
        "skills_count": len(per_skill),
    }


def render_human(data):
    lines = []
    lines.append("=== REGISTRO DE USO DE SKILLS (desde state.db) ===")
    lines.append(f"Total cargas en ventana: {data['total_loads']} | skills distintos: {data['skills_count']}"
                 + (f" | errores de parseo: {data['parse_errors']}" if data['parse_errors'] else ""))
    lines.append("")
    lines.append("--- Cargas por semana ---")
    for w in data["weeks"]:
        lines.append(f"  {w.isoformat()}: {data['weekly_counts'].get(w.isoformat(), 0)}")
    lines.append("")
    lines.append("--- Top skills por nº de cargas ---")
    for name, cnt in list(data["per_skill"].items())[:40]:
        last = data["per_skill_last"].get(name, "?")
        fl = data["file_loads"].get(name, 0)
        extra = f" (incluye {fl} carga(s) de reference/archivo)" if fl else ""
        lines.append(f"  {cnt:>4}  {name}{extra}  [último: {last}]")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weeks", type=int, default=8)
    ap.add_argument("--skill", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    db = os.path.expandvars(r"%LOCALAPPDATA%\hermes\state.db")
    if not os.path.exists(db):
        print("No se encuentra state.db en:", db)
        sys.exit(1)

    usage, bad = load_usage(db)
    data = summarize(usage, args.weeks, args.skill)
    data["parse_errors"] = bad

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print(render_human(data))


if __name__ == "__main__":
    main()
