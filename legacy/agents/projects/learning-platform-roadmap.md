# Learning Platform v2.0 — Roadmap Completo

## Visión
Una plataforma educativa **visual, gamificada y personalizada** que enseña a cualquier persona (no solo programadores) a construir y usar su propio sistema de agentes inteligentes sobre Obsidian.

**Modelo:** Pago único — los usuarios compran acceso completo
**Promesa:** En 2 horas tienes tu sistema operativo de inteligencia funcionando

---

## 📊 Estado Actual (v1.0)

### ✅ Lo que funciona
- [x] 6 módulos de contenido (M0-M5)
- [x] Sistema de quizzes básico
- [x] Personalización de nombre ({{NAME}})
- [x] Timer y progreso global
- [x] Deploy en Vercel
- [x] Export de progreso a JSON

### ❌ Lo que falla / falta
- [ ] Contenido genérico — no adaptado por tipo de usuario
- [ ] Gamificación superficial — solo puntos, sin recompensas reales
- [ ] Pocos ejemplos visuales — mucho texto, pocas demostraciones
- [ ] No hay casos prácticos por perfil (writer, consultor, dev, etc.)
- [ ] Quizzes no verifican comprensión profunda
- [ ] No hay "sandbox" para experimentar
- [ ] Certificado final básico (solo JSON, no PDF visual)
- [ ] Sin comunidad ni forma de compartir logros

---

## 🎯 Objetivos v2.0

| Objetivo | Métrica | Prioridad |
|----------|---------|-----------|
| Reducir tiempo de setup | De 2h a 45min | ALTA |
| Aumentar completion rate | De ~40% a ~75% | ALTA |
| Mejorar comprensión | Quiz avg: 60% → 85% | ALTA |
| Soportar 5 perfiles | 100% contenido adaptado | ALTA |
| Gamificación real | 8+ badges, 5 niveles | MEDIA |
| Ejemplos visuales | 3+ diagramas por módulo | MEDIA |

---

## 📅 Fases de Implementación

### FASE 1: Fundamentos (Semana 1)
**Objetivo:** Nueva arquitectura de contenido + sistema de perfiles

#### 1.1 Sistema de Perfiles
- [ ] Crear archivo `profiles.json` con 5 perfiles:
  - `no-programador` — Gente de negocios, writers, operadores
  - `junior-dev` — Programadores que quieren productividad
  - `consultor` — Freelance gestionando múltiples proyectos
  - `equipo-pequeno` — Startups 2-10 personas
  - `estudiante` — Aprendiendo a trabajar con IA
- [ ] Cada perfil define:
  - Vocabulario (evitar jerga técnica si aplica)
  - Ejemplos de dominio (escritura, código, negocios, etc.)
  - Casos de uso prioritarios
  - Duración estimada de módulos

#### 1.2 Nueva Estructura de Módulos
- [ ] Reemplazar `modules.json` con estructura por perfil:
```json
{
  "profiles": {
    "no-programador": { "modules": [...] },
    "junior-dev": { "modules": [...] },
    ...
  },
  "common": { "modules": [...] }
}
```
- [ ] Módulos comunes (todos los perfiles): M0, M1, M2
- [ ] Módulos específicos (varían por perfil): M3, M4, M5

#### 1.3 Onboarding Mejorado
- [ ] Pantalla de selección de perfil (con iconos y descripciones claras)
- [ ] Test rápido de 3 preguntas para recomendar perfil
- [ ] Guardar perfil en localStorage + exportar en JSON final

**Criterios de aceptación:**
- Usuario puede seleccionar perfil al inicio
- El contenido de M3-M5 cambia según perfil
- El export final incluye el perfil seleccionado

---

### FASE 2: Gamificación (Semana 2)
**Objetivo:** Sistema de recompensas que motive a completar

#### 2.1 Sistema de XP y Niveles
- [ ] Definir 5 niveles con nombres temáticos:
  1. `Iniciado` (0-100 XP)
  2. `Aprendiz` (100-300 XP)
  3. `Operador` (300-600 XP)
  4. `Arquitecto` (600-1000 XP)
  5. `Maestro` (1000+ XP)
- [ ] Ganar XP por:
  - Completar módulo: +50 XP
  - Quiz perfecto (100%): +25 XP bonus
  - Completar todos los módulos: +200 XP bonus
  - Tiempo récord (<90min): +50 XP bonus

#### 2.2 Sistema de Badges
- [ ] Crear 10+ badges desbloqueables:
  - 🏁 **Primera Misión** — Completar M0
  - 🧠 **Arquitecto** — Entender el sistema (M1 quiz 100%)
  - 🤖 **Domador de Agentes** — Conocer los 10 agentes (M2 quiz 100%)
  - ⚡ **Rápido y Furioso** — Completar en <90min
  - 🎯 **Francotirador** — 90%+ en todos los quizzes
  - 🔥 **Racha Perfecta** — Sin errores en quizzes
  - 📚 **Empollón** — Visitar todos los recursos extra
  - 🛠️ **Manitas** — Completar setup práctico
  - 🎓 **Graduado** — Completar todos los módulos
  - 💎 **Maestro Brain** — 100% completion + todos los badges

#### 2.3 UI de Gamificación
- [ ] Navbar mejorada:
  - XP bar animada con level-up
  - Badge showcase (3 badges visibles, click para ver todos)
  - Nivel actual con icono
- [ ] Modal de "Level Up" con animación
- [ ] Modal de "Badge Desbloqueado" con detalles

#### 2.4 Leaderboard (Opcional)
- [ ] Si hay backend: guardar scores anónimos
- [ ] Si no hay backend: leaderboard local (solo tu progreso)

**Criterios de aceptación:**
- Usuario gana XP y sube de nivel visible
- Badges se desbloquean automáticamente al cumplir criterios
- Animaciones de recompensa se muestran

---

### FASE 3: Contenido Visual (Semana 3)
**Objetivo:** Hacer el contenido más comprensible con diagramas y ejemplos

#### 3.1 Diagramas Interactivos
- [ ] M1: Diagrama del flujo de agentes (click en cada agente → detalles)
- [ ] M2: Cards de agentes con iconos + animación hover
- [ ] M3: Visualización de la memoria (grafo de learnings/clusters)
- [ ] M5: Timeline interactivo del primer ciclo

#### 3.2 Ejemplos por Tipo de Tarea
- [ ] Crear 8 ejemplos visuales (screenshots o demos):
  - Software: dashboard de datos
  - Research: análisis comparativo
  - Escritura: SOP document
  - Operaciones: checklist automatizada
  - Creatividad: brainstorming estructurado
  - Análisis: visualización de CSV
  - Estrategia: roadmap de producto
  - Conocimiento: mapa mental Obsidian

#### 3.3 Micro-videos (Opcional)
- [ ] Grabar 6 videos cortos (2-3min cada uno):
  - M0: Bienvenida y qué esperar
  - M1: Tour del sistema
  - M2: Los agentes en acción
  - M3: Cómo funciona la memoria
  - M4: Setup paso a paso
  - M5: Ciclo completo en tiempo real

**Criterios de aceptación:**
- Cada módulo tiene al menos 2 elementos visuales
- Los diagramas son interactivos (hover/click)
- Ejemplos son relevantes para el perfil seleccionado

---

### FASE 4: Casos Prácticos por Perfil (Semana 4)
**Objetivo:** Que cada usuario vea ejemplos de SU tipo de trabajo

#### 4.1 Casos por Perfil

**No-programador:**
- [ ] Ejemplo: Writer creando SOPs de procesos
- [ ] Ejemplo: Operador automatizando reportes semanales
- [ ] Ejemplo: Negocios analizando datos de ventas

**Junior-dev:**
- [ ] Ejemplo: Debuggear código con el critic
- [ ] Ejemplo: Refactorizar módulo legacy
- [ ] Ejemplo: Crear tests automatizados

**Consultor:**
- [ ] Ejemplo: Análisis de datos de cliente (CSV → insights)
- [ ] Ejemplo: Generar propuestas comerciales
- [ ] Ejemplo: Seguir múltiples proyectos con hubs

**Equipo pequeño:**
- [ ] Ejemplo: Onboarding de nuevo miembro
- [ ] Ejemplo: Retrospectiva de sprint
- [ ] Ejemplo: Documentación compartida

**Estudiante:**
- [ ] Ejemplo: Resumir papers académicos
- [ ] Ejemplo: Organizar apuntes de clase
- [ ] Ejemplo: Preparar presentaciones

#### 4.2 Sandbox de Práctica (Opcional)
- [ ] Modo "práctica guiada" con tarea predefinida
- [ ] El sistema simula ser OpenCode
- [ ] Feedback paso a paso sin instalar nada

**Criterios de aceptación:**
- Cada perfil tiene 3 casos prácticos específicos
- Los ejemplos son realistas y detallados
- El usuario puede ver el output esperado

---

### FASE 5: Certificado y Export (Semana 5)
**Objetivo:** Que el usuario pueda demostrar lo aprendido

#### 5.1 Certificado PDF
- [ ] Generar PDF con:
  - Nombre del usuario
  - Perfil completado
  - Fecha de finalización
  - XP total y nivel
  - Badges desbloqueados
  - Score de quizzes
  - Tiempo total
  - QR code para verificar autenticidad
- [ ] Diseño profesional (usar plantilla)
- [ ] Firmado digitalmente (opcional)

#### 5.2 Export Mejorado
- [ ] JSON actual incluye:
  - Perfil seleccionado
  - XP y nivel
  - Badges desbloqueados
  - Detalles de quizzes por módulo
  - Tiempo por módulo
- [ ] Opción de compartir en LinkedIn/Twitter

**Criterios de aceptación:**
- PDF se genera y descarga automáticamente
- El certificado es visualmente profesional
- Los datos de export son completos

---

### FASE 6: Pulido y Lanzamiento (Semana 6)
**Objetivo:** QA, testing con usuarios reales, launch

#### 6.1 Testing con Usuarios
- [ ] Reclutar 5-10 beta testers (1 por perfil)
- [ ] Recoger feedback estructurado
- [ ] Iterar sobre puntos de fricción

#### 6.2 Analytics (Opcional)
- [ ] Tracking de eventos:
  - Módulo completado
  - Quiz respondido
  - Badge desbloqueado
  - Tiempo en cada módulo
  - Abandono (punto de salida)
- [ ] Dashboard para ver métricas

#### 6.3 Landing Page de Venta
- [ ] Página de venta con:
  - Propuesta de valor clara
  - Testimonios de beta testers
  - Demo del sistema
  - Precio y CTA
  - FAQ
- [ ] Integración con sistema de pago (Gumroad, LemonSqueezy, etc.)

#### 6.4 Documentación
- [ ] README para compradores
- [ ] Guía de troubleshooting
- [ ] Video de setup

**Criterios de aceptación:**
- 5+ usuarios reales han completado la plataforma
- Feedback promedio > 4/5
- Landing page funcional con pago

---

## 📈 Métricas de Éxito

| Métrica | Línea base | Objetivo v2.0 |
|---------|------------|---------------|
| Completion rate | ~40% | 75% |
| Tiempo promedio | 120min | 90min |
| Quiz score avg | 60% | 85% |
| NPS | N/A | >50 |
| Refunds | N/A | <5% |

---

## 🛠️ Stack Técnico

### Frontend
- HTML/CSS/JS vanilla (mantener portabilidad)
- Chart.js para visualizaciones (opcional)
- jsPDF para generar certificados PDF

### Backend (Opcional)
- Netlify Functions o Vercel Serverless
- Supabase o Firebase para leaderboard
- Gumroad/LemonSqueezy para pagos

### Herramientas
- Figma para diseño de badges/certificados
- Loom para grabar micro-videos
- Google Forms para feedback de beta testers

---

## 📋 Tareas Inmediatas (Próximos 7 días)

### Día 1-2: Sistema de Perfiles
- [ ] Crear `profiles.json` con los 5 perfiles
- [ ] Modificar `modules.json` para soportar perfiles
- [ ] Actualizar `platform.js` para cargar contenido por perfil
- [ ] Añadir pantalla de selección de perfil en onboarding

### Día 3-4: Gamificación Básica
- [ ] Implementar sistema de XP y niveles
- [ ] Crear 5 badges iniciales
- [ ] Añadir UI de XP bar y nivel en navbar
- [ ] Modal de level-up

### Día 5-7: Contenido Visual M1-M2
- [ ] Diagrama interactivo del flujo (M1)
- [ ] Cards de agentes mejoradas (M2)
- [ ] Ejemplos visuales de tipos de tarea

---

## 🔗 Archivos Relacionados

- `learning-platform/modules.json` — Contenido actual
- `learning-platform/platform.js` — Lógica de la plataforma
- `learning-platform/index.html` — Estructura HTML
- `learning-platform/ntizar.css` — Estilos personalizados
- `agents/learnings/_index.md` — Learnings del sistema
- `agents/projects/learning-platform.md` — Hub del proyecto

---

*Roadmap creado: 2026-03-25*
*Última actualización: 2026-03-25*
*Versión: 2.0-draft*
