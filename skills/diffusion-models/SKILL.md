---
name: diffusion-models
version: "1.0.0"
title: Diffusion Models
description: Modelos generativos de difusión — DDPM, DDIM, Stable Diffusion, DiT, LCM, Flow Matching. Fundamentos matemáticos, implementaciones desde cero, series temporales, forecasting probabilístico, generación de escenarios.
tags: [deep-learning, diffusion, ddpm, ddim, stable-diffusion, dit, latent-diffusion, time-series, probabilistic-forecasting, scenario-generation, consistency-models, flow-matching]
added: 2026-06-13
---

# Diffusion Models — Fundamentos, Implementación y Aplicaciones

## Qué es

Los Diffusion Models son modelos generativos que aprenden a **invertir un proceso de difusión de ruido gaussiano**. Forward: añade ruido progresivamente hasta convertir datos en ruido puro. Reverse: una red neuronal aprende a eliminar el ruido paso a paso, generando datos nuevos.

## Cuándo usarlo

- **Forecasting probabilístico** — modelar distribución completa de futuros posibles (no solo una media)
- **Generación de escenarios** — crear datos sintéticos realistas para stress testing, planificación
- **Incertidumbre cuantificada** — intervalos de confianza bien calibrados (VaR, CVaR)
- **Datos multimodales** — cuando hay múltiples modos plausibles (ej: día laborable vs festivo)
- **Detección de anomalías** — reconstrucción con error alto = anomalía

## No usar cuando

- Necesitas inference ultra-rápida sin GPU → usa SSM (Mamba) o AR models
- Tienes muy pocos datos (<500 secuencias) → overfitting rápido
- Solo necesitas predicción puntual → autoregresivos son suficientes

## Ecuación Base

**Forward (fijado, no aprendido):**
```
q(x_t | x_{t-1}) = N(x_t; √(1-β_t) · x_{t-1}, β_t · I)
x_t = √(ᾱ_t) · x_0 + √(1-ᾱ_t) · ε,   ε ~ N(0, I)
```

**Reverse (aprendido — predicción de ruido):**
```
L = E_{t, x_0, ε} [ || ε - ε_θ(x_t, t) ||² ]
```

Solo regresión L2 de el ruido. La simplicidad es su belleza.

## Evolución de la Familia

| Modelo | Año | Innovación | Pasos |
|--------|-----|-----------|-------|
| **DDPM** | 2020 | Predicción de ruido + U-Net | 1000 |
| **DDIM** | 2020 | Muestreo no-markoviano | 10-50 |
| **Stable Diffusion** | 2021 | Latent Diffusion (VAE + U-Net) | 50 |
| **ADM** | 2021 | U-Net con attention + guidance | 1000 |
| **SDXL** | 2023 | Two-stage (refiner + base) | 50 |
| **DiT** | 2022 | U-Net → Transformer puro | 1000 |
| **SD3** | 2024 | MMDiT (multi-modal DiT) | 50 |
| **Flux** | 2024 | Flow Matching + DiT | 250 |
| **LCM** | 2023 | Consistency distillation | 4-8 |

### SSM (Mamba) vs Diffusion para el Stack

| Aspecto | SSM (Mamba) | Diffusion |
|---------|-------------|-----------|
| Inference | O(N) secuencial, muy rápido | Iterativo, lento (a menos que distillado) |
| Incertidumbre | Puntual (una predicción) | Distribución completa (multimodal) |
| Condicionamiento | Directo (input concatenado) | Flexible (cross-attention, CFG) |
| Edge deployment | ✅ Excelente | ⚠️ Requiere distillation |
| Forecasting puntual | ✅ Bueno | ⚠️ Overkill |
| Forecasting probabilístico | ❌ Limitado | ✅ Excelente |
| Generación de escenarios | ❌ No | ✅ Nativo |

**Recomendación:** SSM para forecast puntual rápido + Diffusion para escenarios de riesgo y generación de datos sintéticos. Son complementarios.

## Patrones de Implementación

### Patrón General para Series Temporales

```
1. Encoder: Mapear TS a latente (opcional, si Latent Diffusion)
2. Noise Scheduler: Añadir ruido gaussiano a la serie temporal
3. Denoiser Model: U-Net o Transformer que predice el ruido añadido
4. Conditioning: Inyectar datos exógenos (clima, hora, día) en el denoiser
5. Sampling: Iterar desde ruido aleatorio hasta predicción final
```

### Classifier-Free Guidance

```
ε_guided = ε_uncond + w · (ε_cond - ε_uncond)

w = 1.0  → sin guidance (comportamiento estándar)
w > 1.0  → más fiel al condicionamiento (menos variado)
w < 1.0  → más variado/creativo (menos fiel)
```

Durante training: drop conditioning con prob p_drop≈0.1 para que el modelo aprenda ambos modos.

### Fast Sampling para MicroVM (1vCPU/2GB)

1. **LCM (Latent Consistency Models):** Reducir pasos de 50 a 4-8
2. **DDIM:** Muestreo no-markoviano para 10-20 pasos con buena calidad
3. **Distillation:** Entrenar modelo "estudiante" que mapea ruido → datos en pocos pasos
4. **Quantización INT8:** Reduce modelo de ~2MB a ~0.5MB
5. **ONNX export:** Inferencia sin PyTorch

## Aplicaciones al Stack Actual

### Forecasting de Demanda Eléctrica
- **Modelo:** DiffusionTime o TSDiff
- **Input:** Series históricas de demanda + datos meteorológicos
- **Output:** Distribución de probabilidad (mediana, percentiles 5/95)
- **Ventaja:** Mejor calibración de riesgo que LSTM/Transformer

### Forecasting de Generación Renovable
- **Modelo:** Conditional Latent Diffusion
- **Input:** Irradiación/viento + patrones históricos
- **Output:** Escenarios de generación posible
- **Ventaja:** Captura eventos extremos (nubes repentinas, rachas de viento)

### Detección de Anomalías
- **Modelo:** Diffusion reconstrucción
- **Lógica:** Entrenar DM en datos normales. Alto error de reconstrucción = anomalía

## Pitfalls Críticos

1. **Loss NaN:** Asegurar que el schedule de ruido no tenga β_t = 1 (clip a max 0.02)
2. **Inestabilidad en sampling:** Clamp predicciones a [-5, 5] en cada paso DDIM
3. **Overfitting rápido:** Los DM necesitan ≥1000 secuencias para resultados decentes
4. **Gradientes explosivos:** Usar `clip_grad_norm_` (max 1.0)
5. **No usar SD3/Flux en MicroVM:** Muy pesados. Usar DiffusionTime o MLP pequeño (hidden_dim=64, layers=3)
6. **Schedule cosine > linear:** Más estable numéricamente en los primeros pasos
7. **Guidance scale:** w > 5 produce artefactos. Rango seguro: 1.5-3.0

## Referencias

- **Implementación completa:** `references/diffusion-implementation.md`
- **DDPM original:** arXiv:2006.11239 — Ho et al.
- **DDIM:** arXiv:2010.02502 — Song et al.
- **Stable Diffusion:** arXiv:2112.10752 — Rombach et al.
- **DiT:** arXiv:2212.09748 — Pezeshki et al.
- **SD3:** arXiv:2403.03206 — Esser et al.
- **Flux:** arXiv:2410.25781 — Black Forest Labs
- **LCM:** arXiv:2310.04378 — Lu et al.
- **Consistency Models:** arXiv:2303.11216 — Song et al.
- **Flow Matching:** arXiv:2302.03686 — Lipman et al.
- **DiffusionTime:** arXiv:2302.04548 — Wang et al. (series temporales)
- **TSDiff:** arXiv:2303.08313 — Kim et al.
- **Repos:** github.com/huggingface/diffusers, github.com/hojonathanho/diffusion, github.com/thuml/Time-Series-Library