# MLX-VLM

**URL:** https://github.com/Blaizzy/mlx-vlm
**Categoría:** Visión/ML
**Estrellas:** 4,780
**Lenguaje:** Python

## ¿Qué hace?
MLX-VLM es un paquete para **inferencia y fine-tuning** de Vision Language Models (VLMs) y Omni Models (VLMs con soporte de audio y video) en Mac usando el framework MLX de Apple. Soporta más de 60 modelos de visión, incluyendo Qwen2/2.5/3/3.5-VL, LLaVA, Llama-3.2-Vision, DeepSeek-VL, Gemma, Phi-4, y muchos más. Incluye características avanzadas como decoding especulativo (2-3x más rápido), cuantización del KV cache (TurboQuant a 3.5 bits), caching de características de visión, batching continuo, caching automático de prefijos (APC), y una API OpenAI-compatible vía servidor FastAPI.

## Casos de uso
1. **Inferencia local de VLMs en Apple Silicon** — Ejecutar modelos como Qwen2-VL o LLaVA directamente en un Mac sin necesidad de GPUs NVIDIA ni conexión a la nube.
2. **Fine-tuning con LoRA/QLoRA** — Adaptar un VLM preentrenado a un dominio específico (OCR, diagnóstico médico, etc.) con mínimos recursos en un Mac.
3. **Servidor API OpenAI-compatible** — Levantar un endpoint `/v1/chat/completions` con soporte multimodal (imágenes, audio, video) para integrar VLMs en aplicaciones existentes.
4. **Análisis de video e imágenes múltiples** — Soporte nativo para análisis de video y comparación de múltiples imágenes en una sola consulta.
5. **Inferencia distribuida** — Ejecutar modelos masivos (p.ej., Kimi-K2.6 de 1T parámetros) en múltiples Macs conectados por Thunderbolt.

## Snippets útiles

### Inferencia básica (imagen + texto)
```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

# Cargar modelo
model_path = "mlx-community/Qwen2-VL-2B-Instruct-4bit"
model, processor = load(model_path)
config = load_config(model_path)

# Preparar entrada
image = ["http://images.cocodataset.org/val2017/000000039769.jpg"]
prompt = "Describe this image."

# Aplicar chat template
formatted_prompt = apply_chat_template(
    processor, config, prompt, num_images=len(image)
)

# Generar respuesta
output = generate(model, processor, formatted_prompt, image, verbose=False)
print(output)
```

### Inferencia con audio (Omni Model)
```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

model_path = "mlx-community/gemma-3n-E2B-it-4bit"
model, processor = load(model_path)

audio = ["/path/to/audio1.wav", "/path/to/audio2.mp3"]
prompt = "Describe what you hear in these audio files."

formatted_prompt = apply_chat_template(
    processor, model.config, prompt, num_audios=len(audio)
)

output = generate(model, processor, formatted_prompt, audio=audio, verbose=False)
print(output)
```

### Multi-imagen
```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

model, processor = load("mlx-community/Qwen2-VL-2B-Instruct-4bit")

images = ["path/to/image1.jpg", "path/to/image2.jpg"]
prompt = "Compare these two images."

formatted_prompt = apply_chat_template(
    processor, model.config, prompt, num_images=len(images)
)

output = generate(model, processor, formatted_prompt, images, verbose=False)
print(output)
```

### Streaming con caching de visión (multi-turn)
```python
from mlx_vlm import load, stream_generate, VisionFeatureCache
from mlx_vlm.prompt_utils import apply_chat_template

model, processor = load("google/gemma-4-26b-a4b-it")
cache = VisionFeatureCache()

image = "path/to/image.jpg"

# Turno 1 — cache miss (codifica la imagen)
prompt1 = apply_chat_template(processor, model.config, "Describe this image.", num_images=1)
for chunk in stream_generate(model, processor, prompt1, image=[image],
                              max_tokens=200, vision_cache=cache):
    print(chunk.text, end="")

# Turno 2 — cache hit (omite el encoder visual, 11x más rápido)
prompt2 = apply_chat_template(processor, model.config, "What colors do you see?", num_images=1)
for chunk in stream_generate(model, processor, prompt2, image=[image],
                              max_tokens=200, vision_cache=cache):
    print(chunk.text, end="")
```

### Servidor FastAPI (API OpenAI-compatible)
```bash
# Iniciar servidor con modelo precargado
mlx_vlm.server --model mlx-community/Qwen2-VL-2B-Instruct-4bit --port 8080

# Con cuantización de KV cache (ahorra memoria)
mlx_vlm.server --model google/gemma-4-26b-a4b-it --kv-bits 8

# Con decoding especulativo (~2-3x más rápido)
mlx_vlm.server --model Qwen/Qwen3.5-4B \
    --draft-model z-lab/Qwen3.5-4B-DFlash
```

```python
# Consumir el servidor con la librería OpenAI
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="mlx-community/Qwen2-VL-2B-Instruct-4bit",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is in this image?"},
                {"type": "image_url", "image_url": {"url": "path/to/image.jpg"}}
            ]
        }
    ],
    max_tokens=256,
    stream=True,
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Fine-tuning con LoRA
```bash
# LoRA básico
python -m mlx_vlm.lora \
    --model-path mlx-community/Qwen3-VL-2B-Instruct-bf16 \
    --dataset your-dataset-id \
    --batch-size 2 \
    --epochs 2 \
    --learning-rate 2e-5 \
    --output-path ./qwen3-lora-adapter.safetensors

# QLoRA con modelo cuantizado (menos memoria)
python -m mlx_vlm.lora \
    --model-path mlx-community/Qwen3-VL-2B-Instruct-4bit \
    --dataset your-dataset-id \
    --batch-size 4 \
    --epochs 2 \
    --learning-rate 2e-4 \
    --lora-rank 16 \
    --lora-alpha 32 \
    --output-path ./qwen3-qlora-adapter.safetensors

# Full fine-tuning con módulos de visión
python -m mlx_vlm.lora \
    --model-path mlx-community/Qwen3-VL-2B-Instruct-bf16 \
    --dataset your-dataset-id \
    --full-finetune \
    --train-vision \
    --grad-checkpoint \
    --output-path ./qwen3-full-finetune.safetensors
```

### Decoding especulativo (Python API)
```python
from mlx_vlm import load
from mlx_vlm.generate import stream_generate
from mlx_vlm.speculative.drafters import load_drafter

model, processor = load("Qwen/Qwen3.5-4B")
drafter = load_drafter("z-lab/Qwen3.5-4B-DFlash")

for result in stream_generate(
    model, processor,
    prompt="Write a quicksort in Python.",
    max_tokens=512,
    temperature=0,
    draft_model=drafter,
    enable_thinking=True,
):
    print(result.text, end="", flush=True)

print(f"\nAccepted {sum(drafter.accept_lens)/len(drafter.accept_lens):.1f} tokens/round")
```

## Cómo integrarlo en proyectos

### Instalación
```bash
pip install -U mlx-vlm
```
Requiere macOS con chip Apple Silicon (M1/M2/M3/M4) y el framework MLX instalado.

### Flujo de integración típico
1. **Instalar** `mlx-vlm` y `mlx` (depende automáticamente de `mlx-cpu` o `mlx-metal`).
2. **Elegir un modelo** de la lista de soportados (60+ modelos en `mlx_vlm/models/`): Qwen2-VL, Qwen2.5-VL, Qwen3-VL, LLaVA, Llama-3.2-Vision (mllama), DeepSeek-VL, Gemma, Phi-4, Pixtral, Florence-2, PaliGemma, Molmo, MiniCPM-V, y muchos más.
3. **Cargar y generar** con la API `load()` + `generate()`, o usar el servidor FastAPI para exponer una API REST compatible con OpenAI.
4. **Optimizar memoria** con cuantización (`--kv-bits 8` para 8-bit KV cache, `--kv-bits 3.5 --kv-quant-scheme turboquant` para TurboQuant a 3.5 bits — hasta 76% reducción de memoria KV).
5. **Optimizar velocidad** con decoding especulativo (`--draft-model`) — 2-3x más rápido en Qwen3.5, hasta 3.94x en Gemma 4.
6. **Fine-tunar** con `lora.py` para adaptar el modelo a datos propios — soporta LoRA, QLoRA y full fine-tuning con opción de entrenar también los módulos visuales.

### Modelos soportados (selección)
| Familia | Modelos |
|---------|---------|
| **Qwen** | Qwen2-VL, Qwen2.5-VL, Qwen3-VL, Qwen3.5-VL, Qwen3-VL-MoE, Qwen3-Omni-MoE |
| **LLaVA** | LLaVA, LLaVA-NeXT, LLaVA-Bunny |
| **Llama** | Llama-3.2-Vision (mllama), Llama-4 |
| **Gemma** | Gemma3, Gemma3n, Gemma4 |
| **Otros** | DeepSeek-VL/V2, Florence-2, PaliGemma, Molmo, Phi-3-V/Phi-4-Multimodal, Pixtral, MiniCPM-V/O, Idefics2/3, Jina VLM, InternVL, y 40+ más |

### Características avanzadas destacadas
- **Vision Feature Caching** — Reutiliza features visuales en conversaciones multi-turno (11x más rápido en prompt processing).
- **TurboQuant KV Cache** — Cuantización a 2-4 bits del KV cache con kernels Metal personalizados.
- **Automatic Prefix Caching (APC)** — Reutiliza bloques de KV cache entre requests con prefijos compartidos, con persistencia en disco.
- **Continuous Batching** — El servidor procesa múltiples requests concurrentes en batches dinámicos.
- **Structured Outputs** — Soporte para JSON schema con `response_format` (OpenAI-compatible).
- **Thinking Budget** — Control del número de tokens en el bloque de razonamiento (think) para modelos como Qwen3.5.
- **Distributed Inference** — Sharding del LLM en múltiples Macs vía JACCL/Thunderbolt.

## Fecha de aprendizaje: 2026-05-27
