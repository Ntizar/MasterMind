---
name: ecctrl
description: "Usa a controlar personajes con Epic Controls (Three.js)."
version: "2.0.0"
tags: [ecctrl, threejs, controles, fps, character, character-controller, mocap]
related_skills: [ecctrl, threejs-3d-maps, seed-three]
---

# Ecctrl — controles de personaje para Three.js

> ⚠️ Corrección 2026-09-05 (auditoría): el paquete npm es **`ecctrl`** (no `@ecctrl/core`) y la export es **`Ecctrl`** (no `EcctrlControls`).

**Repo:** `https://github.com/pmndrs/ecctrl` (TypeScript, ~1.5K⭐). Controles FPS/TPS para Rapier + React Three Fiber.

## When to Use

- Cuando pidas **controlar un personaje** (movimiento, salto, sprint) en una escena Three.js / R3F con física Rapier.

## Uso (API real)

```bash
npm install ecctrl rapier2d-compat    # paquete 'ecctrl' (no @ecctrl/core)
```

```jsx
import { Ecctrl } from 'ecctrl';      // componente/export Ecctrl (no EcctrlControls)
<Ecctrl />                             // (default export o named, según docs)
```

## Pitfalls

- Paquete: **`ecctrl`**, no `@ecctrl/core`.
- Export: **`Ecctrl`**, no `EcctrlControls`.

## Verificación

- Montar `<Ecctrl />` en una escena R3F y comprobar que el personaje se mueve con física.
