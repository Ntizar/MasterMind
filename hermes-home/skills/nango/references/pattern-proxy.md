# Pattern: Proxy con Nango

Fuente: NangoHQ/nango — README.md + src/

## Authenticated API Requests

Nango resuelve el provider, inyecta credentials, maneja retries y rate limits automáticamente.

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: 'sk_dev_xxxx' });

// GET request
const response = await nango.get({
    endpoint: '/v3/contacts',
    providerConfigKey: 'hubspot',
    connectionId: 'user_123'
});

// POST request
const created = await nango.post({
    endpoint: '/v1/contacts',
    providerConfigKey: 'salesforce',
    connectionId: 'user_123',
    data: { name: 'David', email: 'david@example.com' }
});

// PUT, DELETE, PATCH también soportados
const updated = await nango.put({
    endpoint: '/v1/contacts/123',
    providerConfigKey: 'hubspot',
    connectionId: 'user_123',
    data: { name: 'David Updated' }
});
```

## Query Params & Headers

```typescript
const response = await nango.get({
    endpoint: '/v3/contacts',
    providerConfigKey: 'hubspot',
    connectionId: 'user_123',
    params: { limit: 100, offset: 0 },
    headers: { 'X-Custom-Header': 'value' }
});
```

## Retry & Rate Limits

Nango maneja automáticamente:
- **Retry** con backoff exponencial en errores 429, 5xx
- **Rate limits** de cada provider
- **Token refresh** antes de cada request

No necesitas implementar lógica de retry manualmente.
