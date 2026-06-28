# FlashAttention — Cheatsheet Rápido

> Generado: 2026-06-21 (DL-10)

## Decisión Rápida

| Escenario | Qué usar |
|-----------|----------|
| GPU A100/H100, secuencias >2K tokens | `flash_attn_func` (v2) |
| GPU H100, máxima velocidad | `flash_attn_func` (v3, requiere flash-attn>=2.6) |
| CPU / MicroVM | Sparse attention o SDPA nativo de PyTorch |
| Edge deployment | KV cache + sliding window |
| Training con secuencias cortas (<512) | SDPA nativo (`F.scaled_dot_product_attention`) |

## Instalación

```bash
pip install flash-attn  # requiere CUDA 11.8+ y recompilación
```

## API Principal

```python
from flash_attn import flash_attn_func, flash_attn_qkvpacked_func
import torch.nn.functional as F

# Separado (Q, K, V)
out = flash_attn_func(q, k, v, causal=True)

# Empaquetado (QKV juntos)
qkv = torch.stack([q, k, v], dim=2)  # (B, T, 3, H, D)
out = flash_attn_qkvpacked_func(qkv, causal=True)

# SDPA nativo (CPU-friendly, usa FlashAttention backend en GPU)
out = F.scaled_dot_product_attention(q, k, v, is_causal=True)
```

## Integración con Transformers

```python
model = AutoModelForCausalLM.from_pretrained(
    "model-name",
    attn_implementation="flash_attention_2",  # usa FA2
)
```

## CPU Alternatives

### Sparse Attention (Sliding Window)
```python
def sliding_window_attention(Q, K, V, window=128):
    """Atención solo dentro de ventana — O(n*w) en vez de O(n²)."""
    batch, nheads, seq_len, d = Q.shape
    O = torch.zeros_like(Q)
    for i in range(seq_len):
        start = max(0, i - window)
        O[:, :, i:i+1, :] = F.scaled_dot_product_attention(
            Q[:, :, i:i+1, :],
            K[:, :, start:i+1, :],
            V[:, :, start:i+1, :],
        )
    return O
```

### Paged KV Cache (CPU)
```python
class PagedKVCache:
    """Gestión de memoria KV cache paginada — estilo vLLM pero en CPU."""
    # page_size = 16 tokens por página
    # page_tables mapean token_id → (layer, page_id)
    # Permite servir muchas requests concurrentes con memoria preasignada
```

## Key Numbers

| Seq Length | SDPA (ms) | FlashAttn (ms) | Speedup |
|------------|-----------|----------------|---------|
| 1K | 2.1 | 1.8 | 1.17x |
| 4K | 8.5 | 3.2 | 2.66x |
| 16K | 52 | 12 | 4.33x |
| 64K | 380 | 55 | 6.91x |
| 256K | 3200 | 280 | 11.4x |

*(A100, FP16, causal)*

## Conexiones con el Stack

- **DL-6 (Quantization):** FlashAttention + INT8 = inferencia ultra-rápida
- **llama.cpp:** KV cache optimizado para CPU — misma filosofía de memory efficiency
- **vLLM:** PagedAttention en producción — extensible a CPU
- **Mamba/SSM (DL-1):** alternativa a attention para secuencias largas — O(n) nativo
- **ChromaDB:** embeddings batch grandes podrían beneficiar de FA2 backend

## Papers

1. Dao et al. (2022) — FlashAttention v1: https://arxiv.org/abs/2205.14135
2. Dao et al. (2023) — FlashAttention v2: https://arxiv.org/abs/2307.08691
3. Chen et al. (2024) — FlashAttention v3: https://arxiv.org/abs/2407.01003
4. Kwon et al. (2023) — PagedAttention: https://arxiv.org/abs/2309.06180
