# TerrAn — Auto-Auditoría Iteración 106

## Fase: Seguridad y Compliance (06-security-compliance)

**Resultado:** ⚠️ 36 issues activos, 0 fijados
**Progreso:** 5/8 fases completadas (06 no completada)

## Resumen

Auditoría exhaustiva de los 3 documentos de arquitectura (ARQUITECTURA.md, RENDIMIENTO-Y-NEGOCIO.md, DOCUMENTOS-Y-IA.md) contra checklist de seguridad y compliance. Se encontraron **13 issues nuevos** que se suman a los 23 previos.

### Issues nuevos (SEC-024 a SEC-036)

| ID | Severidad | Título |
|---|---|---|
| SEC-024 | 🔴 Alta | Roles hardcodeados en CHECK — no escalan a multi-tenant |
| SEC-025 | 🔴 Alta | Tabla permisos sin org_id — permisos globales entre organizaciones |
| SEC-026 | 🔴 Alta | Desactivar usuario no invalida sesiones activas |
| SEC-027 | 🟡 Media | Sin algoritmo de hash de contraseñas especificado |
| SEC-028 | 🟡 Media | Sin tabla de permisos temporarios |
| SEC-029 | 🔴 Alta | ChromaDB sin aislamiento multi-tenant |
| SEC-030 | 🟡 Media | URLs de streams de cámaras expuestas en la API |
| SEC-031 | 🟡 Media | Sin sistema de migraciones con rollback |
| SEC-032 | 🟡 Media | Regex de validación de alcance insuficiente |
| SEC-033 | 🟢 Baja | Enumeración de emails vía feedback diferenciado |
| SEC-034 | 🔴 Alta | Sin lockout tras intentos fallidos de login |
| SEC-035 | 🟡 Media | Upload de documentos sin validación MIME |
| SEC-036 | 🟡 Media | Sin política CORS documentada |

### Distribución por severidad

- 🔴 **Alta:** 12 nuevos (SEC-024, 025, 026, 029, 034) + 13 previos = **25 alta**
- 🟡 **Media:** 10 nuevos (SEC-027, 028, 030, 031, 032, 035, 036) + 9 previos = **19 media**
- 🟢 **Baja:** 1 nuevo (SEC-033) + 0 previos = **1 baja**
- **Total: 45 issues**

### Categorías principales

1. **Multi-tenant isolation (4 issues):** RLS no implementado, permisos sin org_id, ChromaDB sin aislamiento, audit_log sin org_id
2. **Authentication/Authorization (6 issues):** JWT sin revocación, sin lockout, activo=false no invalida sesiones, roles hardcodeados, permisos sin org_id, sin permisos temporarios
3. **Data protection (5 issues):** JSONB sin encriptar, snapshots completos en audit, config JSONB sin encriptar, sin exportación, sin derecho al olvido
4. **Infrastructure security (5 issues):** Sin TLS, sin CORS, sin backup, sin rate limiting, sin CSRF
5. **Compliance (4 issues):** Ley 39/2015, RGPD Art. 17/20, sin política de retención, firma electrónica

## Próximos pasos

La fase 06 NO se avanza hasta que los issues de severidad ALTA se resuelvan. En la próxima iteración se auditarán las propuestas de solución para cada issue de alta severidad.
