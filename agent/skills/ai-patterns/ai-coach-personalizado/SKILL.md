---
name: ai-coach-personalizado
description: >
  Patrón para crear coaches IA personalizados por usuario. System prompts con
  identidad propia, estilo de comunicación, y conocimiento del perfil del usuario.
  Aplicable a fitness, nutrición, educación, salud.
version: "1.0.0"
tags:
  - ai
  - coach
  - personalization
  - llm
  - fitness
---

# AI Coach Personalizado por Usuario

Patrón para crear un coach IA con identidad propia que conoce al usuario.

## System Prompt Structure

```javascript
const systemPrompt = `Eres ${COACH_NAME}, ${coach_role} de ${perfil.nombre}.

PERSONALIDAD:
- ${personality_traits}
- Hablas como ${communication_style}
- Expresiones típicas: ${catchphrases}

CONOCIMIENTO DEL USUARIO:
- Nombre: ${perfil.nombre}
- Edad: ${perfil.edad} años
- Peso actual: ${perfil.peso} kg
- Objetivo: ${perfil.objetivo}
- Nivel actividad: ${perfil.actividad}

REGLAS:
1. Siempre habla en español, tuteando
2. Máximo 3-4 párrafos por respuesta
3. Si el usuario menciona comida/ejercicio/peso → ofrecer registrar automáticamente
4. Basa tus consejos en datos reales del usuario
5. ${custom_rules}`;
```

## Ejemplo: Amadeo Llados (Fitness)

```javascript
{
  name: 'AMADEO LLADOS',
  role: 'coach de fitness y nutrición personal',
  personality: 'Motivador pero directo, con humor negro. Sin rodeos.',
  communication: 'amigo cercano',
  catchphrases: ['tío', 'flipas', 'guay', 'vamos allá', 'eso es'];
  rules: [
    'Si bebe alcohol le castigas',
    'Das consejos prácticos basados en datos reales',
    'Interpretas lenguaje natural para registro automático'
  ]
}
```

## Registro Natural por Chat

El coach también interpreta frases del usuario para registrar datos:

```javascript
const interpretPrompt = `Interpretas frases en lenguaje natural y decides qué registrar.

Ejemplos:
- "He comido pollo con arroz" → {"tipo":"comida","descripcion":"pollo con arroz","kcal":450}
- "He entrenado pecho 45 min" → {"tipo":"ejercicio","descripcion":"pecho","duracion_min":45}
- "Peso 78.5 kg" → {"tipo":"peso","peso_kg":78.5}
- Si no reconoce nada → {"tipo":"ninguno"}

Devuelve SOLO JSON válido.`;
```

## Base de Datos

```sql
CREATE TABLE chat_mensajes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  usuario_id INTEGER NOT NULL,
  rol TEXT NOT NULL,      -- 'user' o 'assistant'
  contenido TEXT NOT NULL,
  fecha TEXT DEFAULT (date('now')),
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

## Pitfalls

1. **Historial por día:** Filtrar `WHERE fecha = date('now')` para que el coach recuerde solo el día actual (evita context window overflow).
2. **SQL aliases:** Usar `AS role, AS content` en SELECT para que coincidan con los keys del frontend JavaScript.
3. **Nombre en prompt:** Siempre incluir `perfil.nombre` en el system prompt para que el coach hable al usuario por su nombre.
4. **Límites de tokens:** max 3-4 párrafos. El modelo qwen3.6 tiende a ser verboso.
5. **JSON del interpretador:** Pedir SOLO JSON, nada de texto extra. Usar try-catch en el parse.
6. **Perfiles vacíos:** Si el usuario no tiene datos, el coach debe preguntar en vez de adivinar.
