# Patrón: Calibración con Gaussian Process (auto-calibración continua)

Patrón para añadir un modelo ML alternativo (Gaussian Process) que corre junto al modelo principal y se auto-calibra durante uso normal.

## Arquitectura

```
GazeTracker ──GazeFeatures──▶ GazeRegressor (Ridge/polynomial) ──cursor principal
                                    │
                                    └───▶ GP Auto-calibration sample collector
                                              │
                                    (features → cursor_xy pairs when stable)
                                              │
                                    GPGazeRegressor (RBF/Matern kernel)
                                              │
                                    └───▶ predicción alternativa (retrain cada N frames)
```

## Implementación

### 1. Modelo serializable (`profiles/store.py`)

```python
class GPGazeModel(BaseModel):
    kernel_type: str = "RBF"
    lengthscale: float = 1.0
    noise_level: float = 0.1
    alpha: float = 1e-6
    feature_version: int = 1
    training_features: list[list[float]] = Field(default_factory=list)
    training_targets_x: list[list[float]] = Field(default_factory=list)
    training_targets_y: list[list[float]] = Field(default_factory=list)
    n_samples: int = 0
```

- Los GPs de sklearn NO son serializables → persistimos los ingredientes (X, y, hyperparams)
- Se reconstruye en runtime con `GaussianProcessRegressor(kernel=..., alpha=...)`
- Añadido como campo `gp_model: GPGazeModel` en `Profile`

### 2. Regressor con Kalman smoothing (`gaze/calibration.py`)

```python
class GPGazeRegressor:
    def __init__(self, gp: GPGazeModel, screen_size, kalman_params=None):
        self._gp = gp
        self._screen_w, self._screen_h = screen_size
        self._kalman = KalmanCursorFilter(kalman_params)
        self._gp_x, self._gp_y = None, None
        self._fit_gps()

    def _fit_gps(self):
        """Fit temporary GPs from stored training data for prediction."""
        if self._gp.n_samples < GP_MIN_SAMPLES:
            self._gp_x = self._gp_y = None
            return
        X = np.array(self._gp.training_features, dtype=float)
        yx = np.array(self._gp.training_targets_x, dtype=float).flatten()
        yy = np.array(self._gp.training_targets_y, dtype=float).flatten()
        kernel = _build_kernel(self._gp.kernel_type, self._gp.lengthscale, self._gp.noise_level)
        self._gp_x = GaussianProcessRegressor(kernel=kernel, alpha=self._gp.alpha, n_restarts_optimizer=0)
        self._gp_y = GaussianProcessRegressor(kernel=kernel, alpha=self._gp.alpha, n_restarts_optimizer=0)
        self._gp_x.fit(X, yx)
        self._gp_y.fit(X, yy)

    def predict(self, features):
        """Mirrors GazeRegressor.predict() API for swap-in compatibility."""
        ...

    def update(self, new_samples):
        """Add samples and retrain."""
        self._gp = update_gp_model(self._gp, new_samples)
        self._fit_gps()
```

### 3. Auto-calibración en runtime (`main.py`)

```python
# Init
if profile.gp_model.n_samples >= GP_MIN_SAMPLES:
    gp_regressor = GPGazeRegressor(profile.gp_model, screen_size)
gp_sample_buffer = []
gp_frame_counter = 0

# In tick():
if (gp_regressor is not None
        and fusion.sm.state == State.ACTIVE
        and cursor is not None
        and feats is not None):
    # Collect only when cursor is stable (movement < 15px) and confidence > 0.7
    if movement < 15.0 and feats.confidence > 0.7:
        sample = CalibrationSample(features=feats.vector, target_xy=(float(cursor[0]), float(cursor[1])))
        gp_sample_buffer.append(sample)
        gp_frame_counter += 1

        if gp_frame_counter >= GP_RETRAIN_INTERVAL:
            gp_regressor.update(gp_sample_buffer)
            gp_sample_buffer.clear()

        if now - gp_last_save >= GP_SAVE_INTERVAL:
            profile.gp_model = gp_regressor._gp
            save_profile(profile)
```

### 4. Constantes recomendadas

| Constante | Valor | Razón |
|-----------|-------|-------|
| `GP_MAX_SAMPLES` | 200 | Ventana deslizante — evita memory leak, mantiene datos recientes |
| `GP_MIN_SAMPLES` | 8 | Mínimo para que el GP tenga señal |
| `GP_RETRAIN_INTERVAL` | 30 frames (~1s) | Equilibrio entre adaptación y rendimiento |
| `GP_SAVE_INTERVAL` | 300s (5 min) | Persistencia periódica al perfil |
| Movement threshold | 15px | Solo muestras cuando cursor es estable |
| Confidence threshold | 0.7 | Solo muestras con buena detección de ojos |

### 5. Tests

Añadir tests en `tests/test_gaze_calibration.py`:
- Mínimo de samples requerido
- Modelo serializable (model_dump / model_validate)
- Predicción con modelo entrenado
- None cuando no entrenado
- Update con nuevas muestras
- Ventana deslizante (max samples)
- gp_model_has_data
- Método update del regressor
- Función module-level gp_predict
- Serialización JSON round-trip

## Pitfalls

- **sklearn GP no es serializable** — persistir ingredientes (X, y, hyperparams), reconstruir en runtime
- **GPs por eje** — entrenar uno para X y otro para Y, nunca un GP multivariado
- **n_restarts_optimizer=0 en runtime** — al pre-fit para predicción, no optimizar kernel cada frame
- **n_restarts_optimizer=3 en entrenamiento** — usar al entrenar/reentrenar para evitar mínimos locales
- **ConvergenceWarning** — si el lengthscale llega al límite inferior, escalar datos de entrada
- **CalibrationSample.target_xy** — debe ser `float`, no `int`, para evitar truncamiento
- **Feature version** — usar `build_gaze_design_vector()` con la versión correcta del modelo