---
name: huly-crm-erp-platform
version: "1.0.0"
description: "Huly — plataforma open-source todo-en-uno de gestión empresarial (CRM+ERP). Alternativa a Linear, Notion, Jira. 26K⭐. Proyectos, ventas, HR, contabilidad."
tags: [crm, erp, project-management, business, huly, typescript, platform]
---

# Huly — All-in-One CRM/ERP Platform

## Resumen

Huly es una plataforma **open-source todo-en-uno** de gestión empresarial del equipo `hcengineering/platform`. Sustituye a Linear (tickets), Notion (docs), Jira (proyectos) y Salesforce (CRM).

## Módulos

- **Project Management:** Tickets, sprints, kanban, timeline
- **CRM:** Contactos, deals, pipeline de ventas
- **HR:** Empleados, ausencias, perfiles
- **Accounting:** Facturación, gastos, presupuestos
- **Inventory:** Gestión de stock y activos
- **Documents:** Wiki, documentación interna

## Instalación

```bash
git clone https://github.com/hcengineering/platform
cd platform && docker-compose up -d
# Acceder en http://localhost:8080
```

## CRM + ERP combinado

| Feature | Huly | Alternativas |
|---------|------|-------------|
| Pipelines de venta | ✅ Kanban CRM | Salesforce, HubSpot |
| Proyectos | ✅ Timeline + Sprints | Jira, Linear |
| Documentos | ✅ Wiki | Notion, Confluence |
| RRHH | ✅ Perfiles + Ausencias | BambooHR |
| Facturación | ✅ Básico | QuickBooks |
| Open-source | ✅ Apache 2.0 | — |

## Comparativa de alternativas (si montas un CRM)

Para elegir CRM, además de Huly, considera según tu caso (todas las fechas de consulta 2026-09):

| CRM | Stars | Stack | Cuándo elegir |
|-----|-------|-------|---------------|
| **twenty** | 50K⭐ | TypeScript/Next | El CRM open-source más popular (#1). SPA moderna, modelado de PRM a tu gusto, autohost o cloud. Buena base para un CRM cliente con UI al día. |
| **SuiteCRM** | 5.5K⭐ | PHP | Maduro, plugins, comunidad LGPL. Buena elección clásica si prefieres PHP y muchos módulos hechos. |
| **EspoCRM** | 3K⭐ | PHP + SPA | SPA frontend + REST API PHP, self-hosted sencillo (PHP 8.3+/MySQL/Postgres). Ligero y fácil de desplegar. |
| **trycompai/crm** | 9K⭐ | agentic-first | CRM *agent-first*: los agentes IA son usuarios de primer nivel con datos/acciones expuestos vía MCP. Enfoque novedoso si quieres un CRM que tus agentes operen solos. |
| **nocobase** | 23K⭐ | No-code | Plataforma no-code AI y CRUD declarativo. Alternativa si quieres montar el modelo de datos sin escribir backend. |

Regla práctica: **twenty** si quieres el CRM más moderno y listo; **Huly** si necesitas todo-en-uno (CRM+proyectos+docs+HR); **EspoCRM** si quieres algo ligero en PHP; **trycompai/crm** si lo quieres agentic. Evalúa el coste de mantener tu instancia vs SaaS antes de self-hostear.

## Integración con Mastermind

- Base CRM+ERP para Terral (municipal)
- Sistema de tickets para proyectos de software
- Pipeline de ventas SaaS

## Referencia

- Repo: `hcengineering/platform`
- Web: https://huly.io