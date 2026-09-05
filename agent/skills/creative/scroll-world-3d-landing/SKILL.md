---
name: scroll-world-3d-landing
description: "Usa a crear landings 3D scroll-scrub con Video (Monid)."
version: "2.0.0"
tags: [scroll, 3d, landing, video, monid, threejs, secuencial]
related_skills: [scroll-world-3d-landing, webgl-scene-wow, threejs-3d-maps]
---

# Scroll World — landings 3D con scroll-scrubbed vídeo

> ⚠️ Corrección 2026-09-05 (auditoría): el backend por defecto real es **Monid CLI (Seedance 2.0)**; Higgsfield CLI es solo backend/fallback (kling3_0), y hay **Codex CLI** opcional para stills. Stars: ~9K (no 483).

**Repo:** `https://github.com/oso95/scroll-world` (JavaScript, ~9K⭐).

## When to Use

- Cuando pidas una **landing 3D con scroll-scrub** (texto apareciendo con vídeo/fondos animados al hacer scroll).

## Requisitos (reales)

- **Monid CLI** — backend por defecto (Seedance 2.0)
- **Higgsfield CLI** — backend/fallback (kling3_0) *(no es el principal)*
- **Codex CLI** *(opcional)* — generar stills
- ffmpeg / Pillow

## Pitfalls

- Backend por defecto: **Monid CLI**, no Higgsfield.
- **No** omitir Monid/Codex en los requisitos.

## Verificación

- Configurar Monid CLI como backend y comprobar que el scroll produce vídeo/landing correcto.
