---
name: nango
description: "Usa a integrar APIs con Nango (900+ integraciones)."
version: "2.0.0"
tags: [nango, integracion, api, oauth, saas, sync, backend]
related_skills: [nango, api-mega-catalog, postgres-mcp]
---

# Nango — integración de APIs/SaaS y sync (900+)

> ⚠️ Corrección 2026-09-05 (auditoría): son **900+ APIs**, no 800+; licencia **Elastic License 2.0**; versiones de paquetes actuales 0.71.x.

**Repo:** `https://github.com/NangoHQ/nango` (TypeScript, ~11.7K⭐) · Licencia: **Elastic 2.0** (self-hostable open-source).

## When to Use

- Cuando pidas **integrar muchas APIs/SaaS** en tu backend (OAuth, sync de datos, tokens) sin escribirlas a mano.

## Uso

```bash
npm install nango            # CLI / orquestador
npm install @nangohq/node    # SDK Node
npm install @nangohq/runner-sdk
```

- Flujo en vivo con `nango.openConnectUI()` para conectarse a proveedores; el paquete npm `nango` es la CLI.

## Pitfalls

- **900+** integraciones (no 800+).
- Licencia **Elastic 2.0** (open-source self-hostable, pero no MIT).
- Versiones: 0.71.x (nango, @nangohq/node, @nangohq/runner-sdk).

## Verificación

- Registrar un proveedor, hacer OAuth y comprobar que los datos se sincronizan.
