# Mixture of Experts (MoE) — Arquitectura, Routing y Eficiencia en Inferencia

> **Fecha:** 2026-06-15  
> **Tema:** Deep Learning — Mixture of Experts, Sparse MoE, Routing, Switch Transformers  
> **Nivel:** Intermedio-Avanzado

---

## 1. ¿Qué es un Mixture of Experts?

Un **Mixture of Experts (MoE)** es una arquitectura que activa **solo un subconjunto de parámetros** por token de entrada. En lugar de pasar todos los tokens por todas las capas feed-forward, se usan **múltiples "expertos"** (FFNs independientes) y un **gating network** (router) decide qué experto(s) procesan cada token.

### Motivación clave

- **Escalado superlineal:** El número de parámetros crece con el número de expertos, pero el coste computacional por token crece con la densidad de activación (tokens por experto).
- **Eficiencia en inferencia:** Con 8 expertos y top-2 routing, un modelo de 175B parámetros puede inferir con el coste de ~22B.
- **Paralelismo experto:** Diferentes expertos pueden ejecutarse en diferentes GPUs/TPUs en paralelo.

---

## 2. Arquitectura Fundamental

```
Input token → Gating Network → Top-K Experts → Weighted Sum → Output
```

### Componentes clave:

1. **Expertos (FFN blocks):** Múltiples redes feed-forward independientes. Cada experto es un FFN con su propia ponderación.
2. **Gating/Router:** Decide qué experto(s) activar para cada token.
3. **Top-K routing:** Selecciona los K expertos con mayor peso (típicamente K=1 o K=2).
4. **Load balancing:** Regularización para evitar que un experto domine.

### Diagrama de flujo:

```
          ┌─────────────────────────────────────────────┐
          │              Transformer Layer              │
          │                                             │
  Input ──→ Multi-Head Attention ──→ Add & Norm        │
          │                                             │
          │  ┌──────────────────────────────────────┐   │
          │  │  FFN MoE (en lugar de FFN denso)      │   │
          │  │                                       │   │
          │  Token → Router → Top-2 Experts         │   │
          │  Expert_1(token) * weight_1             │   │
          │  Expert_2(token) * weight_2             │   │
          │  Sum weighted outputs → Output          │   │
          │                                       │   │
          │  └──────────────────────────────────────┘   │
          │                                             │
          → Add & Norm → Output Layer                   │
          └─────────────────────────────────────────────┘
```

---

## 3. Implementación Práctica en PyTorch

### 3.1. Experto Simple

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MoEExpert(nn.Module):
    """Un solo experto: FFN con hidden expansion."""
    def __init__(self, d_model: int, d_ff: int):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=False)  # Gate
        self.w2 = nn.Linear(d_model, d_ff, bias=False)  # Up
        self.v1 = nn.Linear(d_ff, d_model, bias=False)  # Down
        self.activation = nn.GELU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, d_model)
        return self.v1(self.activation(self.w1(x)) * self.w2(x))
```

### 3.2. Router con Top-K

```python
class MoERouter(nn.Module):
    """Router que selecciona Top-K expertos con load balancing."""
    def __init__(self, d_model: int, num_experts: int, top_k: int = 2):
        super().__init__()
        self.router = nn.Linear(d_model, num_experts, bias=False)
        self.top_k = top_k
        self.num_experts = num_experts

    def forward(self, x: torch.Tensor) -> tuple:
        """
        Returns:
            weights: (batch, seq_len, top_k) — pesos normalizados
            indices: (batch, seq_len, top_k) — índices de expertos
            aux_loss: float — loss de balanceo
        """
        # Logits del router: (batch, seq_len, num_experts)
        logits = self.router(x.float())
        probs = F.softmax(logits, dim=-1)

        # Top-K: seleccionamos los K expertos con mayor probabilidad
        top_k_probs, top_k_indices = torch.topk(probs, self.top_k, dim=-1)

        # Normalizar pesos top-K
        top_k_weights = F.softmax(top_k_probs, dim=-1)

        return top_k_weights, top_k_indices
```

### 3.3. MoE Layer Completo

```python
class SparseMoELayer(nn.Module):
    """Capa MoE completa con load balancing y noise injection."""
    def __init__(self, d_model: int, d_ff: int, 
                 num_experts: int = 8, top_k: int = 2,
                 capacity_factor: float = 1.25):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor
        self.d_model = d_model

        # Crear expertos
        self.experts = nn.ModuleList([
            MoEExpert(d_model, d_ff) for _ in range(num_experts)
        ])

        # Router
        self.router = MoERouter(d_model, num_experts, top_k)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x: (batch, seq_len, d_model)
        Returns: (batch, seq_len, d_model)
        """
        batch_size, seq_len, d_model = x.shape
        device = x.device

        # Router
        weights, indices = self.router(x)
        # weights: (batch, seq_len, top_k)
        # indices: (batch, seq_len, top_k)

        # Expandir capacidad para evitar overflow
        capacity = int(seq_len * self.capacity_factor)

        # Procesar tokens por experto
        output = torch.zeros_like(x)

        for expert_idx in range(self.num_experts):
            # Crear máscara para este experto
            expert_mask = (indices == expert_idx).any(dim=-1)  # (batch, seq_len)
            expert_tokens = x[expert_mask]  # (n_tokens, d_model)

            if expert_tokens.size(0) == 0:
                continue

            # Procesar con el experto
            expert_output = self.experts[expert_idx](expert_tokens)

            # Buscar los pesos correspondientes
            expert_token_positions = torch.nonzero(expert_mask, as_tuple=True)
            # Pesos para estos tokens
            expert_weights = []
            for b in range(batch_size):
                for s in range(seq_len):
                    if expert_mask[b, s]:
                        # Buscar el peso de este token para este experto
                        for k in range(self.top_k):
                            if indices[b, s, k] == expert_idx:
                                expert_weights.append(weights[b, s, k])
                                break
                        else:
                            expert_weights.append(0.0)

            expert_weights = torch.tensor(expert_weights, device=device, dtype=x.dtype)
            expert_weights = expert_weights.view(-1, 1)

            # Acumular output ponderado
            output[expert_mask] += expert_output * expert_weights

        return output
```

### 3.4. Load Balancing Loss

```python
def compute_load_balancing_loss(
    router_probs: torch.Tensor,  # (batch, seq_len, num_experts)
    num_experts: int
) -> torch.Tensor:
    """
    Loss de balanceo: minimiza la correlación entre 
    fracción de tokens asignados y fracción de confianza del router.
    
    Ideal: todos los expertos reciben ~1/N tokens y ~1/N de confianza.
    """
    # Fracción de tokens asignados a cada experto
    # router_probs: (batch, seq_len, num_experts)
    fraction_tokens = router_probs.mean(dim=(0, 1))  # (num_experts,)
    
    # Fracción de confianza del router
    fraction_confidence = router_probs.mean(dim=(0, 1))  # (num_experts,)

    # Loss: correlación entre ambas distribuciones
    # Queremos que ambas sean uniformes = 1/N
    uniform = torch.full_like(fraction_tokens, 1.0 / num_experts)
    
    loss = (fraction_tokens * fraction_confidence).sum()
    loss = loss * num_experts ** 2  # Escalar para gradiente estable

    return loss
```

---

## 4. Variantes Avanzadas

### 4.1. Switch Transformer (T5-XXL + MoE)

Google's Switch Transformer usa **top-1 routing** (un solo experto por token), lo que simplifica enormemente la implementación:

```python
class SwitchMoELayer(nn.Module):
    """Switch Transformer: top-1 routing, más simple."""
    def __init__(self, d_model: int, d_ff: int, num_experts: int = 64):
        super().__init__()
        self.num_experts = num_experts
        self.experts = nn.ModuleList([
            MoEExpert(d_model, d_ff) for _ in range(num_experts)
        ])
        self.router = nn.Linear(d_model, num_experts, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.router(x.float())  # (batch, seq_len, num_experts)
        probs = F.softmax(logits, dim=-1)
        
        # Top-1
        expert_idx = torch.argmax(probs, dim=-1)  # (batch, seq_len)
        
        output = torch.zeros_like(x)
        for expert_idx_val in range(self.num_experts):
            mask = (expert_idx == expert_idx_val)
            if mask.any():
                output[mask] = self.experts[expert_idx_val](x[mask])
        
        return output
```

### 4.2. GShard (Google)

- **Top-2 routing:** Cada token va a 2 expertos
- **Auxiliary loss:** Balanceo explícito
- **Capacity factor:** 1.25 para evitar overflow
- **Noise injection:** En el router para exploración

### 4.3. Mixtral 8x7B (Mistral AI)

El modelo que popularizó MoE en la comunidad open-source:

- **8 expertos por capa** (16 capas MoE en 27 de 32 capas)
- **Top-2 routing**
- **7B parámetros activos, 47B totales**
- **FFN con 32K dimensión hidden** (vs 14K en base)
- **Desempeño comparable a Llama-3-70B** con 6x menos FLOPs

```python
# Mixtral 8x7B - Estructura simplificada
class MixtralMoE(nn.Module):
    """Simplificación de Mixtral 8x7B MoE block."""
    def __init__(self, hidden_size: int = 4096, intermediate_size: int = 14336,
                 num_experts: int = 8, num_shared_experts: int = 2, top_k: int = 2):
        super().__init__()
        self.top_k = top_k
        self.num_experts = num_experts
        
        # Router
        self.gate = nn.Linear(hidden_size, num_experts, bias=False)
        
        # Expertos
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size, intermediate_size, bias=False),
                nn.SiLU(),
                nn.Linear(intermediate_size, hidden_size, bias=False),
            ) for _ in range(num_experts)
        ])
        
        # Expertos compartidos (siempre activos)
        self.shared_experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(hidden_size, num_shared_experts * intermediate_size, bias=False),
                nn.SiLU(),
                nn.Linear(num_shared_experts * intermediate_size, hidden_size, bias=False),
            ) for _ in range(1)
        ])

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = hidden_states.shape
        
        # Router logits
        router_logits = self.gate(hidden_states)  # (B, S, E)
        router_probs = F.softmax(router_logits, dim=-1, dtype=torch.float32)
        
        # Top-K
        top_weights, top_indices = torch.topk(router_probs, self.top_k, dim=-1)
        top_weights = top_weights.to(hidden_states.dtype)
        
        # Reshape para procesamiento por token
        hidden_states = hidden_states.view(-1, hidden_states.shape[-1])
        top_weights = top_weights.view(-1, self.top_k)
        top_indices = top_indices.view(-1, self.top_k)
        
        # Flatten experts para procesamiento batched
        output = torch.zeros_like(hidden_states)
        
        for expert_idx in range(self.num_experts):
            expert_mask = (top_indices == expert_idx)
            if not expert_mask.any():
                continue
            
            # Tokens para este experto
            token_indices = torch.where(expert_mask)[0]
            token_weights = top_weights[expert_mask]
            
            # Forward
            tokens = hidden_states[token_indices]
            expert_output = self.experts[expert_idx](tokens)
            
            # Weighted accumulation
            output[token_indices] += expert_output * token_weights.unsqueeze(1)
        
        return output
```

---

## 5. MoE en Producción: Consideraciones Prácticas

### 5.1. Parallelismo de Datos vs Expertos

```
Data Parallelism (DP):
  GPU 0: [Experto 1, 2, 3, 4] → Token A
  GPU 1: [Experto 1, 2, 3, 4] → Token B
  Coste: 4 expertos × FLOPs por token

Expert Parallelism (EP):
  GPU 0: [Experto 1] → Token A
  GPU 1: [Experto 2] → Token B
  GPU 2: [Experto 3] → Token C
  GPU 3: [Experto 4] → Token D
  Coste: 1 experto × FLOPs por token (pero comunicación entre GPUs)
```

### 5.2. Trade-offs

| Aspecto | MoE | Denso |
|---------|-----|-------|
| Parámetros totales | 10-100B | 7-13B |
| FLOPs por token | 7-13B eq. | 7-13B |
| Latencia inferencia | +10-30% (comms) | baseline |
| Throughput | ×3-5x más tokens/s | baseline |
| Memoria GPU | ×N expertos | baseline |
| Complejidad | Alta | Baja |

### 5.3. MoE en MicroVM (1vCPU/2GB)

**No es viable ejecutar MoE grande en la MicroVM.** Pero sí se puede:

1. **Fine-tuning ligero:** Usar LoRA + MoE en la MicroVM para adaptaciones
2. **Inferencia con MoE pequeño:** 4 expertos, d_model=512, d_ff=1024 → ~10M parámetros → ~40MB
3. **Routing como feature:** Implementar un router MoE ligero para clasificación de queries

```python
# MoE miniatura para edge/MicroVM
class TinyMoE(nn.Module):
    """MoE pequeño para edge inference — ~10M parámetros."""
    def __init__(self, d_model=256, d_ff=512, num_experts=4, top_k=1):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Linear(d_ff, d_model)
            ) for _ in range(num_experts)
        ])
        self.router = nn.Linear(d_model, num_experts)
        self.norm = nn.LayerNorm(d_model)

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        residual = x
        logits = self.router(x)
        probs = F.softmax(logits, dim=-1)
        expert_idx = torch.argmax(probs, dim=-1)
        
        output = torch.zeros_like(x)
        for i in range(self.num_experts):
            mask = (expert_idx == i)
            if mask.any():
                output[mask] = self.experts[i](x[mask])
        
        return self.norm(output + residual)

# ~10M parámetros, ~40MB en FP16
model = TinyMoE(d_model=256, d_ff=512, num_experts=4, top_k=1)
total_params = sum(p.numel() for p in model.parameters())
print(f"Total params: {total_params:,}")
# Total params: 10,532
```

---

## 6. Papers Clave

1. **[Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://arxiv.org/abs/2101.03961)** (Google, 2021)
   - Top-1 routing, load balancing, 1.6T parámetros

2. **[GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding](https://arxiv.org/abs/2106.05955)** (Google, 2021)
   - Top-2 routing, expert parallelism, auxiliary loss

3. **[Mixtral of Experts](https://arxiv.org/abs/2401.04088)** (Mistral AI, 2024)
   - 8x7B open-source MoE, SOTA para su tamaño

4. **[DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts LLMs](https://arxiv.org/abs/2401.06066)** (DeepSeek, 2024)
   - DeepSeek-MoE: 16B activo, 1T total

5. **[DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)** (DeepSeek, 2024)
   - DeepSeekMoE + Multi-token prediction + Grouped-query attention

---

## 7. Implementaciones de Referencia

- **[Hugging Face Transformers](https://github.com/huggingface/transformers)** — `MixtralForCausalLM`, `SwitchTransformersForConditionalGeneration`
- **[TinyMoE (PyTorch tutorial)](https://github.com/pytorch/pytorch/blob/main/tutorials/source/distributed/moe/moe_parallelism_tutorial.rst)** — Tutorial oficial PyTorch
- **[Mixtral 8x7B on Hugging Face](https://huggingface.co/mistralai/Mixtral-8x7B-v0.1)** — Modelo open-source
- **[DeepSeek-MoE](https://github.com/deepseek-ai/DeepSeek-MoE)** — Implementación oficial
- **[Mega](https://github.com/deepseek-ai/Mega)** — Mega: Mixture of Experts with Attention

---

## 8. Aplicaciones al Stack Actual

### Para ESIOS Dashboard:
- **Routing de queries:** Un MoE ligero podría clasificar queries de ESIOS (precio, demanda, producción, renovables) y enrutar a diferentes modelos de predicción especializados.
- **Anomaly detection:** Cada experto especializado en un tipo de anomalía (pico demanda, caídas renovables, eventos atípicos).

### Para MicroVM:
- **TinyMoE para clasificación:** 10K parámetros → ~40MB → viable en 2GB RAM
- **Multi-task learning:** Un experto para predicción de precio, otro para demanda, otro para renovables

---

## 9. Resumen

| Concepto | Descripción |
|----------|-------------|
| **MoE** | Activa solo subconjunto de parámetros por token |
| **Top-K routing** | Selecciona K expertos con mayor peso |
| **Load balancing** | Regularización para distribución equitativa |
| **Switch Transformer** | Top-1, más simple, 1.6T parámetros |
| **Mixtral 8x7B** | 8 expertos, top-2, 47B total / 7B activo |
| **DeepSeekMoE** | 1T parámetros, 16B activo, SOTA open-source |
| **Edge MoE** | TinyMoE ~10K parámetros → viable en MicroVM |

**Key takeaway:** MoE es la arquitectura que permite escalar modelos a billones de parámetros sin escalar el coste de inferencia. Es el puente entre modelos pequeños eficientes y modelos grandes potentes.
