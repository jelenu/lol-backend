import json
from django.core.files import File
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol.settings')
django.setup()

from items.models import Item, Stat, ItemStat

# Ruta al directorio donde se encuentran las imágenes guardadas
image_directory = "static/item/"

# Lee el JSON
with open('item.json', 'r') as f:
    data = json.load(f)

# Crear un diccionario para mapear los nombres de las imágenes a los paths completos
image_paths = {}
for item_id, item_data in data['data'].items():
    image_path = os.path.join(image_directory, item_data['image']['full'])

    if os.path.exists(image_path):
        image_paths[item_id] = image_path

# Lista para almacenar los identification de los ítems ya creados
created_item_ids = []

# Itera sobre los datos de los items y crea las instancias de Item
for item_id, item_data in data['data'].items():
    if item_id in created_item_ids:
        print(f"Item con identification '{item_id}' ya ha sido creado, omitiendo la creación.")
        continue

    # Verifica si el mapa 11 es verdadero
    if item_data.get('maps', {}).get('11', False):
        # Verifica si la imagen existe en el diccionario de paths
        image_path = image_paths.get(item_id)
        if not image_path or not os.path.exists(image_path):
            print(f"La imagen para el item con identification '{item_id}' no existe, omitiendo la creación.")
            continue

        # Verifica si el campo 'inStore' no está presente o es verdadero
        if 'inStore' not in item_data or item_data['inStore']:
            # Crea una instancia de Item
            item = Item(
                identification=item_id,
                name=item_data['name'],
                description=item_data['description'],
                colloq=item_data['colloq'],
                plaintext=item_data['plaintext'],
                gold_base=item_data['gold']['base'],
                gold_total=item_data['gold']['total'],
                gold_sell=item_data['gold']['sell'],
            )

            with open(image_path, 'rb') as img_file:
                item.image.save(os.path.basename(image_path), File(img_file))

            # Guarda el identification del ítem creado
            created_item_ids.append(item_id)

            # Guarda el item en la base de datos
            item.save()
            print(f"item {item_id} guardado")

            # Itera sobre las estadísticas del item
            for stat_name, stat_value in item_data['stats'].items():
                # Busca o crea la instancia de Stat
                stat, created = Stat.objects.get_or_create(name=stat_name)
                # Crea una instancia de ItemStat
                item_stat = ItemStat(
                    item=item,
                    stat=stat,
                    amount=stat_value
                )
                # Guarda el ItemStat en la base de datos
                item_stat.save()

        else:
            print(f"No se guardará el item con identification '{item_id}' porque 'inStore' es false.")


# Itera sobre los datos de los items y crea las relaciones from e into
for item_id, item_data in data['data'].items():
    if item_id in created_item_ids:
        item = Item.objects.get(identification=item_id)
        # Guarda los datos de "from" e "into" si existen
        for related_item_id in item_data.get('from', []):
            related_item = Item.objects.filter(identification=related_item_id).first()
            if related_item:
                item.item_from.add(related_item)
            else:
                print(f"No se encontró el item con identification '{related_item_id}', omitiendo la relación.")

        for related_item_id in item_data.get('into', []):
            related_item = Item.objects.filter(identification=related_item_id).first()
            if related_item:
                item.item_into.add(related_item)
            else:
                print(f"No se encontró el item con identification '{related_item_id}', omitiendo la relación.")

        # Guarda los cambios en la relación "from" e "into"
        item.save()
