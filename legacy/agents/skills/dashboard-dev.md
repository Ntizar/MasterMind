---
nombre: Dashboard Development Universal
tipo: skill
clusters: [sistema, datos]
aplica_a: datos, visualización
creado: 2026-03-19
---

# Skill: Dashboard Development — Universal

## Aplica cuando
El classifier detecta una tarea de visualización de datos en cualquiera de estas formas:
- Crear un dashboard, informe visual o herramienta exploratoria desde datos externos
- Transformar un CSV, Excel u otra fuente tabular en una herramienta visual local
- Limpiar y visualizar datos de baja calidad (Open Data, datos propios, exportaciones)
- Actualizar o extender un dashboard existente con nuevos datos o vistas

---

## Fases universales
El pipeline tiene este orden fijo. No se puede visualizar sin limpiar. No se puede limpiar sin auditar.

1. **Auditar** — Inspeccionar el dato crudo sin modificarlo: encoding, tipos, nulos, rangos, anomalías.
2. **Limpiar** — Corregir solo los problemas que impiden el análisis: encoding, tipos, nulos críticos.
3. **Transformar** — Agregar, filtrar, calcular métricas derivadas. Solo lo que el dashboard necesita.
4. **Visualizar** — Seleccionar el tipo de gráfico correcto para cada métrica. Una pregunta = un gráfico.
5. **Empaquetar** — Generar el artefacto final: fichero autocontenido ejecutable en local sin servidor.
6. **Verificar** — Abrir el artefacto en el entorno real y confirmar que los datos y visualizaciones son correctos.

---

## Decisiones clave
El planner debe tener respuesta a estas preguntas antes de que el implementer empiece:

| Pregunta | Por qué es bloqueante |
|----------|-----------------------|
| ¿Cuál es la pregunta que el dashboard debe responder? | Sin una pregunta concreta no hay criterio de éxito visual |
| ¿Cuál es el formato y encoding del dato de entrada? | Determina el método de ingesta; un encoding erróneo corrompe todo |
| ¿El dato tiene fechas? ¿En qué formato? | Las fechas en formato español (DD/MM/YYYY) necesitan conversión explícita |
| ¿Qué tecnología tiene disponible el entorno local? | Define el formato de output posible sin instalaciones adicionales |
| ¿El dashboard se actualiza o es un snapshot puntual? | Cambia radicalmente la arquitectura del artefacto |
| ¿Cuántas filas tiene el dato? ¿Supera las 100k filas? | Impacta el rendimiento del artefacto local elegido |

---

## Reglas de datos
Estas reglas aplican durante las fases de Auditar y Limpiar.

- **Leer siempre el dato antes de asumir su estructura** — el schema real casi nunca coincide con el documentado
- **Detectar encoding antes de cargar** — los datos españoles suelen ser ISO-8859-1 o Windows-1252, no UTF-8
- **Tratar las fechas DD/MM/YYYY como cadenas de texto hasta conversión explícita** — nunca asumir que la herramienta las interpreta correctamente
- **Unificar valores nulos antes del análisis**: `""`, `"-"`, `"N/A"`, `"No consta"`, `"S/D"`, `"N.D."`, `"."` son todos nulos; tratarlos igual
- **No eliminar filas con nulos sin documentar cuántas y por qué** — afecta la interpretación de los resultados
- **Auditar duplicados antes de agregar** — una fila duplicada silenciosa produce métricas incorrectas
- **No limpiar más de lo necesario para el análisis** — cada transformación extra es una fuente de error

---

## Reglas de visualización
Estas reglas aplican durante las fases de Visualizar y Empaquetar.

- **Una pregunta = un gráfico** — si un gráfico necesita leyenda extensa, son dos preguntas distintas
- **El artefacto final debe ser un fichero único autocontenido** — sin dependencias externas, sin servidor, abre en navegador o ejecuta sin instalación
- **El título del gráfico debe responder la pregunta, no describir los ejes** — "¿Cuánto creció el paro en 2023?" no "Evolución paro 2023"
- **Los colores deben funcionar en escala de grises** — accesibilidad por defecto
- **No mostrar más de 7 categorías en un gráfico de barras o pastel** — agrupa el resto en "Otros"

---

## Anti-patrones (nunca hacer)
- **Visualizar sin auditar** — los datos de Open Data casi siempre tienen sorpresas; descubrirlas después de visualizar obliga a rehacer todo
- **Asumir UTF-8** — el 60% de los ficheros de administraciones públicas españolas no son UTF-8
- **Usar el mismo gráfico para todas las preguntas** — el tipo de gráfico debe seguir al tipo de relación, no al revés
- **Mezclar la lógica de limpieza con la de visualización** — si falla algo, no sabrás en qué fase está el error
- **Generar un dashboard que requiere el fichero original para funcionar** — el artefacto final debe ser autocontenido
- **Ignorar el volumen de datos** — un artefacto HTML con 500k filas incrustadas no abrirá en un navegador normal

---

## Ciclo de reaprendizaje

Este skill aprende de cada proyecto. El protocolo es el siguiente:

### Qué captura el archiver después de cada proyecto de dashboard
En el learning file, añadir una sección `## Dashboard: datos del proyecto` con estos 5 campos:

```
fuente: [datos.gob.es / datos.madrid.es / Excel propio / otro]
encoding_encontrado: [UTF-8 / ISO-8859-1 / Windows-1252 / otro]
problema_principal: [descripción en 1 línea del mayor obstáculo de limpieza]
solucion_aplicada: [cómo se resolvió, en 1 línea]
tipo_artefacto: [HTML autocontenido / Python script / Jupyter / otro]
```

### Cuándo actúa el librarian
Cuando `agents/learnings/_index.md` acumule **≥ 2 entradas de tipo `datos`**, el librarian:
1. Lee los campos `problema_principal` + `solucion_aplicada` de todos los learnings de tipo datos
2. Identifica problemas que aparecen en ≥ 2 proyectos
3. Añade una fila por problema frecuente a la tabla de "Patrones aprendidos" a continuación
4. Actualiza la fecha de la última revisión en el campo `Revisado` de la sección Creado

### Límite de la tabla
Máximo 20 filas en la tabla de patrones. Si se supera, el librarian agrupa las entradas más antiguas en una fila "Otros patrones — ver learnings anteriores a [fecha]".

---

## Patrones aprendidos de proyectos

> Esta tabla la mantiene el librarian. Empieza vacía. No editar manualmente.
> Última revisión: —

| Fecha | Fuente | Problema encontrado | Solución aplicada | Frecuencia |
|-------|--------|---------------------|-------------------|------------|
| — | — | — | — | — |

---

## Creado
Fecha: 2026-03-19
Revisado: —
Origen: ciclo 2 del sistema — tarea dashboard-skill-md
