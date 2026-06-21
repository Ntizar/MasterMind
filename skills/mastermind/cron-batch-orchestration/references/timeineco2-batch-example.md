# TimeIneco2 — Cron Batch Orchestration en Acción

**Fecha:** 21/06/2026  
**Tipo:** Ejemplo real de batch de 16 crons one-shot secuenciales

## Contexto

David quiere evolucionar TimeIneco (visor de isocronas) a la herramienta definitiva de planes de movilidad en 24h, sin intervención manual. Solución: fork + 16 crons one-shot programados.

## Ejecución

1. **Repo original:** `Ntizar/TimeIneco` (v1.3) — NO tocar
2. **Fork creado:** `Ntizar/TimeIneco2` vía GitHub API (`urllib.request`)
3. **Copia manual:** rsync de archivos (sin .git), git init, push
4. **16 crons creados:** cada uno con prompt autocontenido, horario escalonado 18:00→09:00 UTC
5. **Plan guardado:** `CRONS-PLAN.md` en el repo fork

## Lecciones

- El token de GitHub aparece truncado en algunos logs (`ghp_gG...wMGe`) — siempre leer completo desde `/hermes-home/.env`
- `gh` CLI no está instalado en este entorno — usar API REST directamente
- `shutil.rmtree()` necesario antes de clonar si el directorio ya existe
- Los crons se ejecutan en sesión aislada: cada uno clona, trabaja, y push — no hay estado compartido entre sesiones
