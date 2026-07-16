---
name: scientific-agent-skills
description: Skills de IA para investigación científica — papers, datos, análisis, herramientas de investigación.
version: "1.0.0"
tags: [AI, research, scientific, papers, data, analysis]
---

# Scientific Agent Skills

## Resumen

Skills de IA para investigación científica — papers, datos, análisis. 28k⭐.

## Repo de referencia

- **GitHub:** `github.com/K-Dense-AI/scientific-agent-skills`
- **Lenguaje:** Markdown/Python
- **Licencia:** MIT

## Instalación

```bash
git clone https://github.com/K-Dense-AI/scientific-agent-skills.git
cd scientific-agent-skills
```

## Skills Incluidos

1. **Paper Search:** Búsqueda en arXiv, PubMed, Semantic Scholar
2. **Data Analysis:** Análisis estadístico con Python
3. **Citation Management:** Gestión de referencias
4. **Literature Review:** Automatización de revisiones sistemáticas
5. **Hypothesis Testing:** Testing de hipótesis con datos

## Uso Básico

```python
# Ejemplo: Buscar papers en arXiv
import arxiv

search = arxiv.Search(
    query="transformer attention mechanism",
    max_results=10
)

for result in search.results():
    print(f"{result.title}")
    print(f"  Authors: {', '.join(result.authors)}")
    print(f"  Abstract: {result.summary[:200]}")
```

## Integración con Mastermind

- Complementa `prisma-systematic-review` — skills de investigación
- Útil para `research-paper-writing` — búsqueda y análisis
- Reemplaza búsqueda manual de papers
- Ideal para `llm-wiki` — conocimiento científico

## Pitfalls

- **API limits:** arXiv tiene rate limiting (3 requests/segundo)
- **Calidad:** Los papers no están curados — verificar fuentes
- **Acceso:** Muchos papers requieren suscripción (PDF no disponible)

## Referencias

- [GitHub: K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
