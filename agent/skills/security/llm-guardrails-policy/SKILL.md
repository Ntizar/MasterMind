---
name: llm-guardrails-policy
version: "1.0.0"
description: "Usa para optimizar políticas LLM por ASR con autoguardrails."
tags: [llm, alignment, guardrails, safety, autoguardrails]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [llm, alignment, guardrails, safety, autoguardrails]
    related_skills: [hermes-agent]
---
# autoguardrails — Ajuste de políticas LLM por ASR

## Resumen
`autoguardrails` (Santander AI Lab) es un harness de investigación de alineación estilo autoresearch: optimiza una única superficie mutable `policy.md` para minimizar la tasa de éxito de ataque (ASR) contra un suite de evaluación fija, con un suelo de paso benigno. Metrica top-line: `ASR` (menor es mejor). Reporta también `asr_unguarded` (política vacía) y `asr_with_policy`.

## Uso (comandos reales del README)

```bash
# 1. Registrar baseline
python -m autoguardrails baseline --reset --repeat 2 --notes "initial baseline"

# 2. Editar solo policy.md

# 3. Evaluar nuevo candidato
python -m autoguardrails candidate --repeat 2 --notes "cover jailbreak and obfuscation"

# 4. Inspeccionar resultado mantenido
python -m autoguardrails status

# 5. Ver log completo
cat results.tsv
```

Wrapper single-entrypoint:

```sh
sh run_autoguardrails.sh status
sh run_autoguardrails.sh evaluate
sh run_autoguardrails.sh baseline "initial baseline" 2
sh run_autoguardrails.sh candidate "cover jailbreak and obfuscation" 2
```

## Patrones / Arquitectura
- Superficie mutable pequeña (solo `policy.md`), evaluador fijo, presupuesto wall-clock fijo.
- Comparar candidatos con una única métrica top-line; registrar cada decisión keep/discard.
- Si un candidato se rechaza, el harness restaura `policy.md` a la última versión aceptada automáticamente.
- Config de modelo real vía variables de entorno: target (`AUTOGUARDRAILS_TARGET_PROVIDER`, `_MODEL`, `_API_BASE`, `_API_KEY`) y judge (`AUTOGUARDRAILS_JUDGE_PROVIDER`, `_MODEL`, `_API_BASE`, `_API_KEY`). Usar `openai_compatible` como provider.

## Pitfalls
- Usar un juez congelado durante la serie: no cambiar prompts ni modelo de juez a mitad de experimento.
- En Windows ejecutar el wrapper desde Git Bash u otro shell POSIX, no `cmd`.
- El set por defecto usa un stub local determinista (offline); configurar endpoints reales solo para experimentos reales.

## Verificación
- `python -m autoguardrails status` muestra el resultado mantenido.
- `cat results.tsv` muestra el log completo con `asr_unguarded` y `asr_with_policy`.
- Confirmar el suelo benigno (que el sistema no gane rechazándolo todo).

## Referencia
README de https://github.com/SantanderAI/autoguardrails (Apache 2.0, Python 3.10+).
