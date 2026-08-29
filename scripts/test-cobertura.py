#!/usr/bin/env python3
"""
Test de cobertura semántica: valida que consultar-skills.py devuelve los
skills esperados en el top-3 para consultas canónicas (data/queries-test.json).

Ejecutar tras cada reindexado o cambio de modelo de embeddings.
Umbral por defecto: 85% de consultas con un expected en el top-3.

Uso:
  python scripts/test-cobertura.py            # informe legible
  python scripts/test-cobertura.py --json     # para cron/agent
"""
import json
import subprocess
import sys
from pathlib import Path

PY_SYS = r"C:/Users/d_ant/AppData/Local/Programs/Python/Python312/python.exe"
REPO = Path(__file__).resolve().parent.parent
SUITE = REPO / "data" / "queries-test.json"
TOP_K = 3

def consultar(q: str) -> list:
    r = subprocess.run([PY_SYS, str(REPO / "scripts" / "consultar-skills.py"), q, "--json"],
                       capture_output=True, text=True, timeout=120, cwd=str(REPO))
    data = json.loads(r.stdout)
    if isinstance(data, list):
        return data
    return data.get("results") or data.get("skills") or []

def main():
    suite = json.loads(SUITE.read_text(encoding="utf-8"))
    casos = []
    for c in suite["consultas"]:
        try:
            res = consultar(c["q"])
            top3 = [r["name"] for r in res[:TOP_K]]
            acierto = next((s for s in c["expected"] if s in top3), None)
            casos.append({"q": c["q"], "top3": top3, "esperado": c["expected"],
                          "ok": acierto is not None, "acierto": acierto})
        except Exception as e:
            casos.append({"q": c["q"], "top3": [], "esperado": c["expected"],
                          "ok": False, "acierto": None, "error": str(e)[:120]})

    ok_n = sum(1 for c in casos if c["ok"])
    pct = ok_n * 100 // len(casos)
    umbral = suite.get("umbral_top3_pct", 85)

    if "--json" in sys.argv:
        print(json.dumps({"ok": pct >= umbral, "pct": pct, "umbral": umbral,
                          "casos": casos}, ensure_ascii=False, indent=2))
        sys.exit(0 if pct >= umbral else 1)

    print(f"🎯 Cobertura semántica — {ok_n}/{len(casos)} ({pct}%, umbral {umbral}%)\n")
    for c in casos:
        if c["ok"]:
            print(f"✅ {c['acierto']:<38} ← {c['q'][:60]}")
        else:
            print(f"❌ {c['q'][:60]}")
            print(f"   top3: {c['top3']}")
            print(f"   esperado (cualquiera): {c['esperado']}")
    print()
    if pct >= umbral:
        print(f"✅ Umbral superado ({pct}% ≥ {umbral}%)")
    else:
        print(f"❌ Por debajo del umbral ({pct}% < {umbral}%) — revisar indexación")
        sys.exit(1)

if __name__ == "__main__":
    main()
