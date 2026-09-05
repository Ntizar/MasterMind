---
name: rvc-voice-conversion
description: "Usa al convertir voz con RVC entrenando por voz."
version: "2.0.0"
tags: [rvc, voice-conversion, vc, voz, entrenamiento, webui, python]
related_skills: [openvoice-voice-cloning, f5-tts, gpt-sovits-tts, rvc-voice-conversion]
---

# RVC — Conversión de voz (retrieval-based, por entrenamiento)

> ⚠️ Corrección 2026-09-05 (auditoría stars-explorer): la v1 decía "zero-shot, clones de voz sin fine-tuning" y `python infer.py`. **Falso:** RVC requiere **entrenar un modelo por voz** y se lanza con `python webui.py`.

**Repo:** `https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI` (MIT, Python, ~38K⭐).

## When to Use

- Cuando pidas **conversión de voz** (cambiar el timbre de un audio a otra voz) y dispongas de unos ~10 min de voz limpia para entrenar.
- Para controlar el resultado (pitch, preservación del habla) de la voz objetivo.

## Qué es

Conversor de voz **basado en recuperación/entrenamiento**: para cada voz objetivo hay que **entrenar un modelo** (el README abre con "Easily train a good VC model with voice data <= 10 mins!"). **No es zero-shot**: no clona sin datos.

## Uso

```bash
# 1) En el root del repo
# 2) Instalar dependencias según hardware (NO existe requirements.txt genérico):
#    CPU:
pip install -r requirments_cpu_py312.txt        # (nombre tal cual en el repo)
#    NVIDIA CUDA 11.8 / 12.x:
#    pip install -r requirments_cu118_py312.txt
#    pip install -r requirments_cu128_py312.txt
# 3) Arrancar la web UI:
python webui.py        # (o go-webui.bat en Windows)
```

*(El nombre exacto de los ficheros de requisitos y de `webui.py` puede variar por versión — verificar en el README. `infer.py` NO existe.)*

## Pitfalls

- **No es zero-shot** — hay que entrenar un modelo por voz (muestra limpia). Cualquier afirmación de "clones sin fine-tuning" es falsa.
- El lanzador es `python webui.py`, no `infer.py` (404 en el repo).
- Los requisitos van por hardware, no un único `requirements.txt`.

## Verificación

- Entrenar con una muestra limpia (~10 min) y convertir un clip de prueba; comprobar que la voz resultante es consistente y no pierde nitidez.
