---
name: pydantic-ai
description: "Framework completo de agentes GenAI para Python: fundamentos (agentes, tipos, validación), patrones de producción (DI, structured outputs, testing, streaming), sistema de tools, y 10 skills de programación fundamentales. Todo de Pydantic AI docs."
version: 2.0.0
author: Hermes Agent
tags: [pydantic, ai, python, agent, testing, streaming, structured-output, tools, dependency-injection]
---

# Pydantic AI — Guía Completa

Framework de agentes GenAI para Python que lleva la ergonomía de FastAPI al desarrollo con IA generativa.

## Tabla de Contenidos

1. [Fundamentos](#1-fundamentos) — Agentes básicos, tipos, validación, Hello World
2. [Tools y Dependency Injection](#2-tools-y-dependency-injection) — @agent.tool, @agent.tool_plain, RunContext
3. [Patrones de Producción](#3-patrones-de-producción) — Testing, streaming, capabilities, override
4. [10 Skills de Programación](#4-10-skills-de-programación) — Type-safe, DI, structured outputs, tools, streaming, model-agnostic

---

## 1. Fundamentos

**Agentes básicos:**
```python
from pydantic_ai import Agent
agent = Agent('openai:gpt-4o', system_prompt='Eres un asistente útil.')
result = agent.run_sync('¿Qué tiempo hace en Madrid?')
print(result.data)
```

**Validación con Pydantic:**
```python
from pydantic import BaseModel
class Tiempo(BaseModel):
    ciudad: str
    temperatura: float
agent = Agent('openai:gpt-4o', output_type=Tiempo)
result = agent.run_sync('¿Qué tiempo hace en Madrid?')
# result.data es una instancia validada de Tiempo
```

**Concepto clave:** Agent = LLM + System Prompt + Tools + Output Schema. Todo tipado.

---

## 2. Tools y Dependency Injection

**Tool básico:**
```python
@agent.tool
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b
```

**Tool con contexto (DI):**
```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class AppDeps:
    db: Database

agent = Agent('openai:gpt-4o', deps_type=AppDeps)

@agent.tool
def buscar(query: str, ctx: RunContext[AppDeps]) -> list:
    """Busca en la base de datos."""
    return ctx.deps.db.query(query)
```

**Reglas:**
- `@agent.tool` → necesita `RunContext[Deps]` como primer parámetro
- `@agent.tool_plain` → sin contexto
- `ctx.deps` para acceder a dependencias
- Preferir `async def` (las sync se ejecutan en thread pool)
- La docstring es la descripción que ve el LLM

---

## 3. Patrones de Producción

**Structured Outputs:**
```python
class SupportOutput(BaseModel):
    advice: str = Field(description='Advice returned to customer')
    risk: int = Field(description='Risk level', ge=0, le=10)

agent = Agent('openai:gpt-4o', output_type=SupportOutput)
```

**Testing con TestModel/FunctionModel:**
```python
from pydantic_ai import TestModel
with agent.override(model=TestModel()):
    result = agent.run_sync("test")
# Para tests custom:
from pydantic_ai import FunctionModel
agent = Agent('openai:gpt-4o', model=FunctionModel(my_model_fn))
```

**Streaming:**
```python
async with agent.run_stream('query') as result:
    print(result.output)  # output parcial en tiempo real
```

**Dynamic Instructions:**
```python
@agent.instructions
async def add_context(ctx: RunContext[Deps]) -> str:
    return f"Customer: {await ctx.deps.db.name(id=ctx.deps.customer_id)}"
```

**Capabilities:**
```python
from pydantic_ai.capabilities import Thinking, WebSearch
agent = Agent('anthropic:claude-sonnet-4-6', capabilities=[Thinking(), WebSearch(...)])
```

**Agent Override (producción):**
```python
with agent.override(model='openai:gpt-5.2' if prod else 'ollama:llama3'):
    result = await agent.run("query")
```

---

## 4. 10 Skills de Programación

1. **Type-Safe by Design** — Type hints mueven errores de runtime a write-time
2. **Dependency Injection con Dataclasses** — `RunContext[DepsType]` como primer parámetro
3. **Structured Outputs con BaseModel** — Fuerza al LLM a devolver datos estructurados
4. **Function Tools** — `@agent.tool` y `@agent.tool_plain`
5. **Dynamic Instructions** — Inyectar contexto dinámico en runtime
6. **Composable Capabilities** — Bundles reutilizables (Thinking, WebSearch, MCP)
7. **TestModel/FunctionModel** — Tests sin llamadas LLM reales
8. **Agent Override** — Reemplazar modelo/deps en runtime sin modificar el agente
9. **Streaming con Validación** — `run_stream()` para outputs estructurados en tiempo real
10. **Model-Agnostic** — 20+ proveedores, solo cambias `'provider:model-name'`

---

## ⚠️ Pitfalls

- **No confundir** `run_sync` (bloqueante) con `run` (async)
- **TestModel no emula native tools** — sobrescribe con `Agent.override()` en tests
- **Funciones sync en tools** se ejecutan en thread pool → preferir `async def`
- **`ALLOW_MODEL_REQUESTS=False`** es global → úsalo en tests
- **Dependencias son dataclasses** — no objetos arbitrarios sin tipado
- **Pydantic v2 strict validation** — `list[float]` NO acepta `list[list[float]]`