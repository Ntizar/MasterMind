# 🛡️ Hermes Backup

**Última sincronización:** 2026-06-20

Este directorio contiene el backup completo de todo lo que vive en `/hermes-home/` y que se perdería si la VM de Hermes se cae.

## 📦 Contenido

### `config.yaml` — Configuración de Hermes
- Modelo: qwen3.6 vía NaN.builders
- TTS: Edge (es-ES-AlvaroNeural)
- STT: Local
- Cron jobs, toolsets, gateways, integraciones (Telegram, Discord)
- **200+ líneas de configuración crítica**

### `memories/` — Memoria persistente
- **MEMORY.md** — 9 entradas de contexto de proyectos (wave3, nogal9, timeineco, ChromaDB, etc.)
- **USER.md** — Perfil de David: edad, CSS, TTS, estilo de comunicación
- **INDEX.yaml** — Índice de memoria

### `notes/` — Notas de aprendizaje
- 25 notas de sesiones y auditorías
- 10 notas de deep-learning
- Formato: `YYYY-MM-DD-titulo.md`

### `scripts/` — Scripts de utilidades
- 167 scripts: ChromaDB, deploy, bicimad, esios, control-m, etc.
- Herramientas de backup, re-indexación, monitoring

### `skills/` — Skills (245 archivos SKILL.md)
- Backup de todos los skills de `/hermes-home/skills/`
- Incluye referencias, scripts, templates, workflows
- 244 SKILL.md files + ~1000 archivos totales

### `INDEX.md` — Índice de skills
- Vista global de todos los skills organizados por categoría

### `STEM-INDEX.md` — Índice STEM
- Skills de matemáticas, física, química, biología, ingeniería

## 🔄 Auto-sync

Un cron job ejecuta este backup cada 6 horas:
- `skills-sync-to-github` (job_id: 55f6ed2e2da8)
- Sincroniza config, memories, scripts, skills

## 📊 Estado actual

| Recurso | En Hermes | En GitHub |
|---------|-----------|-----------|
| Skills | 245 | 244 ✅ |
| Config | 1 archivo | 1 ✅ |
| Memories | 3 archivos | 3 ✅ |
| Notas | 25 | 25 ✅ |
| Scripts | 167 | 167 ✅ |
| SOUL.md | 1 | 1 ✅ |

## 🚨 Si Hermes se cae

1. Clonar el repo: `git clone https://github.com/Ntizar/NtizarBrainMasterMind.git`
2. Copiar `hermes-backup/config.yaml` → `/hermes-home/config.yaml`
3. Copiar `hermes-backup/memories/` → `/hermes-home/memories/`
4. Copiar `hermes-backup/skills/` → `/hermes-home/skills/`
5. Copiar `hermes-backup/scripts/` → `/hermes-home/scripts/`
6. Copiar `hermes-backup/notes/` → `/hermes-home/notes/`
7. Reiniciar Hermes

Todo se recupera. Nada se pierde.

---

**Hecho con ❤️ por David Antizar**
