---
name: deep-learning-patterns
description: Ecosistema completo de patrones de deep learning — inference optimization, model architectures, training techniques, generation methods
version: "1.0.0"
author: mastermind
---

# Deep Learning — Patrones y Técnicas

## Categorías

### Inference-Time Optimization
- **Test-Time Scaling (TTC/TTS)** — Dynamic compute allocation during inference
  - Subcategories: CoT, Self-Consistency, Best-of-N, Beam Search, MCTS, Self-Correction
  - Verifiers: ORM (outcome) vs PRM (process)
  - Key insight: Performance = f(Parámetros × Datos × Cómputo de Inferencia)
  - See: references/test-time-scaling.md

- **Speculative Decoding** — Fast autoregressive generation with draft models
- **Quantization** — FP32 → FP16 → INT8 → INT4 compression
- **KV Cache Optimization** — PagedAttention, continuous batching

### Model Architectures
- **Transformers** — Standard, Sparse, Longformer, BigBird
- **Vision Transformers (ViT)** — Patches, hybrid, Swin
- **Diffusion Models** — U-Net, DiT, Rectified Flow, Consistency Models
- **State Space Models** — Mamba, S4, Mamba-2
- **Mixture of Experts (MoE)** — Switch, GShard, Mixtral
- **Graph Neural Networks** — GNN, GAT, GraphSAGE
- **World Models** — Generative simulation, Sora, Gen-2

### Training Techniques
- **Fine-Tuning** — Full, LoRA, QLoRA, DoRA, AdaLoRA
- **RLHF / RLAIF** — PPO, DPO, GRPO, Constitutional AI
- **Self-Supervised** — Contrastive, Masked, Self-Distillation
- **Knowledge Distillation** — LLM → small model, cross-modal

### Multimodal
- **CLIP** — Image-text alignment
- **Vision-Language Models** — LLaVA, BLIP, Flamingo

## Usage

When working on a deep learning task:
1. Identify the category (inference, architecture, training, multimodal)
2. Load specific sub-skills with `skill_view(name='dl-<specific>')`
3. Consult `references/` for detailed notes from past sessions
4. Check `references/test-time-scaling.md` for TTC/TTS comprehensive guide
