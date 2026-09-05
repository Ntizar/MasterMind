---
name: genealogia-espanola
description: Use al investigar apellidos, árboles genealógicos españoles.
version: 1.0.0
author: Mastermind
license: MIT
metadata:
  tags: [genealogia, apellidos, espana, euskadi, historia-familiar]
  related_skills: [research]
---

# Genealogía Española (y Vasca)

## When to Use
- El usuario pide origen/distribución/heráldica de un apellido español, o construir un árbol genealógico / localizar ascendientes en registros parroquiales o civiles.
- Incluye apellidos vascos y ramas caídas en la Guerra Civil.

## Cuándo usar
- Investigar el origen, significado, distribución o heráldica de un apellido español.
- Construir un árbol genealógico de una familia española/vasca (normalmente hasta ~1800 vía registros parroquiales).
- Localizar una rama concreta o ascendientes de un apellido raro.

## Mapa de fuentes (a qué recurso para qué)

### 1) Apellido: distribución y heráldica
- `historiaapellidos.com/apellido/<apellido>.html` — censo nacional, nº de portadores, provincias, blasón.
- `wikiapellidos.com/apellido/<apellido>` — distribución por provincia y concentración.
- `apellidos.net/apellido/<apellido>` — etimología (a menudo especulativa, contrastar).
- Heráldica: confía solo en fuentes que citen al **Cronista y Rey de Armas (Vicente de Cadenas y Vicent)** o en `coatofarmsof.com` para un blasón *documentado*. Las webs comerciales suelen decir "sin blasón documentado" — no es una refutación del escudo español.
- Fuente bibliográfica clave: **"Memorandum de la genealogía familiar" (Vicente de Cadenas y Vicent, 1975)**.

### 2) Registros parroquiales (bautismos/matrimonios/defunciones) — la clave para llegar a 1800
- **Bizkaia: AHEB-BEHA** → `internet.aheb-beha.org/paginas/portada/n_portada.php`. **~2.28 millones de partidas** sacramentales de las parroquias vizcaínas (1501–2019). Es LA base para Bizkaia. App web con JS (bloquea `curl`; usar navegador). Físico: Archivo Histórico Eclesiástico de Bizkaia, Derio.
- **Cantabria: Archivo Diocesano de Santander** (registros parroquiales) y **Archivo Histórico Provincial de Cantabria** (padrones/censos, **Padrón/Censo de Policía de 1824**, **Catastro del Marqués de la Ensenada**).
- **FamilySearch** (`familysearch.org`) — colecciones "España, Vizcaya" y "España, Santander" digitalizadas; **requiere login** para ver registros.
- **Geneanet** (`es.geneanet.org`) — páginas de apellido (distribución + árboles públicos); los árboles suelen requerir login.
- **MyHeritage** — login / prueba de pago.

### 3) ASCAGEN (Cantabria)
- `ascagen.es` — Asociación Cántabra de Genealogía; guían con el padrón de 1824 y el Catastro de Ensenada. Muy útil para apellidos cántabros raros.

### 4) Guerra Civil / ramas vascas y cántabras
- **Euskal Memoria** → `euskalmemoria.eus/es/db/borrokan_hildakoak` — 6.317 fallecidos/as en combate; fichas en `/es/db/borrokan_hildakoak/ikusi/<id>`.
- **Intxorta** → `intxorta.org/izendegia` — lista de víctimas del franquismo en Euskadi ("MUERTO FRENTE", "FUSILADO", etc.), ordenada por apellido.

### 5) Esquelas / obituarios — mejor ancla para la generación reciente
- `esquelas.eldiariomontanes.es` (Diario Montañés), `esquelasdecantabria.com`. Las esquelas dan la **estructura familiar completa** (cónyuge, hijos, hijos políticos, nietos) y el **pueblo** de la familia. Enormemente útiles para anclar el árbol moderno y detectar **apellidos compuestos**.

## Estrategia
1. **Anclar en lo verificable** de la generación reciente (esquela, obituario) antes de ir hacia atrás. El árbol moderno confirma nombres compuestos y pueblo.
2. **Apellido compuesto español** = primer apellido (paterno) + segundo (materno). Hijos de "X Fernández" + "Y Cruz" llevan "X Y". Buscar el compuesto ("A-B") y también el primer apellido por separado.
3. Ir hacia atrás con **registros parroquiales** (AHEB / FamilySearch / Geneanet) para llegar a 1800.
4. Usar las bases de la Guerra Civil para ramas que "desaparecen" o migraron (muchos vascos/cántabros caídos en el frente).

## Trampas (importante)
- **NO inventar el árbol.** La genealogía exige registros reales. Si no se puede acceder (login/archivo físico), declararlo y listar los archivos donde están los registros. Nunca fabricar nombres/fechas.
- **Apellido raro ≠ registros indexados online.** La rareza de un apellido no hace que los registros parroquiales estén en la web; siguen en archivos con login o visita presencial. No asumir "como es raro, llega a 1800".
- **AHEB / FamilySearch / Geneanet son JS-heavy** → bloquean `curl`. Usar el navegador real. Si el harness del navegador pide permiso de depuración de Chrome ("Allow remote debugging"), es un paso que el usuario debe aprobar; pedirlo.
- Para páginas públicas sin JS: descargar con `curl` a un archivo y filtrar con `search_files` (p. ej. listados de víctimas, esquelas).

## Archivos de apoyo
- `references/antizar-case-study.md` — estado de la investigación Antizar / Antizar-Ladislao (anclas verificadas, fuentes, dónde está bloqueada).
