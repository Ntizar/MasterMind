# Patrón: Funciones RLS auxiliares con SECURITY DEFINER

## Cuándo usar
Cuando TerrAn usa RLS policies que referencian `current_user_id()`, `current_user_email()` o `current_org_id()` en las cláusulas `USING`/`FILTERING`, estas funciones DEBEN existir o PostgreSQL falla con "function does not exist".

## Implementación

```sql
-- Funciones auxiliares para RLS (SEC-037)
-- Se usan en policies y triggers. El middleware Node.js debe hacer:
--   SET LOCAL app.user_id = '<uuid>';
--   SET LOCAL app.user_email = '<email>';
--   SET LOCAL app.org_id = '<uuid>';

CREATE OR REPLACE FUNCTION current_user_id()
RETURNS UUID AS $$
BEGIN
    RETURN current_setting('app.user_id')::UUID;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;  -- Si no se ha seteado, RLS deniega por defecto
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION current_user_email()
RETURNS TEXT AS $$
BEGIN
    RETURN current_setting('app.user_email');
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;

CREATE OR REPLACE FUNCTION current_org_id()
RETURNS UUID AS $$
BEGIN
    RETURN current_setting('app.org_id')::UUID;
EXCEPTION WHEN OTHERS THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER STABLE;
```

## Claves del diseño

1. **SECURITY DEFINER** — las funciones ejecutan con los privilegios del creador (superuser), no del caller. Esto permite que RLS policies las llamen sin dar acceso directo a `current_setting`.
2. **STABLE** — garantiza que el resultado es consistente dentro de una sola query (importante para policies que se evalúan múltiples veces).
3. **EXCEPTION → NULL** — si el middleware no ha seteado el setting, devuelve NULL. En RLS, NULL en `USING` = deniega acceso. Esto es un fallback seguro: mejor denegar que exponer datos.
4. **El middleware Node.js es responsable** de hacer `SET LOCAL` al inicio de cada request con el user_id, user_email y org_id del usuario autenticado.

## Uso en policies

```sql
-- ❌ Malo: hardcodear current_setting en cada policy
CREATE POLICY bad ON activos FOR ALL
    USING (org_id = current_setting('app.org_id')::UUID);

-- ✅ Bueno: usar la función helper
CREATE POLICY good ON activos FOR ALL
    USING (org_id = current_org_id());
```

## Verificación post-deploy

```bash
# Verificar que las funciones existen
curl 'http://localhost:5432/'  # o psql: \df current_user*
# Debe mostrar: current_org_id, current_user_email, current_user_id

# Verificar que las policies referencian las funciones, no current_setting directo
grep -n 'current_org_id()' ARQUITECTURA.md
# Debe aparecer en todas las RLS policies
```

## Sesión de referencia
- 2026-06-16: Fix SEC-037 — funciones nunca definidas, RLS policies fallaban en runtime. Todas las policies actualizadas de `current_setting('app.org_id')::UUID` a `current_org_id()`.
