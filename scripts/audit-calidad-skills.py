#!/usr/bin/env python3
"""Auditoría anti-slop: calidad real del contenido de los skills."""
import re
import datetime
from pathlib import Path

base = Path("agent/skills")
sk = [p for p in base.rglob("SKILL.md") if not any(x.startswith(".") for x in p.parts)]
total = len(sk)
vacio, corto, con_fechas, con_comandos, con_urls = [], [], 0, 0, 0
for p in sk:
    t = p.read_text(encoding="utf-8", errors="ignore")
    body = re.sub(r"^---.*?---\s*", "", t, count=1, flags=re.S).strip()
    if len(body) < 120:
        vacio.append(p)
    elif len(body) < 400:
        corto.append(p)
    if re.search(r"20\d\d-\d\d-\d\d", t):
        con_fechas += 1
    if re.search(r"```(bash|sh|shell|powershell)", t):
        con_comandos += 1
    if re.search(r"https?://", t):
        con_urls += 1

print(f"SKILL.md totales: {total}")
print(f"Cuerpo <120 chars (sospechoso de hueco): {len(vacio)}")
for p in vacio[:10]:
    print("   HUECO:", p)
print(f"Cuerpo 120-400 chars (delgado): {len(corto)}")
for p in corto[:8]:
    print("   delgado:", p)
print(f"Con fechas: {con_fechas} ({con_fechas*100//total}%) | "
      f"Con comandos: {con_comandos} ({con_comandos*100//total}%) | "
      f"Con URLs: {con_urls} ({con_urls*100//total}%)")

corte = datetime.datetime.now().timestamp() - 30 * 86400
frescos = sum(1 for p in sk if p.stat().st_mtime > corte)
print(f"Modificados en últimos 30 días: {frescos} ({frescos*100//total}%)")

m = Path("agent/MEMORY.md")
print(f"MEMORY.md: {m.stat().st_size} bytes, "
      f"{len(m.read_text(encoding='utf-8', errors='ignore').splitlines())} líneas")
