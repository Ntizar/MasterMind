# RLHF y Técnicas de Alineación — Cheatsheet

## Resumen

Técnicas para alinear LLMs con preferencias humanas, desde el pipeline clásico de RLHF (InstructGPT) hasta DPO, ORPO y KTO.

## Pipeline Clásico RLHF (4 fases)

```
SFT → Reward Modeling → PPO (RL) → Deploy
(1 modelo)  (1 modelo)  (Actor+Critic)
```
- Requiere 4 modelos distintos
- PPO es inestable y costoso
- Reward hacking (el modelo optimiza la recompensa, no el comportamiento real)

## DPO — Direct Preference Optimization (Rafael et al., 2023)

**Paper:** [arXiv:2305.18290](https://arxiv.org/abs/2305.18290)

- Elimina Reward Model + PPO
- Una sola función de pérdida sobre preferencias
- 1 modelo + 1 de referencia
- Perdida: `L_DPO = -E[log(σ(β * Δlogπ))]`
- SGD simple, mucho más estable

```python
def dpo_loss(chosen_lp, rejected_lp, ref_chosen, ref_rejected, beta=0.1):
    log_ratios_chosen = chosen_lp - ref_chosen
    log_ratios_rej = rejected_lp - ref_rejected
    return -F.logsigmoid(beta * (log_ratios_chosen - log_ratios_rej)).mean()
```

## ORPO — Odds Ratio Preference Optimization (Menon et al., 2024)

**Paper:** [arXiv:2402.01714](https://arxiv.org/abs/2402.01714)

- Sin reference model
- Combina SFT + DPO en una fase
- Menos overhead, rendimiento comparable

## KTO — Kahneman-Tversky Optimization

**Paper:** [arXiv:2402.01306](https://arxiv.org/abs/2402.01306)

- Datos etiquetados individualmente (no pares)
- Más fácil de obtener datos
- Similar rendimiento a DPO

## Comparativa Rápida

| Técnica | Modelos | Datos | Complejidad | Rendimiento |
|---------|---------|-------|-------------|-------------|
| RLHF (PPO) | 4 | Pares | Muy alta | Excelente |
| DPO | 2 | Pares | Baja | Muy bueno |
| ORPO | 1 | Pares | Muy baja | Muy bueno |
| KTO | 2 | Individual | Baja | Bueno |

## Implementación: TRL

La librería [TRL](https://github.com/huggingface/trl) de Hugging Face implementa DPO, ORPO, KTO, PPO-RLHF:

```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model, ref_model,
    beta=0.1,
    train_dataset=dataset_con_pares_chosen_rejected,
    tokenizer=tokenizer,
)
trainer.train()
```

## Datasets de Preferencia

- **UltraFeedback** (1.3M): Pares + individual — Stanford
- **hh-rlhf** (~90K): Pares Reddit — Anthropic
- **OpenHermes 2.5** (1M): Instrucciones — Apple/Open
- **RLHF-V** (10K+): Visual + texto — MIT

## ¿Cuándo usar qué?

```
¿Tienes pares (chosen/rejected)?
├── Sí → ¿Máximo rendimiento sin importar complejidad?
│   └── Sí → RLHF
│   └── No → DPO (standard) o ORPO (sin ref model)
└── No → ¿Tienes etiquetas individuales?
    └── Sí → KTO
```

## Aplicaciones al Stack

- **Generación de reportes personalizados** ESIOS con modelo alineado
- **Dolphin/OpenHermes**: generación de datos con rejection sampling
- **Adela**: modelos alineados para generación de código
