# 2026-09-02 — Colapso del gateway: el token de Telegram revocado y los ángulos muertos del doctor

## Qué pasó

El token del bot @NtizarBot fue revocado en Telegram. Consecuencia en cascada:

1. El gateway **muere al arrancar** con error non-retryable ("Telegram bot token
   rejected") — no reintenta, se apaga.
2. Todos los crons que entregan a Telegram (Gobierno IA ×4, kit72h-vigilante,
   digest…) fallaban la entrega con `Unauthorized` desde hacía ~1 día.
3. El escáner seguía corriendo y generando contenido: el sistema estaba cuerdo
   pero mudo.

## Por qué no se detectó antes (los 3 ángulos muertos)

1. **doctor.py leía `cron/jobs/*/job.json` — una estructura que NUNCA existió**
   (Hermes guarda todo en `cron/jobs.json`). El glob devuelve vacío → cero checks
   `cron:` → el doctor daba OK en silencio. Bug en el detector, no en el sistema.
2. **Nada verificaba la salud del token** contra la API real de Telegram.
3. **Nada vigilaba al gateway fuera del gateway** — si el gateway muere, sus
   propios crons de vigilancia mueren con él (bombero dentro de la casa).

## Qué se hizo (restauración)

- Token nuevo de @BotFather (bot renace como @Ntizarbot, ID 8925992141) → `.env`
  → gateway arriba → prueba real `sendMessage` entregada.
- El token viejo del `.env` era idéntico al que David reenvió primero: comparar
  la ID de bot (prefijo del token) delata si es el revocado.

## Qué se blindó (para que no vuelva a ser invisible)

| Capa | Qué hace | Dónde |
|---|---|---|
| `doctor.py` check `telegram-token` | `getMe` en directo contra Telegram: 401 = fallo con instrucción de recuperación | scripts/ |
| `doctor.py` check `cron:*` (reescrito) | Lee `jobs.json` REAL: run en error, **entrega caída** (aviso), sin disparar >2h (= gateway muerto) | scripts/ |
| `doctor.py` checks `vigia-cron` + `vigia-gateway` | Verifican que los VIGÍAS siguen declarados (un PC nuevo los pierde) | scripts/ |
| `Hermes_Gateway_Watchdog` (Task Scheduler, cada 10 min) | Vive FUERA del gateway: relanza si muere, distingue "gateway caído" de "token revocado" y avisa por Telegram (con fallback: si Telegram no conecta, el aviso lo dice) | scripts/vigia-gateway.ps1 + registrar-vigia-gateway.ps1 |
| `test-doctor.py` +5 casos | Inyección de: token revocado, entrega caída, sin-disparar, last_status error — 12/12 verde | scripts/ |

Lección de gobierno de crons: el Pase de lista (10:00) coincidía con doctor y
Consejo → 429 de concurrencia NaN (max 5). Movido a 10:15.

## Regla operativa nueva

Tras CUALQUIER problema de entrega/gateway, el orden de diagnóstico es:
`hermes gateway status` → `logs/gateway.log` (buscar "telegram connected") →
`doctor.py` (checks telegram-token y cron:*). Los tres en verde y no llega
mensaje = David no ha hecho `/start` al bot nuevo.
