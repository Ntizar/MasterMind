---
name: deep-learning-notes
version: "1.0.0"
description: "Pipeline para crear notas técnicas profundas (15-30KB) sobre temas de deep learning. Incluye investigación, implementación práctica con código, y referencias a papers. Se ejecuta como cron diario."
tags: [deep-learning, research, notes, cron, learning]
---

# Deep Learning Notes — Pipeline de Aprendizaje Profundo

## Trigger

Se ejecuta automáticamente como cron diario (`mastermind-autoconfig` o cron dedicado). Elige un tema nuevo de deep learning que no esté ya cubierto en `/hermes-home/notes/deep-learning/`.

## Workflow

### 1. Elegir tema

Revisar `/hermes-home/notes/deep-learning/` para ver qué temas ya se cubrieron. Elegir un tema:
- **NO repetido** — verificar lista de temas cubiertos
- **Práctico** — priorizar implementaciones sobre teoría abstracta
- **Relevante** — preferir temas que impacten el stack actual (LLMs, inference, vision, RL)

### 2. Investigar

- Buscar papers recientes (arXiv, Nature, ICML, NeurIPS)
- Buscar implementaciones de referencia en GitHub
- Buscar tutoriales y documentación clave

### 3. Escribir nota

La nota debe tener:
- **Extensión:** 15-30KB mínimo
- **Código funcional** — implementaciones PyTorch completas
- **Diagramas ASCII** — arquitecturas, flujos de datos
- **Referencias** — papers, repos, libros, recursos
- **Comparaciones** — tablas de algoritmos, cuándo usar cada uno
- **Ejemplos prácticos** — experimentos ejecutables

### 4. Guardar

Guardar en `/hermes-home/notes/deep-learning/YYYY-MM-DD-titulo.md`

### 5. Proponer siguiente tema

Al final del reporte, sugerir 1-2 temas para la siguiente sesión.

## Temas típicos de deep learning

- Redes convolucionales (CNNs, ResNet, EfficientNet)
- Transformers (architectures, attention variants, scaling laws)
- GANs (StyleGAN, DCGAN, conditional GANs)
- Reinforcement Learning (DQN, PPO, SAC, A2C, TD3)
- Model compression (pruning, quantization, distillation)
- Self-supervised learning (SimCLR, MoCo, MAE)
- Multi-modal models (CLIP, DALL-E, LLaVA)
- Inference optimization (KV cache, speculative decoding, FlashAttention)
- Architecture innovations (State Space Models, Mamba, RWKV)
- Generative models (Diffusion, VAE, Flow-based, Normalizing Flows)
- Graph Neural Networks (GNN, GCN, GAT, GraphSAGE)
- Neural ODEs, Continuous normalizing flows
- Bayesian Deep Learning, Uncertainty quantification
- Federated Learning, Distributed training
- Prompt engineering, In-context learning
- RLHF, DPO, Constitutional AI
- Vision Transformers (ViT, Swin, DeiT)
- 3D vision (NeRF, Gaussian Splatting, 3DGS)
- Time series / forecasting (TimesFM, PatchTST, TiDE)

## Reglas

1. **NUNCA repetir temas** — siempre verificar el directorio primero
2. **Código ejecutable** — las implementaciones deben funcionar con PyTorch + Gymnasium
3. **Referencias reales** — papers con links, repos con stars
4. **En español** — TODO el contenido en castellano
5. **15-30KB mínimo** — notas cortas no aportan valor profundo
6. **No usar docstrings en código** — usar comentarios `#` para evitar SyntaxError en write_file

## Instalación de dependencias

```bash
# Crear venv (PEP 668 bloquea pip global)
python3 -m venv /tmp/rl-venv
source /tmp/rl-venv/bin/activate

# Instalar libs
pip install gymnasium stable-baselines3[extra] sb3-contrib torch

# IMPORTANTE: limpiar después
rm -rf /tmp/rl-venv  # PyTorch ocupa ~5GB en venv
```

**Pitfall:** Los venvs con PyTorch ocupan ~5GB. Siempre limpiar después de la sesión.

## Pitfalls

- **`write_file` con docstrings en código Python** — usar `#` comentarios en vez de `"""` docstrings dentro de bloques de código en markdown
- **`cat > file << 'EOF'` heredoc** — falla si el contenido tiene `&` (terminal lo interpreta como background). Usar `write_file` directo.
- **`execute_code` → `write_file` para contenido >10KB** — puede colgarse. Usar `write_file` directo.
- **`df -h` antes de instalar** — verificar espacio disponible antes de instalar PyTorch (ocupa ~2GB)
- **No instalar en sistema** — siempre usar venv temporal, nunca `pip install --break-system-packages`

## Referencias

- `references/covered-topics.md` — Lista completa de temas ya cubiertos en `/hermes-home/notes/deep-learning/` (actualizada 2026-07-14, 29 notas)
- `/hermes-home/notes/deep-learning/` — directorio de notas existentes
- `research-paper-writing` — skill para papers académicos (no confundir con notas técnicas)
- `python-code-implementation` — pitfall de docstrings en `write_file`
