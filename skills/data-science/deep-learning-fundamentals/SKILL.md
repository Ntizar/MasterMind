---
name: deep-learning-fundamentals
version: "1.0.0"
description: "Serie de aprendizaje profundo sobre arquitecturas de redes neuronales modernas — SSMs, Diffusion, MoE, Quantization, y más. Notas técnicas con código, papers de referencia y aplicaciones al stack ESIOS/MicroVM."
tags: [deep-learning, neural-networks, transformers, diffusion, quantization, edge-ai]
added: 2026-06-16
---

# Deep Learning Fundamentals — Serie de Aprendizaje

## Qué es

Serie de sesiones de aprendizaje profundo sobre arquitecturas de redes neuronales modernas, implementaciones prácticas y aplicaciones al stack actual (ESIOS, geodatos, edge deployment en MicroVM).

## Temas Cubiertos

| # | Tema | Fecha | Ref |
|---|------|-------|-----|
| 1 | State Space Models (Mamba) | 2026-06-12 | Skill `state-space-models` |
| 2 | Diffusion Models | 2026-06-13 | Skill `diffusion-models` |
| 3 | Subquadratic Architectures (xLSTM vs Mamba-2 vs GDN) | 2026-06-14 | `references/subquadratic-architectures-comparison.md` |
| 4 | Mixture of Experts (MoE) | 2026-06-15 | `references/mixture-of-experts.md` |
| 5 | Quantization & Model Compression | 2026-06-16 | `references/quantization-model-compression.md` |
| 6 | Graph Neural Networks (GNNs) | 2026-06-17 | `notes/deep-learning/2026-06-17-graph-neural-networks.md` |
| 7 | Speculative Decoding | 2026-06-18 | `notes/deep-learning/2026-06-18-speculative-decoding.md` |
| 8 | LoRA / PEFT | 2026-06-19 | `notes/deep-learning/2026-06-19-lora-peft.md` |

## Cómo se trabaja

Cada sesión sigue este patrón:
1. Revisar `/hermes-home/notes/deep-learning/` para evitar repetir temas
2. Elegir un tema no cubierto de la lista de candidatos
3. Investigar papers, implementaciones y repositorios relevantes
4. Escribir nota técnica con código de ejemplo en `/hermes-home/notes/deep-learning/YYYY-MM-DD-titulo.md`
5. Guardar copia en `/root/workspace/Mastermind/notes/` y hacer commit+push
6. Proponer tema siguiente

## Candidatos para Siguientes Sesiones

### Alta prioridad (relevante al stack):
- **RAG (Retrieval-Augmented Generation)** — Integración con ChromaDB existente, búsqueda semántica aplicada. Conecta con LoRA/PEFT (modelo fine-tuneado + RAG = mejor resultado).
- **Vision Transformers (ViT)** — Puente entre CV y transformers. Útil para imágenes satelitales.
- **Diffusion Transformers (DiT)** — Evolución de diffusion models (SD3, Flux). Conecta con nota de diffusion models.

### Media prioridad:
- **Self-Supervised Learning / Contrastive Learning** — Paradigma fundamental pre-entrenamiento.
- **Multi-Modal Models (CLIP, etc.)** — Para imágenes satelitales y análisis visual.
- **FlashAttention v2/v3** — Optimización de atención O(n²d) → O(n√d). Complementa speculative decoding.

## Referencias Cruzadas

- `references/lora-peft-inventory.md` — Inventario completo de +30 métodos PEFT, inicializaciones, configs recomendadas
- **state-space-models** — SSM, Mamba, aplicaciones a series temporales
- **diffusion-models** — Modelos de difusión, series temporales
- **geoai-city2graph-pattern** — GNN para datos geoespaciales
- **llama-cpp** — Inferencia GGUF en CPU (conecta con quantización)
- **serving-llms-vllm** — Serving de LLMs con cuantización
