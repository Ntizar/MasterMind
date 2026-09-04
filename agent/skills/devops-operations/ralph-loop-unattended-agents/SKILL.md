---
name: ralph-loop-unattended-agents
version: "1.0.0"
description: "Loop que relanza un CLI de IA para runs desatendidos."
tags: [ai-agent, loop, bash, powershell, codex, claude, gemini, devin]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [ai-agent, loop, bash, cli]
    related_skills: [codex, claude-code, opencode, batch-cron-jobs]
---
# ralph — Loop de Agentes IA Desatendido

## Resumen
Herramienta de developer, open source por **Santander AI Lab**, sin dependencias (Bash/PowerShell). Ejecuta un CLI de IA / agente LLM en bucle, lanzando **una sesión de agente completamente nueva en cada iteración** para ejecuciones largas y desatendidas. Envuelve (wrapper delgado `ralph-loop.sh`) CLIs ya instalados: **Codex**, **Claude Code**, **Gemini CLI** y **Devin CLI**. Técnica "Ralph Wiggum": repetir el mismo prompt contra un agente limpio, dejando que el trabajo se acumule en el repo entre corridas.

## Instalación (comandos reales)
```sh
# Instalador sin dependencias (solo curl y tar); copia ralph-loop.sh a ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/SantanderAI/ralph/main/install.sh | sh
# Opciones: --no-skills, --ref, --repo, --install-dir (o vars RALPH_SKIP_SKILLS, RALPH_REF, RALPH_REPO, RALPH_INSTALL_DIR)
curl -fsSL https://raw.githubusercontent.com/SantanderAI/ralph/main/install.sh | sh -s -- --no-skills

# Windows / PowerShell (pwsh 6+): instala ralph-loop.ps1
powershell -c "irm https://raw.githubusercontent.com/SantanderAI/ralph/main/install.ps1 | iex"
```

## Requisitos
- Bash.
- Al menos uno de estos CLIs en `PATH`: `codex`, `claude`, `gemini`, `devin`.
- Opcional: `just` para la receta de instalación.

## Patrones / Arquitectura
Cada iteración el script:
1. Comprueba una señal de parada (`stop.md`) y sale limpiamente si está presente.
2. Recarga la configuración (live reload).
3. Lanza el CLI seleccionado como sesión nueva con el prompt canalizado, en el directorio donde se invocó el script.
4. Escribe un log con timestamp en `.ralph/logs/` y rota logs antiguos.

## Pitfalls
- Como cada iteración es una sesión nueva, **toda la continuidad debe vivirse en el workspace**: los archivos que edita el agente, un plan, notas, etc.
- El prompt debe pedir al agente leer ese estado y avanzar incrementalmente.
- Requiere que el CLI de IA esté autenticado/accesible en `PATH`; `stop.md` es el mecanismo de parada.

## Verificación
- `ralph-loop.sh` relanza el agente en bucle; crear `stop.md` debe abortar limpiamente.

## Referencia
- Repo: https://github.com/SantanderAI/ralph (Licencia Apache 2.0). Parte de Santander AI Open Source.
