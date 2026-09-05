---
name: huly-crm-erp-platform
description: "Usa a desplegar Huly, la plataforma de gestión (self-host)."
version: "2.0.0"
tags: [huly, crm, erp, plataforma, self-host, docker, eclipes]
related_skills: [huly-crm-erp-platform, nocobase-nocode-backend, backend]
---

# Huly — plataforma todo-en-uno de gestión (self-host)

> ⚠️ Corrección 2026-09-05 (auditoría): licencia **EPL-2.0** (no Apache 2.0), el self-host oficial es **`hcengineering/huly-selfhost`** (no clonar `platform`) y el acceso es **http://localhost:8087** (no 8080).

**Repo:** `https://github.com/hcengineering/platform` (TypeScript, ~27K⭐) · Licencia: **EPL-2.0**. Self-host: `hcengineering/huly-selfhost`.

## When to Use

- Cuando pidas una **plataforma de gestión empresarial todo-en-uno** (menSAJE + project management + CRM + HRM) autoalojada, tipo Notion/ClickUp.

## Uso (self-host)

```bash
git clone https://github.com/hcengineering/huly-selfhost.git
cd huly-selfhost
docker compose up -d
# acceso: http://localhost:8087
```

## Módulos

- Chat, Project Management, CRM, HRM, ATS (chat + proyectos + CRM + RRHH + recruiting).
- *(No sobre-afirmar "Accounting/Inventory/ERP completo" — no están como módulos explícitos.)*
- El hosting gratuito de Huly se está discontinuando → migrar a self-host.

## Pitfalls

- Licencia: **EPL-2.0**, no Apache 2.0.
- Self-host: **huly-selfhost**, no `docker-compose up` sobre `hcengineering/platform`.
- Puerto: **8087**.

## Verificación

- `docker compose up -d` en huly-selfhost y abrir `http://localhost:8087`.
