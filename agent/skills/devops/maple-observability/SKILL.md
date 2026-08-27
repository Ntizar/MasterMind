---
name: maple-observability
version: "1.0.0"
description: "Maple — plataforma de observabilidad open-source con OpenTelemetry + ClickHouse, monorepo Effect + TanStack Router"
---

# Maple — Open-Source Observability Platform

## Descripción

Plataforma de observabilidad open-source para traces, logs y métricas, construida sobre OpenTelemetry y ClickHouse. Monorepo con frontend SPA (TanStack Router + Vite), backend Effect, OTLP ingest gateway, y múltiples apps.

## Por qué importa para David

- **ClickHouse + OTel**: Patrón de almacenamiento de series temporales de alta performance
- **Effect framework**: Patrón functional para backend robusto con manejo de errores
- **Monorepo pattern**: Estructura de workspace con Bun para proyectos grandes
- **Real-time dashboard**: Pattern de dashboard observable en tiempo real

## Arquitectura

```
apps/web       → TanStack Router SPA (Vite)
apps/api       → Effect HTTP API + MCP server
apps/ingest    → OTLP ingest gateway + collector forwarding
apps/alerting  → Alert evaluation worker
apps/cli       → CLI utilities
apps/mobile    → Expo mobile app
packages/domain → Shared Effect contracts
packages/query-engine → Query & observability logic
packages/ui     → Shared UI primitives
```

## Instalación local

```bash
# Homebrew (recomendado)
brew install Makisuo/tap/maple
maple start

# Manual con Bun
bun install
bun run dev

# Docker
docker compose up
```

## Integración con proyectos de David

- **Control Center**: Usar ClickHouse como backend de métricas
- **Dashboards**: Pattern de real-time observability reusable
- **Alerting**: Worker pattern para evaluaciones de alertas

## Pitfalls

- Requiere Bun runtime (no Node)
- ClickHouse embedded consume RAM (mínimo 2-4GB)
- Effect framework tiene curva de aprendizaje
- No es trivial migrar de otro stack a Effect

## Referencias

- GitHub: https://github.com/MapleTechLabs/maple
- Docs: Monorepo README con instrucciones detalladas
