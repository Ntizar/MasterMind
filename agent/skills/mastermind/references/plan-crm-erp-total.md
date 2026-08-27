# Plan Maestro: AdelaCRM → CRM + ERP Total

**Versión:** 2.0 — Junio 2026
**Autor:** David Antizar
**Arquitectura:** Marca blanca, multi-empresa, modular, API-first

---

## Índice

1. [Visión General](#1-visión-general)
2. [Estado Actual (AdelaCRM v2.0)](#2-estado-actual)
3. [Roadmap de Implementación](#3-roadmap-de-implementación)
4. [Arquitectura de Módulos](#4-arquitectura-de-módulos)
5. [Esquema de Base de Datos](#5-esquema-de-base-de-datos)
6. [API por Módulo](#6-api-por-módulo)
7. [Flujo de Datos entre Módulos](#7-flujo-de-datos)
8. [Seguridad y Cumplimiento](#8-seguridad-y-cumplimiento)
9. [Plan de Despliegue](#9-plan-de-despliegue)

---

## 1. Visión General

AdelaCRM evoluciona a un **CRM + ERP total** que gestiona desde la captación de un lead hasta el cobro final de una factura. Unifica en una sola plataforma:

- **CRM:** Contactos, leads, pipeline de ventas, oportunidades
- **Ventas:** Presupuestos, pedidos, facturación, cobros
- **Operaciones:** Compras, proveedores, inventario, proyectos
- **Soporte:** Tickets, contratos, base de conocimiento
- **RRHH:** Empleados, ausencias, fichaje
- **Financiero:** Contabilidad, informes, VeriFactu, SII
- **Marketing:** Campañas, segmentación, automatizaciones
- **Administración:** Multi-tenant, marca blanca, roles y permisos

### Principios de diseño

| Principio | Descripción |
|-----------|-------------|
| **Modularidad** | Cada módulo se activa/desactiva por instancia |
| **Multi-tenant** | Una instalación aloja múltiples empresas aisladas |
| **API-first** | Todos los módulos exponen REST + Webhooks |
| **Mobile-ready** | 100% responsive, PWA preparada |
| **Auditable** | Registro inmutable de cada acción |
| **Cumplimiento** | VeriFactu, RGPD, Ley Crea y Crece |

---

## 2. Estado Actual

### AdelaCRM v2.0 — Implementado y funcionando ✅

```
src/
├── server.ts           # Express + rutas
├── db.ts               # SQLite + persistencia
├── types.ts            # Interfaces TS
├── config.ts           # JWT_SECRET compartido
├── middleware/auth.ts  # JWT auth middleware
└── routes/
    ├── auth.ts         # Login + perfil
    ├── usuarios.ts     # CRUD usuarios (admin)
    ├── empresas.ts     # CRUD empresas
    ├── contactos.ts    # CRUD contactos
    ├── leads.ts        # Pipeline Kanban + stats
    ├── oportunidades.ts# CRUD oportunidades
    ├── actividades.ts  # Calendario de actividades
    └── notas.ts        # Notas polimórficas
```

### Frontend actual (`public/`)
```
public/
├── index.html          # SPA con 7 tabs
├── css/crm.css         # Aurora + Liquid Glass
└── js/crm.js           # Lógica frontend
```

### Tablas SQL existentes
- `usuarios` — Auth + roles (admin/vendedor/gestor)
- `empresas` — Datos fiscales + contacto
- `contactos` — Personas vinculadas a empresas
- `leads` — Pipeline con estados (nuevo→perdido)
- `oportunidades` — Valor €, fechas cierre
- `actividades` — Calendario (llamada/email/reunion/tarea/nota)
- `notas` — Notas polimórficas por entidad

---

## 3. Roadmap de Implementación

### Fase 1 — Núcleo Comercial (AHORA)
| Módulo | Prioridad | Dependencias | Estado |
|--------|-----------|--------------|--------|
| Productos/Servicios | 🔴 Crítica | — | ⏳ Pendiente |
| Presupuestos | 🔴 Crítica | Productos, Contactos | ⏳ Pendiente |
| Facturación básica | 🔴 Crítica | Presupuestos, Productos | ⏳ Pendiente |
| Cobros | 🟡 Alta | Facturas | ⏳ Pendiente |

### Fase 2 — Operaciones (Siguiente)
| Módulo | Prioridad | Dependencias | Estado |
|--------|-----------|--------------|--------|
| Proveedores | 🔴 Crítica | Productos | ⏳ Pendiente |
| Inventario/Almacén | 🟡 Alta | Productos, Proveedores | ⏳ Pendiente |
| Proyectos + Tareas | 🟡 Alta | Contactos, Presupuestos | ⏳ Pendiente |
| VeriFactu AEAT | 🔴 Crítica | Facturación | ⏳ Pendiente |

### Fase 3 — Servicio y Personas
| Módulo | Prioridad | Dependencias | Estado |
|--------|-----------|--------------|--------|
| Tickets/Soporte | 🟡 Alta | Contactos, Proyectos | ⏳ Pendiente |
| RRHH | 🟢 Media | — | ⏳ Pendiente |
| Contratos | 🟡 Alta | Contactos, Presupuestos | ⏳ Pendiente |
| Automatizaciones | 🟢 Media | Todos los módulos | ⏳ Pendiente |

### Fase 4 — Enterprise
| Módulo | Prioridad | Dependencias | Estado |
|--------|-----------|--------------|--------|
| Contabilidad + Informes | 🟡 Alta | Facturación, Cobros, Compras | ⏳ Pendiente |
| Marketing | 🟢 Media | Contactos, Segmentación | ⏳ Pendiente |
| SuperAdmin + Multi-tenant | 🟢 Media | Todos los módulos | ⏳ Pendiente |
| Panel Config empresa | 🟡 Alta | SuperAdmin | ⏳ Pendiente |

---

## 4. Arquitectura de Módulos

### Mapa de dependencias entre módulos

```
                    ┌─────────────┐
                    │  USUARIOS   │
                    │  + ROLES    │
                    └──────┬──────┘
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
┌──────────┐      ┌──────────────┐      ┌──────────────┐
│ EMPRESAS │      │  CONTACTOS   │      │  PROVEEDORES │
│ (clientes)│     │  (personas)  │      │  (compras)   │
└────┬─────┘      └──────┬───────┘      └──────┬───────┘
     │                   │                     │
     ▼                   ▼                     ▼
┌──────────┐      ┌──────────────┐      ┌──────────────┐
│  LEADS   │◄─────│  ACTIVIDADES │      │  INVENTARIO  │
│ (pipeline)│     │  (timeline)  │      │  (stock)     │
└────┬─────┘      └──────────────┘      └──────┬───────┘
     │                                         │
     ▼                                         │
┌──────────────┐                               │
│ OPORTUNIDADES│                               │
│ (valor €)    │                               │
└──────┬───────┘                               │
       │                                       │
       ▼                                       │
┌──────────────┐                        ┌──────────────┐
│ PRESUPUESTOS │◄───────────────────────│  PRODUCTOS   │
│ (cotización) │                        │  (catálogo)  │
└──────┬───────┘                        └──────────────┘
       │
       ▼
┌──────────────┐      ┌──────────────┐
│  PEDIDOS     │─────►│  PROYECTOS   │
│ (venta)      │      │  + TAREAS    │
└──────┬───────┘      └──────┬───────┘
       │                     │
       ▼                     ▼
┌──────────────┐      ┌──────────────┐
│  FACTURAS    │      │  TICKETS     │
│ (+VeriFactu) │      │  (soporte)   │
└──────┬───────┘      └──────────────┘
       │
       ▼
┌──────────────┐      ┌──────────────┐
│   COBROS     │─────►│ CONTABILIDAD │
│  + SEPA      │      │  + INFORMES  │
└──────────────┘      └──────────────┘
```

### Módulos transversales

```
┌──────────────────────────────────────────────────┐
│              SUPERADMIN + CONFIG                   │
│  (multi-tenant, marca blanca, planes, fact. SaaS) │
├──────────────────────────────────────────────────┤
│              AUTOMATIZACIONES                       │
│  (workflow engine: si X → hacer Y)                │
├──────────────────────────────────────────────────┤
│              AUDITORÍA + RGPD                       │
│  (log inmutable, consentimiento, derecho olvido)   │
├──────────────────────────────────────────────────┤
│              INTEGRACIONES                          │
│  (VeriFactu AEAT, Stripe, SEPA, WhatsApp, Zapier)  │
└──────────────────────────────────────────────────┘
```

---

## 5. Esquema de Base de Datos

### 5.1 Tablas existentes (sin cambios)

```sql
-- usuarios (existente)
-- empresas (existente)
-- contactos (existente)
-- leads (existente)
-- oportunidades (existente)
-- actividades (existente)
-- notas (existente)
```

### 5.2 Nuevas tablas — Fase 1 (Núcleo Comercial)

```sql
-- ═══════════════════════════════════════
-- CATÁLOGO DE PRODUCTOS Y SERVICIOS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS productos (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  sku TEXT UNIQUE,
  tipo TEXT NOT NULL DEFAULT 'producto',       -- 'producto' | 'servicio' | 'kit'
  precioVenta REAL NOT NULL DEFAULT 0,
  precioCoste REAL DEFAULT 0,
  tipoIva TEXT NOT NULL DEFAULT 'general',     -- 'general' | 'reducido' | 'superreducido' | 'exento'
  unidadMedida TEXT DEFAULT 'unidad',          -- 'unidad' | 'hora' | 'kg' | 'm2' | 'litro'
  categoriaId TEXT,
  activo INTEGER NOT NULL DEFAULT 1,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categorias_producto (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  padreId TEXT,
  creado TEXT NOT NULL,
  FOREIGN KEY (padreId) REFERENCES categorias_producto(id)
);

CREATE TABLE IF NOT EXISTS precios_especiales (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  entidadTipo TEXT NOT NULL,                  -- 'cliente' | 'grupo'
  entidadId TEXT NOT NULL,
  precio REAL NOT NULL,
  creado TEXT NOT NULL,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

CREATE TABLE IF NOT EXISTS tarifas_volumen (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  cantidadMinima INTEGER NOT NULL,
  cantidadMaxima INTEGER,
  precioUnitario REAL NOT NULL,
  creado TEXT NOT NULL,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ═══════════════════════════════════════
-- PRESUPUESTOS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS presupuestos (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  serie TEXT DEFAULT 'PRE',
  empresaId TEXT NOT NULL,
  contactoId TEXT,
  oportunidadId TEXT,
  titulo TEXT,
  fecha TEXT NOT NULL,
  fechaValidez TEXT,
  estado TEXT NOT NULL DEFAULT 'borrador',    -- 'borrador' | 'en_revision' | 'aprobado' | 'enviado' | 'aceptado' | 'rechazado'
  moneda TEXT DEFAULT 'EUR',
  tipoCambio REAL DEFAULT 1,
  descuentoGlobal REAL DEFAULT 0,
  baseImponible REAL DEFAULT 0,
  totalIva REAL DEFAULT 0,
  total REAL DEFAULT 0,
  notasInternas TEXT,
  condiciones TEXT,
  aceptadoIp TEXT,
  aceptadoTimestamp TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (contactoId) REFERENCES contactos(id),
  FOREIGN KEY (oportunidadId) REFERENCES oportunidades(id)
);

CREATE TABLE IF NOT EXISTS lineas_presupuesto (
  id TEXT PRIMARY KEY,
  presupuestoId TEXT NOT NULL,
  productoId TEXT,
  descripcion TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 1,
  precioUnitario REAL NOT NULL DEFAULT 0,
  descuento REAL DEFAULT 0,
  tipoIva TEXT NOT NULL DEFAULT 'general',
  importe REAL NOT NULL DEFAULT 0,
  orden INTEGER DEFAULT 0,
  FOREIGN KEY (presupuestoId) REFERENCES presupuestos(id) ON DELETE CASCADE,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ═══════════════════════════════════════
-- PEDIDOS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS pedidos (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  serie TEXT DEFAULT 'PED',
  presupuestoId TEXT,
  empresaId TEXT NOT NULL,
  contactoId TEXT,
  fecha TEXT NOT NULL,
  fechaEntrega TEXT,
  estado TEXT NOT NULL DEFAULT 'pendiente',    -- 'pendiente' | 'confirmado' | 'en_proceso' | 'enviado' | 'entregado' | 'cancelado'
  baseImponible REAL DEFAULT 0,
  totalIva REAL DEFAULT 0,
  total REAL DEFAULT 0,
  notas TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (presupuestoId) REFERENCES presupuestos(id),
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (contactoId) REFERENCES contactos(id)
);

CREATE TABLE IF NOT EXISTS lineas_pedido (
  id TEXT PRIMARY KEY,
  pedidoId TEXT NOT NULL,
  productoId TEXT,
  descripcion TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 1,
  precioUnitario REAL NOT NULL DEFAULT 0,
  descuento REAL DEFAULT 0,
  tipoIva TEXT NOT NULL DEFAULT 'general',
  importe REAL NOT NULL DEFAULT 0,
  FOREIGN KEY (pedidoId) REFERENCES pedidos(id) ON DELETE CASCADE,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ═══════════════════════════════════════
-- FACTURACIÓN (VeriFactu-ready)
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS facturas (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  serie TEXT DEFAULT 'FAC',
  tipo TEXT NOT NULL DEFAULT 'ordinaria',      -- 'ordinaria' | 'rectificativa' | 'proforma' | 'recapitulativa' | 'simplificada' | 'abono'
  facturaRectificadaId TEXT,                  -- si es rectificativa, a quién rectifica
  pedidoId TEXT,
  empresaId TEXT NOT NULL,
  contactoId TEXT,
  fechaExpedicion TEXT NOT NULL,
  fechaOperacion TEXT,
  fechaVencimiento TEXT,
  estado TEXT NOT NULL DEFAULT 'borrador',    -- 'borrador' | 'emitida' | 'enviada' | 'cobrada_parcial' | 'cobrada' | 'vencida' | 'anulada'
  baseImponible REAL DEFAULT 0,
  totalIva REAL DEFAULT 0,
  totalIrpf REAL DEFAULT 0,
  total REAL DEFAULT 0,
  pendienteCobro REAL DEFAULT 0,
  moneda TEXT DEFAULT 'EUR',

  -- VeriFactu
  hashAnterior TEXT,                           -- hash SHA-256 de la factura anterior (cadena)
  hashActual TEXT,                             -- hash SHA-256 de esta factura
  huellaDigital TEXT,                          -- fingerprint VeriFactu
  codigoQr TEXT,                               -- datos QR AEAT
  verifactuEnviado INTEGER DEFAULT 0,          -- 0=no enviado, 1=enviado, 2=error
  verifactuFechaEnvio TEXT,
  verifactuRespuesta TEXT,

  -- SII
  siiEstado TEXT,                              -- 'pendiente' | 'enviado' | 'aceptado' | 'rechazado'
  siiRespuesta TEXT,

  notas TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (facturaRectificadaId) REFERENCES facturas(id),
  FOREIGN KEY (pedidoId) REFERENCES pedidos(id),
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (contactoId) REFERENCES contactos(id)
);

CREATE TABLE IF NOT EXISTS lineas_factura (
  id TEXT PRIMARY KEY,
  facturaId TEXT NOT NULL,
  productoId TEXT,
  descripcion TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 1,
  precioUnitario REAL NOT NULL DEFAULT 0,
  descuento REAL DEFAULT 0,
  tipoIva TEXT NOT NULL DEFAULT 'general',
  cuotaIva REAL DEFAULT 0,
  importe REAL NOT NULL DEFAULT 0,
  FOREIGN KEY (facturaId) REFERENCES facturas(id) ON DELETE CASCADE,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ═══════════════════════════════════════
-- COBROS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS cobros (
  id TEXT PRIMARY KEY,
  facturaId TEXT NOT NULL,
  fecha TEXT NOT NULL,
  importe REAL NOT NULL,
  metodoPago TEXT NOT NULL DEFAULT 'transferencia',  -- 'transferencia' | 'tarjeta' | 'efectivo' | 'domiciliacion' | 'paypal' | 'stripe'
  referencia TEXT,
  estado TEXT NOT NULL DEFAULT 'registrado',         -- 'registrado' | 'conciliado' | 'rechazado'
  conciliado INTEGER DEFAULT 0,
  extractoId TEXT,
  sepaXml TEXT,
  creado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (facturaId) REFERENCES facturas(id)
);
```

### 5.3 Nuevas tablas — Fase 2 (Operaciones)

```sql
-- ═══════════════════════════════════════
-- PROVEEDORES
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS proveedores (
  id TEXT PRIMARY KEY,
  cif TEXT UNIQUE,
  nombre TEXT NOT NULL,
  email TEXT,
  telefono TEXT,
  web TEXT,
  direccion TEXT,
  ciudad TEXT,
  provincia TEXT,
  codigoPostal TEXT,
  pais TEXT DEFAULT 'España',
  contactoNombre TEXT,
  contactoEmail TEXT,
  contactoTelefono TEXT,
  plazoPago INTEGER DEFAULT 30,                -- días
  notas TEXT,
  activo INTEGER DEFAULT 1,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos_compra (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  serie TEXT DEFAULT 'PC',
  proveedorId TEXT NOT NULL,
  fecha TEXT NOT NULL,
  fechaEntrega TEXT,
  estado TEXT NOT NULL DEFAULT 'borrador',      -- 'borrador' | 'enviado' | 'recibido_parcial' | 'recibido_total' | 'cancelado'
  baseImponible REAL DEFAULT 0,
  totalIva REAL DEFAULT 0,
  total REAL DEFAULT 0,
  notas TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (proveedorId) REFERENCES proveedores(id)
);

CREATE TABLE IF NOT EXISTS lineas_pedido_compra (
  id TEXT PRIMARY KEY,
  pedidoCompraId TEXT NOT NULL,
  productoId TEXT,
  descripcion TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 1,
  precioUnitario REAL NOT NULL DEFAULT 0,
  descuento REAL DEFAULT 0,
  tipoIva TEXT NOT NULL DEFAULT 'general',
  importe REAL NOT NULL DEFAULT 0,
  cantidadRecibida REAL DEFAULT 0,
  FOREIGN KEY (pedidoCompraId) REFERENCES pedidos_compra(id) ON DELETE CASCADE,
  FOREIGN KEY (productoId) REFERENCES productos(id)
);

-- ═══════════════════════════════════════
-- INVENTARIO / ALMACÉN
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS almacenes (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  direccion TEXT,
  ciudad TEXT,
  activo INTEGER DEFAULT 1,
  creado TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stock (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  almacenId TEXT NOT NULL,
  cantidad REAL NOT NULL DEFAULT 0,
  stockMinimo REAL DEFAULT 0,
  stockMaximo REAL,
  ubicacion TEXT,
  FOREIGN KEY (productoId) REFERENCES productos(id),
  FOREIGN KEY (almacenId) REFERENCES almacenes(id),
  UNIQUE(productoId, almacenId)
);

CREATE TABLE IF NOT EXISTS movimientos_stock (
  id TEXT PRIMARY KEY,
  productoId TEXT NOT NULL,
  almacenId TEXT NOT NULL,
  tipo TEXT NOT NULL,                          -- 'entrada_compra' | 'salida_venta' | 'ajuste' | 'traslado' | 'merma' | 'devolucion_cliente' | 'devolucion_proveedor'
  cantidad REAL NOT NULL,
  stockAnterior REAL NOT NULL,
  stockPosterior REAL NOT NULL,
  referenciaTipo TEXT,                         -- 'pedido' | 'factura' | 'ajuste' | 'traslado'
  referenciaId TEXT,
  lote TEXT,
  notas TEXT,
  creado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (productoId) REFERENCES productos(id),
  FOREIGN KEY (almacenId) REFERENCES almacenes(id)
);

-- ═══════════════════════════════════════
-- PROYECTOS Y TAREAS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS proyectos (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  empresaId TEXT,
  oportunidadId TEXT,
  presupuestoId TEXT,
  responsableId TEXT,
  fechaInicio TEXT,
  fechaFin TEXT,
  presupuestoReal REAL DEFAULT 0,
  costeReal REAL DEFAULT 0,
  estado TEXT NOT NULL DEFAULT 'planificado',   -- 'planificado' | 'en_curso' | 'en_revision' | 'completado' | 'archivado'
  prioridad TEXT DEFAULT 'media',              -- 'baja' | 'media' | 'alta' | 'urgente'
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (oportunidadId) REFERENCES oportunidades(id),
  FOREIGN KEY (presupuestoId) REFERENCES presupuestos(id)
);

CREATE TABLE IF NOT EXISTS tareas (
  id TEXT PRIMARY KEY,
  proyectoId TEXT,
  titulo TEXT NOT NULL,
  descripcion TEXT,
  prioridad TEXT DEFAULT 'media',
  estado TEXT NOT NULL DEFAULT 'pendiente',    -- 'pendiente' | 'en_curso' | 'completada' | 'cancelada'
  responsableId TEXT,
  fechaLimite TEXT,
  estimacionHoras REAL,
  tiempoReal REAL DEFAULT 0,
  padreId TEXT,                                -- subtarea de
  orden INTEGER DEFAULT 0,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (proyectoId) REFERENCES proyectos(id),
  FOREIGN KEY (padreId) REFERENCES tareas(id)
);

CREATE TABLE IF NOT EXISTS registros_tiempo (
  id TEXT PRIMARY KEY,
  tareaId TEXT NOT NULL,
  usuarioId TEXT NOT NULL,
  fecha TEXT NOT NULL,
  horas REAL NOT NULL,
  descripcion TEXT,
  facturable INTEGER DEFAULT 1,
  facturado INTEGER DEFAULT 0,
  creado TEXT NOT NULL,
  FOREIGN KEY (tareaId) REFERENCES tareas(id)
);
```

### 5.4 Nuevas tablas — Fase 3 (Servicio)

```sql
-- ═══════════════════════════════════════
-- TICKETS / SOPORTE
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS tickets (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  empresaId TEXT,
  contactoId TEXT,
  proyectoId TEXT,
  asunto TEXT NOT NULL,
  descripcion TEXT,
  prioridad TEXT NOT NULL DEFAULT 'media',     -- 'baja' | 'media' | 'alta' | 'urgente'
  estado TEXT NOT NULL DEFAULT 'abierto',      -- 'abierto' | 'en_curso' | 'pendiente_cliente' | 'resuelto' | 'cerrado'
  categoria TEXT,
  asignadoA TEXT,
  slaHoras INTEGER,
  origen TEXT DEFAULT 'manual',                -- 'manual' | 'email' | 'portal' | 'api'
  fechaLimiteSla TEXT,
  satisfaccion INTEGER,                        -- 1-5
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  cerradoPor TEXT,
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (contactoId) REFERENCES contactos(id),
  FOREIGN KEY (proyectoId) REFERENCES proyectos(id)
);

CREATE TABLE IF NOT EXISTS mensajes_ticket (
  id TEXT PRIMARY KEY,
  ticketId TEXT NOT NULL,
  tipo TEXT NOT NULL DEFAULT 'respuesta',      -- 'respuesta' | 'nota_interna' | 'cambio_estado'
  contenido TEXT NOT NULL,
  esInterno INTEGER DEFAULT 0,
  adjuntos TEXT,
  creado TEXT NOT NULL,
  creadoPor TEXT,
  FOREIGN KEY (ticketId) REFERENCES tickets(id) ON DELETE CASCADE
);

-- ═══════════════════════════════════════
-- RRHH
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS empleados (
  id TEXT PRIMARY KEY,
  usuarioId TEXT,
  nombre TEXT NOT NULL,
  email TEXT,
  telefono TEXT,
  dni TEXT UNIQUE,
  puesto TEXT,
  departamento TEXT,
  responsableId TEXT,
  fechaAlta TEXT,
  fechaBaja TEXT,
  tipoContrato TEXT,                           -- 'indefinido' | 'temporal' | 'autonomo' | 'practicas'
  salarioBruto REAL DEFAULT 0,
  activo INTEGER DEFAULT 1,
  notas TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  FOREIGN KEY (usuarioId) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS ausencias (
  id TEXT PRIMARY KEY,
  empleadoId TEXT NOT NULL,
  tipo TEXT NOT NULL,                          -- 'vacaciones' | 'baja' | 'permiso' | 'formacion'
  fechaInicio TEXT NOT NULL,
  fechaFin TEXT,
  estado TEXT NOT NULL DEFAULT 'pendiente',    -- 'pendiente' | 'aprobado' | 'rechazado'
  aprobadoPor TEXT,
  notas TEXT,
  creado TEXT NOT NULL,
  FOREIGN KEY (empleadoId) REFERENCES empleados(id)
);

-- ═══════════════════════════════════════
-- CONTRATOS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS contratos (
  id TEXT PRIMARY KEY,
  numero TEXT NOT NULL,
  empresaId TEXT NOT NULL,
  contactoId TEXT,
  presupuestoId TEXT,
  titulo TEXT NOT NULL,
  tipo TEXT NOT NULL DEFAULT 'servicio',       -- 'servicio' | 'producto' | 'arrendamiento' | 'nda' | 'otro'
  fechaInicio TEXT NOT NULL,
  fechaFin TEXT,
  fechaFirma TEXT,
  estado TEXT NOT NULL DEFAULT 'borrador',     -- 'borrador' | 'pendiente_firma' | 'activo' | 'expirado' | 'cancelado' | 'renovado'
  importe REAL DEFAULT 0,
  periodicidad TEXT,                           -- 'unico' | 'mensual' | 'trimestral' | 'anual'
  clausulas TEXT,
  documentoAdjunto TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL,
  FOREIGN KEY (empresaId) REFERENCES empresas(id),
  FOREIGN KEY (contactoId) REFERENCES contactos(id),
  FOREIGN KEY (presupuestoId) REFERENCES presupuestos(id)
);
```

### 5.5 Nuevas tablas — Fase 4 (Enterprise)

```sql
-- ═══════════════════════════════════════
-- CONFIGURACIÓN MULTI-TENANT Y MARCA BLANCA
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  cif TEXT,
  dominio TEXT UNIQUE,
  logo TEXT,
  colores TEXT,                                 -- JSON: {primario, secundario, fondo}
  modulosActivos TEXT,                          -- JSON: ["crm", "facturacion", "proyectos", ...]
  plan TEXT DEFAULT 'basico',                   -- 'basico' | 'profesional' | 'enterprise'
  activo INTEGER DEFAULT 1,
  fechaAlta TEXT NOT NULL,
  fechaRenovacion TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL
);

-- ═══════════════════════════════════════
-- AUDITORÍA (log inmutable)
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS auditoria (
  id TEXT PRIMARY KEY,
  entidadTipo TEXT NOT NULL,
  entidadId TEXT NOT NULL,
  accion TEXT NOT NULL,                        -- 'crear' | 'actualizar' | 'eliminar' | 'anular' | 'enviar'
  usuarioId TEXT,
  datosAnteriores TEXT,                         -- JSON del estado anterior
  datosNuevos TEXT,                             -- JSON del estado nuevo
  ip TEXT,
  userAgent TEXT,
  creado TEXT NOT NULL
);

-- ═══════════════════════════════════════
-- AUTOMATIZACIONES (Workflow Engine)
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS automatizaciones (
  id TEXT PRIMARY KEY,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  activo INTEGER DEFAULT 1,
  disparadorTipo TEXT NOT NULL,                -- 'creacion' | 'cambio_estado' | 'fecha' | 'webhook' | 'email'
  disparadorConfig TEXT NOT NULL,              -- JSON con configuración del disparador
  accionTipo TEXT NOT NULL,                    -- 'email' | 'webhook' | 'tarea' | 'cambio_estado' | 'notificacion'
  accionConfig TEXT NOT NULL,                  -- JSON con configuración de la acción
  ejecuciones INTEGER DEFAULT 0,
  ultimaEjecucion TEXT,
  creado TEXT NOT NULL,
  actualizado TEXT NOT NULL
);

-- ═══════════════════════════════════════
-- CAMPOS PERSONALIZADOS
-- ═══════════════════════════════════════

CREATE TABLE IF NOT EXISTS campos_personalizados (
  id TEXT PRIMARY KEY,
  entidadTipo TEXT NOT NULL,                   -- 'empresa' | 'contacto' | 'lead' | 'producto' | 'factura'
  nombre TEXT NOT NULL,
  etiqueta TEXT NOT NULL,
  tipo TEXT NOT NULL,                          -- 'texto' | 'numero' | 'fecha' | 'desplegable' | 'booleano'
  opciones TEXT,                               -- JSON array para desplegable
  requerido INTEGER DEFAULT 0,
  orden INTEGER DEFAULT 0,
  activo INTEGER DEFAULT 1,
  creado TEXT NOT NULL
);
```

---

## 6. API por Módulo

### 6.1 Rutas API completas

Cada módulo sigue el patrón REST estándar de AdelaCRM:

| Módulo | Ruta base | Endpoints |
|--------|-----------|-----------|
| Productos | `/api/productos` | GET, GET/:id, POST, PUT/:id, DELETE/:id |
| Categorías | `/api/categorias-producto` | GET, POST, PUT/:id, DELETE/:id |
| Presupuestos | `/api/presupuestos` | GET, GET/:id, POST, PUT/:id, DELETE/:id |
| Líneas Presupuesto | `/api/presupuestos/:id/lineas` | GET, POST, PUT/:lineaId, DELETE/:lineaId |
| Pedidos | `/api/pedidos` | GET, GET/:id, POST, PUT/:id, DELETE/:id |
| Facturas | `/api/facturas` | GET, GET/:id, POST, PUT/:id, DELETE/:id |
| Facturas (VeriFactu) | `/api/facturas/:id/verifactu` | POST (enviar a AEAT) |
| Cobros | `/api/cobros` | GET, POST, PUT/:id |
| Proveedores | `/api/proveedores` | GET, GET/:id, POST, PUT/:id, DELETE/:id |
| Pedidos Compra | `/api/pedidos-compra` | GET, GET/:id, POST, PUT/:id |
| Stock | `/api/stock` | GET, POST (ajuste) |
| Movimientos Stock | `/api/stock/movimientos` | GET |
| Proyectos | `/api/proyectos` | GET, GET/:id, POST, PUT/:id |
| Tareas | `/api/tareas` | GET, POST, PUT/:id |
| Tiempo | `/api/tiempo` | GET, POST |
| Tickets | `/api/tickets` | GET, GET/:id, POST, PUT/:id |
| Contratos | `/api/contratos` | GET, GET/:id, POST, PUT/:id |
| Empleados | `/api/empleados` | GET, GET/:id, POST, PUT/:id |
| Ausencias | `/api/ausencias` | GET, POST, PUT/:id |
| Automatizaciones | `/api/automatizaciones` | GET, POST, PUT/:id |
| Auditoría | `/api/auditoria` | GET |
| Configuración | `/api/config` | GET, PUT |

### 6.2 Convención de respuestas

```typescript
// Éxito
{ [entidad]: { ...datos } }             // GET /:id
{ [entidadPlural]: [{ ... }] }          // GET /
{ [entidad]: { ... } }                  // POST
{ [entidad]: { ... } }                  // PUT
{ mensaje: 'Entidad eliminada' }       // DELETE

// Error
{ error: 'Mensaje descriptivo' }
{ error: 'Mensaje', campo: 'nombre' }  // Error de validación por campo
```

---

## 7. Flujo de Datos entre Módulos

### Flujo comercial completo

```
1. CAPTACIÓN
   Lead (web/email/manual)
     → Actividad de seguimiento
     → Oportunidad con valor €

2. COTIZACIÓN
   Oportunidad → Productos del catálogo
     → Presupuesto con líneas e IVA
     → Envío al cliente (email + portal)
     → Firma electrónica / Aceptación

3. VENTA
   Presupuesto aceptado → Pedido
     → Pedido → Proyecto (si aplica)
     → Pedido → Tareas de preparación

4. FACTURACIÓN
   Pedido confirmado → Factura
     → Hash VeriFactu + QR
     → Envío SII (AEAT)
     → Envío al cliente

5. COBRO
   Factura emitida → Registro de cobro
     → Conciliación bancaria
     → Factura marcada como cobrada
     → Asiento contable

6. POST-VENTA
   Cliente → Ticket de soporte
     → Proyecto de post-venta
     → Contrato de mantenimiento
     → Factura recurrente
```

### Eventos del sistema (para automatizaciones)

| Evento | Disparador | Acciones típicas |
|--------|-----------|------------------|
| Lead creado | `lead.created` | Notificar comercial, asignar lead |
| Lead sin actividad 7 días | `lead.stale` | Email recordatorio, cambiar estado |
| Presupuesto aceptado | `presupuesto.accepted` | Crear pedido, notificar almacén |
| Factura vencida | `factura.overdue` | Email aviso, recargo, enviar a gestoría |
| Ticket urgente | `ticket.urgent` | Notificar equipo, crear tarea urgente |
| Stock bajo mínimo | `stock.low` | Crear pedido de compra automático |

---

## 8. Seguridad y Cumplimiento

### 8.1 Roles del sistema

| Rol | Acceso |
|-----|--------|
| `superadmin` | Todas las instancias, configuración global |
| `admin` | Configuración completa de su instancia |
| `gestor` | Acceso completo a módulos asignados |
| `comercial` | CRM, presupuestos, oportunidades propias |
| `tecnico` | Proyectos, tareas, tickets asignados |
| `contable` | Facturación, cobros, contabilidad |
| `solo_lectura` | Consulta sin modificar |
| `personalizado` | Permisos módulo a módulo |

### 8.2 VeriFactu (AEAT)

Cada factura emitida debe:
1. Calcular hash SHA-256 encadenado (incluye hash de factura anterior)
2. Generar huella digital (fingerprint)
3. Incrustar código QR con datos AEAT
4. (Opcional) Envío automático a AEAT vía API
5. Registrar el registro como inmutable

### 8.3 RGPD

- Consentimiento explícito por contacto (timestamp + texto)
- Exportación de datos personales con un clic
- Derecho al olvido: anonimización preservando histórico agregado
- Log de auditoría con IP y user-agent
- Notificación de brechas de seguridad

### 8.4 Buenas prácticas de desarrollo

- JWT_SECRET compartido desde `config.ts` (única fuente de verdad)
- PIN/contraseñas con bcrypt, nunca texto plano
- SQL parametrizado (sin concatenación)
- Sanitize de campos sensibles en respuestas API
- Admin PIN desde variable de entorno, nunca hardcodeado

---

## 9. Plan de Despliegue

### 9.1 Estructura de archivos final

```
AdelaTest01/
├── src/
│   ├── server.ts              # Express + montaje de rutas
│   ├── db.ts                  # SQLite + TODAS las tablas
│   ├── types.ts               # Interfaces de TODAS las entidades
│   ├── config.ts              # Configuración compartida
│   ├── middleware/
│   │   └── auth.ts            # JWT + roles
│   └── routes/
│       ├── auth.ts            # Login + perfil
│       ├── usuarios.ts        # CRUD usuarios
│       ├── empresas.ts        # CRUD empresas
│       ├── contactos.ts       # CRUD contactos
│       ├── leads.ts           # Pipeline + stats
│       ├── oportunidades.ts   # CRUD oportunidades
│       ├── actividades.ts     # Calendario
│       ├── notas.ts           # Notas polimórficas
│       ├── productos.ts       # Catálogo + categorías
│       ├── presupuestos.ts    # Presupuestos + aprobación
│       ├── pedidos.ts         # Pedidos de venta
│       ├── facturas.ts        # Facturación + VeriFactu
│       ├── cobros.ts          # Cobros + SEPA
│       ├── proveedores.ts     # Proveedores
│       ├── pedidosCompra.ts   # Pedidos de compra
│       ├── stock.ts           # Inventario + movimientos
│       ├── proyectos.ts       # Proyectos + tareas
│       ├── tareas.ts          # Tareas + time tracking
│       ├── tickets.ts         # Soporte
│       ├── contratos.ts       # Contratos
│       ├── empleados.ts       # RRHH
│       └── automatizaciones.ts # Workflow engine
├── public/
│   ├── index.html             # SPA principal
│   ├── css/crm.css            # Aurora + Liquid Glass
│   └── js/crm.js              # Lógica frontend
├── docs/
│   ├── PLAN-CRM-ERP-TOTAL.md  # Este documento
│   ├── API.md                 # Documentación de API
│   └── ARQUITECTURA.md        # Arquitectura del sistema
├── data/
│   └── datos.db               # SQLite (auto-generado)
├── tests/                     # Tests por módulo
├── package.json
├── tsconfig.json
└── Dockerfile
```

### 9.2 Priorización de implementación

El orden de implementación sigue el flujo de datos natural:

1. **Productos** (base del catálogo)
2. **Presupuestos** (conversión de oportunidades)
3. **Pedidos** (de presupuesto aceptado)
4. **Facturación** (de pedido confirmado)
5. **Cobros** (de factura emitida)
6. **VeriFactu** (cumplimiento AEAT)
7. **Proveedores + Compras** (operaciones)
8. **Inventario** (gestión de stock)
9. **Proyectos + Tareas** (ejecución)
10. **Tickets** (soporte post-venta)
11. **Contratos** (acuerdos recurrentes)
12. **RRHH** (gestión interna)
13. **Contabilidad** (informes financieros)
14. **Automatizaciones** (workflow engine)
15. **SuperAdmin + Config** (multi-tenant)

---

*Este plan es un documento vivo. Se actualiza con cada fase completada.*

---

**Hecho con ❤️ por David Antizar**
