# Guía de Estilo HTML para Resúmenes de Documentos Institucionales

## Sistema de diseño

### Colores
- Azul principal: `#2563eb`
- Azul claro (fondos): `#dbeafe`
- Naranja acento: `#f97316`
- Naranja claro (fondos warning): `#ffedd5`
- Gris oscuro texto: `#1e293b`
- Gris medio: `#64748b`
- Gris claro fondo: `#f1f5f9`
- Blanco: `#ffffff`
- Verde éxito: `#22c55e`
- Rojo alerta: `#ef4444`
- Amarillo: `#eab308`

### Componentes

#### Hero (cabecera)
```css
linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #3b82f6 100%)
```
Título blanco grande + subtítulo + badge con metadatos del documento.

#### Tarjetas KPI (summary-cards)
Grid responsive de 4 columnas (auto-fit minmax 220px). Cada tarjeta:
- Borde izquierdo de 4px según tipo (azul estándar, naranja warning, rojo danger, verde success)
- Número grande (1.8rem) en color correspondiente
- Label descriptivo debajo en gris

#### Tablas
- Cabecera azul con texto blanco
- Filas pares con fondo `#f8fafc`
- Hover en azul claro `#dbeafe`
- Border-bottom sutil `#e2e8f0`

#### Highlight boxes
Fondo de color + borde izquierdo de 4px:
- Azul: info general
- Naranja: warning/atención
- Rojo: dato crítico

#### Conclusion cards (conclusion-item)
Fondo `#fffbeb` + borde izquierdo naranja + padding 1rem.

### Responsive
- Container max-width 1100px
- En móvil (<640px): hero font reducido, padding 1rem en container y section

### Reglas
- Sin dependencias externas (no CDN, no fuentes externas)
- Todo en un solo archivo HTML autónomo
- Estilo inline en `<style>` dentro del `<head>`
- JS no necesario (puro HTML+CSS)

### Secciones estándar
1. Hero (título, subtítulo, badge)
2. Summary cards (4 KPIs principales)
3. Resumen ejecutivo con highlight box
4. Tablas de datos principales
5. Comparativas €/km o tiempo/ruta
6. Análisis de impacto (si aplica)
7. Escenarios / internalización (si aplica)
8. Conclusiones / recomendaciones
9. Metodología breve
10. Footer con fuente