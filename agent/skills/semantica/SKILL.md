---
name: semantica
description: "Semantica: grafo contexto+provenance para agentes IA."
version: "1.0.0"
category: ia
tags: [graph-rag, knowledge-graph, agentes, memoria, provenance, contexto, python]
---

# Semantica — Graph-Native Infrastructure for Context & Accountable AI (semantica-agi/semantica, 11.5k⭐, MIT, Python)

## Qué es

Framework "el Palantir open-source para agentes IA": ingiere datos, extrae entidades, construye un **Context Graph + knowledge graph (RDF y LPG)** y ejecuta analítica de grafo y razonamiento causal, con **provenance de decisiones W3C PROV** integrada. Diseñado para dominios regulados: explicable, auditable, trazable.

Puntos fuertes: entity resolution, extracción de tripletas, gestión de ontología, búsqueda semántica, graph RAG, audit trail. Python 3.8-3.12, deps: networkx, lxml, grpcio, librosa (multimodal), GitPython. Docker-compose para self-host.

```bash
pip install semantica   # verificar nombre exacto en pyproject del repo
docker compose up       # self-host completo
```

## Patrones reutilizables para Mastermind

1. **Memoria de agente como grafo de contexto** — entidades + relaciones + provenance, no solo texto/vector. Aplicable a memorias de skills/estados.
2. **Tripletas → grafo consultable** — pipeline documento → entidades → tripletas → networkx.
3. **Decision provenance (W3C PROV)** — registrar el origen de cada dato/decisión; útil para el auditor en gobierno-ia y para trazabilidad de skills.
4. **Graph RAG sobre repos propios** — combinar ChromaDB (vectorial) con contexto relacional.

## Cuándo usar (y cuándo no)

- USAR como referencia de patrones: memoria como grafo, provenance, graph RAG
- NO instalar por defecto: infraestructura pesada (self-host, gRPC); copiar patrones, ChromaDB ya cubre lo vectorial
- Alternativas ya en catálogo: memory-context-engine, agent-memory, rag-knowledge-base — semantica se diferencia por grafo + provenance + governance

## Pitfalls

- Repo muy reciente y en evolución diaria
- El nombre del paquete pip puede diferir; verificar en pyproject
- Multimodal vía librosa añade deps pesadas; instalar solo el core
