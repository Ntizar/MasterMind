---
name: memory-context-engine
version: "1.0.0"
description: "Motor de memoria y contexto para agentes IA — rápido, escalable, self-hosted. Inspirado en supermemoryai/supermemory (⭐28K)."
tags: [memory, context, rag, vector, ai, agent, embedding]
---

# Motor de Memoria y Contexto para Agentes IA

## Resumen

[supermemory](https://github.com/supermemoryai/supermemory) (⭐28K) es un motor de memoria y contexto para agentes IA. Extremadamente rápido, escalable, y self-hostable. Permite que agentes recuerden información entre sesiones.

## Cuándo usar

- Agentes IA con memoria persistente entre sesiones
- RAG (Retrieval-Augmented Generation) con grandes volúmenes de datos
- Sistema de memoria para múltiples agentes
- Context engine para LLMs con contexto limitado

## Arquitectura

```
Documentos/Conversaciones
  ↓ Chunking
  ↓ Embedding (modelo local o API)
  ↓ Vector store (ChromaDB/Qdrant/Postgres+pgvector)
  ↓
Query → Embedding → Búsqueda semántica → Top-K chunks → Contexto para LLM
```

## Patrón de uso

```python
from supermemory import SuperMemory

# Inicializar motor de memoria
memory = SuperMemory(
    vector_store="chromadb",  # o qdrant, pgvector
    embedding_model="qwen3-embedding",
    api_key="your-api-key"
)

# Almacenar memoria
memory.add(
    content="David prefiere dashboards con mapa a tabla",
    metadata={"user": "david", "type": "preference"},
    tags=["ui", "dashboard", "maps"]
)

# Recuperar memoria relevante
results = memory.search(
    query="¿qué prefiere David para visualización?",
    top_k=5,
    filter={"user": "david"}
)

for result in results:
    print(f"Score: {result.score} | {result.content}")
```

```javascript
// Integración con agente
const memory = new SuperMemory({
  vectorStore: 'chromadb',
  embeddingModel: 'qwen3-embedding'
});

// Antes de cada llamada al LLM, recuperar contexto relevante
async function agentWithMemory(userMessage) {
  const context = await memory.search(userMessage, { topK: 5 });
  
  const prompt = `
Contexto relevante de memoria:
${context.map(c => c.content).join('\n')}

Usuario: ${userMessage}
  `;
  
  const response = await llm.chat(prompt);
  
  // Guardar la interacción en memoria
  await memory.add({
    content: `Usuario: ${userMessage}\nAsistente: ${response}`,
    metadata: { type: 'conversation', timestamp: Date.now() }
  });
  
  return response;
}
```

## Pitfalls

- **Chunking:** Tamaño de chunk óptimo: 500-1000 tokens. Solapamiento de 50-100 tokens.
- **Embedding model:** Modelos locales (sentence-transformers) son gratis pero menos precisos. APIs (OpenAI, NaN) son mejores pero cuestan.
- **Vector store:** ChromaDB para desarrollo, Qdrant para producción, pgvector si ya tienes Postgres.
- **Re-indexing:** Al cambiar el modelo de embedding, hay que re-indexar todo.
- **Metadata filtering:** Usar metadata para filtrar por usuario, tipo, fecha. Mejora precisión.

## Referencias

- supermemory: https://github.com/supermemoryai/supermemory
- ChromaDB: https://www.trychroma.com/
- Qdrant: https://qdrant.tech/

---

**Hecho con ❤️ por David Antizar**
