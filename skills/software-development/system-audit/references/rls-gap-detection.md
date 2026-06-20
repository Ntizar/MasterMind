# RLS Gap Detection — Caso TerrAn/GeoAsset v25

## Problema detectado

24 issues SEC activos por **tablas con RLS enabled pero sin policy**, o tablas sin org_id que sí la necesitan.

## Detección sistemática

### Paso 1: Tablas con RLS enabled
```python
import re
rls_enabled = re.findall(r'ALTER TABLE (\w+) ENABLE ROW LEVEL SECURITY', content)
```

### Paso 2: Tablas con policy
```python
policies = re.findall(r'CREATE POLICY (\w+) ON (\w+)', content)
tables_with_policy = set(table for _, table in policies)
```

### Paso 3: Tablas con org_id
```python
# Buscar CREATE TABLE \w+ que contenga 'org_id' en su definición
org_id_tables = []
current_table = None
for line in content.split('\n'):
    if 'CREATE TABLE' in line:
        current_table = re.search(r'CREATE TABLE (\w+)', line)
    if current_table and 'org_id' in line:
        if 'REFERENCES' in line or 'UUID' in line:
            org_id_tables.append(current_table.group(1))
```

### Paso 4: Diferencias = issues
```python
# Tablas con RLS enabled pero sin policy
rls_without_policy = set(rls_enabled) - tables_with_policy

# Tablas con org_id pero sin RLS
org_without_rls = set(org_id_tables) - set(rls_enabled)
```

## Fixes aplicados en TerrAn v25

### org_id añadido (7 tablas)
- `usuarios` → org_id UUID NOT NULL + UNIQUE(email, org_id) WHERE deleted_at IS NULL
- `firmas_electronicas` → org_id UUID NOT NULL
- `security_log` → org_id UUID NOT NULL
- `login_attempts` → org_id UUID NOT NULL
- `password_history` → org_id UUID NOT NULL
- `token_blacklist` → org_id UUID NOT NULL
- `activos_humanos` → org_id UUID NOT NULL

### RLS policies añadidas (14 tablas)
- `roles_organizacion` → tenant_isolation_roles
- `permisos_temporarios` → tenant_isolation_permisos_temp
- `grupos` → tenant_isolation_grupos
- `grupos_usuarios` → tenant_isolation_grupos_usuarios
- `system_config` → tenant_isolation_config
- `activos_humanos` → tenant_isolation_humanos
- `activos_infraestructura` → tenant_isolation_infra
- `activos_medico` → tenant_isolation_medico
- `activos_vehiculo` → tenant_isolation_vehiculo
- `departamentos` → tenant_isolation_depts
- `orden_trabajo_activos` → tenant_isolation_ow_act
- `tipos_activos` → tenant_isolation_tipos
- `asset_types` → tenant_isolation_asset_types
- `firma_electronica` → tenant_isolation_firma

### superadmin_bypass corregido
- Antes: `ro.nombre = 'superadmin'`
- Después: `ro.nivel >= 5` (admin+)
- Aplica a: activos, organizaciones

### Encriptación DNI/NSS (activos_humanos)
- `dni VARCHAR(10)` → `dni BYTEA`
- `nss VARCHAR(20)` → `nss BYTEA`
- Funciones `encriptar_dato()` y `desencriptar_dato()` con pgcrypto AES-256

### fuentes_video
- Campo `publica BOOLEAN` eliminado
- Acceso controlado por RLS + permisos en vez de campo booleano

## Resultado
- 24 issues SEC → 0 activos
- 133/143 issues total fixed
- 10 restantes: fase BL (Business Logic), no seguridad
