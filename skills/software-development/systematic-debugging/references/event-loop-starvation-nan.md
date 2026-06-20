# Caso de estudio: Colapso de event loop por concurrencia HTTP en NaN

## Contexto
Dashboard ESIOS se queda atascado en spinner de carga en móvil. Funciona en desktop.

## Diagnóstico

### Paso 1: Verificar si el servidor está vivo
```
curl -s https://esios-dashboard-ntizar-ntizar.apps.nan.builders/healthz
# → 200 OK (servidor vivo)

curl -s https://esios-dashboard-ntizar-ntizar.apps.nan.builders/readyz
# → 200 ready (token ESIOS configurado)
```

### Paso 2: Verificar el endpoint problemático
```
curl -s -w "HTTP: %{http_code} TIME: %{time_total}s" \
  "https://esios-dashboard-ntizar-ntizar.apps.nan.builders/api/esios/summary?fecha=2026-05-30"
# → 502 error code: 502 TIME: 3.97s
```

### Paso 3: Verificar que la API externa funciona
```
curl -s -H "x-api-key: $TOKEN" \
  "https://api.esios.ree.es/indicators/1000?start_date=2026-05-30T22:00:00&end_date=2026-05-31T22:00:00"
# → 200 OK (API ESIOS funciona)
```

**Conclusión**: Servidor vivo, API externa funciona, pero `/api/esios/summary` devuelve 502 → event loop colapsado.

### Paso 4: Analizar el código problemático
`src/domains/energy/summary.service.js` `buildSummary()`:
- Hace 4 batches en paralelo de ~8 indicadores cada uno
- Cada batch hace 8 llamadas HTTP simultáneas a ESIOS
- Total: 32 llamadas HTTP concurrentes
- En servidor de 1 vCPU (NaN), esto colapsa el event loop

### Paso 5: Verificar el impacto frontend
`public/js/data.js` `cargarDatos()`:
- Timeout de 30s en `Promise.race([summaryPromise, summaryTimeout])`
- Si el event loop está bloqueado, el timer de 30s nunca se ejecuta
- Resultado: loading spinner eterno sin error

## Fix aplicado

### Backend: `src/domains/energy/summary.service.js`
```javascript
// Antes: 4 batches en paralelo (32 llamadas simultáneas)
const batchResults = await Promise.all(
  batches.map(batch => fetchIndicatorBatch(batch, fecha, token))
);

// Después: max 2 batches simultáneos
const CONCURRENCY = 2;
for (let i = 0; i < batches.length; i += CONCURRENCY) {
  const slice = batches.slice(i, i + CONCURRENCY);
  const results = await Promise.all(slice.map(batch => fetchIndicatorBatch(batch, fecha, token)));
  results.forEach(r => Object.assign(allData, r));
}
```

### Frontend: `public/js/data.js`
- Timeout reducido de 30s a 20s
- Mensajes de error más claros con indicación de reintentar

## Lecciones

1. **Healthz no prueba endpoints con I/O** — un servidor puede responder a health checks pero colapsar en endpoints que hacen fetch
2. **Promise.all() es peligroso en 1 vCPU** — cada llamada HTTP consume CPU para parsing
3. **Los timeouts de Node.js necesitan el event loop** — si está bloqueado, los timers no se disparan
4. **El diagnóstico rápido**: healthz=200 + endpoint-fetch=502 = event loop colapsado
5. **Fix mínimo**: reducir concurrencia, no añadir más capas de abstracción

## Métricas

| Métrica | Antes | Después |
|---------|-------|---------|
| Llamadas HTTP simultáneas máx | 32 | ~16 |
| Batches en paralelo | 4 | 2 |
| Timeout frontend | 30s | 20s |
| Comportamiento en colapso | Spinner eterno | Error claro + retry |
