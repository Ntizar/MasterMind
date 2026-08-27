# Auditoría TerrAn — Iteración 181 (2026-06-24)

## Resumen

Iteración que auditó 3 fases (06, 07, 08). Encontró 12 nuevos issues:
- 6 en security-compliance (SEC-096 a SEC-101)
- 6 en business-logic (BL-015 a BL-020)
- 0 en ux-workflow (realmente limpia)

## Issues críticos descubiertos

### SEC-096: BIGSERIAL PRIMARY KEY,, (doble coma)
**Líneas 3050 y 3305 de ARQUITECTURA.md.** Doble coma en sintaxis SQL que impide crear security_log y login_attempts. Error de copy-paste.
- **Impacto:** Tablas de seguridad no se pueden crear → sin logging de intentos de login, sin rate limiting, sin detección de fuerza bruta.
- **Solución:** Eliminar doble coma → `BIGSERIAL PRIMARY KEY`.

### SEC-097: security_log y login_attempts sin org_id
Las tablas no tienen `org_id` pero sus RLS policies refieren `app_current_org_id()`. Las policies no funcionan.
- **Impacto:** Fuga de logs de seguridad entre organizaciones.
- **Solución:** Añadir `org_id UUID NOT NULL` a ambas tablas.

### SEC-098: password_history sin encriptar
Almacena `password_hash TEXT NOT NULL` en texto plano. Si se filtra, se pierden TODAS las contraseñas pasadas.
- **Impacto:** Violación de defense in depth. Hashes antiguos podrían tener bcrypt con coste bajo.
- **Solución:** Encriptar con pgcrypto o tabla separada con acceso restringido.

### SEC-100: DEFAULT_POLICIES en JS sin tabla retention_policies en BD
Las políticas de retención están hardcodeadas en JavaScript (RENDIMIENTO-Y-NEGOCIO.md líneas 565-582).
- **Impacto:** No configurables por cliente, requieren redeploy para cambios.
- **Solución:** Crear tabla `retention_policies (org_id, tabla, dias_retencion, accion, activo)`.

### SEC-101: getTier() hardcodeado en JS
La función `getTier(orgId)` referencia `tier.price`, `tier.maxActivos` pero no hay tabla tiers.
- **Impacto:** Modelo de negocio es solo texto, no funcional.
- **Solución:** Crear tabla `tiers` + `suscripciones` + `getTier()` query real a BD.

## Business-Logic issues

### BL-015: Sin tabla modulos_disponibles
Módulos cargados de JSONB sin validación de existencia, versión o compatibilidad.

### BL-016: Add-ons sin tabla de configuración
9 add-ons con precios hardcodeados en el documento. Sin tabla `add_ons` ni `org_add_ons`.

### BL-017: Sin tabla trials
Sin mecanismo de prueba de 30 días para ayuntamientos B2G.

### BL-018: Solo export RGPD
No hay export funcional: inventario Excel, reportes PDF, auditoría CSV.

### BL-019: POST /api/activos sin verificación de límite de tier
Cliente Starter puede crear 10.000 activos sin pagar más. Crítico.

### BL-020: Turnos/asignaciones sin endpoints
Tablas existen pero sin CRUD. Inútiles sin endpoints de gestión.

## Lecciones aprendidas

1. **Los issues de "doble coma" son reales y recurrentes.** Cada iteración hay que greppear `,,` en ARQUITECTURA.md.
2. **El modelo de negocio (tiers, add-ons, trials) NO está en BD.** Solo existe en texto plano. Es un problema sistémico que afecta a SEC-101 y BL-015/BL-016/BL-017/BL-019.
3. **Phase 08 (UX) está limpia** porque no hay documentación de frontend. Las carencias de UX están ya capturadas en business-logic (BL-003 onboarding, BL-007 demo data).
4. **La auditoría de seguridad ya tiene 101 issues.** La fase 06 es la más densa. Priorizar fixes críticos (SEC-096 bloquea todo, SEC-097 fuga de datos, SEC-101 modelo de negocio roto).