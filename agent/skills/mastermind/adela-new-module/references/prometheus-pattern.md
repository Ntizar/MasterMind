# Patrón: Formato Prometheus Exposition para módulos Adela

## Resumen

Cuando un módulo Adela necesita exponer métricas en formato Prometheus-compatible, seguir este patrón:

## Estructura

```
src/
├── prometheus.ts   # toPrometheusFormat() + toPrometheusJSON()
└── metrics.ts      # createMetrics() que usa prometheus.ts internamente
```

## Funciones clave

### `toPrometheusFormat(snapshot: MetricsSnapshot): string`

Convierte un snapshot interno al formato texto plano de Prometheus:

```
# HELP app_peticiones Total de peticiones
# TYPE app_peticiones counter
app_peticiones 42
# HELP app_latencia_seconds Latencia en segundos
# TYPE app_latencia_seconds histogram
app_latencia_seconds_bucket{le="0.01"} 5
app_latencia_seconds_bucket{le="0.05"} 12
app_latencia_seconds_bucket{le="0.1"} 20
app_latencia_seconds_bucket{le="0.5"} 35
app_latencia_seconds_bucket{le="1"} 40
app_latencia_seconds_bucket{le="5"} 42
app_latencia_seconds_bucket{le="+Inf"} 42
app_latencia_seconds_sum 15.3
app_latencia_seconds_count 42
app_latencia_seconds 0.15
# HELP app_memoria_bytes Memoria usada
# TYPE app_memoria_bytes gauge
app_memoria_bytes 268435456
```

### `toPrometheusJSON(snapshot: MetricsSnapshot): Record<string, any>`

Versión JSON para endpoints `/metrics` que acepten JSON.

### Sanitización de nombres

Los nombres de métricas Prometheus solo pueden contener `[a-zA-Z_:][a-zA-Z0-9_:]*`.

**Regla:** Reemplazar cualquier carácter inválido con `_`. Ejemplo:
- `app mi-métrica!` → `app_mi_m_trica_`
- `http.request.duration` → `http_request_duration`

## Integración con Express

El middleware de métricas debe:
1. Registrar `req.method`, `req.path`, `res.statusCode`
2. Medir latencia con `Date.now()` delta
3. Actualizar histograma con la latencia
4. No bloquear la respuesta (solo actualizar estado interno)

## Test mínimo

Siempre incluir tests para:
1. Formato texto plano correcto
2. Sanitización de nombres
3. Buckets de histograma
4. Integración completa (metrics → snapshot → prometheus)
5. Versión JSON
