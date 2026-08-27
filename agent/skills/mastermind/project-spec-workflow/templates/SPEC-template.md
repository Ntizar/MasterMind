# [Nombre del proyecto] — SPEC

> **Generado por:** Mastermind con skill `project-spec-workflow`
> **Fecha:** [YYYY-MM-DD]

---

## Visión

[1 frase: qué es y para qué]

## Alcance

### Sí hace
- [feature 1]
- [feature 2]
- [feature 3]

### NO hace (non-goals)
- [non-goal 1]
- [non-goal 2]
- [non-goal 3]

## Pantallas

1. **[Pantalla 1]** — [descripción]
2. **[Pantalla 2]** — [descripción]
3. **[Pantalla 3]** — [descripción]

## Datos

| Fuente | Tipo | Actualización | Volumen |
|--------|------|---------------|---------|
| [fuente 1] | [API/JSON] | [frecuencia] | [tamaño] |
| [fuente 2] | [API/JSON] | [frecuencia] | [tamaño] |

## Arquitectura

### Capas

| Capa | Archivo | Responsabilidad | NO hace |
|------|---------|----------------|---------|
| **Estado** | js/state.js | Estado global, flags de carga | No renderiza, no hace fetch |
| **API** | js/api.js | Fetch de APIs, normalización | No guarda estado, no renderiza |
| **UI** | js/ui.js | Eventos, panels, interacción | No hace lógica de datos |
| **Render** | js/render.js | Gráficos, mapa, tablas | No hace fetch, no gestiona estado |

### Estado global

```javascript
const Estado = {
  datos: {
    // un campo por fuente de datos
  },
  ui: {
    tabActiva: 'panel',
    cargando: false,
  },
  cargado: {
    // un flag por módulo (lazy load)
  }
};
```

**Regla:** Ningún otro archivo modifica `Estado` directamente. Usan funciones de state.js.

### Interfaces entre módulos

```
state.js expone:
  - setDato(clave, valor)
  - getDato(clave)

api.js expone:
  - fetch[Source]() → Promise<datos>

[modulo].js expone:
  - init[Modulo]()
  - render[Modulo](params)
```

## Stack

- **Frontend:** [tecnologías]
- **Deploy:** [plataforma]

## Criterios de éxito

- [métrica 1: ej, carga en < 3s]
- [métrica 2: ej, click → respuesta < 500ms]
- [métrica 3]

## Anti-patrones (lo que evitamos)

- ❌ [patrón 1]
- ❌ [patrón 2]
- ❌ [patrón 3]

## Referencias

- [proyectos similares del usuario]
- [links de inspiración]

---

*Hecho con ❤️ por David Antizar — Mastermind es ejecutor, David es autor.*
