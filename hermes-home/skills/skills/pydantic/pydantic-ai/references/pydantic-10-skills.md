# Referencia Pydantic AI — 10 Skills de Programación

Extraído de https://pydantic.dev/docs/ai/overview/ y subpáginas (core concepts, tools, dependencies, output, testing).

## Resumen Visual

```
┌─────────────────────────────────────────────────────────────────┐
│              10 Skills Pydantic AI — Resumen                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🏗️  ARQUITECTURA                                               │
│  1. Type-Safe by Design        → Type hints + Pydantic          │
│  2. Dependency Injection       → Dataclasses + RunContext       │
│  3. Structured Outputs         → BaseModel como output_type     │
│                                                                 │
│  🔧  HERRAMIENTAS                                               │
│  4. Function Tools             → @tool + @tool_plain           │
│  5. Dynamic Instructions       → @agent.instructions           │
│  6. Composable Capabilities    → Thinking, WebSearch, MCP      │
│                                                                 │
│  🧪  TESTING                                                     │
│  7. TestModel/FunctionModel    → Sin llamadas LLM reales        │
│  8. Agent Override             → Inyección en runtime           │
│                                                                 │
│  ⚡  AVANZADO                                                    │
│  9. Streaming                  → Validación en tiempo real      │
│  10. Model-Agnostic            → 20+ proveedores soportados     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
