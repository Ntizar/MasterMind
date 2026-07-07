---
name: architecture-patterns
description: "Patrones de diseño para sistemas de software — arquitectura de componentes modulares, sistemas de permisos multi-tenant, y patrones de diseño de arquitecturas completas. Incluye TerrAn (ERP municipal), FreeHands (control de versiones), y patrones de arquitectura modular reutilizable."
version: "1.0.0"
tags: [architecture, design-patterns, modularity, rbac, multi-tenant, erp, version-control]
---

# Architecture Patterns — Patrones de Arquitectura de Software

## Resumen

Patrones de diseño para construir sistemas de software robustos, modulares y escalables. Cubre desde componentes reutilizables hasta arquitecturas completas (ERP, sistemas de control de versiones, RBAC multi-tenant).

## Sub-skill: Modular Component Ecosystem (absorbido de `modular-component-ecosystem`)

Diseño de módulos base reutilizables con patrón `@namespace/component` para compartir entre proyectos. Incluye: estructura de módulos, sistema de versionado, documentación de APIs internas, y patrones de composición.

**Ver referencia:** `references/modular-patterns.md` en el skill absorbido.

## Sub-skill: Multi-Tenant RBAC (absorbido de `multi-tenant-rbac`)

Patrones de diseño para sistemas de permisos multi-tenant. Incluye: modelo de roles jerárquicos, herencia de permisos entre tenants, auditoría de accesos, y patrones de aislamiento de datos.

**Ver referencia:** `references/multi-tenant-rbac-patterns.md` en el skill absorbido.

## Sub-skill: TerrAn Architecture (absorbido de `terran-architecture`)

Arquitectura completa de TerrAn — ERP municipal con vista cartográfica. Incluye: modelo de datos municipal, integración GIS, módulos de gestión (urbanismo, tributación, servicios), y patrones de despliegue.

**Ver referencia:** `references/terran-architecture.md` en el skill absorbido.

## Sub-skill: FreeHands Architecture (absorbido de `freehands-architecture`)

Arquitectura completa del proyecto FreeHands — control de versiones distribuido. Incluye: modelo de grafos de commits, resolución de conflictos, sistema de branches, y patrones de sincronización.

**Ver referencia:** `references/freehands-architecture.md` en el skill absorbido.