---
name: research-paper-writing
description: "End-to-end pipeline for producing publication-ready ML/AI research papers targeting NeurIPS, ICML, ICLR."
version: "1.1.0"
tags: [research, paper, writing, ML/AI]

---

# Research Paper Writing Pipeline

End-to-end pipeline for producing publication-ready ML/AI research papers targeting **NeurIPS, ICML, ICLR, ACL, AAAI, and COLM**.

## Workflow Overview

```
Phase 0: Setup → Phase 1: Lit Review → Phase 2: Experiment → Phase 3: Analysis
→ Phase 4: Writing → Phase 5: Review → Phase 6: Revision → Phase 7: Submission
```

Iterative loop — results trigger new experiments, reviews trigger new analysis.

## Referencias

Carga los refs bajo demanda con `skill_view(name='research-paper-writing', file_path='references/<nombre>')`:

| Ref | Contenido |
|-----|-----------|
| `workflow-phases.md` | Detalle completo de las 8 fases del pipeline |
| `operations.md` | Memoria, todo, cron monitoring, comunicación con usuario |
| `report-format.md` | Formatos de reporte, decision points, human input |
| `full-skill.md` | Skill completo (100KB) — cargar solo si se necesita todo |

## Cuándo usar

- Escribir papers de ML para conferencias top (NeurIPS, ICML, ICLR)
- Pipeline completo de experimentación → análisis → escritura → submission
- No usar para tareas de investigación no relacionadas con papers académicos
