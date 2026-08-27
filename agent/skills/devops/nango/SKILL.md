---
name: nango
description: "Skill: Nango — plataforma open-source para construir integraciones de producto con 800+ APIs. Maneja OAuth, API keys, token refresh, proxy de requests y ejecución de funciones de integración."
version: "1.0.0"
tags: [devops, nango, API, integrations]

---

# Skill de Nango

**Nango** es una plataforma open-source para construir **integraciones de producto** con 800+ APIs. Maneja OAuth, API keys, token refresh, proxy de requests, y ejecución de funciones de integración. Usado en producción por Replit, Ramp, Mercor y cientos más.

## Qué es

Nango permite conectar tu producto con APIs externas escribiendo la lógica de integración como **funciones TypeScript** que se despliegan en un runtime de producción. Nango se encarga de:

- **Auth**: OAuth gestionado, API keys, token refresh, multi-tenant connections
- **Proxy**: Requests autenticados con retry automático y límites de tasa
- **Functions**: Lógica de integración como funciones TypeScript con acceso API integrado, retries, almacenamiento, y observabilidad

## 3 Primitivas

### 1. Auth
OAuth gestionado, API keys, y token refresh para 800+ APIs. Incrusta un flujo de auth white-label en tu app con `nango.openConnectUI()`. Maneja credenciales, almacenamiento de tokens, y gestión de conexiones multi-tenant automáticamente.

### 2. Proxy
Realiza requests autenticados a APIs en nombre de tus usuarios. Nango resuelve el provider, inyecta credenciales, maneja retries y límites de tasa. Usa `nango.get()`, `nango.post()`, etc. con `providerConfigKey` y `connectionId`.

### 3. Functions
Escribe lógica de integración como funciones TypeScript usando `createSync()`, `createAction()`, o `createOnEvent()`. Se compilan con esbuild, se typecheck con TypeScript, y se despliegan al runtime de Nango con `nango deploy`.

## Instalación

```bash
# Instalar el CLI
npm install -D nango

# Inicializar proyecto de integraciones
nango init

# Crear una sync o action
nango create --sync <integration> <name>
nango create --action <integration> <name>

# Compilar y typecheck
nango compile

# Deploy a producción
nango deploy prod

# Dry run para debugging
nango dryrun <name> <connection_id>
```

## Variables de entorno

```bash
NANGO_SECRET_KEY_DEV=sk_dev_xxxx
NANGO_SECRET_KEY_PROD=sk_prod_xxxx
NANGO_HOSTPORT=https://api.nango.dev
```

## Cuándo usarlo

- **AI tool calling & MCP**: Dar a agentes IA la capacidad de actuar sobre APIs externas
- **Data syncing**: Sync one-way/two-way para RAG pipelines, indexing, triggers
- **Webhook processing**: Recibir y procesar webhooks de APIs externas
- **API unification**: Normalizar múltiples APIs a tu propio schema universal
- **Actions**: Escribir data y ejecutar operaciones behalf de tus usuarios
- **Per-customer config**: Customizar comportamiento de integración por cliente

## Cuándo NO usar

- Solo necesitas hacer una llamada puntual a una API → un simple `fetch()` o `curl` es suficiente
- Tu app no necesita integraciones con terceros → no hay valor añadido en montar Nango
- Necesitas control total sobre la infraestructura de auth → implementa tu propio sistema OAuth

## Estructura del proyecto

```
nango-integrations/
├── package.json          # devDependencies: nango, zod
├── tsconfig.json
├── index.ts              # Exports todas las funciones
├── .env                  # NANGO_SECRET_KEY_DEV/PROD
└── <integration>/        # ej: github/
    ├── syncs/
    │   └: fetchIssues.ts  # createSync(...)
    ├── actions/
    │   └: createIssue.ts  # createAction(...)
    └── on-events/
        └: pre-connection-deletion.ts  # createOnEvent(...)
```

## Dependencias clave

| Paquete | Versión | Uso |
|---------|---------|-----|
| `nango` | 0.70.4 | CLI + SDK (createSync, createAction, createOnEvent) |
| `@nangohq/node` | 0.70.4 | SDK de cliente para Auth/Proxy desde tu backend |
| `@nangohq/runner-sdk` | 0.70.4 | SDK para funciones (NangoActionBase, NangoSyncBase) |
| `zod` | 4.3.6 | Validación de schemas para input/output/models |

## Referencias

- [Pattern: Auth](references/pattern-auth.md) — OAuth gestionado, flujo de auth white-label, multi-tenant
- [Pattern: Proxy](references/pattern-proxy.md) — requests autenticados, retry, límites de tasa
- [Pattern: Functions](references/pattern-functions.md) — funciones de integración TypeScript, constructor de IA, deploy
