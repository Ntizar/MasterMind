# Caso: Tabla usuarios sin org_id — RLS runtime failure

## Síntoma

La tabla `usuarios` tiene una RLS policy `tenant_isolation_usuarios` que referencia `org_id`, pero la tabla no tiene la columna `org_id`. PostgreSQL permite crear la policy, pero en runtime falla con:

```
ERROR:  column "org_id" does not exist
```

## Causa

La tabla `usuarios` fue definida sin columna `org_id`, pero la RLS policy se escribió asumiendo que existía. Esto rompe el aislamiento multi-tenant a nivel de BD.

## Verificación

```sql
-- Verificar si la columna existe
SELECT column_name FROM information_schema.columns
WHERE table_name = 'usuarios' AND column_name = 'org_id';
-- Si devuelve 0 filas → BUG

-- Verificar policies que referencian la columna
SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename = 'usuarios';
```

## Solución

1. Añadir la columna `org_id UUID NOT NULL` a la tabla `usuarios`
2. Migrar datos existentes (asignar org_id por defecto o por rol)
3. Recrear la RLS policy con la columna correcta
4. Añadir índices sobre `org_id` para rendimiento

## Impacto

- **Multi-tenant roto:** no hay aislamiento de datos entre organizaciones a nivel de BD
- **Seguridad:** un usuario de una organización podría acceder a datos de otra
- **Runtime error:** cualquier query que pase por RLS falla silenciosamente

## Referencia

- Descubierto: iter 144, 2026-06-18
- Issue asociado: SEC-064 en audit-state.json
