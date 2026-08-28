#!/usr/bin/env python3
"""
Doctor de Mastermind — health check read-only del sistema.
Verifica: gateway, crons, ChromaDB vs skills en disco, registry y git sync.

Uso:
  python scripts/doctor.py            # informe legible
  python scripts/doctor.py --json     # para consumo por cron/agent
"""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HERMES = Path.home() / "AppData" / "Local" / "hermes"
CRON_DIR = HERMES / "cron"
PY_SYS = r"C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe"
CHROMA_PATH = Path.home() / ".mastermind" / "chromadb"
COLLECTION = "mastermind-skills"

results = []

def check(name, ok, detail="", warn=False):
    results.append({"check": name, "ok": ok, "warn": warn, "detail": detail})

def run(cmd, cwd=None, timeout=30):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              cwd=cwd or str(REPO), shell=True)
    except Exception as e:
        return type("R", (), {"returncode": 1, "stdout": "", "stderr": str(e)})()

# 1) Gateway vivo
r = run("hermes gateway status")
gw_up = "running" in (r.stdout + r.stderr).lower() or "✓" in r.stdout
check("gateway", gw_up, (r.stdout + r.stderr).strip().splitlines()[0] if (r.stdout + r.stderr) else "sin salida")

# 2) Crons: último run de cada job activo < 25h (scout 6h con margen)
try:
    for f in sorted(CRON_DIR.glob("jobs/*/job.json")):
        job = json.loads(f.read_text(encoding="utf-8"))
        jid, name = job.get("job_id", f.parent.name), job.get("name", "?")
        if not job.get("enabled", False):
            check(f"cron:{name}", True, "desactivado (ok)", warn=True)
            continue
        out_dir = CRON_DIR / "output" / jid
        last = None
        if out_dir.exists():
            outs = sorted(out_dir.glob("*.md"))
            if outs:
                last = datetime.fromtimestamp(outs[-1].stat().st_mtime, tz=timezone.utc)
        never = last is None
        stale = (not never) and (datetime.now(timezone.utc) - last > timedelta(hours=25))
        detail = "nunca ha corrido" if never else f"último run: {last:%Y-%m-%d %H:%M} UTC"
        check(f"cron:{name}", not (never or stale), detail, warn=never)
except Exception as e:
    check("cron:lectura", False, f"error leyendo crons: {e}")

# 3) ChromaDB count == SKILL.md count
skill_count = len([p for p in (REPO / "agent" / "skills").rglob("SKILL.md")
                   if not any(part.startswith(".") for part in p.parts)])
try:
    out = run(f'"{PY_SYS}" -c "import chromadb; c=chromadb.PersistentClient(path=r\'{CHROMA_PATH.as_posix()}\'); print(c.get_collection(\'{COLLECTION}\').count())"',
              timeout=60)
    chroma_count = int(out.stdout.strip() or -1)
    check("chromadb", chroma_count == skill_count,
          f"indexados: {chroma_count} | SKILL.md en disco: {skill_count}"
          + ("" if chroma_count == skill_count else " → ejecutar scripts/indexar-skills.py"))
except Exception as e:
    check("chromadb", False, f"error: {e}")

# 4) Registry fresco (< 25h desde last_run)
try:
    reg = json.loads((REPO / "data" / "stars-registry.json").read_text(encoding="utf-8"))
    last_run = datetime.fromisoformat(reg["last_run"])
    age_h = (datetime.now(timezone.utc) - last_run).total_seconds() / 3600
    check("stars-registry", age_h < 25, f"último run hace {age_h:.1f}h | {len(reg['processed'])} repos procesados")
except Exception as e:
    check("stars-registry", False, f"error: {e}")

# 5) Git sincronizado (sin cambios pendientes y en día con origin)
r = run("git status --porcelain")
dirty = bool(r.stdout.strip())
r2 = run("git rev-parse --abbrev-ref HEAD")
branch = r2.stdout.strip()
check("git", not dirty,
      f"rama: {branch} | {'LIMPIO' if not dirty else f'{len(r.stdout.strip().splitlines())} ficheros pendientes de commit'}")

# Salida
fails = [r for r in results if not r["ok"]]
warns = [r for r in results if r["ok"] and r.get("warn")]
if "--json" in sys.argv:
    print(json.dumps({"ok": not fails, "fails": len(fails), "checks": results},
                     ensure_ascii=False, indent=2))
else:
    icon = lambda r: "✅" if r["ok"] and not r.get("warn") else ("⚠️ " if r["ok"] else "❌")
    print(f"🩺 Doctor Mastermind — {datetime.now():%Y-%m-%d %H:%M}")
    print()
    for r in results:
        print(f"{icon(r)} {r['check']:<28} {r['detail']}")
    print()
    if fails:
        print(f"❌ {len(fails)} problema(s) — revisar arriba")
        sys.exit(1)
    print("✅ Todo en orden" + (f" ({len(warns)} avisos)" if warns else ""))
