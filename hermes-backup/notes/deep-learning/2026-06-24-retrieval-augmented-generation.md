# Retrieval-Augmented Generation (RAG) — De Básico a State-of-the-Art

## Resumen Ejecutivo

**RAG** (Retrieval-Augmented Generation, Liu et al. 2020) es la técnica que permite a un LLM enriquecer sus respuestas con conocimiento externo recuperado dinámicamente. Es la técnica más usada en producción para LLMs empresariales.

Lo que empezó como un paper simple se ha convertido en un ecosistema enorme:
- **LightRAG** (HKUDS, 37K+ stars) — GraphRAG ligero y rápido
- **Microsoft GraphRAG** — GraphRAG para análisis de corpus narrativo
- **RAGFlow** (83K+ stars) — Motor de RAG con parsing profundo de documentos
- **RAGAS** — Framework de evaluación de calidad RAG

---

## 1. El Paper Original: Retrieval-Augmented Generation for NLP (2020)

**Autores:** Iz Beltagy, Matthew E. Peters, Arman Cohan (AI2)
**arXiv:** 2005.11401

### La idea

En lugar de entrenar un modelo con más parámetros para "memorizar" más conocimiento, **separar memoria y cómputo**:

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Query   │────▶│ Retrieve │────▶│  Generate│
│          │     │  Index   │     │   w/ LLM │
└──────────┘     └──────────┘     └──────────┘
```

**Pre-training:**
```
P(z | x) = ∫ P(z | x, s) P(s | x) ds
```
Donde `s` es un contexto de documentos recuperados de una base de conocimiento externa.

**Key insight:** El modelo solo necesita aprender a *combinar* su conocimiento paramétrico con el conocimiento no-paramétrico recuperado. No necesita memorizar todo.

---

## 2. Arquitectura RAG Clásica (Three-Stage Pipeline)

### Stage 1: Indexing (Offline)

```python
# Pipeline clásico: Chunk → Embed → Store
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Cargar y chunkear documentos
def chunk_text(text, chunk_size=512, overlap=64):
    """Chunkeo con solapamiento para mantener contexto."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap  # solapamiento
    return chunks

# 2. Embedding
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Almacenamiento vectorial
client = chromadb.PersistentClient(path="/tmp/rag-index")
collection = client.get_or_create_collection("documents")

for i, chunk in enumerate(chunks):
    collection.add(
        ids=[f"doc_{i}"],
        embeddings=[embedder.encode(chunk).tolist()],
        documents=[chunk],
        metadatas=[{"source": "doc.pdf", "chunk": i}]
    )
```

### Stage 2: Retrieval (Online)

```python
# Búsqueda vectorial simple
def retrieve(query, n_results=5):
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results
```

### Stage 3: Generation

```python
# Prompt enriquecido con contexto recuperado
def generate(query, context_docs):
    prompt = f"""
    Responde a la pregunta usando SOLO la información de los documentos
    proporcionados. Si no puedes responder, di que no lo sabes.

    Contexto:
    {'---'.join(context_docs)}

    Pregunta: {query}

    Respuesta:
    """
    return llm.generate(prompt)
```

---

## 3. Evolución: Las 5 Generaciones de RAG

### Generación 1: Naive RAG
El pipeline básico de arriba. Problemas:
- Chunkeo fijo rompe contexto semántico
- Solo búsqueda por similitud vectorial
- Sin reordenamiento

### Generación 2: Hybrid Search + Reranking
```python
# Combinar búsqueda vectorial + BM25 (lexical)
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, chunks, embeddings):
        self.chunks = chunks
        self.embeddings = np.array(embeddings)
        # BM25 para búsqueda lexical
        tokenized = [self._tokenize(c) for c in chunks]
        self.bm25 = BM25Okapi(tokenized)
    
    def retrieve(self, query, top_k=5, alpha=0.5):
        # Vectorial (normalizada a 0-1)
        q_emb = self.embedder.encode(query)
        vec_scores = self._cosine_sim(q_emb)
        vec_norm = (vec_scores - vec_scores.min()) / (vec_scores.max() - vec_scores.min() + 1e-8)
        
        # BM25 (normalizada)
        q_tokens = self._tokenize(query)
        bm25_scores = np.array(self.bm25.get_scores(q_tokens))
        bm25_norm = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-8)
        
        # Combinación ponderada
        combined = alpha * vec_norm + (1 - alpha) * bm25_norm
        return np.argsort(combined)[::-1][:top_k]
```

### Generación 3: Self-Querying + Metadata Filtering
```python
# LangChain Self-Query: el LLM extrae filtros de la consulta
from langchain.retrievers import SelfQueryRetriever
from langchain_chroma import Chroma

self_query_retriever = SelfQueryRetriever.from_llm(
    vectorstore=chroma_store,
    llm=llm,
    document_contents="Notas de reuniones y documentos corporativos",
    metadata_field_info=[
        {"field": "fecha", "type": "datetime", "description": "Fecha del documento"},
        {"field": "autor", "type": "string", "description": "Autor del documento"},
        {"field": "departamento", "type": "string", "description": "Departamento"},
        {"field": "tipo", "type": "string", "description": "Tipo de documento"},
    ],
    structured_query_translator=ChromaTranslator(),  # para ChromaDB
)

# Consulta: "¿Qué dijo María sobre el presupuesto en 2025?"
# → El retriever genera: vector_search + filter={"autor": "María", "fecha": ">=2025-01-01"}
results = self_query_retriever.invoke("presupuesto 2025")
```

### Generación 4: Reranking (Cross-Encoder)
```python
# Cross-encoder para reordenar los top-k recuperados
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, candidates, top_k=3):
    pairs = [[query, doc] for doc in candidates]
    scores = cross_encoder.predict(pairs)
    # Ordenar por score descendente
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]

# Pipeline completo: Hybrid → Rerank → Generate
def rag_pipeline(query, n_hybrid=20, n_rerank=3):
    # 1. Hybrid retrieval (vectorial + BM25)
    candidates = hybrid_retrieve(query, top_k=n_hybrid)
    # 2. Reranking con cross-encoder
    ranked = rerank(query, candidates, top_k=n_rerank)
    # 3. Generate
    return generate(query, ranked)
```

### Generación 5: GraphRAG (LightRAG / Microsoft GraphRAG)
```
┌─────────────────────────────────────────────────┐
│              GraphRAG Architecture               │
│                                                  │
│  Documents → Chunking → Entity/Relation Extraction │
│                      ↓                           │
│            Knowledge Graph (entities + edges)     │
│                      ↓                           │
│  ┌─────────────────┐  ┌──────────────────┐       │
│  │  Vector Index   │  │  Community Graph │       │
│  │  (local search) │  │  (global search) │       │
│  └────────┬────────┘  └────────┬─────────┘       │
│           │                    │                   │
│           └───────┬────────────┘                   │
│                   ↓                                │
│           Combined Context → LLM → Answer          │
└─────────────────────────────────────────────────┘
```

**LightRAG** (Guo et al., 2024 — arXiv:2410.05779, EMNLP 2025):
- Dual-level retrieval: **low-level** (entities) + **high-level** (communities)
- Incremental updates sin re-indexar todo
- 4 chunking strategies: Fix, Recursive, Vector, Paragraph
- Reranker integrado por defecto

**Microsoft GraphRAG** (Edge et al., 2024 — arXiv:2404.16130):
- Community detection en el grafo de conocimiento
- Summarización jerárquica por comunidades
- Ideal para **query-focused summarization** sobre corpus privado

---

## 4. Implementación Práctica: RAG con ChromaDB (Stack Mastermind)

```python
#!/usr/bin/env python3
"""
RAG completo con ChromaDB — compatible con el stack actual de Mastermind.
Usa qwen3-embedding vía API NaN (igual que consultar-skills.py).
"""

import os
import json
import requests
import numpy as np
from pathlib import Path
from datetime import datetime

# ─── Config ──────────────────────────────────────────────
NAN_API_KEY = os.environ.get("NAN_API_KEY", "")
NAN_EMBEDDING_MODEL = "qwen3-embedding"
EMBEDDING_URL = "https://api.nan.builders/v1/embeddings"

# ─── Embedding via NaN API ───────────────────────────────
def get_embedding(text: str) -> list[float]:
    """Generar embedding usando qwen3-embedding de NaN."""
    resp = requests.post(
        EMBEDDING_URL,
        headers={"Authorization": f"Bearer {NAN_API_KEY}", "Content-Type": "application/json"},
        json={"model": NAN_EMBEDDING_MODEL, "input": text},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["data"][0]["embedding"]

def batch_embed(texts: list[str]) -> list[list[float]]:
    """Embedding en batch (más eficiente)."""
    resp = requests.post(
        EMBEDDING_URL,
        headers={"Authorization": f"Bearer {NAN_API_KEY}", "Content-Type": "application/json"},
        json={"model": NAN_EMBEDDING_MODEL, "input": texts},
        timeout=60
    )
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]

# ─── ChromaDB Integration ────────────────────────────────
import chromadb

class ChromaRAG:
    def __init__(self, collection_name: str = "mastermind-rag", 
                 persist_dir: str = "/tmp/mastermind-rag"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            collection_name,
            metadata={"hnsw:space": "cosine"}  # cosine distance (igual que ChromaDB actual)
        )
    
    def index_documents(self, documents: list[dict], batch_size: int = 10):
        """Indexar documentos con embedding batch."""
        texts = [doc["content"] for doc in documents]
        
        # Embedding en batch
        embeddings = batch_embed(texts)
        
        ids = [doc.get("id", f"doc_{i}") for i, doc in enumerate(documents)]
        metadatas = [{k: v for k, v in doc.items() if k != "content"} for doc in documents]
        
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        return len(ids)
    
    def search(self, query: str, n_results: int = 5, 
               where: dict = None) -> list[dict]:
        """Búsqueda con filtro opcional."""
        query_emb = get_embedding(query)
        
        kwargs = {
            "query_embeddings": [query_emb],
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"]
        }
        if where:
            kwargs["where"] = where
        
        results = self.collection.query(**kwargs)
        
        return [
            {
                "document": docs,
                "metadata": metas,
                "distance": dist,
                "similarity": 1.0 - dist  # cosine distance → similarity
            }
            for docs, metas, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]

# ─── Advanced: Self-Querying ─────────────────────────────
def self_query_retrieve(rag: ChromaRAG, query: str, llm_api_url: str = "https://api.nan.builders/v1/chat/completions"):
    """
    El LLM extrae filtros de metadatos de la consulta natural.
    """
    filter_prompt = f"""
    Analiza esta consulta y extrae filtros de búsqueda como JSON.
    
    Campos disponibles:
    - tipo: "nota" | "skill" | "memoria" | "repo"
    - fecha: YYYY-MM-DD
    - tags: lista de tags
    
    Consulta: "{query}"
    
    Responde SOLO con JSON: {{"tipo": "...", "fecha": "...", "tags": [...]}}
    Si no hay filtro para un campo, usa null.
    """
    
    # Llamar a LLM para extraer filtros
    resp = requests.post(
        llm_api_url,
        headers={"Authorization": f"Bearer {NAN_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "qwen3.6",
            "messages": [{"role": "user", "content": filter_prompt}],
            "temperature": 0
        },
        timeout=30
    )
    
    try:
        filter_text = resp.json()["choices"][0]["message"]["content"]
        # Parsear JSON del LLM
        filters = json.loads(filter_text)
    except:
        filters = {}
    
    # Construir where clause para ChromaDB
    where = {}
    if filters.get("tipo"):
        where["$eq"] = filters["tipo"]
    if filters.get("tags"):
        where["tags"] = {"$all": filters["tags"]}
    
    return rag.search(query, n_results=5, where=where if where else None)

# ─── Advanced: Reranking ─────────────────────────────────
def cross_encoder_rerank(query: str, candidates: list[str], 
                          reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2") -> list[tuple[str, float]]:
    """
    Reranking con cross-encoder.
    En producción: usar un endpoint de reranking (ej. Cohere Rerank, jina-reranker).
    """
    # Opción práctica: usar Cohere Rerank API (gratuito hasta 1K req/día)
    import os
    cohere_key = os.environ.get("COHERE_API_KEY", "")
    
    if cohere_key:
        resp = requests.post(
            "https://api.cohere.com/v1/rerank",
            headers={"Authorization": f"Bearer {cohere_key}", "Content-Type": "application/json"},
            json={
                "model": "rerank-v3.5",
                "query": query,
                "documents": candidates,
                "top_n": 3
            }
        )
        results = resp.json()["results"]
        return [(candidates[r["index"]], r["relevance_score"]) for r in results]
    
    # Fallback: cosine similarity (menos preciso pero sin dependencia externa)
    query_emb = np.array(get_embedding(query))
    scored = []
    for doc in candidates:
        doc_emb = np.array(get_embedding(doc))
        sim = float(np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb) + 1e-8))
        scored.append((doc, sim))
    return sorted(scored, key=lambda x: x[1], reverse=True)[:3]

# ─── Usage Example ───────────────────────────────────────
if __name__ == "__main__":
    rag = ChromaRAG(collection_name="mastermind-rag")
    
    # Indexar notas de deep learning
    notes_dir = Path("/hermes-home/notes/deep-learning")
    documents = []
    for note_file in notes_dir.glob("*.md"):
        content = note_file.read_text()
        documents.append({
            "id": note_file.stem,
            "content": content,
            "tipo": "nota",
            "fecha": note_file.stem.split("-")[0],
            "tags": ["deep-learning"]
        })
    
    n_indexed = rag.index_documents(documents)
    print(f"📚 Indexados {n_indexed} documentos")
    
    # Buscar
    results = rag.search("¿cómo funcionan los transformers de visión?", n_results=3)
    for i, r in enumerate(results):
        print(f"\n📄 Resultado {i+1} (similarity: {r['similarity']:.3f})")
        print(r["document"][:200] + "...")
```

---

## 5. Evaluación: RAGAS Framework

**RAGAS** (RAG Assessment) es el estándar para evaluar calidad de RAG:

```python
# pip install ragas
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

# Evaluación requiere:
# - questions: las queries del usuario
# - answers: las respuestas del LLM
# - contexts: los contextos recuperados
# - ground_truths: respuestas de referencia

evaluation_result = evaluate(dataset, metrics=[
    faithfulness,       # ¿La respuesta se basa en el contexto?
    answer_relevancy,   # ¿La respuesta responde la pregunta?
    context_precision,  # ¿Los contextos relevantes están arriba?
    context_recall,     # ¿Se recuperó todo lo necesario?
])

# Interpretación:
# faithfulness > 0.8: buena grounding
# answer_relevancy > 0.7: respuestas útiles
# context_precision > 0.7: buen retrieval
# context_recall > 0.6: buena cobertura
```

**Las 4 métricas explicadas:**

| Métrica | Pregunta | Valor bueno |
|---------|----------|-------------|
| Faithfulness | ¿La respuesta usa solo el contexto? | > 0.8 |
| Answer Relevancy | ¿La respuesta responde la pregunta? | > 0.7 |
| Context Precision | ¿Los docs relevantes están primero? | > 0.7 |
| Context Recall | ¿Se recuperó todo lo necesario? | > 0.6 |

---

## 6. Patrones Avanzados (2025-2026)

### 6.1 Multi-Document Chunking Strategies

```python
# LightRAG-style chunking strategies
def smart_chunking(text, strategy="recursive", chunk_size=512):
    """
    4 estrategias de chunking:
    
    1. Fix: tamaño fijo con overlap
    2. Recursive: por párrafos/oraciones, respeta estructura
    3. Vector: chunkea hasta que el embedding supere un umbral de distancia
    4. Paragraph: por bloques de texto (resalta estructura semántica)
    """
    if strategy == "recursive":
        # Respeta límites de párrafos y oraciones
        paragraphs = text.split('\n\n')
        chunks = []
        current = ""
        for p in paragraphs:
            if len(current) + len(p) > chunk_size:
                if current:
                    chunks.append(current.strip())
                current = p
            else:
                current += "\n\n" + p if current else p
        if current:
            chunks.append(current.strip())
        return chunks
    
    elif strategy == "vector":
        # Chunkea hasta que la similitud con el siguiente baje de umbral
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        chunks = []
        current = sentences[0] if sentences else ""
        
        for i in range(1, len(sentences)):
            current_emb = get_embedding(current)
            next_emb = get_embedding(sentences[i])
            sim = np.dot(current_emb, next_emb) / (
                np.linalg.norm(current_emb) * np.linalg.norm(next_emb) + 1e-8
            )
            if sim < 0.7:  # umbral de similitud
                chunks.append(current)
                current = sentences[i]
            else:
                current += ". " + sentences[i]
        if current:
            chunks.append(current)
        return chunks
    
    else:  # "fix" o default
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
```

### 6.2 Agentic RAG (ReAct + Retrieval)

```
┌─────────────────────────────────────────────────────┐
│              Agentic RAG Loop                        │
│                                                      │
│  Query → LLM (plan)                                 │
│    ├── ¿Necesito buscar? → Retrieve → Add context   │
│    ├── ¿Necesito más info? → Retrieve again         │
│    ├── ¿Tengo suficiente? → Generate answer         │
│    └── ¿La respuesta es correcta? → Self-correct    │
│                                                      │
│  Máximo N iteraciones de retrieve → generate         │
└─────────────────────────────────────────────────────┘
```

```python
def agentic_rag(query, max_iterations=3):
    """
    Patrón ReAct: el LLM decide cuándo buscar y cuándo responder.
    """
    context = []
    for i in range(max_iterations):
        # LLM decide la acción
        action_prompt = f"""
        Dada la consulta "{query}" y el contexto acumulado,
        ¿qué haces?
        
        Opciones:
        1. [SEARCH] <query de búsqueda>
        2. [ANSWER] <respuesta final>
        
        Solo responde con la acción.
        """
        decision = llm.generate(action_prompt)
        
        if decision.startswith("[SEARCH]"):
            search_query = decision.replace("[SEARCH]", "").strip()
            results = rag.search(search_query, n_results=3)
            context.extend([r["document"] for r in results])
        elif decision.startswith("[ANSWER]"):
            return decision.replace("[ANSWER]", "").strip()
    
    # Fallback: generar con todo el contexto acumulado
    return generate(query, context)
```

### 6.3 Hierarchical / Summarization RAG

```python
# Para corpus muy grande: sumarizar chunks antes de indexar
def hierarchical_rag(documents, llm):
    """
    Pipeline en dos niveles:
    1. Nivel bajo: chunks individuales
    2. Nivel alto: resumen de grupo de chunks
    """
    # Agrupar chunks por documento
    groups = group_by_document(documents)
    
    # Generar resumen para cada grupo
    summaries = []
    for group in groups:
        combined = "\n\n".join(group)
        summary = llm.generate(f"Resume este texto en 3 frases:\n{combined}")
        summaries.append({
            "summary": summary,
            "source_docs": group,
            "type": "summary"
        })
    
    # Indexar AMBOS niveles
    all_index = summaries + documents
    # ... indexar todo en ChromaDB
```

---

## 7. Comparativa de Frameworks

| Framework | Stars | Enfoque | Storage | Ideal para |
|-----------|-------|---------|---------|------------|
| **RAGFlow** | 83K+ | Parsing profundo (PDF, tablas) | Elasticsearch + vector | Documentos complejos |
| **LightRAG** | 37K+ | GraphRAG ligero, dual-level | ChromaDB/Neo4j/PG | Conocimiento estructurado |
| **LangChain** | 120K+ | Orquestación completa | Cualquier vectorstore | Flexibilidad total |
| **LlamaIndex** | 40K+ | Data frameworks, indexación | Cualquier vectorstore | Integración de datos |
| **Microsoft GraphRAG** | 18K+ | Community detection | NetworkX + GPT-4 | Análisis narrativo |

---

## 8. Relevancia para Mastermind

### Conexiones directas con el stack actual:

1. **ChromaDB ya está en producción** — El sistema de skills vectoriales usa ChromaDB + qwen3-embedding. Un RAG sobre las notas de Mastermind sería trivial de implementar con la infraestructura existente.

2. **Skills como knowledge base** — Los 200+ skills podrían indexarse como un corpus RAG, permitiendo al agente "recordar" skills que ChromaDB no encontró por similitud semántica.

3. **Notas como contexto de proyecto** — Las 12 notas de deep-learning + notas generales formarían un corpus de ~300K tokens, perfecto para RAG de alta calidad.

4. **GraphRAG para dependencies** — LightRAG podría mapear dependencias entre skills, notas y repositorios, permitiendo consultas como "¿qué skills dependen de ChromaDB?"

### Posible skill a crear: `rag-knowledge-base`
Un sistema RAG ligero sobre las notas y skills de Mastermind, usando la infraestructura ChromaDB existente.

---

## 9. Referencias Clave

### Papers
- **[RAG Original]** Liu et al. (2020) — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — arXiv:2005.11401
- **[GraphRAG]** Edge et al. (2024) — *From Local to Global: A Graph RAG Approach to Query-Focused Summarization* — arXiv:2404.16130
- **[LightRAG]** Guo et al. (2024) — *LightRAG: Simple and Fast Retrieval-Augmented Generation* — arXiv:2410.05779 (EMNLP 2025)
- **[RAGAS]** Ronankhi et al. (2023) — *RAGAS: Automated Evaluation of Retrieval Augmented Generation* — arXiv:2309.15217

### Repositorios
- [infiniflow/ragflow](https://github.com/infiniflow/ragflow) — 83K+ stars
- [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) — 37K+ stars
- [microsoft/graphrag](https://github.com/microsoft/graphrag) — 18K+ stars
- [NirDiamante/RAG_Techniques](https://github.com/NirDiamante/RAG_Techniques) — Tutorial de todas las técnicas RAG
- [explodinggradients/ragas](https://github.com/explodinggradients/ragas) — Framework de evaluación

### Herramientas de Embedding
- **qwen3-embedding** (NaN API) — ya en uso en Mastermind
- **all-MiniLM-L6-v2** (SentenceTransformers) — rápido, ligero, 384d
- **text-embedding-3-small** (OpenAI) — estado del arte general
- **jina-embeddings-v3** — multilingüe, buen rendimiento

---

## 10. Próximos Pasos

1. **Implementar RAG sobre notas** — Usar ChromaDB existente + qwen3-embedding para indexar `/hermes-home/notes/`
2. **Evaluar con RAGAS** — Medir faithfulness y context_precision de las respuestas
3. **Explorar LightRAG** — Probar graph-based retrieval para dependencias entre skills
4. **Crear skill `rag-knowledge-base`** — Sistematizar el patrón RAG para uso recurrente

---

## Tema Sugerido para la Siguiente Sesión

**MLOps & Model Serving** — Después de 12 sesiones cubriendo arquitecturas de modelos (SSM, Diffusion, Transformers, GNN, etc.), el siguiente paso lógico es **cómo desplegar y servir estos modelos en producción**: vLLM, TGI, TensorRT-LLM, ONNX Runtime, Triton Inference Server. Esto cierra el ciclo: de la arquitectura del modelo a su despliegue real en la MicroVM de NaN.

Alternativa más específica: **State Space Models más allá de Mamba** — Mamba-2, RWKV v6, and Hyena, que son las siguientes generaciones de SSMs con rendimiento competitivo a Transformers pero con inferencia O(1).
