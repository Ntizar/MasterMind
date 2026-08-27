# ESIOS API /values 404 masivo — 2026-06-16

## Resumen

El 16 de junio de 2026, la API de ESIOS devuelve 404 para todos los endpoints `/indicators/{id}/values`.

## Evidencia

```bash
# Todos estos devuelven {"status": 404, "message": "Not Found"}
curl -s -H 'x-api-key: <TOKEN>' -H 'Accept: application/json' \
  'https://api.esios.ree.es/indicators/1001/values?date=2026-05-30'
curl -s -H 'x-api-key: <TOKEN>' -H 'Accept: application/json' \
  'https://api.esios.ree.es/indicators/10205/values'
```

## Lo que SÍ funciona

```bash
# Info del indicador → OK
curl -s -H 'x-api-key: <TOKEN>' 'https://api.esios.ree.es/indicators/1001'

# Listado de indicadores → OK
curl -s -H 'x-api-key: <TOKEN>' 'https://api.esios.ree.es/indicators?filter=precios'
```

## Fallback recomendado

Usar cache local en `/root/workspace/esios-dashboard/data/esios-cache/`:
- Archivos: `{id}_{fecha}.json`
- Estructura: `{ts, data: {indicator: {...}, values: [...]}}`
- Verificar si hay datos válidos antes de intentar API
