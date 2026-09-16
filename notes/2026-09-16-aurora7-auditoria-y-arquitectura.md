# Aurora 7 — auditoría campo a campo y la arquitectura que evita que se vuelva a romper

**Fecha:** 2026-09-16
**Repo:** github.com/Ntizar/Aurora7 (local `C:\Users\d_ant\Projects\Aurora-7`)
**Encargo de David:** «entra en el GitHub Aurora 7 y llévalo al siguiente nivel, una auditoría campo a campo; que todos los apartados sean más coherentes con el sistema Aurora; añade muchas más opciones».

---

## 1. Qué encontró la auditoría

El catálogo decía **565 objetos** y el número cuadraba: son clases `.nz-*` declaradas. Pero al cruzar cada objeto contra las demos apareció lo que ningún vistazo a ojo habría pillado:

| Avería | Detalle |
|---|---|
| **24 componentes fantasma** | 5 de las 12 páginas usaban clases de packs que no cargaban (`.nz-switch` en Overlays, `.nz-badge` en Media y Comercio, `.nz-avatar` en Social, `.nz-checkbox` en Sistema). Se veían **sin estilo** en la web pública. |
| **El shell pisaba al sistema** | `p0-catalog.css` declaraba `.nz-btn`, `.nz-btn--primary/--accent/--ghost`, `.nz-eyebrow`, `.nz-fab`… y cada página lo cargaba **después** del pack de la categoría. Resultado: los botones que veías en la categoría 04 **no eran** los de `p4-actions.css`. El catálogo mentía sobre su propio sistema. |
| **3 tokens inexistentes** | `--nz-space-7`, `--nz-space-9`, `--nz-radius-pill` en uso → paddings y radios que no resolvían. |
| **Tres cifras para la misma categoría** | La 01 decía «50 objetos» en su cabecera, `p1-layout.css` declaraba 71 y la portada decía 71. Además la 01 era la única página escrita a mano, así que se desincronizaba sola. |
| **Selector inválido** | `.nz-root :focus-visible--accent` no es una pseudo-clase real: no hacía absolutamente nada. |
| **Deuda menor** | 4 colores a mano, 4 `!important` (uno evitable), `.nz-spin` sin declaración propia. |
| **Y lo gordo para «más opciones»** | **107 familias** de objeto sin una sola variante (`nz-col`, `nz-masonry`, `nz-search`, `nz-table-wrap`, `nz-otp`…). |

**Lección:** una auditoría de design system no se hace mirando. Se hace cruzando el CSS declarado con el uso real, y contando.

## 2. La arquitectura nueva (lo que de verdad aporta valor)

El problema de fondo no era ninguna de las 24 averías: era que **no había forma de saber si el sistema estaba coherente**. Eso ahora es automático:

```
specs/NN.json        → fuente de verdad de las demos (declarativo, editable)
scripts/build-catalog.py → genera páginas + portada + datos/objetos.json + packs/all.css
scripts/audit-catalog.py → auditoría campo a campo → audit/AUDITORIA.md + .json
scripts/audit-html.py    → el informe, contado con el propio Aurora (audit/index.html)
scripts/validar-css.py   → manifiesto + cobertura + propiedad única  ← lo que corre CI
.github/workflows/validar.yml → pone el push en rojo si algo se degrada
```

**Ninguna cifra se escribe a mano.** Portada, cabeceras, pies y el índice del buscador salen de contar el CSS y los specs. Así es imposible que tres sitios digan tres números distintos.

**Reglas que verifica el validador** (y que son portables a cualquier otro design system):

1. **El shell nunca declara componentes.** Si el chrome del catálogo define `.nz-btn`, se carga después y pisa el componente real. El shell solo tiene clases propias (`.cat-*`).
2. **Una clase, un dueño.** Una clase no puede declararse en dos packs. Los ajustes contextuales (`.nz-product .nz-btn`) no cuentan como declaración.
3. **Cobertura total.** Cada clase declarada aparece en una demo. «Si no está en el catálogo, no existe».
4. **Cero colores a mano, cero gradientes, cero glass, cero `!important`** (salvo `.nz-visually-hidden`).

## 3. Pitfalls de medición (costaron dos intentos)

- El regex de CSS (`\.nz-x`) **no ve** las clases del HTML: allí van en `class="nz-x"`. Hay que leer los dos formatos o el censo dice que se usan 2 clases.
- El parser de selectores debe recoger los que viven **dentro de `@media`**. El primer parser solo miraba el nivel superior y se perdía una docena de objetos (y acusaba de fantasma a `.nz-drawer-layout__drawer`, `.nz-holy__nav`, `nz-plans--3`…).

## 4. Lecciones de orquestación

- **NaN aguanta ~5 peticiones simultáneas.** Lancé 7 subagentes: uno murió con **HTTP 429 concurrency limit**. Máximo 4 hijos vivos a la vez; mejor escalonar.
- **Subagentes que escriben archivos muy grandes se truncan** («Response truncated due to output length limit», y tras 4 reintentos, `failed`). Para archivos de más de ~15 KB hay que pedir escritura por trozos (write_file inicial + patches por bloques).
- Lo que sí funcionó muy bien: **repartir por archivos disjuntos** (un subagente = sus packs + sus specs) y dejar que el orquestador haga la integración. Cero colisiones.
- **Darles el léxico cerrado de modificadores** (`--sm`, `--brand`, `--soft`, `--vertical`, `.is-*`) es lo que hace que 15 packs escritos en paralelo hablen el mismo idioma.

## 5. Decisión de doctrina

David eligió **mantener el manifiesto Aurora 7**: sólido, **0 gradientes, 0 glass**, azul `#2563eb` + naranja `#f97316` nunca fundidos. Y ampliación máxima: 15 categorías. Esto confirma lo que ya sabíamos de sesiones anteriores: el look «tech/startup» con glass y mesh no es lo que quiere para sus catálogos y webs.

**No confundir repos:** `Ntizar-Aurora` (v5/v6, liquid glass, packs opt-in) ≠ `Ntizar/Aurora7` (v7, sólido, 15 categorías, specs + CI). El skill `aurora-design-system` ya lo recoge.

---

Hecho con ❤️ por David Antizar
