# INE REST API — Acceso real a datos INE desde servidor

## Descubrimiento

Aunque la web principal de INE (ine.es) bloquea curl/headless, la **API REST antigua SÍ funciona sin autenticación**.

## Endpoint

```
GET https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/{tabla_id}?tip=AM&nult=1
```

- `tip=AM` → Anual, Modalidad
- `nult=1` → Solo el último año
- Sin API key, sin CAPTCHA, sin User-Agent especial

## Tablas conocidas

| Tabla ID | Contenido | Ejemplo |
|----------|-----------|---------|
| 28201 | Salario bruto por CA, sexo, edad | País Vasco: 35.170€ |
| 2852 | Población por provincia y sexo | Madrid: 6.792.723 hab |
| 28200 | Salario bruto por provincia, contrato | Nacional: 29.540€ |

## Formato de respuesta

```json
[
  {
    "Nombre": "Ambos sexos. Todas las edades. Dato base. Salario medio bruto.",
    "MetaData": [...],
    "Data": [{ "Anyo": 2024, "Valor": 34410.01 }]
  }
]
```

## Ejemplo de uso

```python
import urllib.request, json

url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/28201?tip=AM&nult=1"
data = json.loads(urllib.request.urlopen(url).read())

# Filtrar: Ambos sexos + Todas las edades + Salario medio bruto + por CA
for item in data:
    md = {m['T3_Variable']: m['Nombre'] for m in item['MetaData']}
    if (md.get('Sexo') == 'Ambos sexos' and 
        md.get('Totales de edad') == 'Todas las edades' and
        md.get('Conceptos salariales/laborales') == 'Salario medio bruto'):
        ca = md.get('Comunidades y Ciudades Autónomas', '')
        valor = item['Data'][0]['Valor']
        print(f"{ca}: {valor}€")
```

## Pitfalls

1. **Nombres de provincia:** El INE usa formatos oficiales ("Coruña, A" no "A Coruña", "Palmas, Las" no "Las Palmas"). Mapear manualmente.
2. **Sin datos por CP:** El INE NO publica datos a nivel de código postal, solo por municipio/provincia/CA.
3. **Tabla incorrecta:** La tabla 56934 es población, NO renta. Las tablas de salarios están en 28xxx.
4. **Límite de registros:** Algunas tablas tienen miles de registros. Filtrar por variables antes de procesar.
