---
name: qlib-quant
version: "1.0.0"
description: "Qlib — plataforma de inversión cuantitativa con IA de Microsoft (44K⭐). Modelos ML, factor mining, backtesting, RL trading."
tags: [finance, quant, trading, machine-learning, deep-learning, backtesting, microsoft]
---

# Qlib — AI Quantitative Investment Platform

## Resumen

Qlib es una plataforma open-source de Microsoft para **inversión cuantitativa con IA**. Cubre todo el pipeline: desde adquisición de datos hasta producción de estrategias de trading.

## Capacidades

- **Data:** Download, procesamiento, almacenamiento de datos financieros
- **Factor mining:** Extracción automática de factores con RD-Agent
- **Modelos:** LSTM, GRU, Transformer, LightGBM, RL agents
- **Backtesting:** Simulación de estrategias con datos históricos
- **Portfolio optimization:** Sharpe ratio, VaR, CVaR
- **RL trading:** Entrenamiento de agentes RL para trading

## Instalación

```bash
pip install pyqlib
```

## Uso básico

```python
import qlib
from qlib.config import REG_CN
from qlib.data import D

# Inicializar
qlib.init(provider_uri="~/.qlib/qlib_data/cn_data", region=REG_CN)

# Cargar datos
data = D.features(["SH600519"], ["Ref($close, -2) / Ref($close, -1) - 1"], start_time="2020-01-01", end_time="2020-12-31")
```

## Integración con Mastermind

- Usar `qlib-quant` para análisis de mercados financieros
- Integrar con `esios-indicators-correct` para energía
- Backtesting de estrategias híbridas (energía + mercados)

## Referencia

- Repo: `microsoft/qlib`
- Docs: https://qlib.readthedocs.io
- RD-Agent: https://github.com/microsoft/RD-Agent