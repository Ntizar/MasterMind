---
name: llm-model-selection
description: "Investigación comparativa de modelos LLM — encontrar alternativas a un modelo base, comparar specs (parámetros, VRAM, contexto), benchmarks, y requisitos de infraestructura"
version: "1.0.0"
author: Mastermind
tags: [llm, model-selection, comparison, research, benchmark, infrastructure]
---

# LLM Model Selection

Investigación comparativa de modelos LLM para encontrar alternativas a un modelo base, con análisis de specs, requisitos de infraestructura, y benchmarks.

## Cuándo usar

- Usuario pide "modelos similares a X pero mejores"
- Comparar alternativas a un modelo actual
- Evaluar si escalar a un modelo más grande merece la pena
- Buscar modelos open-weight con requisitos de infra específicos
- Decidir entre API-based vs self-hosted

## Pasos

### 1. Identificar el modelo base y sus specs

- Buscar en HuggingFace: `https://huggingface.co/ORG/MODEL`
- Extraer: parámetros totales, parámetros activos (MoE), context length, arquitectura (dense/MoE)
- Verificar que el modelo existe (páginas 404 son comunes en HuggingFace blog URLs)

**⚠️ Pitfall:** Las URLs de blog de HuggingFace (`/blog/nombre-modelo`) a menudo dan 404. Usar la URL del modelo directo en HuggingFace o el blog oficial del proveedor (`https://qwenlm.github.io/blog/qwen3/`).

### 2. Buscar alternativas en fuentes fiables

Fuentes prioritarias:
1. **HuggingFace model page** → specs, downloads, inference providers, pricing
2. **LMSYS Chatbot Arena** → `https://lmsys.org` → benchmarks reales de usuarios
3. **HuggingFace Open LLM Leaderboard** → benchmarks académicos
4. **Blog oficial del proveedor** → specs técnicos detallados
5. **Qwen blog** → `https://qwenlm.github.io/blog/` (redirige a qwen.ai)

**⚠️ Browser tool:** Las páginas de HuggingFace Spaces (como LMSYS Arena) son iframes — no se puede leer contenido directamente. Usar curl-based analysis para datos técnicos.

### 3. Extraer specs clave

Para cada modelo candidato, recopilar:
- **Total parameters** (ej: 235B)
- **Activated parameters** (MoE: ej: 22B activados)
- **Context length** (32K, 128K, etc.)
- **VRAM necesaria** (BF16: params × 2 bytes; INT4: params × 0.5 bytes)
- **Arquitectura** (dense, MoE, hybrid)
- **License** (Apache 2.0, etc.)
- **Idiomas soportados**
- **Capacidades** (tool calling, reasoning, coding, multimodal)

**Fórmula VRAM aproximada:**
- BF16: `params × 2 bytes` → 32B params = ~64GB VRAM
- INT4: `params × 0.5 bytes` → 32B params = ~16GB VRAM
- FP8: `params × 1 byte` → 32B params = ~32GB VRAM

### 4. Comparar con modelo base

Categorizar alternativas:
1. **Mejor calidad general** → modelos API (Claude Sonnet 4, GPT-4.5, Gemini 2.5 Pro)
2. **Mejor open-weight** → modelos con buena relación calidad/tamaño
3. **Mejor para infra actual** → modelos que caben en la infra del usuario
4. **Mejor relación precio/calidad** → modelos económicos vía API

### 5. Presentar resultados

Formato recomendado:
- Tabla comparativa con specs clave
- Categorías de recomendación (mejor calidad, mejor para infra, etc.)
- Recomendación concreta basada en el contexto del usuario
- Notas sobre APIs disponibles y precios si relevantes

## Pitfalls

- **No confundir versiones:** "Qwen 3.6" no existe — la familia actual es Qwen3 (con variantes: 0.6B, 1.7B, 4B, 8B, 14B, 32B, 30B-A3B, 235B-A22B). Verificar siempre la versión exacta.
- **No confundir nombres:** "Fable" no es un modelo independiente — es un fine-tune de Gemma 4 31B hecho por Lambent (`Lambent/Fabled-Gemma4-31B`). Buscar siempre en el contexto correcto.
- **MoE vs Dense:** Los modelos MoE tienen parámetros totales MUY superiores a los activos. Comparar siempre por parámetros activos, no totales.
- **VRAM no es solo parámetros:** El contexto largo (128K-256K tokens) añade overhead significativo de KV cache. Un modelo de 32B con 256K contexto puede necesitar más VRAM del calculado solo por parámetros.
- **Modelos API vs self-hosted:** Para infra pequeña (1vCPU/2GB), solo es viable API. No sugerir self-hosted si la infra no lo permite.
- **Benchmarks no son absolutos:** LMSYS Arena es más fiable que los benchmarks académicos (MMLU, GSM8K) porque refleja uso real.
- **curl-based research es más fiable que browser:** Para páginas técnicas (HuggingFace model pages, blogs), curl + grep/sed es más rápido y completo que el browser tool, que puede truncar o dar 404.
- **HuggingFace URLs de blog dan 404 frecuentemente:** `/blog/nombre-modelo` casi siempre falla. Ir directo a `/models?search=nombre` o a la URL del modelo.
- **HuggingFace Spaces son iframes:** No se puede leer contenido directo. Usar curl-based analysis para datos técnicos.
- **Verificar si un "nombre de modelo" es realmente un modelo:** A veces nombres como "Fable", "Fabled", etc. son espacios, usuarios, o fine-tunes, no modelos base. Buscar en `huggingface.co/api/models?search=NOMBRE&sort=downloads` para filtrar ruido.
- **Gemma 4 (junio 2026) es el modelo open-weight más reciente de Google:** Familia con variantes Dense (2B, 4B, 12B, 31B) y MoE (26B A4B). Multimodal nativo (texto+imagen+audio, encoder-free). Contexto 256K. Supera a Qwen3 en contexto y multimodalidad.

## Archivos de soporte

- `references/llm-comparison-qwen3-2026-06-09.md` — Datos concretos: specs Qwen3, alternativas, análisis VRAM, benchmarks