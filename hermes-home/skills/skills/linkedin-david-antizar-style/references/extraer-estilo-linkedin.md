# Extraer estilo de escritura de export de LinkedIn

## Procedimiento

### Paso 1: Localizar archivos del export

El export de LinkedIn de David Antizar (2026-06-05) contiene:
- **29 CSVs** — perfil, posiciones, skills, endorsements, certificaciones, etc.
- **4 HTMLs** — artículos publicados en LinkedIn (2020-2022)

Los archivos están en el workspace del usuario. Buscar con:
```bash
find /root/workspace -name "*.csv" -o -name "*.html" | grep -i linkedin
```

### Paso 2: Leer los CSVs clave

CSVs más importantes para el perfil:
- `Profile.csv` — nombre, headline, summary, web
- `Positions.csv` — experiencia laboral (título, empresa, descripción, fechas)
- `Skills.csv` — skills listadas
- `Endorsement_Received_Info.csv` — skills con más endorsements
- `Certifications.csv` — certificaciones recientes
- `Education.csv` — formación
- `Publications.csv` — libros, artículos
- `Company_Follows.csv` — empresas que sigue (intereses)

### Paso 3: Leer los HTMLs (artículos)

Cada HTML contiene un artículo publicado en LinkedIn. Extraer:
```python
import re
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = text.strip()
```

### Paso 4: Analizar el estilo

Métricas clave a extraer:
- **Longitud de párrafos** — media, max, min (en caracteres)
- **Frases cortas** — count de frases <80 chars
- **Emojis** — count total (David: 0 en 4 artículos)
- **Números/datos** — count de menciones numéricas
- **Citas** — frases entre comillas
- **Hashtags** — count y tipo (#tema vs #general)
- **Estructura** — gancho → contexto → datos → análisis → conclusión

### Paso 5: Extraer patrones de escritura

Buscar:
- Frases típicas (repetitivas, fórmulas)
- Tono (formal, informal, técnico, directo)
- Opinión vs neutralidad
- Uso de primera persona
- Estructura de argumentos

### Paso 6: Generar skill

Crear `SKILL.md` con:
- Perfil real del usuario (datos extraídos)
- Principios del estilo (tono, estructura, formato)
- Lo que NO hace
- Frases típicas
- Pitfalls

### Paso 7: Actualizar user.md

Guardar datos estructurados del usuario en `/hermes-home/user.md`:
- Identidad
- Experiencia profesional
- Educación
- Skills principales
- Certificaciones
- Proyectos
- Intereses
- Estilo de escritura

## Ejemplo de análisis (David Antizar)

```
Artículo: World Energy Outlook 2022
Párrafos: 23
Longitud media: 130 chars
Frases cortas (<80 chars): 12
Números mencionados: 19
Emojis: 0
Citas: 0

Estructura:
1. Gancho: "Como cada año, la AIE ha sacado su WEO."
2. Contexto: "Este año ha sido movidito..."
3. Datos: precios gas, inversión 500B USD
4. Análisis: 3 escenarios (STEPS, APS, NZE)
5. Conclusión: "Sin duda la energía ha sido el gran negocio del siglo XX..."
```
