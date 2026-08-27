# Patrón: Página de Documentación Responsive con Tabs

## Contexto

Cuando un proyecto técnico tiene múltiples artefactos interconectados (DECISIONES.md, README, spec, código, validador, ejemplos), crear una página HTML responsive con tabs que explique todo el proyecto a técnicos externos.

## Estructura del HTML

```
app/docs.html
├── Hero (título + badges + links)
├── Nav tabs sticky (6+ secciones)
├── Sections (una por tab):
│   ├── Overview — qué es, por qué, métricas
│   ├── Estructura — diagramas de entidades
│   ├── Decisiones — cada decisión con por qué, pros/contras
│   ├── Comparativa — tabla con alternativas
│   ├── Validador — módulos, reglas, clasificación
│   └── Uso — CLI, API, UI, resultados
└── Footer (atribución)
```

## Estilo

- **Aurora Ntizar**: azul `#2563eb` + naranja `#f97316`, fondo blanco `#fafafa`
- **Responsive**: `@media (max-width: 640px)` con grid-column: 1fr, padding reducido
- **Sin dependencias**: CSS puro, JS vanilla
- **Diagramas ASCII**: clases `.diagram`, `.indent`, `.label`, `.ref`
- **Decision blocks**: borde izquierdo azul, grid de pros/contras
- **Alert boxes**: warning (naranja), info (azul), success (verde)

## JS mínimo

```javascript
// Tab navigation
document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
```

## Reglas

1. **Siempre incluir atribución**: "Hecho con ❤️ por David Antizar"
2. **Siempre incluir link al repo**
3. **Los diagramas deben ser ASCII-art legible**, no imágenes
4. **Las decisiones deben tener pros Y contras**, nunca solo ventajas
5. **Las comparativas deben incluir alternativas reales**, no solo "nosotros vs nadie"
6. **El HTML debe ser autocontenido**: un solo archivo, sin CSS/JS externo

## Ejemplo

Ver `app/docs.html` en el proyecto NeTEx-ES (`/root/workspace/netex/app/docs.html`).
