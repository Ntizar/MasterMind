# Supermemory - Detalles de Integracion

**URL:** https://github.com/supermemoryai/supermemory  
**Estrellas:** ~24k | **Creado:** 2024-02-27  
**Benchmarks:** #1 en LongMemEval, LoCoMo, ConvoMem

## Instalacion

```bash
npm install supermemory
pip install supermemory
```

## API Key
Crear cuenta en https://console.supermemory.ai para obtener API key.

## Endpoints Clave

### extract()
Extrae facts de una conversacion. Aprende automaticamente:
- Preferencias del usuario
- Hechos relevantes
- Contexto de tareas

### getProfile(userId)
Obtiene perfil de usuario completo en ~50ms. Incluye:
- Facts estables (preferencias, rol, habilidades)
- Actividad reciente
- Contexto actual

### search(query, {memory, knowledge})
Busqueda hibrida que combina:
- Documents del knowledge base (RAG)
- Memory personal del usuario

## Conectores Disponibles
- Google Drive
- Gmail
- Notion
- OneDrive
- GitHub

Todos con auto-sync via webhooks en tiempo real.

## Multi-modal Extractors
- **PDFs** — Extraccion de texto y estructura
- **Imágenes** — OCR integrado
- **Videos** — Transcripcion automatica
- **Codigo** — AST-aware chunking (conoce la estructura del codigo)

## Infraestructura
- Cloudflare Workers (serverless)
- Cloudflare KV (almacenamiento)
- Cloudflare Pages (dashboard)
- Drizzle ORM + PostgreSQL

## Notas de Integracion
- SDK auto-contenido, no requiere Node.js runtime propio
- API REST + SDKs Python/TypeScript
- Ideal para agentes que necesitan memoria persistente entre sesiones
- El dashboard web permite gestionar memoria manualmente