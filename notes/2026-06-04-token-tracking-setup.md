# Nota Inicial — Sistema de Tracking de Tokens y Costes

**Fecha:** 2026-06-04
**Autor:** Koldo vía David Antizar

## Contexto

Tras la auditoría completa del sistema NtizarBrainMasterMind v4.0 (puntuación 5.6/10), se identificó que una de las carencias más importantes era la **ausencia total de tracking de tokens y costes**.

No existía ningún mecanismo para medir:
- Cuántos tokens consume cada sesión
- Qué skill o tarea consume más
- Cuánto cuesta cada operación en NaN.builders

## Acción Realizada

Se ha creado un sistema de tracking de tokens completo:

1. **Skill Hermes:** `/hermes-home/skills/koldo/token-tracking/SKILL.md`
2. **Log JSON:** `/hermes-home/tokens/tokens-log.json` (con 2 entradas de ejemplo)
3. **Dashboard web:** `tokens/index.html` (estático, Aurora Design System)
4. **Reglas:** Koldo registra cada tarea compleja (>3 tool calls)

## Precios de Referencia (NaN.builders)

| Modelo | Input | Output |
|--------|-------|--------|
| qwen3.6 / deepseek-v4-flash | $0.50/1M tokens | $0.50/1M tokens |

## Próximos Pasos

- Revisar el dashboard cada semana para detectar fugas de tokens
- Ajustar skills que consuman demasiado contexto
- Si el coste mensual supera $10, considerar optimización agresiva

---

**Hecho con (L) por David Antizar**