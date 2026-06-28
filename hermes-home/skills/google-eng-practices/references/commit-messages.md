# Guía: Escribir Mensajes de Commit (CL Descriptions)

Fuente: google/eng-practices — review/developer/cl-descriptions.md

## Estructura de un Buen Commit Message

```
[Resumen corto en imperativo]

Explicación del qué y por qué. Contexto, decisiones, alternativas
consideradas. Links a issues o docs relevantes.
```

### Regla de la Primera Línea

- **Corta** (< 50 caracteres idealmente)
- **Imperativo**: "Fix bug" NO, "Fix auth bug in login" SÍ
- **Completa**: como una orden
- **Separada del cuerpo** con línea en blanco

### Ejemplos de Primera Línea

```
✅ Fix auth bug causing session timeout on mobile
✅ Add rate limiting to /api/search endpoint
✅ Refactor user model to use enum for roles
✅ Update dependency: upgrade axios to v1.7.0
✅ Remove deprecated config option from docker-compose
```

```
❌ Fix
❌ Fixed the thing
❌ Changes
❌ WIP
❌ Update
```

### Cuerpo: Qué Incluir

1. **Qué** cambia exactamente
2. **Por qué** se hace este cambio
3. **Contexto**: decisiones tomadas, alternativas consideradas
4. **Links**: issues, PRs relacionados, docs
5. **Impacto**: breaking changes, migration notes

### Ejemplo Completo: Funcionalidad Nueva

```
Add OAuth2 login support for GitHub

Users can now authenticate via GitHub OAuth2 in addition to email/password.
This adds the OAuth2 flow using the existing auth middleware.

Changes:
- Added GitHub OAuth2 client configuration
- Created /auth/github callback endpoint
- Updated login page with GitHub button
- Added migration for social_auth table

Closes #247
```

### Ejemplo Completo: Refactoring

```
Extract payment processing into dedicated service

The checkout controller was handling payment logic directly, making it
hard to test and reuse. This extracts the payment logic into a
PaymentService class.

Benefits:
- Checkout controller reduced from 200 to 80 lines
- PaymentService is now unit-testable
- Payment logic can be reused in subscription flows

The migration maintains backward compatibility with the existing
checkout flow. No breaking changes.
```

### Ejemplo Completo: Bug Fix

```
Fix race condition in cache invalidation

When multiple requests invalidated the same cache key simultaneously,
the last writer would win, causing stale data to be served.

Fixed by adding a distributed lock around cache invalidation using
Redis SETNX with TTL. Lock expires after 5 seconds to prevent deadlocks.

This was discovered during load testing at 1000 RPS.

Fixes #312
```

## Tags Útiles para Commits

```
[breaking] - Breaking change, needs migration
[security] - Security fix or improvement
[performance] - Performance optimization
[docs] - Documentation only
[tests] - Test additions/fixes
[refactor] - Code restructuring, no behavior change
[feat] - New feature
[fix] - Bug fix
[chore] - Maintenance tasks
```

## Commit Conventional (alternativa)

```
type(scope): short summary

Body with details.

BREAKING CHANGE: description of breaking change.
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Ejemplo:
```
feat(auth): add OAuth2 GitHub login support

Users can now authenticate via GitHub OAuth2...

Closes #247
```

## Lo que NUNCA hacer en un commit message

- "Fix bug" (¿qué bug?)
- "Update" (¿qué actualizaste?)
- "WIP" (no hagas commits WIP al main)
- Mensajes en mayúsculas todo
- Mensajes sin contexto
