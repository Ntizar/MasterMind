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

## Integración con Mastermind

- Base CRM+ERP para Terral (municipal)
- Sistema de tickets para proyectos de software
- Pipeline de ventas SaaS

## Referencia

- Repo: `hcengineering/platform`
- Web: https://huly.io