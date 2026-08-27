# Casos Reales de Auditoría

## Caso 1: Mastermind v3.1 → v4.0

**Fecha:** 2026-06-04  
**Repo:** Ntizar/NtizarBrainMasterMind  
**Antes:** 5.6/10 | **Después:** 8.1/10  
**Delta:** +2.5 puntos (2 sesiones)

### Hallazgos detectados

| # | Hallazgo | Severidad | Estado |
|---|----------|-----------|--------|
| 1 | Directorios fantasma (skills/, projects/, notes/) referenciados pero inexistentes | 🔴 Crítico | ✅ Resuelto |
| 2 | pages.yml excluía verify-system.bat (eliminado) | 🔴 Crítico | ✅ Resuelto |
| 3 | Roadmap con items ya completados | 🔴 Crítico | ✅ Resuelto |
| 4 | Sin tracking de tokens | 🟡 Importante | ✅ Resuelto |
| 5 | Memoria/aprendizaje no implementados | 🟡 Importante | ✅ Resuelto |
| 6 | Landing page incompleta (HERO, features vacíos) | 🟡 Importante | ✅ Resuelto |
| 7 | innerHTML en dashboard (XSS) | 🟡 Importante | ✅ Resuelto |
| 8 | Branch master activo | 🟡 Importante | ✅ Resuelto |
| 9 | learning-platform/ en raíz | 🟡 Importante | ✅ Resuelto |
| 10 | CDN @master inestable | 🟡 Importante | ✅ Resuelto |

### Cambios ejecutados

| # | Cambio | Técnica |
|---|--------|---------|
| 1 | `(L)` → `❤️` en 6 archivos | `execute_code` con bucle Python |
| 2 | `learning-platform/` → `legacy/learning-platform/` | `terminal` mv |
| 3 | Dashboard tokens: hardcoded → `fetch()` + fallback | `patch` quirúrgico |
| 4 | `innerHTML` → `document.createElement` + `textContent` | `patch` (seguridad) |
| 5 | 12 Rules: v3.1 → v4.0 | `patch` |
| 6 | SOUL.md: eliminada referencia a `docs/` | `patch` |
| 7 | verify-system.sh: 11/11 checks | `patch` |
| 8 | pages.yml: excludes limpiados | `patch` |
| 9 | CHANGELOG.md: entrada v4.0.1 | `patch` |
| 10 | README.md: roadmap, rules, tree | `patch` |

---

## Caso 2: Mastermind + Mastermind v3 — Auditoría Crítica + Pipeline de Crons

**Fecha:** 2026-06-10  
**Repo:** Ntizar/Mastermind  
**Antes:** 4.5/10 | **Después:** ~7/10 (Fase 1 completa, Fase 2 pendiente)  
**Delta:** +2.5 puntos (pipeline secuencial de 14 crons)

### Contexto

David pidió una "auditoría crítica de los proyectos con lo que hace realmente, no solo lo que dice el readme". El sistema tenía una brecha significativa entre documentación aspiracional y estado real. Además, pidió "máxima ambición" pero "cuidado con la sobreingeniería".

### Hallazgos principales

| # | Hallazgo | Severidad | Evidence |
|---|----------|-----------|----------|
| 1 | ChromaDB online con 190+ skills indexados pero Mastermind NUNCA lo consultaba | 🔴 Crítico | `consultar-skills.py` nunca invocado en sesiones reales |
| 2 | README con métricas infladas (decía 190+ skills, 12 crons cuando era 192/13) | 🟡 Importante | Verificación manual contra estado real |
| 3 | Mastermind v3 marcado como "operativo" pero era diseño conceptual | 🟡 Importante | Sin scripts de memory decay, knowledge graph, etc. |
| 4 | 143 skills duplicadas en repo (267 en repo vs 124 únicas) | 🟡 Importante | Comparación repo vs agent/ |
| 5 | skill-priority.json listaba 123/192 skills reales | 🟡 Importante | Análisis de cobertura |
| 6 | ChromaDB no persistía tras reinicio (sin auto-start) | 🟡 Importante | Sin systemd unit ni script de arranque |
| 7 | Crons pausados acumulándose (GitHub Stars, skill-learning) | 🟢 Menor | `cronjob action=list` |

### Pipeline de implementación: 14 Crons Secuenciales

**Patrón:** Cada cron es autocontenido (lee → ejecuta → verifica → commit → resumen) e idempotente.

#### Fase 1: Infraestructura y Limpieza (8 crons)

| Cron | Tarea | Resultado |
|------|-------|-----------|
| 01 | Actualizar README con métricas reales | ✅ 192 skills, 13 crons, 70 notas |
| 02 | Marcar Mastermind v3 como "diseño conceptual" | ✅ Disclaimer añadido |
| 03 | Crear script auto-start ChromaDB | ✅ `start-chromadb.sh` con health check |
| 04 | Re-indexar ChromaDB desde cero | ✅ 192 skills, collection online |
| 05 | Integrar ChromaDB en SOUL.md como flujo obligatorio | ✅ Flujo vector search documentado |
| 06 | Eliminar skills duplicadas del repo | ✅ 267→124 (143 eliminadas) |
| 07 | Consolidar skill-priority.json | ✅ 123→192 skills |
| 08 | Eliminar crons pausados | ✅ GitHub Stars + skill-learning eliminados |

#### Fase 2: Inteligencia (6 crons — pendientes)

| Cron | Tarea | Componente |
|------|-------|------------|
| 09 | Memoria decay Ebbinghaus | `memory-decay.py` |
| 10 | Knowledge graph | `knowledge-graph.py` |
| 11 | Skill lifecycle auto-prioritización | `skill-lifecycle.py` |
| 12 | Flujos de delegación por complejidad | `delegation-flows.py` |
| 13 | Dashboard interactivo HTML | `mastermind-status.html` |
| 14 | Revisión final + loop semanal | Verificación + crons reparación |

### Lecciones clave

1. **Deployment ≠ Integración** — El hallazgo más importante: ChromaDB estaba técnicamente operativo pero nunca se invocaba. Tener infraestructura no significa que esté integrada. Siempre verificar: "¿hay un trigger real que llame a esto?"

2. **Documentación aspiracional es deuda técnica** — Si un componente está descrito como "operativo" en docs pero no tiene código que lo ejecute, marcarlo explícitamente como "diseño conceptual". No confundir al futuro yo.

3. **Pipeline de crons para implementación escalonada** — Cuando el usuario no puede supervisar en vivo, crear crons `once` escalonados (15-20 min separación). Ventajas: parcial failure no bloquea todo, cada cron es idempotente, el usuario ve progreso en tiempo real via `deliver: origin`.

4. **Fase 1/Fase 2 split** — Separar infraestructura (crea paths/scripts que otros usan) de inteligencia (usa esos paths/scripts). Si un cron de Fase 2 falla porque depende de un path de Fase 1, el error es claro y localizable.

5. **Cron de revisión final crea loop semanal** — El último cron verifica todo y crea un cron recurrente (domingos 05:00 UTC) que re-ejecuta mantenimiento. Auto-sostenible.

6. **Sobreingeniería: detectar y cortar** — David corrigió explícitamente: "con cuidado con la sobreingeniería que te gusta mucho". Señales: arquitectura documentada que no se implementa, N agentes cuando M bastan, fórmulas complejas sin código. En cada auditoría, preguntar "¿esto es funcional o es documentación aspiracional?"

7. **Métricas reales > métricas infladas** — README con métricas incorrectas destruye la credibilidad del sistema. Verificar contra estado real antes de publicar.

### Stack real del sistema

| Componente | Estado | Detalle |
|---|---|---|
| Modelo | qwen3.6 vía NaN | `api.nan.builders/v1`, sin multi-model routing |
| Infra | MicroVM 1vCPU/2GB/20GB | NaN.builders |
| ChromaDB | ONLINE, 192 skills | localhost:8000, qwen3-embedding 4096-dim |
| Skills en repo | 124 (deduplicated) | agent/ es fuente de verdad |
| Skills en priority.json | 192 | Cobertura completa |
| Cron jobs | 19 activos | 6 permanentes + pipeline + otros |
| GitHub auth | Token HTTPS | `GITHUB_TOKEN` en `.env`, gh CLI no instalado |
