# CIAF Visor — Referencia: Guía de Handoff Completa

**Proyecto:** CIAF-visor (https://ntizar.github.io/CIAF-visor/)  
**Fecha:** 2026-07-02  
**Resultado:** `/root/workspace/CIAF-visor/GUIA-CODIGO-CIAF-VISOR.md` (24 KB)

## Qué se documentó

- **1735 líneas** de `frontend/index.html` (HTML + CSS + JS monolítico) → explicadas en 29 bloques
- **4 scripts Python** de pipeline de datos → explicados con flujos y dependencias
- **Esquemas de datos** → JSON de informes y memorias con ejemplos reales
- **Despliegue** → GitHub Pages, workflow automático
- **Errores conocidos** → cross-reference por expediente, geolocalización por PK

## Estructura del output

El `.md` generado tiene 7 secciones:
1. Qué es el CIAF Visor (no técnico)
2. Estructura del proyecto (árbol comentado)
3. Sistema de datos (esquemas JSON)
4. Frontend por bloques (29 subsecciones con código + explicación)
5. Scripts del pipeline (4 scripts con flujos)
6. Despliegue y mantenimiento
7. Errores conocidos

## Patrón de lectura aplicado

1. Inventario: `search_files` por extensiones (.html, .js, .json, .py)
2. README → entender qué es el proyecto
3. `index.html` completo (1735 líneas) → dividir en bloques CSS/HTML/JS
4. Scripts Python → entender pipeline de datos
5. JSONs de ejemplo → documentar esquemas
6. Generar guía consolidada

## Lecciones

- **Archivos monolíticos grandes** (1735 líneas) se documentan dividiendo por secciones marcadas con comentarios (`/* ===== HEADER ===== */`), no por líneas arbitrarias
- **Los JSONs de datos son parte de la documentación** — incluir ejemplos reales con campos explicados
- **Los scripts de pipeline son críticos** — sin ellos, el proyecto no se puede actualizar
- **Incluir "errores conocidos"** es el valor más alto para el siguiente mantenedor
