---
name: timesfm-forecast
version: "1.0.0"
description: "TimesFM — Time Series Foundation Model de Google Research (22K⭐). Modelo fundacional pre-entrenado para forecasting de series temporales. 100M+ timepoints."
tags: [timeseries, forecasting, google, foundation-model, ml, prediction]
---

# TimesFM — Time Series Foundation Model

## Resumen

TimesFM (Time Series Foundation Model) de Google Research es un **modelo pre-entrenado** para forecasting de series temporales. Entrenado en **100 millones+ de timepoints** de diversas fuentes (dominios públicos).

## Características

- **Foundation model:** No necesitas entrenar — zero-shot forecasting
- **Multi-dominio:** Finanzas, energía, clima, IoT, tráfico, demanda
- **Escala:** 100M+ timepoints → cubre casi cualquier patrón
- **API simple:** `pip install timesfm` → `model.forecast()`

## Instalación

```bash
pip install timesfm
```

## Uso

```python
import timesfm

# Cargar modelo pre-entrenado
model = timesfm.TimesFm(
    hparams=timesfm.TimesFmHparams(
        backend="gpu",
        num_layers=20,
        context_len=512,
        horizon_len=128,
    ),
)

# Forecast
forecast = model.forecast(
    inputs=timeseries_data,  # shape: (batch, time, features)
    freq="D",                 # Daily
)

# Con quantiles
quantile_forecast = model.forecast_with_quantiles(
    inputs=timeseries_data,
    quantiles=[0.1, 0.5, 0.9],  # P10, P50, P90
    freq="H",  # Hourly
)
```

## Aplicaciones en Mastermind

- **ESIOS:** Forecast de demanda eléctrica horaria
- **Monte Carlo:** Como base de distribución temporal para simulaciones
- **Dashboard:** Integrar como componente de predicción en dashboards

## Referencia

- Repo: `google-research/timesfm`
- Paper: "A Decoder-only Foundation Model for Time-Series Forecasting"