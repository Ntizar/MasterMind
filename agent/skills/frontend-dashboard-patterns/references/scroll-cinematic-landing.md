# Scroll Cinematic Landing — Patrón de Landing Inmersiva

Patrón para landings de pantalla completa con scroll que "viaja" por secciones con efecto cinemático.

## Caso de uso
- Landing de ciudades, proyectos creativos, portafolios
- Efecto "scroll-world" (viaje inmersivo al hacer scroll)
- Experiencias de storytelling visual

## Arquitectura

### Estructura de archivos
```
proyecto/
├── index.html          ← Estructura DOM con secciones
├── style.css           ← Estilos: fullscreen panels, transiciones, parallax
├── script.js           ← Lógica de scroll: wheel, touch, keyboard
└── README.md
```

### HTML — Secciones como panels
```html
<section class="panel" id="hero">
  <div class="bg-image" style="background-image: url('...');"></div>
  <div class="content">
    <h1>TÍTULO</h1>
    <p>Descripción</p>
  </div>
</section>
```

**Regla:** Cada panel = 100vh, position absolute, opacity 0 por defecto. Solo el `.panel.active` es visible.

### CSS — Transición cinemática
```css
.panel {
  position: absolute;
  width: 100%; height: 100%;
  opacity: 0; visibility: hidden;
  transition: opacity 0.5s ease-out, visibility 0.5s;
}
.panel.active { opacity: 1; visibility: visible; z-index: 2; }

.bg-image {
  position: absolute;
  top: -10%; left: -10%;
  width: 120%; height: 120%;
  background-size: cover;
  transform: scale(1.1);          /* Start zoomed */
  transition: transform 8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  filter: brightness(0.6);
}
.panel.active .bg-image {
  transform: scale(1.0);          /* Scrub out to normal */
}

.content {
  opacity: 0; transform: translateY(30px);
  transition: all 1s cubic-bezier(0.16, 1, 0.3, 1) 0.3s;
}
.panel.active .content {
  opacity: 1; transform: translateY(0);
}
```

**Claves:**
- `scale(1.1)` → `scale(1.0)` crea efecto de "zoom out" cinemático al activar
- `brightness(0.6)` en bg-image para legibilidad del texto
- `cubic-bezier(0.25, 0.46, 0.45, 0.94)` para transición suave tipo "ease-out-quad"
- Delay de 0.3s en `.content` para que el fondo aparezca primero

### JS — Scroll-to-panel navigation
```javascript
let currentPanel = 0;
let isScrolling = false;

window.addEventListener('wheel', (e) => {
  if (isScrolling) return;
  if (e.deltaY > 0 && currentPanel < total - 1) {
    isScrolling = true;
    panels[currentPanel].classList.remove('active');
    currentPanel++;
    panels[currentPanel].classList.add('active');
    setTimeout(() => isScrolling = false, 800);
  }
  // ... similarly for scroll up
});
```

**Patrones de input soportados:**
- `wheel` — Desktop scroll
- `touchstart`/`touchend` — Mobile swipe ( threshold > 50px)
- `keydown` — Arrow keys, Space, Enter
- Anti-doble-scroll: flag `isScrolling` + timeout de 800ms

## Fuentes de imágenes
- Unsplash API: `https://images.unsplash.com/photo-ID?auto=format&fit=crop&q=80&w=1920`
- Buscar por ciudad/tema: `?q=madrid+skyline`, `?q=gran+via+night`

## Pitfalls

- **NO usar `overflow-y: scroll` en body** — El scroll lo controla el JS, no el navegador. Usar `overflow: hidden` y manejar wheel/touch manualmente.
- **Imágenes pesadas** — Usar `w=1920` en Unsplash para balance calidad/peso. No usar original.
- **Transiciones demasiado rápidas** — El efecto cinemático necesita tiempos largos (5-8s para bg-image scale). Si es muy rápido, parece un slideshow, no un viaje.
- **Touch en mobile** — El threshold de 50px evita swipes accidentales. Sin esto, el scroll es errático.
- **Z-index** — Solo `.panel.active` debe tener `z-index: 2`. Los demás en `z-index: 1` para que las transiciones de opacidad funcionen correctamente.

## Ejemplo real
- Repo: `Ntizar/NtizarMadrid` — Landing de la ciudad de Madrid con scroll cinemático
- Efecto: Full-screen images de landmarks con zoom-out al hacer scroll
