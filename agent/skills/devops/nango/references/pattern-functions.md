# Pattern: Functions con Nango

Fuente: NangoHQ/nango — README.md + src/

## Integration Functions

Escribe lógica de integración como TypeScript functions que se despliegan al runtime de Nango.

### Sync Function (Data Sync)

```typescript
// syncs/fetchIssues.ts
import { NangoSync } from '@nangohq/runner-sdk';

export default async function run(nango: NangoSync) {
    const response = await nango.get({
        endpoint: `/repos/${nango.input.owner}/${nango.input.repo}/issues`,
        providerConfigKey: 'github',
        connectionId: nango.connectionId
    });

    // Return data to be stored
    return response.data;
}
```

### Action Function (Write/Execute)

```typescript
// actions/createIssue.ts
import { NangoAction } from '@nangohq/runner-sdk';

export default async function run(nango: NangoAction) {
    const { owner, repo, title, body } = nango.input;
    
    const response = await nango.post({
        endpoint: `/repos/${owner}/${repo}/issues`,
        providerConfigKey: 'github',
        connectionId: nango.connectionId,
        data: { title, body }
    });
    
    return response.data;
}
```

### On-Event Function (Webhooks)

```typescript
// on-events/pre-connection-deletion.ts
import { NangoOnEvent } from '@nangohq/runner-sdk';

export default async function run(nango: NangoOnEvent) {
    if (nango.event.type === 'PRE_CONNECTION_DELETION') {
        // Clean up your data before connection is deleted
        await cleanupUserRecords(nango.event.connectionId);
    }
}
```

## Project Structure

```
nango-integrations/
├── package.json
├── tsconfig.json
├── index.ts              # Exports all functions
├── .env
└── github/
    ├── syncs/
    │   └── fetchIssues.ts
    ├── actions/
    │   └── createIssue.ts
    └── on-events/
        └── pre-connection-deletion.ts
```

## index.ts — Exports

```typescript
// index.ts
export { default as fetchIssues } from './github/syncs/fetchIssues';
export { default as createIssue } from './github/actions/createIssue';
```

## Deploy & Run

```bash
# Compile and typecheck
nango compile

# Deploy to production
nango deploy prod

# Dry run for debugging
nango dryrun fetchIssues <connection_id>

# Run sync manually
nango sync run fetchIssues --connection <connection_id>
```

## AI Builder

Puedes usar el AI builder de Nango para generar funciones desde una descripción:
- Describe qué quieres hacer (ej: "fetch GitHub issues and create Jira tickets")
- Nango genera el TypeScript automáticamente
- Revisas y ajustas el código generado
- Desplegas con `nango deploy`

## Zod Validation

```typescript
import { z } from 'zod';

const schema = z.object({
    owner: z.string(),
    repo: z.string(),
    title: z.string(),
    body: z.string().optional()
});

export default async function run(nango: NangoAction) {
    const validated = schema.parse(nango.input);
    // ... use validated data
}
```
