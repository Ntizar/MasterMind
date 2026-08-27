# Caso TerrAn — Auditoría de Arquitectura con "Fixed" No Aplicado

## Contexto

**Fecha:** 2026-06-16  
**Proyecto:** TerrAn (ERP municipal 3D — Node.js + PostgreSQL + PostGIS + Three.js + ChromaDB)  
**Iteración:** 116 de auditoría cíclica  
**Fase auditada:** 06 — Seguridad y Compliance  

## Problema detectado

La auditoría encontró **9 issues activos** en una fase donde 36 de 45 issues estaban marcados como "fixed". El patrón revelado:

> **Los fixes estaban documentados en comentarios/secciones al final del documento, pero el schema base (CREATE TABLEs principales) NO fue modificado.**

Esto significa que la seguridad multi-tenant (RLS) estaba documentada como "activa" pero era completamente inoperativa porque:
1. Las RLS policies referencian `current_user_id()` que nunca está definida → error de runtime
2. La tabla `usuarios` no tiene `org_id` → la RLS policy `tenant_isolation_all` es inválida
3. El CHECK constraint de `usuarios.rol` sigue presente → bloquea roles personalizados
4. `audit_log` en RENDIMIENTO-Y-NEGOCIO.md no tiene `org_id` (ARQUITECTURA.md sí) → inconsistencia

## Hallazgos clave

| # | Issue | Severidad | Root Cause |
|---|-------|-----------|------------|
| SEC-037 | `current_user_id()` nunca definida | 🔴 Alta | RLS policies referencian función inexistente → RLS completamente roto |
| SEC-038 | `usuarios` sin `org_id` | 🔴 Alta | Schema base no actualizado tras fix de SEC-024 |
| SEC-039 | CHECK constraint en `usuarios.rol` no eliminado | 🔴 Alta | Fix documentado en comentarios, schema base intacto |
| SEC-040 | `audit_log` sin `org_id` en RENDIMIENTO-Y-NEGOCIO.md | 🔴 Alta | Dos documentos inconsistentes |
| SEC-041 | `audit_log` usa BIGSERIAL + PARTITION (incompatible) | 🔴 Alta | ARQUITECTURA.md tiene fix, RENDIMIENTO-Y-NEGOCIO.md no |
| SEC-042 | `fuentes_video` con `publica BOOLEAN` | 🟡 Media | SEC-010 "fixed" pero schema no actualizado |
| SEC-043 | Datos sensibles en texto plano sin pgcrypto | 🔴 Alta | Tabla `activos_humanos` existe pero sin encriptación |
| SEC-044 | `security_log` y `login_attempts` sin `org_id` | 🟡 Media | Fuga multi-tenant en logs |
| SEC-045 | `organizaciones` sin RLS policy para superadmin | 🟡 Media | Admin no puede ver su propia org |

## Lecciones

### 1. "Fixed" ≠ "Applied"
Marcar un issue como "fixed" cuando la solución está documentada en un comentario pero el schema base no cambió es un **falso positivo**. En auditorías de arquitectura:
- **Fixed real** = El schema base fue modificado para reflejar la solución
- **Fixed falso** = La solución está documentada pero el código/schema sigue igual

### 2. Verificar consistencia entre documentos
TerrAn tiene 3 documentos de arquitectura. Si una tabla aparece en 2+ documentos con definiciones diferentes, hay un riesgo de implementación. Siempre verificar que:
- Todas las definiciones de la misma tabla son idénticas
- No hay `CREATE TABLE` duplicados con esquemas diferentes
- Los fixes aplicados en un documento se replican en todos

### 3. Funciones referenciadas deben existir
Si una RLS policy, trigger o función referencian `current_user_id()`, `current_user_email()`, o cualquier función definida por el usuario, verificar que el `CREATE OR REPLACE FUNCTION` existe en el mismo documento. Si no existe, la RLS es inoperativa.

### 4. BIGSERIAL + PARTITION BY RANGE es incompatible
PostgreSQL no permite `BIGSERIAL` en tablas particionadas por rango. Siempre usar `BIGINT DEFAULT nextval('seq')` en tablas particionadas.

## Métricas de la fase

- **Total issues:** 45
- **Fixed (aplicados):** 36
- **Activos:** 9
- **Fixed falsos (documentados pero no aplicados):** ~20 (estimado)
