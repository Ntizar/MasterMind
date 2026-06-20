# Macros Chart Implementation

## Implementación (2026-06-14)

Se añadió un gráfico de donut (Chart.js) en la tab Resumen que muestra la distribución de macronutrientes del día.

### Cálculo del TDEE

Usando fórmula Mifflin-St Jeor:
- Hombres: `10 × peso + 6.25 × altura - 5 × edad + 5`
- Mujeres: `10 × peso + 6.25 × altura - 5 × edad - 161`

TDEE = TMB × factor_actividad
- Sedentario: 1.2, Ligero: 1.375, Moderado: 1.55, Activo: 1.725, Intenso: 1.9, Muy intenso: 2.1

### Distribución de macros

Split 40/35/25 (proteínas/hidratos/grasas):
- Proteínas: `TDEE × 0.40 / 4` kcal→g
- Hidratos: `TDEE × 0.35 / 4` kcal→g
- Grasas: `TDEE × 0.25 / 9` kcal→g

### Código clave

```javascript
function renderMacrosChart(prot, hidr, grasa, objProt, objHidr, objGrasa) {
  if (appState.charts.macros) {
    appState.charts.macros.destroy();
    appState.charts.macros = null;
  }
  // Chart.js doughnut con cutout: 65%
  // Colores: #2563eb (prot), #f97316 (hidr), #22c55e (grasa)
  // Si totalActual === 0 → placeholder con data [0,0,0]
}
```

### Estado vacío

Cuando no hay comidas registradas, el donut muestra un placeholder con data [0,0,0] y leyenda sin tooltips.

### Dependencias

- Chart.js (ya incluido en el `<head>`)
- `var charts = window.charts = {}` — NUNCA `const charts`
