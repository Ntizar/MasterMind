---
name: prisma-systematic-review
description: "Sistema completo de revisiones sistemáticas PRISMA 2020 sobre infraestructura Hermes Agent. Orquestación multi-fase, auditoría automática, DOI-first, gate editorial, paquetes publicables."
version: "1.0.0"
tags: [research, prisma, systematic-review, hermes, methodology, academia]
author: "David Antizar"
---

# PRISMA Systematic Review — Sistema sobre Hermes Agent

## Resumen ejecutivo

Sistema de revisión sistemática que convierte una pregunta de investigación en un paquete editorial publicable (PDF + LaTeX + Markdown) con trazabilidad completa, auditoría automática y cumplimiento PRISMA 2020 / PRISMA-S. No es un agente que escribe artículos: es una infraestructura con reglas, archivos, comandos y controles materiales.

**Filosofía:** La memoria del sistema no está en el chat, sino en archivos. Hermes no "recuerda" — relee lo que dejó escrito para generar decisiones adecuadas. La continuidad depende de archivos de estado persistentes, no de la memoria conversacional.

## Cuándo usar

- Revisión sistemática de literatura con metodología PRISMA 2020
- Revisión que debe ser auditable por revisores/peer reviewers
- Búsqueda multi-fuente con normalización DOI
- Generación de paquetes editorial + LaTeX editables
- Cuando se necesita watchdog/reanudación automática
- Proyectos académicos que requieren transparencia metodológica

## Cuándo NO usar

- Revisión narrativa sin protocolo formal
- Búsqueda rápida de estado del arte (usar web_search)
- Papers originales de ML (usar research-paper-writing)
- Revisiones de solo un par de papers

---

## Arquitectura del sistema

### Capas

1. **Superficie** — Telegram (no dependencia de interfaz web)
2. **Runtime Docker** — 2 servicios:
   - `hermes-agent`: gateway + trabajo principal
   - `hermes-prisma-watchdog`: monitoriza revisiones vivas, reanuda fases ante estancamiento
3. **Política de modelos** — cadena de relevo:
   - Primario: Qwen 3.6 (NaN Builders)
   - Relevo: DeepSeek v4-pro, Kimi K2.6, Qwen3-coder, Gemma4 (Ollama Cloud)
   - Config en `config.yaml` con temperatura, top-p, max tokens, frequency penalty, response format
4. **Orquestación** — scripts Python + skills locales
5. **Skills** (10 en `hermes-home/skills/research/`):
   - Revisión sistemática (base)
   - Estado (runtime-state)
   - Revisión académica
   - Integridad
   - Mapa de cambios
   - Y 5 más de soporte

### Artefactos de configuración

```
config.yaml           — política de modelos, parámetros
docker-compose.yml    — servicios hermes-agent + watchdog
start-gateway.sh      —启动仪式
prisma-watchdog.py    — monitor de estancamiento
```

---

## 6 Reglas metodológicas (no negociables)

1. **PRISMA 2020** como marco de elaboración de informes
2. **PRISMA-S** como marco de transparencia de búsqueda
3. **DOI-first** siempre que el identificador exista
4. **Texto completo obligatorio** para el corpus final
5. **Recomputación de conteos** desde artefactos reales (no escritos a mano)
6. **Cierre editorial solo con gate PASS**, no con impresión subjetiva

### Fuentes de las reglas

- Page et al. 2021 (BMJ n71) — PRISMA 2020
- Rethlefsen et al. 2021 (PRISMA-S)
- Cochrane Handbook ch. 4
- Whiting et al. 2016 (ROBIS)
- Shea et al. 2017 (AMSTAR 2)

---

## Fases del sistema

### FASE 1: Intake, pregunta y criterios

**Objetivo:** Congelar la frontera metodológica desde el primer momento.

**Artefactos generados:**
- `protocol/intake.md` — pregunta, ventana temporal, tipo de estudio, N deseado
- `protocol/eligibility-criteria.md` — criterios de inclusión/exclusión
- `protocol/search-strategy.md` — estrategia de búsqueda documentada

**Script clave:** `bootstrap_topic_review.py`
- Crea directorios del proyecto
- Materializa el punto de partida
- Genera los protocol iniciales
- Fija el contrato metodológico de la revisión

**Decisión importante:** Sin revista concreta → modo `generic-common-core` (plantilla primer filtro). Esto afecta LaTeX, paquete y tono editorial.

**Pitfalls:**
- Si el tema nace como "vamos a ver qué sale", el resto automatiza ambigüedad
- La sesión debe congelar: pregunta, ventana temporal, tipo de estudio, N final, criterios, marco editorial
- Si el sesgo nace aquí, toda la revisión está comprometida

### FASE 2: Búsqueda multi-fuente y normalización DOI

**Fuentes de datos:**
- OpenAlex
- Crossref
- Semantic Scholar
- arXiv

**Scripts clave:**
- `bootstrap_topic_review.py` — queries HTTP directas + parseo JSON/Atom
- `doi_audit.py` — estabiliza identidad bibliográfica

**Artefactos generados:**
```
searches/search-log.csv        — consulta, fuente, fecha, volumen
records/master-records.csv     — universo bruto normalizado
records/doi-index.csv          — clave canónica por DOI
records/duplicates.csv         — colisiones detectadas
records/missing-doi.csv        — sin DOI (usa hash → RID)
```

**Lógica DOI-first:**
- Si existe DOI → identificador canónico
- Sin DOI → hash estable genera RID
- Duplicados → merges con trazabilidad
- Ambiguos → se señalan, no se descartan silenciosamente

### FASE 3: Cribado (Screening)

**Lógica de decisión (4 capas):**
1. **Reglas mínimas** — umbral de texto útil
2. **Decisión asistida por modelo** — el modelo propone
3. **Canonización de decisión** — normaliza variantes
4. **Auditoría con recomputación** — conteos recalculados desde decisiones canonizadas

**Script clave:** `complete_review.py`
- `canonicalize_screening_decision()` — normaliza: include, include_ft, exclude, excluido, excluir, maybe → conjunto consistente
- Umbral mínimo de texto para inclusión final

**Decisión OK:** supera reglas mínimas + confirma foco en texto completo + justificación trazable en CSV

**Decisión KO:** falla criterios / motivo de exclusión claro

**Decisión "más":** cribado rápido no basta → requiere revisión adicional

**Referencia:** ROBIS (Whiting et al. 2016), AMSTAR 2 (Shea et al. 2017)

### FASE 4: Extracción profunda

**Objetivo:** No solo saber que es "experimental", sino extraer qué nombra, qué benchmark, qué muestra, qué variables, qué método, qué teoría.

**Artefacto clave:** `extraction/extraction-table.csv`

**Campos de extracción (4 bloques):**

**Núcleo común:**
- work_type, year, DOI, authors, publication, keywords, abstract

**Bloque empírico:**
- empirical_type, design_detail, country, sample_size, method, dependent_variables, independent_variables, instruments

**Bloque técnico:**
- models_or_systems_studied, benchmark_dataset_or_corpus, corpus, tasks

**Bloque teoría y síntesis:**
- theoretical_framework, key_findings, extraction_confidence

**Script de refuerzo:** `refresh_extraction_depth.py`
- Relee texto extraído del PDF
- Fuerza capa más profunda cuando el primer pase es insuficiente
- Resuelve: artículos que parecían "experimental" pero en texto completo ofrecen más datos

### FASE 5: Evidencia visual (figuras)

**Script clave:** `prepare_paper_figures.py`

**Separación de tipos:**
- `figures/extracted/` — figuras científicas detectadas en PDFs
- `figures/page-renders/` — renderizados de apoyo
- `figures/manifest.csv` — trazabilidad
- `figures/figure-catalog.md` — catálogo navegable
- `figures/figure-ranking.csv` — ranking por relevancia

**Firma de figuras propias:** prefijo hexadecimal (ej: `686f6c6a`) para distinguir de evidencia ajena. Mezclar reutilización de evidencia ajena y síntesis visual propia = mala práctica.

**Referencias:** FAIR (Wilkinson et al. 2016), ACM Artifact Review

### FASE 6: Generación del manuscrito

**Script clave:** `publication_audit.py`

**Funciones:**
- Recompone secciones
- Limpia incoherencias
- Normaliza citas y referencias
- Integra tablas y figuras
- Detecta huecos obvios
- Genera manuscrito en 3 formatos

**Artefactos finales:**
```
paper/manuscript/publication-ready.md      — editable
paper/manuscript/publication-ready.tex     — LaTeX técnico
paper/manuscript/publication-ready.pdf     — compilado listo
paper/references/references.generated.bib  — BibTeX
main-common-core.tex                       — plantilla sin revista objetivo
```

**Requisitos editoriales:**
- Cada estudio relevante → ficha con 1-2 párrafos ANTES de tabla compacta
- Bloques ampliados: discusión, implicaciones teóricas, aportación original, conclusiones, líneas futuras
- Tono "determinista" — validez académica reconocible

### FASE 7: Revisión cruzada, integridad y gate editorial

**Capa que más diferencia de un flujo convencional con LLMs.**

**Scripts y funciones:**

| Script | Función |
|--------|---------|
| `publication_peer_review.py` | Revisión cruzada multi-modelo |
| `check_manuscript_integrity.py` | Detecta afirmaciones flojas, inconsistencias, huecos |
| `build_revision_roadmap.py` | Convierte revisión en matriz de cambios accionables |
| `publication_gate.py` | Comprueba artefactos + si cierre es legítimo |
| `publication_autopilot.py` | Bucle de reiteración hasta PASS o bloqueo documentado |

**Política de modelos revisores (`reviewer-models.csv`):**
- Revisor A: Qwen 3.6 (NaN)
- Revisor B: DeepSeek v4-pro
- Relevo editorial: Kimi K2.6

**Salidas de revisión:**
```
paper/review/review-manifest.csv
paper/review/peer-review-overview.md
paper/review/reviewer-A/
paper/review/reviewer-B/
```

**Referencia:** lógica de evaluación estructurada ROBIS/AMSTAR 2 + espíritu ACM Artifact Review

### FASE 8: Paquetes finales y memoria operativa

**Gate PASS → genera 2 paquetes:**

| Paquete | Contenido | Destino |
|---------|-----------|---------|
| `paper/package/publication-package.zip` | Paquete editorial general | Envío a revista |
| `paper/package/publication-latex-editable.zip` | Continuidad académica editable | Colaboradores |

**Sincronización Obsidian:**
```
sync_review_to_obsidian.py
```
- Sincroniza revisión al vault de Obsidian
- Versión navegable: fichas, overview, biblioteca visual, notas, rastro PRISMA
- Cumple principios FAIR: localizable, accesible, interoperable

**Memoria operativa:**
```
notes/runtime-state.md    — estado legible
notes/runtime-state.json  — estado serializado
```
- El watchdog relee y reanuda desde aquí
- La memoria real del sistema está FUERA del chat

---

## Guardrails no negociables

### Metodológicos
- **Texto completo obligatorio** para inclusión final (resumen no basta)
- **Conteos recalculados** desde decisiones canonizadas (nunca escritos a mano)
- **Gate PASS** para cierre (no impresión subjetiva)
- **Trazabilidad** en cada decisión de inclusión/exclusión
- **Separación** de figuras propias vs. evidencia ajena

### Operativos
- **Estado persistente** en archivos, no en memoria conversacional
- **Watchdog** para reanudación automática
- **Multi-modelo** para revisión cruzada
- **Configuración en YAML** con todos los parámetros visibles
- **Scripts versionables** como contrato metodológico

### Técnicos
- **Tokens:** exigir texto completo legible para inclusión final
- **Modelo:** debe soportar papers largos y extraer bien el texto
- **No recursion:** NO llamar buildSummary() recursivamente (causa OOM)
- **Charts:** `var charts = window.charts = {}` (NO const) en frontend
- **Tab lazy:** NO marcar clima/gas en renderTab, solo al terminar fetch

---

## Scripts del sistema (inventario completo)

| Script | Fase | Función principal |
|--------|------|-------------------|
| `bootstrap_topic_review.py` | 1-2 | Crear proyecto + queries multi-fuente |
| `doi_audit.py` | 2 | Normalización DOI, duplicados, trazabilidad |
| `complete_review.py` | 2-3 | Orquestación de secuencia completa |
| `review_runtime_state.py` | Todas | Serialización de estado operativo |
| `refresh_extraction_depth.py` | 4 | Re-extracción profunda de PDFs |
| `prepare_paper_figures.py` | 5 | Separación y catálogo de figuras |
| `publication_audit.py` | 6 | Generación manuscrito multi-formato |
| `publication_peer_review.py` | 7 | Revisión cruzada multi-modelo |
| `check_manuscript_integrity.py` | 7 | Auditoría de integridad del manuscrito |
| `build_revision_roadmap.py` | 7 | Matriz de cambios accionables |
| `publication_gate.py` | 7 | Validación de artefactos + gate |
| `publication_autopilot.py` | 7-8 | Bucle de reiteración |
| `sync_review_to_obsidian.py` | 8 | Sincronización vault Obsidian |

---

## Estructura de directorios de una revisión

```
review-project/
├── protocol/
│   ├── intake.md
│   ├── eligibility-criteria.md
│   └── search-strategy.md
├── searches/
│   └── search-log.csv
├── records/
│   ├── master-records.csv
│   ├── doi-index.csv
│   ├── duplicates.csv
│   └── missing-doi.csv
├── screening/
│   └── screening-decisions.csv
├── extraction/
│   └── extraction-table.csv
├── figures/
│   ├── extracted/
│   ├── page-renders/
│   ├── manifest.csv
│   ├── figure-catalog.md
│   └── figure-ranking.csv
├── paper/
│   ├── manuscript/
│   │   ├── publication-ready.md
│   │   ├── publication-ready.tex
│   │   └── publication-ready.pdf
│   ├── references/
│   │   └── references.generated.bib
│   ├── review/
│   │   ├── review-manifest.csv
│   │   ├── peer-review-overview.md
│   │   └── reviewer-A/
│   └── package/
│       ├── publication-package.zip
│       └── publication-latex-editable.zip
├── notes/
│   ├── runtime-state.md
│   └── runtime-state.json
└── main-common-core.tex
```

---

## Casos de uso interesantes

### 1. Revisión rápida de estado del arte
- Intake automatizado → búsqueda multi-fuente → screening → extracción superficial → manuscrito borrador
- Útil para: tesis, propuestas de investigación, state-of-the-art sections

### 2. Revisión completa para publicación
- Pipeline completo con gate editorial y paquete LaTeX
- Útil para: journals, congresos, revisiones Cochrane-style

### 3. Auditoría de revisiones existentes
- Cargar una revisión hecha → ejecutar DOI audit + integrity check
- Útil para: peer reviewers, editores, revisión de calidad

### 4. Monitor de literatura continua
- Watchdog re-ejecuta búsqueda periódicamente
- Detecta nuevos papers relevantes
- Útil para: laboratorios, grupos de investigación activos

### 5. Generación de protocolos para comités de ética
- Solo la Fase 1 (intake + criteria + search strategy)
- Genera protocolo PRISMA-compliant para presentar a comités

### 6. Enseñanza de metodología
- El sistema como ejemplo vivo de cómo funciona PRISMA 2020
- Estudiantes pueden auditar cada fase, cada decisión
- Material didáctico interactivo

---

## Referencias bibliográficas del sistema

- Page et al. 2021 (BMJ n71) — PRISMA 2020
- Page et al. 2021 (BMJ n160) — PRISMA 2020 Elaboración
- Rethlefsen et al. 2021 (PRISMA-S)
- Cochrane Handbook ch. 4
- Kitchenham et al. 2009 — SLRs en Software Engineering
- Whiting et al. 2016 — ROBIS
- Shea et al. 2017 — AMSTAR 2
- Wilkinson et al. 2016 — FAIR
- Wohlin 2014 — Snowballing Guidelines
- ACM — Artifact Review and Badging

---

## Pitfalls conocidos

1. **Sesgo nace en intake** — si la pregunta es ambigua, el resto automatiza ambigüedad
2. **Resumen no basta** — exigir texto completo para inclusión final
3. **Conteos manuales** — siempre recomputar desde decisiones canonizadas
4. **Modelo único para revisión** — usar mínimo 2 modelos para cruzar
5. **Sin watchdog** — revisiones largas se estancan sin reanudación
6. **Mezclar figuras propias y ajenas** — usar firma hexadecimal para distinguir
7. **Memoria en chat** — la continuidad depende de archivos, no de "recordar"
8. **generic-common-core** — si no hay revista, no fingir alineación
9. **Recursividad** — buildSummary() recursivo causa OOM
10. **Sin gate** — entregar "algo que parece terminado" sin controles

---

## Checklist de implementación

- [ ] Docker compose con 2 servicios (agent + watchdog)
- [ ] Config.yaml con política de modelos completa
- [ ] 10 skills de investigación en hermes-home/skills/research/
- [ ] Scripts: bootstrap, doi_audit, complete_review, runtime_state
- [ ] Scripts: refresh_extraction, prepare_figures, publication_audit
- [ ] Scripts: peer_review, integrity, roadmap, gate, autopilot
- [ ] Scripts: sync_to_obsidian
- [ ] Watchdog configurado y activo
- [ ] Telegram como superficie operativa
- [ ] Protocolo de 3 archivos (intake, criteria, search)
- [ ] Extracción de 4 bloques (núcleo, empírico, técnico, teoría)
- [ ] Gate editorial con PASS/FAIL real
- [ ] Paquetes ZIP generados
- [ ] Sincronización Obsidian funcional