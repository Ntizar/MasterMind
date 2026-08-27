# Microsoft VibeVoice

- **URL:** https://github.com/microsoft/VibeVoice
- **Categoría:** Audio / Voz / IA / TTS / ASR
- **¿Qué hace?:** VibeVoice es una familia de modelos open-source de voz AI de frontera por Microsoft. Incluye modelos de Text-to-Speech (TTS) y Automatic Speech Recognition (ASR). La innovación clave es el uso de tokenizadores de speech continuos (Acoustic y Semantic) a **7.5 Hz** (ultra bajo framerate), que preservan fidelidad de audio mientras boostean eficiencia computacional. Usa un framework de **next-token diffusion** con LLM para contexto textual y un diffusion head para detalles acústicos de alta fidelidad.
- **Casos de uso:**
  - **TTS (VibeVoice-TTS-1.5B):** Síntesis de hasta 90 minutos con 4 speakers distintos. Aceptado como Oral en ICLR 2026.
  - **ASR (VibeVoice-ASR-7B):** Transcripción de audio largo-form (60 min en un solo pass) con Who/When/What estructurado
  - **Realtime TTS (VibeVoice-Realtime-0.5B):** Streaming TTS con input de texto en streaming, 9 idiomas, 11 estilos ingleses
  - **Multilingual ASR:** Soporte nativo para 50+ idiomas con code-switching
  - **Fine-tuning:** Código LoRA disponible para ASR
  - **vLLM inference:** Inferencia acelerada con vLLM plugin
- **Snippets útiles:**

```python
# Instalación
pip install -e .
# O desde HuggingFace Transformers (ASR)
# pip install transformers

# VibeVoice-ASR - Inferencia con Transformers
from transformers import AutoModel
import torch

model = AutoModel.from_pretrained("microsoft/VibeVoice-ASR-HF", torch_dtype=torch.float16)
model = model.to("cuda")

# Inference desde archivo de audio
# python demo/vibevoice_asr_inference_from_file.py \
#     --model_path microsoft/VibeVoice-ASR \
#     --audio_files [audio_path]

# Gradio Demo
# python demo/vibevoice_asr_gradio_demo.py \
#     --model_path microsoft/VibeVoice-ASR \
#     --share
```

```python
# Arquitectura VibeVoice (TTS)
from vibevoice.modular.modeling_vibevoice import VibeVoiceModel
from vibevoice.modular.configuration_vibevoice import VibeVoiceConfig

# Componentes clave:
# 1. Language Model (Qwen2) - entiende contexto textual
# 2. Acoustic Tokenizer - tokeniza audio acústico
# 3. Semantic Tokenizer - tokeniza audio semántico
# 4. SpeechConnector - conecta LM con componentes de speech
# 5. Diffusion Head - genera detalles acústicos de alta fidelidad
# 6. DPMSolver Scheduler - scheduler de difusión

# Architecture pattern:
class SpeechConnector(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, output_dim)
        self.norm = LlamaRMSNorm(output_dim, eps=1e-6)
        self.fc2 = nn.Linear(output_dim, output_dim)

    def forward(self, features, **kwargs):
        x = self.fc1(features)
        x = self.norm(x)
        x = self.fc2(x)
        return x
```

```python
# VibeVoice-Realtime-0.5B - Streaming TTS
# Colab: https://colab.research.google.com/github/microsoft/VibeVoice/blob/main/demo/vibevoice_realtime_colab.ipynb

# Soporta:
# - Streaming text input
# - Generación de speech largo-form
# - 9 idiomas: DE, FR, IT, JP, KR, NL, PL, PT, ES
# - 11 estilos ingleses distintos
# - Modelo de solo 0.5B parámetros (ligero)
```

```python
# VibeVoice-ASR - Características clave
# - 60 minutos de audio en un solo pass (64K tokens)
# - Who (Speaker) + When (Timestamps) + What (Content)
# - Customized Hotwords para dominio específico
# - 50+ idiomas con code-switching nativo
# - Multilingual: English, French, German, Italian, Japanese, Korean,
#   Portuguese, Russian, Spanish, Thai, Vietnamese, Chinese, etc.

# Evaluación en MLC-Challenge:
# English DER: 4.28, cpWER: 11.48
# Spanish DER: 2.67, cpWER: 10.51
# Japanese DER: 0.82, cpWER: 15.33
```

```python
# Finetuning ASR con LoRA
# python finetuning-asr/lora_finetune.py
# Inference LoRA:
# python finetuning-asr/inference_lora.py
```

- **Cómo integrarlo en proyectos:**
  1. **ASR:** Usar el modelo desde HuggingFace Transformers (`microsoft/VibeVoice-ASR-HF`) para integración directa
  2. **TTS:** Clonar el repo, instalar con `pip install -e .`, usar los demos como punto de partida
  3. **Realtime:** Usar el modelo 0.5B para aplicaciones de baja latencia
  4. **vLLM:** Para producción, usar el vLLM plugin para inferencia acelerada
  5. **Fine-tuning:** El código LoRA está disponible en `finetuning-asr/`
  6. Requiere GPU NVIDIA con CUDA (recomendado NVIDIA PyTorch Container)
- **Fecha de aprendizaje:** 2026-05-26
- **Autores:** Microsoft Research
- **Stars:** 47,435
- **Paper:** ICLR 2026 (Oral) para TTS, arXiv para ASR
- **Modelos:** VibeVoice-TTS-1.5B, VibeVoice-ASR-7B, VibeVoice-Realtime-0.5B
