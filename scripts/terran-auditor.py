#!/usr/bin/env python3
"""
TerrAn Auditor — Motor de auto-auditoría cíclica.
Lee los docs de arquitectura + el estado de auditoría y genera un informe estructurado.

Modos:
  ./terran-auditor.py status         → Muestra estado actual
  ./terran-auditor.py run            → Ejecuta auditoría (fase actual)
  ./terran-auditor.py advance        → Avanza a siguiente fase
  ./terran-auditor.py reset          → Reinicia auditoría desde 0
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATE_PATH = Path("/root/workspace/geoasset/audit-state.json")
DOCS_PATHS = [
    Path("/root/workspace/geoasset/ARQUITECTURA.md"),
    Path("/root/workspace/geoasset/RENDIMIENTO-Y-NEGOCIO.md"),
    Path("/root/workspace/geoasset/DOCUMENTOS-Y-IA.md"),
]


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return None


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    print(f"✅ Estado guardado en {STATE_PATH}")


def get_current_phase(state):
    """Devuelve la fase actual (primera no-clear) o None si todo completado."""
    for phase in state["phases"]:
        if not phase["clear"]:
            return phase
    return None


def read_docs():
    """Lee todos los documentos de arquitectura y devuelve su contenido."""
    docs = {}
    for doc_path in DOCS_PATHS:
        if doc_path.exists():
            content = doc_path.read_text()
            # Truncar a ~30K para no saturar
            if len(content) > 30000:
                content = content[:30000] + "\n\n[... TRUNCADO - resto del archivo omitido ...]"
            docs[doc_path.name] = {
                "path": str(doc_path),
                "size_bytes": doc_path.stat().st_size,
                "lines": content.count("\n") + 1,
                "preview": content[:2000],
                "full_content": content
            }
        else:
            docs[doc_path.name] = {"error": "Archivo no encontrado"}
    return docs


def cmd_status():
    state = load_state()
    if not state:
        print("❌ No hay estado de auditoría. Ejecuta 'init' primero.")
        return 1

    current = get_current_phase(state)
    total = len(state["phases"])
    cleared = sum(1 for p in state["phases"] if p["clear"])
    total_issues = sum(len(p["issues_found"]) for p in state["phases"])
    total_fixed = sum(len(p["issues_fixed"]) for p in state["phases"])

    print(f"""
╔══════════════════════════════════════════════╗
║      📋 TERRÁN — AUTO-AUDITORÍA             ║
╠══════════════════════════════════════════════╣
║ Estado:       {state['status']:<30s} ║
║ Iteración:    {state['iteration']:<30d} ║
║ Fases:        {cleared}/{total} completadas{' ' * 24} ║
║ Issues:       {total_issues} encontrados, {total_fixed} fijados{' ' * 10} ║
║ Último run:   {state['last_run'] or 'nunca':<30s} ║
║ Completo:     {str(state['completed']):<30s} ║
╠══════════════════════════════════════════════╣
""")

    for phase in state["phases"]:
        icon = "✅" if phase["clear"] else ("🔄" if phase == current else "⏳")
        issues_n = len(phase["issues_found"])
        fixed_n = len(phase["issues_fixed"])
        print(f" {icon}  {phase['name']:<35s} ({issues_n} issues, {fixed_n} fixed)")

    if current:
        print(f"\n▶  Fase activa: {current['name']} ({current['id']})")
    if state["completed"]:
        print("\n🎉 ¡AUDITORÍA COMPLETA! No se encontraron más issues.")

    return 0


def cmd_run():
    """Ejecuta la auditoría para la fase actual y emite un JSON estructurado."""
    state = load_state()
    if not state:
        print("❌ No hay estado de auditoría.")
        return 1

    current = get_current_phase(state)
    if not current:
        print("🎉 ¡Todas las fases están limpias! La auditoría ha terminado.")
        state["completed"] = True
        state["status"] = "completed"
        save_state(state)
        return 0

    docs = read_docs()

    # Verificar qué docs existen
    docs_status = {}
    for name, doc_info in docs.items():
        docs_status[name] = "ok" if "full_content" in doc_info else "missing"

    output = {
        "action": "audit_run",
        "iteration": state["iteration"] + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "phase": {
            "id": current["id"],
            "name": current["name"],
            "description": current["description"],
            "issues_already_found": current["issues_found"],
            "issues_already_fixed": current["issues_fixed"]
        },
        "docs_available": docs_status,
        "docs_content": {k: v.get("full_content", "") for k, v in docs.items() if "full_content" in v},
        "state": state
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


def cmd_advance():
    """Marca la fase actual como completada y avanza a la siguiente."""
    state = load_state()
    if not state:
        print("❌ No hay estado de auditoría.")
        return 1

    current = get_current_phase(state)
    if not current:
        print("🎉 Ya están todas las fases completadas.")
        return 0

    current["clear"] = True
    state["last_run"] = datetime.utcnow().isoformat() + "Z"
    save_state(state)

    next_phase = get_current_phase(state)
    if next_phase:
        print(f"✅ Fase '{current['name']}' marcada como clara.")
        print(f"▶  Siguiente fase: '{next_phase['name']}'")
    else:
        print(f"✅ Fase '{current['name']}' marcada como clara.")
        state["completed"] = True
        state["status"] = "completed"
        save_state(state)
        print("🎉 ¡AUDITORÍA COMPLETA! Todas las fases pasadas.")

    return 0


def cmd_log_issue(phase_id, issue):
    """Registra un issue encontrado en una fase (para uso del cron)."""
    state = load_state()
    if not state:
        print("❌ No hay estado.")
        return 1

    for phase in state["phases"]:
        if phase["id"] == phase_id:
            # Evitar duplicados
            existing_ids = {i.get("id") for i in phase["issues_found"]}
            if issue.get("id") not in existing_ids:
                phase["issues_found"].append(issue)
                state["iteration"] += 1
                state["last_run"] = datetime.utcnow().isoformat() + "Z"
                save_state(state)
                print(f"✅ Issue registrado en fase '{phase['name']}': {issue.get('title', 'sin título')}")
            else:
                print(f"⏭️  Issue ya existe (ID: {issue.get('id')})")
            return 0

    print(f"❌ Fase '{phase_id}' no encontrada.")
    return 1


def cmd_log_fix(phase_id, issue_id, resolution):
    """Registra un issue como fijado."""
    state = load_state()
    if not state:
        print("❌ No hay estado.")
        return 1

    for phase in state["phases"]:
        if phase["id"] == phase_id:
            for i, issue in enumerate(phase["issues_found"]):
                if issue.get("id") == issue_id:
                    fixed = issue.copy()
                    fixed["resolution"] = resolution
                    fixed["fixed_at"] = datetime.utcnow().isoformat() + "Z"
                    phase["issues_fixed"].append(fixed)
                    phase["issues_found"].pop(i)
                    state["iteration"] += 1
                    state["last_run"] = datetime.utcnow().isoformat() + "Z"
                    save_state(state)
                    print(f"✅ Issue '{issue_id}' marcado como fijado.")
                    return 0
            print(f"❌ Issue '{issue_id}' no encontrado en fase '{phase['name']}'.")
            return 1

    print(f"❌ Fase '{phase_id}' no encontrada.")
    return 1


def cmd_reset():
    """Reinicia completamente la auditoría."""
    state = load_state()
    if state:
        confirm = input("¿Seguro? Se perderá todo el historial de auditoría. (s/N): ")
        if confirm.lower() != "s":
            print("Cancelado.")
            return 0

    for phase in state["phases"]:
        phase["clear"] = False
        phase["issues_found"] = []
        phase["issues_fixed"] = []

    state["iteration"] = 0
    state["status"] = "active"
    state["completed"] = False
    state["last_run"] = None
    state["audit_history"] = []
    save_state(state)
    print("🔄 Auditoría reiniciada.")
    return 0


def cmd_help():
    print("""
Terrán Auditor — Uso:

  python3 terran-auditor.py status     → Estado actual
  python3 terran-auditor.py run        → Ejecuta auditoría (fase actual)
  python3 terran-auditor.py advance    → Marca fase actual como completada
  python3 terran-auditor.py reset      → Reinicia auditoría desde 0

  Modo cron (uso interno):
  python3 terran-auditor.py log-issue <phase_id> '<json_issue>'
  python3 terran-auditor.py log-fix <phase_id> <issue_id> '<resolution>'
""")


def main():
    if len(sys.argv) < 2:
        cmd_help()
        return 0

    command = sys.argv[1]

    if command == "status":
        return cmd_status()
    elif command == "run":
        return cmd_run()
    elif command == "advance":
        return cmd_advance()
    elif command == "reset":
        return cmd_reset()
    elif command == "log-issue" and len(sys.argv) >= 4:
        phase_id = sys.argv[2]
        issue = json.loads(sys.argv[3])
        return cmd_log_issue(phase_id, issue)
    elif command == "log-fix" and len(sys.argv) >= 5:
        phase_id = sys.argv[2]
        issue_id = sys.argv[3]
        resolution = sys.argv[4]
        return cmd_log_fix(phase_id, issue_id, resolution)
    elif command == "help":
        cmd_help()
        return 0
    else:
        print(f"❌ Comando desconocido: {command}")
        cmd_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())