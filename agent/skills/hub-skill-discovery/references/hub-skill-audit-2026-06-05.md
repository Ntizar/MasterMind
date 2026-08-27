# Hub Skill Audit — 2026-06-05

## Resumen

- **Skills instalados:** 207
- **Skills en hub oficial:** 89 (opcionales)
- **Skills ya instalados del hub:** 4 (`baoyu-comic`, `canvas`, `dspy`, `ideation`)
- **Skills faltantes:** 85

## Priorización

### 🔥 Alta prioridad (20)
1. `duckduckgo-search` — Búsqueda web mejorada
2. `searxng-search` — Búsqueda privada con SearXNG
3. `scrapling` — HTTP fetching + scraping avanzado
4. `code-wiki` — Genera wiki docs + Mermaid para código
5. `rest-graphql-debug` — Debug de APIs REST/GraphQL
6. `docker-management` — Gestión de contenedores
7. `fastmcp` — Gestionar servidores MCP
8. `outlines` — Generación estructurada JSON/regex/Pydantic
9. `instructor` — Extracción de datos de LLM responses
10. `stocks` — Datos históricos de acciones/crypto
11. `qdrant-vector-search` — Búsqueda vectorial
12. `pinecone` — Base de datos vectorial
13. `chroma` — Base de datos embeddings
14. `llava` — Asistente visual (visión)
15. `whisper` — Reconocimiento de voz
16. `huggingface-hub` (bundled) — HF CLI
17. `llama-cpp` (bundled) — GGUF local
18. `vllm` (bundled) — LLM serving
19. `evaluating-llms-harness` (bundled) — Benchmark LLMs
20. `weights-and-biases` (bundled) — ML experiment tracking

### 📦 Media prioridad (45)
- `concept-diagrams`, `domain-intel`, `osint-investigation`, `sherlock`, `watchers`, `stable-diffusion-image-generation`, `meme-generation`, `hyperframes`, `qmd`, `siyuan`, `obsidian` (bundled), `gif-search` (bundled), `youtube-content` (bundled), `heartmula` (bundled), `songsee` (bundled), `arxiv` (bundled), `blogwatcher` (bundled), `polymarket` (bundled), `research-paper-writing` (bundled), `himalaya` (bundled), `airtable` (bundled), `google-workspace` (bundled), `maps` (bundled), `nano-pdf` (bundled), `notion` (bundled), `ocr-and-documents` (bundled), `powerpoint` (bundled), `teams-meeting-pipeline` (bundled), `openhue` (bundled), `xurl` (bundled), `hermes-agent-skill-authoring` (bundled), `plan` (bundled), `spike` (bundled), `systematic-debugging` (bundled), `test-driven-development` (bundled), `requesting-code-review` (bundled), `node-inspect-debugger` (bundled), `python-debugpy` (bundled), `kanban-orchestrator` (bundled), `kanban-worker` (bundled), `yuanbao` (bundled), `audiocraft-audio-generation` (bundled), `segment-anything-model` (bundled), `docker-management`

### 🗄️ Baja prioridad (20)
- `1password`, `evm`, `solana`, `hyperliquid`, `shopify`, `shop-app`, `telephony`, `drug-discovery`, `bioinformatics`, `neuroskill-bci`, `slime-rl-training`, `sparse-autoencoder-training`, `tensorrt-llm`, `pytorch-fsdp`, `pytorch-lightning`, `unsloth`, `peft-fine-tuning`, `fine-tuning-with-transformers`, `huggingface-accelerate`, `huggingface-tokenizers`, `lambda-labs-gpu-cloud`, `modal-serverless-gpu`, `nemo-curator`, `simpo-training`, `optimizing-attention`, `hermes-s6-container-runtime`, `here-now`, `blackbox`, `antigravity-cli`, `grok`, `parallel-cli`, `mcporter`, `inference-sh-cli`, `kanban-video-orchestrator`, `openclaw-migration`, `blender-mcp`, `3-statement-model`, `dcf-model`, `lbo-model`, `merger-model`, `excel-author`, `pptx-author`, `fitness-nutrition`, `memento-flashcards`, `one-three-one-rule`, `guidance`, `faiss`, `pinggy-tunnel`, `page-agent`, `oss-forensics`, `adversarial-ux-test`, `agentmail`, `comps-analysis`, `darwinian-evolver`, `distributed-llm-pretraining`, `clip`, `baoyu-article-illustrations`

## Decisiones

- No instalar de golpe — usar cron de 1 skill/hora
- Priorizar por relevancia al stack actual (web, data, ESIOS, creative, MLOps)
- Guardar cada skill aprendido en `/root/workspace/Mastermind/mastermind/` + commit
