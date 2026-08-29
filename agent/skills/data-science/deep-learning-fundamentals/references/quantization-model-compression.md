# Quantización y Compresión de Modelos — De FP32 a INT4 en la Práctica

> **Fecha:** 2026-06-16
> **Tema:** Quantization, Model Compression, Edge Deployment

## 1. ¿Por qué cuantizar?

| Formato | Bytes/param | Llama 3 8B | Llama 3 70B |
|---------|------------|-----------|------------|
| FP32 | 4 | 32 GB | 280 GB |
| FP16/BF16 | 2 | 16 GB | 140 GB |
| **INT8** | **1** | **8 GB** | **70 GB** |
| **INT4** | **0.5** | **4 GB** | **35 GB** |
| **NF4** | **0.5** | **~4 GB** | **~35 GB** |

En MicroVM 1vCPU/2GB: modelos 1B-3B en INT4/NF4 son viables.

## 2. Tipos de Cuantización

### PTQ (Post-Training Quantization)
Cuantizar modelo ya entrenado, sin reentrenamiento. 1-3% pérdida de precisión.

```python
import torch
import torch.quantization as quantization

model = torch.hub.load('microsoft/DeBERTa', 'microsoft/deberta-v3-base')
model.eval()
model.qconfig = quantization.get_default_qconfig('fbgemm')
quantization.prepare(model, inplace=True)

# Calibrar con 100-500 muestras
for inputs, labels in calibration_dataloader:
    model(inputs)

quantization.convert(model, inplace=True)
torch.save(model, 'model_int8.pt')
```

### QAT (Quantization-Aware Training)
Simular cuantización durante training. 0.5-1% pérdida, pero requiere reentrenar.

### AWQ (Activation-Aware Weight Quantization)
Identifica weights importantes y las preserva en FP16. INT4 con calidad cercana a FP16.

```python
from autoawq import AutoAWQForCausalLM
from transformers import AutoTokenizer

model = AutoAWQForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", device_map="cpu"
)
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

calibration_data = ["David, explain quantum computing", "...", "...", "..."]
model.quantize(tokenizer, config={"q_bit": 4, "exponent_format": "awq"})
model.save_quantized("./phi3-mini-int4")
```

### GGUF / llama.cpp
Formato de facto para LLMs en CPU.

```bash
# Convertir HF → GGUF
python convert-hf-to-gguf.py <model_dir> --outtype f16

# Cuantizar (Q4_K_M = sweet spot)
llama-quantize <model_dir>/ggml-model-f16.gguf <model_dir>/ggml-model-q4_k_m.gguf Q4_K_M

# Inferencia CPU
./llama-cli -m <model_dir>/ggml-model-q4_k_m.gguf \
    -p "David, what's PTQ?" -n 256 -t 1 -ngl 0
```

**Schemes:** `Q4_0` (simple), `Q4_K_M` (recomendado), `Q5_K_M` (casi FP16), `Q8_0` (mínima pérdida).

## 3. Compresión CV (ONNX)

```python
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    "yolov8n.onnx",
    "yolov8n-int8.onnx",
    weight_type=QuantType.QUInt8
)
# En CPU con NEON/AVX2: 2-3x más rápido que FP32
```

## 4. LoRA / PEFT

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16
)

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    quantization_config=bnb_config, device_map="auto"
)

lora_config = LoraConfig(
    r=16, lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05, bias="none"
)
model = get_peft_model(model, lora_config)
# trainable params: ~0.5% del total
```

## 5. Pipeline para MicroVM

```python
class QuantizedLLM:
    """Wrapper mínimo para llama.cpp en MicroVM"""
    def __init__(self, model_path, n_threads=1):
        self.model_path = model_path
        self.n_threads = n_threads

    def generate(self, prompt, max_tokens=256, temperature=0.7):
        import subprocess
        cmd = ['./llama-cli', '-m', self.model_path, '-p', prompt,
               '-n', str(max_tokens), '-t', str(self.n_threads),
               '--temp', str(temperature), '-ngl', '0']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.stdout

    def classify(self, text, categories):
        cat_str = ", ".join(categories)
        prompt = f"Clasifica en: {cat_str}\nTexto: {text}\nCategoría:"
        return self.generate(prompt, max_tokens=16, temperature=0.1).strip()
```

**Estimación de recursos (1vCPU):**

| Modelo | Formato | RAM | ms/token |
|--------|---------|-----|----------|
| Qwen2.5-1.5B | GGUF Q4_K_M | ~1.2 GB | ~80-120 |
| Qwen2.5-0.5B | GGUF Q4_K_M | ~0.5 GB | ~40-60 |
| TinyLlama-1.1B | GGUF Q8_0 | ~1.2 GB | ~60-90 |

## 6. Conexión con el Stack

- **ChromaDB embeddings** → cuantizar embedding models
- **Clasificación de texto** → Qwen2.5-1.5B-GGUF para categorización
- **Modelos de CV** → YOLOv8n INT8 para detección de tráfico
- **API de NaN** → servir modelos cuantizados como endpoints ligeros

## 7. Pitfalls

- GGUF no funciona bien con threads > 1 en 1vCPU — siempre `-t 1`
- Q4_K_M es el sweet spot — Q3 es demasiado agresivo, Q5 apenas ahorra más
- ONNX INT8 en CPU requiere NEON (ARM) o AVX2 (x86) — verificar con `lscpu`
- LoRA + 4bit requiere `bitsandbytes` — no compatible con todas las architectures
- Calibración PTQ necesita datos representativos — si no representan la distribución real, precisión cae 5-10%

## Referencias

- **AWQ (2023):** arXiv:2306.00978 — Activation-Aware Weight Quantization
- **GPTQ (2022):** arXiv:2210.17323 — Post-Training Quantization
- **LLM.int8() (2022):** arXiv:2208.07339 — Eight-bit Quantization
- **QLoRA (2023):** arXiv:2305.14314 — NF4 quantization
- **Repos:** ggerganov/llama.cpp, casper-hansen/AutoAWQ, huggingface/optimum, huggingface/peft, bitsandbytes-foundation/bitsandbytes
