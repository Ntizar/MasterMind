# Patrón: Verificación de fixes en auditoría TerrAn

## Cuándo usar
Después de marcar un issue como `fixed` en `audit-state.json`, verificar que el fix es real y funcional, no solo documentado.

## Problema (iter 146, 2026-06-19)
El auditor encontró 64 issues marcados como `fixed` pero al verificar los documentos se descubrieron:
- 4 tablas con doble coma en PRIMARY KEY (`BIGSERIAL PRIMARY KEY,,`)
- 4 tablas de seguridad sin columna `org_id` referenciada por RLS policies
- Función `invalidar_tokens_usuario()` que INSERTA en audit_log sin org_id
- RENDIMIENTO-Y-NEGOCIO.md sin RLS (inconsistente con ARQUITECTURA.md)

## Verificación en 4 pasos

### 1. Sintaxis SQL válida
```bash
# Buscar dobles comas, // en SQL, otros errores de sintaxis
grep -n 'PRIMARY KEY,,' ARQUITECTURA.md
grep -n '//' ARQUITECTURA.md | grep -v '^.*--' | grep -v '^.*//'
```

### 2. Columnas referenciadas existen
```bash
# Para cada RLS policy, verificar que la columna existe
# Ejemplo: tenant_isolation_sec_log referencia org_id
grep -A2 'tenant_isolation_sec_log' ARQUITECTURA.md
# Luego verificar que security_log CREATE TABLE tiene org_id
grep -A15 'CREATE TABLE security_log' ARQUITECTURA.md
```

### 3. Funciones que INSERTAN incluyen org_id
```bash
# Buscar todas las funciones que INSERTAN en audit_log
grep -n 'INSERT INTO audit_log' ARQUITECTURA.md
# Para cada una, verificar que org_id se incluye
```

### 4. Sincronización entre documentos
```bash
# Verificar que RLS aparece en ambos documentos
grep -c 'ENABLE ROW LEVEL SECURITY' ARQUITECTURA.md
grep -c 'ENABLE ROW LEVEL SECURITY' RENDIMIENTO-Y-NEGOCIO.md
# Si RY-NEGOCIO.md tiene 0, hay inconsistencia
```

## Checklist post-fix
- [ ] Sintaxis SQL válida (sin dobles comas, sin `//` en SQL)
- [ ] Todas las columnas referenciadas existen en el CREATE TABLE
- [ ] RLS policies referencian columnas que existen
- [ ] Funciones que INSERTAN en audit_log incluyen org_id
- [ ] RENDIMIENTO-Y-NEGOCIO.md sincronizado con ARQUITECTURA.md
- [ ] DOCUMENTOS-Y-IA.md sincronizado con ARQUITECTURA.md
