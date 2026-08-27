# RAG Techniques Overview — Referencia Rápida

## Las 5 Generaciones de RAG

### Gen 1: Naive RAG
Chunk fijo → Embedding → Búsqueda vectorial → LLM
- Chunkeo con overlap fijo
- Solo similitud vectorial (cosine)
- Sin reordenamiento

### Gen 2: Hybrid Search + Reranking
Combinar vectorial + BM25 lexical + cross-encoder reranker
- Alpha ponderable (0.5 default)
- BM25 para términos exactos
- Cross-encoder para precisión

### Gen 3: Self-Querying
El LLM extrae filtros de metadatos de la consulta natural
- Metadata field definitions
- Filtros estructurales (fecha, autor, tipo)
- ChromaDB where clauses

### Gen 4: Reranking
Cross-encoder reordena los top-k recuperados
- Cohere Rerank v3.5 (recomendado)
- jina-reranker-v2 (alternativa)
- Fallback: cosine similarity

### Gen 5: GraphRAG
Conocimiento estructurado en grafos
- LightRAG: dual-level (entities + communities)
- Microsoft GraphRAG: community detection jerárquico
- Incremental updates sin re-indexar

## Frameworks Comparados

| Framework | Stars | Enfoque | Storage |
|-----------|-------|---------|---------|
| RAGFlow | 83K+ | Parsing profundo | Elasticsearch + vector |
| LightRAG | 37K+ | GraphRAG ligero | ChromaDB/Neo4j/PG |
| LangChain | 120K+ | Orquestación total | Cualquier vectorstore |
| LlamaIndex | 40K+ | Data frameworks | Cualquier vectorstore |
| Microsoft GraphRAG | 18K+ | Community detection | NetworkX + GPT-4 |

## Evaluación RAGAS

Las 4 métricas estándar:
- **Faithfulness** (>0.8): ¿La respuesta usa solo el contexto?
- **Answer Relevancy** (>0.7): ¿Responde la pregunta?
- **Context Precision** (>0.7): ¿Docs relevantes arriba?
- **Context Recall** (>0.6): ¿Todo lo necesario recuperado?

## Patrones Avanzados

- **Multi-chunking**: Fix, Recursive, Vector, Paragraph
- **Agentic RAG**: ReAct loop con retrieve → generate iterativo
- **Hierarchical RAG**: Resumen de grupo + chunks individuales
- **Citation**: Rastreo de fuentes en respuestas

## Referencias

- RAG Original: Liu et al. (2020) — arXiv:2005.11401
- LightRAG: Guo et al. (2024) — arXiv:2410.05779
- GraphRAG: Edge et al. (2024) — arXiv:2404.16130
- RAGAS: Ronankhi et al. (2023) — arXiv:2309.15217
- VideoRAG (2025): RAG sobre corpus de video
