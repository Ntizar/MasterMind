# Módulos avanzados CRM+ERP — Spec 26 secciones

Suplemento al plan maestro `plan-crm-erp-total.md`. Captura los módulos del spec detallado del usuario (junio 2026) que amplían el alcance original.

## Marketing y Comunicaciones

**Segmentación:** Filtros combinados sobre contactos (sector, etiquetas, actividad, ubicación, etc.). Crear segmentos guardados reusables.

**Campañas de email:** Integración con Mailchimp/Brevo vía API o motor interno:
- Plantillas con variables dinámicas del CRM (`{{contacto.nombre}}`, `{{empresa.cif}}`)
- Seguimiento de apertura, clics, rebotes
- Secuencias de nurturing automáticas (lead → 3 días → email1 → 7 días → email2)

**Formularios web:** HTML embebible que crea leads automáticamente. Tracking de fuente (web, redes, referido, campaña).

## Comunicaciones Internas

**Chat:** Mensajería en tiempo real entre usuarios. Canales por equipo/proyecto.

**Notificaciones:** Centro de notificaciones en la app. Eventos: menciones (@usuario), tareas vencidas, facturas cobradas, tickets urgentes, aprobaciones pendientes.

**Correo desde plataforma:** Integración IMAP/SMTP. Vincular emails entrantes/salientes al CRM automáticamente (por asunto o dirección).

**Calendario compartido:** Eventos vinculables a clientes, oportunidades, proyectos. Integración Google Calendar / Outlook (sync bidireccional).

## Marca Blanca (detalle)

- **Identidad visual:** Logo (cabecera, login, favicon, email footer), colores primario/secundario/fondo, tipografía personalizada, sin referencias al software base
- **Dominio:** app.miempresa.com → DNS → SSL automático (Let's Encrypt)
- **Textos:** Nombre de app configurable. Bienvenida editable. Multi-idioma (ES, EN, FR, PT) con archivos JSON de traducción
- **Reventa:** El distribuidor crea sub-cuentas con planes. Cada plan define módulos disponibles. Facturación integrada

## Integraciones (22 partners)

| Categoría | Partners | Patrón API |
|-----------|----------|------------|
| Pagos | Stripe, Redsys | POST link de pago → webhook cobro |
| Bancos | Nordigen, GoCardless | GET extractos → conciliación |
| Correo | Gmail, Outlook, IMAP | OAuth2 → sync bidireccional |
| Calendario | Google Calendar, Outlook | OAuth2 → sync eventos |
| Cloud | Drive, Dropbox, OneDrive | OAuth2 → file picker |
| Firma | DocuSign, Signaturit, Viafirma | POST documento → webhook firmado |
| ERP | Sage, A3, Holded | Export asientos contables |
| Ecommerce | WooCommerce, Shopify | Webhook pedido → CRM |
| VoIP | Aircall, Ringover | Click-to-call + log |
| WhatsApp | WhatsApp Business API | Plantilla → mensaje → webhook |
| Automatización | Zapier, Make | Webhook público → trigger |
| AEAT | VeriFactu, SII | POST registro factura |

## Panel Super-Admin

- **Gestión de tenants:** CRUD de instancias (crear, pausar, suspender, eliminar). Cada tenant = una base de datos aislada
- **Planes:** Definir qué módulos incluye cada plan (básico, profesional, enterprise). Precio, límites (usuarios, facturas/mes, almacenamiento GB)
- **Facturación SaaS:** Suscripciones, pagos, vencimientos, recordatorios automáticos
- **Monitorización:** Dashboard por instancia: usuarios activos, facturas emitidas (€), almacenamiento, última actividad
- **Soporte escalado:** Tickets de usuarios de instancias que escalan al superadmin
- **Actualizaciones:** Despliegue de nuevas versiones por instancia o global

## Granularidad de permisos

Cada módulo → 7 permisos booleanos por rol: `ver`, `crear`, `editar`, `eliminar`, `exportar`, `ver_otros` (vs solo propios), `aprobar` (flujos de aprobación)

## Mapa de relaciones completo

```
                    CONTACTOS / CLIENTES
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
       LEADS          PROYECTOS         TICKETS
          │                │                │
          ▼                ▼                ▼
    OPORTUNIDADES      TAREAS ──── TICKETS
          │           TIME TRACKING
          ▼
    PRESUPUESTOS ◄─── HORAS FACTURABLES
          │
          ▼
      PEDIDOS
          │
          ▼
      FACTURAS ──── VERIFACTU / AEAT
          │
          ▼
       COBROS ──── CONCILIACIÓN BANCARIA
          │
          ▼
    CONTABILIDAD ──── INFORMES / KPIs
```