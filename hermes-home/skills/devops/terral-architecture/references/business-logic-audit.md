# TerrAn — Auditoría de Lógica de Negocio (Iter 107, 2026-06-15)

## Contexto

Fase 07 del auditor cíclico: **Importación masiva, export, pricing, onboarding, migración desde Excel**.

Los 3 documentos de arquitectura (ARQUITECTURA.md, RENDIMIENTO-Y-NEGOCIO.md, DOCUMENTOS-Y-IA.md) cubren bien el schema técnico y la seguridad, pero **no mencionan absolutamente nada** sobre cómo un ayuntamiento real introduce datos en el sistema, cómo se gestiona el onboarding, o cómo se convierte un trial en cliente pagador.

## 10 Issues Encontrados

### 🔴 ALTA (4 issues — bloqueantes)

#### BL-001: Sin mecanismo de importación masiva de activos
- **Problema:** No hay endpoint CSV/Excel, no hay mapeo de columnas, no hay validación.
- **Impacto:** Bloqueo total del onboarding. 500+ activos no se pueden crear uno a uno.
- **Solución:** `POST /api/import/activos` con CSV, `GET /api/import/templates/{tipo}`, `POST /api/import/preview`, mapeo automático, reporte de errores fila por fila, rollback si errores > 5%.

#### BL-002: Sin tabla de tiers/suscripciones en el schema
- **Problema:** RENDIMIENTO-Y-NEGOCIO.md define 6 tiers pero NO hay tabla tiers, suscripciones ni facturacion en el schema. `getTier(orgId)` no tiene de qué leer.
- **Impacto:** Modelo de negocio es solo texto, no funcional. No se puede facturar ni limitar tenant por tier.
- **Solución:** Tablas `tiers`, `suscripciones`, `add_on_suscripcion`, `add_ons`. Middleware que verifique límites.

#### BL-003: Sin flujo de onboarding
- **Problema:** Primer usuario entra a dashboard vacío. No hay wizard, empty states, tutorial ni datos demo.
- **Impacto:** Abandono masivo en el primer minuto. Tasa de conversión registro→uso activo ≈ 0%.
- **Solución:** Wizard 4 pasos (elegir municipio → elegir módulos → subir datos → invitar equipo). Empty states descriptivos. Datos demo precargados.

#### BL-004: Sin migración desde Excel
- **Problema:** Los ayuntamientos viven en hojas de cálculo. No hay mecanismo para migrar datos existentes. Competidores cobran 50K€ por esto.
- **Impacto:** Barrera de entrada insalvable. 10.000 registros manuales no son viables.
- **Solución:** `POST /api/import/excel` con detección automática de formato, mapeo + UI confirmación, validación coordenadas/tipos/duplicados, reporte de errores, opción "importar como borradores".

### 🟡 MEDIA (4 issues)

#### BL-005: Pricing con incentivo perverso
- **Problema:** Facturar por activos = cliente oculta activos para pagar menos. El propio documento reconoce el problema sin mitigación.
- **Impacto:** Ayuntamientos con 1000 activos pagarán 199€ (declarando 500) en lugar de 799€. Modelo se autodestruye.
- **Solución:** Facturar por usuarios/módulos, no por activos. O límite generoso (10.000 activos gratis). O auditar geo-mapeo vs activos declarados.

#### BL-006: Add-ons sin tabla de configuración
- **Problema:** Add-ons (Cámaras +99€, Renfe +199€) son texto plano, no funcional. No hay tabla add_ons ni mecanismo de activación.
- **Impacto:** No se pueden vender add-ons. Cualquier cambio de precio requiere redeploy.
- **Solución:** Tablas `add_ons` + `org_add_ons` + feature flags en middleware.

#### BL-008: Sin export funcional para clientes
- **Problema:** El export existe solo para RGPD, no para uso operativo. Cliente no puede sacar inventarios en Excel ni reportes en PDF.
- **Impacto:** Cliente depende de la plataforma para todo. No puede cumplir con administración externa.
- **Solución:** Endpoints `export/inventario`, `export/reportes/{tipo}`, `export/auditoria`. Filtros + notificación cuando están listos.

#### BL-009: Métricas de facturación sin verificación real
- **Problema:** Billing depende de métricas auto-reportadas que el tenant podría manipular. No hay sistema de billing independiente.
- **Impacto:** En B2G, facturación injusta es especialmente delicada.
- **Solución:** Billing independiente + límites hard en backend (rechazar 403 si superan tier).

### 🟢 BAJA (2 issues)

#### BL-007: Sin política de datos demo
- **Problema:** Sin datos demo, primer usuario ve sistema vacío.
- **Solución:** `POST /api/demo/cargar` con 50 activos, `POST /api/demo/limpiar`, flag `is_demo`.

#### BL-010: Sin gestión de trial/período de prueba
- **Problema:** Sin trial, ayuntamiento no puede probar antes de pagar. En B2G las decisiones son lentas.
- **Solución:** Tabla `trials`, auto-creación 30 días, modo lectura al expirar, notificación 7 días antes.

## Estado tras iter 107

- **Total issues activos en proyecto:** 10 (todos en fase 07)
- **Total issues fijados hasta ahora:** 105
- **Fases completadas:** 5/8 (01-05 ✅)
- **Fase actual:** 07-business-logic ⚠️ 10 issues activos
- **Fase pendiente:** 08-ux-workflow (sin auditar)
