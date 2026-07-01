# Rectified Flow — Referencia Rápida

> Generado: 2026-06-23 (DL-12)

## Concepto Central

Rectified Flow endereza las trayectorias de transporte entre distribuciones, transformando las curvas de los diffusion models en trayectorias casi rectas. Resultado: **1-4 pasos de inferencia** con calidad SOTA.

## Tres Capas de Framework

```
Diffusion (DDPM)     → SDE, score matching, 50-1000 pasos
Flow Matching        → ODE, velocity matching, 4-12 pasos
Rectified Flow       → ODE + rectificación iterativa, 1-4 pasos
     ↓ Consistency Distillation
InstaFlow            → 1 paso directo
```

## Core: Rectificación Iterativa

```
Iter 0: x_t = (1-t)*x_noise + t*x_data  (lineal)
Iter 1: resolver ODE con v_θ → trayectorias más rectas
Iter 2: re-entrenar con trayectorias de Iter 1
...
Cada iteración → trayectorias más rectas → menos pasos inferencia
```

Loss: `L = E[||v_θ(x_t, t) - (x_1 - x_0)||²]`

## Implementaciones Clave

| Componente | Detalle |
|-----------|---------|
| VelocityNet | MLP con sinusoidal time embedding + residual time connection |
| ODE Solver | Euler (simple), torchdiffeq (adaptive) |
| Consistency Distillation | Student predice x_1 desde x_t, teacher da target con 1 Euler step |
| DiT Block | AdaLN-Zero: shift/scale/gate condicionales en timestep |

## Modelos de Producción

| Modelo | Org | Año | Stars | Base |
|--------|-----|-----|-------|------|
| FLUX.1 | Black Forest Labs | 2024 | 25K+ | Rectified Flow Transformer |
| SD3 | Stability AI | 2024 | — | Flow Matching + DiT |
| TripoSG | VAST AI | 2025 | 1.7K+ | 3D shape synthesis |
| FluxMusic | — | 2025 | 1.7K+ | Text-to-Music |
| InstaFlow | — | 2024 | 1.4K+ | One-step SD |

## Papers Clave

1. **Rectified Flow** — Liu et al., ICLR 2023 Spotlight (arXiv:2210.02747)
2. **Flow Matching** — Lipman et al., ICLR 2023 (arXiv:2302.00410)
3. **Consistency Models** — Saharia et al., ICML 2022
4. **Variational Rectified Flow** — Guo & Schwing, 2025 (arXiv:2502.09616)
5. **Hierarchical Rectified Flow** — 2025 (arXiv:2502.17436)
6. **RAC: Rectified Flow Auto Coder** — 2026

## Repos GitHub

- [gnobitab/RectifiedFlow](https://github.com/gnobitab/RectifiedFlow) — 1618⭐ oficial
- [gnobitab/InstaFlow](https://github.com/gnobitab/InstaFlow) — 1409⭐ one-step
- [black-forest-labs/flux](https://github.com/black-forest-labs/flux) — 25K⭐
- [huggingface/diffusers](https://github.com/huggingface/diffusers) — 33K⭐ `FlowMatchEulerDiscreteScheduler`

## Conexiones con el Stack

- **DL-2 (Diffusion):** Rectified Flow es evolución natural — mismo objetivo, ODE en vez de SDE
- **DL-10 (FlashAttention):** FLUX usa transformers en vez de U-Net → FA2 acelera training
- **DL-8 (LoRA/PEFT):** Fine-tuning de FLUX con LoRA es viable y documentado
- **DL-6 (GNNs):** Flow matching puede modelizar distribuciones sobre grafos
- **DL-11 (ViT):** DiT (Diffusion Transformer) = ViT adaptado para generación
- **ESIOS:** Flow matching para series temporales energéticas (conectar con DL-2)

## Instalación

```bash
pip install torchdiffeq  # ODE solver
pip install diffusers    # FlowMatchEulerDiscreteScheduler
pip install accelerate   # para FLUX inference
```
