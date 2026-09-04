---
name: pysyft-federated-ml
version: "1.0.0"
description: "ML federado y privacidad con PySyft v2 (syft 0.10+)."
tags: [federated, pytorch, syft, privacidad, mlearn, pysyft]
author: 'Hecho con ❤️ por David Antizar'
license: Apache-2.0
metadata:
  hermes:
    tags: [federated, pytorch, syft, privacidad, ml]
    related_skills: [deep-learning-fundamentals, huggingface-hub, pydantic-ai]
---

# PySyft — Aprendizaje Federado y Privacidad (v2)

## Resumen

PySyft (repo `OpenMined/PySyft`, ~10K⭐, licencia Apache-2.0) permite a data scientists
**enviar cómputos que otros ejecutan sin compartir los datos subyacentes**. Es el framework de
referencia en **ML federado** (federated learning) y computación privada.
La versión actual (`syft` **0.10+**) adoptó una API nueva respecto al legacy ≤0.9.

## Instalación y uso

```bash
pip install -U "syft[data_science]" "syft-rds"   # instalar el sync engine + dataset/jobs registry
```

```python
import syft as sy                       # motor de sync (nuevo)
from syft_rds import login_do, login_ds # datasets y jobs (login_do = data owner, login_ds = data scientist)
```

> Si dependes de la API legacy **≤0.9**, fija `syft<0.10` (la vieja API cambió).

## Arquitectura / Patrones reutilizables

- **Sync engine**: `import syft as sy` — los datasets y jobs viven en `syft-rds` (`from syft_rds import ...`).
- **Separación de roles**: `login_do` (dueño de datos) vs `login_ds` (científico). El dato nunca se transfiere,
  se envía el *cómputo* al dato (pattern submit-computation-to-data).
- **Privacidad por diseño**: aplicar modelos sobre datos que no ves — útil para proyectos que tratan
  datos sensibles (salud, movilidad personal, geo) sin exponerlos.
- Patrón de **training federado**: los workers entrenan localmente y solo comparten gradientes/actualizaciones.

## Pitfalls

- La API **cambió** entre ≤0.9 y 0.10: si copias código viejo, `syft-client` ya no aplica → usa `syft` + `syft_rds`.
- Requiere **Python 3.10+**.
- El flujo federado real necesita varios workers/nodos activos; para pruebas locales, levantar nodos de
  entrenamiento simulados (tutorial oficial) antes de esperar convergencia.

## Verificación

`pip install -U "syft[data_science]" "syft-rds"` + `import syft as sy; from syft_rds import login_do, login_ds`
debe ejecutarse sin error.

## Referencia

- Repo: https://github.com/OpenMined/PySyft
- Docs: https://docs.openmined.org
- PyPI: `syft` (0.10+), `syft-rds` (datasets/jobs)
