---
name: quantstats-pro
description: "Use al analizar backtests y generar tearsheets de portfolios."
version: "2.0.0"
tags: [quant, finance, portfolio-analytics, tearsheet, monte-carlo, backtesting, python]
license: Apache-2.0
author: Mastermind (stars-explorer)
metadata:
  hermes:
    tags: [quant, finance, portfolio-analytics, tearsheet, monte-carlo]
    related_skills: [monte-carlo-stock-simulator, qlib-quant]
---

# QuantStats Pro — Análisis cuantitativo de portfolios

**Repo:** github.com/diegoalvarezmgl/quantstats-pro (23⭐, Python, Apache-2.0, beta, push jul-2026)
Drop-in replacement mantenido del QuantStats original de ranaroussi: mismo `import quantstats as qs`, métricas endurecidas y capa de reporting que va más allá del original.

## ⚠️ Nota de upgrade (2026-09-04)

Este skill fue reescrito tras auditar el README real. La v1 (maratón 2026-06-18) estaba inventada: decía `pip install quantstats` (el paquete es `quantstats-pro`), 12⭐ (son 23⭐) y describía el paquete upstream, no Pro. Lección aplicada del pitfall "skills-v1 inventados" de stars-explorer.

## Cuándo usarlo

- Validar backtests de estrategias (rentabilidades diarias → tearsheet HTML compartible)
- Informes de riesgo para clientes/inversión: Monte Carlo forward, decay de alfa
- Dashboard de seguimiento de portfolio (se integra con `monte-carlo-stock-simulator` y `qlib-quant`)

## Instalación

```bash
pip uninstall quantstats         # OBLIGATORIO: comparten namespace `quantstats`, no coexisten
pip install quantstats-pro
```

## Módulos del paquete

| Módulo | Propósito |
|---|---|
| `quantstats.stats` | 50+ métricas (Sharpe, Sortino, drawdown, VaR, …) |
| `quantstats.plots` | Visualizaciones (returns, drawdown, heatmaps, rolling stats) |
| `quantstats.reports` | Tearsheets HTML y tablas de métricas |
| `quantstats.montecarlo` | Motor de simulación forward multi-modelo (nuevo; el legacy shuffle-based queda en `qs.stats.montecarlo()`) |
| `quantstats.alphadecay` | Diagnóstico rolling de decaimiento de alfa a corto horizonte |
| `quantstats.utils` | Preparación de datos, `download_returns`, helpers pandas |

## Quick start

```python
import quantstats as qs

qs.extend_pandas()                          # habilita returns.sharpe() etc.
returns = qs.utils.download_returns("QQQ")  # Series de rentabilidades

qs.stats.sharpe(returns)                    # métrica suelta
qs.plots.snapshot(returns, title="QQQ", show=True)
qs.reports.html(returns, "SPY", output="qqq_full.html")   # tearsheet clásico vs benchmark
```

## Los 4 tearsheets HTML (superficie de producto)

| Función | Uso | Open-source |
|---|---|---|
| `qs.reports.html(...)` | Tearsheet completo clásico (rediseñado v0.2.0+) | ✅ |
| `qs.reports.html_simple(...)` | Curva de equity lean para revisión rápida | ❌ Pro |
| `qs.reports.html_montecarlo(...)` | Riesgo forward multi-modelo: P(bust)/P(goal), consenso entre modelos, stress envelope (horizonte 1a por defecto) | ❌ Pro |
| `qs.reports.html_alpha_decay(...)` | Monitor de salud rolling: 10 métricas × ventanas 7/15/30d, semáforos z-score, detección CUSUM, time-underwater | ❌ Pro |

```python
qs.reports.html_montecarlo(returns, bust=-0.25, goal=0.50, sims=500, seed=42,
                           output="qqq_montecarlo.html")
qs.reports.html_alpha_decay(returns, windows=(7, 15, 30), output="qqq_alpha_decay.html")
```

Todos abren en el navegador por defecto; con `output="path.html"` se guardan a disco.

## Mercados 24/7 (cripto)

Para datos diarios de cripto pasar `periods_per_year=365` a reports y stats que anualizan (por defecto asume 252 días bursátiles):

```python
returns = qs.utils.download_returns("BTC-USD")
qs.reports.html(returns, periods_per_year=365, output="btc.html")
```

## Pitfalls

- **Colisión de namespace**: no se puede tener `quantstats` y `quantstats-pro` instalados a la vez — desinstalar el original primero o el import carga quién sabe cuál.
- **Pro gating**: 3 de los 4 tearsheets (simple, montecarlo, alpha_decay) son de pago. Lo libre es el clásico completo + stats/plots. Encaja con la regla "solo gratuito" de David: planificar pipelines sobre `html`/`stats`/`plots` y tratar los Pro como mejora opcional.
- **Beta (Development Status 4)**: API en movimiento, roadmap activo — fijar versión en requirements.
- **Formato de datos**: exige Series pandas de rentabilidades (no precios); anualizaciones mal configuradas inflan Sharpe en datos intradía.
- Repo pequeño (23⭐): menos battle-testing que el upstream; validar métricas críticas contra el original si hay dudas.

## Verificación

```bash
python -c "import quantstats as qs; print(qs.__version__ if hasattr(qs,'__version__') else 'ok')"
python -c "import quantstats as qs; r=qs.utils.download_returns('QQQ'); print(round(qs.stats.sharpe(r),3))"
```

## Referencias

- Repo: https://github.com/diegoalvarezmgl/quantstats-pro
- Docs Monte Carlo: docs/montecarlo.md · Alpha Decay: docs/alphadecay.md
- Upstream original: https://github.com/ranaroussi/quantstats
- Ejemplo tearsheet interactivo: via htmlpreview.github.io sobre docs/tearsheet.html
