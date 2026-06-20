---
name: state-space-models
version: "1.0.0"
title: State Space Models (Mamba)
description: Arquitectura State Space Models para modelado de secuencias — Mamba-1, Mamba-2, S4, RWKV. Ecuaciones diferenciales, discretización ZOH, mecanismo selectivo, atención kernelizada. Aplicaciones a series temporales eléctricas y edge deployment.
tags: [deep-learning, ssm, mamba, state-space, sequence-modeling, time-series, edge-ai]
added: 2026-06-12
---

# State Space Models (Mamba) — Arquitectura y Aplicaciones

## Qué es

State Space Models (SSMs) reformulan el modelado de secuencias como una ecuación diferencial de control continuo. Alternativa eficiente a Transformers con complejidad O(N) por token en inference.

## Cuándo usarlo

- Series temporales largas con dependencias a largo plazo (demanda eléctrica, precios, renovables)
- Contextos >32K tokens donde los Transformers exceden memoria
- Deployment en edge/resource-constrained (MicroVM 1vCPU/2GB)
- Inference en tiempo real con latencia constante
- Reemplazar LSTM/GRU cuando se necesita mejor scaling

## Ecuación Base

```
h'(t) = A·h(t) + B·x(t)
y(t) = C·h(t) + D·x(t)
```

Discretización con Zero-Order Hold (ZOH):
```
h_t = Ā·h_{t-1} + B̄·x_t
y_t = C·h_t + D·x_t
```

## Evolución de la Familia

| Modelo | Año | Innovación | Paralelizable |
|--------|-----|-----------|---------------|
| S4 | 2021 | SSM estructurado para secuencias | Parcial |
| S5 | 2022 | Multi-variable, mejor estabilidad | Parcial |
| Mamba-1 | 2023 | Mecanismo selectivo (B,C,Δ dependen de x) | ❌ Secuencial |
| Mamba-2 | 2024 | Attention kernelizada (SSD), full parallel | ✅ Full |
| RWKV-6 | 2024 | RNN-like con expressividad Transformer | ✅ Full |
| xLSTM | 2024 | LSTM expandida + element-wise gating | ✅ Full |
| Gated DeltaNet | 2023 | Linear Attention con gating | ✅ Full |

### Comparativa Subcuadrática (2026)

Ver `references/subquadratic-architectures-comparison.md` para análisis completo de Hartl et al. 2026 comparando xLSTM vs Mamba-2 vs Gated DeltaNet.

**Hallazgos clave (junio 2026):**
- xLSTM gana en rendimiento general (mejor state tracking, gating flexible)
- Mamba-2 sigue siendo rey en eficiencia de inference (latencia + memoria)
- Gated DeltaNet es la opción más hardware-friendly (NPUs, edge)
- Patrón hybrid Mamba2+Transformer (Zamba2-VL) compite con VLMs de 7B+
- State sink en Mamba-2: probes de single-bucket pierden mitad del circuito (2606.00930)
- Task-dependent encoding: misma arquitectura invierte perfil según tarea (2606.00926)

### Mamba-1 vs Mamba-2

**Mamba-1:** Scan secuencial con mecanismo selectivo. O(N) inference pero training lento por falta de paralelización.

**Mamba-2:** Reformula el scan como atención kernelizada. Mismo O(N) inference pero training paralelizable como Transformer. Mejor estabilidad y reasoning.

## Implementación

Ver `references/mamba-implementation.md` para código completo funcional (Mamba2SSM, Mamba2Block, forecaster ESIOS).

Puntos críticos:
1. Discretización ZOH para estabilidad numérica
2. Parámetros selectivos (B, C, Δ) dependen de la entrada
3. Conv1d short-cut para patrones locales
4. Log-space para cumprod de A (evita underflow)
5. Skip connection con D (parámetro diagonal)

## Aplicaciones al Stack Actual

### Predicción de Demanda Eléctrica
- Ventana semanal (168h) → predicción 24-168h adelante
- Captura estacionalidad + patrones semanales + ruido
- Ideal para datos ESIOS/REE

### Detección de Anomalías
- Modelar distribución normal del sistema
- Detectar desviaciones en producción renovable o demanda

### Edge Deployment
- O(N) memory + inference constante = perfecto para MicroVM
- Sin necesidad de GPU, sin bundler

## Referencias

- **Implementación completa:** `references/mamba-implementation.md`
- **Comparativa con Diffusion:** Ver skill `diffusion-models` — SSM para forecast rápido + Diffusion para escenarios de riesgo
- **Mamba original:** arXiv:2312.00752 — Gu & Dao
- **Mamba-2:** arXiv:2405.21060 — Dao & Gu
- **S4:** arXiv:2111.00396 — Gu et al.
- **VMamba:** arXiv:2401.10166 — Liu et al.
- **RWKV-6:** arXiv:2404.05892 — Peng et al.
- **Hyena:** arXiv:2302.10866 — Poli et al.
- **Jamba (MoE hybrid):** AI21 Labs 2024
- **Repos:** github.com/state-spaces/mamba, github.com/BlinkDL/RWKV-LM, github.com/MzeroMiko/VMamba

## Próximos Temas Relacionados

- **Diffusion Models** → ✅ Cubierto. Ver skill `diffusion-models`
- **Subquadratic Architectures** → ✅ Cubierto. Ver `references/subquadratic-architectures-comparison.md` (xLSTM vs Mamba-2 vs GDN)
- Transformers architecture deep-dive (FlashAttention, RoPE, MoE)
- Graph Neural Networks (para redes eléctricas, transporte)
- **Quantization & Model Compression** → ✅ Cubierto. Ver skill `deep-learning-fundamentals` — INT8/INT4/GGUF/AWQ para edge deployment en MicroVM
- **LoRA/PEFT** → ✅ Cubierto. Ver skill `deep-learning-fundamentals` — fine-tuning con 4bit + adapters
- **RAG systems** → Integración con ChromaDB, búsqueda semántica
- **FlashAttention** → Optimización de atención O(n²d) → O(n√d) para acelerar inference