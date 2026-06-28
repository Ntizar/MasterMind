# Pattern: Auth con Nango

Fuente: NangoHQ/nango — README.md

## Managed OAuth

Nango maneja OAuth, API keys, y token refresh para 800+ APIs automáticamente.

### White-label Auth Flow

```typescript
// Embed auth in your frontend
nango.openConnectUI({ 
    onEvent: (event) => { 
        if (event.type === 'AUTH_SUCCESS') {
            console.log('Connected:', event.connectionId);
        }
    } 
});
```

### Multi-Tenant Connections

```typescript
import { Nango } from '@nangohq/node';

const nango = new Nango({ secretKey: 'sk_dev_xxxx' });

// List all connections for a user
const connections = await nango.listConnections({ userId: 'user_123' });

// Get a specific connection
const connection = await nango.getConnection('github', 'user_123');

// OAuth credentials are managed automatically
// Token refresh happens transparently
```

### Connection Management

```typescript
// Delete a connection
await nango.deleteConnection('github', 'user_123');

// Get connection metadata
const metadata = await nango.getConnectionMetadata('github', 'user_123');
// { connectionId: 'xxx', connectionConfig: {...}, oauthCredential: {...} }
```

## API Key Auth

```typescript
// For APIs that use API keys instead of OAuth
const connection = await nango.createConnection({
    providerConfigKey: 'stripe',
    connectionId: 'customer_123',
    credentials: {
        type: 'API_KEY',
        access_token: 'sk_live_xxxx'
    }
});
```

## Token Refresh

Nango maneja el token refresh automáticamente. No necesitas preocuparte por:
- Expiración de access tokens
- Refresh token rotation
- Token storage
- Multi-tenant credential management

Simplemente usa `nango.get()`, `nango.post()`, etc. y Nango inyecta las credenciales.
