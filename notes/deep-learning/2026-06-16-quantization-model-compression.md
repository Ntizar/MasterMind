# Quantización y Compresión de Modelos — De FP32 a INT4 en la Práctica

> **Fecha:** 2026-06-16
> **Tema:** Deep Learning — Quantization, Model Compression, Edge Deployment
> **Nivel:** Intermedio
> **Contexto:** MicroVM 1vCPU/2GB/20GB — necesidad crítica de ejecutar modelos ligeros

---

## 1. ¿Por qué cuantizar?

Los modelos LLM modernos tienen un coste de memoria brutal:

| Formato | Bytes por parámetro | Llama 3 8B | Llama 3 70B |
|---------|-------------------|-----------|------------|
| FP32 | 4 | 32 GB | 280 GB |
| FP16 | 2 | 16 GB | 140 GB |
| BF16 | 2 | 16 GB | 140 GB |
| **INT8** | **1** | **8 GB** | **70 GB** |
| **INT4** | **0.5** | **4 GB** | **35 GB** |
| **NF4** | **0.5** | **~4 GB** | **~35 GB** |

En una MicroVM de 2 GB RAM, incluso un modelo de 7B en INT4 es inviable. Pero modelos pequeños (1B-3B) en INT4/NF4 **sí caben**.

### Casos de uso en el stack:
- **LLM local en MicroVM**: ejecutar un modelo pequeño para tareas de clasificación, extracción, resumen
- **ONNX Runtime**: cuantizar modelos de CV (YOLO, segmentación) para inferencia rápida
- **Embeddings**: cuantizar embedding models para búsqueda semántica (ChromaDB)
- **Edge deployment**: modelos de detección de tráfico, clasificación de imágenes

---

## 2. Tipos de Cuantización

### 2.1 PTQ (Post-Training Quantization)

Cuantizas el modelo **ya entrenado**, sin reentrenamiento.

```python
# Ejemplo con PyTorch — PTQ con torch.ao.quantization
import torch
import torch.quantization as quantization

# 1. Modelo FP32 original
model = torch.hub.load('microsoft/DeBERTa', 'microsoft/deberta-v3-base')
model.eval()

# 2. Configurar cuantización
model.qconfig = quantization.get_default_qconfig('fbgemm')  # x86 CPU optimized
quantization.prepare(model, inplace=True)

# 3. Calibrar con datos de referencia (100-500 muestras)
def calibrate(dataloader):
    model.eval()
    with torch.no_grad():
        for inputs, labels in datataloader:
            model(inputs)

calibrate(calibration_dataset)

# 4. Cuantizar
quantization.convert(model, inplace=True)

# 5. Guardar modelo cuantizado
torch.save(model, 'model_int8.pt')
```

**Ventaja:** Rápido, sin necesidad de reentrenar.
**Desventaja:** Pérdida de precisión moderada (1-3%).

### 2.2 QAT (Quantization-Aware Training)

Entrenas el modelo **simulando** cuantización durante el training.

```python
# QAT con PyTorch — simula quantización durante training
model = MyModel()

# Configurar qconfig para cada submódulo
model.qconfig = quantization.QConfigDynamic(
    activation=torch.quantization.default_dynamic_qfunc,
    weight=torch.quantization.default_per_channel_weight_qfunc
)

# Training normal, pero con ops cuantizadas simuladas
for epoch in range(num_epochs):
    for inputs, targets in train_loader:
        # Las operaciones se cuantizan/dequantizan en forward
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

# Convertir a modelo cuantizado real
quantization.convert(model, inplace=True)
```

**Ventaja:** Menor pérdida de precisión (0.5-1%).
**Desventaja:** Requiere reentrenar (coste computacional).

### 2.3 AWQ (Activation-Aware Weight Quantization)

Técnica moderna que identifica **weights importantes** y las preserva en FP16.

```python
# AWQ con transformers library
from autoawq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model_path = "microsoft/Phi-3-mini-4k-instruct"

# 1. Cargar modelo
model = AutoAWQForCausalLM.from_pretrained(
    model_path,
    device_map="cpu",  # o "cuda"
    low_cpu_mem_usage=True
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# 2. Configurar datos de calibración (4 samples, 512 tokens)
calibration_data = [
    "David, explain quantum computing",
    "¿Cómo funciona el mercado eléctrico español?",
    # ... 2 más
]

# 3. Cuantizar a INT4
model.quantize(tokenizer, config={"q_bit": 4, "exponent_format": "awq"})

# 4. Guardar
model.save_quantized("./phi3-mini-int4")
tokenizer.save_pretrained("./phi3-mini-int4")
```

**Resultado:** Modelo INT4 con calidad cercana a FP16.
**Paper:** [AWQ (2023)](https://arxiv.org/abs/2306.00978)

### 2.4 GGUF / llama.cpp Format

El formato **de facto** para ejecutar LLMs en CPU.

```bash
# Convertir un modelo HuggingFace a GGUF
# 1. Instalar llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# 2. Convertir (ejemplo con Q4_K_M — quantización mixta)
python convert-hf-to-gguf.py <model_dir> --outtype f16

# 3. Cuantizar
llama-quantize <model_dir>/ggml-model-f16.gguf <model_dir>/ggml-model-q4_k_m.gguf Q4_K_M

# 4. Inferencia en CPU
./llama-cli -m <model_dir>/ggml-model-q4_k_m.gguf \
    -p "David, what's the difference between PTQ and QAT?" \
    -n 256 -t 2
```

**Quantization schemes en llama.cpp:**
- `Q4_0`: INT4 simple
- `Q4_K_M`: Mezcla INT4+INT6 (recomendado, mejor calidad)
- `Q5_K_M`: INT5+INT6 (casi FP16 quality)
- `Q8_0`: INT8 (mínima pérdida)

---

## 3. Compresión de Modelos de Visión (ONNX)

Para modelos de CV (YOLO, segmentación), ONNX Runtime con cuantización INT8 es ideal:

```python
import onnx
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType

# 1. Modelo ONNX exportado (desde PyTorch/TensorFlow)
model = onnx.load("yolov8n.onnx")

# 2. Cuantización dinámica (solo weights, activations en FP32)
quantize_dynamic(
    "yolov8n.onnx",
    "yolov8n-int8.onnx",
    weight_type=QuantType.QUInt8
)

# 3. Inferencia con ONNX Runtime (automáticamente usa INT8)
session = ort.InferenceSession("yolov8n-int8.onnx")
# En CPU con NNAPI/NEON: 2-3x más rápido que FP32
```

### Comparativa de rendimiento ONNX Runtime:

| Modelo | FP32 (ms) | INT8 (ms) | Reducción |
|--------|-----------|-----------|-----------|
| YOLOv8n | 45 | 18 | 60% |
| ResNet50 | 35 | 14 | 60% |
| BERT-base | 28 | 12 | 57% |

---

## 4. LoRA / PEFT para Modelos Pequeños

Parameter-Efficient Fine-Tuning: ajustar solo un 1% de parámetros.

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

# 1. Configurar cuantización INT4 con bitsandbytes
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",  # NormalFloat4 (mejor que INT4)
    bnb_4bit_compute_dtype=torch.float16
)

# 2. Cargar modelo cuantizado
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    quantization_config=bnb_config,
    device_map="auto"
)

# 3. Añadir LoRA adapters (solo ~0.5% parámetros adicionales)
lora_config = LoraConfig(
    r=16,                    # Rank de LoRA
    lora_alpha=32,           # Scaling
    target_modules=["q_proj", "v_proj"],  # Solo attention layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# 4. Entrenar solo los LoRA adapters
# Los parámetros del modelo base están congelados
model.print_trainable_parameters()
# "trainable params: 393,216 || all params: 7,609,812,480 || 0.005%"
```

**Resultado:** Fine-tuning de un modelo 7B con ~2 GB RAM.

---

## 5. Pipeline Práctico para MicroVM

### Estrategia: modelo pequeño + cuantización agresiva

```python
"""
Pipeline de inferencia cuantizada para MicroVM 1vCPU/2GB
Modelo: Qwen2.5-1.5B (pequeño, bueno, chino-optimizado)
Formato: GGUF Q4_K_M (~1 GB)
"""

import subprocess
import json

class QuantizedLLM:
    """Wrapper mínimo para llama.cpp en MicroVM"""
    
    def __init__(self, model_path, n_threads=1):
        self.model_path = model_path
        self.n_threads = n_threads  # 1 thread para 1vCPU
        
    def generate(self, prompt, max_tokens=256, temperature=0.7):
        """Inferencia via llama.cpp CLI"""
        cmd = [
            './llama-cli',
            '-m', self.model_path,
            '-p', prompt,
            '-n', str(max_tokens),
            '-t', str(self.n_threads),
            '--temp', str(temperature),
            '-ngl', '0',  # No GPU layers
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.stdout
    
    def classify(self, text, categories):
        """Clasificación con prompt engineering"""
        cat_str = ", ".join(categories)
        prompt = f"""Clasifica el siguiente texto en una de estas categorías: {cat_str}

Texto: {text}

Respuesta solo con el nombre de la categoría:"""
        
        response = self.generate(prompt, max_tokens=16, temperature=0.1)
        return response.strip()

# Uso:
# llm = QuantizedLLM("./qwen2.5-1.5b-instruct-q4_k_m.gguf")
# result = llm.classify(
#     "La demanda eléctrica ha subido un 15% respecto a la hora anterior",
#     ["energia", "clima", "economia", "politica"]
# )
# print(result)  # → energia
```

### Estimación de recursos:

| Modelo | Formato | Tamaño RAM | Inferencia (ms/token) |
|--------|---------|-----------|---------------------|
| Qwen2.5-1.5B | GGUF Q4_K_M | ~1.2 GB | ~80-120 (CPU) |
| Qwen2.5-0.5B | GGUF Q4_K_M | ~0.5 GB | ~40-60 (CPU) |
| Phi-3-mini-3.8B | GGUF Q4_K_M | ~2.5 GB | ~150-200 (CPU) |
| TinyLlama-1.1B | GGUF Q8_0 | ~1.2 GB | ~60-90 (CPU) |

**Recomendación para MicroVM:** Qwen2.5-1.5B o Qwen2.5-0.5B en GGUF Q4_K_M.

---

## 6. Referencias Clave

### Papers:
- **AWQ** (2023) — [Activation-Aware Weight Quantization](https://arxiv.org/abs/2306.00978)
- **GPTQ** (2022) — [Post-Training Quantization with GPTQ](https://arxiv.org/abs/2210.17323)
- **LLM.int8()** (2022) — [LLM.int8() — Eight-bit Quantization](https://arxiv.org/abs/2208.07339)
- **NF4** (2023) — [QLoRA: Training a Quantized LLM](https://arxiv.org/abs/2305.14314)
- **GGUF** (2023) — [llama.cpp format](https://github.com/ggerganov/ggml/blob/master/docs/llamafile/gguf.md)

### Repositorios:
- [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) — Inferencia LLM en CPU
- [casper-hansen/AutoAWQ](https://github.com/casper-hansen/AutoAWQ) — AWQ quantization
- [huggingface/optimum](https://github.com/huggingface/optimum) — ONNX quantization
- [huggingface/peft](https://github.com/huggingface/peft) — LoRA/PEFT
- [huggingface/bitsandbytes](https://github.com/bitsandbytes-foundation/bitsandbytes) — 4bit/8bit quantization

### Herramientas del ecosistema:
- `ollama` — Docker-like para LLMs cuantizados (ya disponible en muchas setups)
- `mlx` — Apple Silicon optimized, pero útil para entender quantization schemes
- `onnxruntime` — Runtime optimizado con soporte INT8 nativo

---

## 7. Conexión con el Stack Actual

### Aplicaciones inmediatas:

1. **ChromaDB embeddings** → cuantizar embedding models para reducir memoria
2. **Clasificación de texto** → Qwen2.5-1.5B-GGUF para categorización automática
3. **Modelos de CV** → YOLOv8n INT8 para detección de tráfico desde satélite
4. **API de NaN** → servir modelos cuantizados como endpoints ligeros

### Skill potencial:
- `quantization-edge-deploy` — Procedimiento para cuantizar y desplegar modelos en MicroVM
- `gguf-pipeline` — Pipeline completo HF → GGUF → llama.cpp

---

## 8. Pitfalls

- **GGUF no funciona bien con threads > 1** en 1vCPU — siempre usar `-t 1`
- **Q4_K_M es el sweet spot** — Q3 es demasiado agresivo, Q5 apenas ahorra más
- **ONNX INT8 en CPU** requiere soporte NEON (ARM) o AVX2 (x86) — verificar con `lscpu`
- **LoRA + 4bit** requiere `bitsandbytes` — no siempre compatible con todas las architectures
- **Calibración PTQ** necesita datos representativos — si los datos de calibración no representan la distribución real, la precisión cae un 5-10%
