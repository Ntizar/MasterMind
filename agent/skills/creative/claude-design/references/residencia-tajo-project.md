# Real Estate Property Cards - Session Notes

## Project: Residencia Estudiantes Tajo

### Data Structure

9 apartments extracted from architectural PDF:

| Apt | Tipo | m² | Habitaciones | Baños | Planta |
|-----|------|-----|--------------|-------|--------|
| 1 | Estudio | 25.46 | 1 | 1 | Semisótano |
| 2 | Estudio | 26.15 | 1 | 1 | Semisótano |
| 3 | Estudio | 27.54 | 1 | 1 | Semisótano |
| 4 | Estudio | 29.22 | 1 | 1 | Semisótano |
| 5 | 1 Habitación | 30.72 | 1 | 1 | Planta Baja |
| 6 | 1 Habitación | 33.68 | 1 | 1 | Planta Baja |
| 7 | Estudio | 28.66 | 1 | 1 | Planta Primera |
| 8 | Estudio | 26.19 | 1 | 1 | Planta Segunda |
| 9 | 2 Habitaciones | 46.66 | 2 | 1 | Planta Baja |

### Room Areas (extracted from PDF)

**Apartamento 1 (25.46 m²):**
- Habitación 1: 18.50 m²
- Cocina: 2.98 m²
- Baño 1: 2.27 m²
- Salón: 1.50 m²

**Apartamento 2 (26.15 m²):**
- Habitación 1: 19.20 m²
- Cocina: 3.10 m²
- Baño 1: 2.45 m²
- Salón: 1.40 m²

**Apartamento 9 (46.66 m²) - Más grande:**
- Habitación 1: 14.20 m²
- Habitación 2: 12.80 m²
- Cocina: 5.60 m²
- Baño 1: 3.40 m²
- Salón: 10.66 m²

### SVG Floor Plan Pattern

Color coding for zones:
- Green (#e8f5e9): Dormitorios
- Orange (#fff3e0): Cocinas
- Blue (#e3f2fd): Baños
- Purple (#f3e5f5): Salones

Room labels use `text-anchor="middle"` for centering.

### CSS Render Pattern

Minimalist Scandinavian style:
- White furniture with subtle shadows
- Color-coded backgrounds per room type
- Position absolute for furniture placement
- Border-radius for soft edges

### File Structure

```
fichas-residencia-tajo/
├── index.html              # Landing page
├── fichas_completas.html   # All apartments in tabs
├── planos_2d.html         # SVG floor plans
├── renders_interiores.html # CSS interior renders
├── README.md              # Documentation
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Pages workflow
└── fichas_apartamentos/   # Individual fichas
    ├── index.html
    ├── apartamento_01.html
    └── ... (9 total)
```

### Export to PDF Instructions

1. Open page in browser (Chrome recommended)
2. Ctrl+P (Cmd+P on Mac)
3. Destination: "Save as PDF"
4. Layout: Landscape
5. Margins: Minimum
6. Scale: Adjust to fit
7. Click "Save"

### GitHub Pages

- **URL:** https://ntizar.github.io/fichas-residencia-tajo/
- **Deploy:** Automatic via GitHub Actions on push to master
- **Initial deploy time:** 2-5 minutes
