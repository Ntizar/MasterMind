# Cron failures — Lecciones aprendidas

## Problema: write_file falla en cron jobs por tamaño

Cuando un cron job intenta generar un HTML grande (>15KB) y falla con "write_file: missing required field 'content'" o "stream stalled mid tool-call", significa que el contenido excede el límite de contexto del cron agent.

## Solución

1. **Dividir en sub-sesiones más pequeñas** (1 tema por archivo HTML en lugar de 6 temas en uno)
2. **Generar directamente** en lugar de depender del cron cuando se necesita contenido inmediato
3. **Usar execute_code con write_file** en lugar de write_file directo del agent (el agent pierde el argumento content cuando el prompt es muy largo)

## Ejemplo

S04 (4º Primaria) tenía 6 temas en un solo HTML → reestructurado en 6 sub-sesiones de ~15KB cada una. Lo mismo para S01, S02, S03.

## Archivos generados

- `/root/workspace/matematicas/s04-1-fracciones-equivalentes.html` (18KB)
- `/root/workspace/matematicas/s01-1-contar-0-10.html` (14KB)
- `/root/workspace/matematicas/s01-2-contar-10-100.html` (15KB)
- `/root/workspace/matematicas/s01-3-sumar-hasta-10.html` (13KB)
- `/root/workspace/matematicas/s01-4-sumar-hasta-20.html` (11KB)
- `/root/workspace/matematicas/s01-5-restar-hasta-10.html` (12KB)
- `/root/workspace/matematicas/s01-6-restar-hasta-20.html` (10KB)
- `/root/workspace/matematicas/s01-7-figuras-basicas.html` (14KB)
- `/root/workspace/matematicas/s01-10-patrones.html` (12KB)

Plan completo en MEGA-PLAN.md con estructura reestructurada.