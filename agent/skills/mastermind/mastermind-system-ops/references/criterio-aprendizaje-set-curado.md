# Criterio de aprendizaje de un set curado (estrellas/recursos) — regla David 2026-09-04

## Señal del usuario (literal)

> "Me parece que no has aprendido muchas cosas. De las demos tmb se podría sacar cosa o cosas con pocas stars.
> Si les he dado like es por algo. Me da la sensación de que has desechado demasiada información. Tmb puede haber
> GitHub que mejoren otras stars etc y nos sean útiles para otros proyectos o buscar otros enfoques a soluciones."

## La regla

Cuando el usuario marca/likea un conjunto (stars de GitHub, favoritos, bookmarks), **cada elemento aporta algo**.
NO los filtres por estrellas, por "ya hay algo parecido", ni por "fuera de dominio". La pregunta correcta NO es
**"¿merece skill?"** sino **"¿qué ÁNGULO / ENFOQUE / TÉCNICA aporta que el ecosistema no tenga?"**.

## Qué hacer con cada elemento (decisión de 3 vías)

1. **UPGRADE** — es la versión mejor/nueva de un skill existente, o aporta un enfoque que a ese skill le falta
   (open-vocab vs YOLO de clases fijas, pose 2D→3D, pipeline CCTV completo vs detección aislada). → `skill_manage(patch)`
   al skill: añadir sección `## Comparativa de alternativas` con el repo y el valor concreto. **NUNCA lo descartes.**
   El valor del dedup es la comparativa — saber que existe algo mejor y por qué.
2. **NEW_SKILL** — aunque sea una demo de pocas estrellas (5⭐), si tiene un enfoque/patrón reutilizable
   (shader, técnica de composición, forma de encadenar APIs, UX de mapa, librería alternativa, pipeline). Estrellas ≠ filtro.
3. **REFERENCE / reconsidera** — un CRM, ERP, BaaS, framework de dominio (twenty, SuiteCRM, EspoCRM, nocobase,
   Supabase, login/auth) que NO es el stack de hoy pero vale si David monta algo mañana. Marca `category: "reference"`
   y enriquece el skill del dominio con la comparativa. Los CRMs NO son "basura": son la opción para un proyecto futuro.

## Huecos de conocimiento

Un tema que David **quiere aprender** (p.ej. "montar login/gestión de usuarios en mis webs") merece skill aunque NO
venga de una star concreta. Detecta el hueco (p.ej. solo había `github-auth`, no auth de webs) y crea el skill.

## Resultado en un barrido real (2026-09-04)

Un primer paso agresivo descartó ~180 repos como "bajo valor / <100⭐ / ya cubierto / fuera de dominio". La
re-análisis con criterio abierto extrajo de esos "descartados": **18 skills potenciales + 70 mejoras**. El descarte
por estrellas/overlap fue un ERROR reconocido y corregido.

## Ejemplos concretos del barrido

- `cctv-yolo` ← open-vocab OWL-ViT (nanoowl), pipeline completo CCTV (clearcam), training YOLO, pose 2D→3D.
- `osint-live-globe` ← recon toolkit + dossiers IA (aegis), geolocalización VLM (NVIDIA Eagle).
- `video-gen-from-topic` ← edits infinitos con LLM (ComfyUI HR Sampler), recorte vertical de podcast (openshorts).
- `huly-crm-erp-platform` ← tabla comparativa de twenty/SuiteCRM/EspoCRM/trycompai/nocobase.
