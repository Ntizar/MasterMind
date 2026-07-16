---
name: ez-tree
description: Visualización de árboles y grafos en 3D — útil para datos jerárquicos y mapas de decisión.
version: "1.0.0"
tags: [3D, trees, graphs, visualization, hierarchy, three.js]
---

# EZ-Tree — Visualización 3D de Árboles y Grafos

## Resumen

Visualización de árboles y grafos en 3D — útil para datos jerárquicos y mapas de decisión. 1.4k⭐.

## Repo de referencia

- **GitHub:** `github.com/dgreenheck/ez-tree`
- **Lenguaje:** JavaScript
- **Licencia:** MIT

## Instalación

```bash
npm install ez-tree
# o
git clone https://github.com/dgreenheck/ez-tree.git
cd ez-tree && npm install
```

## Uso Básico

```javascript
import EzTree from 'ez-tree';

const tree = new EzTree({
  container: '#tree-container',
  data: {
    name: 'Root',
    children: [
      { name: 'A', children: [
        { name: 'A1' },
        { name: 'A2' }
      ]},
      { name: 'B', children: [
        { name: 'B1' }
      ]}
    ]
  },
  layout: 'radial',  // 'radial', 'hierarchical', 'force'
  colors: ['#2563eb', '#f97316', '#10b981'],
});

tree.render();

// Interacción
tree.on('click', (node) => {
  console.log('Clicked:', node.name);
});
```

## Patrones Clave

1. **Layouts:** Radial, hierárquico, force-directed
2. **Interacción:** Click, hover, zoom, pan
3. **Custom:** Colores, tamaños, formas personalizables
4. **Animation:** Transiciones suaves entre layouts
5. **Export:** PNG, SVG de la visualización

## Integración con Mastermind

- Complementa `threejs-3d-maps` — visualización jerárquica vs geoespacial
- Útil para `competitive-intelligence` — mapas de competencia
- Ideal para `dspy` — visualización de programas
- Reemplaza D3.js trees para visualización 3D

## Pitfalls

- **Tamaño:** Datos muy grandes (>1000 nodos) pueden ser lentos
- **Layout:** El layout radial no siempre es el óptimo
- **Dependencias:** Requiere Three.js
- **Mobile:** Puede no funcionar bien en móviles

## Referencias

- [GitHub: dgreenheck/ez-tree](https://github.com/dgreenheck/ez-tree)
