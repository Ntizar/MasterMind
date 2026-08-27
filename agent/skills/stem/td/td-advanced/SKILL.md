---
name: td-advanced
description: Normalización avanzada, tolerancias geométricas y dimensionales, cortes y secciones, representación de piezas complejas y planos de conjunto.
tags: [stem, td, advanced]
---

# Dibujo Técnico Avanzado

## Referencias de autoridad

- Norma UNE-EN ISO 1101: Tolerancias geométricas de formas y posiciones — Tolerancias básicas, definiciones, símbolos e indicaciones
- Norma UNE-EN ISO 286-1: Sistemas de tolerancias y ajustes — Parte 1: Fundamentos de sistemas de tolerancias, dimensiones y tolerancias estándar
- Norma UNE-EN ISO 286-2: Tablas de tolerancias para tamaños de 1 a 500 mm
- Norma UNE-EN ISO 128-4: Representación en dibujos técnicos — Convenciones generales — Cortes y secciones
- Norma ISO 13715: Soldadura estructural — Representación simplificada en dibujos y planos
- Manuales de normalización industrial de AENEL (Asociación Española de Normalización)
- Barrón-Bravo, F. — "Dibujo Técnico" — Editorial Paraninfo, ISBN 978-84-283-3405-7

## Contenido clave

### Normalización avanzada

Tolerancias geométricas según ISO 1101:

La norma ISO 1101 establece el sistema de tolerancias geométricas para controlar la forma, orientación, ubicación y batimento de los elementos geométricos de una pieza.

Cajas de tolerancia:

- La caja de tolerancia es un rectángulo dividido en dos o más casillas. La primera casilla contiene el símbolo de la tolerancia geométrica. La segunda casilla contiene el valor de la tolerancia. Si se utiliza un diámetro, se antepone el símbolo Ø.
- La tercera casilla (opcional) contiene el datum primario. La cuarta (opcional) contiene el datum secundario. La quinta (opcional) contiene el datum terciario.

Símbolos de tolerancias geométricas:

- Forma: rectitud, planitud, circularidad, cilindricidad.
- Orientación: paralelismo, perpendicularidad, inclinación.
- Ubicación: posición, simetría, batimento circular y batimento total.
- Batimento: control de la variación radial o axial de una superficie respecto a un eje o plano de referencia.

Tolerancia de planitud:

- Controla la irregularidad de una superficie plana. La tolerancia se define como la distancia entre dos planos paralelos entre los cuales debe estar contenida toda la superficie.
- Símbolo: una línea horizontal (—). No requiere datum.

Tolerancia de perpendicularidad:

- Controla la perpendicularidad de un elemento (superficie, eje, plano) respecto a un datum. La tolerancia se define como la distancia entre dos planos paralelos entre los cuales debe estar contenida la superficie o el eje.
- Símbolo: un cuadrado (□). Requiere un datum de referencia.

Tolerancia de concentricidad:

- Controla la coincidencia del eje o centro de un elemento con el eje o centro de un datum. La tolerancia se define como el diámetro de un cilindro de tolerancia cuyo eje coincide con el eje del datum.
- Símbolo: dos círculos concéntricos (◎). Requiere un datum.

Tolerancia de paralelismo:

- Controla la paralelidad de un elemento respecto a un datum. La tolerancia se define como la distancia entre dos planos paralelos entre los cuales debe estar contenida la superficie o el eje.
- Símbolo: dos líneas inclinadas paralelas (//). Requiere un datum.

Tolerancia de posición:

- Controla la ubicación exacta de un elemento (orificio, eje, ranura) respecto a un datum. La tolerancia se define como el diámetro de un cilindro de tolerancia cuyo eje está en la posición teóricamente exacta.
- Símbolo: un círculo con una cruz interior (⊕). Requiere datums de referencia.

Tolerancias dimensionales según ISO 286:

- El sistema ISO 286 define tolerancias estándar para dimensiones de 1 a 500 mm.
- Los grados de tolerancia (IT) van desde IT01 (mayor precisión) hasta IT16 (menor precisión).
- Los ajustes se clasifican en tres tipos: ajuste con juego, ajuste con transición y ajuste con interferencia.

Sistemas de ajuste:

- Ajuste con juego: el eje es siempre más pequeño que el agujero. Se utiliza cuando hay movimiento relativo entre las piezas.
- Ajuste con transición: puede haber juego o interferencia según las dimensiones reales. Se utiliza para ensamblajes que requieren precisión sin movimiento.
- Ajuste con interferencia: el eje es siempre más grande que el agujero. Se utiliza para ensamblajes fijos sin elementos de unión adicionales.

Notación de ajustes:

- Agujero base: H (mayúscula) indica que la cara inferior de la banda de tolerancia del agujero está en cero (IT fundamental). Ejemplo: H7/g6.
- Eje base: h (minúscula) indica que la cara superior de la banda de tolerancia del eje está en cero (IT fundamental). Ejemplo: H7/k6.
- Las letras mayúsculas se usan para agujeros y las minúsculas para ejes.

Cotas encadenadas, paralelas y por coordenadas (ISO 129-2):

- Cotas encadenadas: las cotas se disponen una detrás de otra en la misma dirección. Cada cota parte del extremo de la anterior. No se recomienda cuando se requiere alta precisión dimensional acumulativa.
- Cotas paralelas: todas las líneas de cota son paralelas entre sí y parten de una línea de referencia común. Se utiliza cuando hay múltiples dimensiones en la misma dirección.
- Cotas por coordenadas: cada dimensión se indica desde un origen común (datum). Es el método más preciso ya que cada cota es independiente.

### Cortes y secciones

Cortes según ISO 128-4:

Un corte es la representación de un objeto al que se le ha imaginariamente separado una porción para mostrar su interior.

Corte total:

- El plano de corte atraviesa completamente el objeto, separándolo en dos partes. Se representa la parte que queda entre el observador y el plano de corte.
- El plano de corte se indica con una línea de trazo y punto gruesa, con flechas en los extremos que indican la dirección de la vista.
- Las superficies de corte se rellenan con rayado (trazos finos inclinados a 45° respecto a la horizontal o a los ejes del dibujo).

Corte parcial (o corte por media sección):

- Solo se representa una parte del objeto, dejando la otra parte sin cortar. Se utiliza para mostrar el interior de una mitad y el exterior de la otra.
- La separación entre la parte cortada y la no cortada se indica con una línea continua fina ondulada (línea de ruptura).
- Se utiliza frecuentemente en ejes, pernos y piezas simétricas.

Corte escalonado:

- El plano de corte cambia de dirección una o más veces, formando ángulos rectos. Se utiliza cuando las características internas del objeto no están alineadas en un mismo plano.
- En el dibujo, el corte escalonado se representa como si todos los planos de corte estuvieran en el mismo plano. No se representan las líneas de cambio de dirección del plano de corte.

Corte combinado:

- Combina un corte total con una vista parcial no cortada. Se utiliza cuando solo una parte del objeto necesita ser cortada.

Secciones según ISO 128-4:

Una sección es la representación de la intersección de un plano de corte con el objeto.

Sección sacada o superpuesta:

- La sección se representa directamente sobre la vista, con líneas continuas gruesas. Se utiliza para mostrar la forma transversal de un elemento.
- La sección superpuesta se representa con líneas continuas finas para no interferir con las líneas de contorno de la vista.

Sección permitida:

- Se representa la sección de un elemento en una posición intermedia del dibujo, sin cortar la vista principal. Se indica con líneas de trazo y punto finas y las letras correspondientes.

Secciones sucesivas:

- Se representan varias secciones en la misma vista para mostrar diferentes secciones transversales de un objeto.

Rayado:

- Las superficies de corte se rellenan con rayado (trazos finos paralelos inclinados a 45°).
- El rayado debe ser uniforme y proporcional al tamaño del dibujo.
- En piezas metálicas, el rayado es el estándar. Para otros materiales se utilizan símbolos específicos (hormigón, madera, plástico, etc.).
- En un mismo dibujo, las piezas diferentes deben tener rayados con ángulos diferentes o espaciados diferentes.

### Normalización industrial

Tolerancias geométricas en la industria (ISO 1101):

- Las tolerancias geométricas son esenciales en la fabricación industrial para garantizar la funcionalidad y el ensamblaje de las piezas.
- El módulo de control define la relación entre la tolerancia geométrica y el tamaño de la pieza. Cuando se aplica el módulo, la tolerancia se amplía proporcionalmente a la desviación del tamaño real respecto al tamaño nominal.
- El módulo máximo (M) y el módulo mínimo (L) permiten ajustar la tolerancia geométrica según el tamaño real de la pieza.

Tolerancias de soldadura (ISO 13715):

- La norma ISO 13715 establece las convenciones para la representación simplificada de soldaduras en dibujos técnicos.
- La línea de referencia consta de una línea base y una línea punteada (cuando la soldadura está en el lado opuesto al observador).
- La flecha de la línea de referencia apunta al cordón de soldadura.
- Los símbolos de soldadura se colocan en la línea base (soldadura en el lado de la flecha) o en la línea punteada (soldadura en el lado opuesto).
- Los símbolos incluyen: soldadura a tope, soldadura de ángulo, soldadura de filete, soldadura de ranura, etc.

### Representación de piezas complejas

Piezas complejas requieren múltiples vistas, cortes y secciones para su representación completa.

Estrategia de representación:

- Determinar la vista principal que mejor represente la forma general de la pieza.
- Utilizar cortes y secciones para mostrar las características internas.
- Utilizar vistas auxiliares para mostrar caras inclinadas en verdadera magnitud.
- Utilizar vistas parciales para mostrar detalles específicos.

Representación de elementos normalizados:

- Roscas: se representan según normas ISO 228 (roscas cilíndricas para tuberías) e ISO 68 (perfil básico de rosca métrica). La rosca exterior se representa con líneas gruesas para el diámetro mayor y líneas finas para el diámetro menor. La rosca interior es inversa.
- Engranajes: dientes se representan con líneas finas en la zona de paso y líneas gruesas en el círculo de cabeza.
- Resortes: se representan con líneas finas para los alambres y líneas gruesas para las secciones cortadas.
- Chaveteros y ranuras: se representan en corte longitudinal, mostrando la profundidad y el ancho.

### Planos de conjunto

Un plano de conjunto representa un ensamblaje de varias piezas, mostrando cómo se relacionan entre sí.

Elementos del plano de conjunto:

- Vista general del ensamblaje: muestra la disposición de todas las piezas.
- Lista de piezas (o desglose): lista numerada de todas las piezas que componen el conjunto, con su nombre, material, cantidad y observaciones.
- Numeración de piezas: cada pieza se identifica con un número de referencia (balón) que apunta a la pieza correspondiente.
- Vista despiezada: muestra las piezas separadas pero en su posición relativa en el ensamblaje.
- Vista exploded: muestra las piezas separadas a lo largo de un eje de ensamblaje.

Reglas para planos de conjunto:

- Las piezas adyacentes en un corte deben tener rayados con ángulos diferentes (generalmente 45° en sentidos opuestos).
- Las piezas macizas (ejes, pernos, tuercas, pasadores) no se cortan en corte longitudinal.
- Las roscas se representan según las normas correspondientes.
- Las holguras entre piezas se representan con líneas separadas.
- Las piezas estándar (rodamientos, resortes, retenes) se representan según normas específicas.

Representación de elementos repetidos:

- Los elementos repetidos (agujeros, dientes de engranaje, etc.) se representan completamente en una posición y se indican con líneas de trazo y punto en las demás posiciones.
- Se indica el número total y las dimensiones en la lista de piezas o en una nota.

## Unidades y sistema SI

- Longitud: milímetro (mm). Las cotas se expresan en mm sin indicar la unidad.
- Tolerancias dimensionales: se indican como desviaciones superior e inferior (ejemplo: 50 +0,025/-0,000).
- Tolerancias geométricas: se indican en milímetros (mm) como ancho de la caja de tolerancia.
- Ángulos: grado sexagesimal (°).
- Conversión de grados de tolerancia IT: el valor de la tolerancia depende del tamaño nominal y del grado IT. Las tablas ISO 286-2 proporcionan los valores exactos.
- Módulo de control: la tolerancia geométrica puede modificarse según el tamaño real de la pieza cuando se aplica el módulo máximo (M) o mínimo (L).

## Errores comunes / Pitfalls

- Interpretación incorrecta de símbolos de tolerancias geométricas: confundir planitud (—) con paralelismo (//). La planitud no requiere datum, mientras que el paralelismo sí requiere un datum de referencia. Confundir concentricidad (◎) con simetría (≡). La concentricidad controla ejes, mientras que la simetría controla planos medios.
- Confusión entre corte y sección: el corte muestra tanto la sección como la parte del objeto que queda detrás del plano de corte. La sección muestra únicamente la intersección del plano de corte con el objeto. No usar el término "corte" cuando se representa una sección.
- Ajuste juego/interferencia/transición: confundir los tipos de ajuste. El ajuste con juego (ejemplo: H7/g6) tiene siempre holgura. El ajuste con interferencia (ejemplo: H7/p6) tiene siempre interferencia. El ajuste con transición (ejemplo: H7/k6) puede tener juego o interferencia según las dimensiones reales.
- Rayado incorrecto: usar el mismo rayado para piezas adyacentes diferentes. Las piezas adyacentes deben tener rayados con ángulos o espaciados diferentes.
- Error en la caja de tolerancia: colocar el valor de la tolerancia sin el símbolo Ø cuando corresponde a una tolerancia cilíndrica. La caja debe tener el símbolo de tolerancia en la primera casilla y el valor en la segunda.
- Olvidar los datums: las tolerancias de orientación y ubicación requieren datums de referencia. No indicar el datum equivale a una indicación incompleta.
- Representación incorrecta de roscas: representar el diámetro menor con línea gruesa en lugar de línea fina. En la rosca exterior, el diámetro mayor es línea gruesa y el diámetro menor es línea fina. En la rosca interior es al revés.
- Piezas macizas cortadas longitudinalmente: los ejes, pernos, tuercas y pasadores no se cortan en corte longitudinal. Representarlos cortados es un error grave.
- Error en cotas encadenadas: utilizar cotas encadenadas cuando se requiere alta precisión acumulativa. Cada cota encadenada acumula el error de la cota anterior, lo que puede provocar desviaciones significativas.

## Verificación

- [ ] ¿Las cajas de tolerancia geométrica tienen el símbolo correcto en la primera casilla?
- [ ] ¿Los datums están correctamente indicados en las casillas correspondientes?
- [ ] ¿El tipo de ajuste (juego, transición, interferencia) corresponde a la aplicación funcional?
- [ ] ¿Los rayados de piezas adyacentes tienen ángulos o espaciados diferentes?
- [ ] ¿Las piezas macizas (ejes, pernos) no se cortan en corte longitudinal?
- [ ] ¿La lista de piezas incluye todas las piezas del ensamblaje con sus cantidades correctas?
- [ ] ¿Las cotas por coordenidas tienen un origen de referencia claro y consistente?
- [ ] ¿Las tolerancias dimensionales indican correctamente las desviaciones superior e inferior?
- [ ] ¿Los símbolos de soldadura están correctamente colocados en la línea base o en la línea punteada?
- [ ] ¿Las roscas se representan con el diámetro mayor en línea gruesa y el diámetro menor en línea fina?
