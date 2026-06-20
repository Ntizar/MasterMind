---
name: proyecto-grande-pasos
version: "2.6.0"
description: Patrón para crear proyectos grandes (cursos, dashboards, ecosistemas) manteniendo proceso y formato consistente. Captura el approach que David usa con Mastermind.
tags: [proceso, proyecto, planificacion, workflow, grande]
triggers: [proyecto grande, curso, ecosistema, plan maestro, mega-plan, proyecto por partes]
references:
  - references/template-ts-module.md — Plantilla de módulo TypeScript estandarizada (package.json, tsconfig, README, tests)
  - references/patron-modulos-js-lazy-load.md — Patrón de módulos JS en `js/modules/` con lazy-load en SPA single-file
---

# Proyecto Grande por Pasos

Patrón para construir proyectos ambiciosos (cursos, dashboards, ecosistemas de skills) de forma incremental sin perder calidad ni coherencia.

## Principios clave

0. **David quiere disruptivo, no convencional** — Cuando pide ideas, quiere "chorradas" que escalean, no negocios serios. Test: ¿se lo contarías en un bar y se ríe? Si la respuesta es "es interesante pero aburrido", descartar. Ver skill `producto-web-viral` para el patrón completo.

1. **Plan maestro primero** — Antes de escribir una línea de contenido, crear un `MEGA-PLAN.md` que defina:
   - Objetivo general y por qué partes
   - Estructura de bloques/módulos
   - Dependencias entre partes
   - Criterios de calidad por bloque
   - Casos de uso reales por nivel

2. **Formato autocontenido** — Cada pieza (lección, módulo, skill) debe funcionar por sí misma:
   - Referenciar el plan maestro para contexto
   - No depender de piezas anteriores para ser útil
   - Incluir su propio header/navegación

3. **Límite duro por pieza** — Máximo 500 líneas por archivo entregable. Si es más largo, dividir.

4. **Iteración visible** — Progreso constante, sin pausas silenciosas:
   - Terminar un bloque → mostrar resultado → seguir al siguiente
   - Si algo falla, documentar y continuar
   - Nunca parar sin explicar dónde estamos

5. **Reusar antes de crear** — Siempre consultar skills existentes antes de inventar.

## Flujo estándar

### FASE 1: DIAGNÓSTICO
- Leer skills existentes relacionados
- Identificar qué ya existe vs qué crear
- Definir alcance concreto (NO infinito)

### FASE 2: PLAN MAESTRO
- Crear MEGA-PLAN.md con:
  - Visión general y filosofía del proyecto
  - Lista de bloques numerados con sesiones
  - Dependencias entre bloques
  - Estilo/formato unificado
  - Criterios de completado
  - Casos de uso reales por bloque

### FASE 3: VISUAL FIRST (nuevo en v2.1)
- **ANTES de tocar backend/datos/lógica**, construir lo visual
- El wow visual es lo que se comparte y lo que engancha
- Mostrar el resultado visual en <5 min de inicio de sesión
- Si el proyecto tiene componente 3D/visual → essa va primero, el backend después
- **Regla David:** Si pasas 20 min en backend sin mostrar nada visual, estás haciendo algo mal

### FASE 4: LÓGICA + PAYMENTS
- Conectar backend a lo visual ya existente
- Pagos (PayPal SDK), WebSocket, base de datos
- Ahora sí, infraestructura

### FASE 5: EJECUCIÓN INCREMENTAL
- **Batch generation**: Usar Python scripts para generar bloques en lote con la misma plantilla
- Cada batch: generar → verificar → commit/push → siguiente batch
- Mantener formato consistente con el template
- **NO hacer todo de golpe** — Dividir por niveles/fases

### FASE 5: INTEGRACIÓN
- Verificar que todos los bloques son coherentes
- Actualizar el plan maestro con estado real
- Actualizar INDEX.html con el contenido completo
- Commit y push final

## Patrón de batch generation (nuevo en v2)

Cuando hay 5+ archivos similares que generar:

1. Crear un diccionario Python con metadata de cada archivo (nombre, título, contenido)
2. Iterar sobre el diccionario, inyectando metadata en un template HTML
3. Escribir cada archivo con `write_file`
4. Verificar conteo de KaTeX, Plotly, atribuciones con un script de validación
5. Commit y push tras cada batch

**Ventaja**: 10 archivos en 1 script vs 10 llamadas individuales.

## Formato para contenido educativo HTML

- **Plantilla base**: KaTeX (CDN) + Plotly.js (CDN) para fórmulas y gráficos
- **Estructura**: Header → Nav → Capítulos → Ejercicios → Resumen → Footer
- **Componentes**:
  - Cajas de teoría (azul), ejemplo (naranja), error (rojo), idea (púrpura), éxito (verde)
  - Gráficos interactivos con Plotly.js (mínimo 1 por sesión)
  - Ejercicios con inputs y feedback inmediato
  - Barra de progreso scroll
  - Navegación Anterior/Siguiente
- **Footer**: "Hecho con ❤️ por David Antizar"
- **Responsive**: media query para móvil

## Niveles de contenido

| Nivel | Contenido | Complejidad |
|-------|-----------|-------------|
| Primaria | Textos simples, emojis, Canvas 2D | Baja |
| ESO | Funciones, ecuaciones, trigonometría | Media |
| Bachiller | LaTeX con KaTeX, gráficos interactivos | Alta |
| Carrera | Multivariable, álgebra lineal, EDOs | Muy alta |

## Fase 0: DIAGNÓSTICO DE VIABILIDAD (nuevo en v2.2)

**Antes de crear un MEGA-PLAN**, evaluar si el proyecto es viable cargando skills existentes:

1. **Cargar skill del proyecto existente más parecido** (ej: `matematicas-curso-educativo` para un nuevo curso)
2. **Cargar skills del dominio específico** (ej: `stem/td/td-proyecciones`, `stem/td/td-perspectivas`...)
3. **Cargar skills de visualización** (ej: `architecture-diagram`, `excalidraw`)
4. **Comparar estructura**:
   - ¿Cuántos temas/hitos tiene el proyecto existente?
   - ¿Cuántos skills de dominio existen? (cada skill = bloque temático)
   - ¿Cuál es la complejidad visual? (fórmulas vs dibujos SVG vs gráficos 3D)
5. **Estimar tamaño**: temas × tamaño estimado por archivo
6. **Evaluar diferencia clave**: ¿qué hace este proyecto DIFERENTE al existente? (esto define el valor)
7. **Viabilidad en %**: basado en skills existentes × complejidad visual × tamaño estimado

**Fórmula rápida de viabilidad**:
- ✅ +5 skills de dominio con contenido → conocimiento base sólido
- ✅ Template HTML existente → estructura probada
- ⚠️ Visual más complejo que el existente → cada archivo será más grande/lento
- ❌ 0 skills de dominio → hay que crear el conocimiento desde cero

**Resultado típico**: 85% si hay skills de dominio + template existente. 60% si hay template pero poco conocimiento de dominio. <40% si todo es nuevo.

## Fase 0: IDEACIÓN (antes del plan maestro)

David NO quiere ideas "seguras" o "negocios". Quiere **chorradas disruptivas** que:

1. **Concepto de 2 segundos** — lo entiendes y te ríes al instante
2. **Visual / compartible** — la gente comparte capturas, no texto
3. **Urgencia o escasez** — algo se acaba, algo crece, algo muere
4. **Precio tan bajo que no piensas** — 1€ es impulse buy, no decisión

**Patrón ganador (pixel store):**
- Mecánica absurda pero visual → "1 píxel = 1$"
- Progreso colectivo observable → la gente VE cómo crece
- Social proof → "mira, ya van 50.000 personas"
- FOMO natural → "si no participo me lo pierdo"

**NO funciona:**
- "Resolver un problema serio" → aburrido, hay mil competidores
- Nichos pequeños →David quiere que TODO el mundo lo necesite
- Ideas que ya existen → "esto ya lo hace X app"
- Razonar como business plan →David se frustra con "estudio de mercado"

**Check de ideación:** Si la idea no te hace sonreír en 5 segundos, descártala.

## Patrón MEGA-PLAN 2: Sistema de mejora continua

**Descubierto:** 2026-06-09 con DeSumarIntegrar. Cuando un proyecto grande tiene 100+ piezas, crear un segundo plan (`MEGA-PLAN2.md`) dedicado a la mejora continua automatizada.

### Estructura del sistema

```
proyecto/
├── MEGA-PLAN.md          ← Plan original de creación
├── MEGA-PLAN2.md         ← Plan de mejora continua
├── progress.json         ← Estado de cada pieza
└── cron job cada 30min   ← Ejecuta mejoras incrementales
```

### El archivo progress.json

```json
{
  "last_improved": "nombre-pieza",
  "last_run": "2026-06-09T15:00:00Z",
  "total_runs": 0,
  "topics": {
    "pieza-1.html": {
      "status": "pending",       // pending → improved_1 → improved_2 → complete
      "priority": 1,              // 1=alta, 2=media, 3=baja
      "improvement_count": 0,
      "scores": {
        "dimension_1": 0,         // Métricas específicas del dominio
        "dimension_2": 0
      }
    }
  }
}
```

### Criterios del plan de mejora

1. **Priorización** — Las piezas的基础icas van primero (prioridad 1)
2. **Rondas** — Cada pieza pasa por 3-4 rondas de mejora
3. **Criterio de completado** — Todos los scores ≥ umbral
4. **Un tema por ejecución** — Cada cron improve exactamente 1 pieza
5. **Autocontenido** — El prompt del cron no depende del contexto de la sesión

### Calidad vs Cantidad

**Pitfall crítico (descubierto):** Si el cron solo optimiza "más ejercicios", genera contenido repetitivo y de baja calidad.

**Regla:** El prompt debe forzar variedad:
- Mínimo N tipos diferentes de contenido por pieza
- Verificación post-mejora (¿realmente mejoró?)
- Revisión periódica de resultados (David pregunta "¿cómo va esto?")

### Domain-Adaptive Quality Dimensions (nuevo en v2.3)

Cada dominio educativo necesita sus propias métricas de calidad. NO usar las mismas dimensiones para Matemáticas que para Dibujo Técnico.

#### Matemáticas (DeSumarIntegrar)

| Dimensión | Peso | Qué mide |
|-----------|------|----------|
| exercises | 30% | Variedad de tipos: completar, V/F, ordenar, quiz, problema contextual, canvas interactivo |
| text | 20% | Explicación estructurada 4 pasos: ¿qué es? → ¿para qué sirve? → ¿cómo se hace? → ¿error común? |
| visual | 15% | Plotly solo si aporta (NO en primaria básica). Línea numérica, barras, funciones según nivel |
| real_world | 20% | Casos cotidianos que enganchen (pizza, caramelos, ascensor, temperatura) |
| connections | 10% | Conexiones entre temas: suma↔resta inversas, ×↔÷, fracción↔decimal |
| difficulty_range | 5% | Ejercicios fáciles, medios y difíciles mezclados |

#### Dibujo Técnico

| Dimensión | Peso | Qué mide |
|-----------|------|----------|
| svg_interactive | 30% | SVG con click, hover, animación, arrastre. NO estáticos decorativos |
| exercises | 25% | Identificar vistas, completar proyecciones, V/F visual, ordenar planos |
| text_explanation | 15% | Explicación paso a paso con llamadas visuales a elementos del SVG |
| real_world | 15% | Planos reales, piezas industriales, casos de taller/obra |
| error_common | 10% | Error típico VISUAL (trazos mal colocados, confusión diedros, vistas intercambiadas) |
| navigation | 5% | Enlaces entre temas relacionados, breadcrumbs, progresión lógica |

#### Otras disciplinas (patrón a seguir)

Al crear dimensiones para un nuevo dominio:
1. Identificar el **stack visual dominante** (Plotly para maths, SVG para DT, Three.js para 3D, Canvas 2D para primaria)
2. Priorizar la **interactividad específica del dominio** (no genérica)
3. Incluir al menos una dimensión de **error común típico del dominio**
4. Incluir al menos una dimensión de **caso real profesional** (taller, obra, industria, laboratorio)

### CSS Coherence Audit (nuevo en v2.4)

**Problema:** En proyectos con 50+ HTMLs, el CSS inline puede derivar entre temas. Temas viejos sin ciertas clases, temas nuevos con CSS extra, variables renombradas.

**Solución:** Al final de cada sesión de mejora, ejecutar una auto-auditoría CSS:

```
1. Elegir 3-5 HTMLs aleatorios (que NO sean los que acabas de mejorar)
2. Leer sus bloques <style>
3. Comparar con el TEMPLATE CSS BASE del proyecto
4. Verificar:
   - ¿Todas las clases obligatorias están presentes?
   - ¿Las variables CSS son las mismas?
   - ¿No hay CSS muerto (clases definidas pero no usadas)?
   - ¿No falta CSS necesario (clases usadas pero no definidas)?
5. Puntuar coherencia (0-10)
6. Si hay deriva, anotar en progress.json.audit
```

**Clases obligatorias del template base (proyectos educativos):**
```
.header, .container, .chapter-title, .box, .box-teoria, .box-ejemplo,
.box-error, .box-idea, .box-success, .svg-container, .interactive,
.exercises, .exercise, .quiz-options, .quiz-btn, .quiz-btn.correct,
.quiz-btn.wrong, .summary, .nav, .footer, .progress-bar, .progress-fill
```

**Variables CSS obligatorias:**
```
--azul:#2563eb, --naranja:#f97316, --verde:#10b981, --rojo:#ef4444,
--fondo:#fff, --texto:#1e293b, --gris:#94a3b8, --azul-claro:#eff6ff,
--naranja-claro:#fff7ed, --verde-claro:#ecfdf5, --rojo-claro:#fef2f2,
--pura-claro:#faf5ff, --pura:#a855f7
```

**Estructura del audit en progress.json:**
```json
{
  "audit": {
    "last_css_audit": "2026-06-10",
    "css_coherence_score": 8.5,
    "total_themes_audited": 3,
    "drift_found": ["b03-04-caballera.html: falta .box-idea"],
    "drift_fixed": 1
  }
}
```

### Nocturnal Cron Orchestration (nuevo en v2.4)

**Problema:** Los crons de mejora cada 30min saturan el sistema y no dan tiempo a mejoras profundas. Además, compiten por recursos con otros crons.

**Solución:** Agrupar las mejoras en **sesiones nocturnas de 2 horas**, con horarios escalonados para múltiples proyectos.

#### Arquitectura

```
22:00 UTC — DibujoTecnico (3-5 temas, prioriza SVG interactivos)
23:30 UTC — DeSumarIntegrar (3-5 temas, rotación de niveles)
```

#### Flujo del cron nocturno

```
CADA NOCHE:
1. Leer progress.json
2. Seleccionar 3-5 temas (prioridad + menos mejorados + rotación nivel)
3. Para CADA tema:
   a. Leer HTML actual
   b. ANALIZAR qué falta
   c. MEJORAR 2-3 dimensiones concretas
   d. VERIFICAR que el HTML no está roto
   e. ACTUALIZAR progress.json
   f. GIT COMMIT (un commit por tema)
4. AUTO-AUDITORÍA CSS (3-5 HTMLs aleatorios)
5. Resumen de la sesión
```

#### Criterios de selección de temas

1. **Prioridad 1:** Temas con improvement_count = 0 (nunca mejorados)
2. **Prioridad 2:** Temas con scores más bajos
3. **Prioridad 3:** Temas de bloques básicos primero
4. **Rotación forzada:** Cada 6 ejecuciones, forzar un nivel superior aunque tenga prioridad baja
5. **Nunca repetir** el mismo tema en la misma noche

#### Configuración del cron en Hermes

```bash
# Crear cron nocturno
cronjob action=create \
  name="proyecto-mejora-continua" \
  schedule="0 22 * * *" \    # 22:00 UTC
  deliver="local" \
  workdir="/root/workspace/Proyecto" \
  prompt="[prompt autocontenido con MEGA-PLAN2.md + progress.json]"

# Para segundo proyecto, escalonar:
# schedule="30 23 * * *"  (23:30 UTC)
```

**Regla:** El prompt del cron debe ser **autocontenido** — incluir el template CSS base, las dimensiones de mejora, y las reglas críticas. No debe depender del contexto de la sesión que lo creó.

### SVG Interactivity Patterns for Technical Drawing (nuevo en v2.4)

Para proyectos de Dibujo Técnico, los SVG deben ser interactivos, no decorativos. Cada SVG debe tener al menos una de estas interacciones:

| Tipo | Implementación | Uso |
|------|---------------|-----|
| **Click toggle** | `onclick="this.classList.toggle('show-aux')"` + CSS `.show-aux .aux-line { opacity: 1 }` | Mostrar líneas auxiliares, trazos ocultos |
| **Hover info** | `onmouseover="showInfo(event, 'texto')"` + tooltip div | Identificar elementos del dibujo |
| **CSS animation** | `@keyframes draw { from { stroke-dashoffset: 1000 } to { stroke-dashoffset: 0 } }` | Mostrar proceso de construcción paso a paso |
| **Drag** | `mousedown/mousemove/mouseup` handlers | Colocar vistas, alinear proyecciones |
| **Comparison** | Two SVGs side-by-side with toggle button | Correcto vs incorrecto, antes vs después |

**Patrón de SVG comparativo (error común):**
```html
<div class="svg-container">
  <svg viewBox="0 0 400 200">
    <!-- Versión correcta -->
    <g id="correcto">
      <line ... stroke="var(--verde)" />
    </g>
    <!-- Versión incorrecta (oculta por defecto) -->
    <g id="incorrecto" style="display:none">
      <line ... stroke="var(--rojo)" />
    </g>
  </svg>
  <button onclick="toggleError()">Ver error común</button>
</div>
<script>
function toggleError() {
  var c = document.getElementById('correcto');
  var i = document.getElementById('incorrecto');
  c.style.display = c.style.display === 'none' ? 'block' : 'none';
  i.style.display = i.style.display === 'none' ? 'block' : 'none';
}
</script>
```

**Regla de oro:** Si el SVG no se puede tocar (click, hover, animación), no está bien. Un SVG decorativo vale menos que un SVG interactivo simple.

### Stagnation detection (nuevo en v2.3)

**Problema:** Un tema puede recibir 3-4 rondas de mejora sin que sus scores suban apreciablemente. El cron sigue añadiendo contenido repetitivo.

**Solución:** Tras la 3ª ronda sin mejora en ninguna dimensión (score sin cambios), el cron debe:
1. **Cambiar estrategia**: en lugar de añadir contenido, REEMPLAZAR ejercicios repetitivos por tipos nuevos
2. **Bajar prioridad** temporalmente (de 1 a 3) para que otros temas tengan oportunidad
3. **Anotar en progress.json** como `"stagnation": true` con la estrategia de cambio

**Si tras 5 rondas sigue estancado:** marcar como `status: "complete"` y pasar al siguiente. No todo necesita 10/10 en todas las dimensiones.

### Level rotation (nuevo en v2.3)

**Problema:** El cron prioriza siempre los temas de prioridad 1 (normalmente primaria/base) y nunca llega a niveles superiores (bachiller, carrera).

**Solución forzada:** El cron debe alternar entre niveles cada N ejecuciones:

```
Ejecución 1-5:  Prioridad 1 (base)
Ejecución 6:    Forzar nivel bachiller aunque tenga prioridad 2
Ejecución 7-11: Prioridad 1 (base)
Ejecución 12:   Forzar nivel carrera/universidad
...
```

**Implementación en progress.json:** Añadir `last_level_rotation` y `executions_since_rotation` al nivel raíz, y el cron debe comprobarlos antes de seleccionar tema.

### Escalado de progress.json (nuevo en v2.3)

**Problema observado:** Un projecto con 100+ temas (como DeSumarIntegrar) genera un progress.json de 60KB+ en pocos días. Cada ejecución del cron lo lee y reescribe entero.

**Prácticas recomendadas:**
- Mantener solo los **últimos 3 improvements** por tema (limpiar históricos viejos)
- Usar nombres de tema cortos pero únicos
- Si supera 100KB, particionar en `progress/b01.json`, `progress/b02.json`, etc. por bloque
- El cron solo carga el fichero del bloque que va a mejorar

### Reporte semanal combinado (nuevo en v2.3)

Cuando haya 2+ proyectos con mejora continua activa, crear un cron de reporte semanal que:
1. Lea los progress.json de todos los proyectos
2. Calcule: temas mejorados esta semana, score medio, estancamientos
3. Genere un resumen Markdown en `reports/semana-YYYY-MM-DD.md`
4. Opcional: entregue a Telegram como resumen

**Formato del reporte:**

```markdown
# 📊 Reporte Semanal — Semana del DD/MM

## DeSumarIntegrar
- Temas mejorados: 12/107
- Score medio: 7.4/10
- Estancados: 2
- Próxima semana: ESO+ (8 temas pendientes)

## DibujoTecnico
- Temas mejorados: 5/52
- Score medio: 6.2/10
- Estancados: 0
- Próxima semana: Bloque 3 (perspectivas)

## Total ejecuciones: 45
```

### Actualización del README

El cron debe auto-actualizar el README con el progreso actual. Ver `matematicas-curso-educativo/references/readme-auto-update-prompt.md` para el template.

## Despliegue: Escalera de hosting

| Fase | Hosting | Cuándo | URL |
|------|---------|--------|-----|
| **Preview rápido** | `python3 -m http.server` | Desarrollo local | `localhost:8080` |
| **Demo pública** | **GitHub Pages** | Cuando el frontend funciona | `user.github.io/repo/` |
| **Producción** | **NaN.builders** | Cuando hay backend real-time | `app.apps.nan.builders` |

**GitHub Pages (fastest para frontend):**
- Repo debe ser **público** (o plan pago para privado)
- Activar vía API: `POST /repos/{owner}/{repo}/pages`
- Build automático en ~1 min
- Ideal para: Three.js, HTML/CSS/JS puro, demos visuales
- Limitación: no sirve Node.js, no WebSocket, no backend

**NaN (para backend real):**
- Requiere Dockerfile + usuario no-root
- Puerto configurable (NUNCA 80 desde appuser)
- Auto-deploy por polling de GitHub (no webhooks)
- Ideal para: Express, SQLite, WebSocket, pagos

**Regla David:** "Lo quiero en GitHub primero" → Pages es el path más rápido. NaN solo cuando el backend es imprescindible.

## Ejecución por fases con crons one-shot (v2.6 — ampliado)

**Problema:** Proyectos grandes (scaffold + 5+ fases) no caben en una sola sesión de chat. Si el agente dice "mañana" o "más tarde", el usuario se frustra. El contexto se pierde, los tool calls se acumulan.

**Solución:** Dividir el proyecto en fases. **La Fase 0 la ejecuta el agente principal INMEDIATAMENTE** (investigación, scaffold, config). Las fases restantes se ejecutan como crons one-shot espaciados a intervalos regulares (1h típicamente).

### Regla de oro: NUNCA decir "mañana"

**David odia que le digas "mañana lo hacemos" o "empezamos mañana".** La frase "¿Cómo que mañana?" es una señal de frustración inequívoca.

Cuando David propone un proyecto:
1. **La Fase 0 se hace AHORA** — investigación, scaffold, config, GH Pages → en esta misma sesión sin pausa
2. **Los crons se programan en esta sesión** — no "los creamos luego", se crean inmediatamente
3. **El primer cron empieza en ≤1h** — schedule mínimo para no saturar el sistema
4. **Cada fase entrega resultado visible** — GH Pages deploy automático para ver progreso

### Cuándo usar este patrón

- **Proyectos nuevos (greenfield):** crear repo → Fase 0 ahora → crons one-shot para fases → GH Pages → auditoría final
- Renombrados masivos (100+ archivos)
- Migraciones de plataforma
- Generación de 50+ archivos de contenido
- Refactorizaciones profundas
- Cualquier tarea que requiera 10+ tool calls o 5+ minutos de ejecución

### Estructura

```
proyecto/
├── MEGA-PLAN.md              ← Plan maestro con sesiones numeradas
├── scripts/sesion-N.py       ← Script autocontenido para sesión N
└── progress.json             ← Estado de cada sesión
```

### Flujo

1. **Crear MEGA-PLAN.md** con sesiones numeradas, dependencias y criterios de completado
2. **Crear script** para la Sesión 1 (autocontenido, dry-run, modo ejecución)
3. **Ejecutar dry-run** para verificar alcance
4. **Mostrar al usuario** el plan y pedir OK
5. **Crear cron one-shot** que ejecuta el script
6. **Verificar resultado** y pasar a siguiente sesión

### Patrón greenfield: GH Actions + auditoría final

Para proyectos nuevos desde cero (como WaveThree en junio 2026):

#### Secuencia estándar

```
1. CREAR REPO (github.com/Ntizar/<nombre>)
   - scaffold: README, package.json, directorios, .gitignore
   - docs: ARCHITECTURE.md, ADR-001

2. FASE 0 — AGENTE PRINCIPAL AHORA (no cron)
   - Investigación de fuentes, zona piloto, stack
   - docs/sources/FASE-0-investigacion.md
   - Mapa de fuentes, backlog priorizado

3. GITHUB PAGES WORKFLOW (antes del primer cron)
   - .github/workflows/deploy-gh-pages.yml
   - peaceiris/actions-gh-pages@v4
   - Build automático en cada push

4. CRONS ONE-SHOT (espaciados 1h)
   - F1.1, F1.2, ..., F5, Auditoría
   - Cada cron: task autocontenida → commit → push → resultado
   - GH Actions despliega automáticamente cada cambio

5. AUDITORÍA FINAL (último cron, 1h después de F5)
   - Revisión de código: imports, memory leaks, dispose
   - Revisión Three.js: geometrías, texturas, controls
   - Revisión UI: sliders, selector, export
   - CHANGELOG.md, docs/auditoria.md
```

#### Creación del cron one-shot para greenfield

```bash
cronjob action=create \
  name="WaveThree-Fase1.1-Mejora-MVP-visual" \
  schedule="2026-06-17T17:18:00Z" \     # Timestamp ISO exacto
  deliver="local" \
  prompt="[Prompt autocontenido: 
   - Proyecto, repo, GITHUB_TOKEN
   - Qué archivos modificar
   - Qué verificar al final
   - Instrucción explícita de commit + push]"
```

#### Reglas del patrón greenfield

1. **GH Actions ANTES del primer cron** — Cada push despliega automáticamente. No esperar a tener todo listo.
2. **Auditoría SIEMPRE al final** — Un cron dedicado a bugs, calidad, CHANGELOG. No mezclar con F5.
3. **Investigación ≠ Desarrollo** — La Fase 0 la hace el agente principal porque requiere síntesis, no ejecución mecánica.
4. **1h espaciado mínimo** — Da tiempo a que cada cron termine sin solaparse con el siguiente. Reduce conflictos de merge.
5. **Cada cron es independiente** — No depende del output del cron anterior. Lee del repo el estado actual.
6. **Commit por fase** — Si un cron falla, el repo queda en el último estado bueno. Fácil rollback.

### Creación del cron one-shot

```bash
# Sesión 1: inmediata
cronjob action=create \
  name="proyecto-sesion-1" \
  schedule="now" \
  deliver="local" \
  workdir="/root/workspace/Proyecto" \
  prompt="Ejecuta python3 scripts/sesion-1.py y verifica el resultado"
```

### Ventajas

- **Contexto limpio** — Cada sesión empieza fresco
- **Paralelizable** — Sesiones sin dependencias pueden ejecutarse simultáneamente
- **Recuperable** — Si una sesión falla, solo esa se repite
- **Trazable** — Cada sesión deja un output en cron/output/
- **Escalable** — 10 sesiones = 10 crons, no 10 horas de chat

### Reglas

1. **Sesión 1 siempre es dry-run + plan** — Nunca ejecutar cambios sin ver antes
2. **Cada sesión termina con commit** — git add, git commit, git push
3. **No empezar sesión N+1 sin verificar la N** — Leer el output del cron
4. **Script autocontenido** — No depende de variables de entorno de la sesión
5. **Exclusiones claras** — El script debe listar qué NO toca (históricos, backups, .git)

### Ejemplo real: Renombrado Koldo → Mastermind

Ver `/root/workspace/Koldo/MEGA-PLAN-RENAME.md` y `scripts/rename-koldo-to-mastermind.py` para el caso real completo.

Resumen:
- **Sesión 1:** Script de renombrado base (dry-run + ejecución) → **hecho en 1 sesión**
- **Sesión 2:** Skills + Scripts (renombrar directorios en /hermes-home/skills/)
- **Sesión 3:** Documentación + Crons + Memoria
- **Sesión 4:** Repo GitHub + Verificación + ChromaDB re-index

## Pitfalls

- **🔥 Python f-strings + JS template literal collision:** NUNCA usar f-strings para generar código JS/HTML. Las llaves `{}` del JS se interpretan como placeholders de Python → NameError. Usar `.replace()` con `{PLACEHOLDER}`.
- **🔥 JSON extraction from JS file — brace counting over regex:** El regex `r'const VAR = (\{.*\});'` falla con JSON de 700KB+. Contar braces manualmente es la única forma fiable.
- **🔥 GitHub Pages deploy — token inline puede fallar:** El token de GitHub en curl inline puede romperse. Usar Python para leer el token de `/hermes-home/.env` directamente.
- **No saltarse el plan maestro** — Si lo haces directo sin plan, el formato se pierde entre piezas
- **No crear todo de golpe** — Dividir en sesiones/iteraciones, mostrar progreso
- **⚠️ COMPLETAR ANTES DE AÑADIR (David, 2026-06-15):** Cuando el usuario dice "completa lo que hay primero" o "vamos parte a parte", el flujo correcto es: (1) diagnosticar estado actual, (2) arreglar UN módulo/pieza, (3) verificar que funciona, (4) siguiente. **NUNCA** intentar arreglar 16 módulos + crear READMEs + hacer starter template en una sola pasada — causa timeouts, respuestas cortadas, y frustración del usuario. Si hay 16 módulos y 5 fallan, arreglar 1 de golpe y verificar, no los 5 a la vez.
- **⚠️ NO PARAR ENTRE TANDAS (descubrimiento junio 2026):** David NO interpreta las pausas entre tandas como "reflexión estratégica". Las interpreta como "se ha quedado bloqueado" o "ha parado el proceso". Cada tanda debe ejecutarse inmediatamente tras la anterior, sin esperar confirmación explícita a menos que haya errores de compilación o el usuario pida específicamente revisar antes de seguir. Si el usuario dice "Como que has parado?" es señal de que has esperado demasiado. Regla: completar tanda → mostrar resumen → arrancar siguiente tanda sin pausa.
- **No olvidar el repo** — Cada batch completado se commitea
- **No confundir plan con ejecución** — El plan es guía, no prisión. Si algo no funciona, adaptar el plan
- **Crons self-contained** — Si el contenido se entrega por cron, cada prompt debe ser autocontenido con referencia al MEGA-PLAN
- **No usar subagentes para HTML >10KB** — Hacer directo con write_file/patch. Subagentes fallan con timeout.
- **INDEX.html debe reflejar la realidad** — Si las sesiones cambian de nombre, actualizar los enlaces en INDEX.html
- **NO unificar CSS de niveles distintos en un solo archivo externo** — Cada nivel educativo (Primaria, ESO, Bachiller, Carrera) debe mantener su CSS inline con su propia paleta de colores. El usuario prefiere que cada nivel tenga personalidad visual propia. La unificación aceptable es solo de valores cosméticos (fondos, bordes, line-height, espaciado) manteniendo el CSS inline de cada archivo.
- **No usar Aurora Design System para contenido educativo tipo libro** — Aurora es para dashboards y apps. Para cursos/tutoriales, usar CSS inline con cajas didácticas (`.box-teoria`, `.box-ejemplo`, `.box-error`, `.box-idea`), header con gradiente, y footer con atribución. El estilo libro-interactivo no debe mezclarse con estilos de dashboard.
- **NO escribir scripts Python con JS embebido** — `\n` y `\` en el código JS se interpretan como escapes de Python → errores de sintaxis. Siempre usar `patch`/`write_file` directo para modificar archivos JS/HTML, nunca incrustar código JS en strings de Python.
- **⚠️ NUNCA decir "mañana" o "más tarde" (David, 2026-06-17):** Cuando David dice "Quiero hacer el proyecto X", espera ejecución inmediata. La Fase 0 (investigación, scaffold, config) debe hacerse en esa misma sesión sin pausa. Frases como "¿Qué tal si mañana empezamos?" provocan frustración inmediata ("¿Cómo que mañana?"). El flujo correcto: Fase 0 ahora → crons one-shot programados ahora → deploy GH Pages → auditoría final.
- **⚠️ GH Actions es mejor que activar Pages manualmente (2026-06-17):** Para proyectos nuevos, crear un workflow YAML en `.github/workflows/deploy-gh-pages.yml` con peaceiris/actions-gh-pages es más robusto que activar Pages vía API. El workflow se dispara en cada push, no necesita configuración manual, y fuerza orphan branch (historial limpio). Siempre crear el workflow DENTRO del commit de creación del repo, no en un cron posterior.

## Linked Files

- `references/caso-mejora-continua-multi-proyecto.md` — Caso real: DeSumarIntegrar + DibujoTecnico, dimensiones por dominio, lecciones aprendidas tras 38 ejecuciones cron
- `references/template-html-educativo-katex-plotly.md` — Plantilla base con KaTeX + Plotly.js, componentes CSS, y patrones de gráficos interactivos
- `references/verificacion-contenido-html.md` — Script de verificación automática y criterios de "hecho" para cada sesión
- `references/unificacion-css-educativo.md` — Patrón para unificar CSS entre niveles sin perder personalidad visual (aprendido en auditoría junio 2026)
- `references/viabilidad-cursos-educativos.md` — Banco de conocimiento para evaluar viabilidad de cursos educativos: DeSumarIntegrar como referencia base, estimaciones de tamaño, stack, y comparación por dominio
  - references/caso-contrata-publico.md — Caso real: Ley 9/2017, 347 artículos, MEGA-PLAN.md + 8 sesiones cron, GitHub Pages, f-string+JS pitfall, formulario inteligente con validación en vivo, historial localStorage
  - references/caso-wave3-visor-marino.md — Caso real: WaveThree junio 2026. Greenfield + Fase 0 ahora + 9 crons one-shot 1h spacing + GH Actions + auditoría final. Señal de aprendizaje: "¿Cómo que mañana?"
  - templates/formulario-inteligente-validacion.md — Plantilla reutilizable: validación en vivo + auto-cálculo + resumen visual para formularios en SPA