# Guía de diseño de demos (anti-plantilla, anti-slop)

Espejo del archivo `plantillas/GUIA-DISENO.md` del repo prospeccion-mvp.
Esta guía NO define un layout: define el nivel de calidad y las reglas fijas.
Nacida de la corrección explícita del cliente (ago-2026): *"el problema es la plantilla,
cierra demasiado cómo tiene que ser la web; quiero más margen para inventar cosas mejores"*.

## Proceso por negocio

1. Escrapear su web actual: estructura de secciones, menú, textos reales, servicios, contactos,
   fotos (a `demos/<slug>/img/`), colores de marca reales (del logo, no del CSS del CMS).
2. Identificar su negocio de verdad: ¿tienda/showroom? ¿urgencias 24h? ¿obras? El hero y las
   secciones responden a ESO, no a un arquetipo genérico.
3. Escribir el HTML completo desde cero: composición, tipografía, ritmo y secciones nacen del
   negocio. **Si dos demos de negocios distintos comparten estructura, está mal hecho.**
   Casos validados: Tenofransa = corporativa-industrial con lista numerada de 9 servicios;
   La Cañada = banda 24h pulsante + 3 teléfonos como sección + sección oscura para su
   diferencial (trasteros); Aluche = showroom/catálogo con "desde 1968".

## Reglas fijas (innegociables)

- `<meta name="robots" content="noindex, nofollow">` + banner de disclosure arriba:
  "Demo conceptual — propuesta no oficial para [Negocio]. No es su web."
- Contacto SOLO el publicado por el negocio (tel:, mailto:, wa.me con sus números).
  Dato no verificado → "(a confirmar)". Nunca inventar.
- Fotos: las suyas, optimizadas (<250 KB), en `img/`. Sin stock ni placeholders vacíos.
- Colores: su marca real. Sin gradientes morados, sin emojis decorativos en títulos,
  sin "✨ Soluciones innovadoras".
- Todo botón de contacto funcional (`tel:`, `mailto:`, `wa.me/34XXXXXXXXX`). Nada de "#".
- Móvil primero: barra de contacto fija abajo, tap targets grandes, sin scroll horizontal.
- Rendimiento: una página, cero dependencias externas, <500 KB total con fotos.

## Anti-slop (si aparece, se rechaza)

- Filas de 3 tarjetas idénticas con icono-emoji + título + párrafo de relleno.
- Texto que no diría el dueño: "soluciones a medida", "excelencia", "pasión por...".
- Secciones porque sí (testimonios inventados, contadores falsos, logos de clientes).
- Templado visual idéntico entre dos negocios distintos.
- Promesas de resultado ("garantizamos", "el mejor precio de Madrid").

## Personalidad por tipo de negocio (orientativo, NUNCA molde)

- Urgencias 24h: teléfono gigante arriba, tono directo, prueba técnica (equipos, método),
  cobertura por zonas.
- Comercio/showroom: producto y visita primero, catálogo, dirección y horario visibles.
- Profesional/estudio: obra y método, sobriedad, sin urgencia falsa.

El resto lo decide quien escribe la web mirando lo que el negocio ya es.

## Nota del cliente sobre SU plantilla de ventas (no de las demos)

La página de venta de David (presentación de la oferta) va en blanco + azul + naranja con
liquid glass sobre blanco — excepción deliberada que ÉL pide para su marca, pese a que
normalmente rechaza liquid glass y dark themes. Las demos de los NEGOCIOS siguen su marca.
