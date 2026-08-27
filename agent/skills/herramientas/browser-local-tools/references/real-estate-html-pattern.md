# Real Estate Property Cards - HTML Pattern

## Context
Creating technical property cards for apartments from architectural PDFs. The workflow extracts data from PDF, creates SVG floor plans, CSS-styled interior renders, and deploys to GitHub Pages.

## Architecture

```
fichas-residencia-tajo/
├── index.html              # Landing page
├── fichas_completas.html   # All apartments in tabs
├── planos_2d.html         # SVG floor plans
├── renders_interiores.html # CSS interior renders
├── fichas_apartamentos/   # Individual fichas
│   ├── index.html
│   └── apartamento_01.html ... apartamento_09.html
└── .github/workflows/deploy.yml
```

## SVG Floor Plans Pattern

Color-coded zones with labels:

```html
<svg viewBox="0 0 400 280" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect x="0" y="0" width="400" height="280" fill="#fafafa"/>
    
    <!-- Outer walls -->
    <rect x="20" y="20" width="360" height="240" fill="none" stroke="#333" stroke-width="3"/>
    
    <!-- Bedroom (green) -->
    <rect x="20" y="20" width="240" height="160" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
    <text x="140" y="100" text-anchor="middle" font-size="11" fill="#333">Habitación</text>
    <text x="140" y="115" text-anchor="middle" font-size="9" fill="#666">18.50 m²</text>
    
    <!-- Kitchen (orange) -->
    <rect x="260" y="20" width="120" height="90" fill="#fff3e0" stroke="#333" stroke-width="2"/>
    <text x="320" y="70" text-anchor="middle" font-size="10" fill="#333">Cocina</text>
    
    <!-- Bathroom (blue) -->
    <rect x="260" y="110" width="120" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
    <text x="320" y="150" text-anchor="middle" font-size="10" fill="#333">Baño</text>
    
    <!-- Window (cyan line) -->
    <line x1="80" y1="20" x2="140" y2="20" stroke="#2196f3" stroke-width="3"/>
</svg>
```

## CSS Interior Renders Pattern

Minimalist Scandinavian style with position absolute for furniture:

```css
/* Bedroom */
.render-dormitorio { background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%); }
.bed { 
    position: absolute; bottom: 50px; left: 20px; 
    width: 100px; height: 50px; 
    background: white; border-radius: 4px; 
    box-shadow: 0 2px 6px rgba(0,0,0,0.15); 
}
.bed::before { 
    content: ''; position: absolute; top: 5px; left: 5px; right: 5px; 
    height: 20px; background: #e3f2fd; border-radius: 2px; 
}

/* Kitchen */
.render-cocina { background: linear-gradient(180deg, #fff3e0 0%, #ffe0b2 100%); }
.counter { 
    position: absolute; bottom: 40px; left: 10px; right: 10px; 
    height: 40px; background: #e0e0e0; border-radius: 2px; 
}
.counter::before { 
    content: ''; position: absolute; top: 0; left: 0; right: 0; 
    height: 6px; background: #757575; border-radius: 2px 2px 0 0; 
}

/* Bathroom */
.render-bano { background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 100%); }
.shower { 
    position: absolute; top: 20px; left: 20px; 
    width: 60px; height: 80px; 
    background: white; border-radius: 4px; border: 2px solid #e0e0e0; 
}

/* Living room */
.render-salon { background: linear-gradient(180deg, #f3e5f5 0%, #e1bee7 100%); }
.sofa { 
    position: absolute; bottom: 50px; left: 20px; 
    width: 120px; height: 40px; 
    background: linear-gradient(180deg, #5d4037 0%, #4e342e 100%); 
    border-radius: 6px 6px 2px 2px; 
}
```

## GitHub Pages Deployment

**Workflow file:** `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ master ]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with: { path: '.' }
      - uses: actions/deploy-pages@v4
        id: deployment
```

## Export to PDF Instructions

1. Open page in browser (Chrome recommended)
2. Ctrl+P (Cmd+P on Mac)
3. Destination: "Save as PDF"
4. Layout: Landscape
5. Margins: Minimum
6. Scale: Adjust to fit
7. Click "Save"

## Pitfalls

- **Image generation unavailable:** When FAL_KEY or other image gen provider is not configured, fall back to HTML/CSS stylized renders — they are often better for technical documentation anyway.
- **GitHub Pages deployment:** Initial deployment takes 2-5 minutes. Do not report failure until waiting at least 3 minutes.
- **SVG text centering:** Always use `text-anchor="middle"` for centered labels.
- **CSS renders:** Use `position: absolute` for furniture placement within containers with `position: relative`.
