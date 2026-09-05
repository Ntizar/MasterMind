---
name: scientific-agent-skills
description: "Usa a investigar con skills de IA científica (Agent)."
version: "2.0.0"
tags: [cientifico, research, agent-skills, papers, data, skills]
related_skills: [scientific-agent-skills, arxiv, prisma-systematic-review]
---

# Scientific Agent Skills — colección de skills para ciencia con agentes

> ⚠️ Corrección 2026-09-05 (auditoría): es una **colección de skills Agent (SKILL.md)**, no una librería Python. Instalación vía `npx skills add` / `gh skill install`, no git clone + import arxiv.

**Repo:** `https://github.com/K-Dense-AI/scientific-agent-skills` (Python, ~43K⭐).

## When to Use

- Cuando pidas **investigación científica con un agente IA** (papers, datos, experimentos): es un set de skills preempaquetadas (163) para el agente, no código importable.

## Uso

```bash
# Recomendado
npx skills add K-Dense-AI/scientific-agent-skills
# o
gh skill install
# (o copiar skills/ al directorio de skills del agente)
```

- El "uso" es **activar el skill del agente** (delegar a una de las skills de la colección), no `import arxiv` (Python genérico).

## Pitfalls

- NO es una librería Python; no hay `import scientific_agent_skills`.
- Instalación: `npx skills add`/`gh skill install` (o copiar skills/), no `git clone && cd`.
- El ejemplo "import arxiv" no corresponde al mecanismo del repo.

## Verificación

- Instalar y comprobar que las skills aparecen en el agente; delegar un tema y ver el flujo científico.
