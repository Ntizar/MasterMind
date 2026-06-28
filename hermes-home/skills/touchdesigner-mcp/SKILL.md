---
name: touchdesigner-mcp
description: "Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools."
version: 1.1.0
author: kshitijk4poor
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [TouchDesigner, MCP, twozero, creative-coding, real-time-visuals, generative-art, audio-reactive, VJ, installation, GLSL]
    related_skills: [native-mcp, ascii-video, manim-video, hermes-video]

---

# TouchDesigner Integration (twozero MCP)

## CRITICAL RULES

1. **NEVER guess parameter names.** Call `td_get_par_info` for the op type FIRST. Your training data is wrong for TD 2025.32.
2. **If `tdAttributeError` fires, STOP.** Call `td_get_operator_info` on the failing node before continuing.
3. **NEVER hardcode absolute paths** in script callbacks. Use `me.parent()` / `scriptOp.parent()`.
4. **Prefer native MCP tools over td_execute_python.** Use `td_create_operator`, `td_set_operator_pars`, `td_get_errors` etc. Only fall back to `td_execute_python` for complex multi-step logic.
5. **Call `td_get_hints` before building.** It returns patterns specific to the op type you're working with.

## Cuándo usar

- Quieres crear visuales en tiempo real con TouchDesigner controlados por código
- Necesitas construir redes de nodos (TOP/CHOP/SOP) programáticamente
- Buscas generar arte generativo, visuales audio-reactivos, o instalaciones interactivas
- Quieres controlar TouchDesigner de forma automatizada desde Hermes Agent

## Cuándo NO usar

- Solo necesitas generar una imagen estática → usa `comfyui` o `ascii-art`
- Quieres animaciones 2D/3D para vídeo educativo → usa `manim-video` o `p5js`
- No tienes TouchDesigner instalado o no tienes una instancia corriendo → este skill solo controla TD existente

## Architecture

```
Hermes Agent -> MCP (Streamable HTTP) -> twozero.tox (port 40404) -> TD Python
```

36 native tools. Free plugin (no payment/license — confirmed April 2026).
Context-aware (knows selected OP, current network).
Hub health check: `GET http://localhost:40404/mcp` returns JSON with instance PID, project name, TD version.

## Setup (Automated)

Run: `bash "${HERMES_HOME:-$HOME/.hermes}/skills/creative/touchdesigner-mcp/scripts/setup.sh"`

The script: checks if TD is running, downloads twozero.tox, adds MCP server to Hermes config, tests connection on port 40404, reports manual steps.

### Manual steps (one-time)
1. **Drag `~/Downloads/twozero.tox` into TD network editor** → Install
2. **Enable MCP:** twozero icon → Settings → mcp → "auto start MCP" → Yes
3. **Restart Hermes session**

Verify: `nc -z 127.0.0.1 40404 && echo "twozero MCP: READY"`

## Environment Notes

- **Non-Commercial TD** caps resolution at 1280×1280. Use `outputresolution = 'custom'`.
- **Codecs:** `prores` (preferred on macOS) or `mjpa` as fallback. H.264/H.265/AV1 require Commercial.
- Always call `td_get_par_info` before setting params — names vary by TD version.

## Key Implementation Rules

- **GLSL time:** No `uTDCurrentTime`. Use Values page: set `value0name` → `uTime`, then `op('/project1/shader').par.value0.expr = "absTime.seconds"`. Fallback: Constant TOP in `rgba32float`.
- **Feedback TOP:** Use `top` parameter reference, not direct wire.
- **Resolution:** Non-Commercial caps at 1280×1280.
- **Large shaders:** Write to `/tmp/file.glsl`, then `td_write_dat`.
- **Vertex access (TD 2025.32):** `point.P[0]` etc. — NOT `.x`, `.y`, `.z`.
- **Extensions:** `ext0object` = `"op('./datName').module.ClassName(me)"` in CONSTANT mode. Call `td_reinit_extension` after editing.
- **Script callbacks:** ALWAYS use `me.parent()` / `scriptOp.parent()`.
- **Cleaning nodes:** Always `list(root.children)` + `child.valid` check.

## Workflow

### Step 0: Discover
Call `td_get_par_info` for each op type, `td_get_hints` for patterns, `td_get_focus` for selection, `td_get_network` for structure. No temp nodes, no cleanup.

### Step 1: Clean + Build
**Split cleanup and creation into SEPARATE MCP calls.** Use `td_create_operator` for each node. For bulk: `td_execute_python`.

```
td_create_operator(type="noiseTOP", parent="/project1", name="bg", parameters={"resolutionw": 1280, "resolutionh": 720})
```

### Step 2: Set Parameters
Prefer native tool: `td_set_operator_pars(path="/project1/bg", parameters={"roughness": 0.6, "monochrome": true})`

### Step 3: Wire
Use `td_execute_python` — no native wire tool exists.

### Step 4: Verify
`td_get_errors`, `td_get_perf`, `td_get_operator_info(path="/project1/out", detail="full")`

### Step 5: Display / Capture
`td_get_screenshot(path="/project1/out")` or open window via `windowCOMP`.

## MCP Tool Quick Reference

**Core (use these most):**
| Tool | What |
|------|------|
| `td_execute_python` | Run arbitrary Python in TD |
| `td_create_operator` | Create node with params + auto-positioning |
| `td_set_operator_pars` | Set params safely |
| `td_get_operator_info` | Inspect one node |
| `td_get_operators_info` | Inspect multiple nodes |
| `td_get_network` | See network structure |
| `td_get_errors` | Find errors/warnings |
| `td_get_par_info` | Get param names for an OP type |
| `td_get_hints` | Get patterns/tips |
| `td_get_focus` | What's selected |

**Read/Write:**
| Tool | What |
|------|------|
| `td_read_dat` | Read DAT text |
| `td_write_dat` | Write/patch DAT |
| `td_read_chop` | Read CHOP values |
| `td_read_textport` | Read TD console |

**Visual:**
| Tool | What |
|------|------|
| `td_get_screenshot` | Capture OP viewer |
| `td_get_screenshots` | Capture multiple OPs |
| `td_navigate_to` | Jump to an OP |

**System:**
| Tool | What |
|------|------|
| `td_get_perf` | Performance profiling |
| `td_list_instances` | List running TD instances |
| `td_get_docs` | In-depth TD docs |
| `td_reinit_extension` | Reload extension |
| `td_clear_textport` | Clear console |

**Input Automation:**
| Tool | What |
|------|------|
| `td_input_execute` | Send mouse/keyboard |
| `td_input_status` | Poll input queue |
| `td_input_clear` | Stop input automation |

The remaining 4 tools (`td_project_quit`, `td_test_session`, `td_dev_log`, `td_clear_dev_log`) are admin/dev-mode utilities — see `references/mcp-tools.md` for the full 36-tool reference.

## Key Implementation Rules

**GLSL time:** No `uTDCurrentTime` in GLSL TOP. Use the Values page:
```python
# Call td_get_par_info(op_type="glslTOP") first to confirm param names
td_set_operator_pars(path="/project1/shader", parameters={"value0name": "uTime"})
# Then set expression via script:
# op('/project1/shader').par.value0.expr = "absTime.seconds"
# In GLSL: uniform float uTime;
```

Fallback: Constant TOP in `rgba32float` format (8-bit clamps to 0-1, freezing the shader).

**Feedback TOP:** Use `top` parameter reference, not direct input wire. "Not enough sources" resolves after first cook. "Cook dependency loop" warning is expected.

**Resolution:** Non-Commercial caps at 1280×1280. Use `outputresolution = 'custom'`.

**Large shaders:** Write GLSL to `/tmp/file.glsl`, then use `td_write_dat` or `td_execute_python` to load.

**Vertex/Point access (TD 2025.32):** `point.P[0]`, `point.P[1]`, `point.P[2]` — NOT `.x`, `.y`, `.z`.

**Extensions:** `ext0object` format is `"op('./datName').module.ClassName(me)"` in CONSTANT mode. After editing extension code with `td_write_dat`, call `td_reinit_extension`.

**Script callbacks:** ALWAYS use relative paths via `me.parent()` / `scriptOp.parent()`.

**Cleaning nodes:** Always `list(root.children)` before iterating + `child.valid` check.

## Recording / Exporting Video

```python
root = op('/project1')
rec = root.create(moviefileoutTOP, 'recorder')
op('/project1/out').outputConnectors[0].connect(rec.inputConnectors[0])
rec.par.type = 'movie'; rec.par.file = '/tmp/output.mov'
rec.par.videocodec = 'prores'  # NOT license-restricted on macOS
rec.par.record = True  # start; False to stop
```

H.264/H.265/AV1 need Commercial license. Use `prores` on macOS or `mjpa`.
Extract frames: `ffmpeg -i /tmp/output.mov -vframes 120 /tmp/frames/frame_%06d.png`
**TOP.save() is useless for animation** — always use MovieFileOut.

### Before Recording: Checklist
1. **Verify FPS > 0** via `td_get_perf`. If FPS=0, recording will be empty.
2. **Verify shader output is not black** via `td_get_screenshot`.
3. **If recording with audio:** cue audio first, then delay recording by 3 frames.
4. **Set output path before starting record** — setting both in same script can race.

## Audio-Reactive GLSL (Proven Recipe)

### Correct signal chain
```
AudioFileIn CHOP (playmode=sequential) → AudioSpectrum CHOP (FFT=512, outlength=256, timeslice=ON) → Math CHOP (gain=10) → CHOP to TOP (dataformat=r, layout=rowscropped) → GLSL TOP input 1
Constant TOP (rgba32float, time) → GLSL TOP input 0
GLSL TOP → Null TOP → MovieFileOut
```

### Critical audio-reactive rules
1. **TimeSlice must stay ON** for AudioSpectrum. OFF = 24000+ samples → overflow.
2. **Set Output Length manually** to 256 via `outputmenu='setmanually'` and `outlength=256`.
3. **DO NOT use Lag CHOP** — expands 256 samples to 2400+, averaging to ~1e-06.
4. **DO NOT use Filter CHOP** — same expansion problem.
5. **Smoothing belongs in GLSL** — `mix(prevValue, newValue, 0.3)` via feedback texture.
6. **CHOP to TOP dataformat = 'r'**, layout = 'rowscropped'. Sample at y=0.25.
7. **Math gain = 10** (not 5). Raw spectrum ~0.19 in bass range.
8. **No Resample CHOP needed.** Use `outlength` param directly.

### GLSL spectrum sampling

```glsl
float iTime = texture(sTD2DInputs[0], vec2(0.5)).r;
float bass = (texture(sTD2DInputs[1], vec2(0.02, 0.25)).r + texture(sTD2DInputs[1], vec2(0.05, 0.25)).r) / 2.0;
float mid  = (texture(sTD2DInputs[1], vec2(0.2, 0.25)).r + texture(sTD2DInputs[1], vec2(0.35, 0.25)).r) / 2.0;
float hi   = (texture(sTD2DInputs[1], vec2(0.6, 0.25)).r + texture(sTD2DInputs[1], vec2(0.8, 0.25)).r) / 2.0;
```

See `references/network-patterns.md` for complete build scripts + shader code.

## Operator Quick Reference

TOP (Purple): noiseTOP, glslTOP, compositeTOP, levelTOP, blurTOP, textTOP, nullTOP | CHOP (Green): audiofileinCHOP, audiospectrumCHOP, mathCHOP, lfoCHOP, constantCHOP | SOP (Blue): gridSOP, sphereSOP, transformSOP, noiseSOP | DAT (White): textDAT, tableDAT, scriptDAT, webserverDAT | MAT (Yellow): phongMAT, pbrMAT, glslMAT, constMAT | COMP (Gray): geometryCOMP, containerCOMP, cameraCOMP, lightCOMP, windowCOMP

## Security Notes

- MCP runs on localhost only (port 40404). No authentication — any local process can send commands.
- `td_execute_python` has unrestricted access to the TD Python environment and filesystem as the TD process user.
- `setup.sh` downloads twozero.tox from the official 404zero.com URL. Verify the download if concerned.
- The skill never sends data outside localhost. All MCP communication is local.

## References

See `references/` for: pitfalls, operators, network-patterns, mcp-tools, python-api, troubleshooting, glsl, postfx, layout-compositor, operator-tips, geometry-comp, audio-reactive, animation, midi-osc, particles, projection-mapping, external-data, panel-ui, replicator, dat-scripting, 3d-scene. Plus `scripts/setup.sh`.

---

> You're not writing code. You're conducting light.
