# Santander AI Lab — Repositorios Relevantes

## Contexto
David tiene 11 repos de `SantanderAI` en sus stars de GitHub. Todos son open-source (Apache 2.0) y del equipo de IA del Banco Santander.

## Los 11 repos

| Repo | Stars | Lenguaje | Descripción | Relevancia para Ineco |
|------|-------|----------|-------------|----------------------|
| `SantanderAI/gen-fraud-graph` | 132 | Python | Generador de grafos sintéticos de fraude con embeddings | 🔴 ALTA — Grafos aplicables a redes de transporte |
| `SantanderAI/ralph` | 49 | PowerShell | Loop de agentes de coding (Claude Code, Codex, Gemini) | 🟡 Media — Más para desarrollo |
| `SantanderAI/ralph-vault-skill` | 41 | Python | Knowledge vault para proyectos con Ralph | 🟡 Media — Documentación automática |
| `SantanderAI/llm_bridge` | 41 | Python | Cliente LLM vendor-neutral (OpenAI, Bedrock, Gemini) | 🟡 Media — Multi-proveedor LLM |
| `SantanderAI/auto-bayesian` | 24 | Python | Redes Bayesianas interpretables para AutoML | 🔴 ALTA — Predicción interpretable para datos tabulares |
| `SantanderAI/sota-stressed-datasets` | 22 | HTML | Benchmarks de datasets estresados para evaluar robustez ML | 🟢 Baja — Testing de modelos |
| `SantanderAI/autoguardrails` | 65 | Python | Guardrails para LLMs (AI safety) | 🟢 Baja — Seguridad LLM |
| `SantanderAI/mech-gov-framework` | 36 | Python | Gobernanza mecánica para decisiones LLM | 🟢 Baja — Gobernanza IA |
| `SantanderAI/causal-perception-implementation` | 17 | Python | Inferencia causal con SCMs | 🟡 Media — Análisis de impacto causal |
| `SantanderAI/mutatis-mutandis` | 13 | Python | Detección de discriminación algorítmica | 🟢 Baja — Fairness IA |
| `SantanderAI/linear-adapter-trainer` | 15 | Python | Ajuste de embeddings para RAG sin re-indexar | 🔴 ALTA — Mejora búsqueda en documentación |

## Top 3 para Ineco

### 1. gen-fraud-graph (132⭐)
- Genera grafos masivos (1K-100M+ nodos) con patrones de fraude inyectados
- Output CSV listo para Neo4j, TigerGraph, Neptune, JanusGraph
- Embeddings opcionales (fake, SentenceTransformers, OpenAI)
- **Aplicación Ineco:** Grafos sintéticos de redes de transporte (rutas, conexiones, flujos) para benchmarkear GNNs en detección de anomalías

### 2. linear-adapter-trainer (15⭐)
- Fine-tunea embeddings de consultas SIN re-indexar el corpus
- Genera triplets automáticamente con negative mining
- Mejoras de +19% en precision@1
- **Aplicación Ineco:** Mejorar RAG sobre documentación técnica (normativas, informes) sin re-indexar

### 3. auto-bayesian (24⭐)
- Redes Bayesianas interpretables desde datos tabulares relacionales
- Output 100% legible: `P(Variable | Condiciones) = Valor`
- Diagrama Mermaid de la red aprendida
- **Aplicación Ineco:** Predicción interpretable para datos de transporte (afluencia, incidencias, mantenimiento)

## Notas técnicas
- Todos Apache 2.0 — libres de usar
- Todos Python (excepto ralph en PowerShell y sota-stressed-datasets en HTML)
- Todos actualizados junio 2026
- READMEs completos y bien documentados
- CI/CD activo en la mayoría
