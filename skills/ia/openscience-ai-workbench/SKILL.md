---
name: openscience-ai-workbench
version: "1.0.0"
description: "OpenScience — AI workbench open-source para investigación científica: agente autónomo con ciclo completo de investigación"
---

# OpenScience — AI Workbench para Investigación Científica

## Descripción

OpenScience es un workbench de IA open-source para investigación científica. Le das un objetivo, y el sistema hace el ciclo completo: revisión de literatura, hipótesis, código, experimentos, análisis y write-up. Model-agnostic con 290+ skills de dominio.

## Por qué importa para David

- **Agente autónomo**: Patrón de agente que ejecuta un workflow completo sin intervención humana
- **290+ skills de dominio**: Training (DeepSpeed, PEFT, TRL), biología, química, física
- **Model-agnostic**: Soporta Anthropic, OpenAI, Google y muchos más via API keys
- **Workspace en browser**: Interfaz web para gestionar sesiones de investigación

## Arquitectura

```
Goal → Research Agent → Literature Review → Hypothesis
    ↓
Code Generation → Run Experiments → Query Databases
    ↓
Analysis → Write-up → Critique & Review
```

Agentes especializados: `research`, `biology`, `physics`, `ml` con sub-agents de critique y literature-review

## Instalación

```bash
npm install @synsci/openscience
# o
bun install @synsci/openscience
```

## Integración con proyectos de David

- **Research assistant**: Patrón para agentes de investigación en temas de transporte/urbanismo
- **Multi-agent**: Patrón de agents especializados con critique loop
- **Skills domain pattern**: 290+ skills de referencia para diseñar skills propios

## Pitfalls

- Proyecto muy nuevo (creado julio 2026) → API puede cambiar
- Requiere API keys de proveedores (Anthropic, OpenAI, etc.)
- Consume mucho LLM tokens en ciclos de investigación
- Dependencias de npm con Bun pueden ser inestables

## Referencias

- GitHub: https://github.com/synthetic-sciences/openscience
- Docs: https://openscience.sh/docs
- npm: https://www.npmjs.com/package/@synsci/openscience
