---
name: skillspector
description: "Usa a escanear skills en busca de vulnerabilidades."
version: "2.0.0"
tags: [skillspector, seguridad, skills, escaneo, vulnerabilidades, docker]
related_skills: [skillspector, presidio-pii, llm-guardrails-policy]
---

# SkillSpector — scanner de seguridad para skills de agentes

> ⚠️ Corrección 2026-09-05 (auditoría): el README declara **71 patrones de vulnerabilidad en 17 categorías** (incluye anti-refusal), no 64/16; el tag de imagen docker del README es `skillspector` (verificar el ghcr correcto).

**Repo:** `https://github.com/NVIDIA/SkillSpector` (Python, ~16K⭐).

## When to Use

- Cuando pidas **escanear skills de agentes** (SKILL.md) en busca de vulnerabilidades/patrones peligrosos (prompt injection, exfiltración de secrets, etc.).

## Uso

```bash
# Docker (tag del README)
docker run --rm -v "$PWD:/app" skillspector /app
# o usar el CLI del proyecto si se ejecuta en python
```

## Pitfalls

- Recuento real: **71 patrones / 17 categorías** (añade anti-refusal), no 64/16.
- Tag docker: el del README (`skillspector`); verificar el ghcr si se usa la imagen remota.

## Verificación

- Escanear un skill de prueba que contenga un patrón peligroso (p.ej. leer secrets) y confirmar que lo detecta.
