# Preferencias de David — Cards y KPIs

## ❌ NUNCA hacer
- `border-left: 4px solid #color` en cards/KPIs → "se nota mucho que es IA"
- Glass/blur/saturate effects → rechazado en v1
- Diseño "liquid glass" → "el diseño es bastante mierda"
- Puntos/círculos en mapas → "deben ser áreas"

## ✅ SÍ hacer
- **Gradientes sutiles de fondo** por tipo de KPI
- **Hover elevación** con box-shadow + translateY
- **Fondo blanco sólido** (#ffffff) con borde sutil (#e2e8f0)
- **Border radius** 10px (KPIs) / 12px (cards)
- **Choropleths** con GeoJSON real, no puntos

## CSS de referencia (DataHub España v2.1)

```css
.kpi {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    transition: all 0.2s ease;
}
.kpi:hover {
    background: #ffffff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transform: translateY(-1px);
}
.kpi.green { background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%); }
.kpi.orange { background: linear-gradient(135deg, #fff7ed 0%, #ffffff 100%); }
.kpi.red { background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%); }
.kpi.blue { background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%); }

.card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
```

## Paleta oficial
- Background: `#f8fafc`
- Cards: `#ffffff` + `border: 1px solid #e2e8f0`
- Texto primario: `#0f172a`
- Texto secundario: `#64748b`
- Labels KPI: `#94a3b8`
- Azul: `#2563eb`
- Naranja: `#f97316`
- Verde: `#16a34a`
- Rojo: `#dc2626`
