# Nango

**URL:** https://github.com/NangoHQ/nango
**Categoría:** Backend/APIs
**Estrellas:** 8,971
**Lenguaje:** TypeScript
**Licencia:** Elastic License

## ¿Qué hace?

Nango es una plataforma open-source para construir **integraciones de productos** con 800+ APIs. Permite conectar tu producto y agentes de IA con APIs externas, gestionando autenticación (OAuth, API keys), ejecución, escalado y observabilidad.

Tres primitivas principales:
1. **Auth** — OAuth, API keys y token refresh para 800+ APIs. UI white-label embebible.
2. **Proxy** — Peticiones autenticadas a APIs externas a través del proxy de Nango (resuelve provider, inyecta credenciales, maneja retries y rate limits).
3. **Functions** — Lógica de integración como funciones TypeScript desplegadas en un runtime de producción.

## Casos de uso

1. **AI Tool Calling & MCP** — Dar a agentes IA la capacidad de actuar sobre APIs externas (GitHub, Slack, HubSpot, etc.)
2. **Data Syncing** — Sincronización bidireccional para pipelines RAG, indexación y triggers
3. **Webhook Processing** — Recibir y procesar webhooks de APIs externas de forma fiable
4. **API Unification** — Normalizar múltiples APIs a un esquema universal propio
5. **Actions** — Escribir datos y ejecutar operaciones en nombre de usuarios
6. **Per-customer config** — Personalizar comportamiento de integración por cliente
7. **Embed auth flow** — Embeber flujo de autenticación OAuth en tu producto

## Snippets útiles

### 1. Inicialización y proxy requests

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: '<NANGO-SECRET-KEY>' });

// Hacer petición autenticada a cualquier API
const response = await nango.get({
    endpoint: '/v3/contacts',
    providerConfigKey: '<INTEGRATION-ID>',
    connectionId: '<CONNECTION-ID>'
});

// POST request
const created = await nango.post({
    endpoint: '/v3/deals',
    providerConfigKey: 'hubspot',
    connectionId: 'conn_abc123',
    data: { properties: { dealname: 'New Deal', amount: 5000 } }
});
```

### 2. Embed auth flow en frontend

```typescript
import Nango from '@nangohq/frontend';

const session = await fetch('/api/nango/session', { method: 'POST' });
const { connectSessionToken } = await session.json();

const nango = new Nango({ connectSessionToken });

nango.openConnectUI({
    onEvent: (event) => {
        console.log(event);
        if (event.type === 'CONNECT') {
            // Refresh UI, show success, etc.
        }
    }
});
```

### 3. Custom integration function (TypeScript)

```typescript
// Integración personalizada como función TypeScript
export default async function run(nango: Nango) {
    const { owner, repo, title, body } = nango.input;
    
    const response = await nango.post({
        endpoint: `/repos/${owner}/${repo}/issues`,
        data: { title, body }
    });
    
    return response.data;
}
```

### 4. Tool calling para AI Agents (OpenAI)

```typescript
import { Nango } from '@nangohq/node';
import OpenAI from 'openai';

const nango = new Nango({ secretKey: process.env.NANGO_SECRET_KEY! });
const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });

// Tool definition
const tools = [{
    type: 'function' as const,
    name: 'who_am_i',
    description: 'Get the current HubSpot user information.',
    strict: true,
    parameters: { type: 'object', properties: {}, required: [], additionalProperties: false }
}];

// Ejecutar tool call
const response = await client.responses.create({
    model: 'gpt-5',
    input: [{ role: 'user', content: 'Tell me about my HubSpot account.' }],
    tools
});

for (const item of response.output) {
    if (item.type !== 'function_call' || item.name !== 'who_am_i') continue;
    const connId = await getUserConnection('user_123');
    const result = await nango.triggerAction('hubspot', connId, 'whoami', {});
}
```

### 5. Obtener credentials / token de conexión

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: process.env.NANGO_SECRET_KEY! });

// Obtener conexión completa (incluye credentials)
const connection = await nango.getConnection('hubspot', 'conn_abc123');
console.log(connection.credentials);

// Obtener solo el access token (OAuth2)
const accessToken = await nango.getToken('hubspot', 'conn_abc123');

// Obtener metadata personalizada
const metadata = await nango.getMetadata('hubspot', 'conn_abc123');

// Set metadata
await nango.setMetadata('hubspot', 'conn_abc123', { plan: 'enterprise', region: 'eu' });
```

### 6. Webhook signature verification

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: process.env.NANGO_SECRET_KEY! });

// Verificar webhook entrante (recomendado - HMAC-SHA256)
const isValid = nango.verifyIncomingWebhookRequest(
    rawBodyString,
    { 'x-nango-hmac-sha256': signatureFromHeader }
);
```

### 7. Trigger action desde backend

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: process.env.NANGO_SECRET_KEY! });

// Sincronizar
const result = await nango.triggerAction(
    'github',
    'conn_abc123',
    'get-repository',
    { owner: 'NangoHQ', repo: 'nango' }
);

// Asíncrono (para operaciones largas)
const { id, statusUrl } = await nango.triggerActionAsync(
    'github', 'conn_abc123', 'bulk-import', { files: ['a.csv', 'b.csv'] }
);
const asyncResult = await nango.getAsyncActionResult({ id });
```

## Cómo integrarlo en proyectos

### Instalación
```bash
npm install @nangohq/node
# o
yarn add @nangohq/node
```

### Frontend
```bash
npm install @nangohq/frontend
```

### Arquitectura de integración

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Tu App     │────▶│  Nango API   │────▶│  API Externa    │
│  (Frontend) │     │  (Proxy)     │     │  (GitHub, etc.) │
└─────────────┘     └──────────────┘     └─────────────────┘
                         │
                    ┌──────────┐
                    │  Auth    │
                    │ Manager  │
                    │ (OAuth)  │
                    └──────────┘
```

### Flujo típico

1. **Crear integración** en Nango Dashboard (configurar OAuth/API keys)
2. **Embeber Connect UI** en tu frontend para que usuarios autoricen
3. **Usar Proxy** para hacer peticiones autenticadas
4. **Escribir funciones** personalizadas para lógica de negocio
5. **Conectar con AI** vía tool calling o MCP

### Compatibilidad

- Backend: Cualquier lenguaje (Node.js, Python, Go, Java, etc.)
- AI tools: Cursor, Codex, Claude Code, LangChain
- Agent SDKs: MCP, tool calling
- Infra: Nango Cloud o self-hosted (Docker)

### Compliance

- SOC 2 Type II
- HIPAA
- GDPR

## Fecha de aprendizaje: 2026-05-27
