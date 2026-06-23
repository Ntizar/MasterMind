---
name: santander-ai-lab
version: "1.0.0"
description: "Conocimiento de los repositorios open-source de Santander AI Lab — 11 proyectos Apache 2.0 cubriendo grafos ML, RAG, Bayesian networks, LLM clients, causal inference y más. Documenta qué repos existen, su utilidad y relevancia para proyectos de Ineco y otros."
tags: [santander, ai-lab, open-source, graph-ml, rag, bayesian, llm, causal-inference]
---

# Santander AI Lab — Ecosistema de Repositorios

## Resumen

El equipo de IA del Banco Santander (Santander AI Lab) mantiene **11 repositorios open-source** (Apache 2.0) que cubren un ecosistema coherente de herramientas de IA/ML. David los tiene en sus stars de GitHub.

## Repositorios

Ver `references/santander-ai-lab-repos.md` para la tabla completa con stars, lenguajes y relevancia.

### Top 3 para Ineco

1. **gen-fraud-graph** (132⭐) — Generador de grafos sintéticos de fraude. Output CSV para Neo4j/TigerGraph/Neptune. Aplicable a grafos de redes de transporte.
2. **linear-adapter-trainer** (15⭐) — Fine-tune de embeddings para RAG sin re-indexar corpus. Mejora +19% precision@1.
3. **auto-bayesian** (24⭐) — Redes Bayesianas interpretables desde datos tabulares relacionales. Predicción legible directamente.

### Los 11 repos completos

1. `gen-fraud-graph` (132⭐) — Grafos sintéticos de fraude
2. `ralph` (49⭐) — Loop de agentes de coding
3. `ralph-vault-skill` (41⭐) — Knowledge vault
4. `llm_bridge` (41⭐) — Cliente LLM vendor-neutral
5. `auto-bayesian` (24⭐) — Bayesian networks interpretables
6. `sota-stressed-datasets` (22⭐) — Benchmarks estresados
7. `autoguardrails` (65⭐) — Guardrails LLM
8. `mech-gov-framework` (36⭐) — Gobernanza LLM
9. `causal-perception-implementation` (17⭐) — Inferencia causal
10. `mutatis-mutandis` (13⭐) — Fairness algorítmica
11. `linear-adapter-trainer` (15⭐) — Embedding adapters para RAG

## Uso

Cuando necesites:
- Grafos sintéticos para benchmarkear GNNs → `gen-fraud-graph`
- Mejorar búsqueda RAG sin re-indexar → `linear-adapter-trainer`
- Predicción interpretable desde datos tabulares → `auto-bayesian`
- Cliente LLM multi-proveedor → `llm_bridge`
- Inferencia causal → `causal-perception-implementation`

## Notas técnicas
- Todos Apache 2.0
- Todos Python (excepto ralph en PowerShell)
- Actualizados junio 2026
- READMEs completos con CI/CD activo
