---
name: timesfm-forecast
description: "Usa a pronosticar series temporales con TimesFM 3.0."
version: "2.0.0"
tags: [timesfm, forecast, series-temporales, timesfm3, time-series, python]
related_skills: [timesfm-forecast, qlib-quant, monte-carlo-stock-simulator]
---

# TimesFM — forecasting de series temporales (API 3.0)

> ⚠️ Corrección 2026-09-05 (auditoría): la v1 usaba `timesfm.TimesFm`/`model.forecast()` (TimesFM v1/v2). La versión actual **3.0** usa `from timesfm3 import TimesFM3Evaluator, ModelConfig` y `forecaster.predict_batch(...)`. Install real: `pip install timesfm[torch]`.

**Repo:** `https://github.com/google-research/timesfm` (Python, ~31K⭐).

## When to Use

- Cuando pidas **pronosticar una serie temporal** (modelo fundacional de Google) para tus datos.

## Uso (API 3.0)

```bash
pip install "timesfm[torch]"
```

```python
from timesfm3 import TimesFM3Evaluator, ModelConfig
model = TimesFM3Evaluator(config=ModelConfig(...))
forecasts = model.predict_batch(inputs, horizon=..., return_quantiles=True)
```

## Pitfalls

- **Install** `pip install "timesfm[torch]"`, no `pip install timesfm`.
- API **3.0**: `TimesFM3Evaluator`/`predict_batch`; no `TimesFm/forecast/forecast_with_quantiles` (v1/v2).

## Verificación

- `predict_batch(inputs, horizon=N)` y comprobar el forecast + quantiles.
