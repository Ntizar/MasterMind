---
name: synthetic-tabular-data-evaluation
description: "Evalúa datos tabulares sintéticos: parecido y privacidad."
version: "1.0.0"
author: "Mastermind (David Antizar)"
license: MIT
metadata:
  hermes:
    tags: [datos-sinteticos, evaluacion, privacidad, rgpd, tstr, mia, ctgan]
    related_skills: [auto-bayesian, deep-learning-fundamentals, pysyft-federated-ml]
---

# Evaluación de datos tabulares sintéticos

Metodología y scripts para medir si un dataset sintético **sirve** (utilidad) sin **filtrar** los datos reales (privacidad), en tres dimensiones: *resemblance*, *utility* y *privacy*.

## When to Use (cuándo usarlo)

- Antes de **publicar o compartir** un dataset sintético (RGPD): medir fuga y pérdida de utilidad, no solo correlaciones.
- Comparar generadores (copulas, SDV, CTGAN, ydata-synthetic).
- Justificar por escrito la calidad de datos anonimizados/sintéticos en un informe.

## Estructura del repo

10 scripts Python bajo `EVALUATION FUNCTIONS/` (RESEMBLANCE, UTILITY, PRIVACY) + `PREPROCESSING/`, con **108 notebooks** y **6 datasets reales** de ejemplo (uno por caso A–F: diabetes, cardio, obesity, contraceptive, Pima Indians, liver patient).

- **Resemblance**: `compute_mra_score(real, synthetic)` con `get_numerical_correlations` / `get_categorical_correlations`; `dra_distance(real, synthetic)` con `pca_transform` / `isomap_transform`; `mix_data()` / `split_data()` para *Data Labelling Analysis* (DLA).
- **Utility**: `train_evaluate_model(model_name, x_train, y_train, x_test, y_test)` + `initialize_model()` → comparar **TRTR** (train/test real) vs **TSTR** (entrenar con sintético, testar con real).
- **Privacidad**: `pairwise_euclidean_distance`, `hausdorff_distance`, `rts_similarity` (`similarity_evaluation.py`) + `membership_inference.py` y `attribute_inference.py` (ataques MIA / AIA).

Generadores en `requirements.txt`: copulas (Gaussian Multivariate), `sdv`, `ctgan`, `ydata-synthetic` (WGANGP). Datasets de ejemplo: diabetes 130-US hospitals, cardiovascular, obesity levels, contraceptive, Pima Indians, Indian Liver Patient.

## Patrón reutilizable

Aplicar la taxonomía **resemblance / utility / privacy** como checklist antes de publicar cualquier dato sintético:
1. ¿Se parece a los reales? (MRA, DRA)
2. ¿Sirve para entrenar? (TSTR vs TRTR)
3. ¿Deja escapar individuos? (distancias, `rts_similarity`, MIA, AIA)

Citar el paper asociado: *Methods of Information in Medicine*, DOI `10.1055/s-0042-1760247`.

## Pitfalls

- Un buen *resemblance* **no implica** privacidad: son ejes independientes, hay que reportar los tres.
- Los umbrales de MIA/AIA dependen del modelo atacante elegido → documentar la configuración para que el resultado sea comparable.
- Los nombres de fichero llevan espacios (`EVALUATION FUNCTIONS/`) — citarlos siempre entre comillas en scripts.

## Referencia

- Repo: `Vicomtech/STDG-evaluation-metrics` (~36 ⭐, Python/Jupyter, consultado 2026-09-15).
