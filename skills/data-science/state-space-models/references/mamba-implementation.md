# Implementación Completa — Mamba-2

**Fuente:** Note de sesión 2026-06-12  
**Archivo original:** `/hermes-home/notes/deep-learning/2026-06-12-state-space-models-mamba.md`

## Mamba2SSM — Bloque SSM con Mecanismo Selectivo

Implementación funcional de Mamba-2 con:
- Discretización ZOH
- Parámetros selectivos (B, C, Δ dependen de x)
- Conv1d short-cut para patrones locales
- Atención kernelizada reformulada como scan

## Mamba2Block — Bloque Completo

Incluye LayerNorm, Mamba2SSM, FFN con GELU, y residual connections.

## SimpleSSMForecaster — Predicción de Demanda Eléctrica

Forecaster para series temporales del sistema eléctrico español:
- Ventana de entrada: 168h (1 semana)
- Horizonte: 24-168h adelante
- Datos sintéticos estilo ESIOS con patrones diarios, semanales y estacionales

## Generación de Datos Sintéticos

Función `generate_electricity_data()` con:
- Ciclo diario (pico mañana/tarde, valle noche)
- Ciclo semanal (laboral vs fin de semana)
- Tendencia estacional (más demanda en invierno)
- Ruido realista

## Función de Ventanas

`create_windows(data, window_size=168, horizon=24)` para crear datasets de training con ventanas deslizantes.

## Referencias de Papers

1. Mamba: arXiv:2312.00752 — Gu & Dao (2023)
2. Mamba-2: arXiv:2405.21060 — Dao & Gu (2024)
3. S4: arXiv:2111.00396 — Gu et al. (2021)
4. VMamba: arXiv:2401.10166 — Liu et al. (2024)
5. RWKV-6: arXiv:2404.05892 — Peng et al. (2024)
6. Hyena: arXiv:2302.10866 — Poli et al. (2023)
7. Jamba: AI21 Labs (2024)