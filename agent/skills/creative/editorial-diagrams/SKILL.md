---
name: editorial-diagrams
version: "1.0.0"
description: "Use al crear diagramas editoriales claros en HTML+SVG."
tags: [diagrams, svg, html, visualization, editorial, documentation]
---

# Editorial Diagrams — diagram-design (cathrynlavery)

Repo: https://github.com/cathrynlavery/diagram-design (MIT, ~28K⭐). Skill de agente: produce diagramas "que tu diseñador no odiará" — HTML+SVG autocontenido, sin sombras, sin cajas redondeadas genéricas de Mermaid.

## Cuándo usarlo
- Diagramas editoriales para posts, docs, informes (David: fondo claro, sin dark themes).
- 39 tipos: arquitectura, flujo, pirámide, Sankey, fishbone (ishikawa), Wardley map, kanban, user journey, deployment, grafo de dependencias, UML class, story map, database schema, flywheel "Loop" (2.0: hub de memoria compartida con write-backs punteados), etc.
- Redibujar fuentes draw.io o Mermaid existentes a un formato/tamaño/nivel de detalle elegido.

## Filosofía de diseño (reglas clave)
1. **Semántica separada del layout**: los "patrones semánticos" describen comportamiento (cola, traza de política, frontera de confianza) y se mapean al tipo de layout más cercano — NO crear un tipo nuevo por cada caso.
2. **HTML estático por defecto**; movimiento solo opcional para explicaciones ordenadas (accesible).
3. Sin Figma, sin cajas genéricas, sin sesiones de 30 min eligiendo colores.
4. Output: un único archivo `.html` autocontenido con SVG inline — funciona offline.

## Workflow
1. Identifica el **tipo de diagrama** más cercano al contenido (no inventes topología).
2. Escribe el HTML+SVG a mano siguiendo la estética editorial: tipografía cuidada, líneas limpias, etiquetas junto a los flujos, dashed lines solo para write-backs/fronteras.
3. Guarda con `write_file` y abre en navegador. Exportable vía captura.
4. Si el origen es Mermaid/draw.io: parsea la estructura y redibuja al tipo editorial correspondiente.

## Pitfalls
- No mezclar dark-theme infra (ver `creative/architecture-diagram`) con este estilo: este skill es para estética editorial clara.
- Los dashed lines tienen significado semántico (write-back en el Loop, fronteras) — no decorativas.
- Elegir el tipo por el CONTENIDO, no por costumbre: un user journey no es un flowchart.

## Verificación
- El HTML se abre en cualquier navegador offline.
- Cada nodo/flujo tiene etiqueta legible; leyenda fuera del área de dibujo.
- Un observador entiende el mensaje en <10 s sin explicación.

## Comparativa de alternativas

- **[LiamGvchi/gc-minimal-zine-poster](https://github.com/LiamGvchi/gc-minimal-zine-poster)** — skill Codex que lleva tema/idea/foto a un sistema visual editorial tipo poster (focal + acento cromático), complementando el enfoque de diagramas con un estilo de póster editorial minimalista.
