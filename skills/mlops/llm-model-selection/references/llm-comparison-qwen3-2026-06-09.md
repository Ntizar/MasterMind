# LLM Comparison: Qwen3, Gemma 4 & Alternatives (2026-06-09)

## Qwen3 Family Specs (Alibaba)

### Dense Models
| Model | Params | Layers | Heads | Context | License |
|-------|--------|--------|-------|---------|---------|
| Qwen3-0.6B | 0.6B | 28 | 16/8 | 32K | Apache 2.0 |
| Qwen3-1.7B | 1.7B | 28 | 16/8 | 32K | Apache 2.0 |
| Qwen3-4B | 4B | 36 | 32/8 | 32K | Apache 2.0 |
| Qwen3-8B | 8B | 36 | 32/8 | 128K | Apache 2.0 |
| Qwen3-14B | 14B | 40 | 40/8 | 128K | Apache 2.0 |
| Qwen3-32B | 32B | 64 | 64/8 | 128K | Apache 2.0 |

### MoE Models
| Model | Total Params | Activated | Experts (Total/Active) | Context | License |
|-------|-------------|-----------|----------------------|---------|---------|
| Qwen3-30B-A3B | 30B | 3B | 128/8 | 128K | Apache 2.0 |
| Qwen3-235B-A22B | 235B | 22B | 128/8 | 128K | Apache 2.0 |

### Key Facts
- **Training data:** ~36 trillion tokens
- **Languages:** 119 languages
- **Features:** Hybrid thinking modes, agentic capabilities, MCP support
- **Multimodal:** ❌ Solo texto

### VRAM Estimates
| Model | BF16 | FP8 | INT4 |
|-------|------|-----|------|
| Qwen3-8B | ~16GB | ~8GB | ~4GB |
| Qwen3-14B | ~28GB | ~14GB | ~7GB |
| Qwen3-32B | ~64GB | ~32GB | ~16GB |
| Qwen3-30B-A3B (MoE) | ~60GB | ~30GB | ~15GB |
| Qwen3-235B-A22B (MoE) | ~470GB | ~235GB | ~118GB |

## Gemma 4 Family (Google) — Released ~June 2026

### Dense Models
| Model | Params | Layers | Context | License |
|-------|--------|--------|---------|---------|
| Gemma 4 E2B | 2B | — | 256K | Apache 2.0 |
| Gemma 4 E4B | 4B | — | 256K | Apache 2.0 |
| Gemma 4 12B | 12B | — | 256K | Apache 2.0 |
| Gemma 4 31B | 31B | — | 256K | Apache 2.0 |

### MoE Models
| Model | Total Params | Activated | Context | License |
|-------|-------------|-----------|---------|---------|
| Gemma 4 26B A4B | 26B | 4B | 256K | Apache 2.0 |

### Key Facts
- **Training data:** No especificado públicamente (Google)
- **Languages:** 140+ idiomas
- **Features:** Encoder-free multimodal (texto + imagen + audio nativo)
- **Multimodal:** ✅ Texto + Imagen + Audio nativo (sin encoders separados)
- **Arquitectura:** Dense + MoE, encoder-free unified

### VRAM Estimates
| Model | BF16 | INT4 |
|-------|------|------|
| Gemma 4 12B | ~24GB | ~6-8GB |
| Gemma 4 26B A4B (MoE) | ~52GB | ~8-10GB |
| Gemma 4 31B | ~62GB | ~16GB |

### Fine-tunes destacados
- **Fabled-Gemma4-31B** (Lambent) → Fine-tune conversacional sobre Gemma 4 31B. Mejor para chat/rol. ~16GB VRAM INT4.

## Comparativa directa

| Modelo | VRAM INT4 | Contexto | Multimodal | Calidad | Infra mínima |
|--------|-----------|----------|------------|---------|--------------|
| **Gemma 4 12B** | ~8GB | 256K | ✅ Texto+Img+Audio | ⭐⭐⭐⭐ | 1x GPU 8GB |
| **Gemma 4 26B A4B** | ~8-10GB | 256K | ✅ Texto+Img+Audio | ⭐⭐⭐⭐⭐ | 1x GPU 8GB (MoE) |
| **Gemma 4 31B** | ~16GB | 256K | ✅ Texto+Img+Audio | ⭐⭐⭐⭐⭐ | 1x GPU 16GB |
| **Qwen3 32B** | ~16GB | 128K | ❌ Solo texto | ⭐⭐⭐⭐ | 1x GPU 16GB |
| **Qwen3 30B-A3B** | ~15GB | 128K | ❌ Solo texto | ⭐⭐⭐⭐ | 1x GPU 16GB |
| **Qwen3 235B-A22B** | ~118GB | 128K | ❌ Solo texto | ⭐⭐⭐⭐⭐ | 8x GPU A100 |

### Conclusiones clave
1. **Gemma 4 26B A4B** es el mejor ratio calidad/VRAM: solo 4B activos pero calidad de modelo grande
2. **Gemma 4 12B** es perfecto para GPUs de 8GB (RTX 3060, 4060) con contexto 256K
3. **Gemma 4** tiene multimodal nativo (audio + imagen) que Qwen3 NO tiene
4. **Gemma 4** tiene contexto 256K vs 128K de Qwen3
5. **Qwen3** sigue siendo competitivo en reasoning puro y coding

## Fuentes
- Gemma 4 12B: https://huggingface.co/google/gemma-4-12B-it
- Gemma 4 31B: https://huggingface.co/google/gemma-4-31B-it
- Fabled-Gemma4-31B: https://huggingface.co/Lambent/Fabled-Gemma4-31B
- Qwen3 blog: https://qwenlm.github.io/blog/qwen3/
- Qwen3-32B HuggingFace: https://huggingface.co/Qwen/Qwen3-32B