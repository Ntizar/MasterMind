---
name: auto-bayesian
description: "AutoML interpretable con redes bayesianas relacionales."
version: "1.0.0"
tags: [mlops, bayesian-network, automl, interpretable-ml, explainable-ai, tabular, pgmpy, xai]
---

# auto-bayesian — AutoML interpretable con redes bayesianas relacionales

Repo: `github.com/SantanderAI/auto-bayesian` (41⭐, Python 3.12+, Apache-2.0, open source de Santander AI Lab, push activo 2026-09).
**Qué resuelve:** entrenar clasificadores binarios sobre VARIAS tablas relacionadas (leads→customers→interacciones) cuyo output NO es una caja negra: cada nodo del grafo lleva una tabla de probabilidad condicional legible, p.ej. `P(Convierte=1 | Fuente=referral, Región=oeste) = 0.85`, más un diagrama Mermaid del grafo aprendido.

## Cuándo usarlo (y cuándo no)

- ✅ Lead scoring, churn, next-best-action donde hay que **explicar a negocio/regulador** por qué
- ✅ Datos relacionales (varias tablas con claves) sin montar un feature store
- ✅ Dataset binario pequeño-mediano en CSV/Parquet local
- ❌ Regresión, multiclase, imágenes, texto (solo clasificación binaria y next-best-action binario)
- ❌ Cuando max-AUC sea lo único que importa → XGBoost/LightGBM gana; aquí se sacrifica algo de accuracy por transparencia
- ❌ Más de un padre por tabla (límite: cada tabla tiene ≤1 relación padre) y el target DEBE estar en la tabla raíz

## Pipeline end-to-end (el patrón reutilizable)

```
TOML declarativo → validate-schema → materialize (joins+agregados)
→ train (3 candidatos: Naive Bayes, TAN, Hill-Climb; selección por ROC-AUC o PR-AUC)
→ umbral afinado por F1 → predict / explain (Mermaid + lenguaje llano)
```

1. **CLI** (`uv run auto-bayesian <cmd>`):
```bash
uv run auto-bayesian validate-schema examples/lead_scoring.toml
uv run auto-bayesian materialize examples/lead_scoring.toml
uv run auto-bayesian train examples/lead_scoring.toml
uv run auto-bayesian predict artifacts/lead_scoring artifacts/lead_scoring/materialized.parquet
uv run auto-bayesian explain artifacts/lead_scoring --output explanation.md
```

2. **Config TOML** (tablas + relaciones + agregados por tabla hijo):
```toml
[task]
root_table = "leads"
target_column = "converted"
positive_label = "1"

[preprocess]
numeric_bins = 4        # binning cuantile o supervisado (target-aware)
max_categories = 10     # capping de categorías raras

[[tables]]
name = "interactions"
path = "data/interactions.csv"
primary_key = "interaction_id"
timestamp_column = "event_time"

[[relations]]
parent = "leads"
child = "interactions"
parent_key = "lead_id"
child_key = "lead_id"
kind = "one_to_many"
aggregations = [
  { op = "count", name = "interaction_count" },
  { column = "channel", op = "latest", name = "latest_channel" },
]
```
Ops soportadas: `count, nunique, sum, mean, min, max, latest`. Rutas se resuelven relativas al TOML.

3. **API Python** (sin TOML, desde DataFrames):
```python
from auto_bayesian import build_project, fit_tables, load_project, fit_project
model = fit_tables(project, {"leads": df_leads, ...})   # o load_project + fit_project
model.describe().selected_candidate
[(c.name, c.roc_auc) for c in model.describe().candidates]
```

4. **Explicabilidad**: `generate_explanation(model, output_path)` y `to_mermaid(model)` — flecha `A --> B` = dependencia probabilística directa; target resaltado. En GitHub/Markdown el Mermaid se renderiza solo → encaja con informes HTML/dashboards del stack de David.

5. **Artefactos** en `output_dir`: `materialized.parquet`, `metrics.json`, `network.json`, `model.pkl`.

## Por qué es interesante como patrón (más allá de la librería)

- **AutoML declarativo config-first**: el TOML ES el experimento (versionable en git, reproducible con `random_seed`) — patrón exportable a cualquier pipeline ML propio
- **Selección automática de métrica por desbalance**: PR-AUC si el positivo es raro + umbral afinado por F1 en vez del 0.5 fijo
- **Preprocesado determinista**: binning cuantile/target-aware, rare-category capping, missing handling, outlier removal y poda por correlación opcionales
- **Alternativa a Featuretools/Deep Feature Synthesis** para materializar agregados one-to-many, pero con contrato de esquema explícito

## Pitfalls

- **Alpha (v0.1)**: "Development Status :: 3 - Alpha" — API puede romperse; pinear versión
- `model.pkl` es pickle: `AutoBayesModel.load()` solo sobre directorios propios/de confianza (ejecución de código arbitrario)
- `one_to_many` exige agregados o features de secuencia explícitos — si no, falla el materialize
- CLI `predict` NO materializa: espera tabla ya materializada
- Depende de `pgmpy` como único motor; binning agresivo (numeric_bins=4) puede destruir señal en features muy informativas → subir bins y comparar candidatos
- Notebook de ejemplo (Olist Kaggle) necesita credenciales `~/.kaggle/kaggle.json` + `pip install -e ".[examples]"`

## Verificación

Tras entrenar: (1) `metrics.json` existe y el candidato seleccionado tiene AUC > base rate obvio, (2) abrir `explanation.md` y comprobar que las CPD del nodo target son legibles y plausibles (una regla por fila), (3) scorear 10 filas a mano desde el `network.json` y contrastar con `predict` — con CPD explícitas esto es auditable al 100%.

## Referencias

- Repo: https://github.com/SantanderAI/auto-bayesian — README + `DOCUMENTATION.md` (21 secciones con matemáticas paso a paso: Bayes, DAGs, CPDs, métricas) — la documentación didáctica es buen modelo para skills/notas propias
- Ejemplos: `examples/lead_scoring.toml`, `examples/notebooks/olist_relational_quickstart.ipynb`
- Colectora hermana del laboratorio: `SantanderAI/sota-stressed-datasets` (datasets estresados para robustez — ver registry skip 2026-09-02)
