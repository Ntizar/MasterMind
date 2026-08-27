---
name: supermemory
description: Memoria semántica para agentes IA — almacenamiento y recuperación de contexto a largo plazo.
version: "1.0.0"
tags: [memory, AI, agents, semantic, context, retrieval, vector]
---

# SuperMemory — Memoria Semántica para Agentes IA

## Resumen

Sistema de memoria semántica para agentes IA — almacenamiento y recuperación de contexto a largo plazo. 27k⭐.

## Repo de referencia

- **GitHub:** `github.com/supermemoryai/supermemory`
- **Lenguaje:** Python
- **Licencia:** MIT

## Instalación

```bash
pip install supermemory
# o
git clone https://github.com/supermemoryai/supermemory.git
cd supermemory && pip install -e .
```

## Uso Básico

```python
from supermemory import SuperMemory

# Crear memoria
mem = SuperMemory()

# Guardar información
mem.store("El usuario prefiere respuestas en español", category="preference")
mem.store("Proyecto actual: dashboard de transporte", category="project")
mem.store("API key de Esios: esios-xxx", category="secret")

# Buscar información
results = mem.search("preferencias del usuario")
for r in results:
    print(f"{r['category']}: {r['content']}")

# Buscar semánticamente
results = mem.search("qué proyecto estoy trabajando", top_k=3)
```

## Patrones Clave

1. **Almacenamiento:** Guardar texto, notas, preferencias
2. **Recuperación semántica:** Búsqueda por significado, no por palabra clave
3. **Categorización:** Tags y categorías para organización
4. **Expire:** Información con fecha de caducidad
5. **Multi-agent:** Memoria compartida entre agentes

## Integración con Mastermind

- Complementa `memory` tool de Hermes — memoria persistente local
- Útil para `rag-knowledge-base` — memoria de agentes
- Reemplaza `chromadb` para memoria de agentes simples
- Ideal para `shepherd-meta-agents` — memoria compartida

## Pitfalls

- **Privacidad:** No guardar secrets en memoria sin encriptar
- **Escalabilidad:** Limitado para millones de entradas
- **Dependencias:** Requiere vector DB (SQLite + numpy mínimo)
- **Consistencia:** No hay transacciones — puede haber duplicados

## Referencias

- [GitHub: supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)
