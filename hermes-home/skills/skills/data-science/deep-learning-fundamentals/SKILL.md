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
| 9 | Neural Radiance Fields / Gaussian Splatting | 2026-06-20 | `notes/deep-learning/2026-06-20-nerf-gaussian-splatting.md` |
| 10 | FlashAttention v2/v3 | 2026-06-21 | `references/flashattention-cheatsheet.md` |
| 11 | Vision Transformers (ViT) | 2026-06-22 | `notes/deep-learning/2026-06-22-vision-transformers.md` |
| 12 | Rectified Flow | 2026-06-23 | `references/rectified-flow.md` |
| 13 | Retrieval-Augmented Generation (RAG) | 2026-06-24 | `notes/deep-learning/2026-06-24-retrieval-augmented-generation.md` |
| 14 | Self-Supervised Learning (Contrastive) | 2026-06-25 | `notes/deep-learning/2026-06-25-self-supervised-learning-contrastive.md` |
| 15 | CLIP / Multimodal Learning | 2026-06-26 | `notes/deep-learning/2026-06-26-clip-multimodal-learning.md` |
| 16 | Knowledge Distillation | 2026-06-27 | `notes/deep-learning/2026-06-27-knowledge-distillation.md` |
| 17 | RLHF y Técnicas de Alineación (DPO, ORPO, KTO) | 2026-06-29 | `references/rlhf-alignment-cheatsheet.md` |

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
- **Mixture of Tokenizers (MoT)** — Mezclar tokenizadores para vocabularios mixtos (texto+code+medicina). Conecta con LoRA/PEFT (adapter por tokenizador).
- **Distillation de LLMs grandes a pequeños** — LLM distillation: Llama-70B → Llama-8B. Conecta con Knowledge Distillation (#16) y Quantización (#5).
- **Chain-of-Thought & Reasoning LLMs** — CoT, ToT, GoT, self-consistency. Complementa generación con razonamiento estructurado.

### Media prioridad:
- **Diffusion Transformers (DiT)** — Evolución de diffusion models (SD3, Flux). Conecta con Diffusion Models (#2).
- **Multi-Agent Systems & Agentic Workflows** — Sistemas de agentes que colaboran. Conecta con mastermind-orchestration.
- **Edge AI / On-device LLMs** — Inferencia de LLMs en edge (Raspberry Pi, móvil). Conecta con Quantización (#5) y llama-cpp.
- **Evaluation & Benchmarking de LLMs** — Medir calidad: MMLU, HumanEval,IFEval. Conecta con RLHF (#17).
## Referencias Cruzadas

- `references/lora-peft-inventory.md` — Inventario completo de +30 métodos PEFT, inicializaciones, configs recomendadas
- `references/quantization-model-compression.md` — FP32 → INT4 en la práctica
- `references/flashattention-cheatsheet.md` — Cheatsheet rápido: decisión, API, benchmarks, CPU alternatives
- `references/rectified-flow.md` — Flow matching, ODE solvers, consistency distillation, FLUX/SD3
- `references/rlhf-alignment-cheatsheet.md` — RLHF clásico, DPO, ORPO, KTO, comparativa y decisión
- **state-space-models** — SSM, Mamba, aplicaciones a series temporales
- **diffusion-models** — Modelos de difusión, series temporales
- **geoai-city2graph-pattern** — GNN para datos geoespaciales
- **llama-cpp** — Inferencia GGUF en CPU (conecta con quantización)
- **serving-llms-vllm** — Serving de LLMs con cuantización
