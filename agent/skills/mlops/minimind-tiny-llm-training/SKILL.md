---
name: minimind-tiny-llm-training
description: "Entrena un LLM de 64M desde cero en una sola GPU."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [llm, entrenamiento, pytorch, lora, dpo, grpo, tiny-model]
    related_skills: [llama-cpp, deep-learning-fundamentals, huggingface-hub]
---

# MiniMind — entrenar un LLM de 64M desde cero

Proyecto de formación completo: **pretrain → SFT → LoRA → DPO → PPO/GRPO → RL agéntico**, todo en PyTorch puro y ejecutable en una sola GPU doméstica. Sirve para entender el ciclo completo de entrenamiento sin cluster.

## Cuándo usarlo

- Quieres **entender/experimentar** el pipeline real de entrenamiento (no solo inferencia).
- Necesitas un modelo diminuto para pruebas de tool-calling, tokenizer o RL.
- Buscas template de entrenamiento reproducible (DDP, DeepSpeed, wandb) en escala pequeña.

## Modelos y datos

- **MiniMind-3**: 64M denso · **minimind-3-moe**: 198M con 64M activos, alineados con el ecosistema Qwen3/Qwen3-MoE.
- Tokenizer BPE + ByteLevel con marcas propias para `<tool_call>`, `<tool_response>` y tokens de pensamiento.
- Datasets "mini" (`pretrain_t2t_mini.jsonl`, `sft_t2t_mini.jsonl`) permiten reproducir **MiniMind Zero en ~2,31 h en una RTX 3090** (≈3,0 ¥ ≈ 0,4 $ de GPU alquilada — el README estima 3,0 律 a ~1,3 ¥/h, con 7 ¥ ≈ 1 $).

## Comandos verificados

```bash
pip install -r requirements.txt
modelscope download --model gongjy/minimind-3 --local_dir ./minimind-3   # o git clone https://huggingface.co/jingyaogong/minimind-3
python eval_llm.py --load_from ./minimind-3        # inferencia
python eval_llm.py --load_from ./model --weight full_sft

cd trainer
python train_pretrain.py        # pretrain
python train_full_sft.py        # SFT completo
python train_lora.py            # LoRA
python train_dpo.py             # DPO
python train_ppo.py             # PPO  (o train_grpo.py)
python train_agent.py --rollout_engine sglang --sglang_base_url http://localhost:8998   # RL agéntico
# cualquier script admite --from_resume 1 (incluso cambiando el nº de GPUs)
```

Sirve una API OpenAI-compatible con `python serve_openai_api.py` (soporta `reasoning_content`, `tool_calls`, `open_thinking`) — enchufable a OpenWebUI, Dify, FastGPT. También compatible con `ollama run jingyaogong/minimind-3`, `vllm serve` y llama.cpp.

Utilidades: `scripts/convert_model.py` (torch↔transformers y fusión de LoRA), `train_tokenizer.py`, `cd scripts && streamlit run web_demo.py`.

## Pitfalls

- Los scripts asumen **estructura de directorios del repo** (`trainer/`, `dataset/`): no copiar solo un fichero.
- `--from_resume 1` es la vía para continuar tras un corte, pero el estado se guarda por script: no mezcles checkpoints de `train_full_sft.py` en `train_lora.py`.
- Extrapolación de contexto con **YaRN**: se activa **en inferencia, sin reentrenar** — `python eval_llm.py --weight full_sft --inference_rope_scaling` (modelo PyTorch nativo) o añadiendo `"rope_scaling": {"type": "yarn", "factor": 16.0, "original_max_position_embeddings": 2048}` al `config.json` de los modelos Transformers.

## Referencia

- Repo: `jingyaogong/minimind` (~61.194 ⭐, Python, consultado 2026-09-15).
