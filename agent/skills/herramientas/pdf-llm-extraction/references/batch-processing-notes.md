# Batch Processing Notes — v4.0 (270 PDFs CIAF)

## Configuración final
- **Text limit:** 60,000 chars (antes 28K)
- **max_tokens:** 8,192 (antes 4,000)
- **Throttle:** 1.5s entre requests
- **Modelo:** qwen3.6 vía NaN API
- **Temperature:** 0.1
- **Fuente:** `/root/workspace/CIAF/` (2007-2025, 270 informes)

## Análisis de longitudes de texto (Fase 0)
```
PDFs muestreados: 54
Mínimo: 13,402 chars
Máximo: 266,290 chars
Promedio: 59,836 chars
Mediana: 47,788 chars
P90: 100,430 chars
P95: 143,250 chars
→ Límite elegido: 60,000 chars
```

**Lección:** El P95 es 143K pero 60K es un buen compromiso. Los PDFs más grandes (200K+) tienen mucho texto repetido o格式 de tablas que el LLM no necesita. Las secciones clave (conclusiones, recomendaciones) suelen estar en los primeros 60K chars.

## Resultados v4.0
- **Procesados:** 231/232 (1 error API timeout)
- **Tiempo total:** 71 minutos 25 segundos
- **Errores:** 1 (API 524 timeout, retry manual fixeado)
- **Tasa de éxito:** 99.6%

## Estadísticas consolidadas
- **Total informes:** 270
- **Conclusiones:** 713
- **Recomendaciones:** 438
- **Trenes:** 381
- **Víctimas:** 517
- **Con GPS:** 8
- **Por tipo:** 134 accidentes, 71 incidentes, 51 descarrilamientos, 9 colisiones

## Errores encontrados y fixes

### 1. API 524 timeout (1 caso)
- **Archivo:** IF060912300713CIAF.pdf (2012)
- **Causa:** API de NaN temporalmente caída
- **Fix:** Retry manual con el mismo script
- **Resultado:** 5 conclusiones, 6 recomendaciones

### 2. NoneType en span["text"] (0 en v4.0)
- **Causa:** PyMuPDF retorna None en algunos PDFs
- **Fix:** `span.get("text") or ""` (ya estaba en el código desde v3.0)
- **Resultado:** 0 errores de este tipo en v4.0

## Patrón de batch exitoso

```python
# Configuración óptima para 200+ PDFs
TEXT_LIMIT = 60000
MAX_TOKENS = 8192
THROTTLE = 1.5  # segundos
TEMPERATURE = 0.1
TIMEOUT = 180  # segundos por request

# Progress tracking
elapsed = time.time() - start_time
avg = elapsed / max(i, 1)
eta = avg * (total - i)
eta_str = f"~{int(eta//60)}m{int(eta%60):02d}s"
print(f"[{i+1}/{total}] {filename} — {eta_str}")
```

## Directorios de salida
- **Individuales:** `/root/workspace/ciaf-data/data/individual/*.json` (270 archivos)
- **Consolidado:** `/root/workspace/ciaf-data/data/reports.json` (v4.0, 763KB)
- **Dashboard:** `/root/workspace/ciaf-data/dashboard/data/reports.json` (copia)

## Repos actualizados
- `Ntizar/PdfToJson` → batch-final.py
- `Ntizar/ciaf-data` → 270 JSONs + reports.json v4.0
