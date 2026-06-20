# Skill-Priority Reconciliation

Procedimiento para reconciliar `config/skill-priority.json` con las skills reales en `/hermes-home/skills/`.

## Cuándo ejecutar

- Cuando el usuario reporta que hay skills faltantes o stale en el priority JSON
- Después de crear/eliminar múltiples skills
- Cuando el conteo de skills en el JSON difiere significativamente del filesystem
- Como parte de la auditoría mensual de skills

## Pasos

### 1. Obtener conteo real

```bash
find /hermes-home/skills -name 'SKILL.md' -not -path '*/.git/*' | wc -l
```

### 2. Listar todas las skills del filesystem

```bash
find /hermes-home/skills -name 'SKILL.md' -not -path '*/.git/*' -exec dirname {} \; | sort | while read dir; do basename "$dir"; done
```

### 3. Comparar con el JSON (Python)

Usar `execute_code` con un script que:
1. Lea `config/skill-priority.json` y extraiga todas las skills de HIGH/MEDIUM/LOW
2. Compare con la lista del filesystem
3. Identifique **stale** (en JSON pero no en filesystem)
4. Identifique **missing** (en filesystem pero no en JSON)
5. Identifique **en común**

### 4. Regenerar el JSON

Categorización recomendada:

**HIGH (core):**
- Mastermind propio: `mastermind`, `mastermind-setup`, `mastermind-orchestration`
- Hermes: `hermes-agent`
- ESIOS: `esios-complete`, `esios-indicators-correct`, `esios-nan-deploy`, `esios-telegram-report`
- ChromaDB: `chromadb-skills-vector-search`
- DevOps/infra: `devops-operations`, `docker-management`, `static-digest-pipeline`, `node-esm-interop`, `github-workflow`, `infraestructura`
- Frontend core: `frontend-dashboard-patterns`, `aurora-design-system`, `liquid-glass-css`, `popular-web-designs`
- Tools: `system-audit`, `systematic-debugging`, `google-eng-practices`, `writing-plans`, `9009-multi-iteration`, `delegar-no-comprimir`, `subagent-driven-development`, `native-mcp`, `agent-memory`, `humanizer`
- Documentos: `documentos-institucionales`
- Diagramas: `architecture-diagram`, `excalidraw`, `sketch`, `claude-design`

**MEDIUM (dominio específico):**
- Creative: ascii-art, ascii-video, pixel-art, manim-video, p5js, baoyu-comic, baoyu-infographic, design-md, creative-ideation, pretext, threejs-3d-web, webapp-viral-rapida, madrid-visualization, render-3d-isometrico-ciudad, touchdesigner-mcp
- Video/media: agentic-video-pipeline, video-processing-pipeline, pdf-to-artifacts-david-antizar, markitdown, liteparse-rust-pdf-ocr
- Research: web-research-fallback, github-trending-research, competitive-intelligence, duckduckgo-search, searxng-search
- Audio: heartmula, songwriting-and-ai-music, songsee, tts-setup, voicebox
- Satellite: satellite-ai-vision, satellite-gis-patterns, satellite-traffic-detection
- ML/LLM tools: pydantic-ai, llm-model-selection
- Testing: testing, testing-jest-mocks-api, test-driven-development, requesting-code-review, codebase-inspection
- Y todo lo que no sea HIGH ni STEM/nicho

**LOW (nicho/educativo):**
- STEM: stem-*, math-*, physics-*, td-*
- MLOps nicho: lm-evaluation-harness, weights-and-biases, vllm, mlx-vlm-inference, audiocraft, segment-anything, dspy
- Red teaming: godmode, obliteratus
- Apple ecosystem: apple-calendar, apple-notes, apple-reminders, findmy, imessage, macos-computer-use
- Delegación: claude-code, codex, opencode
- Research papers: research-paper-writing, llm-wiki, prisma-systematic-review
- Otros nicho: yuanbao, fastmcp, diet/dieta

### 5. Actualizar note

La note debe reflejar que **ChromaDB es la fuente de verdad** para relevancia de skills. El JSON es solo un fallback estático.

### 6. Commit y push

```bash
cd /root/workspace/Mastermind && git add -A && git commit -m "fix: consolidar skill-priority.json con X skills reales" && git push
```

## Ejemplo real (2026-06-10)

- Antes: 141 skills en JSON (34 stale, 85 missing)
- Después: 192 skills (0 stale, 0 missing)
- Distribución: HIGH 34, MEDIUM 86, LOW 72
- Version actualizada: 1.0.0 → 2.0.0

## Pitfalls

- **Duplicados en JSON:** El JSON puede tener el mismo skill en múltiples niveles (ej: `nango` aparecía en MEDIUM y LOW). Eliminar duplicados.
- **Nombres de directorio vs frontmatter:** Algunos skills tienen nombre de directorio diferente al frontmatter `name:`. Comparar con nombres de directorio (find) vs nombres del JSON.
- **Skills en múltiples categorías:** El JSON puede tener skills duplicados entre HIGH, MEDIUM y LOW. La regeneración debe usar `set` para eliminar duplicados.
- **Coverage total:** Después de regenerar, verificar que `len(HIGH) + len(MEDIUM) + len(LOW) == count de SKILL.md en filesystem`.
