---
name: social-media-content-system
version: "1.0.0"
description: "Usa al montar un sistema de contenido para redes sociales."
tags: [redes-sociales, contenido, linkedin, voz, analytics, content-matrix, hooks]
author: 'Hecho con ❤️ por David Antizar'
license: MIT
metadata:
  hermes:
    tags: [redes-sociales, contenido, linkedin, voz, analytics, content-matrix, hooks]
    related_skills: [linkedin-david-antizar-style, humanizer, ai-report-generation]
---

# Sistema de contenido para redes sociales (patrón social-media-skills)

## Cuándo usarlo

- El usuario pide planificar contenido para redes (ideas mensuales, matriz de posts, "qué publico esta semana")
- Pide hooks, formatos o estructura de post más allá de la voz (PAS/AIDA/contrarian/listicle)
- Pide puntuar/validar un borrador contra sus datos reales de publicación
- Pide analizar un export de LinkedIn Analytics como dashboard con recomendaciones
- Pide montar un pipeline newsletter → multicanal (carruseles, reels, thumbnails)

**Fuente:** github.com/charlie947/social-media-skills (3.262⭐, MIT, actualizado 2026-08-30). 17 skills de Claude detrás del sistema de contenido de Charlie Hills: 415k seguidores, 100M+ vistas/año en LinkedIn, Instagram, Substack, X y YouTube, todo alimentado desde UNA newsletter.

**Diferencia con `linkedin-david-antizar-style`:** ese skill es la autoridad de LA VOZ de David (cómo suena un texto suyo). Este skill documenta el SISTEMA de operaciones de contenido alrededor de la voz: ideación en matriz, hooks, puntuación contra datos reales, analítica y cascada multicanal. Se usan juntos: voz → `linkedin-david-antizar-style`; sistema → este.

## Arquitectura central: voz compartida como única fuente

```
voice-builder (entrevista + 3-5 muestras de escritura)
   → about-me.md + voice.md        ← TODOS los demás skills leen esto primero
      → newsletter-voice.md        ← la newsletter es la FUENTE de todo lo demás
         → cascada: post-writer, reels-scripting, youtube-thumbnail,
           pinned-comment, gemini-carousel, quote-post, graphic-designer
```

Regla de oro del patrón: cada skill del ecosistema (17 en el repo) empieza comprobando si existen los archivos de voz; si no, REDIRIGE al skill fundacional y para. Ningún skill escribe de cero sin contexto compartido.

**Adaptación a Mastermind:** los archivos de voz de David ya existen de facto en `linkedin-david-antizar-style` (filosofía, frases típicas, reglas de formato). Al montar cualquier pipeline de contenido, cargar ese skill como `voice-builder` en lugar de repetir la entrevista.

## Los 5 patrones reutilizables

### 1. Matriz de contenido (ideación en bloque)
Pilares (3-5, de about-me.md) × 8 formatos FIJOS y en este orden:
1. Actionable (cómo-hacer ultraespecífico, una sola cosa)
2. Motivational (historia extraordinaria del nicho)
3. Analytical (por qué algo funciona)
4. Contrarian (contra el consejo dominante, con respaldo)
5. Observation (detalle oculto/silencioso que nadie nombra)
6. X vs Y (comparación directa)
7. Present vs Future (ahora vs luego)
8. Listicle

Celda = UNA idea concreta e irrepetible (no genérica). Salida: tabla markdown de 32+ ideas de mes. Basado en la content matrix de Justin Welsh.

### 2. Hooks quirúrgicos (2 líneas, 40 caracteres cada una)
- Línea 1: ≤40 chars, SIN preguntas, algo inesperado/específico.
- Línea 2: ≤40 chars, contradice o reencuadra la 1.
- Debe incluir "Cómo yo…"/"Yo…" y un dígito/métrica cuando sea posible.
- 6 ángulos obligatorios: number-led, contrarian, transformación personal (antes/después con dígito), authority steal (nombre/herramienta/marca), admisión (error o pérdida), future shock (predicción).
- Reglas duras: contar los 40 chars de verdad, sin em-dashes, sin relleno, preferir "3" sobre "tres", nunca dudar ("never hedge").

### 3. Puntuar contra datos propios (post-scorer)
Score de un borrador NO contra best practices genéricas sino contra el historial real del autor (métricas de sus últimas ~100 publicaciones). El repo original usa Apify (actor `apimaestro/linkedin-profile-posts`, `total_posts:100`, pitfall real: NO pasar el parámetro `fields` porque elimina los datos de engagement).

**Adaptación obligatoria para David (regla: solo herramientas gratuitas):** sustituir Apify por el EXPORT nativo de LinkedIn (CSV/HTML gratuito). El procedimiento de extracción ya está documentado en el skill `linkedin-david-antizar-style` (sección de extracción de estilo desde export + inventario de 29 CSVs). El patrón (score contra historial propio) se conserva; el extractor cambia.

### 4. Dashboard de analítica con cuadrantes
Export xlsx de LinkedIn Analytics (5 hojas: DISCOVERY, ENGAGEMENT, TOP POSTS, FOLLOWERS, DEMOGRAPHICS) → dashboard interactivo (el original: React+Recharts, tema oscuro `#0f1117`) + 5 recomendaciones respaldadas por datos. Scatter impresiones×engagements con 4 cuadrantes:
- Stars: alcance alto + engagement alto
- Viral superficial: alcance alto + engagement bajo
- Oro de nicho: alcance bajo + engagement alto
- Flojos: ambos bajos

Métricas mínimas: impresiones totales, reach, nuevos seguidores, medias diarias, tasa engagement = engagements/impresiones, picos de 3 días marcados, media móvil 7d de seguidores. Las dos tablas de TOP POSTS (por engagements y por impresiones) se fusionan y deduplican.

**Adaptación Mastermind:** para las webs de David este encaje natural es HTML vanilla en navegador (skill `frontend-dashboard-patterns` / `aurora-design-system`), no React obligatorio. Los cuadrantes son el hallazgo transferible.

### 5. Cascada multicanal desde una fuente
La newsletter es el activo madre; cada pieza de contenido derivado (post, reel, thumbnail, comentario fijado, carrusel, quote-post) se genera a partir de ella con gate de aprobación por paso. Un trabajo de escritura → N publicaciones. El orden del repo: voice → newsletter → LinkedIn → formatos visuales (Gemini prompts listos para pegar, sin API key) → comunidad → analítica.

## Cómo aplicar el sistema (receta)

1. **Voz:** cargar `linkedin-david-antizar-style` (o ejecutar voice-builder interview solo si el usuario es otra persona).
2. **Ideación:** matriz pilares×8 formatos → tabla de 32+ ideas; el usuario elige.
3. **Producción:** por idea elegida → hook (patrón 2) → framework (PAS/AIDA/BAB/STAR/SLAY) → post con reglas de la voz.
4. **Calidad:** puntuar contra export real (patrón 3) ANTES de publicar; iterar hasta pasar del percentil propio.
5. **Derivados:** newsletter → carrusel/reels/thumbnail/pinned-comment con gate.
6. **Analítica:** cada 30-90 días, cuadrantes + 5 recomendaciones (patrón 4) → alimentar la matriz.

## Pitfalls

- **Apify es de pago** (~$0.50/scrape, actor externo) — para David NUNCA: usar export nativo de LinkedIn (gratis) o caché de posts ya analizados.
- El "auto-start sin resumen" de los skills originales (la primera respuesta es la entrevista, sin preámbulos) funciona en Claude Code; en Hermes conviene confirmar el plan primero (convención Mastermind de acuerdos previos en tareas largas).
- No trasplantar las reglas de voz inglesas del repo ("British English unless voice.md says otherwise") — la voz de David está en `linkedin-david-antizar-style`: tuteo, sin emojis, sin tablas, párrafos ≤250 chars.
- Hooks: los 40 caracteres son por línea Y hay que contarlos (no estimarlos a ojo); un hook que parece corto suele pasarse.
- La matriz NO funciona con pilares genéricos ("tecnología", "datos") — exigen 2+ párrafos de posicionamiento específico o las celdas salen reutilizables y vacías.
- Cuadrantes: clasificar por percentiles del propio historial, no por umbrales absolutos (100 likes no es "alto" para todos).

## Verificación

- ¿Todos los textos generados pasan el checklist de voz del skill de David (sin emojis, sin tablas, párrafos cortos, datos concretos)?
- ¿Cada celda de la matriz es irrepetible entre pilares? (prueba: tapar el nombre del pilar y adivinarlo)
- ¿Los hooks cuentan ≤40 chars por línea verificado programáticamente?
- ¿El score cita métricas del export real del usuario (no benchmarks ajenos)?
- ¿El dashboard abre con métricas headline antes de gráficos y cierra con las 5 recomendaciones accionables?

## Referencias

- Repo: https://github.com/charlie947/social-media-skills — skills/voice-builder, post-scorer, content-matrix, hook-generator, analytics-dashboard (SKILL.md de cada uno)
- Newsletter del autor: charliehills.substack.com
- Skill hermano de voz: `linkedin-david-antizar-style`
