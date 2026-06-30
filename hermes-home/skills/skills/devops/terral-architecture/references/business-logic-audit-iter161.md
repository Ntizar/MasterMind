# Business Logic Audit — Iteración 161 (2026-06-21)

## Contexto

Fase 07 (Lógica de Negocio) de la auditoría cíclica de TerrAn.
14 issues activos: 10 previos (BL-001 a BL-010) + 4 nuevos (BL-011 a BL-014).

## Issues previos (sin fijar)

| ID | Título | Severidad |
|---|---|---|
| BL-001 | Sin importación masiva de activos | Alta |
| BL-002 | Sin tabla de tiers/suscripciones | Alta |
| BL-003 | Sin flujo de onboarding | Alta |
| BL-004 | Sin migración desde Excel | Alta |
| BL-005 | Pricing por activos = incentivo perverso | Media |
| BL-006 | Add-ons sin tabla de configuración | Media |
| BL-007 | Sin datos demo | Baja |
| BL-008 | Export funcional inexistente | Media |
| BL-009 | Métricas de facturación sin verificación | Media |
| BL-010 | Sin gestión de trial | Baja |

## Issues nuevos (iter 161)

### BL-011: loadModules sin error handling
- **Ubicación:** ARQUITECTURA.md línea 720-736
- **Problema:** `require()` sin try/catch. Un módulo roto tira TODO el servidor.
- **Impacto:** Inestabilidad total. Cualquier cambio en un módulo puede caer la plataforma.
- **Solución:** Envolver cada require en try/catch, verificar mod.routesHandler/mod.hooks, health check por módulo.

### BL-012: Módulos habilitados en JSONB sin esquema
- **Ubicación:** ARQUITECTURA.md línea 721 (`orgConfig.modules`)
- **Problema:** Sin tabla modulos_disponibles ni org_modulos. JSONB sin validación.
- **Impacto:** No se puede facturar módulos, no hay control de versiones, typos causan fallos silenciosos.
- **Solución:** Tablas modulos_disponibles + org_modulos. Validar nombre antes de cargar.

### BL-013: eventBus sin manejo de errores
- **Ubicación:** ARQUITECTURA.md líneas 730-731 (`eventBus.on(event, handler)`)
- **Problema:** Si un handler de hook falla, evento se pierde. Estado inconsistente.
- **Impacto:** Datos en BD correctos pero lógica de negocio rota. Sin logging.
- **Solución:** try/catch por handler, dead letter queue, métricas de hooks.

### BL-014: Sin validación de límites de tier
- **Ubicación:** RENDIMIENTO-Y-NEGOCIO.md línea 635 (`getTier(orgId)`)
- **Problema:** No hay middleware que verifique max_activos/max_usuarios antes de crear.
- **Impacto:** Cliente Starter puede crear 10.000 activos sin pagar. Modelo de facturación autodestructivo.
- **Solución:** Tabla tiers + middleware de verificación + 403 con mensaje claro.

## Estado de verificación

Todos los 14 issues verificados contra ARQUITECTURA.md, RENDIMIENTO-Y-NEGOCIO.md y DOCUMENTOS-Y-IA.md.
Ninguno tiene solución implementada en los documentos.
