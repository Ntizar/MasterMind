---
name: tts-setup
description: "Configure and troubleshoot Text-to-Speech in Hermes Agent — provider selection, voice discovery, language-specific voices, and config patching."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [tts, voice, text-to-speech, edge-tts, elevenlabs, openai, configuration]
---

# TTS Setup

Configure Text-to-Speech for Hermes Agent. Covers provider selection, voice discovery, language-specific voice lists, and config patching.

## Providers

| Provider | Free? | Env Var | Best For |
|----------|-------|---------|----------|
| **Edge TTS** | Yes (default) | None | Free, many languages/voices |
| **ElevenLabs** | Free tier | `ELEVENLABS_API_KEY` | Highest quality, voice cloning |
| **OpenAI** | Paid | `VOICE_TOOLS_OPENAI_KEY` | Natural voices (alloy, echo, fable, onyx, nova, shimmer) |
| **NeuTTS** | Free (local) | None (`pip install neutts[all]` + `espeak-ng`) | Offline, voice cloning via reference audio |
| **Piper** | Free (local) | None | Lightweight, fast, offline |
| **Mistral** | Paid | `MISTRAL_API_KEY` | |
| **xAI** | Paid | `XAI_API_KEY` | |

## Config Location

```
~/.hermes/config.yaml          # Standard install
/hermes-home/config.yaml       # When HERMES_HOME=/hermes-home
```

Find it with: `hermes config path` or check `get_hermes_home()` in Python.

### TTS Config Structure

```yaml
tts:
  provider: edge          # edge | elevenlabs | openai | xai | minimax | mistral | gemini | neutts | kittentts | piper
  edge:
    voice: es-ES-AlvaroNeural
  elevenlabs:
    voice_id: pNInz6obpgDQGcFmaJgB    # Adam
    model_id: eleven_multilingual_v2
  openai:
    model: gpt-4o-mini-tts
    voice: alloy
  neutts:
    ref_audio: ""
    ref_text: ""
    model: neuphonic/neutts-air-q4-gguf
    device: cpu
  piper:
    voice: en_US-lessac-medium
```

## Voice Discovery

Edge TTS voices are discovered via the Hermes venv Python:

```bash
# List all voices
/opt/hermes/.venv/bin/python -c "
import asyncio, edge_tts
async def main():
    voices = await edge_tts.list_voices()
    for v in sorted(voices, key=lambda x: x['ShortName']):
        print(f\"{v['ShortName']:40s} | {v['Gender']:8s} | {v['FriendlyName']}\")
asyncio.run(main())
"

# Filter by language (e.g., Spanish)
/opt/hermes/.venv/bin/python -c "
import asyncio, edge_tts
async def main():
    voices = await edge_tts.list_voices()
    es = [v for v in voices if v['Locale'].startswith('es-')]
    for v in sorted(es, key=lambda x: (x['Gender'], x['ShortName'])):
        print(f\"{v['ShortName']:40s} | {v['Gender']:8s} | {v['FriendlyName']}\")
asyncio.run(main())
"
```

If `edge_tts` is not installed in the venv:
```bash
uv pip install edge-tts --system -q
```

## Patching the Voice

```bash
# Find the current voice
grep -A 3 "^tts:" /hermes-home/config.yaml | head -5

# Patch it (use the patch tool, not sed)
# Old: voice: en-US-AriaNeural
# New: voice: es-ES-AlvaroNeural
```

## Linked Files

- `references/spanish-voices.md` — Complete list of all 45 Spanish (es-*) Edge TTS voices

## Pitfalls

- **Default voice is `en-US-AriaNeural`** (female, English). Always check what's configured before assuming.
- **Edge TTS CLI (`edge-tts`) may not be in PATH** — use the venv Python directly: `/opt/hermes/.venv/bin/python`
- **`edge_tts.list_voices()` is async** — must be called with `await` inside an `asyncio.run()` context.
- **Voice names are case-sensitive** — use exact `ShortName` from the list (e.g., `es-ES-AlvaroNeural`, not `alvaro`).
- **Config changes require `/reset` or gateway restart** to take effect.