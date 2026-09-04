# ChromaDB Dedup — Resultados Verificados (2026-06-16)

## Setup

- Threshold: 0.25 (qwen3-embedding rara vez da >0.5)
- Colección: mastermind-skills (244 skills indexados)
- Script: `consultar-skills.py "keywords" --json`

## Resultados del primer batch nocturno

| Repo | Stars | Score ChromaDB | Skill existente detectado | Decisión |
|------|-------|---------------|--------------------------|----------|
| 3b1b/manim | 87.7k | 0.85 | creative/manim-video | skip |
| twentyhq/twenty | 50.1k | 0.79 | mastermind/crm-erp-fullstack | skip |
| microsoft/VibeVoice | 49.4k | 0.89 | media/voicebox | skip |
| harry0703/MoneyPrinterTurbo | 88.6k | — (no match) | — | **skill creado: video-gen-from-topic** |

## Análisis

- **3 de 4 repos** fueron detectados como "ya cubiertos" → ChromaDB funciona correctamente
- Los scores de 0.79-0.89 son altos y consistentes para repos semánticamente similares
- MoneyPrinterTurbo no tuvo match porque el patrón "topic-driven video generation" es único en el ecosistema
- **El threshold 0.25 es correcto:** No produce falsos positivos en este rango de scores

## Cómo verificar duplicado antes de crear skill

```bash
cd /hermes-home/scripts && /hermes-home/chromadb-venv/bin/python consultar-skills.py "descripción del repo" --json
```

Si el score del top resultado es > 0.5, casi seguro ya existe un skill cubriendo eso.
Si el score es 0.25-0.5, revisar manualmente si el skill existente es suficiente.
Si no hay resultados > 0.25, es un candidato seguro para skill nuevo.
