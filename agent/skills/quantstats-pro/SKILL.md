---
name: quantstats-pro
description: QuantStats Pro — librería de análisis cuantitativo y visualización de portfolios con métricas avanzadas.
category: data-science
---

# QuantStats Pro — Análisis Cuantitativo de Portfolios

## Qué es

QuantStats Pro es una librería de análisis cuantitativo que ofrece:
- **Performance metrics** — Sharpe ratio, Sortino, max drawdown, etc.
- **Visualization** — gráficos de rendimiento, drawdown, returns
- **Comparison** — comparar portfolios con benchmarks
- **Report generation** — generar reportes PDF/HTML

## Instalación

```bash
pip install quantstats
```

## Uso básico

```python
import quantstats as qs

# Calcular métricas de rendimiento
qs.reports.full(returns, benchmark=None)

# Generar reporte HTML
qs.reports.html(returns, output="report.html")

# Gráfico de drawdown
qs.plots.drawdown(returns)
```

## Casos de uso para David

- **Portfolio analysis** — analizar rendimiento de portfolios
- **Backtesting** — validar estrategias de inversión
- **Dashboard** — integrar métricas en dashboards
- **Monte Carlo** — combinar con simulador Monte Carlo

## Pitfalls

- Requiere datos de returns en formato pandas DataFrame
- Las métricas son estadísticas — no predicen futuro
- No incluye ejecución de trades — solo análisis
- Depende de pandas y numpy

## Referencias

- Repo: `github.com/diegoalvarezmgl/quantstats-pro` (12⭐)
- QuantStats original: `github.com/ranaroussi/quantstats`
