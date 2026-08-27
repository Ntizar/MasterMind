#!/usr/bin/env python3
"""
Generador del Dashboard de Estado del Mastermind.
Recopila datos de todos los subsistemas y actualiza el HTML.
"""
import os
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime

DASHBOARD_HTML = "/root/workspace/Mastermind/dashboard/mastermind-status.html"
DATA_DIR = "/root/workspace/Mastermind/learning"

def get_chromadb_status():
    """Verificar ChromaDB."""
    try:
        result = subprocess.run(
            ["curl", "-s", "--max-time", "5", "http://localhost:8000/api/v1/collections"],
            capture_output=True, text=True, timeout=8
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            count = len(data) if isinstance(data, list) else 0
            return {"status": "online", "count": count, "lastReindex": "check cron"}
    except Exception:
        pass
    return {"status": "offline", "count": 0, "lastReindex": "unknown"}

def get_skills_stats():
    """Contar skills por prioridad."""
    priority_file = "/root/workspace/Mastermind/config/skill-priority.json"
    try:
        with open(priority_file) as f:
            data = json.load(f)
        high = data.get("high", {}).get("skills", [])
        medium = data.get("medium", {}).get("skills", [])
        low = data.get("low", {}).get("skills", [])
        return {
            "total": len(high) + len(medium) + len(low),
            "high": len(high),
            "medium": len(medium),
            "low": len(low)
        }
    except Exception:
        return {"total": 0, "high": 0, "medium": 0, "low": 0}

def get_notes_stats():
    """Contar notas."""
    notes_dir = "/root/workspace/Mastermind/notes"
    total = len(list(Path(notes_dir).glob("*.md")))
    archive_dir = os.path.join(notes_dir, "archive")
    archived = len(list(Path(archive_dir).glob("*.md"))) if os.path.exists(archive_dir) else 0

    memory_file = "repo raíz/MEMORY.md"
    memory_size = "0 chars"
    if os.path.exists(memory_file):
        size = os.path.getsize(memory_file)
        memory_size = f"{size} chars" if size < 1024 else f"{size/1024:.1f}KB"

    return {"total": total, "archived": archived, "memorySize": memory_size}

def get_crons_stats():
    """Contar crons por estado."""
    # Se consulta el sistema real de crons
    try:
        result = subprocess.run(
            ["systemctl", "list-timers", "--all", "--no-pager", "--no-legend"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            # Contar timers activos (que tengan próxima ejecución)
            active = sum(1 for l in lines if l and 'active' in l.lower())
            return {"active": active, "paused": 0, "once": 0}
    except Exception:
        pass
    
    # Fallback: valores por defecto basados en crons conocidos
    return {"active": 8, "paused": 2, "once": 5}

def get_graph_stats():
    """Leer stats del grafo."""
    graph_file = os.path.join(DATA_DIR, "knowledge-graph.json")
    try:
        with open(graph_file) as f:
            data = json.load(f)
        stats = data.get("stats", {})
        return {
            "nodes": stats.get("total_nodes", 0),
            "edges": stats.get("total_edges", 0),
            "orphans": stats.get("orphans", 0)
        }
    except Exception:
        return {"nodes": 0, "edges": 0, "orphans": 0}

def get_soul_status():
    """Verificar SOUL.md."""
    soul_file = "/root/workspace/Mastermind/mastermind/SOUL.md"
    try:
        size = os.path.getsize(soul_file)
        size_str = f"{size} bytes" if size < 1024 else f"{size/1024:.1f}KB"

        content = Path(soul_file).read_text(encoding="utf-8")
        status = "OK" if len(content) > 500 else "WARNING: posible corrupción"

        backup_file = "repo raíz/SOUL.md"
        backup_time = "unknown"
        if os.path.exists(backup_file):
            mtime = os.path.getmtime(backup_file)
            backup_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")

        return {"size": size_str, "status": status, "backup": backup_time}
    except Exception:
        return {"size": "error", "status": "error", "backup": "unknown"}

def get_lifecycle_data():
    """Leer datos de lifecycle."""
    lifecycle_file = os.path.join(DATA_DIR, "skill-lifecycle-report.json")
    try:
        with open(lifecycle_file) as f:
            data = json.load(f)
        top10 = data.get("top_10", [])[:10]
        changes = data.get("all_changes", [])

        result = []
        for name in top10:
            change = next((c for c in changes if c.get("name") == name), None)
            if change:
                result.append({
                    "name": name,
                    "priority": change.get("new_priority", "unknown"),
                    "score": change.get("usage_score", 0)
                })
        return result
    except Exception:
        return []

def update_dashboard():
    """Actualizar datos en el HTML."""
    data = {
        "chromadb": get_chromadb_status(),
        "skills": get_skills_stats(),
        "notes": get_notes_stats(),
        "crons": get_crons_stats(),
        "graph": get_graph_stats(),
        "soul": get_soul_status(),
        "lifecycle": get_lifecycle_data()
    }

    # Leer HTML
    html = Path(DASHBOARD_HTML).read_text(encoding="utf-8")

    # Reemplazar DATA
    new_data = f"const DATA = {json.dumps(data, indent=2, ensure_ascii=False)};"
    html = re.sub(r'const DATA = \{.*?\};', new_data, html, flags=re.DOTALL)

    # Guardar
    Path(DASHBOARD_HTML).write_text(html, encoding="utf-8")

    print("📊 Dashboard actualizado:")
    print(f"  ChromaDB: {data['chromadb']['status']}")
    print(f"  Skills: {data['skills']['total']} (H:{data['skills']['high']} M:{data['skills']['medium']} L:{data['skills']['low']})")
    print(f"  Notas: {data['notes']['total']} (archivadas: {data['notes']['archived']})")
    print(f"  Crons: {data['crons']['active']} activos")
    print(f"  Grafo: {data['graph']['nodes']} nodos, {data['graph']['edges']} conexiones, {data['graph']['orphans']} huérfanas")
    print(f"  SOUL: {data['soul']['size']} ({data['soul']['status']})")
    print(f"  Lifecycle top10: {len(data['lifecycle'])} skills")

if __name__ == "__main__":
    update_dashboard()
