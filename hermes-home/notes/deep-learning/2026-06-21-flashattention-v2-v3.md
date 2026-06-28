# FlashAttention v2 y v3 — Atención de Complejidad Sublineal

> **Fecha:** 2026-06-21  
> **Autor:** Mastermind (David Antizar)  
> **Serie:** Deep Learning Fundamentals — Sesión 10

## 1. El Problema Fundamental

La atención estándar de transformers tiene complejidad **O(n²d)** donde n = longitud de secuencia, d = dimensión de embedding. Esto es porque hay que:

1. **Materializar** la matriz completa `softmax(QK^T / √d)` de tamaño n×n
2. **Multiplicar** por V: `(n×n) × (n×d) → (n×d)`

Para secuencias largas (100K+ tokens), la matriz de atención ocupa **n² × 4 bytes** en memoria. Con n=100K → **40 GB** solo para la matriz de atención.

El bottleneck no es la computación (GPU FLOPs), sino el **memory bandwidth**. Las GPUs modernas son compute-bound para atención estándar, pero el problema es que la matriz QK^T es tan grande que se sale de SRAM y hay que hacer múltiples pasadas por HBM (High Bandwidth Memory), que es 5-10x más lenta.

## 2. FlashAttention v1 (2022) — Tiling en la GPU

### Paper: ["FlashAttention: Fast and Memory-Efficient Exact Attention"](https://arxiv.org/abs/2205.14135)

**Idea central:** En lugar de materializar la matriz completa QK^T en HBM, procesarla en tiles que caben en SRAM.

### Algoritmo en 4 pasos:

```
Para cada tile O_i (de salida):
  Para cada tile S_ij (de QK^T):
    1. Cargar Q_i, K_j, V_j de HBM → SRAM
    2. Computar S_ij = Q_i × K_j^T en SRAM
    3. Actualizar O_i con S_ij en SRAM (online softmax)
    4. Escribir O_i actualizado a HBM
```

**Online softmax** es la clave: en vez de computar softmax sobre toda la fila (n elementos), se hace incrementalmente:

```python
# Online softmax (Welford-style incremental)
# Para cada tile j=1..m:
#   1. m_ij = max(S_ij)                    # nuevo máximo parcial
#   2. l_ij = sum(exp(S_ij - m_ij))        # suma parcial normalizada
#   3. R_i = max(R_i, m_ij)                # máximo global acumulado
#   4. O_i = (O_i * exp(R_old - R_i) + l_ij * exp(S_ij - R_i)) / (l_i + l_ij)
#   5. l_i = l_i * exp(R_old - R_i) + l_ij
```

### Resultado:
- **13x más rápido** que PyTorch attention para secuencias largas
- **Memoria O(nd)** en vez de O(n²d) — lineal en n
- Exacto (no aproximado)

## 3. FlashAttention v2 (2023) — Optimizaciones

### Paper: ["FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"](https://arxiv.org/abs/2307.08691)

**Mejoras sobre v1:**

1. **Reducción de shared memory bank conflicts** — reorganizar el loading de K y V
2. **Work partitioning mejorado** — cada thread block procesa más tiles de forma balanceada
3. **Cascaded attention** — para batch sizes grandes, mejor distribución de trabajo
4. **Cuda graph support** — mejor para inferencia con batch variable

**Resultado:** 2-3x más rápido que v1 en A100/H100.

## 4. FlashAttention v3 (2024) — Multi-Block SM Partitioning

### Paper: ["FlashAttention-3: Fast and Accurate Attention with O(n²/b) Complexity"](https://arxiv.org/abs/2407.01003)

**Idea central:** Explotar la paralelización dentro de cada Streaming Multiprocessor (SM).

En v1/v2, cada SM procesa un tile completo. En v3:
- Cada SM se divide en **múltiples blocks** (2-4)
- Cada block procesa un sub-tile diferente
- Se usa **warp-level primitives** para comunicación intra-SM

### Optimizaciones clave:

```
v1/v2:  SM → 1 block → 1 tile
v3:     SM → 4 blocks → 4 sub-tiles en paralelo
```

**Tiling de multiplicación de matrices:**
- QK^T se compute en tiles de 64×64
- PV se compute en tiles de 64×64
- Cada tile se procesa con **tiled matmul** en tensor cores

**Resultado:**
- **3x más rápido** que v2 en H100
- **4x más rápido** que v2 en A100
- Mantiene exactitud numérica

## 5. Implementación Práctica

### 5.1. Uso con PyTorch (lo más común)

```python
import torch
import flash_attn  # pip install flash-attn

# FlashAttention v2 integrado en PyTorch
from flash_attn import flash_attn_qkvpacked_func, flash_attn_func

# Método 1: flash_attn_func (Q, K, V separados)
def forward_with_flash_attn(q, k, v, causal=True):
    """
    q, k, v: (batch, seq_len, nheads, headdim)
    """
    output = flash_attn_func(q, k, v, causal=causal)
    return output  # (batch, seq_len, nheads, headdim)

# Método 2: flash_attn_qkvpacked_func (QKV empaquetado)
def forward_with_qkvpacked(qkv, causal=True):
    """
    qkv: (batch, seq_len, 3, nheads, headdim)
    """
    output = flash_attn_qkvpacked_func(qkv, causal=causal)
    return output

# Método 3: Con rotary embeddings integrados (v2+)
from flash_attn.layers.rotary import apply_rotary_emb_func

# Integración con transformers
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Forzar uso de FlashAttention
model.config.use_flash_attention = True
# O con transformers 4.36+:
# model = AutoModelForCausalLM.from_pretrained(
#     "...",
#     attn_implementation="flash_attention_2",
# )
```

### 5.2. Implementación Educativa de FlashAttention v1 (simplificada)

```python
import torch
import torch.nn.functional as F

class FlashAttentionV1Edu(torch.nn.Module):
    """
    Implementación educativa simplificada de FlashAttention v1.
    
    Muestra el algoritmo de tiling + online softmax.
    NO es optimizada — solo para entender el patrón.
    """
    
    def __init__(self, tile_size=64):
        super().__init__()
        self.tile_size = tile_size
    
    def forward(self, Q, K, V, causal=False, scale=None):
        """
        Q, K, V: (batch, nheads, seq_len, d)
        Returns: output (batch, nheads, seq_len, d), attention weights (batch, nheads, seq_len, seq_len)
        """
        batch, nheads, seq_len, d = Q.shape
        scale = scale or (d ** -0.5)
        
        # Inicializar salida
        O = torch.zeros_like(Q)
        L = torch.zeros((batch, nheads, seq_len, 1), device=Q.device)
        M = torch.full((batch, nheads, seq_len, 1), float('-inf'), device=Q.device)
        
        # Procesar en tiles
        tile_size = min(self.tile_size, seq_len)
        
        for j in range(0, seq_len, tile_size):
            j_end = min(j + tile_size, seq_len)
            
            # Cargar tiles de K y V a SRAM (simulado)
            K_tile = K[:, :, j:j_end, :]  # (batch, nheads, tile, d)
            V_tile = V[:, :, j:j_end, :]  # (batch, nheads, tile, d)
            
            for i in range(0, seq_len, tile_size):
                i_end = min(i + tile_size, seq_len)
                
                # Q_i: (batch, nheads, tile, d), K_j^T: (tile, d)
                Q_i = Q[:, :, i:i_end, :]  # (batch, nheads, tile, d)
                
                # S_ij = Q_i @ K_j^T / sqrt(d)
                S_ij = torch.matmul(Q_i, K_tile.transpose(-2, -1)) * scale  # (batch, nheads, tile, tile)
                
                # Causal mask
                if causal and i_end > j:
                    mask = torch.tril(
                        torch.ones(tile_size, tile_size, device=Q.device),
                        diagonal=j_end - i - 1
                    ).unsqueeze(0).unsqueeze(0)  # (1, 1, tile, tile)
                    S_ij = S_ij.masked_fill(mask == 0, float('-inf'))
                
                # Online softmax update
                m_prev = M[:, :, i:i_end, :]  # (batch, nheads, tile, 1)
                m_ij = S_ij.max(dim=-1, keepdim=True)[0]  # (batch, nheads, tile, 1)
                
                # Escalar y acumular
                P_ij = torch.exp(S_ij - m_ij)  # (batch, nheads, tile, tile)
                
                # Update O
                O[:, :, i:i_end, :] = (
                    O[:, :, i:i_end, :] * torch.exp(m_prev - m_ij) +
                    torch.matmul(P_ij.float(), V_tile.float())
                )
                
                # Update L y M
                l_ij = P_ij.sum(dim=-1, keepdim=True)  # (batch, nheads, tile, 1)
                L[:, :, i:i_end, :] = (
                    L[:, :, i:i_end, :] * torch.exp(m_prev - m_ij) + l_ij
                )
                M[:, :, i:i_end, :] = torch.maximum(m_prev, m_ij)
        
        # Normalizar por L
        O = O / L
        
        return O


# Verificación: comparar con PyTorch nativo
def test_flash_attention():
    torch.manual_seed(42)
    batch, nheads, seq_len, d = 2, 8, 128, 64
    
    Q = torch.randn(batch, nheads, seq_len, d, device='cuda', dtype=torch.float16)
    K = torch.randn(batch, nheads, seq_len, d, device='cuda', dtype=torch.float16)
    V = torch.randn(batch, nheads, seq_len, d, device='cuda', dtype=torch.float16)
    
    # PyTorch nativo (SDPA)
    out_native = F.scaled_dot_product_attention(Q, K, V, is_causal=True)
    
    # FlashAttention educativo
    flash = FlashAttentionV1Edu(tile_size=32)
    out_flash = flash(Q, K, V, causal=True)
    
    # Verificar que coinciden
    diff = (out_native - out_flash).abs().max().item()
    print(f"Max diff between native and FlashAttention: {diff:.6f}")
    assert diff < 0.1, f"Outputs don't match: {diff}"
    print("✓ FlashAttention matches PyTorch SDPA")

# test_flash_attention()
```

### 5.3. Benchmark Comparativo

```python
import time

def benchmark_attention(seq_lengths, batch=1, nheads=16, d=128):
    """Benchmark atención estándar vs FlashAttention vs SDPA."""
    results = []
    
    for n in seq_lengths:
        Q = torch.randn(batch, nheads, n, d, device='cuda', dtype=torch.float16)
        K = Q.clone()
        V = Q.clone()
        
        # PyTorch nativo (SDPA con FlashAttention backend si disponible)
        torch.cuda.synchronize()
        t0 = time.time()
        for _ in range(10):
            out1 = F.scaled_dot_product_attention(Q, K, V, is_causal=True)
        torch.cuda.synchronize()
        t_sdpa = (time.time() - t0) / 10
        
        # Memoria peak
        torch.cuda.reset_peak_memory_stats()
        out2 = F.scaled_dot_product_attention(Q, K, V, is_causal=True)
        mem_peak = torch.cuda.max_memory_allocated() / 1024**2  # MB
        
        results.append({
            'seq_len': n,
            'sdpa_time_ms': t_sdpa * 1000,
            'mem_peak_mb': mem_peak,
            'flops': 2 * batch * nheads * n * n * d,  # QK^T + PV
            'gflops': 2 * batch * nheads * n * n * d / 1e9 / t_sdpa,
        })
    
    return results

# Ejemplo de resultados típicos en A100:
# seq_len | SDPA (ms) | FlashAttn (ms) | Speedup
# 1K      | 2.1       | 1.8            | 1.17x
# 4K      | 8.5       | 3.2            | 2.66x
# 16K     | 52        | 12             | 4.33x
# 64K     | 380       | 55             | 6.91x
# 256K    | 3200      | 280            | 11.4x
```

### 5.4. Integración con Transformers Library

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar modelo con FlashAttention 2 integrado
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3-8B-Instruct",
    torch_dtype=torch.float16,
    device_map="auto",
    attn_implementation="flash_attention_2",  # ← clave
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8B-Instruct")

# Generación con secuencias largas
prompt = "Explícame cómo funcionan las redes neuronales convolucionales"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# Con FlashAttention, generation es más rápido para long_context
outputs = model.generate(
    **inputs,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## 6. Cuándo Usar FlashAttention

| Escenario | Recomendación |
|-----------|--------------|
| **Training con secuencias largas** (>2K tokens) | ✅ Siempre FlashAttention |
| **Inferencia con batch pequeño, seq corta** (<512) | ⚠️ SDPA nativo puede ser igual de rápido |
| **Inferencia con secuencias largas** | ✅ FlashAttention 2/3 |
| **MicroVM 1vCPU** | ❌ No aplica — FlashAttention requiere GPU con tensor cores |
| **Edge deployment (CPU-only)** | ❌ Usar quantización + KV cache en vez |

### Limitaciones:

1. **Solo GPU** — Requiere CUDA con compute capability ≥ 7.0 (Volta+)
2. **Solo FP16/BF16** — No funciona en FP32
3. **No para CPU** — En CPU usar SDPA de PyTorch (`torch.nn.functional.scaled_dot_product_attention`)
4. **Instalación compleja** — `pip install flash-attn` requiere recompilar con CUDA correcto

## 7. Alternativas para CPU / Edge

Para nuestra MicroVM (1vCPU, sin GPU), FlashAttention no es aplicable directamente. Pero las ideas sí:

### 7.1. KV Cache + Paged Attention

```python
class PagedKVCache:
    """
    Paged Attention para CPU — gestión de memoria de KV cache
    como en vLLM, pero en CPU.
    
    Ideal para servidores de inferencia con muchas requests concurrentes.
    """
    
    def __init__(self, n_layers, n_heads, head_dim, max_tokens=4096):
        self.n_layers = n_layers
        self.n_heads = n_heads
        self.head_dim = head_dim
        self.max_tokens = max_tokens
        self.page_size = 16  # páginas de 16 tokens
        
        # KV cache paginado
        self.key_pages = [
            torch.zeros(n_heads, max_tokens // page_size, page_size, head_dim)
            for _ in range(n_layers)
        ]
        self.value_pages = [
            torch.zeros(n_heads, max_tokens // page_size, page_size, head_dim)
            for _ in range(n_layers)
        ]
        self.page_tables = [
            torch.zeros(n_heads, max_tokens // page_size, dtype=torch.long)
            for _ in range(n_layers)
        ]
    
    def get_kv(self, layer_idx, token_ids):
        """Obtener KV para tokens específicos usando page table."""
        pages = self.page_tables[layer_idx][token_ids]
        keys = self.key_pages[layer_idx][pages]
        values = self.value_pages[layer_idx][pages]
        return keys, values
```

### 7.2. Sparse Attention (CPU-friendly)

```python
def sparse_attention(Q, K, V, sparsity_pattern="sliding_window", window_size=128):
    """
    Atención esparsa que funciona en CPU.
    
    Patrones de sparsity:
    - sliding_window: cada token solo mira window_size anteriores
    - global_local: algunos tokens globales + ventana local
    - block_sparse: bloques de atención densa + resto cero
    """
    batch, nheads, seq_len, d = Q.shape
    
    if sparsity_pattern == "sliding_window":
        # Solo atención dentro de ventana
        O = torch.zeros_like(Q)
        for i in range(seq_len):
            start = max(0, i - window_size)
            O[:, :, i, :] = F.scaled_dot_product_attention(
                Q[:, :, i:i+1, :],
                K[:, :, start:i+1, :],
                V[:, :, start:i+1, :],
            ).squeeze(2)
        return O
    
    elif sparsity_pattern == "global_local":
        # Primeros 4 tokens son globales, resto es sliding window
        global_tokens = 4
        O = torch.zeros_like(Q)
        
        # Tokens globiales atienden a todos
        O[:, :, :global_tokens, :] = F.scaled_dot_product_attention(
            Q[:, :, :global_tokens, :], K, V
        )
        
        # Resto: sliding window + tokens globales
        for i in range(global_tokens, seq_len):
            local_start = max(global_tokens, i - window_size)
            context_k = torch.cat([
                K[:, :, :global_tokens, :],
                K[:, :, local_start:i+1, :]
            ], dim=2)
            context_v = torch.cat([
                V[:, :, :global_tokens, :],
                V[:, :, local_start:i+1, :]
            ], dim=2)
            O[:, :, i:i+1, :] = F.scaled_dot_product_attention(
                Q[:, :, i:i+1, :], context_k, context_v
            )
        
        return O
```

## 8. Conexión con el Stack Actual

### 8.1. ESIOS Dashboard

Para el dashboard ESIOS, FlashAttention no es directamente aplicable (no hay transformers en el frontend). Pero:

- **Backend predictions**: Si usamos transformers para forecasting energético, FlashAttention permite manejar ventanas temporales más largas (más horas de datos históricos)
- **ChromaDB embeddings**: Los embeddings de ChromaDB usan modelos de embedding que podrían beneficiarse de FlashAttention si se hacen inferencias batch grandes

### 8.2. MicroVM Deployment

En la MicroVM de 1vCPU/2GB:
- FlashAttention **no funciona** (no hay GPU)
- Pero las técnicas de **KV cache** y **sparse attention** sí son relevantes
- Combinar con **quantización INT8** (nota del 2026-06-16) para inferencia ligera

### 8.3. Integración con Skills Existentes

| Skill | Conexión |
|-------|----------|
| `state-space-models` | SSMs (Mamba) son alternativa a FlashAttention para secuencias largas — ambos resuelven O(n²) |
| `llama-cpp` | llama.cpp usa KV cache optimizado para CPU — complementa ideas de paged attention |
| `serving-llms-vllm` | vLLM usa PagedAttention — la misma idea que 7.1 |
| `quantization-model-compression` | FlashAttention + INT8 quantization = inferencia ultra-rápida |

## 9. Papers de Referencia

1. **FlashAttention v1**: Dao et al. (2022) — ["FlashAttention: Fast and Memory-Efficient Exact Attention"](https://arxiv.org/abs/2205.14135)
2. **FlashAttention v2**: Dao et al. (2023) — ["FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"](https://arxiv.org/abs/2307.08691)
3. **FlashAttention v3**: Chen et al. (2024) — ["FlashAttention-3: Fast and Accurate Attention with O(n²/b) Complexity"](https://arxiv.org/abs/2407.01003)
4. **PagedAttention**: Kwon et al. (2023) — ["Efficient Memory Management for Large Language Model Serving with PagedAttention"](https://arxiv.org/abs/2309.06180)
5. **Sparse Attention**: Child et al. (2019) — ["Generating Long Sequences with Sparse Transformers"](https://arxiv.org/abs/1904.10509)

## 10. Repositorios Útiles

- **FlashAttention**: https://github.com/Dao-AILab/flash-attention
- **xFormers** (alternativa con sparse attention): https://github.com/facebookresearch/xformers
- **vLLM** (PagedAttention en producción): https://github.com/vllm-project/vllm
- **Llama.cpp** (CPU inference con KV cache): https://github.com/ggerganov/llama.cpp

## 11. Resumen Técnico

| Aspecto | Detalle |
|---------|---------|
| **Problema** | Atención estándar: O(n²) memoria, bottleneck de bandwidth |
| **Solución v1** | Tiling + online softmax → O(n) memoria |
| **Mejora v2** | Bank conflict reduction + work partitioning → 2-3x más rápido |
| **Mejora v3** | Multi-block SM partitioning → 3x más rápido que v2 |
| **GPU requerida** | CUDA ≥ 7.0 (Volta+), FP16/BF16 |
| **CPU alternative** | Sparse attention, KV cache, sliding window |
| **Impacto real** | 4-10x speedup para secuencias >4K tokens en GPU |

---

**Tema propuesto para la siguiente sesión:** **Retrieval-Augmented Generation (RAG)** — conecta directamente con ChromaDB existente, es la evolución natural después de LoRA/PEFT (modelo fine-tuneado + RAG = mejor resultado), y tiene impacto directo en el sistema de búsqueda semántica de skills.
