---
name: web-auth-user-management
version: "1.0.0"
description: "Montar login y gestión de usuarios en webs y apps."
tags: [auth, login, usuarios, sesion, oauth, jwt, cookies, registro, authjs, supabase, firebase, webapp]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [auth, login, usuarios, sesion, oauth, jwt, cookies, authjs, supabase]
    related_skills: [node-backend-patterns, infraestructura-nodejs, static-digest-pipeline, browser-local-tools]
---

# Autenticación y Gestión de Usuarios en Webs

## Cuándo usar

Cuando tengas que añadir **login, registro, sesión o gestión de usuarios** a una web (dashboards privados,
apps con cuentas, APIs protegidas, áreas de cliente).

## Decisión previa: ¿necesitas backoffice propio o un proveedor?

Antes de escribir código, decide el enfoque según el caso:

1. **Web estática / sin backend** (GitHub Pages, Vercel, vite build): **NUNCA pongas la validación en el navegador**
   (es trasteable). Usa un **servicio BaaS** (Supabase/ Firebase) o un **provider OAuth** — el login se valida en su servidor.
2. **App Node/backend propio**: Auth.js (antes NextAuth) o un servidor con **JWT + httpOnly cookie** (patrón SOLIDO).
3. **Solo "área logueada" sin usuarios complejos**: un **provider OAuth** (Google, GitHub) con un único botón.

## Patrón recomendado: SPA + backend JWT en httpOnly cookie

El patrón más robusto para un SPA:

```
login (POST /auth/login → email+password)
  → backend verifica (bcrypt) y emite JWT firmado
  → se guarda en cookie httpOnly + SameSite=Lax + Secure
  → frontend llama a /me y /logout
```

- **Password: hashear con bcrypt/argon2** (nunca en texto plano, nunca MD5/SHA1).
- **Token: JWT con expiración corta** (access ~15min) + **refresh token** en cookie httpOnly.
- **Cookie**: `httpOnly` (no legible por JS → mitiga XSS), `SameSite=Lax` (mitiga CSRF), `Secure` (solo HTTPS).
- **CSRF**: con SameSite=Lax y peticiones con header custom, en la mayoría de casos es suficiente; si no, token anti-CSRF.
- **Revalidación**: nunca confíes solo en el frontend; cada endpoint protegido debe verificar el token en el server.

## Alternativas listas (sin montar auth a mano)

| Opción | Cuándo | Pros |
|--------|--------|------|
| **Supabase Auth** | Web/SPA con backend o sin él | Gmail, GitHub, magic link, email+pass; JS SDK; RLS en Postgres para datos por usuario |
| **Firebase Auth** | App móvil/web | Integración ecosistema Firebase, social login, anónimo |
| **Auth.js (NextAuth)** | App Next.js | Middleware por proveedor, sesión con JWT o DB, Google/GitHub/OAuth + credentials |
| **Clerk / Auth0** | Sin querer gestionar | Login gestionado, multi-tenant, listo para producto, con costo |
| **Casdoor / Keycloak** | SSO corporativo/self-hosted | AD/LDAP, OIDC, MFA, self-hosted |

**Regla David:** para dashboards temporales o demos, **Supabase Auth** (o un provider OAuth directo) es lo más rápido
y sin secretos en el repo. Si luego crece, migra a backend propio con JWT.

## Supabase Auth — receta rápida

```js
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(url, anonKey)  // anonKey es público (RLS protege los datos)

// Registrar
await supabase.auth.signUp({ email, password })
// Login
await supabase.auth.signInWithPassword({ email, password })
// Provider social
await supabase.auth.signInWithOAuth({ provider: 'google' })
// Sesión actual / logout
supabase.auth.getSession(); await supabase.auth.signOut()
```

Protege los datos con **Row Level Security (RLS)** en Postgres:

```sql
alter table perfiles enable row level security;
create policy "cada usuario ve su perfil"
  on perfiles for select using (auth.uid() = id);
```

## Patrón multi-tenant (varios clientes/usuarios con roles)

- Añade columna `tenant_id`/`org_id` + columna `role` ('admin','user','viewer').
- Usa **RLS o middleware** que filtre por el tenant del usuario en todo query.
- Nunca asumas el rol desde el frontend — verifícalo en el server.

## Pitfalls

- **XSS**: en un SPA con token en localStorage, un XSS roba el token. Usa **cookie httpOnly** siempre que puedas.
- **CSRF**: cookies con `SameSite=Lax` o envía header custom `X-Requested-With`.
- **Secrets**: la service_role / api key de servidor va en `.env`, NUNCA en el repo. Ya es regla del sistema.
- **JWT sin expiración** o sin verificar firma = puerta abierta. Verifica siempre (firma + aud + exp).
- **CORS**: el frontend y el auth deben tener el origen correcto o el login falla silenciosamente.
- **Migración**: si ya tenías contraseñas en claro, fuerza reset; no hay forma segura de "adivinar" el hash.

## Verificación

1. Registro → login → `/me` devuelve el usuario correcto.
2. Deslogueado → endpoint protegido devuelve 401 (no datos).
3. Token inválido/expirado → 401, no crash.
4. Revisa en DevTools la cookie: `httpOnly`, `Secure`, `SameSite`.
5. Doble pestaña o incógnito → la sesión es por navegador/expira correctamente.

## Referencia

- Supabase Auth: https://supabase.com/docs/guides/auth
- Auth.js: https://authjs.dev
- OWASP Auth Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
