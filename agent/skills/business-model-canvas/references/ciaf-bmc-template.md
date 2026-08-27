# CIAF BMC — Template Completo Verificado

**Fecha:** 2026-07-08  
**Proyecto:** CIAF Visor  
**Archivo:** `/root/workspace/ciaf-bmc/index.html`  
**Verificado:** ✅ Se abre en navegador, estructura correcta, 9 bloques distribuidos, responsive, editable

## Implementación clave

### CSS Grid layout (5 cols × 4 rows)

```
[socios:1-2, r1-2] [recursos:2, r1-2] [actividades:3, r1] [propuesta:4, r1-2] [clientes:5, r1-2]
[canales:5, r2] [propuesta:4, r1-2] [relacion:5, r3-4] [costes:2, r3-4] [ingresos:1, r3-4]
```

### Colores por zona

- **Clientes:** `--bmc-blue: #2563eb` → barra superior azul
- **Oferta:** `--bmc-orange: #f97316` → barra superior naranja
- **Infraestructura:** `#6366f1` → barra superior índigo
- **Finanzas:** `--bmc-green: #16a34a` → barra superior verde

### Tags temporales

```html
<span class="future-tag future">ERA</span>  <!-- verde, futuro -->
<span class="future-tag current">HOY</span> <!-- azul, actual -->
```

### Secciones incluidas

1. Header oscuro con título + badge ERA
2. Stats bar con 4 KPIs
3. Leyenda de colores por zona
4. Canvas grid con 9 bloques contenteditable
5. Visión de Futuro ERA 2026+ (6 cards con prioridades)
6. Hoja de Ruta (4 fases con flechas)
7. Footer con atribución

### Responsive

- Desktop: grid 5 columnas
- Móvil (≤900px): todos en 1 columna, flechas timeline ↓

### CSS custom

~383 líneas — justificado por layout grid específico del BMC. No se puede mapear a componentes Aurora genéricos.
