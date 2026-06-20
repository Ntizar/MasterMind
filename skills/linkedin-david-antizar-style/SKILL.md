---
name: linkedin-david-antizar-style
description: "Crear posts LinkedIn al estilo de David Antizar — análisis de export, extracción de patrón de escritura, generación de contenido con tono personal."
version: 3.0.0
tags: [linkedin, estilo, escritura, personal-branding, post, red-social, export]
---

# LinkedIn — Estilo Personal (David Antizar)

## Cuándo usarlo

- El usuario pide crear un post para LinkedIn
- El usuario quiere generar contenido social basado en un documento/informe
- El usuario quiere analizar su estilo de escritura personal
- El usuario quiere crear contenido que suene "personal" y no corporativo

## Proceso general

### Fase 1: Obtener datos del usuario

**Opción A — Export de LinkedIn (recomendado):**
El usuario descarga su datos de LinkedIn → sube los CSVs y HTMLs al workspace.

**Opción B — Manual:**
El usuario describe su estilo, proporciona ejemplos de posts que le gustan, o escribe directamente.

### Fase 2: Analizar el estilo

Ver `references/extraer-estilo-linkedin.md` para el procedimiento detallado.

### Fase 3: Generar contenido

Usar los patrones extraídos para crear contenido que suene auténtico y personal.

## Principios del estilo David Antizar (resumen)

### Tono
- Técnico pero accesible — como explicando a un colega
- Directo, sin rodeos
- Con opinión propia — NO neutral
- Sin jerga corporativa ("sinergias", "hoja de ruta", etc.)
- Datos como argumento principal
- Ironía fina, no sarcasmo barato
- Voz en primera persona

### Estructura típica
1. **Gancho** — frase corta y directa (dato impactante, pregunta retórica, afirmación provocadora)
2. **Contexto** — qué leyó/vio, breve, sin preámbulos
3. **Datos clave** — 3-5 números con contexto
4. **Análisis** — qué significan, por qué importan, opinión propia
5. **Conclusión** — frase que deje poso, no resumen

### Formato
- Párrafos cortos (máximo 250 caracteres)
- Frases sueltas de <80 caracteres para ritmo
- **NUNCA emojis** (David no los usa)
- Negritas para datos y conceptos clave
- Listas con guiones, nunca tablas
- Hashtags específicos del tema (máximo 5)
- Longitud: 500-1500 palabras para análisis

### Lo que NO hace
- ❌ Tablas markdown
- ❌ Lenguaje corporativo
- ❌ Neutralidad
- ❌ Párrafos largos (>300 chars)
- ❌ Emojis
- ❌ Hashtags genéricos
- ❌ Preguntas genéricas finales ("¿qué opináis?")
- ❌ Frases hechas ni clichés

### Frases típicas
- "Como cada año, la [X] ha sacado su [Y]."
- "Este año ha sido [adjetivo], así que intentaré hacer un resumen."
- "Estamos ante el mayor [superlativo] de la historia de la civilización."
- "Sin duda la [X] ha sido el gran negocio del siglo XX y va a ser el GRAN negocio del siglo XXI."
- "Por primera vez se verá una meseta de demanda de los combustibles fósiles."

### Atribución
- El contenido es del usuario (Mastermind es el ejecutor)
- Nunca "Análisis por Mastermind" ni "vía agente"

## Referencias
- `references/extraer-estilo-linkedin.md` — Procedimiento detallado para extraer estilo de export de LinkedIn
- `references/linkedin-export-inventory.md` — Inventario completo de archivos del export de LinkedIn (29 CSVs + 4 HTMLs) con descripción de cada uno

## Pitfalls
- **No usar la referencia genérica** en `documentos-institucionales/references/linkedin-david-antizar-style.md` — esa versión es incorrecta
- **NUNCA usar emojis** — David no los usa en sus publicaciones
- **No ser neutral** — David tiene opinión propia
- **No usar lenguaje corporativo** — nada de "sinergias", "hoja de ruta", etc.
- **Párrafos cortos** — máximo 250 caracteres por párrafo
- **Siempre datos concretos** — los números son el argumento principal
- **Si el informe no declara coste**, usar `tech-report-cost-analysis` para estimarlo desde specs (GPUs, fases, tokens, goodput)
