---
name: linkedin-david-antizar-style
description: "Crear posts para LinkedIn, Substack, newsletters o cualquier escritura pública al estilo de David Antizar — análisis de export, extracción de patrón de escritura, generación de contenido con tono personal."
version: 4.0.0
tags: [linkedin, substack, escritura, personal-branding, post, red-social, blog, estilo, export]
---

# Escritura Pública — Estilo Personal (David Antizar)

## Cuándo usarlo

- El usuario pide crear un post para **LinkedIn**
- El usuario pide crear un post para **Substack** o newsletter
- El usuario quiere generar contenido social basado en un documento/informe
- El usuario quiere analizar su estilo de escritura personal
- El usuario quiere crear contenido que suene "personal" y no corporativo (cualquier plataforma)

## Proceso general

### Fase 1: Obtener datos del usuario

**Opción A — Export de LinkedIn (recomendado):**
El usuario descarga sus datos de LinkedIn → sube los CSVs y HTMLs al workspace.

**Opción B — Manual:**
El usuario describe su estilo, proporciona ejemplos de posts que le gustan, o escribe directamente.

### Fase 2: Identificar el tipo de plataforma

Ver las diferencias entre LinkedIn y Substack abajo.

### Fase 3: Verificar la filosofía del usuario

David tiene una **filosofía de datos y tecnología** que debe impregnar cualquier contenido relacionado:

> **Los datos tienen dos clases: libres y privados.**
> - Los datos libres circulan. Sin barreras.
> - Los datos privados se procesan en local. Sin salir. Sin excepciones.
> - No se necesita IA para gestionar esto. Herramientas deterministas bastan.

Si el contenido toca datos, tecnología o administración, cargar `references/datos-libres-privados.md` y basar el contenido en esta filosofía.

### Fase 4: Generar contenido

Usar los patrones extraídos para crear contenido que suene auténtico y personal.

## Diferencias por plataforma

### LinkedIn
- Hashtags específicos del tema (máximo 5)
- Párrafos cortos (máximo 250 caracteres)
- Longitud: 500-1500 palabras para análisis
- Estructura típica: gancho → contexto → datos clave → análisis → conclusión

### Substack / Newsletter
- Sin hashtags
- Párrafos un poco más largos que LinkedIn (hasta 300 caracteres)
- Más profundidad en el análisis
- Estructura más narrativa: gancho → filosofía/principio → desarrollo → conclusión
- **Más filosofía, menos datos técnicos**
- **Cero tecnicismos innecesarios** (no mencionar bibliotecas, APIs, frameworks específicos salvo que el usuario los pida explícitamente)

## Principios del estilo David Antizar (resumen)

### Tono
- Técnico pero accesible — como explicando a un colega
- Directo, sin rodeos
- Con opinión propia — NO neutral
- Sin jerga corporativa ("sinergias", "hoja de ruta", etc.)
- Datos como argumento principal (cuando correspondan)
- Ironía fina, no sarcasmo barato
- Voz en primera persona

### Estructura típica
1. **Gancho** — frase corta y directa (dato impactante, pregunta retórica, afirmación provocadora)
2. **Contexto** — qué leyó/vio, breve, sin preámbulos
3. **Datos clave** — 3-5 números con contexto (LinkedIn) / **Filosofía/principio** (Substack)
4. **Análisis** — qué significan, por qué importan, opinión propia
5. **Conclusión** — frase que deje poso, no resumen

### Formato
- Párrafos cortos (máximo 250 caracteres en LinkedIn, hasta 300 en Substack)
- Frases sueltas de <80 caracteres para ritmo
- **NUNCA emojis** (David no los usa)
- Negritas para datos y conceptos clave
- Listas con guiones, nunca tablas
- Longitud: 500-1500 palabras
- Sin tablas markdown

### Lo que NO hace
- ❌ Tablas markdown
- ❌ Lenguaje corporativo
- ❌ Neutralidad
- ❌ Párrafos largos (>300 chars)
- ❌ Emojis
- ❌ Hashtags genéricos (LinkedIn: máximo 5 específicos)
- ❌ Preguntas genéricas finales ("¿qué opináis?")
- ❌ Frases hechas ni clichés
- ❌ **Tecnicismos excesivos en Substack** — no mencionar bibliotecas, frameworks, APIs específicas a menos que el usuario las pida
- ❌ **Ejemplos raros o irrelevantes** — cuando David dice "ejemplos raros", se refiere a referencias técnicas que no contribuyen al mensaje principal

### Frases típicas
- "Como cada año, la [X] ha sacado su [Y]."
- "Este año ha sido [adjetivo], así que intentaré hacer un resumen."
- "Estamos ante el mayor [superlativo] de la historia de la civilización."
- "Sin duda la [X] ha sido el gran negocio del siglo XX y va a ser el GRAN negocio del siglo XXI."
- "Por primera vez se verá una meseta de demanda de los combustibles fósiles."

### Atribución
- El contenido es del usuario (Mastermind es el ejecutor)
- Nunca "Análisis por Mastermind" ni "vía agente"
- Footer para Substack: "Hecho con ❤️ por David Antizar"

## Referencias
- `references/extraer-estilo-linkedin.md` — Procedimiento detallado para extraer estilo de export de LinkedIn
- `references/linkedin-export-inventory.md` — Inventario completo de archivos del export de LinkedIn (29 CSVs + 4 HTMLs) con descripción de cada uno
- `references/datos-libres-privados.md` — Filosofía de David sobre datos y tecnología (libres circulan, privados en local, sin IA)

## Pitfalls
- **No usar la referencia genérica** en `documentos-institucionales/references/linkedin-david-antizar-style.md` — esa versión es incorrecta
- **NUNCA usar emojis** — David no los usa en sus publicaciones
- **No ser neutral** — David tiene opinión propia
- **No usar lenguaje corporativo** — nada de "sinergias", "hoja de ruta", etc.
- **Párrafos cortos** — máximo 250 caracteres por párrafo
- **Siempre datos concretos** — los números son el argumento principal
- **Evitar tecnicismos en Substack** — no mencionar herramientas técnicas a menos el usuario las pida
- **No dar ejemplos raros** — si David dice "ejemplos raros", los ejemplos deben ser universales y comprensibles para cualquier lector, no técnicos
- **Si el informe no declara coste**, usar `tech-report-cost-analysis` para estimarlo desde specs (GPUs, fases, tokens, goodput)
