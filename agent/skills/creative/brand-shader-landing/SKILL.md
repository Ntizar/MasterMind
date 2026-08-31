---
name: brand-shader-landing
version: "1.0.0"
description: Use al crear landing de marca con shader vivo y un solo CTA.
tags: [landing, webgl, glsl, shader, marca, diseño-web, github-pages]
metadata:
  hermes:
    tags: [landing, webgl, glsl, shader, marca, diseño-web, github-pages]
    related_skills: [claude-design, oleaje-threejs, github-workflow, scroll-world-3d-landing]
---

# Landings de marca con shader vivo (patrón GlamourSurf)

## Cuándo usar

- Crear la web/landing de una marca personal o comercial con una imagen/logo fuerte.
- El usuario pide algo "disruptivo", "loquísimo" o "llamativo" para una página de marca.
- Convertir una imagen de marca en arte visual animado (agua, humo, niebla) con shader.

Landing pages de marcas que son **una sola pantalla de arte visual animado + un CTA**. Nacido del proyecto GlamourSurf (~/Projects/glamoursurf, Ntizar/glamoursurf — https://ntizar.github.io/glamoursurf/): foto de marca → shader WebGL a pantalla completa → botón Instagram.

## La lección central (David la corrigió dos veces)

1. **v1 (hero + 3 tarjetas + secciones quiénes/qué/contacto) → rechazada**: "no es disruptiva". Una marca con estética fuerte NO quiere web genérica — quiere impacto cinematográfico.
2. **v2 (multi-pantalla, scroll cinematográfico, manifiestos, marquee) → "demasiado texto"**: la web solo debe **llevar al canal de la marca** (Instagram, etc.). Ahí ya verán todo.

**Regla final: una pantalla, arte vivo, un CTA. Cero secciones de relleno.**

## Receta comprobada (deploy en producción 200 OK)

1. **Assets**: copiar la imagen de marca a `assets/`. Repo local en `~/Projects/<marca>`.
2. **Shader fullscreen en WebGL2 puro** (sin three.js — un solo `<script>`, sin dependencias, carga instantánea):
   - Triángulo gigante + fragment shader: textura de marca con *domain-warp* (flujo de agua), ripples desde el puntero, espuma/luz animada, vignette, grano de película.
   - Textura con `MIRRORED_REPEAT` para que el warp nunca muestre bordes.
3. **Tipografía**: Playfair Display (serif editorial) para el logotipo gigante `clamp()` + fantasma translúcido de fondo.
4. **CTA**: botón degradado del canal con micro-copy de una línea ("Everything happens here").
5. **Verificación**: validar llaves del shader y sintaxis JS con `node` + `vm.Script` (NO abrir navegador — file:// no renderiza WebGL2 fiable); desplegar y `curl` producción.
6. **Deploy**: GitHub Pages vía `gh repo create <repo> --public --source=. --push` + `gh api repos/OWNER/REPO/pages -X POST -f "source[branch]=main" -f "source[path]=/"`. `gh` usa keyring (no depende de .env). Verificar con `curl` que sirve el HTML nuevo (grep de contenido característico) — el build tarda ~40s.

## Referencias

- `references/shader-template.md` — fragment shader GLSL completo funcionando (ola domain-warp + ripples + espuma + grano) y el scaffolding JS de uniforms/loop, listos para adaptar a otra imagen de marca.

## Pitfalls

- **No usar `three.js` desde unpkg para landings**: añade 600KB y fallo de carga en file://; WebGL2 crudo es ~150 líneas y cero dependencias.
- **`prefers-reduced-motion`**: congelar el shader (uTime=0) y animaciones CSS — obligatorio.
- **No pedirse confirmación de arte**: David itera rápido (v1→v2→v3 en una sesión); entregar versión completa y esperar feedback directo.
- **Texto en landings de marca**: máximo 2 líneas fuera del logotipo. Si hay más que decir, es contenido del canal, no de la web.
