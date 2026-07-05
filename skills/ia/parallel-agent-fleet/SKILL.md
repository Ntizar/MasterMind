---
name: parallel-agent-fleet
version: "1.0.0"
description: "Flota de agentes paralelos con Orca — ADE (Agent Development Environment) para ejecutar múltiples coding agents en paralelo. Inspirado en stablyai/orca (⭐12K)."
tags: [agents, parallel, fleet, orchestration, coding, automation]
---

# Flota de Agentes Paralelos

## Resumen

[Orca](https://github.com/stablyai/orca) (⭐12K) es un ADE (Agent Development Environment) para trabajar con flotas de agentes en paralelo. Ejecuta cualquier coding agent (Claude Code, Codex, Aider) en paralelo sobre diferentes tareas.

## Cuándo usar

- Ejecutar múltiples coding agents en paralelo
- Dividir una feature grande en sub-tareas paralelas
- Comparar outputs de diferentes agentes
- CI/CD con agentes que revisan código en paralelo

## Patrón de uso

```bash
# Instalar Orca
npm install -g @stablyai/orca

# Definir flota de agentes
orca init --fleet my-fleet

# config.orca.yaml
fleet:
  agents:
    - name: frontend-agent
      type: claude-code
      task: "Implementar UI del dashboard con React"
      workspace: ./frontend
    - name: backend-agent
      type: codex
      task: "Crear API REST con Express"
      workspace: ./backend
    - name: test-agent
      type: aider
      task: "Escribir tests para el backend"
      workspace: ./backend

# Ejecutar flota en paralelo
orca run my-fleet
```

```javascript
// API programática
import { Orca } from '@stablyai/orca';

const orca = new Orca();

const fleet = await orca.createFleet({
  agents: [
    {
      name: 'reviewer-1',
      type: 'claude-code',
      task: 'Review PR #42 for security issues',
      workspace: './repo'
    },
    {
      name: 'reviewer-2',
      type: 'codex',
      task: 'Review PR #42 for performance issues',
      workspace: './repo'
    }
  ]
});

// Ejecutar en paralelo y recolectar resultados
const results = await fleet.run();
results.forEach(result => {
  console.log(`${result.agent}: ${result.status}`);
  console.log(result.output);
});
```

## Pitfalls

- **Workspace isolation:** Cada agente debe tener su workspace aislado para evitar conflictos.
- **Resource limits:** Cada agente consume API calls. Limitar número de agentes paralelos.
- **Coordination:** Si los agentes necesitan compartir información, usar un shared state o message queue.
- **Error handling:** Si un agente falla, decidir si continuar o abortar toda la flota.
- **Cost:** Múltiples agentes = múltiples API calls. Monitorizar coste.

## Referencias

- Orca: https://github.com/stablyai/orca
- Claude Code: https://github.com/anthropics/claude-code
- Codex: https://github.com/openai/codex

---

**Hecho con ❤️ por David Antizar**
