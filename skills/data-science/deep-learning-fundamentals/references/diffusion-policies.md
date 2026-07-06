# Diffusion Policies — Control y Robótica

**Nota:** Aplicación de diffusion models a políticas de decisión/robótica.  
**Fecha:** 2026-07-06

---

## Concepto Central

Diffusion Policy (Chen et al., CoRL 2023) entrena un modelo de difusión condicional para modelar la distribución completa de acciones futuras dado el estado del agente. Captura **multimodalidad** que los métodos RL clásicos (PPO, SAC) colapsan.

**Paper:** arXiv:2303.04137 — https://diffusion-policy.cs.columbia.edu/

## Arquitectura

- **Visual encoder:** ResNet-18 → features visuales
- **State encoder:** MLP para estados cinemáticos
- **Fusion:** concat + MLP
- **Diffusion backbone:** U-Net 1D con cross-attention sobre observaciones
- **Horizon:** 16-32 pasos (receding horizon control)
- **Denoising:** 20 pasos default → DPM-Solver reduce a 4-8 pasos (5x más rápido)

## Datasets Clave

| Dataset | Contenido | URL |
|---------|-----------|-----|
| DROID | 337K demos, 5 robots | droid-dataset.github.io |
| Open X-Embodiment | 2M+ demos múltiples robots | robotics-transformer-x.github.io |
| BridgeV2 | Manipulación visión bimodal | github.com/rail-berkeley/bridge_data_robot |

## Variantes SOTA (2024-2025)

1. **Diffusion-Transformer Policy (DTP):** Horizon 100+ pasos con ViT + cross-attention diffusion
2. **Latent Diffusion Policy (LDP):** VAE compression + diffusion en espacio latente
3. **Zero-shot con Foundation Models:** DINOv2 features en lugar de ResNet entrenado

## Comparativa

| Método | Pros | Contras |
|--------|------|---------|
| PPO/SAC | Estable, bien entendido | Colapso a moda única |
| BC | Simple, rápido | Error compuesto |
| Diffusion Policy | Multimodal, SOTA performance | Costo inference, muchos pasos |
| Decision Transformer | Contextual, no necesita recompensa | Rollout data denso |

## Conexiones con el Sistema

- **World Models (#20):** Diffusion policies son un world model simplificado
- **ControlNet (#21):** Mismo cross-attention, aplicado a control de robots
- **SSMs (#1):** Alternativa a diffusion para secuencias largas (inference O(1) vs N pasos)

## Referencias

1. Chen et al., CoRL 2023 — arXiv:2303.04137
2. Ajay et al., ICLR 2023 — Diffuser: arXiv:2212.10156
3. Brohan et al., 2023 — RT-2
4. Liu et al., 2022 — DPM-Solver: https://github.com/LiuXiaoxinPKU/DPM-Solver
