import json

with open('data/database.json', 'r') as f:
    db = json.load(f)

new_meals = [
    {'fecha': '2026-06-10', 'hora': '22:30', 'descripcion': 'Volldamm (caña)', 'kcal': 200, 'proteinas_g': 0, 'hidratos_g': 8, 'grasas_g': 0, 'notas': 'Volldamm caña'},
    {'fecha': '2026-06-10', 'hora': '22:45', 'descripcion': 'Ensaladita de salmón ahumado con queso fresco y mozzarella', 'kcal': 250, 'proteinas_g': 18, 'hidratos_g': 4, 'grasas_g': 18, 'notas': 'Salmón ahumado + queso fresco + mozzarella'}
]

db['comidas'].extend(new_meals)

with open('data/database.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

today = [m for m in db['comidas'] if m['fecha'] == '2026-06-10']
t = {'kcal': sum(m['kcal'] for m in today), 'p': sum(m['proteinas_g'] for m in today), 'h': sum(m['hidratos_g'] for m in today), 'g': sum(m['grasas_g'] for m in today)}
print(f'✅ {len(new_meals)} comidas añadidas')
print(f'Total hoy: {t["kcal"]} kcal | P:{t["p"]}g H:{t["h"]}g G:{t["g"]}g')
print(f'Comidas hoy: {len(today)}')
