# AdelaCRM v2 — Schema Completo

## Entidades y relaciones

```
usuarios (独立)
empresas (1) ──── (N) contactos
   │                    │
   └──── (N) leads ────┘
            │
            ├──── (N) oportunidades
            ├──── (N) actividades
            └──── (N) notas
```

## Tablas

### usuarios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | user-{timestamp}-{random} |
| nombre | TEXT NOT NULL | Nombre |
| email | TEXT UNIQUE | Email (login) |
| pin_hash | TEXT | bcrypt hash del PIN |
| rol | TEXT | admin/vendedor |
| activo | INTEGER | 0/1 |
| creado | TEXT | ISO timestamp |

### empresas
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | emp-{timestamp}-{random} |
| cif | TEXT UNIQUE | CIF/NIF |
| nombre | TEXT NOT NULL | Nombre comercial |
| email, telefono, web | TEXT | Contacto |
| sector | TEXT | Sector industrial |
| tamano | TEXT | micro/pequeña/mediana/grande |
| direccion, ciudad, provincia, codigoPostal | TEXT | Dirección |
| notas | TEXT | Notas generales |
| creado, actualizado | TEXT | Timestamps |
| creadoPor | TEXT FK | usuarios.id |

### contactos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | con-{timestamp}-{random} |
| empresaId | TEXT FK | → empresas.id |
| nombre | TEXT NOT NULL | Nombre completo |
| email, telefono | TEXT | Contacto |
| cargo | TEXT | Cargo / puesto |
| departamento | TEXT | Departamento |
| esDecisionador | INTEGER | 0/1 |
| activo | INTEGER | 0/1 |
| creado, actualizado | TEXT | Timestamps |

### leads (pipeline)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | lead-{timestamp}-{random} |
| empresaId | TEXT FK | → empresas.id (nullable) |
| contactoId | TEXT FK | → contactos.id (nullable) |
| titulo | TEXT NOT NULL | Nombre del lead |
| descripcion | TEXT | Descripción |
| estado | TEXT | nuevo/contactado/cualificado/proposta/negociacion/ganado/perdido |
| valor | REAL | Valor estimado (€) |
| probabilidad | INTEGER | 0-100 % |
| fuente | TEXT | web/telefono/referencia/evento/otro |
| fechaCierre | TEXT | Fecha estimada de cierre |
| creado, actualizado | TEXT | Timestamps |
| creadoPor | TEXT FK | usuarios.id |

### oportunidades
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | opp-{timestamp}-{random} |
| leadId | TEXT FK | → leads.id |
| titulo | TEXT NOT NULL | Nombre |
| descripcion | TEXT | Detalles |
| valor | REAL | Valor en € |
| estado | TEXT | identificada/negociacion/ganada/perdida |
| fechaCierre | TEXT | Fecha de cierre |
| creado | TEXT | ISO timestamp |

### actividades (calendario)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | act-{timestamp}-{random} |
| leadId | TEXT FK | → leads.id (nullable) |
| contactoId | TEXT FK | → contactos.id (nullable) |
| empresaId | TEXT FK | → empresas.id (nullable) |
| tipo | TEXT | llamada/email/reunion/tarea/nota |
| titulo | TEXT NOT NULL | Descripción breve |
| descripcion | TEXT | Detalles |
| fecha | TEXT | ISO timestamp |
| duracion | INTEGER | Minutos |
| resultado | TEXT | completada/pendiente/cancelada |
| esRegistro | INTEGER | 0=evento futuro, 1=registro de pasada |
| creado | TEXT | ISO timestamp |
| creadoPor | TEXT FK | usuarios.id |

### notas (polimórficas)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | TEXT PK | note-{timestamp}-{random} |
| entidadTipo | TEXT | lead/empresa/contacto/oportunidad |
| entidadId | TEXT | ID de la entidad |
| contenido | TEXT NOT NULL | Texto |
| creado | TEXT | ISO timestamp |
| creadoPor | TEXT FK | usuarios.id |

## Pipeline States

```
nuevo → contactado → cualificado → proposta → negociacion
                                                ├── ganado ✅
                                                └── perdido ❌
```

## API Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/auth/login | Login (email + pin) |
| GET | /health | Healthcheck |
| GET/POST | /api/empresas | Listar/crear empresas |
| GET/PUT/DELETE | /api/empresas/:id | CRUD empresa |
| GET/POST | /api/contactos | Listar/crear contactos |
| GET/PUT/DELETE | /api/contactos/:id | CRUD contacto |
| GET/POST | /api/leads | Listar/crear leads |
| GET/PUT/DELETE | /api/leads/:id | CRUD lead |
| GET | /api/leads/stats | Estadísticas dashboard |
| GET/POST | /api/oportunidades | Listar/crear oportunidades |
| DELETE | /api/oportunidades/:id | Eliminar oportunidad |
| GET/POST | /api/actividades | Listar/crear actividades |
| PUT/DELETE | /api/actividades/:id | Actualizar/eliminar actividad |
| GET/POST | /api/notas | Listar/crear notas (por entidad) |
| DELETE | /api/notas/:id | Eliminar nota |
| GET/POST | /api/usuarios | Listar/crear usuarios |
| PUT | /api/usuarios/:id | Actualizar usuario |
