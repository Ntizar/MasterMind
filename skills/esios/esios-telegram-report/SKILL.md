---
name: esios-telegram-report
description: "Generar informe diario del mercado eléctrico español con gráficos Canvas/PNG y análisis automático vía Telegram — script esios-telegram.js."
version: 1.1.0
author: Ntizar
tags: [esios, telegram, cron, informe]

---

# Informe Diario ESIOS — Telegram con Gráficos

## Qué envía

1. **Texto resumen** con análisis automático del día (precios, demanda, renovables, CO2, interconexiones)
2. **5 gráficos PNG** generados con Canvas:
   - 💰 Precio PVPC horario
   - ⚡ Demanda real horaria
   - ☀️ Solar FV vs Demanda (comparativo)
   - 🔌 Interconexiones netas (Francia + Portugal, con negativos)
   - 🌍 CO₂ asociado a generación

## Estructura del script

`scripts/esios-telegram.js` — Node.js puro + canvas npm

### Dependencias
- `canvas` — generación de imágenes PNG
- `https` — llamadas API (sin dependencias externas)

### Variables de entorno
- `TELEGRAM_BOT_TOKEN` — token del bot
- `TELEGRAM_CHAT_ID` — chat de destino
- `ESIOS_API_TOKEN` — token ESIOS/REE

### Uso
```bash
node scripts/esios-telegram.js [YYYY-MM-DD]
# Sin fecha = ayer automáticamente
```

## Gráficos

Todos usan `drawLineChart()` con:
- Fondo oscuro `#0f172a`
- Líneas con relleno semitransparente
- Puntos en cada hora
- Ejes con valores formateados
- Leyenda inferior
- Estilo ESIOS dashboard (azul #2563eb, naranja #f97316)

### Opciones de drawLineChart
```javascript
drawLineChart(title, datasets, unit, { stacked: false, showZero: true })
```
- `stacked: true` — apilado (no se usa actualmente)
- `showZero: true` — línea de cero punteada para datos negativos

## Análisis automático

La función `analyzeDay()` calcula:
- Si precios fueron altos (>150), moderados (>100) o bajos
- Pico/valle de precios con hora
- Diferencia pico-valle
- Demanda media/máx/mín con horas
- % renovable sobre total
- Factor de emisión CO₂
- Balance neto exportación/importación
- Horas exportando de cada país

## Cron job

```yaml
job_id: 9e7570152a99
name: esios-daily-telegram
schedule: 0 9 * * *  (09:00 UTC = 11:00 Madrid verano / 10:00 invierno)
prompt: Ejecuta el script de resumen diario ESIOS: node /root/workspace/Koldo/scripts/esios-telegram.js
```

> **IMPORTANTE:** El cron debe apuntar a la **Koldo version** (`/root/workspace/Koldo/scripts/esios-telegram.js`), NO a la del dashboard. La versión del dashboard no carga `.env` ni `/proc/1/environ`, por lo que falla con "Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID".

## ⚠️ ESIOS API `/values` endpoint — 404 masivo (2026-06-16)

**Estado**: La API de ESIOS devuelve `{"status": 404, "message": "Not Found"}` para **todos** los endpoints `/indicators/{id}/values`, independientemente del indicador, fecha o método de llamada (`date=`, `date_start/end=`).

**Síntomas**:
- `GET /indicators/{id}/values?date=YYYY-MM-DD` → 404
- `GET /indicators/{id}/values?date_start=...&date_end=...` → 404
- `GET /indicators/{id}/values` (sin fecha) → 404
- `GET /indicators/{id}` (info del indicador) → OK
- `GET /indicators?filter=...` → OK
- Token funciona (403 sin token, 404 con token)

**Causas probables**:
1. API de ESIOS migró a nueva versión (endpoint v2 requiere token diferente)
2. Token caducado/restringido para endpoint de valores
3. Datos de 2026 no disponibles aún

**Fallback**: Usar cache local en `/root/workspace/esios-dashboard/data/esios-cache/` (archivos `{id}_{fecha}.json`). Verificar si hay datos válidos antes de intentar API.

**No capturar como restricción persistente**: Esto es un fallo temporal de la API, no una regla duradera.

## ⚠️ Script version mismatch — Solución definitiva (2026-06-17)

**Hay DOS versiones del script:**

1. **Dashboard version** (`/root/workspace/esios-dashboard/scripts/esios-telegram.js`) — simplificada, NO carga `.env`, NO lee `/proc/1/environ`. **NO USAR en cron.**
2. **Koldo version** (`/root/workspace/Koldo/scripts/esios-telegram.js`) — completa, con `.env` loading, `/proc/1/environ` fallback, `TELEGRAM_CHAT_ID` desde `TELEGRAM_HOME_CHANNEL`, gráficos PNG.

**Siempre ejecutar la Koldo version:**
```bash
cd /root/workspace/Koldo && node scripts/esios-telegram.js
```

**NUNCA ejecutar la del dashboard en cron** — siempre fallará con "Faltan TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID".

## Pitfalls

- **NUNCA usar IDs de generación medida por tecnología** (10035-10043) — devuelven null
- **Interconexiones son MWh/periodo** — dividir entre 1000 para MW
- **Solar medida (10205) es MW directo** — NO dividir
- **Valores negativos en interconexiones** = importación, mostrar línea de cero
- **El script usa `canvas` npm** — requiere instalación previa `npm install canvas`
- **Cache en /tmp/esios-telegram-cache/** — se limpia tras envío
- **Cron jobs no heredan variables del gateway** — el script lee `TELEGRAM_BOT_TOKEN` de `/proc/1/environ` y `TELEGRAM_CHAT_ID` de `/hermes-home/.env` como fallback
- **Ruta del script:** `/root/workspace/Koldo/scripts/esios-telegram.js` — SIEMPRE esta (Koldo version). La del dashboard NO funciona en cron.

## Formateo de unidades de potencia

- **NUNCA usar "k MW"** (ej: "30k MW" es incorrecto).
- Valores >= 1000 MW → mostrar en **GW** (ej: "30.0 GW").
- Valores < 1000 MW → mostrar en **MW** (ej: "500 MW").
- Función `fmtMW()` en el script implementa esta lógica: convierte automáticamente a GW cuando corresponde.
- En textos y captions, la función devuelve la unidad incluida ("30.0 GW" o "500 MW"), por lo que NO añadir "MW" manualmente después.

## Archivos del proyecto

- `scripts/esios-telegram.js` — script principal
- `data/esios-reference.json` — mapeo IDs útiles
- `data/esios-indicator-index.md` — índice robusto con unidades
- `data/all-esios-indicators.json` — todos los indicadores ESIOS

## Referencias

- `references/esios-api-values-404-2026-06-16.md` — Transcripción completa del fallo masivo de `/values` en ESIOS API