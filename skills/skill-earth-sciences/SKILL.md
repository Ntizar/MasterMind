---
name: skill-earth-sciences
version: 1.0.0
category: STEM/Ciencias de la Tierra
description: "Geología, meteorología, oceanografía y climatología — Minerales, rocas, tectónica de placas, vulcanismo, sismología, atmósfera, presión, vientos, nubosidad, precipitaciones, corrientes, mareas, salinidad, ecosistemas marinos, climas de la Tierra, cambio climático y factores climáticos."
tags: [geología, minerales, rocas, tectónica de placas, vulcanismo, sismología, meteorología, atmósfera, presión, vientos, nubosidad, precipitaciones, oceanografía, corrientes, mareas, salinidad, ecosistemas marinos, climatología, cambio climático, factores climáticos]
author: Mastermind STEM
---

# skill-earth-sciences — Ciencias de la Tierra: Geología, Meteorología, Oceanografía y Climatología

## Descripción

Este skill proporciona al agente las capacidades para resolver problemas y explicar conceptos de **Geología**, **Meteorología**, **Oceanografía** y **Climatología**. Es el skill especializado del ecosistema STEM de Mastermind para el área de ciencias de la Tierra.

Este skill es **autocontenido**: el agente puede ejecutarlo sin consultar otros documentos. Sin embargo, hace referencia a skills STEM existentes para profundización en temas específicos.

## Temas Cubiertos

### 1. Geología

#### Minerales
- **Definición**: sustancia sólida, natural, inorgánica, con composición química definida y estructura cristalina ordenada.
- **Propiedades de identificación**:
  - **Color**: útil pero engañoso (impurezas cambian el color).
  - **Brillo**: metálico, vítreo, sedoso, resinoso, graso, adamantino.
  - **Raya**: color del mineral en polvo (frotar en porcelana sin esmaltar). Más fiable que el color.
  - **Exfoliación/clivaje**: dirección en que se rompe según planos de debilidad (ej. mica: 1 dirección; calcita: 3 direcciones).
  - **Fractura**: superficie irregular al romperse (ej. cuarzo: fractura concoidea).
  - **Dureza** (escala de Mohs, 1-10):
    ```
    1. Talco       6. Ortoclasa
    2. Yeso        7. Cuarzo
    3. Calcita     8. Topacio
    4. Fluorita    9. Corindón
    5. Apatita     10. Diamante
    ```
  - **Densidad**: masa/volumen. Metales nativos (oro, plata) son muy densos.
  - **Reacción con HCl**: calcita (CaCO₃) effervesce; dolomita effervesce solo con polvo.
- **Estructuras cristalinas**: cúbica, hexagonal, tetragonal, ortorrómbica, monoclínica, triclínica.
- **Grupo de los silicatos** (90% de la corteza): tetraedro SiO₄.
  - **Tectosilicatos**: feldespatos (ortoclasa, plagioclasa), cuarzo.
  - **Filosilicatos**: micas (biotita, moscovita), arcillas.
  - **Inosilicatos**: piroxenos (monoclinos), anfiboles (monoclínicos).
  - **Nesosilicatos**: olivino, granate.
  - **Ciclosilicatos**: berilo, turmalina.
  - **Sorosilicatos**: epidoto.
- **Grupo de los no silicatos**:
  - **Carbonatos**: calcita (CaCO₃), dolomita (CaMg(CO₃)₂).
  - **Sulfatos**: yeso (CaSO₄·2H₂O), baritina (BaSO₄).
  - **Sulfuros**: pirita (FeS₂), galena (PbS), calcopirita (CuFeS₂).
  - **Óxidos**: hematita (Fe₂O₃), magnetita (Fe₃O₄), corindón (Al₂O₃).
  - **Elementos nativos**: oro, plata, cobre, azufre, diamante (C), grafito (C).
  - **Haluros**: halita (NaCl), fluorita (CaF₂).

#### Rocas
- **Rocas ígneas** (formadas por solidificación del magma/lava):
  - **Por textura**:
    - **Plutónicas (intrusivas)**: enfriamiento lento → cristales grandes (fanerítica). Ej.: granito, diorita, gabbro.
    - **Volcánicas (extrusivas)**: enfriamiento rápido → cristales pequeños o vítreas (afanítica). Ej.: andesita, basalto, riolita, obsidiana, pómez.
    - **Hipabieta**: enfriamiento intermedio (diques, sills). Ej.: diabasa, porfido.
  - **Por composición**:
    - **Ácidas (félsicas)**: ricas en SiO₂ (>65%), claras (K-feldespato, cuarzo, biotita). Ej.: granito, riolita.
    - **Intermedias**: SiO₂ 52-65%. Ej.: diorita, andesita.
    - **Básicas (máficas)**: SiO₂ 45-52%, oscuras (piroxeno, olivino, plagioclasa cálcica). Ej.: gabbro, basalto.
    - **Ultramáficas**: SiO₂ <45%, muy oscuras (olivino, piroxeno). Ej.: peridotita (manto).
  - **Clasificación IAT** (tabla de textura vs composición):

| Textura | Ácida | Intermedia | Básica | Ultrabásica |
|---|---|---|---|---|
| Plutónica | Granito | Diorita | Gabbro | Peridotita |
| Volcánica | Riolita | Andesita | Basalto | Komatiita |

- **Rocas sedimentarias** (formadas por acumulación y litificación de sedimentos):
  - **Clasticas (detríticas)**: fragmentos de otras rocas.
    - Por tamaño de clasto: conglomerado (>2 mm), brecha (clastos angulares), arenisca (0.062-2 mm), limolita (0.004-0.062 mm), arcilla (<0.004 mm).
  - **Químicas/bioquímicas**: precipitación de minerales.
    - **Caliza** (CaCO₃): biogénica (conchas, corales) o química (travertino, estalactitas).
    - **Dolomía** (CaMg(CO₃)₂).
    - **Evaporitas**: halita (sal gema), yeso, sylvita.
    - **Chert/flint** (cuarzo microcristalino).
  - **Orgánicas**: carbón (carbón lignito → subbituminoso → bituminoso → antracita).
  - **Proceso de litificación**: compactación + cementación.
  - **Estructuras sedimentarias**: estratificación cruzada, laminación, marcas de corriente, huellas.

- **Rocas metamórficas** (formadas por transformación de rocas preexistentes por P y T):
  - **Factores**: temperatura, presión, fluidos hidrotermales, tiempo.
  - **Tipos de metamorfismo**:
    - **Regional**: grandes áreas, alta P y T (cadenas montañosas).
    - **De contacto (térmico)**: cerca de intrusión ígnea, alta T, baja P.
    - **Dinámico (cataclástico)**: alta presión dirigida (zonas de falla).
    - **Metasomático**: cambio por fluidos ricos en elementos.
  - **Texturas**:
    - **Foliadas** (bandeadas): pizarra → esquistos → gneis (grado creciente).
    - **No foliadas**: mármol (de caliza), cuarcita (de arenisca), ántracita.
  - **Grado metamórfico** (rocas metamórficas foliadas):

| Grado | Roca madre | Roca resultante | Minerales índice |
|---|---|---|---|
| Bajo | Pizarrilla | Pizarra | Clorita, biotita |
| Medio | Pizarra | Esquistos | Granate, mica |
| Alto | Esquisto | Gneis | Feldespato, cuarzo bandeados |

#### Tectónica de Placas
- **Teoría**: la litosfera (corteza + manto superior rígido) está fragmentada en placas que se mueven sobre la astenósfera (manto dúctil).
- **Límites de placas**:
  - **Divergente (constructivo)**: placas se separan.
    - **Dorsales oceánicas**: magma asciende, forma nueva corteza oceánica. Ej.: dorsal Mesoatlántica.
    - **Rift continental**: extensión continental. Ej.: rift africano.
    - **Estructuras**: valles de rift, volcanismo basáltico, sismicidad superficial.
  - **Convergente (destructor)**: placas se acercan.
    - **Oceánica-Continental**: la oceánica (más densa) subduce bajo la continental.
      - Fosa oceánica, arco volcánico continental, terremotos profundos.
      - Ej.: placa de Nazca y Sudamérica (Andes).
    - **Oceánica-Oceánica**: la más densa subduce.
      - Fosa, arco volcánico insular.
      - Ej.: placa del Pacífico y placa de Filipinas (Japón).
    - **Continental-Continental**: colisión, no hay subducción (ambas poco densas).
      - Cadenas montañosas, metamorfismo regional, terremotos profundos.
      - Ej.: placa India y Eurasia (Himalaya).
  - **Transform (conservativo)**: placas se deslizan lateralmente.
    - Fallas transformantes, sismicidad superficial.
    - Ej.: falla de San Andrés (Pacífica y Norteamericana).
- **Zonas de subducción**:
  - **Zona de Wadati-Benioff**: plano de slab subducido, sismicidad hasta ~700 km.
  - **Arco magmático**: el agua liberada del slab reduce el punto de fusión del manto.
  - **Mantos de subducción**: sedimentarios arrastrados, ofiolitas.

#### Vulcanismo
- **Tipos de erupción**:
  - **Hawaiano**: lava basáltica fluida, baja viscosidad, baja gas. Flujos de lava, fuentes de lava. Ej.: Kilauea.
  - **Estromboliano**: explosiones moderadas, bombas volcánicas, conos de escorias. Ej.: Estromboli.
  - **Vulcaniano**: explosiones violentas, columnas de ceniza, nubes piroclásticas. Lava andesítica. Ej.: Vulcano, Monte Pelée.
  - **Pliniano**: explosiones extremadamente violentas, columnas estratosféricas, ignimbritas, calderas. Lava riolítica/andesítica. Ej.: Vesubio (79 d.C.), Monte Santa Helena (1980).
  - **Submarino**: en dorsales o puntos calientes, forma chimeneas hidrotermales.
- **Construcciones volcánicas**:
  - **Volcán escudo**: basáltico, flanco suave, amplio. Ej.: Mauna Loa.
  - **Volcán estratovolcán (composite)**: andesítico, capas alternas de lava y piroclastos, flanco empinado. Ej.: Vesubio, Fuji.
  - **Cono de ceniza**: pequeño, piroclastos sueltos.
  - **Caldera**: colapso tras vaciado de cámara magmática.
  - **Domo de lava**: lava muy viscosa, no fluye.
- **Productos volcánicos**:
  - **Lava**: pāhoehoe (lisa), aa (áspera), bloque (fragmentada).
  - **Piroclastos**: ceniza (<2 mm), lapilli (2-64 mm), bombas (>64 mm).
  - **Gases**: H₂O (70-90%), CO₂, SO₂, H₂S, HCl, HF.
  - **Flujo piroclástico**: mezcla de gas, ceniza y fragmentos a alta velocidad (>100 km/h). Extremadamente peligroso.
  - **Lahar**: flujo de lodo volcánico (ceniza + agua).
- **Puntos calientes (hotspots)**: plumas del manto profundo, crean cadenas volcánicas. Ej.: Hawái, Islas Galápagos, Yellowstone.

#### Sismología
- **Terremoto**: liberación brusca de energía acumulada por deformación elástica (teoría del rebote elástico, Reid 1910).
- **Foco (hipocentro)**: punto de origen del sismo en profundidad.
- **Épicoentro**: punto en superficie sobre el foco.
- **Ondas sísmicas**:
  - **Body waves (internas)**:
    - **P (primarias)**: compresionales, longitudinales, viajan por sólidos y líquidos. Más rápidas (6-8 km/s).
    - **S (secundarias)**: de cizalla, transversales, solo sólidos. Más lentas (3.5-4.5 km/s).
  - **Surface waves (superficiales)**:
    - **Ondas Love**: movimiento horizontal perpendicular a la dirección de propagación.
    - **Ondas Rayleigh**: movimiento elíptico (como olas del mar).
    - Las ondas superficiales causan más daño pero viajan más lento.
- **Magnitud vs Intensidad**:
  - **Magnitud** (escala de Richter/Mw): energía liberada, escala logarítmica. Un aumento de 1 unidad = 32× más energía.
  - **Intensidad** (escala de Mercalli modificada): efectos observados en superficie (I-XII). Depende de distancia, geología, construcción.
- **Sismógrafo**: instrumento que registra ondas sísmicas.
- **Localización del epicentro**: triangulación con al menos 3 estaciones sismográficas (diferencia de tiempos S-P).
- **Zonas sísmicas**:
  - **Cinturón de fuego del Pacífico**: ~80% de los sismos mundiales.
  - **Dorsales oceánicas**: sismos superficiales.
  - **Zonas de colisión continental**: sismos profundos.
- **Tsunamis**: generados por sismos submarinos, deslizamientos, erupciones volcánicas. Velocidad en mar profundo: v = √(g·d).

### 2. Meteorología

#### Atmósfera
- **Composición**: N₂ (78.08%), O₂ (20.95%), Ar (0.93%), CO₂ (~0.041%), gases traza, vapor de agua (0-4%).
- **Capas atmosféricas** (por temperatura):
  - **Tropósfera** (0-12 km): temperatura disminuye con la altura (~6.5°C/km = gradiente térmico vertical). Aquí ocurren los fenómenos meteorológicos.
  - **Estratósfera** (12-50 km): temperatura aumenta (capa de ozono absorbe UV). Inversión térmica.
  - **Mesósfera** (50-85 km): temperatura disminuye (capa más fría, -90°C).
  - **Termósfera** (85-600 km): temperatura aumenta (>1000°C, pero muy baja densidad). Auroras.
  - **Exósfera** (>600 km): transición al espacio.
- **Tropopausa**: límite tropósfera/estratósfera.
- **Capa de ozono (O₃)**: en estratósfera, absorbe radiación UV-B y UV-C. Agotamiento por CFC.

#### Presión atmosférica
- **Definición**: peso de la columna de aire sobre un punto.
- **Unidades**: hPa (hectopascal), mb (milibar), atm, mmHg. 1 atm = 1013.25 hPa = 760 mmHg.
- **Presión media al nivel del mar**: 1013.25 hPa.
- **Variación con la altitud**: disminuye exponencialmente (~1 hPa cada 8 m a nivel del mar).
- **Isobaras**: líneas de igual presión en mapas meteorológicos.
- **Sistemas de presión**:
  - **Anticiclón (alta presión, A)**: aire descendente, tiempo estable, cielos despejados. Rotación horaria (HN) / antihoraria (HS).
  - **Borra (baja presión, B)**: aire ascendente, formación de nubes y precipitaciones. Rotación antihoraria (HN) / horaria (HS).

#### Vientos
- **Causa**: diferencias de presión (fuerza del gradiente de presión). El aire fluye de alta a baja presión.
- **Fuerza de Coriolis**: desvía vientos hacia la derecha (HN) o izquierda (HS) por rotación terrestre. No actúa en el ecuador.
- **Viento geostrófico**: equilibrio entre fuerza del gradiente y Coriolis (flujo paralelo a isobaras, en altura).
- **Viento ciclónico/anticiclónico**: curvatura de isobaras añade fuerza centrípeta.
- **Fricción superficial**: desvía vientos hacia baja presión (~30°), reduce velocidad.
- **Circulación general**:
  - **Celdas de Hadley** (0-30°): aire cálido asciende en ecuador (baja presión intertropical), desciende en 30° (altas subtropicales).
  - **Celdas de Ferrel** (30-60°): circulación indirecta, impulsada por las otras celdas.
  - **Celdas polares** (60-90°): aire frío desciende en polos, fluye hacia el ecuador.
  - **Vientos predominantes**:
    - **Alisios**: de los anticiclones subtropicales hacia el ecuador (NE en HN, SE en HS).
    - **Vientos del oeste** (westerlies): de 30° a 60° (del suroeste en HN).
    - **Vientos polares**: de los polos hacia 60° (NE en HN).
  - **Frente polar**: zona de encuentro entre vientos del oeste y polares (~60°).
- **Vientos locales**:
  - **Brisa marina**: de día, mar→tierra (tierra se calienta más). De noche: tierra→mar.
  - **Brisa de valle/montaña**: de día, valle→montaña (anabático). De noche, montaña→valle (catabático).
  - **Foehn/Chinook**: viento cálido y seco que desciende por la cara de sotavento de una montaña.
  - **Mistral**: viento frío y seco del norte en el Mediterráneo occidental.

#### Nubosidad y Precipitaciones
- **Formación de nubes**:
  1. **Ascenso del aire**: orográfico, convectivo, frontal, convergencia.
  2. **Enfriamiento adiabático**: el aire asciende, se expande y se enfría (~1°C/100 m en aire seco, ~0.6°C/100 m en aire húmedo).
  3. **Punto de rocío**: temperatura a la que el aire se satura (HR = 100%).
  4. **Condensación**: vapor → gotitas sobre núcleos de condensación (aerosoles, polvo, sal marina).
- **Tipos de nubes** (clasificación de Luke Howard):
  - **Cirrus (Ci)**: altas (>6 km), fibrosas, heladas, en forma de plumas. Buen tiempo.
  - **Cirrocumulus (Cc)**: altas, ondas pequeñas, "cielo de corderos".
  - **Cirrostratus (Cs)**: altas, velos, halos alrededor del Sol/Luna.
  - **Altocumulus (Ac)**: medias (2-6 km), ondas, "corderos grandes".
  - **Altostratus (As)**: medias, velo gris, Sol difuso.
  - **Nimbostratus (Ns)**: bajas-medias, grises, precipitación continua.
  - **Stratocumulus (Sc)**: bajas (<2 km), capas onduladas.
  - **Stratus (St)**: bajas, capa uniforme, niebla elevada.
  - **Cumulus (Cu)**: verticales, "algodonosos", base plana. Buen tiempo (cumulus humilis).
  - **Cumulonimbus (Cb)**: verticales enormes, tope en yunque, tormentas, granizo, rayos.
- **Clasificación por altura**:

| Género | Prefix | Ejemplos |
|---|---|---|
| Altas (6-12 km) | Cirro- | Ci, Cc, Cs |
| Medias (2-6 km) | Alto- | Ac, As |
| Bajas (<2 km) | Strato-, Cumulo- | Sc, St, Cu |
| Verticales | Nimo- | Ns, Cb |

- **Tipos de precipitación**:
  - **Lluvia**: gotas >0.5 mm.
  - **Llovizna**: gotas <0.5 mm, continua, ligera.
  - **Granizo**: bolas de hielo, asociadas a Cb fuertes.
  - **Nieve**: cristales de hielo, temperaturas <0°C.
  - **Aguanieve**: mezcla de nieve y lluvia.
  - **Chaparrón**: precipitación intensa, corta duración, convectiva.
- **Formación de lluvia** (teoría de Bergeron vs colisión-coalescencia):
  - **Bergeron (nubes frías)**: cristales de hielo crecen a expensas de gotas sobrefrías (diferencia de presión de vapor).
  - **Colisión-coalescencia (nubes cálidas)**: gotas grandes colisionan y absorben pequeñas.

#### Frentes meteorológicos
- **Frente cálido**: aire cálido avanza sobre aire frío. Nubes estratiformes (Cs, As, Ns), precipitación continua y extensa. Isobaras amplias.
- **Frente frío**: aire frío empuja bajo aire cálido. Nubes convectivas (Cu, Cb), precipitación intensa y breve, chubascos, tormentas. Isobaras apretadas.
- **Frente ocluido**: un frente frío alcanza un cálido, elevando el aire cálido. Combinación de ambos.
- **Ciclón extratropical (borra frontal)**: sistema de baja presión con frentes cálidos, fríos y ocluidos. Rotación ciclónica.

### 3. Oceanografía

#### Estructura del océano
- **Cobertura**: ~71% de la superficie terrestre.
- **Océanos**: Pacífico (mayor, ~165 millones km²), Atlántico, Índico, Ártico, Austral/Antártico.
- **Mares**: porciones menores, limitados parcialmente por tierra (Mediterráneo, Caribe, Báltico).
- **Profundidad media**: ~3,700 m. Profundidad máxima: Fosa de las Marianas (~10,994 m).
- **Divisiones batimétricas**:
  - **Plata continental**: borde continental, pendiente suave (0-200 m).
  - **Talud continental**: pendiente pronunciada (200-2,500 m).
  - **Abanicos submarinos**: depósitos sedimentarios en la base del talud.
  - **Fondo oceánico (llanura abisal)**: 4,000-6,000 m, llano, cubierto de sedimentos.
  - **Dorsales oceánicas**: cadena montañosa submarina, sitio de expansión del fondo marino.
  - **Fosas oceánicas**: zonas de subducción, las profundidades máximas.
  - **Montes submarinos (guyots)**: volcanes submarinos, cimas aplanadas por erosión.
  - **Islas oceánicas**: volcanes emergidos (Hawái, Canarias).

#### Propiedades del agua de mar
- **Salinidad media**: 35‰ (35 g/kg). Varía: Mar Rojo (~40‰), Báltico (~7‰), estuarios (<30‰).
- **Composición iónica principal** (proporciones constantes — principio de Marcet):
  - Cl⁻ (55.04%), Na⁺ (30.61%), SO₄²⁻ (7.68%), Mg²⁺ (3.69%), Ca²⁺ (1.16%), K⁺ (1.10%).
- **Factores que afectan la salinidad**:
  - **Aumentan**: evaporación, formación de hielo marino (la sal queda en el agua).
  - **Disminuyen**: precipitación, deshielo, aportes fluviales.
- **Densidad del agua de mar**: aumenta con salinidad y disminuye con temperatura.
  - **Ecuación de estado**: ρ = f(T, S, P). El agua más densa (~3.5‰, -1.8°C) se hunde.
- **Capas oceánicas** (por temperatura):
  - **Mezcla superficial** (0-200 m): temperatura homogénea, calentada por el Sol.
  - **Termoclina** (200-1,000 m): temperatura disminuye rápidamente.
  - **Profunda** (>1,000 m): temperatura baja y constante (~2-4°C).

#### Corrientes oceánicas
- **Corrientes superficiales** (top 400 m): impulsadas por vientos globales.
  - **Giro subtropical**: circulación circular en cada cuenca oceánica (horaria HN, antihoraria HS).
  - **Corriente del Golfo**: cálida, del Golfo de México al Atlántico norte. Calienta Europa.
  - **Corriente de Humboldt (Perú)**: fría, del sur al norte en la costa oeste de Sudamérica.
  - **Corriente de Kuroshio**: cálida, equivalente del Pacífico de la del Golfo.
  - **Corriente Circumpolar Antártica**: la más caudalosa, rodea la Antártida.
- **Corrientes profundas (circulación termohalina)**: impulsadas por diferencias de densidad (T y S).
  - **Formación de aguas profundas**: en el Atlántico norte (aguas de Labrador y Noruega) y alrededor de la Antártida (agua antártica de fondo).
  - **Cinta transportadora global**: circulación lenta (1,000+ años para completar).
- **Upwelling (afloramiento)**: aguas profundas, frías y ricas en nutrientes ascienden.
  - Causas: vientos paralelos a costa (efecto Ekman), divergencia ecuatorial.
  - Zonas de alta productividad: costa de Perú, California, Canarias, Benguela.
- **Downwelling (hundimiento)**: aguas superficiales descienden.

#### Mareas
- **Causa**: fuerza gravitatoria de la Luna (principal) y el Sol (secundaria, ~46% del efecto lunar).
- **Mareas altas (pleamar)** y **bajas (bajamar)**.
- **Marea viva (spring tide)**: Luna llena o nueva (Sol y Luna alineados, fuerzas se suman). Mayor amplitud.
- **Marea muerta (neap tide)**: Cuarto creciente o menguante (Sol y Luna en cuadratura). Menor amplitud.
- **Ciclo de mareas**:
  - **Diurno**: 1 pleamar y 1 bajamar por día (Golfo de México).
  - **Semidiurno**: 2 pleamares y 2 bajamares por día (mayor parte del mundo, ~12h 25min).
  - **Mixto**: combinación (Pacífico norte).
- **Amplitud de marea**: diferencia entre pleamar y bajamar. Máxima en el Golfo de San Malo (~15 m), mínima en el Mediterráneo (<0.5 m).
- **Onda de marea**: propagación de la deformación del océano. Puede reflejarse en bahías (resonancia).
- **Marejadas ciclónicas**: aumento del nivel del mar por tormentas. Peligroso en costas bajas.

#### Ecosistemas marinos
- **Zonas oceánicas** (por luz y distancia a costa):
  - **Zona fótica** (0-200 m): luz suficiente para fotosíntesis. Fitoplancton.
  - **Zona afótica** (>200 m): sin luz. Bioluminiscencia.
  - **Zona pelágica**: agua abierta.
    - **Necton**: organismos nadadores (peces, mamíferos marinos).
    - **Plancton**: organismos arrastrados (fitoplancton, zooplancton).
  - **Zona bentónica**: fondo marino.
- **Ecosistemas costeros**:
  - **Plataforma continental**: alta productividad, pesquerías.
  - **Estuarios**: mezcla de agua dulce y salada, nursery de especies.
  - **Hábitats rocosos**: organismos adheridos (mejillones, lapas, algas).
  - **Playas**: organismos excavadores (almejas, cangrejos).
  - **Marismas y manglares**: zonas intermareales, protección costera, captura de carbono.
  - **Arrecifes de coral**: aguas cálidas, claras, poco profundas. Simbiosis zooxantelas-coral. Alta biodiversidad. Amenazados por blanqueamiento.
- **Productividad marina**:
  - **Fitoplancton**: diatomeas, dinoflagelados, cianobacterias. Base de la red trófica marina.
  - **Zonas de alta productividad**: afloramientos, estuarios, arrecifes, zonas polares (en verano).
  - **Desiertos oceánicos**: zonas subtropicales centrales, baja productividad.

### 4. Climatología

#### Factores climáticos vs elementos climáticos
- **Elementos climáticos** (describen el clima): temperatura, precipitación, humedad, presión, viento, nubosidad.
- **Factores climáticos** (modifican los elementos): latitud, altitud, distancia al mar, corrientes marinas, relieve, distribución tierra/mar.

#### Factores climáticos detallados
- **Latitud**: principal factor. Determina el ángulo de incidencia solar y la duración del día.
  - **Trópicos** (23.5°N-23.5°S): alta insolación, temperaturas altas todo el año.
  - **Templados** (23.5°-66.5°): estaciones marcadas.
  - **Polares** (>66.5°): baja insolación, inviernos largos y fríos.
  - **Solsticios** (21 jun, 21 dic): máximo/mínimo de insolación. **Equinoccios** (21 mar, 23 sep): día y noche iguales.
- **Altitud**: temperatura disminuye ~6.5°C/km (gradiente térmico).
  - **Pisos térmicos**: tropical, templado, frío, nival.
  - **Inversión térmica**: temperatura aumenta con la altitud (valles de montaña, invierno).
- **Distancia al mar (continentalidad)**:
  - **Clima marítimo**: menor amplitud térmica, precipitaciones regulares, temperaturas suaves.
  - **Clima continental**: mayor amplitud térmica, precipitaciones más irregulares.
- **Corrientes marinas**:
  - **Cálidas**: aumentan temperatura y precipitación en costas adyacentes. Ej.: Corriente del Golfo.
  - **Frías**: disminuyen temperatura, pueden generar aridez costera (inversión térmica). Ej.: Corriente de Humboldt.
- **Relieve**:
  **Barlovento** (cara expuesta al viento): precipitaciones orográficas.
  **Sotavento** (cara protegida): sombra pluviométrica, efecto Foehn (cálido y seco).
- **Distribución tierra/mar**: los continentes se calientan/enfrían más rápido que los océanos → monzones, brisas.

#### Clasificación climática de Köppen
- **Clima tropical (A)**: T media del mes más frío >18°C.
  - **Af**: selva tropical (lluvia todo el año).
  - **Aw/As**: sabana (estación seca marcada).
  - **Am**: monzónico (lluvias intensas breves, estación seca corta).
- **Clima seco (B)**: precipitación < evaporación.
  - **Bw**: desierto.
  - **Bs**: estepa.
  - **h** (cálido), **k** (frío).
- **Clima templado (C)**: T media del mes más frío entre -3°C y 18°C.
  - **Cf**: sin estación seca (oceánico).
  - **Cs**: verano seco (mediterráneo).
  - **Cw**: invierno seco.
  - **a** (verano cálido), **b** (verano suave), **c** (verano frío), **d** (invierno muy frío).
- **Clima boreal/subpolar (D)**: T media del mes más frío < -3°C, del más cálido >10°C.
  - **Df**: sin estación seca.
  - **Ds**: verano seco.
  - **Dw**: invierno seco.
  - **Dfb/Dfc**: taiga, tundra modificada.
- **Clima polar (E)**: T media del mes más cálido <10°C.
  - **ET**: tundra (al menos un mes >0°C).
  - **EF**: casquete de hielo (todos los meses <0°C).

#### Climas de la Tierra (descripción general)
- **Ecuatorial**: alta T (25-28°C), alta precipitación (>2,000 mm), sin estación seca. Ej.: Amazonía, Congo.
- **Tropical de sabana**: T alta, estación seca marcada. Ej.: África subsahariana, Brasil central.
- **Desértico**: baja precipitación (<250 mm), gran amplitud térmica diaria. Ej.: Sahara, Atacama, Gobi.
- **Mediterráneo**: veranos calurosos y secos, inviernos suaves y húmedos. Ej.: cuenca del Mediterráneo, California.
- **Oceánico**: temperaturas suaves todo el año, precipitaciones regulares. Ej.: noroeste de Europa.
- **Continental húmedo**: inviernos fríos, veranos cálidos, precipitaciones moderadas. Ej.: centro de Norteamérica, Europa oriental.
- **Subpolar/taiga**: inviernos muy fríos, veranos cortos y frescos. Ej.: Siberia, Canadá.
- **Tundra**: veranos muy cortos (0-10°C), permafrost. Ej.: Ártico, Alaska.
- **Polar/casquete**: todos los meses bajo 0°C. Ej.: Antártida, Groenlandia.

#### Cambio climático
- **Causas naturales**:
  - **Variaciones orbitales** (ciclos de Milanković): excentricidad (100,000 años), oblicuidad (41,000 años), precesión (26,000 años).
  - **Variaciones solares**: ciclos de manchas solares (11 años).
  - **Volcanismo**: aerosoles de SO₂ enfrían temporalmente (1-3 años).
  - **Deriva continental**: cambia distribución de océanos y continentes.
- **Causas antropogénicas** (dominantes desde ~1850):
  - **Gases de efecto invernadero (GEI)**: CO₂ (quema de combustibles fósiles, deforestación), CH₄ (ganadería, arroz, vertederos), N₂O (fertilizantes), CFC (refrigerantes).
  - **Cambios de uso del suelo**: deforestación, urbanización.
  - **Aerosoles**: efecto enfriante parcial (enmascaran parte del calentamiento).
- **Evidencias del cambio climático actual**:
  - **Aumento de temperatura global**: +1.1°C desde la era preindustrial (IPCC AR6).
  - **Aumento del nivel del mar**: ~20 cm desde 1900, acelerando (~3.6 mm/año actualmente).
  - **Reducción de hielo marino ártico**: ~13% por década.
  - **Acidificación oceánica**: pH ha disminuido ~0.1 unidades (30% más ácido).
  - **Eventos extremos más frecuentes**: olas de calor, sequías, inundaciones, huracanes intensos.
- **Consecuencias**:
  - **Elevación del nivel del mar**: inundación de zonas costeras, salinización de acuíferos.
  - **Alteración de ecosistemas**: migración de especies, blanqueamiento de corales, extinciones.
  - **Impactos agrícolas**: cambios en zonas cultivables, estrés hídrico.
  - **Salud humana**: olas de calor, enfermedades tropicales, inseguridad alimentaria.
  - **Aglomeraciones de permafrost**: liberación de CH₄ (retroalimentación positiva).
- **Escenarios IPCC**:
  - **SSP1-1.9**: <1.5°C (descarbonización rápida).
  - **SSP1-2.6**: ~1.8°C (transición energética).
  - **SSP2-4.5**: ~2.7°C (tendencias actuales).
  - **SSP5-8.5**: ~4.4°C (alto uso de combustibles fósiles).
- **Mitigación**: reducción de emisiones (energías renovables, eficiencia, reforestación, captura de carbono).
- **Adaptación**: ajuste a los efectos (diques, agricultura resiliente, planificación urbana).

#### Efecto invernadero
- **Mecanismo**: los GEI permiten la entrada de radiación solar (visible) pero absorben la radiación infrarroja emitida por la Tierra, reemitiéndola en todas direcciones (incluido de vuelta a la superficie).
- **Sin efecto invernadero natural**: temperatura media terrestre sería ~-18°C en vez de +15°C.
- **GEI principales**:
  - **CO₂**: ~63% del forzamiento radiativo antropogénico. Vida larga (siglos).
  - **CH₄**: ~20%. Potente pero vida corta (~12 años).
  - **N₂O**: ~6%. Vida larga (~114 años).
  - **CFC/HFC**: ~10%. Muy potentes (miles de veces CO₂), vida larga.
  - **Vapor de agua**: mayor contribución total, pero retroalimentación (no forzamiento directo).
- **Forzamiento radiativo**: cambio en el balance energético de la Tierra (W/m²). Actual: ~+2.7 W/m² desde 1750.
- **Retroalimentaciones**:
  - **Positivas** (amplifican): vapor de agua, albedo (hielo-derretimiento), permafrost.
  - **Negativas** (amortiguan): nubes (depende del tipo), aumento de emisión IR.

#### Escala de Beaufort (viento)
| Fuerza | Velocidad (km/h) | Efecto en tierra | Efecto en mar |
|---|---|---|---|
| 0 | <1 | Calma, humo vertical | Mar en espejo |
| 3 | 19-38 | Hojas se mueven, bandera se extiende | Olas pequeñas, crestas cristalinas |
| 6 | 39-49 | Ramas grandes se mueven, paraguas difícil | Olas grandes, espuma blanca |
| 9 | 62-74 | Daños en chimeneas, tejas | Marejada moderada, espuma en bandas |
| 12 | >118 | Destrucción general | Mar blanco, olas enormes, visibilidad reducida |

## Cuándo usar este skill

Usa este skill cuando:

1. El usuario pregunta sobre **minerales y rocas**: identificación, clasificación, formación.
2. Hay problemas de **tectónica de placas**: tipos de límites, estructuras asociadas, ejemplos.
3. Se necesita explicar **vulcanismo**: tipos de erupción, productos, construcciones volcánicas.
4. Hay preguntas de **sismología**: ondas sísmicas, magnitud vs intensidad, localización.
5. El tema es **meteorología**: presión, vientos, nubes, frentes, precipitaciones.
6. Se necesita información de **oceanografía**: corrientes, mareas, salinidad, ecosistemas marinos.
7. Hay preguntas de **climatología**: clasificación de Köppen, factores climáticos, cambio climático.
8. El problema es de nivel **bachillerato o primeros cursos universitarios** de ciencias de la Tierra.

## Instrucciones paso a paso para el agente

### Procedimiento General

1. **Identificar la disciplina**: geología, meteorología, oceanografía o climatología.
2. **Determinar el subtema específico** dentro de la disciplina.
3. **Aplicar el procedimiento específico** del subtema (ver abajo).
4. **Presentar la respuesta** con claridad, usando tablas, esquemas y ejemplos cuando sea útil.
5. **Incluir ejemplos concretos** (nombres de rocas, lugares, fenómenos) cuando corresponda.

### Procedimiento para Geología

1. **Identificar el tipo de problema**: mineral, roca, tectónica, vulcanismo o sismología.
2. **Para minerales**: listar propiedades de identificación relevantes, comparar con la tabla de Mohs.
3. **Para rocas**: determinar tipo (ígneas, sedimentarias, metamórficas), textura y composición. Usar la clasificación IAT para ígneas.
4. **Para tectónica**: identificar el tipo de límite de placa, las estructuras asociadas y dar ejemplos reales.
5. **Para vulcanismo**: clasificar el tipo de erupción por viscosidad del magma y contenido de gas.
6. **Para sismología**: diferenciar ondas P y S, magnitud vs intensidad, explicar la triangulación.

### Procedimiento para Meteorología

1. **Identificar el fenómeno**: presión, viento, nubosidad, precipitación o frentes.
2. **Para presión**: explicar el gradiente, isobaras, sistemas de alta/baja presión.
3. **Para vientos**: identificar la escala (global, regional, local), las fuerzas involucradas.
4. **Para nubes**: clasificar por género (altura) y especie (forma). Relacionar con tipos de tiempo.
5. **Para precipitaciones**: explicar el mecanismo de formación (ascenso, enfriamiento, condensación).

### Procedimiento para Oceanografía

1. **Identificar el aspecto**: estructura batimétrica, propiedades del agua, corrientes, mareas o ecosistemas.
2. **Para corrientes**: diferenciar superficiales (viento) de profundas (termohalina).
3. **Para mareas**: identificar la posición lunar, el tipo de marea (viva/muerta), el patrón (diurno/semidiurno).
4. **Para ecosistemas**: clasificar por zona (pelágica/bentónica, fótica/afótica, costera/open ocean).

### Procedimiento para Climatología

1. **Identificar el enfoque**: factores climáticos, clasificación de Köppen, cambio climático.
2. **Para clasificación Köppen**: determinar la letra principal (A/B/C/D/E) por temperatura, luego la secundaria por precipitación y temperatura estacional.
3. **Para factores climáticos**: analizar cada factor (latitud, altitud, mar, corrientes, relieve) y su efecto.
4. **Para cambio climático**: diferenciar causas naturales de antropogénicas, evidencias y consecuencias.

## Ejemplos de Prompts que Activan Este Skill

### Ejemplo 1: Geología — Clasificación de Rocas Ígneas
```
Una roca es de color claro, tiene cristales visibles de cuarzo, feldespato y mica, y se formó por enfriamiento lento del magma. ¿Qué tipo de roca es?
```
**Respuesta esperada**: Es una roca ígnea plutónica (intrusiva), de composición ácida (félsica). Por la tabla IAT: **granito**. El enfriamiento lento permite cristales grandes (textura fanerítica). El color claro y la presencia de cuarzo y feldespato confirman la composición ácida.

### Ejemplo 2: Geología — Tectónica de Placas
```
¿Qué estructuras geológicas se forman en un límite convergente oceánico-continental? Da un ejemplo real.
```
**Respuesta esperada**: En un límite convergente oceánico-continental se forma:
- **Fosa oceánica** (por subducción de la placa oceánica).
- **Arco volcánico continental** (por fusión del manto inducida por el agua del slab).
- **Terremotos** de profundidad creciente (zona de Wadati-Benioff).
- **Ejemplo real**: placa de Nazca (oceánica) subduce bajo la placa Sudamericana (continental) → Fosa de Perú-Chile, Cordillera de los Andes, volcanes de la Cordillera.

### Ejemplo 3: Meteorología — Formación de Nubes
```
¿Por qué se forman nubes cuando el aire asciende? Explica el proceso paso a paso.
```
**Respuesta esperada**:
1. El aire asciende y se expande (menor presión en altura).
2. La expansión provoca enfriamiento adiabático (~1°C/100 m en aire seco).
3. Al alcanzar el **punto de rocío**, la humedad relativa llega al 100%.
4. El vapor de agua se condensa sobre **núcleos de condensación** (polvo, sal, aerosoles).
5. Se forman **gotitas de nube** (10-20 μm).
6. Si las gotitas crecen por coalescencia o proceso de Bergeron, caen como precipitación.

### Ejemplo 4: Oceanografía — Mareas
```
¿Por qué las mareas vivas ocurren en luna llena y luna nueva? ¿Y las mareas muertas en cuarto creciente y menguante?
```
**Respuesta esperada**:
- **Mareas vivas** (luna llena y nueva): el Sol, la Luna y la Tierra están alineados (sizigia). Las fuerzas gravitatorias del Sol y la Luna se **suman**, produciendo pleamares más altas y bajamares más bajas.
- **Mareas muertas** (cuarto creciente y menguante): el Sol y la Luna forman 90° (cuadratura). Las fuerzas se **contrarrestan parcialmente**, produciendo pleamares más bajas y bajamares más altas.

### Ejemplo 5: Climatología — Clasificación Köppen
```
Clasifica un clima con las siguientes características: T media anual 18°C, T del mes más frío 14°C, T del mes más cálido 28°C, precipitación anual 800 mm, con estación seca en verano.
```
**Respuesta esperada**:
- T del mes más frío >18°C? No (14°C). → No es A.
- T del mes más cálido >10°C? Sí (28°C). → Posible C o D.
- T del mes más frío entre -3°C y 18°C? Sí (14°C). → **Letra principal: C** (templado).
- ¿Estación seca en verano? → **Letra secundaria: s** (Cs).
- Verano cálido (>22°C en el mes más cálido)? Sí (28°C). → **Csa**.
- Clasificación: **Csa — Clima mediterráneo de verano cálido**.

### Ejemplo 6: Meteorología — Vientos y Presión
```
Explica por qué en verano se produce la brisa marina (del mar hacia la tierra).
```
**Respuesta esperada**:
1. **Día de verano**: el Sol calienta la superficie.
2. La **tierra se calienta más rápido** que el mar (menor calor específico del suelo).
3. El aire sobre la tierra se calienta, se expande y se vuelve menos denso → **asciende**.
4. Esto crea una zona de **baja presión** sobre la tierra.
5. Sobre el mar, el aire es más fresco y denso → **alta presión** relativa.
6. El aire fluye de alta a baja presión: de mar → tierra.
7. El aire cálido que asciende sobre tierra es reemplazado por el aire marino → **brisa marina**.
8. Por la noche, el proceso se invierte → **brisa terrestre**.

### Ejemplo 7: Oceanografía — Corrientes y Clima
```
¿Por qué Europa occidental tiene un clima más suave que otras regiones a la misma latitud (ej. Canadá)?
```
**Respuesta esperada**: La **Corriente del Golfo** transporta aguas cálidas tropicales desde el Golfo de México hasta el Atlántico norte. Al llegar a las costas europeas, libera calor a la atmósfera, moderando las temperaturas. Sin esta corriente, ciudades como Londres o Bergen tendrían inviernos mucho más fríos, similares a los de Terranova (canadiense), que está a la misma latitud pero no recibe esta corriente cálida.

## Referencias Cruzadas a Skills STEM Existentes

Este skill hace referencia a los siguientes skills del ecosistema STEM de Mastermind para profundización:

| Skill Referenciado | Ruta | Relación |
|---|---|---|
| `skill-physics-mechanics` | `/hermes-home/skills/skill-physics-mechanics/` | Mecánica de fluidos (presión, corrientes), ondas (sísmicas, marea), termodinámica (gradientes térmicos) |
| `skill-math-foundations` | `/hermes-home/skills/skill-math-foundations/` | Logaritmos (escala de Richter), álgebra (ecuaciones de estado), funciones trigonométricas (ciclos orbitales) |
| `skill-biology-cell` | `/hermes-home/skills/skill-biology-cell/` | Ecosistemas, productividad marina, blanqueamiento de corales, impacto del cambio climático en biodiversidad |
| `skill-chemistry-basics` | `/hermes-home/skills/skill-chemistry-basics/` | Composición del agua de mar, química del CO₂ (acidificación), ciclos biogeoquímicos |
| `skill-scientific-method` | `/hermes-home/skills/skill-scientific-method/` | Diseño de estudios climáticos, análisis de datos meteorológicos |

### Cuándo derivar a otros skills

- Si se necesita **cálculos de presión, ondas o mecánica de fluidos** en contextos geológicos/meteorológicos → derivar a `skill-physics-mechanics`.
- Si se necesita **cálculos logarítmicos** (escala de Richter, pH oceánico) → derivar a `skill-math-foundations`.
- Si se necesita **análisis estadístico de datos climáticos** → derivar a `math-estadistica-probabilidad`.
- Si se necesita **diseñar experimentos o estudios de campo** → derivar a `skill-scientific-method`.

## Pitfalls — Errores Comunes

### Geología
- **Confundir exfoliación con fractura**: la exfoliación (clivaje) sigue planos de debilidad cristalina (superficie plana); la fractura es irregular (ej. concoidea del cuarzo).
- **Confundar textura con composición en rocas ígneas**: la textura (fanerítica/afanítica) indica velocidad de enfriamiento; la composición (ácida/básica) indica contenido de SiO₂. Ambas son independientes.
- **Error en escala de Mohs**: la dureza NO es lineal. El diamante (10) es ~4 veces más duro que el corindón (9), no 10/9 veces.
- **Confundir roca sedimentaria clástica con química**: las clásticas son fragmentos de otras rocas; las químicas son precipitados de minerales disueltos.
- **Error en metamorfismo**: no todas las rocas metamórficas son foliadas. El mármol y la cuarcita son no foliados.
- **Confundir rift con fosa**: el rift es divergente (separación); la fosa es convergente (subducción).

### Meteorología
- **Confundir enfriamiento adiabático con enfriamiento por conducción**: el enfriamiento adiabático es por expansión del aire al ascender (sin intercambio de calor con el entorno).
- **Error en rotación ciclónica**: en el hemisferio norte, los ciclones giran en sentido antihorario; en el hemisferio sur, en sentido horario.
- **Confundir frente cálido con frente frío**: el frente cálido tiene precipitación continua y extensa; el frente frío tiene precipitación intensa y breve.
- **Error en capa de ozono**: el ozono protector está en la estratósfera, NO en la tropósfera (donde es contaminante).
- **Confundir temperatura con calor**: la temperatura es una medida de energía cinética molecular; el calor es la transferencia de energía térmica.

### Oceanografía
- **Error en mareas**: la Luna es el principal causante de las mareas, NO el Sol (aunque el Sol contribuye con ~46% del efecto lunar).
- **Confundir upwelling con downwelling**: el upwelling trae aguas profundas frías y ricas en nutrientes hacia la superficie (alta productividad); el downwelling hunde aguas superficiales.
- **Error en corrientes**: las corrientes cálidas NO son solo "agua caliente"; transportan calor y modifican el clima costero significativamente.
- **Confundir plataforma continental con talud**: la plataforma es la zona poco profunda (<200 m) con pendiente suave; el talud es la pendiente pronunciada que baja a 2,500 m.

### Climatología
- **Confundir factor climático con elemento climático**: los factores modifican el clima (latitud, altitud); los elementos lo describen (temperatura, precipitación).
- **Error en clasificación Köppen**: la letra principal se determina por la T del mes más frío, NO por la T media anual.
- **Confundir efecto invernadero con agujero de ozono**: el efecto invernadero es por GEI (CO₂, CH₄); el agujero de ozono es por CFC que destruyen O₃ estratosférico. Son problemas diferentes.
- **Error en ciclos de Milanković**: la excentricidad (100,000 años) afecta la distancia Sol-Tierra; la oblicuidad (41,000 años) afecta la inclinación axial; la precesión (26,000 años) afecta la orientación del eje.
- **Confundir mitigación con adaptación**: la mitigación reduce emisiones; la adaptación ajusta a los efectos del cambio climático.
- **Error en gradiente térmico**: el gradiente normal es ~6.5°C/km. No confundir con la inversión térmica (temperatura aumenta con la altitud).

## Notas Adicionales

- Este skill es el **pilar de ciencias de la Tierra** del ecosistema STEM de Mastermind.
- En geología, siempre **distinguir entre textura y composición** al clasificar rocas.
- En tectónica de placas, **dar ejemplos reales** de cada tipo de límite (es fundamental para la comprensión).
- En meteorología, recordar que **Coriolis no actúa en el ecuador** (la fuerza es proporcional al seno de la latitud).
- En oceanografía, enfatizar la conexión entre **corrientes y clima** (ej. Corriente del Golfo y Europa).
- En climatología, usar la **clasificación de Köppen como referencia principal**, pero mencionar que existen otras clasificaciones (Thornthwaite, Geiger).
- Para el **cambio climático**, siempre diferenciar entre variabilidad natural y forzamiento antropogénico.
- La **escala de Richter es logarítmica**: un sismo de magnitud 7 libera 32× más energía que uno de magnitud 6, y 1,000× más que uno de magnitud 5.
