# Stars Explorer — Fix Completo (2026-07-10)

## Problemas detectados y arreglados

### 1. Skill `stars-explorer` no cargaba en el cron
- **Problema:** El skill estaba en `agent/skills/mastermind/stars-explorer/` pero el resolver del cron busca solo en `agent/skills/<name>/`
- **Fix:** Symlink creado: `agent/skills/stars-explorer` → `mastermind/stars-explorer/`
- **Estado:** ✅ Arreglado

### 2. DB session_search corrupta
- **Problema:** `/persistrepo raíz/state.db` (1.7GB) con corrupción masiva en árboles B-tree de tablas FTS
- **Causa:** Probablemente disco lleno (94%) + WAL sin checkpoint
- **Fix:** 
  - Recuperadas 125K de 128K mensajes (97%)
  - Reconstruidas 754 sesiones desde session_ids en mensajes
  - FTS index reconstruido desde cero (125K entries)
  - DB nueva: 760MB, integridad OK
  - WAL checkpointeado
- **Datos perdidos:** 3K mensajes, metadata completa de sesiones (reconstruida parcialmente)
- **Estado:** ✅ Funcional (session_search funciona sin errores)

### 3. Cron `deep-learning` fantasma eliminado
- **Problema:** Cron `deep-learning` (job 20e1c2c4adde) fue eliminado pero había generado 26 notas educativas (Jun 12 - Jul 9)
- **Fix:** Recreado como `deep-learning-diario` (job d9519a72452a) a las 03:30 UTC
- **Mejora:** Offset de 30 min respecto al stars-explorer (03:00) para evitar solape
- **Prompt actualizado:** Incluye lista de 26 temas ya cubiertos para no repetir
- **Estado:** ✅ Recreado, arranca mañana 03:30 UTC

### 4. Registry con repos huérfanos
- **Problema:** 10 repos huérfanos a nivel raíz del registry (escritos por el agente del cron, no por el script)
- **Fix:** Eliminados, registry ahora tiene estructura limpia: `processed` (238 repos), `stats`, `last_run`
- **Estado:** ✅ Limpio

### 5. Nuevas stars no procesadas
- **Problema:** 4 nuevas stars detectadas que el cron no había procesado
- **Fix:** Ejecutado manualmente, procesadas las 4:
  - **scroll-world** (483⭐) → skill `scroll-world-3d-landing` (creative)
  - **gtfs-box** (18⭐) → skill `gtfs-box-3d-viewer` (geospatial)
  - **rs-change-detection** (3⭐) → skill `rs-change-detection-satellite` (geospatial)
  - **ChakraCore** (9260⭐) → SKIP (legacy JS engine)
- **Estado:** ✅ Procesadas

### 6. ChromaDB no estaba corriendo
- **Fix:** Iniciado con `start-chromadb.sh`, re-indexado: 219 skills
- **Estado:** ✅ Funcionando

### 7. Disco /persist al 100%
- **Problema:** Partición /persist (20GB) estaba llena
- **Fix:** 
  - Eliminado LSP node_modules (106MB)
  - WAL checkpointeado (451MB → 0)
  - DB compactada de 1.7GB a 760MB
- **Espacio libre:** 407MB (98% usado)
- **⚠️ Pendiente:** Considerar limpiar más espacio o ampliar partición

## Métricas finales

| Métrica | Antes | Después |
|---------|-------|---------|
| Skills totales | 210 | 219 |
| ChromaDB indexados | ? | 219 |
| Repos procesados | 234 | 238 |
| Skills generados | 44 | 47 |
| DB state.db | 1.7GB corrupta | 760MB limpia |
| session_search | Error | Funcional |
| Cron deep-learning | Eliminado | Recreado (03:30 UTC) |
| Disco /persist | 100% | 98% (407MB free) |

## Cron jobs activos (10)

| Job | Schedule | Estado |
|-----|----------|--------|
| esios-daily-telegram | 09:00 UTC | ✅ |
| BiciMad Tetuán | L-Mi 06:30, 13:00 | ✅ |
| inventario-apis-procesar | cada 30m | ✅ |
| inventario-apis-resumen-diario | 22:00 UTC | ✅ |
| skill-maintenance | día 1 cada mes | ✅ |
| chromadb-reindex-semanal | domingo 04:00 UTC | ✅ |
| skills-sync-to-github | 05:00 UTC | ✅ |
| stars-explorer-nocturno | 03:00 UTC | ✅ |
| eravisor-descarga-paises | cada 20m | ✅ |
| deep-learning-diario | 03:30 UTC | ✅ NUEVO |

---
*Hecho con ❤️ por David Antizar*
