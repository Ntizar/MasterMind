---
name: voicebox-estudio-voz-local
description: "Patrón de estudio de voz AI local-first: TTS multi-motor, clonación de voz zero-shot, dictado global, servidor MCP y REST API. Competidor local de ElevenLabs."
version: 2.0.0
author: Ntizar + Mastermind
---

# Voicebox — Estudio de Voz AI Local

Plataforma open-source de voz AI que funciona 100% local: 7 motores TTS, clonación zero-shot, dictado global por teclado, servidor MCP y API REST. (28K⭐)

## Arquitectura

```
┌─────────────────────────────────────┐
│         Voicebox Studio             │
│  (Tauri + React + Rust backend)     │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────┐  ┌──────────────────┐  │
│  │ TTS     │  │ Clonación Voz    │  │
│  │ • Edge  │  │ • Zero-shot      │  │
│  │ • Coqui │  │ • Fine-tune      │  │
│  │ • Piper │  │ • Qwen3-TTS      │  │
│  │ • XTTS  │  │                  │  │
│  │ • Melo  │  └──────────────────┘  │
│  │ • Kokoro│                         │
│  │ • Qwen3 │  ┌──────────────────┐  │
│  └─────────┘  │ MCP Server       │  │
│               │ /tools → TTS      │  │
│  ┌─────────┐  │ REST API          │  │
│  │ Dictado │  │ GET /api/voices   │  │
│  │ Global  │  │ POST /api/tts     │  │
│  │(tecla)  │  └──────────────────┘  │
│  └─────────┘                         │
└─────────────────────────────────────┘
```

## Instalación

```bash
# Opción 1: Binario (recomendada)
# Descargar de releases en GitHub

# Opción 2: Desde código
git clone https://github.com/jamiepine/voicebox
cd voicebox && bun install && bun run dev
```

## Patrón: TTS multi-motor via API REST

```javascript
// Sintetizar texto con voz específica
async function textToSpeech(text, voice = 'alvaro', engine = 'edge') {
  const resp = await fetch('http://localhost:3000/api/tts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      voice,
      engine,  // 'edge', 'coqui', 'piper', 'xtts', 'qwen3'
      outputFormat: 'mp3',
      speed: 1.0,
    }),
  });
  const blob = await resp.blob();
  return blob; // Audio MP3
}

// Listar voces disponibles
async function getVoices() {
  const resp = await fetch('http://localhost:3000/api/voices');
  return resp.json();
}
// → [{id: 'alvaro', engine: 'edge', language: 'es-ES'}, ...]
```

## Patrón: Clonación de voz zero-shot

```javascript
// Clonar voz desde audio de muestra (3 segundos mínimo)
async function cloneVoice(samplePath, name) {
  const form = new FormData();
  form.append('audio', fs.createReadStream(samplePath));
  form.append('name', name);

  const resp = await fetch('http://localhost:3000/api/voices/clone', {
    method: 'POST',
    body: form,
  });
  const voice = await resp.json();
  // → { id: 'mi-voz-clonada', status: 'ready' }
}

// Usar la voz clonada
const audio = await textToSpeech('Hola, soy una voz clonada', 'mi-voz-clonada', 'xtts');
```

## Patrón: MCP Server

```yaml
# config.yaml de Hermes
tools:
  mcp_servers:
    voicebox:
      transport: http
      url: http://localhost:3000/mcp
```

Esto permite que Mastermind hable directamente:

```
Mastermind: "Dime en voz alta el resumen del mercado eléctrico"
→ Mastermind llama a voicebox_mcp.tts({text: "...", voice: "alvaro"})
→ 🔊 Audio reproducido
```

## Motores TTS disponibles

| Motor | Voz | Latencia | Calidad | Idiomas |
|-------|-----|----------|---------|---------|
| Edge TTS | Álvaro, Jorge, Paulina | <1s | Excelente | 100+ |
| Coqui TTS | XTTS v2 | ~2s | Muy buena | 17 |
| Piper | Varias | <0.5s | Buena | 20+ |
| XTTS | Personalizada | ~3s | Excelente (clonación) | 17 |
| Qwen3-TTS | Qwen | ~2s | Excelente | CN, EN |
| Kokoro | Kokoro | <0.5s | Buena | EN, JP, KO, CN |
| Melo TTS | Melo | <1s | Buena | EN, ES, FR, JP, KR, CN |

## Buenas prácticas

1. **Edge TTS para español** — Álvaro (es-ES-AlvaroNeural) es la voz más natural
2. **XTTS para clonación** — con 3-10 segundos de muestra es suficiente
3. **MCP para integración con agentes** — sin MCP, el agente no puede producir audio
4. **Dictado global con tecla configurable** — mapear a Ctrl+Mayús+D
5. **Audio chunks en streaming** — mejor latencia percibida que esperar el audio completo

## Pitfalls

- ❌ Clonación con audio de baja calidad → voz robótica
- ❌ Sin MCP configurado → el agente no sabe que puede hablar
- ❌ Edge TTS requiere internet (es API cloud) — los otros son 100% locales
- ❌ Qwen3-TTS necesita GPU (MLX) en Mac — en CPU es muy lento
- ❌ Dictado global puede interferir con atajos de otras apps

## Referencia

- Repo: https://github.com/jamiepine/voicebox (28K⭐)
- Web: https://voicebox.co
- Skills relacionadas: frontend-fechas-timezone-local, frontend-orquestacion-carga