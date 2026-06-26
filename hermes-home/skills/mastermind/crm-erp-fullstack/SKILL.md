---
name: crm-erp-fullstack
version: "1.0.0"
description: Patrón completo para construir un CRM+ERP total con backend Express/TypeScript, SQLite, multi-tenant, marca blanca, VeriFactu (AEAT) y cumplimiento fiscal español.
tags: [crm, erp, facturacion, verifactu, multi-tenant, marca-blanca, aeat]
triggers: [crm, erp, sistema de gestión, facturación, presupuestos, clientes, proveedores, inventario, multi-tenant, marca blanca, verifactu]
references:
  - references/plan-crm-erp-total.md — Plan maestro completo con 26 secciones, arquitectura, esquema BD, API y roadmap por fases
  - references/tanda-implementacion.md — Patrón de implementación por tandas con pasos detallados, pitfalls y agrupación de módulos
  - references/stock-adjustment-pattern.md — Patrón de ajuste de stock con auto-creación y trazabilidad completa
  - references/compilation-troubleshooting.md — Guía completa de resolución de errores TypeScript: export block faltante, alineación types.ts↔db.ts, y tabla de conversión de campos v2
  - references/modulos-avanzados-spec-26.md — Especificación completa de 26 módulos con requisitos detallados
---

# CRM + ERP FullStack

Patrón para construir un **CRM+ERP total** completo: desde la captación de un lead hasta el cobro final de una factura, pasando por presupuestos, proyectos, RRHH, inventario y contabilidad. Cumplimiento AEAT (VeriFactu, SII) y RGPD.

## Cuándo usarlo

- El usuario dice "construye un CRM completo"
- El usuario dice "necesito facturación con VeriFactu"
- El usuario tiene un CRM básico y quiere añadir ERP (facturas, cobros, compras, inventario)
- El usuario quiere un sistema multi-tenant con marca blanca
- El usuario proporciona una especificación detallada de 20+ secciones

## Stack base

| Capa | Tecnología |
|------|-----------|
| Backend | Node.js + Express + TypeScript (ESM) |
| Base de datos | SQLite (sql.js, persistente en archivo) |
| Auth | JWT + bcrypt (PIN/email) |
| Frontend | SPA vanilla JS + Aurora CSS (Liquid Glass) |
| Cumplimiento | VeriFactu (hash SHA-256 + QR + cadena) |

## Arquitectura de módulos (orden de implementación)

### Fase 1 — Núcleo Comercial
```
1. Productos/Servicios   ← Base del catálogo (SKU, IVA, categorías, tarifas)
2. Presupuestos          ← Cotización con líneas, aprobación, firma
3. Facturación           ← Ordinaria, rectificativa, recurrente, proforma
4. Cobros                ← Registro, SEPA, conciliación bancaria
```

### Fase 2 — Operaciones
```
5. Proveedores           ← Fichas, pedidos de compra, plazos de pago
6. Inventario/Almacén    ← Stock, movimientos, alertas, traslados
7. Proyectos + Tareas    ← Hitos, time tracking, Kanban/Gantt
8. VeriFactu (AEAT)      ← Hash encadenado, QR, envío SII
```

### Fase 3 — Servicio y Personas
```
9. Tickets/Soporte       ← SLA, portal cliente, respuestas predefinidas
10. RRHH                 ← Empleados, ausencias, fichaje, contratos
11. Automatizaciones     ← Workflow engine: si X → hacer Y
12. Contratos            ← Acuerdos recurrentes, renovaciones
```

### Fase 4 — Enterprise
```
13. Contabilidad         ← Libros registro, informes, IVA, IRPF
14. Marketing            ← Campañas, segmentación, email
15. SuperAdmin           ← Multi-tenant, planes, facturación SaaS
16. Config empresa       ← Marca blanca, módulos activos, personalización
```

## Mapa de dependencias entre módulos

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

## Flujo comercial completo

```
1. LEAD (web/email) → Actividad de seguimiento → Oportunidad (valor €)
2. OPORTUNIDAD → Productos del catálogo → Presupuesto (líneas + IVA)
3. PRESUPUESTO aceptado → Pedido → Proyecto (si aplica)
4. PEDIDO confirmado → Factura (hash VeriFactu + QR → AEAT)
5. FACTURA emitida → Cobro → Conciliación bancaria → Contabilidad
6. CLIENTE → Ticket soporte → Contrato mantenimiento → Factura recurrente
```

## Patrón de base de datos (SQLite con sql.js)

Cada módulo sigue este patrón en db.ts:

```typescript
// 1. Tabla SQL en el bloque CREATE TABLE de initDatabase()
db.run(`
  CREATE TABLE IF NOT EXISTS mi_entidad (
    id TEXT PRIMARY KEY,
    campo1 TEXT NOT NULL,
    campo2 REAL DEFAULT 0,
    creado TEXT NOT NULL,
    actualizado TEXT NOT NULL
  );
`)

// 2. Funciones CRUD siguiendo el patrón establecido:
async function obtenerEntidades(): Promise<Entidad[]> {
  await initDatabase()
  return all<Entidad>('SELECT * FROM mi_entidad ORDER BY creado DESC')
}

async function crearEntidad(data: Partial<Entidad>): Promise<Entidad> {
  await initDatabase()
  const id = `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  const ahora = new Date().toISOString()
  run('INSERT INTO mi_entidad (id, campo1, ...) VALUES (?, ?, ...)',
    [id, data.campo1 || null, ahora, ahora])
  return { ...data, id, creado: ahora, actualizado: ahora } as Entidad
}
```

### Reglas de naming para IDs
- Empresas: `emp-{timestamp}-{random}`
- Contactos: `con-{timestamp}-{random}`
- Leads: `lead-{timestamp}-{random}`
- Oportunidades: `opp-{timestamp}-{random}`
- Actividades: `act-{timestamp}-{random}`
- Notas: `note-{timestamp}-{random}`
- Productos: `prod-{timestamp}-{random}`
- Presupuestos: `pre-{timestamp}-{random}`
- Facturas: `fac-{timestamp}-{random}`
- Cobros: `cob-{timestamp}-{random}`
- Proveedores: `prov-{timestamp}-{random}`
- Pedidos compra: `pc-{timestamp}-{random}`
- Proyectos: `proy-{timestamp}-{random}`
- Tareas: `tar-{timestamp}-{random}`
- Tickets: `tick-{timestamp}-{random}`
- Contratos: `cont-{timestamp}-{random}`
- Empleados: `emp-{timestamp}-{random}`

### Números correlativos
```typescript
async function siguienteNumero(serie: string, tabla: string): Promise<string> {
  const last = get<any>(`SELECT MAX(numero) as max FROM ${tabla} WHERE serie = ?`, [serie])
  const nextNum = (parseInt(last?.max?.replace(serie, '') || '0') + 1).toString().padStart(6, '0')
  return `${serie}${nextNum}`
}
```

## Patrón VeriFactu (AEAT)

### Hash encadenado SHA-256

```typescript
import crypto from 'node:crypto'

function calcularHashFactura(factura: Factura, hashAnterior: string | null): string {
  const data = JSON.stringify({
    numero: factura.numero,
    fecha: factura.fechaExpedicion,
    emisor: factura.empresaId,
    base: factura.baseImponible,
    iva: factura.totalIva,
    total: factura.total,
    hashAnterior // ← el hash de la factura anterior forma la cadena
  })
  return crypto.createHash('sha256').update(data).digest('hex')
}
```

### Código QR AEAT

```typescript
function generarQRData(factura: Factura): string {
  // Formato requerido por AEAT para VeriFactu
  return JSON.stringify({
    version: '1.0',
    nif: factura.empresaId,
    numSerie: `${factura.serie}${factura.numero}`,
    fecha: factura.fechaExpedicion,
    base: factura.baseImponible,
    iva: factura.totalIva,
    total: factura.total,
    huella: factura.hashActual
  })
}
```

## Patrón de rutas Express

Cada módulo expone REST estándar:

```typescript
import { Router } from 'express'
import { dbFunctions } from '../db.js'
import type { AuthRequest } from '../middleware/auth.js'

const router = Router()

router.get('/', async (req: AuthRequest, res) => {
  try {
    const items = await dbFunctions.obtener()
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener' })
  }
})

router.get('/:id', async (req, res) => {
  try {
    const item = await dbFunctions.obtenerPorId(req.params.id)
    if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error' })
  }
})

router.post('/', async (req: AuthRequest, res) => {
  try {
    const item = await dbFunctions.crear({ ...req.body, creadoPor: req.usuario?.id })
    res.status(201).json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al crear' })
  }
})

router.put('/:id', async (req: AuthRequest, res) => {
  try {
    const item = await dbFunctions.actualizar(req.params.id, req.body)
    if (!item) { res.status(404).json({ error: 'No encontrado' }); return }
    res.json({ item })
  } catch (error) {
    res.status(500).json({ error: 'Error al actualizar' })
  }
})

router.delete('/:id', async (req: AuthRequest, res) => {
  try {
    await dbFunctions.eliminar(req.params.id)
    res.json({ mensaje: 'Eliminado correctamente' })
  } catch (error) {
    res.status(500).json({ error: 'Error al eliminar' })
  }
})

export default router
```

### Registro en server.ts

```typescript
import entidadesRouter from './routes/entidades.js'

// En server.ts:
app.use('/api/entidades', requerirAuth, entidadesRouter)
```

## Roles del sistema

| Rol | Acceso |
|-----|--------|
| `superadmin` | Todas las instancias, gestión global |
| `admin` | Configuración completa de su instancia |
| `gestor` | Acceso completo a módulos asignados |
| `comercial` | CRM, presupuestos, oportunidades propias |
| `tecnico` | Proyectos, tareas, tickets asignados |
| `contable` | Facturación, cobros, contabilidad |
| `solo_lectura` | Consulta sin modificar |

## Esquema de tipos (types.ts)

Cada entidad debe tener su interfaz TypeScript completa con:
- **Tipos estrictos** para estados (union types: `'borrador' | 'emitida' | 'cobrada'`)
- **Campos opcionales** con `?` para los que pueden ser null
- **Campos de auditoría**: `creado: string`, `actualizado: string`, `creadoPor?: string`
- **IDs descriptivos**: `empresaId`, `productoId`, `facturaId`

## Cumplimiento RGPD

- Consentimiento explícito por contacto (timestamp + texto del consentimiento)
- Exportación de datos personales en un clic
- Derecho al olvido: anonimización preservando histórico agregado
- Log de auditoría con IP y user-agent
- Notificación de brechas de seguridad

## Conexiones flexibles entre entidades

Para que cada usuario pueda personalizar las relaciones entre entidades del sistema, usar el patrón de **conexiones flexibles** (ver `references/conexiones-flexibles-pattern.md`):

- Tabla `tipos_conexion` — catálogo configurable (usuario crea sus propios tipos)
- Tabla `entidades_conectadas` — vincula cualquier entidad con cualquier otra
- Endpoint `/api/conexiones/grafo/:tipo/:id` — explora relaciones N niveles
- Cada tipo tiene: nombre, color, icono, restricciones de entidad, bidireccionalidad

Esto reemplaza la necesidad de crear tablas intermedias por cada combinación (empresa_contacto, empleado_proyecto, etc.) y permite al usuario definir sus propias relaciones según su negocio.

## Marca blanca (multi-tenant)

Cada instancia de empresa puede tener:
- **Logo, colores y favicon** propios
- **Dominio personalizado** (app.miempresa.com)
- **Módulos activables** por plan (básico, profesional, enterprise)
- **Sin referencias al software base** en ningún punto de la interfaz

## Estilo de implementación: por tandas sin pausa (MODO SIGUE)

**⚠️ REGLA DE ORO: El usuario odia las pausas entre tandas. "SIGUE" significa SIGUE.**

El usuario prefiere este flujo de trabajo para proyectos grandes:

1. **Dividir en tandas lógicas** (ej: Tanda 1 = Productos+Presupuestos, Tanda 2 = Facturación+VeriFactu+Cobros, etc.)
2. **Implementar una tanda completa** — types → schema SQL → CRUD → rutas → server → compilar
3. **MOSTRAR resultados** inmediatamente después de cada tanda — qué archivos se crearon/modificaron, qué endpoints están disponibles
4. **Pasar a la siguiente tanda SIN PAUSA** — NO esperar confirmación explícita a menos que haya errores de compilación. Si el usuario pregunta "Cómo vas?" o "Qué queda?", responder RÁPIDO con un breakdown breve y proseguir inmediatamente.
5. **NO parar entre tandas** — el usuario interpreta las pausas como "se ha quedado bloqueado" o "está esperando". La frase "Sigue" significa "continúa sin preguntar".

### Paralelización: delegate_task para módulos pesados

Cuando un módulo tiene 5+ tablas o requiere 150+ líneas de rutas, usar `delegate_task` para paralelizar:

```text
TÚ (orquestador)                              SUBAGENTE
    │                                              │
    ├─ Añadir types a types.ts ────────────────────│
    ├─ Añadir tablas + CRUD a db.ts ───────────────│
    ├─ Actualizar export block ────────────────────│
    │                                              │
    ├─ DELEGAR creación de route file ─────────────►  Crea routes/<modulo>.ts
    │  (context: types, funciones disponibles)        con 5+ endpoints
    │                                              │
    │  ── Mientras tanto ──                        │  (trabaja en paralelo)
    │  Preparar server.ts (import + mount)          │
    │                                              │
    ├─ Recibir resumen del subagente ──────────────◄  "route file creado"
    ├─ Verificar el archivo creado ─────────────────│
    └─ Compilar y montar ──────────────────────────│
```

**Cuándo delegar:**
- Módulos con >6 tablas (Contabilidad, Marketing, SuperAdmin)
- Módulos con lógica compleja (state machines, cálculos)
- Cuando quieras liberar tu contexto para seguir con la siguiente tanda

**Qué delegar EXACTAMENTE:**
- Solo la creación del archivo de rutas (`src/routes/<modulo>.ts`)
- NO delegar db.ts, types.ts ni server.ts (son muy propensos a conflictos de merge)
- Incluir en el `context` del subagente: los nombres exactos de funciones y sus firmas, las interfaces de types.ts, y el patrón de rutas que debe seguir

**Verificación post-delegación:**
- Siempre verificar que el archivo existe y tiene los endpoints esperados
- Verificar que los imports en el route file apuntan a las funciones correctas de db.ts
- Compilar después de montar en server.ts

### Patrón de recuperación post-truncamiento de db.ts

**⚠️ PITFALL CRÍTICO: `read_file()` dentro de `execute_code` solo devuelve 500 líneas por defecto.**

Si se usa `execute_code` con `read_file()` y luego `write_file()`, el archivo se trunca a 500 líneas — pérdida total del trabajo de sesiones anteriores.

**Flujo de recuperación:**

1. **NO tocar más el archivo** — el daño ya está hecho
2. **Recuperar del commit más reciente:**
   ```bash
   git restore src/db.ts
   # o: git checkout HEAD -- src/db.ts
   ```
3. **Auditar qué se perdió:** examinar `src/server.ts` para ver qué rutas están montadas, y `src/types.ts` para ver qué interfaces existen. Los imports en server.ts son la especificación de lo que db.ts debe tener.
4. **Reconstruir en UNA SOLA tanda:** añadir todas las tablas faltantes + funciones CRUD + exports de una sola vez, no tanda por tanda.
5. **Reconstruir rutas:** verificar que cada ruta montada en server.ts tiene su archivo en `src/routes/`. Si se perdió, recrear.
6. **Hacer commit inmediatamente** después de la reconstrucción para tener punto de restauración.

**Prevención:**
- Para ediciones localizadas en db.ts, usar `patch()` (agente principal) o `terminal('sed')` con mucho cuidado
- Si necesitas editar desde execute_code, usar `terminal('cat path/to/db.ts')` en vez de `read_file()`
- Hacer `git add . && git commit -m "checkpoint"` CADA VEZ que se complete una tanda funcional

## Organización del código "por si hay que parar"

David pide explícitamente "organizar todo por si te paras y corregir fácil". Esto significa:

1. **Separadores visuales fuertes** en db.ts entre módulos:
   ```typescript
   // ═══════════════════════════════════════
   // NOMBRE DEL MÓDULO — descripción breve
   // ═══════════════════════════════════════
   ```

2. **Cada función como bloque autónomo** — no mezclar lógica de negocio entre funciones del mismo archivo. Cada función CRUD debe ser autocontenida (hace su initDatabase, su SQL, y devuelve el resultado).

3. **Export block alineado por módulo** con comentarios:
   ```typescript
   // Productos
   obtenerProductos, obtenerProductoPorId, crearProducto,
   // Presupuestos
   obtenerPresupuestos, obtenerPresupuestoPorId,
   ```

4. **Rutas auto-contenidas** — cada ruta en su propio archivo con import directo de db.ts. No compartir lógica entre route files.

5. **Sin archivos "todo en uno"** — cada entidad o grupo de entidades afines tiene su propio archivo de rutas. La excepción: subrutas muy ligadas (cobros dentro de facturas, líneas dentro de presupuestos) pueden vivir en el mismo archivo.

## Agrupación de módulos por tanda (práctica real de AdelaCRM)

Basado en la implementación real del proyecto, los módulos se agrupan así para minimizar tandas:

```text
Tanda 1 — Productos + Presupuestos
  → routes/productos.ts + routes/presupuestos.ts
Tanda 2 — Facturación + VeriFactu + Cobros
  → routes/facturas.ts (cobros anidados como /:id/cobros) + routes/cobros.ts (standalone /api/cobros)
Tanda 3 — Pedidos de venta
  → routes/pedidos.ts (nuevo — completa el flujo Presupuesto→Pedido→Factura)
Tanda 4 — Proveedores + Compras + Inventario
  → routes/proveedores.ts + routes/pedidosCompra.ts + routes/stock.ts
Tanda 5 — Proyectos + Tareas + Time Tracking
Tanda 6 — Tickets + Contratos
Tanda 7 — RRHH + Marketing + Automatizaciones
Tanda 8 — Contabilidad + Informes + SuperAdmin
```

**Flujo de datos completo (con Pedidos como paso intermedio):**
```
Presupuesto aceptado → PEDIDO → Factura (VeriFactu) → Cobro → Contabilidad
```
Pedidos es el paso clave: conecta la venta cerrada (presupuesto aceptado) con la ejecución (proyecto, tareas) y la facturación.

**Nota importante sobre cobros:** Los cobros tienen un patrón DUAL:
- **Rutas anidadas** dentro de facturas: `GET /api/facturas/:id/cobros`, `POST /api/facturas/:id/cobros`, `DELETE /api/facturas/:id/cobros/:cobroId` — estas actualizan automáticamente `pendienteCobro` y estado de la factura (emitida → parcialmente_cobrada → cobrada).
- **Ruta standalone** aparte: `GET /api/cobros`, `POST /api/cobros`, `PUT /api/cobros/:id`, `DELETE /api/cobros/:id`, `POST /api/cobros/:id/conciliar` — para listado global de cobros, conciliación bancaria, y operaciones que no requieren modificar la factura padre.
- Ambas conviven. La ruta standalone NO debe actualizar el estado de la factura si no recibe explícitamente `facturaId` o se llama desde un contexto que lo requiera.
- La ruta standalone se monta en app.ts como `/api/cobros`.

## Módulos avanzados del spec de 26 secciones

Basado en la especificación detallada del usuario (junio 2026), estos módulos adicionales completan el ecosistema CRM+ERP:

### Módulo de Marketing y Comunicaciones
- **Segmentación** avanzada de contactos con filtros combinados
- **Campañas de email marketing** integradas (o vía API con Mailchimp, Brevo, etc.)
- **Plantillas de email** personalizables con variables dinámicas del CRM
- **Seguimiento** de apertura, clics y rebotes
- **Automatizaciones de nurturing**: secuencias de emails según comportamiento
- **Formularios web** embebibles para captura de leads (integración directa al CRM)
- **Fuentes de lead**: tracking de procedencia de cada contacto (web, redes, referido)

### Módulo de Comunicaciones Internas
- **Chat interno**: Mensajería instantánea entre usuarios, canales por equipo/proyecto
- **Notificaciones**: Centro de notificaciones para menciones, tareas vencidas, tickets urgentes
- **Correo desde plataforma**: Envío/recepción vinculados al CRM (integración IMAP/SMTP)
- **Calendario compartido**: Reuniones, llamadas y eventos vinculables a clientes/oportunidades
- **Videoconferencia**: Integración con Google Meet, Zoom o Teams

### Módulo de Automatizaciones (Workflow Engine) — detalle

**Disparadores disponibles:**
- Se crea/modifica/elimina un registro
- Un campo cambia de valor
- Una fecha se acerca o vence
- Se recibe un email o formulario web
- Una factura cambia de estado
- Un ticket lleva X horas sin respuesta

**Acciones disponibles:**
- Crear/actualizar/asignar un registro
- Enviar email automático (con plantilla)
- Enviar notificación interna
- Crear una tarea o recordatorio
- Llamar a un Webhook externo
- Mover un registro en el pipeline
- Ejecutar un script personalizado

### Marca Blanca — Personalización Completa
- **Identidad visual**: Logo en cabecera/login/favicon, paleta de colores primaria/secundaria, tipografía personalizada, fondo de login
- **Dominio y URL**: Acceso bajo dominio propio (app.miempresa.com), SSL automático (Let's Encrypt), sin referencias al software base
- **Textos y localización**: Nombre de la app configurable, textos de bienvenida/emails editables, multi-idioma (ES, EN, FR, PT)
- **Módulos de reventa**: Sub-cuentas con planes, facturación desde panel distribuidor, limitación de módulos por plan

### Integraciones Externas (22 partners)

| Integración | Propósito |
|-------------|-----------|
| Pasarelas de pago (Stripe, Redsys) | Cobro online de facturas con link de pago |
| Open banking (Nordigen/GoCardless) | Importación automática de extractos bancarios |
| Correo (Gmail, Outlook, IMAP) | Sincronización bidireccional de emails |
| Calendario (Google Calendar, Outlook) | Sincronización de eventos y reuniones |
| Almacenamiento (Google Drive, Dropbox, OneDrive) | Adjuntar documentos desde la nube |
| Firma electrónica (DocuSign, Signaturit, Viafirma) | Firma legal de contratos y presupuestos |
| ERP (Sage, A3, Holded) | Exportación de asientos y datos contables |
| Ecommerce (WooCommerce, Shopify) | Sincronización de pedidos y clientes |
| VoIP (Aircall, Ringover) | Click-to-call y registro automático de llamadas |
| WhatsApp Business API | Comunicación con clientes desde el CRM |
| Zapier / Make | Automatizaciones con miles de apps externas |
| AEAT (VeriFactu/SII) | Envío de registros de facturación y libros de IVA |

### Panel Super-Admin
Exclusivo para el propietario o distribuidor del software:
- **Gestión de tenants**: Crear, pausar, suspender o eliminar instancias
- **Facturación de plataforma**: Suscripciones, pagos, vencimientos de clientes del software
- **Configuración de planes**: Definir qué módulos incluye cada plan (básico, profesional, enterprise)
- **Monitorización global**: Dashboard con métricas de uso por instancia (usuarios activos, facturas emitidas, almacenamiento)
- **Actualizaciones**: Despliegue de nuevas versiones por instancia o globalmente
- **Soporte**: Sistema de tickets escalados desde instancias
- **Personalización**: Logo global, colores, textos legales, dominio de acceso

### Granularidad de permisos por rol

Para cada módulo, el rol puede tener permiso para:
- **Ver** (lectura de registros)
- **Crear** (nuevos registros)
- **Editar** (modificar registros existentes)
- **Eliminar** (borrado lógico o físico)
- **Exportar** (descarga de datos en CSV/PDF/Excel)
- **Ver de otros usuarios** (o solo los propios)
- **Aprobar** (en flujos de aprobación)

## Patrón de ajuste de stock con trazabilidad

```typescript
async function ajustarStock(
  productoId: string, almacenId: string, cantidad: number,
  tipo: string, referenciaTipo?: string,
  referenciaId?: string, notas?: string, creadoPor?: string
): Promise<Stock> {
  await initDatabase()
  // 1. Auto-crear registro de stock si no existe
  let stock = get<Stock>('SELECT * FROM stock WHERE productoId = ? AND almacenId = ?', [productoId, almacenId])
  if (!stock) {
    const id = `stk-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    run('INSERT INTO stock (id, productoId, almacenId, cantidad, stockMinimo) VALUES (?,?,?,0,0)', [id, productoId, almacenId])
    stock = get<Stock>('SELECT * FROM stock WHERE id = ?', [id])!
  }
  // 2. Calcular nuevo stock (nunca negativo)
  const stockAnterior = stock.cantidad
  const stockPosterior = Math.max(0, stockAnterior + cantidad)
  // 3. Actualizar
  run('UPDATE stock SET cantidad = ? WHERE id = ?', [stockPosterior, stock.id])
  // 4. Registrar movimiento con trazabilidad completa
  const ahora = new Date().toISOString()
  const movId = `mov-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  run('INSERT INTO movimientos_stock (...) VALUES (?,?,?,?,?,?,?,?,?,?)',
    [movId, productoId, almacenId, tipo, cantidad, stockAnterior, stockPosterior, referenciaTipo||null, notas||null, ahora])
  return { ...stock, cantidad: stockPosterior }
}
```

**Reglas:** auto-creación si no existe registro, stock mínimo seguro (Math.max), trazabilidad stockAnterior→stockPosterior, referencia opcional para auditoría origen-destino.

## Patrón de tests para CRM+ERP (node:test + supertest)

### Estructura de test

```typescript
import { describe, it, before } from 'node:test'
import assert from 'node:assert/strict'
import request from 'supertest'
import app from '../src/app.js'
import { initDatabase } from '../src/db.js'

describe('Módulo X', () => {
  let token = ''
  let entidadId = ''

  before(async () => {
    await initDatabase()
    const login = await request(app)
      .post('/api/auth/login')
      .send({ email: 'admin@adelacrm.local', pin: '1234' })
    token = login.body.token
  })

  it('1) crear entidad', async () => {
    const res = await request(app)
      .post('/api/entidades')
      .set('Authorization', `Bearer ${token}`)
      .send({ campo: 'valor' })
    assert.strictEqual(res.status, 201)
    assert.ok(res.body.entidad)
    entidadId = res.body.entidad.id
  })

  it('2) listar entidades', async () => {
    const res = await request(app)
      .get('/api/entidades')
      .set('Authorization', `Bearer ${token}`)
    assert.strictEqual(res.status, 200)
    assert.ok(Array.isArray(res.body.entidades))
  })
})
```

### Criterios de cobertura mínima
- CRUD completo (crear, listar, obtener por id, actualizar, eliminar)
- Filtros y query params
- Validación de errores (400 campos requeridos, 404 no encontrado)
- Flujos compuestos (crear padre → crear hijo → verificar relación)
- Autenticación (rechazar sin token, rechazar token inválido)

### Agregación de tests por archivo
Un archivo por dominio lógico, NO por tabla:
- `empresas-contactos.test.ts` (entidades base)
- `leads-oportunidades.test.ts` (pipeline ventas)
- `productos-presupuestos.test.ts` (catálogo + cotización)
- `facturas-cobros-pedidos-proveedores.test.ts` (facturación + cobros)
- `proyectos-tickets-empleados-tenants.test.ts` (operaciones + RRHH)

### Subagentes para tests
- delegate_task funciona bien para 10-15 tests por subagente
- **PITFALL:** Archivos de test >1200 líneas causan timeout del subagente (>600s). Si el test es muy grande, crearlo directamente con `write_file` en vez de delegar.
- Si un subagente timeout, verificar qué archivos creó antes de timeout y continuar desde ahí (NO re-delegar la verificación).

### Fix al patrón de rutas Express
Las rutas que usan `req.params` necesitan cast explícito:
```typescript
router.get('/:empleadoId/habilidades', async (req: AuthRequest, res: any) => {
  const habilidades = await obtenerHabilidades(req.params.empleadoId as string)
  // ...
})
```
El `res: any` evita conflictos de tipos con Express. El `as string` en params es obligatorio porque Express devuelve `string | string[]`.

## Auditoría de compatibilidad Frontend↔Backend

**⚠️ PATRÓN OBLIGATORIO tras añadir módulos nuevos al CRM.** El frontend hace llamadas `apiFetch('/api/...')` y si el backend no tiene exactamente esa ruta, la función falla silenciosamente (error 400/404 que el frontend ignora o muestra como "Sin datos").

### Procedimiento de auditoría

```bash
# 1. Extraer todas las llamadas API del frontend
grep -oP "apiFetch\(['\"]([^'\"]+)" public/js/crm.js | sed "s/apiFetch(['\"]//g" | sort -u > /tmp/frontend-rutas.txt

# 2. Extraer rutas registradas en backend
grep -oP "\"(/api/[^\"]+)\"" src/app.ts | tr -d '"' | sort -u > /tmp/backend-rutas.txt

# 3. Comparar — encontrar rutas del frontend sin match en backend
comm -23 /tmp/frontend-rutas.txt /tmp/backend-rutas.txt
```

### Patrones de mismatch comunes

| Frontend llama | Backend tiene | Solución |
|---|---|---|
| `GET/POST /api/ausencias` | Solo `/api/empleados/:id/ausencias` | Convenience route en app.ts |
| `GET/POST /api/contabilidad` (asientos) | Solo `/api/contabilidad/asientos` | Convenience route en app.ts |
| `POST /api/stock` | Solo `POST /api/stock/ajustar` | Redirección interna en app.ts |
| `GET /api/vacaciones` (sin param) | Solo `GET /api/vacaciones/:empleadoId` | Añadir GET / en el router |

### Patrón de convenience routes (en app.ts)

Cuando el frontend llama a `/api/X` pero el backend solo tiene `/api/padre/:id/X` o `/api/X/accion`, crear una ruta proxy delgada en `app.ts` que importe la función CRUD directamente de `db.js`:

```typescript
// En app.ts — importar funciones de db
import { obtenerAusencias, crearAusencia, aprobarAusencia, eliminarAusencia } from './db.js'

// Convenience route — el frontend llama /api/ausencias directamente
app.get('/api/ausencias', async (req, res) => {
  try {
    const items = await obtenerAusencias(String(req.query.empleadoId))
    res.json({ items })
  } catch (error) {
    res.status(500).json({ error: 'Error al obtener ausencias' })
  }
})
```

**Ventaja:** NO reescribir el frontend. El frontend sigue llamando `/api/ausencias` y la convenience route redirige internamente a la función existente de db.ts.

**Cast obligatorio:** `String(req.params.id)` y `String(req.query.xxx)` en todas las convenience routes porque Express devuelve `string | string[]`.

### Cuándo hacer la auditoría

1. **Tras añadir nuevos módulos** al CRM (nuevos tabs frontend + rutas backend)
2. **Tras refactorizar rutas** backend (cambiar estructura de endpoints)
3. **Antes de cada deploy** a producción
4. **Cuando el frontend muestra "Sin datos"** en un tab que debería tener datos

## Pitfalls conocidos

- **No intentar implementar 20 módulos de golpe** — Usar el roadmap por fases. Cada fase produce código funcional y verificado.
- **sql.js es en memoria** — Persistencia obligatoria en archivo tras cada escritura. Ver `adela-new-module` para el patrón exacto.
- **JWT_SECRET compartido** — Un solo `config.ts` exporta el secreto. Todos los archivos importan de ahí. Nunca generar inline.
- **jsonwebtoken en ESM** — Usar `createRequire` (no `import * as jwt`). `jwt.sign` no existe como método directo con import namespace.
- **Template literal SQL: no comerse backticks de cierre** — Al añadir `db.run(\`...\`)` al final de un bloque SQL existente con `patch`, el `old_string` debe incluir el backtick de cierre ` \`)` del bloque anterior para no dejar un `db.run()` sin cerrar. Síntoma: errores TS1005 '`,` expected' en todas las líneas SQL siguientes.
- **Express req.params.id es string | string[]** — NO es `string` directamente. Siempre castear: `const id = req.params.id as string`. Si no, TypeScript da TS2345 en cada llamada a función que espera string.
- **npx tsc funciona, npx tsc --noEmit puede dar falsos positivos** — El LSP del editor a veces reporta errores de `import.meta` o `esModuleInterop` que no existen al compilar de verdad. Usar `npx tsc` (sin --noEmit) para la verificación real. Si el output es vacío y exit_code=0, está limpio.
- **createRequire no va en types.ts** — `createRequire` es para archivos runtime (db.ts, routes, middleware). Si se pone en `types.ts`, causa error `TS1343: import.meta meta-property only allowed with module es2020/esnext/node16+`. types.ts solo debe tener interfaces y tipos, nunca imports de runtime.
- **Números de factura/presupuesto** — Usar serie + correlativo. Último número + 1. La serie se reinicia por año.
- **Líneas de detalle** — Las tablas de líneas (factura, presupuesto, pedido) deben tener `ON DELETE CASCADE` para que al borrar el padre se borren las líneas.
- **Campos VeriFactu** — Marcar `verifactuEnviado=1` solo cuando la AEAT confirme recepción. No asumir envío exitoso.
- **GET /api/vacaciones sin empleadoId** — El frontend llama `GET /api/vacaciones` (listado general) pero el backend solo tiene `GET /api/vacaciones/:empleadoId` (listado por empleado). Solución: añadir `GET /` sin parámetro en el router que devuelva todas las solicitudes. Pattern aplicable a cualquier entidad donde el frontend necesite un listado global + filtrado por padre.
- **`import crypto from 'crypto'` para hashes SHA-256 en ESM** — No usar `require('crypto')` (ReferenceError en ESM). El import directo funciona con `moduleResolution: "bundler"` o `esModuleInterop: true`. Patrón correcto: `import crypto from 'crypto'` al inicio de db.ts, luego `crypto.createHash('sha256').update(data).digest('hex')`.
- **No exportar pin_hash/password** — Helper `sanitizeUser()` en cada ruta que devuelva usuarios.
- **Express route ordering** — Rutas estáticas (`/stats`) antes que rutas con parámetros (`/:id`).
- **Omit type mismatch con auto-generated fields** — Si `crearFactura()` usa `Omit<Factura, 'id' | 'creado' | 'actualizado' | 'hashActual'>` pero auto-genera `numero`, `huellaDigital`, etc., la ruta DEBE pasar valores dummy (`numero: ''`, `verifactuEnviado: 0`, `pendienteCobro: 0`). No saltarse campos porque "la función los genera".
- **noImplicitReturns en Express + TypeScript strict** — Con `noImplicitReturns: true`, cada rama de un handler Express debe acabar con `return` explícito. Síntoma: error TS7030. Patrón correcto: `if (!item) { res.status(404).json({ error: 'No encontrado' }); return }` (el `return` tras `json()` es obligatorio aunque json() devuelva void).
- **noUnusedLocals con destructuring** — Con `noUnusedLocals: true`, al desestructurar `req.body` solo extraer los campos que realmente se pasan a db.ts. Si hay campos que db.ts no recibe (notas, serie, prioridad), eliminarlos del destructuring.
- **Fuente de verdad de nombres de campo** — db.ts (schema SQL + funciones CRUD) es la fuente de verdad, no types.ts. Cuando haya conflicto entre interfaces y columnas reales, actualizar types.ts, no db.ts. Ver `references/compilation-troubleshooting.md` para el flujo completo de resolución de errores de compilación y tabla de conversión de campos v2.
- **`verifactuEnviado` es number (0/1), no boolean** — SQLite INTEGER ≠ boolean. Pasar `0` o `1` en rutas, NUNCA `true`/`false`. El tipo TypeScript es `number`.
- **Cobro → Factura state machine** — Al crear/eliminar cobros, actualizar automáticamente `pendienteCobro` y el estado de la factura: `emitida` → `parcialmente_cobrada` → `cobrada`. Esto se implementa DENTRO de la función `crearCobro()`/`eliminarCobro()` en db.ts, NO en la ruta.
- **Emisión de factura solo desde borrador** — El endpoint `POST /:id/emitir` debe recalcular totales desde líneas (no confiar en valores enviados) y bloquear emisión si no está en `borrador`. Ver `references/tanda-implementacion.md` para el patrón exacto.
- **SQL JOIN con columnas inexistentes en tablas heredadas** — ⚠️ BUG REAL. Las funciones de listado que hacen JOIN con tablas hijas pueden referenciar columnas que no existen en la tabla padre. Ejemplo: `obtenerOportunidades()` hacía `LEFT JOIN leads l ON o.leadId = l.id` y luego `l.nombre, l.email, l.telefono` — pero la tabla `leads` tiene `titulo`, `valor` (NO `nombre`, `email`, `telefono`). **Causa:** 500 Internal Server Error silencioso. **Prevención:** verificar SIEMPRE que las columnas referenciadas en JOINs existen en ambas tablas antes de implementar. Usar `grep "CREATE TABLE.*leads" src/db.ts` y leer las columnas reales.

## Referencias

- `references/plan-crm-erp-total.md` — Plan maestro completo con 26 secciones, esquema BD completo, API por módulo, y roadmap de implementación por fases.
- `references/tanda-implementacion.md` — Patrón de implementación por tandas con pasos detallados (types → schema → CRUD → routes → server → compile), mapeo de tandas para el CRM+ERP completo, y pitfalls de Express typing y template literals SQL.
- El proyecto de referencia está en `/root/workspace/AdelaTest01/` — CRM funcional con los módulos base ya implementados.
- Los módulos Adela base están en `/root/workspace/Adela/` (22 módulos: auth, db, security, logger, etc.)
- `references/stock-adjustment-pattern.md` — Patrón de ajuste de stock con auto-creación, trazabilidad completa y rutas Express.
- `references/conexiones-flexibles-pattern.md` — Patrón de conexiones genéricas entre entidades: tablas, API, grafo N niveles, y tipos configurables por usuario.
- `references/frontend-backend-compat-audit.md` — Auditoría completa frontend↔Backend de AdelaCRM (2026-06-16): rutas que fallaban, convenience routes añadidas, patrones de fix.
- `references/csv-export-universal.md` — Patrón de exportación CSV universal para cualquier entidad del CRM: mapa de columnas, inyección de botón, descarga con BOM UTF-8 + separador `;` compatible con Excel español. Añadido en Tanda 9.
- `references/marca-blanca-implementation.md` — Implementación de marca blanca (white-label) multi-tenant: migración tenantId en usuarios, endpoint de branding, inyección dinámica de CSS variables en frontend tras login. Añadido en Tanda 9.
- `references/csv-export-universal.md` — Patrón de exportación CSV universal para cualquier entidad del CRM: mapa de columnas, inyección de botón, descarga con BOM UTF-8 + separador `;` compatible con Excel español.
- `references/marca-blanca-implementation.md` — Implementación de marca blanca (white-label) multi-tenant: migración tenantId en usuarios, endpoint de branding, inyección dinámica de CSS variables en frontend tras login.