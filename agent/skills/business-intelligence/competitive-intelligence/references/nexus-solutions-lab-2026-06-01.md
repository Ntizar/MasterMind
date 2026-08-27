# Nexus Solutions Lab — Caso de Estudio (2026-06-01)

**Propósito:** Reunión con Juan de la Torre García y su socio técnico para su producto Nexus Platform.
**URL:** nexus-solutions-lab.com
**Sector:** Agentes IA + datos AAPP (BNDS, Contratación) + comunicación multicanal

## Fase 1 — Superficie

- **Tagline:** "Menos trabajo manual. Más control en cada paso."
- **Subtítulo:** "Trabajo asistido, decisiones humanas"
- **Target:** Empresas (mencionan AAPP específicamente porque Juan contactó a David)
- **CTAs:** "Solicita una demo" (HubSpot forms), "Leer casos y guías" (blog vacío)
- **Tono:** Startup moderna, oscuro, gradientes indigo/purple, animaciones framer-motion
- **GTM ID:** GTM-WL7VHXM5 (tienen Google Tag Manager y Facebook Pixel)
- **Meta verification:** facebook-domain-verification = 9culj3ghlxptju0qnuzn3sy8ok17pe

## Fase 2 — Pricing

| Plan | Precio | Créditos | Almacenamiento | Historial | Agentes |
|------|--------|----------|----------------|-----------|---------|
| Starter | 29€/mes | 1.000 | 1 GB | 30 días | 3 |
| Growth | 149€/mes | 3.500 | 10 GB | 6 meses | — |
| Scale | 499€/mes | 12.000 | 50 GB | 1 año | — |
| Enterprise | A medida | — | — | — | — |

- **IVA NO incluido** (lo dicen explícitamente — señal de inmadurez para AAPP)
- **Modelo de créditos:** 1 crédito ≈ 1 consulta corta (~700 in / ~120 out tokens). Mencionan Gemini Flash como referencia económica.
  - Starter ≈ 1.000 consultas cortas/mes o 300 conversaciones normales
  - Growth ≈ 3.500 consultas cortas/mes
  - Scale ≈ 12.000 consultas cortas/mes
- **Playbooks predefinidos:** Ventas (lead por WhatsApp → CRM), Operaciones (cambio estado pedido), Soporte (FAQ → ticket → humano)
- **Sin freemium** — solo trial vía demo request

## Fase 3 — Stack Técnico (desde política de privacidad)

| Proveedor | Servicio | Región | ¿Fuera UE? | Notas |
|-----------|----------|--------|------------|-------|
| **Vercel** | Frontend hosting | UE (DE/NL) | No/Sí* | Next.js serverless |
| **Supabase** | DB + Storage | UE (EU-West) | No | PostgreSQL + auth + storage |
| **GCP** | IA / Infra | UE (europe-west) | No/Sí* | Vertex AI? inferencia |
| **Stripe** | Pagos | UE + EE.UU. | Sí | SCC+DTIA |
| **Pipedream** | Orquestación | EE.UU./Global | Sí | SCC+DTIA — integraciones |
| **Meta (WhatsApp)** | Canal mensajería | Global | Sí | SCC+DTIA |

**API propia:** api.nexus-solutions-lab.com
**Equipo identificado:**
- Juan de la Torre García (contacto, rol no especificado — probable perfil comercial)
- Socio técnico (sin identificar en fuentes públicas)
- Diego Fernández Gil — contacto protección datos (no DPO formal)

**Dominio:** Propietario no identificado via whois (sin datos públicos)

## Fase 4 — Posicionamiento

- **Problema que resuelven:** "Pérdida de horas en tareas manuales. Consultas sin responder. Copiar datos entre 10 herramientas."
- **Diferenciación aparente:** Conectan datos AAPP (BNDS, Contratación del Estado) + comunicación multicanal → nicho concreto poco explotado
- **No compiten con:** Zapier/Make (ellos son low-code genérico). No compiten con chatbots genéricos. Sí compiten con soluciones verticales de IA para AAPP.
- **Limitaciones implícitas:** Producto temprano. Sin casos de éxito públicos. Sin blog con contenido real. Sin demo pública. Sin LinkedIn corporativo visible.

**Señales de madurez:**
- ❌ Sin logos de clientes
- ❌ Sin testimonios
- ❌ Blog sin contenido (placeholder)
- ❌ Solo "solicitar demo"
- ❌ Sin LinkedIn público de la empresa
- ❌ Precios sin IVA
- ✅ Política de privacidad muy trabajada (RGPD, DPA, subprocesadores)

## Fase 5 — Preparación de Reunión

Ver nota principal `notes/2026-06-01-preparacion-nexus-lab.md` en el repo Mastermind.

**Juicio rápido:** Startup <1 año. Han currado la web y compliance, pero no tienen tracción visible. Probablemente quieren a David como partner técnico, caso de uso de referencia, o cartera de contactos. La oportunidad real: combinar sus canales (WhatsApp, Telegram) con los dashboards de datos de David (ESIOS, energía, contratación).
