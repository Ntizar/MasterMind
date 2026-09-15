# MiniMind — detalles de entrenamiento verificados

Extraído del README real de `jingyaogong/minimind` (en chino; consultado 2026-09-15).

## Versiones y tamaños

| Modelo | Parámetros | Fecha de release |
|---|---|---|
| `minimind-3` | 64M (denso) | 2026.04.01 |
| `minimind-3-moe` | 198M-A64M (MoE) | 2026.04.01 |

La estructura principal está alineada con el ecosistema **Qwen3 / Qwen3-MoE** y **elimina el diseño de shared expert**.

## Tool calling y razonamiento (de serie)

- La capacidad `toolcall` ya viene **mezclada en los datos principales** `sft_t2t` / `sft_t2t_mini`: el checkpoint `full_sft` por defecto ya tiene Tool Call básico.
- El `chat_template` soporta etiquetas de Tool Calling y Reasoning (`<tool_call>`, `<think>`, …).
- Ejemplos de inferencia disponibles en `scripts/chat_api.py`.

## Checkpoints y reanudación

- El entrenamiento guarda checkpoints completos (modelo, optimizador, progreso) en `./checkpoints/`.
- Nomenclatura: `<peso>_<dimensión>_resume.pth` — p. ej. `full_sft_512_resume.pth`.
- Salida tras entrenar: `out/full_sft_*.pth` (`full` = ajuste de todos los parámetros).
- `eval_llm.py --weight <prefijo>` acepta los prefijos `pretrain`, `full_sft`, etc.

## Criterio MoE (dato práctico poco obvio)

Más expertos **no** significa más rápido: en PyTorch nativo, el enrutado por tokens y la orquestación de kernels encarecen el entrenamiento. La configuración dulce del proyecto es **4 expertos / top-1**, que resulta ~**50 % más lenta** que el modelo denso equivalente. Para acelerar harían falta librerías con kernels MoE fusionados (Triton, DeepSpeed-MoE, Megatron-LM) — deliberadamente fuera del alcance para mantener PyTorch puro.

## Datasets

- Descarga: ModelScope o HuggingFace (`gongjy/minimind_dataset` / `jingyaogong/minimind_dataset`).
- Orígenes de los datos SFT: instrucciones de alta calidad, conversaciones públicas, datos sintéticos por destilación y datasets abiertos compatibles (DeepCtrl SFT, Magpie-Align, R1-Distill-SFT, COIG, Step-3.5-Flash-SFT…).
- Incluye ~100 k ejemplos de `tool call` sintetizados por el autor a partir de `qwen3-4b`, además de datos de razonamiento de la serie `qwen3`.
- Compatibilidad de licencias cuidado: Apache-2.0 y CC-BY-NC-2.0 según la fuente.
