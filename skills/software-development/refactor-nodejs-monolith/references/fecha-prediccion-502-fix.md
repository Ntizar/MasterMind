# Predicción Monte Carlo — Fecha correcta

## Problema original
El frontend llamaba `/api/esios/prediccion?fecha=getTomorrowStr(fecha)` — es decir, si el usuario selecciona hoy, se pide prediccion para mañana. Como mañana no tiene datos → 502.

## Solución
El endpoint `/api/esios/prediccion?fecha=X` ejecuta Monte Carlo con los últimos 7 días de historia ANTES de la fecha X. **No necesita datos futuros**.

### Reglas
1. **Siempre pasar la MISMA fecha** que seleccionó el usuario, no el día siguiente.
2. `shouldFetchPrediccion(fecha)` debe permitir cualquier fecha dentro de los últimos 7 días (no solo hoy/ayer).
3. El 502 ocurre cuando se pasa una fecha sin 7 días de historial previo.
4. El frontend debe manejar el 502 gracefully: `renderMonteCarlo(null)` maneja datos ausentes.

### Implementación correcta
```javascript
// utils.js
function shouldFetchPrediccion(fecha) {
  const today = getMadridDateStr();
  const sevenDaysAgo = getMadridDateStr(-7);
  return fecha >= sevenDaysAgo && fecha <= today;
}

// data.js — pasar la MISMA fecha, no getTomorrowStr
if (shouldFetchPrediccion(fechaFinal)) {
  promises.push(apiFetch('prediccion', fechaFinal, signal));
}
```

## Lección
El Monte Carlo funciona con HISTORIAL, no con datos futuros. No hay razón para pedir prediccion para mañana — la predicción de mañana ya está incluida en los datos de hoy.