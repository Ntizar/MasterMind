# Implementación KNN en FreeHands — Mejora #34

**Fecha:** 01/06/2026
**Proyecto:** FreeHands (`/root/workspace/FreeHands`)
**Skill:** `serializable-ml-models`

## Contexto

Reemplazar Ridge regression por KNN como alternativa de mapeo gaze en FreeHands. El proyecto ya soporta Ridge y GP (Gaussian Process). Se añade KNN como tercer tipo `knn_regression`.

## Archivos modificados

### `src/freehands/gaze/calibration.py`
- `fit_knn_model()` — Entrena KNeighborsRegressor para x e y por separado
- `GazeRegressor._build_knn_models()` — Construye KNN lazy desde datos almacenados
- `GazeRegressor._predict_knn()` — Predicción con KNN + Kalman smoothing
- `GazeRegressor.trained` — Propiedad que verifica `_knn_x`/`_knn_y`
- `KNN_DEFAULT_K = 5`, `KNN_MIN_SAMPLES = 6`

### `src/freehands/profiles/store.py`
- `GazeModel.weights_x` → `list[float] | list[list[float]]` (Union para compatibilidad)
- `GazeModel.bias_x` → `list[float] | float` (Union para compatibilidad)
- `GazeModel.bias_y` → `float | int` (k almacenado como float)
- Nuevos campos: `training_features`, `training_targets_x`, `training_targets_y`, `k`

### `src/freehands/gaze/__init__.py`
- Exports: `fit_knn_model`, `KNN_DEFAULT_K`, `KNN_MIN_SAMPLES`

### `tests/test_knn_calibration.py` (nuevo)
- 13 tests unitarios: mínimo samples, serialización, k custom, weights, predict, untrained, head pose, compressed predictions, uniform weights, clamping, different k values, model type, ridge regression still works

## Problemas encontrados y soluciones

### Pydantic strict validation
`GazeModel(weights_x=X.tolist())` fallaba con `ValidationError: Input should be a valid number` porque `X.tolist()` es `list[list[float]]` y el campo era `list[float]`.

**Solución:** Cambiar a `list[float] | list[list[float]]` en el schema Pydantic.

### Datos de entrenamiento en campos del regresor
El `GazeRegressor.__init__` lee directamente de `model.weights_x`, `model.weights_y`, `model.bias_x`, `model.bias_y`. No conoce campos `training_*` separados.

**Solución:** Almacenar datos de entrenamiento en los mismos campos que el regresor espera: `weights_x` = matriz X, `weights_y` = vector y_x, `bias_x` = vector y_y, `bias_y` = k.

### Tests existentes intactos
Todos los 26 tests de `test_gaze_calibration.py` siguen pasando. Los 24 fallos en el suite completo son preexistentes (dead zones, face tracker, gesture profiles, profiles store).

## Resultados

- **Tests:** 13 nuevos pasando + 26 existentes = 39/39 tests de calibración
- **Suite completa:** 398 passed (sin cambios en los 24 fallos preexistentes)
- **Ruff:** 1 error preexistente (`tongue_out` repeat en store.py), 0 nuevos errores
