---
name: sales-account-intelligence
description: "Account Intelligence para venta de Control-M — análisis profundo de cuentas, detección de pains, tech stack, oportunidades comerciales y plan de acción. Usa datos CRM (Salesforce) + fuentes públicas para generar dossiers ejecutivos orientados a venta."
version: "1.0.0"
author: Mastermind
tags: [sales-intelligence, account-management, control-m, b2b-sales, competitive-intelligence, crm]
---

# Account Intelligence — Control-M Sales

## Overview

Sistema completo de inteligencia de cuentas para venta de **Control-M de BMC Software** (orquestación de workflows y automatización de procesos de negocio y TI). Combina datos de CRM (Salesforce) con análisis de fuentes públicas para generar dossiers ejecutivos con pains, oportunidades y plan de acción comercial.

## When to Use

- El usuario quiere analizar una cuenta para vender Control-M
- El usuario pide "account intelligence" o "dossier de cuenta"
- El usuario menciona prospectar una empresa
- El usuario quiere preparar una reunión comercial con una cuenta
- El usuario pide "analiza esta empresa para Control-M"

## Do NOT use when

- Solo se necesita auditoría técnica de código/seguridad → usa `web-audit`
- Solo se necesita análisis de un competidor → usa `competitive-intelligence`
- El usuario quiere un informe financiero → no es este skill

## Prerequisites

### 1. Datos de cuentas (Salesforce export)

El skill espera un archivo JSON con cuentas de Salesforce. Formato:

```json
[
  {
    "tier": "A – Atacar primero",
    "score": "10",
    "account": "Banco Sabadell",
    "country": "Spain",
    "segment": "Finance & Insurance",
    "subsegment": "Banking",
    "fit_subsegmento": "5",
    "top_enterprise": "1",
    "cliente_actual": "SaaS",
    "en_curso": "0",
    "aproximacion_notas": "Plan de transformación digital 2025-2027. Inversión 200M€ en cloud."
  }
]
```

**Cargar datos:**
```bash
# Si tienes el Excel de Salesforce, convertirlo:
python3 scripts/convert-xlsx-to-json.py /path/to/accounts.xlsx
# O usar el script incluido:
python3 scripts/control-m/extract-accounts.py /path/to/accounts.xlsx
```

**Si no tienes datos CRM:** El skill funciona con nombre de empresa + sector. Genera análisis basado en fuentes públicas (inferencias marcadas claramente).

### 2. Estructura de directorios

Los scripts están en `scripts/control-m/`:

```
scripts/control-m/
├── extract-accounts.py      # Convierte Excel Salesforce → JSON
├── generate-report.py       # Genera HTML/PDF de informe
├── template.html            # Plantilla HTML del informe (3 páginas)
├── search-stakeholders.py   # Búsqueda de stakeholders (LIMITADA — ver pitfall)
├── data/
│   └── accounts.json        # Cuentas procesadas (614 España)
└── reports/
    └── *.pdf                # Informes generados
```

**Nota:** Los scripts están en `scripts/control-m/`, NO en el skill directory. El skill SKILL.md está en `agent/skills/sales/sales-account-intelligence/`.

## The 6-Phase Account Intelligence Process

### Phase 0: Contexto del Producto

Antes de cualquier análisis, la IA debe conocer exactamente qué vende Control-M:

**Capacidades clave:**
- Orquestación multi-plataforma (batch, data, cloud, mainframe, SAP)
- Multi-cloud nativo (AWS, Azure, GCP, híbrido)
- SAP workload management
- Data workflow orchestration (ETL/ELT)
- Business process automation
- Event-driven automation
- AI/ML Ops
- Self-healing

**Competencia directa:**
| Competidor | Propietario | Fortaleza | Debilidad vs Control-M |
|------------|-------------|-----------|------------------------|
| Automic/UC4 | Broadcom | Mainframe, SAP | Cloud-native débil, licensing complejo |
| Tidal | OpenText | Data workflows | Ecosistema pequeño, pocos conectores cloud |
| Apache Airflow | LF (open source) | Data/ML pipelines | No gestiona batch legacy, SAP, mainframe |
| Cron/K8s Jobs | — | Simple, gratis | Sin visibilidad, sin gestión de dependencias |

**Diferenciadores:**
- Única plataforma que une batch + cloud + SAP + data + mainframe
- +200 conectores nativos
- Pricing más flexible que Broadcom
- Self-healing y event-driven (Airflow no lo tiene)

### Phase 1: Intelligence de Cuenta

**Datos de CRM (si disponibles):**
- Tier (A, B, C, D, I, X)
- Score
- Segment / SubSegment
- Cliente actual / En curso
- Notas de aproximación

**Fuentes públicas a buscar:**
- Trigger events: fusiones, adquisiciones, cambios de CIO/CTO, migraciones cloud anunciadas, nuevas regulaciones
- Señales de compra: hiring de roles IT, RFPs, inversiones IT anunciadas, partnerships tecnológicos
- Presupuesto IT estimado
- Situación financiera (si es pública)

**Output:**
- Visión general de la empresa
- Trigger events recientes (timeline)
- Señales de compra (tabla)
- Estimación de presupuesto IT

### Phase 2: Tech Stack y Automatización

**Analizar:**
- Cloud: AWS/Azure/GCP/híbrido (con fuentes)
- Aplicaciones críticas: SAP, Salesforce, legacy, mainframe
- Data: lakes, warehouses, analytics
- Automatización actual: qué usan, cómo lo hacen
- **Gap analysis:** qué tienen vs. qué les falta vs. qué ofrece Control-M

**Output:**
- Tabla de cloud e infraestructura
- Tabla de aplicaciones críticas
- Tabla de automatización y scheduling (CRÍTICO)
- Identificación de gap crítico

### Phase 3: Pains por Vertical Sectorial

**Pains comunes por sector:**

**Banca:**
- Batch nocturno con scripts manuales
- Compliance regulatorio (BCB, DORA)
- SAP para reporting financiero
- Mainframe legacy con COBOL

**Seguros:**
- Procesamiento de siniestros batch
- Legacy systems + cloud
- Compliance sanitario
- Suscripción automatizada

**Retail:**
- Promociones y pricing batch
- Inventario multi-sucursal
- Omnicanal coordination
- Supply chain optimization

**Manufactura:**
- Producción batch
- Supply chain / IoT
- Compliance industrial
- Maintenance scheduling

**Output:**
- Tabla de pains con: problema, impacto, solución Control-M, beneficios, roles afectados

### Phase 4: Oportunidades Comerciales

**Clasificar oportunidades:**

1. **Quick Wins** (bajo esfuerzo, alto impacto):
   - Migrar batch crítico de scripts a Control-M Cloud
   - Orquestación SAP en cloud
   - Consolidar herramientas fragmentadas

2. **Land & Expand** (entrada pequeña, crecimiento):
   - Control-M Enterprise completo
   - Business Process Automation
   - Multi-región / multi-tenant

3. **Análisis competitivo:**
   - Por qué Control-M sobre X
   - Estrategia de diferenciación

4. **ROI estimado:**
   - Horas ahorradas
   - Reducción de fallos
   - Coste OPEX evitado

### Phase 5: Stakeholders y Plan de Acción

**Identificar stakeholders:**
- CTO / CIO
- Head of Infrastructure & Operations
- SAP Manager
- Head of Data & Analytics
- CRO / Compliance

**Para cada stakeholder:**
- Rol y responsabilidad
- Ángulo de acercamiento
- Objecciones anticipadas y respuestas

**Plan de acción:**
- Pasos concretos con timing
- Prioridad (ALTA/MEDIA/BAJA)
- Probabilidad de cierre

### Phase 6: Generación de Informe

**Output final:**
- Dossier compacto de **3 páginas** (no extenso)
- HTML profesional + conversión a PDF (A4, ~90KB)
- Resumen en texto plano (para Telegram/email)

**Comandos:**
```bash
# Generar informe de cuenta #1
python3 scripts/control-m/generate-report.py 1

# Generar informe de cuenta por nombre
python3 scripts/control-m/generate-report.py --name "Banco Sabadell"

# Generar informe de múltiples cuentas
python3 scripts/control-m/generate-report.py 1 5 12

# Generar todas las Tier A
python3 scripts/control-m/generate-report.py --tier "A – Atacar primero"

# Generar informe de sector
python3 scripts/control-m/generate-report.py --segment "Banking"

# Generar informe y convertir a PDF
python3 scripts/control-m/generate-report.py 1 --pdf
```

**Estructura del informe (3 páginas):**
1. **Portada** — Datos CRM de la cuenta
2. **Tech Stack** — Cloud, SAP, legacy, automatización actual, gap analysis
3. **Pains + Oportunidades** — Tabla de pains con solución Control-M, quick wins, land & expand
4. **Stakeholders + Plan** — Roles clave con ángulo de acercamiento, plan de acción con timing

### ⚠️ LIMITACIÓN CRÍTICA: Búsqueda de Stakeholders

**NO se pueden buscar nombres reales de personas automáticamente:**
- **LinkedIn** → requiere login (no tengo credenciales de acceso)
- **Google** → bloquea por CAPTCHA desde IP de server (46.62.185.46)
- **DuckDuckGo HTML** → no devuelve resultados útiles para queries de personas
- **SearXNG** → no responde o no da resultados útiles

**Solución:** El informe incluye los roles genéricos (CTO, Head of Infra, SAP Manager, Head of Data) con ángulo de acercamiento. Para encontrar nombres reales:
- Buscar manualmente en LinkedIn: `site:linkedin.com "Empresa" CTO`
- Buscar en prensa: `"Empresa" "nuevo CTO"` o `"Empresa" "contrata"`
- Buscar en ofertas de empleo: `"Empresa" "Head of IT"` (a veces aparecen managers)

NUNCA intentar automatizar la búsqueda de stakeholders — no funciona sin credenciales de LinkedIn o proxy residencial. El script `search-stakeholders.py` existe pero es de referencia para cuando haya credenciales disponibles.

### ⚠️ Pitfalls Operativos

- **Google/LinkedIn scraping desde server IP = imposible.** CAPTCHA en Google, login en LinkedIn. DuckDuckGo HTML no devuelve resultados útiles. SearXNG no responde. No perder tiempo intentándolo.
- **`write_file` se trunca en archivos grandes.** Si el contenido supera ~10KB, dividir en múltiples writes o usar `patch`.
- **`patch` puede corromper archivos con `\n` literales.** Cuando un archivo es complejo (>200 líneas), reescribir con `write_file` en vez de parchear.
- **`generate-report.py` usa Playwright Chromium en `/opt/hermes/node_modules/playwright-core`, NO Puppeteer.** Puppeteer no está instalado en el venv.
- **El Excel de Salesforce usa sharedStrings.xml + sheet1.xml con índices.** No se puede parsear con librerías simples sin pip. El script `extract-accounts.py` ya maneja esto.
- **Los datos de tamaño (facturación, empleados) están en `add-company-data.py`.** Solo ~20 Tier A tienen datos. Para añadir más, editar el diccionario `SIZE_DATA`.
- **NUNCA generar todos los informes de golpe.** Son ~600 cuentas. Generar a demanda: por tier, por sector, por nombre, o por índice. Batch de 10-20 máximo.

## Pitfalls

### No inventar datos del CRM
Los datos de CRM (tier, score, notas) son fuente de verdad. NUNCA los modifiques ni inventes datos adicionales. Si una cuenta no tiene datos CRM, marcar todo como "inferencia por sector".

### Distinguir directo de inferencia
Siempre marcar:
- `Fuente directa` — cuando hay confirmación pública (noticias, ofertas de empleo, comunicados)
- `Mención indirecta` — cuando es inferencia por sector, stack típico, o hiring patterns

### Plantilla de 3 páginas, no extensa
El informe debe ser compacto: 3 páginas máximo. No generar dossiers largos. El usuario quiere información accionable, no relleno.

### Datos de tamaño (facturación, empleados, oficinas)
Los datos de tamaño están en `add-company-data.py` para ~20 Tier A. Para añadir más empresas, editar el diccionario `SIZE_DATA` en ese script. Si una cuenta no tiene datos de tamaño, el informe muestra "N/A" — no inventar datos.

### No generar todos los informes de golpe
NUNCA generar los 614 informes de golpe. Son ~100MB de PDFs. Generar a demanda: por tier (`--tier`), por sector (`--segment`), por nombre (`--name`), o por índice (`1 5 12`). Batch de 10-20 máximo por ejecución.

### No confundir con competitive-intelligence
`competitive-intelligence` analiza un competidor/socio/partner. `sales-account-intelligence` analiza una cuenta objetivo para venta. Son complementarios, no sustitutivos.

### El Excel de Salesforce puede tener duplicados
El extract `extract-accounts.py` ya filtra duplicados por nombre. Si ves duplicados en el output, es porque los nombres son ligeramente diferentes. Normalizar antes de procesar.

### Los nombres de archivo HTML pueden ser largos
Sanitizar nombres de cuenta para filenames: reemplazar espacios, acentos y caracteres especiales. Truncar a 60 chars.

### No generar todos los informes de golpe
Generar informes en batch de 10-20 máximo. Para 100+ informes, usar cron jobs o generar a demanda.

### NUNCA intentar buscar stakeholders automáticamente
LinkedIn requiere login, Google bloquea por CAPTCHA desde IP de server, DuckDuckGo no responde. El informe incluye roles genéricos (CTO, Head of Infra...) y el usuario busca nombres manualmente. No perder tiempo intentando automatizar esto.

### Plantilla de 3 páginas, no extensa
El informe debe ser compacto: 3 páginas máximo. No generar dossiers largos. El usuario quiere información accionable, no relleno.

## Integration with Other Skills

### With `competitive-intelligence`
- `competitive-intelligence` → analiza un competidor/socio/partner
- `sales-account-intelligence` → analiza cuentas objetivo para venta
- Usar juntos cuando el competidor está presente en la cuenta objetivo

### With `web-audit`
- `web-audit` → auditoría técnica de código/seguridad
- `sales-account-intelligence` → análisis comercial de cuenta
- Usar juntos para cuentas con interés técnico profundo

### With `linkedin-david-antizar-style`
- Para generar posts LinkedIn sobre casos de éxito de Control-M

## Data Model

### Account Object
```python
{
    "tier": str,           # "A – Atacar primero", "B – Alta prioridad", etc.
    "score": str,          # 0-10
    "account": str,        # Nombre de la empresa
    "country": str,        # País
    "segment": str,        # "Finance & Insurance", "Retail & Wholesale Trade", "Manufacturing"
    "subsegment": str,     # "Banking", "Insurance", "Retail", "Manufacturing", etc.
    "fit_subsegmento": str,# 1-5 (nivel de ajuste con Control-M)
    "top_enterprise": str, # "1" si es empresa top
    "cliente_actual": str, # "SaaS", "Perp", "OPS", "Endpoints", "0"
    "en_curso": str,       # "1" si hay oportunidad en curso
    "aproximacion_notas": str  # Notas de CRM sobre la cuenta
}
```

### Scoring Logic
- **Tier A** → Score >= 7, prioritar atacar
- **Tier A★** → Score >= 9, en curso con comercial asignado
- **Tier B** → Score >= 5, alta prioridad
- **Tier C** → Score >= 3, media prioridad
- **Tier D** → Score >= 0, nurturing
- **Tier I** → Cliente actual, NO prospectar new logo
- **Tier X** → Descartar

### Wallet Estimation
- **Banking/Insurance Tier A:** 300-600K€/año
- **Banking/Insurance Tier B:** 150-400K€/año
- **Retail/Wholesale Tier A:** 250-500K€/año
- **Retail/Wholesale Tier B:** 100-300K€/año
- **Manufacturing Tier A:** 200-500K€/año
- **Manufacturing Tier B:** 100-300K€/año
- **Pharma/Chemicals Tier A:** 200-400K€/año
- **Pharma/Chemicals Tier B:** 100-250K€/año

## Linked Reference Files

- `references/README.md` — Quick reference para Gandarillas con comandos y estructura
- `references/quick-start.md` — Guía de inicio rápido en 3 pasos
- `references/stakeholder-search-limitations.md` — Documentación de la limitación de búsqueda de stakeholders y workaround manual

```bash
# 1. Si tienes Excel de Salesforce:
python3 scripts/control-m/extract-accounts.py /path/to/accounts.xlsx

# 2. Generar informe de cuenta #1:
python3 scripts/control-m/generate-report.py 1

# 3. Generar PDF:
python3 scripts/control-m/generate-report.py 1 --pdf

# 4. Generar todas las Tier A:
python3 scripts/control-m/generate-report.py --tier A --pdf
```
