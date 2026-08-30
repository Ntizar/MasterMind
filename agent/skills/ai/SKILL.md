---
name: ai-agent-sandbox-runtime
version: "1.0.0"
description: "Use al ejecutar código de agentes IA en sandboxes seguros."
tags: [sandbox, ai-agents, kubernetes, seguridad, runtime, infraestructura]
related_skills: [layered-agent-architecture, native-mcp, hermes-agent]
---

# OpenSandbox — Runtime de Sandbox para Agentes IA

Fuente: https://github.com/opensandbox-group/OpenSandbox (14.8k⭐, Go, Apache-2.0, CNCF Landscape, activo 2026).

## Qué es

Runtime seguro, rápido y extensible para ejecutar código generado por agentes IA. Alternativa self-hosted a E2B/Modal. Escrito en Go, desplegable en Kubernetes.

## Cuándo usarlo

- Un agente LLM genera código que hay que ejecutar sin arriesgar el host (Hermes, Claude, etc.)
- Ejecución multitenant de código no confiable
- Entornos efímeros con lifetime corto (destrucción tras cada sesión)

## Patrones clave

1. **Aislamiento por defecto** — cada sandbox es una unidad aislada a nivel kernel (seccomp/microVM), no un contenedor compartido.
2. **API de ciclo de vida** — crear → ejecutar → streaming de salida → destruir. El sandbox es efímero y desechable.
3. **Gateway único** — un plano de control expone API HTTP/gRPC; los sandboxes corren en nodos Kubernetes orquestados.
4. **Extensible por runtime** — se puede correr Python, Node, o binarios custom definiendo un runtime.
5. **Manifiestos YAML** — configuración declarativa de los sandboxes (recursos, red, timeouts).

## Arquitectura de referencia

```
Agente IA → API Gateway (control plane) → Scheduler K8s → Sandbox pod (aislado)
                                                ↓
                                    Streaming de salida → agente
```

## Integración con Mastermind

- Para cualquier tool de ejecución de código de agentes (como `execute_code`) en producción multiusuario, usar un sandbox en lugar del host.
- La ejecución local (Hermes en PC de David) no necesita sandbox; solo cuando el código no es confiable o es multitenant.

## Pitfalls

- No confundir con contenedores Docker normales: el aislamiento es a nivel kernel (seccomp/microVM).
- Requiere Kubernetes para despliegue real; para prototipos locales, alternativas más ligeras (nsjail, firejail) pueden bastar.
- Los sandboxes efímeros pierden estado al destruirse — persistir artefactos ANTES de matar el sandbox.

## Verificación

- Repo activo (push 2026-08-28), licencia Apache-2.0.
- Docs y logo en `docs/public/` del repo; e2e tests en GitHub Actions (`real-e2e.yml`).

Hecho con ❤️ por David Antizar
