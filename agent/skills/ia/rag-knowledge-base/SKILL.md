---
name: rag-knowledge-base
description: Construir y gestionar un sistema RAG (Retrieval-Augmented Generation) sobre el corpus de notas, skills y repos de Mastermind — usando ChromaDB + qwen3-embedding de NaN API.
---

# RAG Knowledge Base — Mastermind

## Contexto

Mastermind ya tiene infraestructura RAG lista:
- **ChromaDB** en `/hermes-home/chromadb-venv/` con colección `mastermind-skills`
- **Embedding**: `qwen3-embedding` vía `https://api.nan.builders/v1/embeddings`
- **Datos**: `/hermes-home/notes/`, `/hermes-home/skills/`, `/root/workspace/Mastermind/`

Esta skill sistematiza el patrón RAG para uso recurrente.

## Pasos

### 1. Indexar corpus como RAG

```bash
# Asegurar ChromaDB corriendo
bash /hermes-home/scripts/start-chromadb.sh
sleep 3

# Crear script de indexación
cat > /tmp/rag-indexer.py << 'PYTHON'
#!/usr/bin/env python3
"""Indexar corpus de Mastermind en ChromaDB para RAG."""
import os, sys, json, requests, glob
from pathlib import Path
import chromadb

NAN_API_KEY = os.environ.get("NAN_API_KEY", "")
if not NAN_API_KEY:
    print("ERROR: NAN_API_KEY no configurada"); sys.exit(1)

def batch_embed(texts):
    resp = requests.post(
        "https://api.nan.builders/v1/embeddings",
        headers={"Authorization": f"Bearer {NAN_API_KEY}", "Content-Type": "application/json"},
        json={"model": "qwen3-embedding", "input": texts},
        timeout=60
    )
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]

client = chromadb.PersistentClient(path="/tmp/mastermind-rag")
collection = client.get_or_create_collection("mastermind-rag", metadata={"hnsw:space": "cosine"})

# Indexar notas
documents = []
for note_file in Path("/hermes-home/notes").rglob("*.md"):
    content = note_file.read_text()[:10000]  # limitar tamaño
    documents.append({
        "id": str(note_file),
        "content": content,
        "tipo": "nota",
        "path": str(note_file),
    })

# Indexar skills SKILL.md
for skill_file in Path("/hermes-home/skills").rglob("SKILL.md"):
    content = skill_file.read_text()[:10000]
    documents.append({
        "id": str(skill_file),
        "content": content,
        "tipo": "skill",
        "path": str(skill_file),
    })

# Indexar notas de deep-learning
for dl_file in Path("/hermes-home/notes/deep-learning").glob("*.md"):
    content = dl_file.read_text()[:10000]
    documents.append({
        "id": str(dl_file),
        "content": content,
        "tipo": "deep-learning",
        "path": str(dl_file),
    })

print(f"📚 Indexando {len(documents)} documentos...")

# Batch embed
texts = [d["content"] for d in documents]
embeddings = batch_embed(texts)

# Upsert en ChromaDB
for i, doc in enumerate(documents):
    collection.upsert(
        ids=[doc["id"]],
        embeddings=[embeddings[i]],
        documents=[doc["content"]],
        metadatas=[{"tipo": doc["tipo"], "path": doc["path"]}]
    )

print(f"✅ Indexados {len(documents)} documentos en ChromaDB")
PYTHON

python3 /tmp/rag-indexer.py
```

### 2. Consultar corpus RAG

```python
# Query RAG sobre notas y skills
import chromadb

client = chromadb.PersistentClient(path="/tmp/mastermind-rag")
collection = client.get_collection("mastermind-rag")

# Obtener embedding de la consulta
import requests
import os
resp = requests.post(
    "https://api.nan.builders/v1/embeddings",
    headers={"Authorization": f"Bearer {os.environ['NAN_API_KEY']}", "Content-Type": "application/json"},
    json={"model": "qwen3-embedding", "input": "cómo configurar ChromaDB"}
)
query_emb = resp.json()["data"][0]["embedding"]

results = collection.query(
    query_embeddings=[query_emb],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)
```

### 3. RAG para generar respuestas

```python
def rag_answer(query, n_context=3):
    """Obtener contexto de ChromaDB + generar respuesta con LLM."""
    # 1. Buscar en corpus
    results = collection.query(
        query_embeddings=[get_embedding(query)],
        n_results=n_context,
        include=["documents", "metadatas"]
    )
    
    # 2. Construir prompt con contexto
    context = "\n\n---\n\n".join(results["documents"][0])
    prompt = f"""
    Usa la siguiente información de contexto para responder:
    
    {context}
    
    Pregunta: {query}
    
    Si la información de contexto no es suficiente, dilo claramente.
    """
    
    # 3. Generar respuesta
    return llm.generate(prompt)
```

## Pitfalls

- **qwen3-embedding** puede dar scores de similitud bajos en ChromaDB (threshold > 0.25 es normal, como en consultar-skills.py)
- **Limitar documento a 10K chars** — qwen3-embedding puede tener límites de longitud de input
- **ChromaDB necesita persistencia** — usar `PersistentClient` para que los datos sobrevivan
- **Batch embedding** es mucho más eficiente que individual (1 req por batch vs N requests)

## Referencias

- **`references/rag-techniques-overview.md`** — Resumen de las 5 generaciones de RAG, frameworks comparados, métricas RAGAS y patrones avanzados
- RAG Original: Liu et al. (2020) — arXiv:2005.11401
- LightRAG: Guo et al. — arXiv:2410.05779 (EMNLP 2025, 37K+ stars)
- Microsoft GraphRAG: Edge et al. — arXiv:2404.16130
- RAGAS: arXiv:2309.15217
- RAGFlow: 83K+ stars — parsing profundo de documentos
