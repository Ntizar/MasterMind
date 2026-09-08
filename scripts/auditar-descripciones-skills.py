#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auditar-descripciones-skills.py — Detecta skills cuya descripción NO dispara bien.

El catálogo de skills se inyecta en el prompt del agente y se trunca a 57 chars
+ "...". Para que un skill se reconozca como relevante, su descripción debe tener
un TRIGGER autocontenido en esa ventana (verbo/capacidad específica). Este script
puntúa lo débil que es el arranque de la descripción de cada SKILL.md.

Criterios de debilidad:
  - Frase genérica inicial ("Ecosistema completo de", "Usa a", "Use al", "Guía
    completa", "Patrones de", "Procedimiento", "Conocimiento completo"...).
  - Los primeros 57 chars no contienen un verbo/capacidad reconocible.
  - Descripción muy larga (>120) o muy corta (<12, sin información).
  - Repite el nombre del skill.

Uso:
  python auditar-descripciones-skills.py            # lista rankeada de débiles
  python auditar-descripciones-skills.py --json     # JSON para procesar
  python auditar-descripciones-skills.py --dir <ruta>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Frases genéricas que no funcionan como trigger
GENERIC_PREFIXES = [
    "ecosistema completo de", "ecosistema de", "usar a", "usa a", "usar al",
    "usa al", "use al", "usar para", "usa para", "use al ejecutar",
    "use al trabajar", "use al crear", "use when", "use cuando",
    "guía completa de", "guía de", "guia completa", "patrón para",
    "patron para", "patrones para", "patrones de", "procedimiento para",
    "procedimiento", "conocimiento completo", "framework de", "cómo construir",
    "como construir", "tutorial", "catálogo de", "catalogo de", "índice de",
    "index de", "colección de", "coleccion de", "lista de", "recurso",
    "recursos de", "diseñar un", "diseñar una", "montar un", "montar una",
    "crear un", "crear una", "generar un", "convertir un", "conectar",
    "usar para trabajar", "patrones completos", "serie de", "fundamentos de",
]

# Verbos/capacidades que sí hacen trigger
TRIGGER_WORDS = [
    "convertir", "desplegar", "montar", "crear", "generar", "detectar",
    "parsear", "extraer", "analizar", "resolver", "construir", "auditar",
    "clonar", "editar", "predecir", "calcular", "visualizar", "simular",
    "trackear", "monitorizar", "mapear", "clasificar", "reconocer", "inferir",
    "traducir", "transcribir", "exportar", "importar", "clonar", "configurar",
    "instalar", "optimizar", "automatizar", "generar", "diseñar", "procesar",
    "scrapear", "crawlear", "automatizar", "orquestar", "delegar", "validar",
    "modelar", "renderizar", "exponer", "consultar", "gestionar", "controlar",
]


def first57(text):
    return text[:57]


def has_trigger(text):
    low = text.lower()
    return any(w in low for w in TRIGGER_WORDS)


# Palabras "genéricas" que no aportan contenido; si la ventana de 57 chars
# apenas tiene palabras FUERA de esta lista, la descripción no dispara.
STOPWORDS = {
    "de", "la", "el", "los", "las", "al", "a", "un", "una", "y", "o", "en",
    "con", "que", "del", "para", "por", "completa", "completo", "ecosistema",
    "patrones", "procedimiento", "guía", "guia", "serie", "catálogo", "catalogo",
    "índice", "indice", "usar", "usa", "use", "usar", "usando", "cuando",
    "trabajar", "ejecutar", "crear", "montar", "convertir", "como", "cómo",
    "sobre", "tema", "todo", "toda", "todos", "todas", "uso", "u", "e", "para",
    "una", "al", "a", "de", "del", "la", "lo", "las", "los", "y", "o", "que",
    "en", "con", "sin", "para", "por", "se", "su", "sus", "más", "mas", "a",
    "esta", "este", "esto", "estos", "estas", "hacer", "haz", "hacer",
}


def content_words(text):
    """Palabras de la ventana de 57 chars que NO son genéricas."""
    t57 = text[:57]
    words = re.findall(r"[a-záéíóúñüç]{3,}", t57.lower())
    return [w for w in words if w not in STOPWORDS]


def generic_prefix(text):
    low = text.lower().strip()
    for g in GENERIC_PREFIXES:
        if low.startswith(g):
            return g
    return None


def weakness(text):
    """Devuelve (score_0_a_1, lista_de_razones). Mayor = más débil."""
    reasons = []
    score = 0.0
    t57 = text[:57]
    cw = content_words(text)

    # Si en los primeros 57 chars hay menos de 3 palabras de contenido
    # específico, la descripción no dice qué hace en la ventana del trigger.
    if len(cw) < 3:
        reasons.append(f"solo {len(cw)} palabra(s) de contenido en la ventana 57ch")
        score += 0.7

    g = generic_prefix(text)
    if g:
        reasons.append(f"frase genérica '{g}'")
        score += 0.3

    if len(text) > 160:
        reasons.append(f"muy larga ({len(text)} chars)")
        score += 0.1

    if len(text) < 12:
        reasons.append(f"corta ({len(text)} chars) sin información")
        score += 0.3

    return min(score, 1.0), reasons


def walk_skills(root):
    import yaml
    found = []
    for sp in sorted(Path(root).rglob("SKILL.md")):
        txt = sp.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^---\n(.*?)\n---\n", txt, re.DOTALL)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1))
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        desc = fm.get("description", "")
        if not desc:
            desc = fm.get("desc", "")
        desc = str(desc).strip().strip('"').strip("'")
        # nombre de la carpeta
        name = sp.parent.name
        found.append({"name": name, "desc": desc, "path": str(sp)})
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--dir", default=os.path.expandvars(r"%LOCALAPPDATA%\hermes\skills"))
    ap.add_argument("--limit", type=int, default=0, help="solo las N más débiles")
    args = ap.parse_args()

    skills = walk_skills(args.dir)
    scored = []
    for s in skills:
        sc, reasons = weakness(s["desc"])
        scored.append({**s, "score": round(sc, 2), "reasons": reasons,
                       "trigger57": first57(s["desc"])})

    scored.sort(key=lambda x: x["score"], reverse=True)
    if args.limit:
        scored = scored[: args.limit]

    if args.json:
        print(json.dumps(scored, ensure_ascii=False, indent=2))
        return

    print(f"=== AUDITORÍA DE DESCRIPCIONES ({len(skills)} skills escaneados) ===")
    print(f"Total con algún indicio de descripción débil: "
          f"{sum(1 for s in scored if s['score'] > 0)}")
    print("")
    for s in scored:
        if s["score"] == 0:
            continue
        print(f"[{s['score']:.2f}] {s['name']}")
        print(f"    razones: {', '.join(s['reasons'])}")
        print(f"    57ch:    {s['trigger57']}")


if __name__ == "__main__":
    main()
