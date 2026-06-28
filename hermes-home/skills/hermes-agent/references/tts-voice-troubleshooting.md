# TTS Voice Troubleshooting

## Diagnosing Voice Issues

**Problem:** User says the voice sounds wrong (wrong gender, wrong language, wrong accent).

**Steps:**
1. Check current config: `~/.hermes/config.yaml` → `tts.provider` and `tts.<provider>.voice`
2. Edge TTS is the default provider (`tts.provider: edge`) with default voice `en-US-AriaNeural` (female, US English).
3. List available voices:
   ```bash
   /opt/hermes/.venv/bin/python -c "
   import asyncio, edge_tts
   async def main():
       voices = await edge_tts.list_voices()
       for v in voices:
           print(f\"{v['ShortName']:40s} | {v['Gender']:8s} | {v['Locale']:6s} | {v['FriendlyName']}\")
   asyncio.run(main())
   ```
4. Filter by locale: `v['Locale'].startswith('es-')` for Spanish, `es-ES` for Spain, etc.
5. Change voice in config: `tts.edge.voice: "es-ES-AlvaroNeural"`

## Edge TTS Spanish Voices Reference

### Spain (es-ES)
| Voice | Gender | Name |
|-------|--------|------|
| `es-ES-AlvaroNeural` | Male | Alvaro |
| `es-ES-ElviraNeural` | Female | Elvira |
| `es-ES-XimenaNeural` | Female | Ximena |

### Mexico (es-MX)
| Voice | Gender | Name |
|-------|--------|------|
| `es-MX-JorgeNeural` | Male | Jorge |
| `es-MX-DaliaNeural` | Female | Dalia |

### Argentina (es-AR)
| Voice | Gender | Name |
|-------|--------|------|
| `es-AR-TomasNeural` | Male | Tomas |
| `es-AR-ElenaNeural` | Female | Elena |

### Colombia (es-CO)
| Voice | Gender | Name |
|-------|--------|------|
| `es-CO-GonzaloNeural` | Male | Gonzalo |
| `es-CO-SalomeNeural` | Female | Salome |

> Full list: 45 Spanish voices total (22 male, 23 female) across 20+ Latin American and Spanish locales.

## Common Pitfalls

- **Default Edge TTS voice is female English** (`en-US-AriaNeural`). If user wants Spanish or male voice, it must be explicitly configured.
- **`edge-tts` CLI may not be installed** even if the Python package is. Use the venv Python directly: `/opt/hermes/.venv/bin/python`.
- **Voice changes require a new session** (`/reset` in chat) to take effect — config is snapshotted at startup.
- **Edge TTS is free** but rate-limited. For production use, consider ElevenLabs or OpenAI.
