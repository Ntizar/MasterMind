# Conexiones Flexibles entre Entidades — Patrón Arquitectónico

## Concepto

Sistema genérico que permite vincular CUALQUIER entidad del CRM con CUALQUIERA otra, sin necesidad de crear tablas intermedias por cada combinación. Cada usuario puede definir sus propios tipos de conexión.

## Tablas

```sql
-- Catálogo de tipos de conexión (configurable por usuario)
CREATE TABLE tipos_conexion (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE,           -- 'proveedor_de', 'trabaja_en', 'familiar_de'
  descripcion TEXT,
  color TEXT DEFAULT '#2563eb',
  icono TEXT DEFAULT '🔗',
  entidadOrigen TEXT NOT NULL DEFAULT '*',   -- '*' = cualquier entidad
  entidadDestino TEXT NOT NULL DEFAULT '*',
  bidireccional INTEGER DEFAULT 1,          -- 1=bidireccional, 0=unidireccional
  creado TEXT NOT NULL
);

-- Conexiones reales entre entidades
CREATE TABLE entidades_conectadas (
  id TEXT PRIMARY KEY,
  tipoConexionId TEXT NOT NULL,
  entidadOrigenTipo TEXT NOT NULL,     -- 'empresa', 'contacto', 'empleado', etc.
  entidadOrigenId TEXT NOT NULL,
  entidadDestinoTipo TEXT NOT NULL,
  entidadDestinoId TEXT NOT NULL,
  peso INTEGER DEFAULT 1,              -- fuerza de la conexión
  notas TEXT,
  creado TEXT NOT NULL,
  FOREIGN KEY (tipoConexionId) REFERENCES tipos_conexion(id)
);
```

## API

```
GET    /api/conexiones?origenTipo=empresa&origenId=X    — conexiones de una entidad
POST   /api/conexiones                                   — crear conexión
DELETE /api/conexiones/:id                                — eliminar conexión
GET    /api/conexiones/grafo/:tipo/:id?profundidad=2     — grafo N niveles
GET    /api/conexiones/tipos                              — listar tipos disponibles
POST   /api/conexiones/tipos                              — crear tipo personalizado
DELETE /api/conexiones/tipos/:id                          — eliminar tipo
```

## Grafo de conexiones

El endpoint `/grafo/:tipo/:id` devuelve un árbol de relaciones hasta N niveles de profundidad:

```typescript
async function obtenerGrafoConexion(
  entidadTipo: string, entidadId: string, profundidad: number = 2
) {
  const conexiones = await obtenerConexiones(entidadTipo, entidadId)
  // Para cada conexión, buscar recursivamente (limitado por profundidad)
  return { origen: { tipo: entidadTipo, id: entidadId }, conexiones: [...] }
}
```

## Uso típico

- **Empleado → Empresa:** tipo "trabaja_en"
- **Contacto → Empresa:** tipo "es_empleado_de"
- **Proveedor → Producto:** tipo "suministra"
- **Proyecto → Contacto:** tipo "dirigido_por"
- **Lead → Contacto:** tipo "referido_por"
- **Cualquier entidad → Cualquier entidad:** tipo personalizado

## Ventaja vs tablas intermedias

| Enfoque | Ventaja | Desventaja |
|---------|---------|------------|
| Tablas intermedias (empresa_contacto, empleado_proyecto...) | Query SQL simple, tipos estrictos | Escala O(n²) — cada combinación = tabla nueva |
| Conexiones flexibles | Escala O(1) — una sola tabla para todo | Query más complejo, menos tipado |
