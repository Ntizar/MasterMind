# PLANDEMOVILIDAD v3.0 — Ejemplo de Spec para Rewrite

## Contexto
Proyecto existente con CSS roto (selectores ID vs clase), JS desconectado (10+ módulos huérfanos), e informe insuficiente (10 páginas vs 60-80 necesarias).

## Patrón de auditoría aplicado
1. Leer todos los archivos (1 HTML, 1 CSS, 17 JS)
2. Tabla de mismatches CSS↔HTML (20+ selectores rotos)
3. Mapeo de funciones llamadas vs implementadas (16 no implementadas)
4. Grafo de dependencias de módulos
5. Clasificación por severidad

## Estructura de la spec generada
La spec incluye:
- **Visión** + alcance (sí/no hace)
- **Estructura del informe** como tabla con 22 secciones y páginas estimadas
- **Arquitectura** con capas y diagrama de archivos
- **Estado global** detallado con schema JavaScript
- **Módulos detallados** — cada módulo nuevo con API de funciones
- **Datos estáticos** — catálogos, normativa, ciudades GBFS
- **CSS** — paleta exacta y reglas
- **Stack técnico** con CDN
- **Iteraciones** — 6 fases con archivos afectados
- **Criterios de éxito** — 12 tests concretos
- **Anti-patrones** — 8 reglas explícitas

## Lecciones aprendidas
- Para rewrites, la spec debe ser MÁS detallada que para proyectos nuevos (porque hay código existente que reconciliar)
- Incluir tablas de CSS mismatches directamente en la spec ayuda a que el implementador sepa exactamente qué cambiar
- El schema de estado global es crítico — define el contrato entre módulos
- Las APIs externas (NAP, GBFS, ORS) necesitan secciones detalladas con endpoints exactos

## Archivo completo
Ver: `/root/workspace/PLANDEMOVILIDAD/SPEC.md` (25KB)
