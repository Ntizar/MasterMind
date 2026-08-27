---
name: ai-work-valuation
version: "1.0.0"
description: "Framework para valorar, posicionar y monetizar trabajo hecho con IA cuando el modelo de negocio tradicional es facturación por horas. Incluye modelos de pricing, análisis comparativo IA vs equipo humano, gestión de incentivos, y técnica de cuantificación de valor via análisis de repos."
tags: [mastermind, monetization, pricing, consulting, ai-strategy, valuation, positioning]
---

# AI Work Valuation — Valorar y monetizar trabajo hecho con IA

## Cuándo se activa

Cuando el usuario habla de:
- Cómo cobrar/preciar trabajo que la IA hace mucho más rápido
- Cómo posicionar soluciones IA frente a clientes que pagan por horas
- El dilema filosófico de "la IA me hace 10x más rápido, ¿cómo no me perjudica?"
- Cómo gestionar incentivos de equipos que usan IA
- Cómo vender conocimiento cuando la IA replica expertise
- "La empresa vende conocimiento y horas"

## El problema central

> **Facturar por horas te penaliza por ser eficiente.** Si la IA te permite hacer en 19 horas lo que un equipo tarda 2 años, cobrar por horas significa ganar menos que la competencia que es más lenta. El modelo de horas recompensa la lentitud.

La solución no es "ser menos eficiente". Es **cambiar lo que vendes**.

## Framework: De "vender tiempo" a "vender juicio"

### Modelo 1 — Facturación por valor, no por tiempo

Si una solución ahorra 50.000€/año a una empresa, no importa si tardaste 5 horas o 500. El valor para el cliente es el mismo.

- Solución que reduce costes operativos 30% → cobras % del ahorro o fee basado en impacto
- Solución que mitiga riesgo regulatorio → cobras por riesgo mitigado
- Solución que acelera proceso crítico → cobras por tiempo ahorrado

**Argumento de venta:** "No te cobro por cuánto trabajo. Te cobro por cuánto te ahorro."

### Modelo 2 — Arbitraje de capacidad

Existe un **spread** entre lo que el cliente espera pagar (precios tradicionales del mercado) y lo que a ti te cuesta producir (IA + juicio).

- **Cobrar precio de mercado y quedarte el margen** → más rentabilidad por proyecto
- **Cobrar menos y comerte el mercado** → más volumen, más clientes, más dominancia
- **La jugada inteligente:** empezar con la primera, moverse a la segunda cuando convenga

### Modelo 3 — Posicionamiento premium, no de "barato"

**Nunca vendas velocidad. Vende calidad.**

- Si dices "soy más rápido" → el cliente oye "más barato" → te devalúa
- Si dices "entrego mejores resultados" → el cliente oye "más valioso" → paga más

La velocidad es tu ventaja operativa, no tu argumento de venta. El cliente no necesita saber que tardaste 3 horas en lo que otros tardan 3 semanas. El cliente necesita saber que tu solución es **mejor que la de la competencia**.

**Argumento correcto:** "Nuestro enfoque nos permite iterar más rápido, probar más hipótesis y refinar más. Por eso el resultado final es superior." La velocidad se vende como **calidad del proceso**, no como eficiencia.

## Cómo trabajarlo concretamente

### Con clientes nuevos

No menciones IA, no menciones horas. Menciona **resultados**:
- "Entregamos X en Y plazo con Z garantía"
- "Trabajamos por objetivos, no por horas"
- "Si no llegamos al resultado, no cobramos" — esto ningún competidor que factura por horas puede ofrecer

Esa garantía la puedes dar **precisamente porque sabes que tu IA + juicio lo va a cumplir**. Tu riesgo es bajísimo. El del competidor es altísimo. Esa asimetría es tu arma.

### Con clientes existentes

La transición es delicada. No quieres que digan "si ahora tardas 5h en vez de 50h, bájame el precio":
- "Estamos evolucionando nuestro modelo. Seguimos entregando el mismo valor, pero ahora con mayor capacidad de iteración y refinamiento."
- Sube el scope, no bajes el precio: "Antes entregábamos un informe. Ahora entregamos informe + dashboard interactivo + monitorización continua."
- El cliente recibe **más valor** por el mismo precio. Tú recibes **más margen** por menos esfuerzo. Ganan ambos.

### Con el equipo

El incentivo tiene que alinearse con el nuevo modelo:
- Si pagas por horas trabajadas → incentivas la lentitud
- Si pagas por **proyectos entregados con calidad** → incentivas eficiencia y buen juicio
- Si pagas por **satisfacción del cliente o impacto** → incentivas lo que de verdad importa

El equipo tiene que entender que su valor ya no es "cuántas horas dedico" sino "qué tan bueno es mi juicio para diseñar y supervisar soluciones".

## Gestión de incentivos

1. **Redefinir el éxito:** el KPI no es "cuántas tareas procesé", sino "cuántos problemas evité", "cuántas oportunidades descubrí"
2. **Liberar humano para lo valioso:** la IA se come el 80% repetitivo, el humano va al 20% que queda — ahí está la diferenciación
3. **Transparencia total:** "la IA está para hacer lo aburrido, no para sustituir tu juicio"
4. **Invertir en lo exclusivamente humano:** relaciones con cliente, pensamiento estratégico, resolución creativa

## Técnica: Cuantificación de valor via análisis de repos

Para argumentar el valor de trabajo IA, cuantifica lo que un equipo humano habría necesitado:

### Pasos

1. **Listar repos relacionados** vía GitHub API (`GET /user/repos?per_page=100`)
2. **Para cada repo, obtener:**
   - Tree completo (`GET /repos/{owner}/{repo}/git/trees/{branch}?recursive=1`)
   - Contar archivos por tipo (.py, .md, .xml, .json, tests)
   - Sumar bytes por tipo → aproximar líneas (bytes / ~35 para Python, / ~45 para Markdown)
   - Commits y fechas (`GET /repos/{owner}/{repo}/commits`)
3. **Identificar conocimiento de dominio requerido:**
   - Estándares implicados (leer DECISIONES.md, README, spec)
   - Complejidad técnica (sistemas de coordenadas, multilingüismo, algoritmos)
   - Contexto específico (normativa, operadores, geografía)
4. **Estimar horas de equipo humano por fase:**
   - Investigación del estándar: 2-3 expertos × 4-6 semanas
   - Escritura de spec: 1-2 personas × 3-4 semanas
   - Desarrollo del validador: 2 devs × 3-4 meses
   - Desarrollo del conversor: 2-3 devs × 3-4 meses
   - Tests e integración: 1-2 testers × 2-3 meses
   - Documentación: 1-2 personas × 2-4 semanas
5. **Calcular valor monetario:**
   - Total horas × tarifa consultoría (80-120€/h)
   - Comparar con tiempo real invertido con IA
6. **Construir la tabla de asimetría:**

| | Equipo tradicional | Tú con IA |
|---|---|---|
| Tiempo | 1.5-2.5 años | X horas |
| Coste | 280K-600K€ | Tu tiempo + IA |
| Conocimiento necesario | 5-10 expertos | Tu juicio + IA |
| Precio de venta | 500K€+ | Lo que decidas |
| Margen | 30-40% | 90%+ |

### Script de referencia

Ver `references/repo-value-analysis.py` — script reutilizable que automatiza el análisis de repos vía GitHub API.

## Modelos de monetización concretos

### Opción A — Producto repetible

El asset se construye una vez, se vende muchas veces. Cada cliente necesita la solución:
- Licencia por cliente: 15.000-50.000€
- Integración + soporte anual: 10.000-30.000€/año
- Personalización: 5.000-15.000€

### Opción B — Proyecto de consultoría

Vendes el proyecto completo a un cliente grande:
- Precio basado en **valor entregado** (cumplimiento normativo, eficiencia), no en horas
- La competencia cobra 500.000€+ y tarda 2 años
- Tú entregas en semanas a 150.000-300.000€

### Opción C — Servicio continuo

- "Mantenimiento y evolución" → 50.000-100.000€/año
- La IA te permite mantener esto con esfuerzo mínimo
- El valor para el cliente es constante

## El límite de la mejora con IA

**Corto plazo (1-3 años):** Automatiza la capa de ejecución del conocimiento repetitivo. Techo = calidad de supervisión y decisión humana.

**Medio plazo (3-5 años):** Agentes hacen reconocimiento de patrones y recomendaciones. Pero el juicio, la relación con cliente, la resolución creativa siguen siendo humanos.

**El límite real:** La IA escala soluciones conocidas a problemas conocidos. El trabajo más valioso es **definir el problema en sí** — requiere entender negocio, personas, cultura. Eso no lo escala nadie.

## La pregunta correcta

> En vez de "¿la IA sustituye a la gente?", pregúntate: **"¿Qué me permite la IA que antes no podía hacer?"**

Proyectos que antes rechazabas por coste — ahora son viables. Clientes que no podías atender por falta de capacidad — ahora puedes. Eso expande fronteras.

**La verdadera competitividad no es "usamos IA para abaratar", es "usamos IA para hacer lo que los competidores no pueden".**

## Referencias

- **Caso de estudio NeTEx-ES:** `references/netex-es-case-study.md` — análisis completo del proyecto NeTEx-ES (5 repos, ~38K líneas Python, 164 tests, 218 reglas validación, 19 horas con IA vs 3.500-5.000h equipo humano)
- **Script de análisis:** `references/repo-value-analysis.py` — automatiza la cuantificación de valor via GitHub API

## Pitfalls

- **NUNCA menciones a un cliente cuánto tiempo tardó la IA:** "Lo hizo la IA en 19 horas" = "esto no vale nada". El cliente necesita saber que tienes la solución, no cómo la construiste.
- **NUNCA vendas velocidad, vende calidad:** "Soy más rápido" = "soy más barato" = devaluación. "Entrego mejores resultados" = "soy más valioso" = premium.
- **NUNCA bajes el precio con clientes existentes:** Sube el scope. Más valor por mismo precio = ganan ambos.
- **NUNCA factures por horas si eres 10x más rápido:** El modelo de horas te penaliza por eficiencia. Cobra por valor, por resultado, por impacto.
- **NUNCA respondas al usuario en un idioma que no sea castellano:** El SOUL.md dice "TODO en castellano". Si el usuario habla español, respondes en español. NUNCA chino, inglés, u otro idioma salvo que el usuario lo pida explícitamente.
- **No asumas que el cliente entiende el valor:** El cliente no sabe que tu solución es única. Tienes que articular el argumento: "esto normalmente tomaría 2 años de un equipo especializado. Nosotros lo entregamos en semanas."
