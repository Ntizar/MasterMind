# PEFT Methods Inventory — Referencia Rápida

## Métodos Implementados en PEFT v0.19.1

### Weight Decomposition (Adaptadores de Matriz)

| Método | Paper | Parámetros | Key Idea |
|--------|-------|-----------|----------|
| **LoRA** | arxiv 2106.09685 | r×(m+n) | Producto de dos matrices de bajo rango |
| **DoRA** | arxiv 2402.09353 | r×(m+n) + m+n | Descompone pesos en magnitud + dirección |
| **VeRA** | arxiv 2402.12308 | 2k (vectores) | Matrices aleatorias fijas + 2 vectores escalares |
| **AdaLoRA** | arxiv 2303.10512 | Variable | Ranks dinámicos por capa durante training |
| **OLoRA** | arxiv 2406.11810 | r×(m+n) | Outlier-aware initialization |
| **CorDA** | arxiv 2406.11810 | r×(m+n) | Correlation-based decomposition |
| **EVA** | PEFT 0.19 | r×(m+n) | Eigenvector-based initialization |
| **PiSSA** | arxiv 2404.02948 | r×(m+n) | SVD principal para initialization |
| **LoFTQ** | arxiv 2310.08659 | r×(m+n) | Fine-tuning-free quantization + LoRA |

### Estructurales

| Método | Paper | Parámetros | Key Idea |
|--------|-------|-----------|----------|
| **IA³** | arxiv 2205.05638 | 3n | Infusión en activations (no weights) |
| **Adapters** | arxiv 1902.00751 | ~12% | Capas modulares insertadas entre capas |
| **Adaption Prompt** | — | n×d | Prompts adaptativos para LLMs |

### Prompt/Prefix

| Método | Parámetros | Key Idea |
|--------|-----------|----------|
| **P-Tuning v2** | n×d | Soft prompts continuos |
| **Prefix Tuning** | n×d×L | Prefixes en cada capa |
| **Prompt Tuning** | n×d | Solo embeddings entrenables |
| **Multitask Prompt** | n×d×T | Múltiples prompts para multitask |

### Avanzados

| Método | Key Idea |
|--------|----------|
| **BOFT** | Basis Orthogonal Fourier Transform |
| **FourierFT** | Adaptación en dominio de frecuencia |
| **HRA** | Hierarchical Reparameterization |
| **LNTuning** | Solo LayerNorm entrenable |
| **LoHa** | Hadamard factored LoRA |
| **LoKr** | Kronecker factored LoRA |
| **aLoRA** | Asynchronous LoRA |

## Inicializaciones de LoRA

| Inicialización | Descripción | Cuándo usar |
|---------------|-------------|-------------|
| `gaussian` (default) | Normal N(0, 0.01) | General purpose |
| `pissa` | SVD principal de pesos originales | Mejor convergencia con ranks bajos |
| `olora` | Outlier-aware SVD | Cuando hay outliers en activations |
| `corda` | Correlation-based | Similar a PiSSA pero con correlación |
| `eva` | Eigenvector-based | Alternativa a PiSSA |
| `loftq` | Fine-tuning-free quant | Para QLoRA pipelines |
| `orthogonal` | Matriz ortogonal | Estabilidad numérica |

## Configurations Recomendadas

### Sweet Spot General (LLMs 3B-13B)
```python
LoraConfig(
    r=16,
    lora_alpha=32,
    use_rslora=True,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    init_lora_weights="pissa",
)
```

### Ultra-Eficiente (MicroVM 2GB RAM)
```python
LoraConfig(
    r=8,
    lora_alpha=16,
    use_rslora=True,
    target_modules=["v_proj", "up_proj", "down_proj"],
    lora_dropout=0.0,
    init_lora_weights="pissa",
)
```

### Máxima Calidad (cuando VRAM permite)
```python
LoraConfig(
    r=64,
    lora_alpha=64,
    use_rslora=True,
    target_modules="all-linear",
    lora_dropout=0.05,
    init_lora_weights="pissa",
)
```
