#!/usr/bin/env python3
"""
Sistema de flujos de delegación por complejidad para Mastermind.
Clasifica peticiones y define qué subagentes usar.
"""
import json

# Definición de flujos por complejidad
FLOWS = {
    "simple": {
        "level": 1,
        "description": "Tarea directa, sin delegación",
        "threshold": "2-3 tool calls",
        "agents": ["Mastermind directo"],
        "examples": [
            "Leer un archivo",
            "Hacer una pregunta sobre código",
            "Crear un archivo pequeño",
            "Ejecutar un comando simple"
        ],
        "template": "Mastermind ejecuta directamente sin subagentes"
    },
    "medium": {
        "level": 2,
        "description": "Tarea con pasos, posible delegación parcial",
        "threshold": "3-5 tool calls",
        "agents": ["Mastermind", "Explorer (si necesita contexto)", "Reviewer (si es crítico)"],
        "examples": [
            "Auditoría de un archivo",
            "Crear skill con references",
            "Refactorizar código específico",
            "Generar informe de un proyecto"
        ],
        "template": """
1. Mastermind analiza la tarea
2. Si necesita contexto → delega a Explorer (read-only)
3. Mastermind ejecuta los cambios
4. Si es crítico → delega a Reviewer
5. Mastermind presenta resultado
"""
    },
    "complex": {
        "level": 3,
        "description": "Tarea multi-paso con múltiples componentes",
        "threshold": "5+ tool calls",
        "agents": ["Explorer", "Planner", "Implementer", "Reviewer", "Critic (si aplica)"],
        "examples": [
            "Crear un dashboard completo",
            "Migrar un sistema",
            "Auditoría + corrección de un repo",
            "Pipeline de datos completo"
        ],
        "template": """
1. Explorer → Analiza contexto (read-only, max 500 tokens)
2. Planner → Define estrategia, pasos y criterios de éxito
3. Implementer → Ejecuta los cambios
4. Reviewer → Valida contra los criterios
5. Critic → Revisión adversarial (solo si impacto alto)
6. Mastermind → Presenta resultado y decide si merece aprendizaje
"""
    }
}

# Criterios de clasificación
CRITERIA = {
    "file_count": {
        "simple": "1-2 archivos",
        "medium": "3-5 archivos",
        "complex": "6+ archivos"
    },
    "tool_calls": {
        "simple": "2-3",
        "medium": "3-5",
        "complex": "5+"
    },
    "domain_familiarity": {
        "simple": "Dominio conocido (ESIOS, GitHub, infra)",
        "medium": "Dominio parcialmente conocido",
        "complex": "Dominio nuevo o desconocido"
    },
    "risk_level": {
        "simple": "Bajo (archivos no críticos)",
        "medium": "Medio (producción pero reversible)",
        "complex": "Alto (datos, seguridad, múltiples sistemas)"
    }
}

def classify_task(description, context=None):
    """Clasificar una tarea según su complejidad."""
    # Heurísticas simples
    words = description.lower()
    
    # Indicadores de complejidad
    complex_indicators = ["migrar", "auditoría completa", "pipeline", "dashboard completo", 
                         "múltiples", "todo el sistema", "refactorizar todo", "deploy"]
    medium_indicators = ["crear skill", "actualizar", "generar informe", "refactorizar",
                        "verificar", "limpiar", "organizar"]
    
    score = 0
    for indicator in complex_indicators:
        if indicator in words:
            score += 2
    for indicator in medium_indicators:
        if indicator in words:
            score += 1
    
    if score >= 3:
        return "complex"
    elif score >= 1:
        return "medium"
    else:
        return "simple"

def main():
    print("🎯 Sistema de Flujos de Delegación")
    print("=" * 50)
    
    for level, flow in FLOWS.items():
        print(f"\n{'='*20} {level.upper()} (Nivel {flow['level']}) {'='*20}")
        print(f"Descripción: {flow['description']}")
        print(f"Threshold: {flow['threshold']}")
        print(f"Agentes: {', '.join(flow['agents'])}")
        print(f"Ejemplos:")
        for ex in flow['examples']:
            print(f"  • {ex}")
    
    print(f"\n{'='*20} CRITERIOS DE CLASIFICACIÓN {'='*20}")
    for criterion, levels in CRITERIA.items():
        print(f"\n{criterion}:")
        for level, desc in levels.items():
            print(f"  {level}: {desc}")
    
    # Ejemplo de clasificación
    test_tasks = [
        "Leer el archivo README.md",
        "Crear skill de ChromaDB con references",
        "Auditoría completa del sistema + corrección de todos los problemas"
    ]
    
    print(f"\n{'='*20} EJEMPLOS DE CLASIFICACIÓN {'='*20}")
    for task in test_tasks:
        level = classify_task(task)
        print(f"\n  \"{task}\"")
        print(f"  → {level.upper()}")

if __name__ == "__main__":
    main()
