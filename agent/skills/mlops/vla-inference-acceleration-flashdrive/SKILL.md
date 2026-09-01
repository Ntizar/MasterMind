---
name: vla-inference-acceleration-flashdrive
version: "1.0.0"
description: "Use al acelerar inferencia VLA en tiempo real (FlashDrive)."
author: "Mastermind (stars-explorer) — fuente: z-lab/flashdrive"
license: "MIT (código; weights NVIDIA no-comerciales)"
tags: [vla, inferencia, vllm, cuantizacion, conduccion-autonoma, gpu, tiempo-real]
metadata:
  hermes:
    author: "David Antizar (Ntizar) — aprendizaje de stars"
    tags: [vla, inferencia, gpu, tiempo-real]
    related_skills: [cctv-yolo, fast-alpr, traffic-digital-twin-cctv, vllm, llama-cpp, deep-learning-patterns]
---

# Aceleración de inferencia VLA — FlashDrive (z-lab/flashdrive)

Fuente: https://github.com/z-lab/flashdrive (MIT, z-lab — UCSD). Acelera los modelos Vision-Language-Action de NVIDIA Alpamayo 1.5 / R1 (10B params) **×4.5 sin pérdida de precisión** (de hecho mejora minADE). Consultada 2026-09-01. El skill cubre el patrón completo: streaming KV + speculative decoding + W4A8 + caching de acciones + CUDA graphs.

## Cuándo usar

- Inferir modelos VLA / fundaciones de conducción (Alpamayo, o futuros VLA de 7-10B) con latencia por ventana <200 ms en una sola GPU.
- Patrones de aceleración para cualquier modelo multimodal con streaming temporal (cámara continua, series de frames): la técnica es transferible a CCTV + LLM, digital twins, etc.
- Presupuestar hardware para proyectos de tráfico con IA de fondo (una sola GPU de un nodo sirve para 10B VLA optimizado).

## Las 5 técnicas (co-diseño algoritmo-sistema; ninguna basta sola)

1. **Streaming inference** — reutilizar el KV cache de cada frame entre ventanas solapadas: la ventana nueva solo prefilla sus frames nuevos. (Encode 87→12 ms, Prefill 165→47 ms.)
2. **Speculative reasoning con draft de difusión por bloques** (DFlash, ICML 2026) — un modelo draft propone bloques de 8 tokens que el target verifica en un solo forward, preservando la distribución del target. (Decode 272→45 ms.)
3. **Cuantización W4A8** (ParoQuant, ICLR 2026) — pesos INT4 con rotación por pares + activaciones INT8 vía kernels Marlin de vLLM; el action-expert se queda en bf16 (la precisión de la acción importa).
4. **Adaptive action caching** — reutilizar la velocidad predicha en pasos seleccionados del difusor de acciones, saltándose forwards del action-expert. (Action 193→47 ms.)
5. **Optimizaciones de sistema** — KV cache estático, proyecciones de expertos fusionadas, `torch.compile` con CUDA graphs sobre el loop de decode completo.

## Uso rápido (stack de referencia)

```bash
git clone https://github.com/z-lab/flashdrive && cd flashdrive
uv venv --python 3.12 && source .venv/bin/activate
uv sync   # CUDA 12.8, GPU con compute capability ≥8.0
python scripts/infer.py --model-path z-lab/Alpamayo-1.5-10B    # optimizado
python scripts/infer.py --model-path nvidia/Alpamayo-1.5-10B   # baseline
```

```python
import flashdrive
model = flashdrive.from_pretrained("z-lab/Alpamayo-1.5-10B")
pred_xyz, pred_rot = model.sample_trajectories_streaming(data)
# 1ª llamada por stream solo prefilla KV y devuelve (None, None); luego cada ventana → trayectorias
```

Convención HF elegante: `from_pretrained` toma la ruta **base**; los companions W4A8 (`-PARO`) y draft (`-DFlash`) se derivan por sufijo y se descargan solos. Checkpoints en huggingface.co/collections/z-lab/flashdrive.

## Números de referencia (RTX PRO 6000, 100 clips PhysicalAI-AV)

| Modelo | minADE ↓ | Latencia/ventana | Speedup |
|---|---|---|---|
| Alpamayo 1.5 baseline | 1.705 | 717 ms | 1.0× |
| + FlashDrive | **1.573** | **151 ms** | 4.7× |
| Alpamayo 1 (R1) baseline | 1.869 | 704 ms | 1.0× |
| + FlashDrive | **1.662** | **155 ms** | 4.5× |

## Aplicación a proyectos de David

- **CCTV-YOLO / traffic-digital-twin-cctv**: el patrón "KV cache streaming entre ventanas solapadas de frames" es directamente aplicable a cualquier pipeline de vídeo + LLM continuo (evita re-procesar el prefijo visual por frame).
- **Espejo mental de latencia**: un VLA de 10B cabe en 150 ms/ventana en GPU de un solo nodo — dimensiona expectativas para dashboards de tráfico con IA sin clúster.
- **DFlash y ParoQuant son repos separados** (z-lab/dflash, z-lab/paroquant) utilizables de forma independiente para LLMs de razonamiento no-VLA.

## Pitfalls

- **No esperar speedups de una sola técnica**: los autores son explícitos — la ×4.5 sale de las cinco combinadas; aplicarlas sueltas da resultados mediocres.
- **Weights de Alpamayo bajo licencia no-comercial de NVIDIA** — el código MIT no libera el uso comercial de los checkpoints.
- **Primera llamada del stream devuelve `(None, None)`** — es prefill, no un fallo; el código cliente debe tolerarlo.
- **Requiere GPU Ampere+ (compute cap ≥8.0) y CUDA 12.8** con kernels Marlin (INT4) — no corre en CPU ni en GPUs viejas.
- **flash-attn + torch.compile + CUDA graphs** es frágil ante cambios de shapes: el KV cache estático es justamente para evitar recompilas por ventana.

## Verificación

- Benchmark propio: `scripts/infer.py` reporta minADE y latencia por ventana — comparar checkpoint `z-lab/` vs `nvidia/` en los mismos clips.
- Sanity check del streaming: la 2ª ventana de un stream debe tardar ≈prefill de los frames nuevos (no de la ventana completa).
