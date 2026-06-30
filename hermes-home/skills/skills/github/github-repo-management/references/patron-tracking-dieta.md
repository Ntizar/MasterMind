# Patrón de tracking de dieta y ejercicio

> Hecho con por David Antizar

## Contexto
David quiere llevar un seguimiento diario de su plan de dieta y ejercicio para bajar 10kg en 2 meses. Todo se almacena en el repo privado `Ntizar/dieta`.

## Estructura del repo

### README.md
- Resumen del objetivo, datos personales, enlace a SEGUIMIENTO.md

### SEGUIMIENTO.md
Archivo principal de tracking con las siguientes tablas:

1. **Peso** — Fecha, Hora, Peso (kg), Notas
2. **Pasos diarios** — Fecha, Hora registro, Pasos, Notas
3. **Registro de comidas** — Fecha, Hora, Desayuno, Almuerzo, Comida, Merienda, Cena, Calorías est., Notas
4. **Resumen semanal** — Semana, Peso inicio/fin, Delta, Pasos media, Entrenamientos, Notas

## Flujo de uso

Cuando David escribe "dieta" o menciona datos de seguimiento:

1. **Registrar timestamp** — siempre con fecha y hora exacta
2. **Actualizar SEGUIMIENTO.md** — añadir fila a la tabla correspondiente
3. **Commit + push** — mantener el repo sincronizado
4. **Feedback en chat** — resumen breve con observaciones

## Datos personales (base)
- Altura: 174 cm
- Inicio entrenamiento personal: 2026-06-04
- Objetivo: -10kg en 8 semanas
