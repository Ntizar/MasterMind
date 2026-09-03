---
name: linear-embedding-adapter
version: "1.0.0"
description: "Use al afinar retrieval RAG sin re-embeddar el corpus."
tags: [rag, embeddings, retrieval, triplet-loss, chromadb, fine-tuning, busqueda-semantica]
---

# Linear Embedding Adapter — Mejorar retrieval sin tocar el índice

> Patrón y herramienta: `SantanderAI/linear-adapter-trainer` (29⭐, Apache-2.0,
> Santander AI Lab, Python 3.12+, activo — push 2026-09-01).

## Qué es

Librería para **afinar retrieval sin reentrenar el modelo de embeddings**: aprende una
pequeña transformación lineal aplicada a los embeddings de QUERY en tiempo de búsqueda.
El índice vectorial NO se toca.

| Enfoque | Coste | ¿Re-indexar? | ¿Reversible? |
|---|---|---|---|
| Fine-tune del embedding model | Alto (GPU, datos) | Sí | No |
| **Adaptador lineal de query (esto)** | **Bajo (CPU)** | **No** | **Sí** |
| Re-ranking model | Medio (latencia) | No | Sí |

**Garantía clave:** la selección de modelo siempre incluye la identidad como baseline →
el adaptador entrenado **nunca puede quedar peor que tus embeddings base**.

## Cuándo usarlo en Mastermind

Búsqueda semántica de skills (ChromaDB + qwen3-embedding, dim 4096, NaN API):
si las queries reales no recuperan el skill correcto, se puede entrenar un adaptador
sobre triplets `(query real, skill-correcto, skill-incorrecto-recuperado)` acumulados de
logs de `consultar-skills.py` — **sin re-embeddar los cientos de skills**.
En query-time: `adapted = adapter.transform(query_vec)` antes del NN-search.

## Pipeline (2 módulos composable)

```bash
pip install "linear-adapter-trainer[sentence-transformers]"   # o [openai], [all]
```

**Módulo 1 — DatasetGenerator:** triplets `(query, positive, negative)` desde una base
de conocimiento (JSONL chunks). Estrategias de negativos: `hard` (más similares pero
incorrectos — señal más fuerte), `semantic_opposite`, `random`, `mixed` (blend).
Split train/val sin leakage. Queries con `TemplateQueryGenerator` (offline) o
`LLMQueryGenerator` (naturales, necesita API key).

**Módulo 2 — AdapterTrainer:** matriz lineal PyTorch (inicializada en identidad),
triplet loss `L = max(0, d(adapter(q), pos) − d(adapter(q), neg) + margin)` con
`d` = coseno (default) o euclidea. Métricas: precision@k, recall@k, MRR, nDCG.
Guarda en **safetensors** (versioned JSON metadata, sin pickle).

### Quickstart real (verificado del README 2026-09-03)

```python
from linear_adapter_trainer import (
    AdapterTrainer, DatasetConfig, DatasetGenerator, KnowledgeBase,
    TemplateQueryGenerator, TrainingConfig, LinearAdapter)
from linear_adapter_trainer.embeddings import SentenceTransformerEmbedder

kb = KnowledgeBase.from_jsonl("kb.jsonl")
embedder = SentenceTransformerEmbedder("sentence-transformers/all-MiniLM-L6-v2")
dataset = DatasetGenerator(knowledge_base=kb, embedder=embedder,
    query_generator=TemplateQueryGenerator(seed=0),
    config=DatasetConfig(queries_per_chunk=4, strategy="mixed", val_fraction=0.2)).generate()
result = AdapterTrainer(kb, embedder, TrainingConfig(epochs=30)).fit(dataset)
print(result.improvement)                      # delta por métrica vs base
result.adapter.save("adapter.safetensors")

# query-time:
adapter = LinearAdapter.load("adapter.safetensors")
adapted = adapter.transform(embedder.embed(["mi consulta"]))
```

### CLI (todo por TOML)

```bash
linear-adapter generate config.toml   # dataset
linear-adapter train    config.toml   # entrenar + métricas
linear-adapter evaluate config.toml   # base vs adaptado
linear-adapter run      config.toml   # generate → train
```

Ejemplo de output real del README: `precision@1 0.52→0.71 (+0.19)`, `mrr 0.631→0.805`, `ndcg@10 0.689→0.842`.

## Pitfalls

- **El demo offline (HashingEmbedder + template queries) da delta ~0 por diseño:** las
  queries reutilizan tokens de los chunks → baseline ya óptimo. Para ver ganancias
  reales hay que usar backend semántico y queries tipo LLM. NO concluir "no funciona".
- Solo adapta el lado QUERY: si los chunks están mal embebidos, el adaptador no lo arregla.
- 29⭐ y proyecto joven (Beta): tratar como patrón+herramienta de laboratorio, no
  infraestructura crítica. Python 3.12+.
- Checkpoints legacy `.pt`/`.pth` se leen con `weights_only=True` (deprecados); migrar con
  `LinearAdapter.migrate_checkpoint(...)`. Un `.safetensors` malformed se rechaza — nunca
  reintenta como torch (medida anti-pickle-RCE, buena práctica a copiar).

## Verificación

1. Comparar métricas base vs adaptado en el split val (`evaluate`) — delta ≥ 0 garantizado.
2. Tras aplicar en producción: A/B manual de 5-10 queries reales contra ChromaDB con y sin `adapter.transform`.
3. Guardar el adaptador junto al índice, versionado (safetensors + metadata JSON).

## Referencias

- Repo: https://github.com/SantanderAI/linear-adapter-trainer (Apache-2.0, CI + CodeQL)
- Notebook demo: `examples/santander_retrieval_demo.ipynb` (scrape → chunks → triplets → train → métricas)
- Explorado por stars-explorer: 2026-09-03
- Relacionados: `ia/rag-knowledge-base`, `ia/supermemory`, scripts propios `consultar-skills.py` / `indexar-skills.py`
