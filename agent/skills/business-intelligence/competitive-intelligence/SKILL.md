---
name: competitive-intelligence
description: "Inteligencia competitiva y análisis de negocio desde presencia web pública — extraer modelo de negocio, pricing, stack técnico, equipo y posicionamiento de un competidor/socio/partner a partir de su dominio, y preparar estrategia de reunión."
version: 1.0.0
author: Mastermind
tags: [business-intelligence, competitor-analysis, research, meetings, sales-intelligence]
---

# Inteligencia Competitiva (Competitive Intelligence)

## Overview

Proceso sistemático para analizar una empresa desde su presencia web pública y preparar una reunión informada. A diferencia de `web-audit` (que analiza código, seguridad y rendimiento técnico), este skill analiza **modelo de negocio, pricing, stack, equipo y posicionamiento de mercado** — todo desde fuentes abiertas.

## When to Use

- El usuario menciona que tiene una reunión con una empresa: "tengo reunion con X"
- El usuario pide analizar un competidor: "analízame esta empresa"
- El usuario pide preparar una reunión comercial/de partnership
- El usuario pregunta: "qué me van a vender" o "qué podemos esperar de ellos"

## Do NOT use when

- Solo se necesita auditoría técnica de código/seguridad → usa `web-audit`
- Solo se necesita analizar el stack técnico → usa `web-audit` (fase de infraestructura)
- El usuario ya conoce la empresa y solo quiere preguntas → puede usar la Fase 5 directamente

## Required Tools

- `terminal` (curl, grep, sed, whois, dig)
- `write_file` (para guardar notas de preparación)
- No requiere browser tool (fallback curl-based si el browser falla)

## The 5-Phase Intelligence Process

### Phase 1: Superficie — Homepage + Metadatos

```
curl -sL "https://target.com" | head -500
```

Extraer: tagline, público objetivo, CTAs, tono, GTM ID, verificación redes sociales, schema.org.

### Phase 2: Pricing y Modelo de Negocio

Buscar sección pricing por ID/clase. Extraer:
- Número de planes y gap entre ellos
- Métrica de consumo (créditos, tokens, consultas)
- ¿IVA incluido o no?
- ¿Enterprise es real o placeholder?
- ¿Modelo freemium?

### Phase 3: Stack Técnico + Equipo (desde la Política de Privacidad)

Esta es la fase más infrautilizada y más reveladora. La política de privacidad lista subprocesadores, cloud providers, pasarelas de pago y nombres del equipo.

Buscar: subprocesadores (Supabase, Vercel, GCP, AWS, Stripe, Pipedream), nombres del responsable/DPO, emails, integraciones (WhatsApp, Slack, HubSpot, Meta).

**Qué revela el stack:**
- Vercel+Supabase = startup early típica
- Multi-región UE = más madurez
- Procesamiento fuera UE (Pipedream, Meta) = relevante para vender a AAPP
- Stripe = pagan con tarjeta, no transferencia

### Phase 4: Análisis de Posicionamiento

Responder:
- ¿Qué problema específico resuelven (no genérico)?
- ¿Contra quién compiten?
- ¿Qué NO hacen?
- ¿Canales de venta?

Señales de madurez comercial:
- ✅ Casos de éxito / logos / blog con contenido
- ❌ Solo "solicitar demo" sin nada más

### Phase 5: Preparación de Reunión (Meeting Prep)

Convertir el análisis en guión estructurado con:

1. **Romper hielo** — cómo surge la empresa, roles del equipo
2. **Pregunta clave de tracción** — "¿clientes de pago?"
3. **Stack técnico** (si hay socio técnico presente)
4. **Compliance** — DPA, auditorías, seguridad
5. **Propuesta de colaboración** — ¿qué quieren de ti?
6. **Cierre** — próximos pasos

Incluir **tabla de indicadores** a vigilar durante la call:

| Buenas señales | Red flags |
|----------------|-----------|
| Clientes de pago reales | Zero clientes |
| Técnico habla con propiedad | Técnico ausente o junior |
| Reconocen problemas reales | Todo suena genérico |
| Propuesta concreta | "Explorar sinergias" |

## Pitfalls

### No confundir con auditoría técnica
`web-audit` analiza código/seguridad. Esto analiza negocio/pricing/stack/posicionamiento. Si estás en modo inteligencia competitiva, no te pierdas en CSP o TTFB.

### La política de privacidad es la mejor fuente de stack
Mucho más fiable que el FAQ. Los listados de subprocesadores son oro puro. No saltarse esta fase.

### No asumir que el browser tool funciona
Tener preparado curl-based desde el principio. Verificar con `curl -sI` antes de intentar browser_navigate.

### Adaptar profundidad al stake de la reunión
- Exploratoria → Fases 1-3 rápido + Fase 5
- Negociación seria → todas las fases a fondo

## Integration with Other Skills

### With `web-audit`
- Este skill responde "¿quién son y qué venden?"
- `web-audit` responde "¿su código es seguro?"
- Complementarios, no sustitutivos

### With `dogfood`
- Si tienes acceso al producto, usa `dogfood` para QA exploratorio
- Inteligencia + dogfood = imagen completa

### With `sales-account-intelligence`
- `competitive-intelligence` → analiza un competidor/socio/partner
- `sales-account-intelligence` → analiza cuentas objetivo para venta (CRM → dossier)
- Usar juntos cuando el competidor está presente en la cuenta objetivo

### With `tech-report-cost-analysis`
- Para estimar costes de entrenamiento de modelos desde whitepapers técnicos, cargar `competitive-intelligence` (incluye sección de cost-analysis)

## Estimación de Costes desde Informes Técnicos

Cuando un informe técnico / whitepaper describe un modelo pero **no declara su coste**, usar este patrón dentro del análisis competitivo.

### Datos necesarios

| Dato | Dónde encontrarlo |
|------|-------------------|
| Número de GPUs | Tabla de especificaciones de entrenamiento |
| Tipo de GPU | Sección de cluster (H100, A100, GB200, etc.) |
| Fases de entrenamiento | Training recipe (pre-training, mid-training, RL, SFT) |
| Tokens por fase | Tabla de training specs |
| Goodput / MFU | Sección de cluster |

### Fórmulas de estimación

**Coste de hardware (CAPEX):**
```
Coste_hardware = GPUs × Precio_GPU_unitario × Factor_infraestructura
```
Precios de referencia (2024-2026):
- H100 SXM: ~$30,000 → ~$50,000 con infraestructura
- GB200 NVL72: ~$30,000 → ~$50,000 con infraestructura
- A100 80GB: ~$15,000 → ~$25,000 con infraestructura

**Coste operativo (OPEX):**
```
Coste_entrenamiento = GPUs × Horas_entrenamiento × Coste_GPU_hora
```
Costes por hora GPU:
- H100: $1-2/hora on-prem, $3-5/hora cloud
- GB200: $1.5-3/hora on-prem, $4-7/hora cloud

### Ejemplo: MAI-Thinking-1 (Microsoft, 2026)
- 8,192 GB200 NVL72, ~90% goodput
- Pre-training: 30T tokens, 8,192 GPUs (~60 días)
- Estimación total: **$50-100M** incluyendo equipo, datos y operación

### Pitfalls
- **No asumir que el informe declara el coste** — la mayoría no lo hacen
- **Goodput importa** — 90% goodput significa 10% tiempo desperdiciado
- **Las iteraciones importan** — el modelo final es resultado de muchas ejecuciones
- **La estimación es un rango, no un número exacto** — siempre dar intervalo

## Linked Reference Files

- `references/nexus-solutions-lab-2026-06-01.md` — Caso de estudio real: análisis completo de Nexus Solutions Lab con pricing, stack (Vercel+Supabase+GCP+Stripe+Pipedream), posicionamiento AAPP y preparación de reunión
