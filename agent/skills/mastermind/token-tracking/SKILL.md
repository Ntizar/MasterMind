---
name: token-tracking
description: >-
  Sistema de tracking de tokens y costes para sesiones en Hermes Agent/NaN.builders.
  Registra consumo de tokens por tarea/sesión, estima costes y genera dashboards.
domain: devops
author: David Antizar
version: 1.0.0
created: 2026-06-04
---

# Token Tracking — Sistema de Tracking de Tokens y Costes

## Propósito

Llevar un registro sistemático del consumo de tokens y costes asociados en todas las sesiones de Hermes Agent ejecutadas sobre NaN.builders. Permite identificar fugas de tokens, sesiones costosas y optimizar el uso del modelo.

## Ubicación de Archivos

| Recurso | Ruta |
|---------|------|
| **Log JSON** | `/hermes-home/tokens/tokens-log.json` |
| **Dashboard HTML** | `tokens/index.html` en el repo del proyecto |
| **Skill** | `/hermes-home/skills/mastermind/token-tracking/SKILL.md` |

## Formato de Registro (tokens-log.json)

El JSON es un **array plano** (no un objeto con `entries`):

```json
[
  {
    "date": "2026-06-04T10:30:00Z",
    "session_id": "sesion-inicial",
    "task": "Auditoría del sistema",
    "model": "qwen3.6",
    "input_tokens": 350000,
    "output_tokens": 7300,
    "total_tokens": 357300,
    "cost_estimate_usd": 0.179,
    "provider": "nan.builders"
  }
]
```

**⚠️ Pitfall:** El dashboard (tokens/index.html) tiene datos fallback embebidos en el `catch()` del fetch. Si añades una entrada al JSON, **también debes actualizar el fallback** para mantener consistencia. Verificar con: comparar entry counts y session_ids entre JSON y fallback.

### Campos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `date` | string (ISO 8601) | Fecha y hora del evento |
| `session_id` | string | Identificador opcional de sesión |
| `task` | string | Descripción breve de la tarea ejecutada |
| `model` | string | Modelo usado (ej: `qwen3.6`, `deepseek-v4-flash`) |
| `input_tokens` | int | Tokens de entrada estimados |
| `output_tokens` | int | Tokens de salida estimados |
| `total_tokens` | int | Suma de input + output |
| `cost_estimate_usd` | float | Coste estimado en USD |
| `provider` | string | Proveedor de API (ej: `nan.builders`) |

## Precios de Referencia (NaN.builders api.nan.builders/v1)

| Modelo | Input (por 1M tokens) | Output (por 1M tokens) |
|--------|----------------------|-----------------------|
| qwen3.6 (deepseek-v4-flash) | ~$0.50 | ~$0.50 |

Fórmula de coste:
```
coste = (input_tokens / 1_000_000) * precio_input + (output_tokens / 1_000_000) * precio_output
```

## Reglas de Tracking

1. **Mastermind registra cada tarea compleja** (>3 tool calls) al finalizarla
2. Cada entrada se añade a `/hermes-home/tokens/tokens-log.json`
3. Al final de cada sesión, si hay datos nuevos, se genera un breve resumen de costes
4. Las tareas simples (1-3 tool calls) se pueden agrupar en una sola entrada al final de la sesión
5. Si no se dispone de tokens exactos (API sin metadatos), se estiman basándose en:
   - Longitud aproximada del contexto de entrada (caracteres / 4 ≈ tokens)
   - Longitud de la respuesta generada

## Cómo Registrar una Entrada

**Desde Hermes Shell (CLI):**
```bash
# Usar jq para añadir entrada al array (formato plano, no { "entries": [...] })
INPUT=$(cat /hermes-home/tokens/tokens-log.json)
echo "$INPUT" | jq '. + [{
  "date": "'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'",
  "session_id": "ID_SESION",
  "task": "DESCRIPCIÓN DE LA TAREA",
  "model": "qwen3.6",
  "input_tokens": 350000,
  "output_tokens": 7300,
  "total_tokens": 357300,
  "cost_estimate_usd": 0.179,
  "provider": "nan.builders"
}]' > /tmp/tokens-tmp.json && mv /tmp/tokens-tmp.json /hermes-home/tokens/tokens-log.json
```

**⚠️ Recordatorio:** Tras actualizar el JSON, también actualizar el fallback en `tokens/index.html` (bloque `catch(function() { ... var ENTRIES = [...] })`).

**Desde el agente (Hermes):**
Añadir manualmente la entrada al JSON con `write_file` o `patch` sobre el archivo.

## Dashboard

El dashboard estático se encuentra en `tokens/index.html` dentro del repositorio del proyecto. Usa HTML+CSS+JS vanilla:

- **Fetch dinámico:** Carga `tokens-log.json` vía `fetch()` con fallback embebido para GitHub Pages (CORS)
- **Safe DOM:** Usa `textEl()` helper (document.createElement + textContent) — **NUNCA innerHTML**
- Muestra tabla de sesiones, totales acumulados, y gráfico de barras CSS
- Diseño responsive, tema oscuro, integrado con Aurora Design System
- Header fijo con links de navegación

## Verificación

Para verificar que el sistema funciona:
1. Confirmar que `/hermes-home/tokens/tokens-log.json` existe y es un JSON válido
2. Confirmar que `tokens/index.html` se despliega correctamente en NaN.builders
3. Tras registrar la primera entrada, comprobar que el dashboard la muestra

---

**Hecho con ❤️ por David Antizar**
**v1.0.0 — 2026-06-04**