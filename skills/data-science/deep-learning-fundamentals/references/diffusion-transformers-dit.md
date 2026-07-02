# Diffusion Transformers (DiT) — Referencia Técnica

## Sesión: 2026-07-02

---

## Paper Original

**"Scalable Diffusion Models with Transformers"** — Dhariwal & Nichol (2023)
- arXiv:2303.08774
- Demostró que un transformer puro reemplaza a la U-Net en generación de difusión
- Mejor FID que U-Net a igual compute, escalado lineal predecible

## Arquitectura Clave

### Patch Embedding
- Imagen → patches → proyección lineal a tokens
- A diferencia de tokenización discreta (BPE), usa embeddings continuos

### Timestep Embedding
- Sinusoidal + MLP proyección
- Conecta con el proceso de difusión (timestep muestreado)

### AdaLN-Zero
- Adaptive Layer Normalization con 6 proyecciones (shift/scale/gate × attn/mlp)
- Zero initialization al inicio del training
- Permite que el timestep module toda la red

### DiT Block
- Self-attention sobre patches
- Cross-attention para conditioning (texto/clase)
- MLP con GELU
- AdaLN-Zero modulation

## Optimizaciones Recientes (arXiv 2024-2026)

### DyDiT (Oct 2024) — arXiv:2410.03456
- Dynamic Width por timestep + Dynamic Token por región espacial
- 51% menos FLOPs en DiT-XL, 1.73x más rápido
- Repo: NUS-HPC-AI-Lab/Dynamic-Diffusion-Transformer

### PiT (May 2025) — arXiv:2505.13219
- Progressive: early layers local attention, late layers global
- Reduce costo cuadrático de self-attention

### Post-Training Quantization (Mar 2025) — arXiv:2503.06930
- Hierarchical timestep grouping para INT8/INT4
- Relevante para deploy en MicroVMs 2GB

### Diffusion Transformer Policy (Mar 2025) — arXiv:2410.15959
- Control robótico: modelar secuencias de acción continua con DiT
- SOTA en SimplerEnv, Franka Arm, Libero

## Aplicación a Series Temporales

```python
# Patrón TimeSeries-DiT:
# Input: (B, T, F) → patches temporales → transformer diffusion
# Output: distribución sobre valores futuros (no punto único)
# Ideal para forecasting probabilístico en ESIOS
```

## Conexiones con Otros Temas

- **Diffusion Models**: DiT es la evolución arquitectural de U-Net a transformer
- **Vision Transformers**: Patch embedding similar, pero con timestep conditioning
- **FlashAttention**: Necesario para escalar self-attention sobre patches
- **Quantización**: DiT es grande → PTQ jerárquica es clave para edge
- **Normalizing Flows**: Flow matching es alternativa a diffusion, DiT también aplica

## Implementaciones de Referencia

- **timm**: `huggingface/pytorch-image-models` (DiT oficial)
- **diffusers**: `diffusers` library (StableDiffusionXLPipeline usa DiT)
- **DyDiT**: `NUS-HPC-AI-Lab/Dynamic-Diffusion-Transformer`
