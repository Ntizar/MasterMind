#!/usr/bin/env python3
"""
Sincronizador bidireccional de skills: instalación Hermes <-> repo.
Ambos lados quedan con la unión de ambos conjuntos (nunca borra).
Uso: python scripts/sincronizar-skills.py [--dry]
"""
import shutil
import sys
from pathlib import Path

INST = Path("C:/Users/d_ant/AppData/Local/hermes/skills")
REPO = Path("C:/Users/d_ant/Projects/MasterMind/agent/skills")
DRY = "--dry" in sys.argv

def rel_skills(base: Path):
    return {str(p.relative_to(base)).replace("\\", "/")
            for p in base.rglob("SKILL.md")}

def sync_dir(rel: str, origen: Path, destino: Path):
    src = origen / rel
    src = src.parent if src.name == "SKILL.md" else src
    dst = destino / src.relative_to(origen)
    if DRY:
        print(f"  [dry] {src.relative_to(origen)} → {dst}")
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)

def main():
    i, r = rel_skills(INST), rel_skills(REPO)
    solo_i = sorted(i - r)
    solo_r = sorted(r - i)
    print(f"Instalación: {len(i)} | Repo: {len(r)}")
    print(f"→ copiar instalación→repo: {len(solo_i)}")
    for s in solo_i:
        print(f"  + {s}")
    print(f"→ copiar repo→instalación: {len(solo_r)}")
    for s in solo_r:
        print(f"  + {s}")
    if DRY:
        print("[dry-run: nada copiado]")
        return
    for s in solo_i:
        sync_dir(s, INST, REPO)
    for s in solo_r:
        sync_dir(s, REPO, INST)
    fi, fr = len(rel_skills(INST)), len(rel_skills(REPO))
    print(f"\nOK — tras sincronizar: instalación {fi} | repo {fr}")

if __name__ == "__main__":
    main()
