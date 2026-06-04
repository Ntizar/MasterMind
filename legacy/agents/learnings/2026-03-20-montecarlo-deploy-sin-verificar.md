---
fecha: 2026-03-20
tarea: montecarlo-deploy-sin-verificar
tipo: operaciones
complejidad: baja
clusters: [github]
proyecto: montecarlo
patron: verify-before-deliver
---

# Verificar deploy antes de entregar — no asumir que funciona

## Decisión clave
Hacer push no es suficiente — hay que verificar que el site live refleja los cambios antes de decirle al humano que está hecho.

## Patrón reutilizable
sí → verify-before-deliver

Después de cualquier deploy, hacer WebFetch al site live e inspeccionar el HTML para confirmar que los cambios están presentes. Solo entonces dar el ciclo por cerrado.

Señales a buscar en el HTML:
- Texto o IDs específicos del cambio (ej: `pdfHeaderBtn`, texto de versión en footer)
- Que NO aparezca contenido de versiones anteriores

## Qué funcionó
- WebFetch a la URL live confirma el estado real del site sin depender de lo que diga GitHub

## Qué evitar
- No dar por bueno un deploy solo porque git push salió sin errores
- No asumir que GitHub Pages está bien configurado en repos nuevos o heredados — verificar siempre la configuración de Pages (rama, carpeta) antes de trabajar
- No esperar a que el humano reporte que la web no carga para investigar el problema de deploy

## Skills usados
- ninguno

## Tests/criterios que validaron esto
- WebFetch al site live mostró pdfHeaderBtn y tab Contexto en el HTML — confirmación directa

## Conexiones
**Cluster:** #github
**Proyecto:** [[montecarlo]]
**Aprendizajes relacionados:** [[2026-03-20-montecarlo-github-pages-subdirectory]] · [[2026-03-20-montecarlo-v35-context-pdf-screener]]
