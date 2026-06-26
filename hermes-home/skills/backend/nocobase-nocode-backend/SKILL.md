---
name: nocobase-nocode-backend
version: "1.0.0"
description: "NocoBase — plataforma open-source AI + no-code para construir backends, APIs y workflows visualmente. 22K⭐. Sistema de plugins extensible."
tags: [nocode, backend, api, database, workflow, plugins, typescript]
---

# NocoBase — No-Code Backend Platform

## Resumen

NocoBase es una plataforma **no-code + AI** para construir backends completos sin escribir código. Genera APIs REST/GraphQL, bases de datos, workflows y dashboards desde una interfaz visual.

## Capacidades

- **Database Manager:** Tablas, relaciones, campos (SQLite/PostgreSQL)
- **API Generator:** REST + GraphQL automáticos
- **Workflow Builder:** Automatización drag-and-drop
- **Plugin System:** 80+ plugins oficiales + custom
- **Auth:** JWT, OAuth, roles y permisos
- **AI Assistant:** Generación de colecciones con IA

## Instalación

```bash
# Docker (5 min)
git clone https://github.com/nocobase/nocobase
cd nocobase && docker-compose up -d
# http://localhost:13000
```

## Plugin System

```bash
# Instalar plugins
npm run nocobase pm install @nocobase/plugin-users
npm run nocobase pm install @nocobase/plugin-workflow
npm run nocobase pm install @nocobase/plugin-charts

# Crear plugin custom
npm run nocobase pm create my-plugin
```

## Comparativa

| Feature | NocoBase | NocoDB | Supabase |
|---------|----------|--------|----------|
| No-Code | ✅ | ✅ | ❌ |
| Plugins | ✅ (sistema extensible) | ❌ | ❌ |
| Workflows | ✅ | ❌ | ✅ (Edge) |
| AI | ✅ Asistente | ❌ | ❌ |
| Multi-tenant | ✅ | ❌ | ❌ |

## Integración con Mastermind

- Prototipado rápido de backends para dashboards
- API Gateway para proyectos multi-fuente
- Gestión de datos sin tocar SQL

## Referencia

- Repo: `nocobase/nocobase`
- Docs: https://docs.nocobase.com