---
name: skillspector
version: "1.0.0"
description: "SkillSpector — scanner de seguridad para skills de agentes IA (Claude Code, Codex, Gemini). 64 patrones de vulnerabilidad en 16 categorías. Dos etapas: análisis estático + LLM semántico. Score 0-100 con severidad."
tags: [security, vulnerability-scanner, ai-agents, skills, claude-code, malware-detection, supply-chain]
---

# SkillSpector — Security Scanner for AI Agent Skills

## Resumen

SkillSpector de NVIDIA es un scanner de seguridad diseñado específicamente para auditar **skills de agentes IA** (Claude Code, Cursor, Codex CLI, Gemini CLI, etc.). Investiga que los skills sean seguros antes de instalarlos.

**Contexto crítico:** investigaciones muestran que 26.1% de skills contienen vulnerabilidades y 5.2% muestran probable intención maliciosa.

## Capacidades

- **Multi-format input:** repos Git, URLs, ZIPs, directorios locales, archivos individuales
- **64 patrones de vulnerabilidad en 16 categorías:**
  1. Prompt injection
  2. Data exfiltration
  3. Privilege escalation
  4. Supply chain attacks
  5. Excessive agency (el skill hace más de lo necesario)
  6. Output handling inseguro
  7. System prompt leakage
  8. Memory poisoning
  9. Tool misuse
  10. Rogue agent patterns
  11. Trigger abuse
  12. Dangerous code (AST analysis)
  13. Taint tracking
  14. YARA signatures
  15. MCP least privilege violations
  16. MCP tool poisoning
- **Dos etapas:** análisis estático rápido + análisis LLM semántico opcional
- **Búsqueda CVE en vivo:** consulta OSV.dev para vulnerabilidades conocidas (fallback offline)
- **Formatos de salida:** terminal, JSON, Markdown, SARIF
- **Risk scoring:** score 0-100 con etiquetas de severidad y recomendaciones

## Instalación

```bash
# Python 3.12+
pip install skillspector
# o con Docker
docker run --rm -v "$PWD:/scan" ghcr.io/nvidia/skillspector scan ./my-skill/ --no-llm
```

## Uso básico

```bash
# Escanear skill local
skillspector scan ./my-skill/

# Escanear con LLM analysis (requiere .env con API key)
cat > .env << 'EOF'
SKILLSPECTOR_PROVIDER=anthropic
ANTHROPIC_API_KEY=tu-clave-aqui
EOF

skillspector scan ./my-skill/ --llm

# Output JSON para integración
skillspector scan ./my-skill/ --format json --output report.json

# Output SARIF para CI/CD
skillspector scan ./my-skill/ --format sarif --output results.sarif
```

## Integración con Mastermind

- **Auditoría de skills nuevos:** antes de instalar cualquier skill externo, escanear con SkillSpector
- **Cron de seguridad:** job recurrente que escanea automáticamente los skills del sistema
- **Quality gate:** en pipeline de creación de skills, agregar `skillspector scan` como verificación pre-commit
- **Integrar con chromadb:** al crear skill desde stars-explorer, ejecutar skillspector automáticamente

## Integración con chromadb-skills-vector-search

Cuando se crea un skill nuevo desde el Stars Explorer, el flujo seguro es:

1. `stars-explorer` analiza el repo
2. `skillspector scan <ruta-skill>` verifica que no haya patrones maliciosos
3. Si pasa el scan, `skill_manage` lo crea y se indexa en ChromaDB
4. Si falla el scan, se marca como `skip` en el registry con la razón de seguridad

## Referencias

- Repo: `NVIDIA/SkillSpector`
- Docs: https://github.com/NVIDIA/SkillSpector
- Docker: `ghcr.io/nvidia/skillspector`
- License: Apache 2.0
- Paper de investigación: https://skillspector.github.io/
