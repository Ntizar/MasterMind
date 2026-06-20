# Checklist de Auditoría de Seguridad y Compliance

Generado iterativamente en sesiones de auditoría TerrAn (iteraciones 80-92).
Cubre los 23 issues encontrados en la fase 06 de seguridad y compliance.

## Alta Severidad (15 issues)

| ID | Problema | Documento |
|---|---|---|
| SEC-001 | `password_hash = 'SYSTEM_HASH'` literal (no bcrypt) | ARQUITECTURA.md:418 |
| SEC-002 | Sin RLS en PostgreSQL | No mencionado |
| SEC-003 | audit_log sin org_id | ARQUITECTURA.md:205-227 |
| SEC-004 | Snapshots JSONB completos en audit | ARQUITECTURA.md:215-216 |
| SEC-005 | Sin export de datos (RGPD Art. 20) | No mencionado |
| SEC-006 | Sin interfaz de recuperación soft delete | No mencionado |
| SEC-007 | DEFAULT_POLICIES solo en JS, no implementado | RENDIMIENTO-Y-NEGOCIO.md:538-556 |
| SEC-008 | DNI/exámenes médicos en JSONB sin encriptar | RENDIMIENTO-Y-NEGOCIO.md:182-219 |
| SEC-009 | JWT sin revocación/blacklist | No mencionado |
| SEC-011 | WebSocket sin autenticación | No mencionado |
| SEC-016 | Sin backup strategy | No mencionado |
| SEC-017 | Sin rate limiting | No mencionado |
| SEC-022 | config JSONB sin encriptación (credenciales) | ARQUITECTURA.md:128 |
| SEC-023 | Sin derecho al olvido (RGPD Art. 17) | No mencionado |

## Media Severidad (8 issues)

| ID | Problema | Documento |
|---|---|---|
| SEC-010 | `publica BOOLEAN DEFAULT true` en cámaras | RENDIMIENTO-Y-NEGOCIO.md:480 |
| SEC-012 | Sin CSRF | No mencionado |
| SEC-013 | Sin security_log | No mencionado |
| SEC-014 | `firma数字化` (chino) sin eIDAS | DOCUMENTOS-Y-IA.md:130 |
| SEC-015 | Sin TLS/SSL | No mencionado |
| SEC-018 | Datos sensibles en metadata sin control | RENDIMIENTO-Y-NEGOCIO.md:182-219 |
| SEC-019 | UNIQUE WHERE deleted_at IS NULL riesgo duplicados | ARQUITECTURA.md:191 |
| SEC-020 | Sin política de contraseñas | No mencionado |
| SEC-021 | updated_at sin trigger (manipulable) | ARQUITECTURA.md:185 |

## Reglas de verificación

1. Leer los 3 documentos completos antes de auditar
2. Verificar cada issue contra línea exacta del documento
3. No asumir que algo "seguro está bien" — comprobar literalmente
4. Issues nuevos deben tener: id único, solución concreta, severidad
5. Usar `execute_code` + `json.dumps()` para generar JSON seguro de `log-issue`
6. La fase activa en audit-state.json es la que tiene `clear: false`
