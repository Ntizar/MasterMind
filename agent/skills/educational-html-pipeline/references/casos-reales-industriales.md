# Banco de Casos Reales Industriales — Dibujo Técnico

Casos industriales concretos para cada bloque temático. Usar en secciones "Caso Real" de los HTMLs.

## Bloque 2: Proyecciones

| Tema | Caso Real |
|------|----------|
| b02-03 Vistas principales | **Biela de motor**: la biela tiene forma compleja que solo se entiende con 3 vistas. El operario CNC lee alzado+planta+perfil para fabricarla. |
| b02-04 Correspondencia vistas | **Brida de tubería**: la correspondencia entre vistas permite localizar los agujeros de tornillos desde cualquier vista. |

## Bloque 3: Perspectivas

| Tema | Caso Real |
|------|----------|
| b03-03 Isométrica círculos | **Tuercas y arandelas**: en isométrica los círculos son elipses. El dibujante usa el método de los 8 puntos. |
| b03-04 Caballera | **Planos arquitectónicos**: los arquitectos usan caballera porque las fachadas se ven en forma real (eje Z vertical). |
| b03-05 Perspectivas piezas | **Catálogo de productos**: ferretería usa isométrica para mostrar piezas. El cliente no es dibujante técnico. |
| b03-06 Perspectivas resumen | **Manuales de montaje**: IKEA usa perspectivas para guiar el ensamblaje sin ser experto. |

## Bloque 4: Diedrico

| Tema | Caso Real |
|------|----------|
| b04-01 Punto diedrico | **Control calidad CMM**: cada punto medido tiene coordenadas (X,Y,Z) respecto a planos de referencia. |
| b04-02 Recta diedrico | **Cableado y tuberías**: la recta en diedrico permite saber la longitud real de un tramo de tubería. |
| b04-03 Plano diedrico | **Bisel de placa**: una cara biselada a 45° se ve como triángulo en alzado y línea en planta. |
| b04-04 Pertenencia | **Verificar punto en cara**: el operario sabe si un agujero de centrado pertenece a la cara visible. |
| b04-05 Paralelismo | **Guiado CNC**: los ejes de una fresadora deben ser perpendiculares entre sí. |
| b04-06 VM | **Soldadura inclinada**: la VM se obtiene con cambio de plano paralelo a la soldadura. |
| b04-07 Cambio plano | **Replanteo de cimentaciones**: el arquitecto técnico coloca un nuevo PV paralelo a la línea. |
| b04-08 Giro | **Rebaje en eje**: se gira el eje para que el rebaje quede paralelo al PV. |
| b04-09 Resumen diedrico | **Caja de cambios**: 20+ piezas con vistas, cortes, secciones, vistas auxiliares. |

## Bloque 5: Cortes y Secciones

| Tema | Caso Real |
|------|----------|
| b05-01 Cortes | **Motor de combustión**: corte longitudinal muestra pistón, biela, cigüeñal. |
| b05-02 Corte tipos | **Válvula de paso**: corte parcial para la junta, corte total para el cuerpo. |
| b05-03 Corte escalonado | **Bloque motor con agujeros**: 4 agujeros de bujía a diferentes profundidades. |
| b05-04 Sección rotura | **Eje largo con ranura**: línea de rotura para no dibujar 500mm completos. |
| b05-05 Hachuras | **Diferenciación de materiales**: acero (45°), aluminio (separado), plástico (puntos). |
| b05-06 Ejercicios cortes | — |

## Bloque 6: Acotación

| Tema | Caso Real |
|------|----------|
| b06-01 Acotación | **Pieza de aeronáutica**: cotas dimensionales, de posición, tolerancias geométricas. |
| b06-02 Métodos acotación | **Bloque motor**: cotas funcionales (montaje) vs auxiliares (fabricación). |
| b06-03 Acotación coordenadas | **Taladrero CNC**: cada agujero tiene coordenadas (X,Y) desde el origen. |
| b06-04 Reglas acotación | **Norma ISO 129**: lenguaje universal entre diseñador y operario. |
| b06-05 Acotación compleja | **Carcasa de bomba**: cotas por grupos (forma, posición, tolerancia). |

## Bloque 7: Intersecciones

| Tema | Caso Real |
|------|----------|
| b07-01 Intersecciones | **Conductos HVAC**: conducto rectangular × circular = línea de soldadura compleja. |
| b07-02 Intersección plano-plano | **Tejado de nave**: dos planos inclinados se cruzan en la cumbrera. |
| b07-03 Intersección recta-recta | **Unión de vigas**: punto exacto de soldadura entre dos vigas cruzadas. |
| b07-04 Verdadera magnitud | **Pasamano inclinado**: longitud real para cortar el tubo de acero. |

## Bloque 8: Abatimientos y Giros

| Tema | Caso Real |
|------|----------|
| b08-01 Abatimientos | **Aleta de disipador**: forma complicada en plano oblicuo, se abate sobre PV. |
| b08-02 Abatimiento PH | **Base de máquina con agujero excéntrico**: distancia real al borde. |
| b08-03 Giros | **Rebaje en eje**: se gira para ver el rebaje en verdadera forma. |

## Bloque 9: Planos de Conjunto

| Tema | Caso Real |
|------|----------|
| b09-01 Planos conjunto | **Reductor de velocidad**: 15 piezas con baloncetes y números de referencia. |
| b09-02 Lista piezas | **Bomba centrífuga**: nº, nombre, material, cantidad, observaciones. |
| b09-03 Despiece | **Motor eléctrico**: 20+ piezas separadas con líneas de referencia. |

## Errores Comparativos por Bloque

| Bloque | Error típico | SVG comparativo |
|--------|-------------|-----------------|
| b02 | Planta encima del alzado | Mostrar vista incorrecta vs correcta |
| b02 | Confundir X con Z | Ejes intercambiados |
| b03 | Círculo en vez de elipse en isométrica | Círculo rojo vs elipse verde |
| b03 | Reducción caballera 1.0 en vez de 0.5 | Profundidad doble vs mitad |
| b04 | Punto en 2º diedro | Punto arriba de LT vs abajo |
| b04 | Recta paralela a LT | Línea horizontal vs oblicua |
| b05 | Corte total innecesario | Corte completo vs corte parcial |
| b05 | Sin corte (líneas ocultas) | Líneas discontinuas vs interior visible |
| b06 | Cota dentro del objeto | Texto dentro del rectángulo |
| b06 | Cotas en cadena (error acumulado) | Cadenas consecutivas vs paralela |
| b07 | Intersección recta en vez de curva | Línea recta vs curva real |
| b07 | Sin cálculo de intersección | Dos planos sin línea común |
| b08 | Sin abatir (forma deformada) | Elipse vs círculo |
| b08 | Reducción 1.0 en vez de 0.5 | Profundidad real vs mitad |
| b09 | Sin número de pieza | Sin baloncete |
| b09 | Sin lista de materiales | Sin columna de material |
