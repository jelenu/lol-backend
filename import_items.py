import json
from django.core.files import File
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol.settings')
django.setup()

from builds.models import Item, Stat, ItemStat, Tag  

# Path to the directory where saved images are located
image_directory = "static/item/"

# Read the JSON
with open('item.json', 'r') as f:
    data = json.load(f)

# Create a dictionary to map image names to their full paths
image_paths = {}
for item_id, item_data in data['data'].items():
    image_path = os.path.join(image_directory, f"{item_id}.png")

    if os.path.exists(image_path):
        image_paths[item_id] = image_path

# List to store the ids of already created items
created_item_ids = []

# Iterate over item data and create Item instances
for item_id, item_data in data['data'].items():
    if item_id in created_item_ids:
        print(f"Item with identification '{item_id}' has already been created, skipping creation.")
        continue

    # Check if map 11 is true
    if item_data.get('maps', {}).get('11', False):
        # Check if the image exists in the paths dictionary
        image_path = image_paths.get(item_id)
        if not image_path or not os.path.exists(image_path):
            print(f"The image for the item with identification '{item_id}' does not exist, skipping creation.")
            continue

        # Check if the 'inStore' field is not present or is true
        if 'inStore' not in item_data or item_data['inStore']:
            # Create an instance of Item
            item = Item(
                identification=item_id,
                name=item_data['name'],
                description=item_data['description'],
                colloq=item_data['colloq'],
                plaintext=item_data['plaintext'],
                gold_base=item_data['gold']['base'],
                gold_total=item_data['gold']['total'],
                gold_sell=item_data['gold']['sell'],
                image=image_path
            )

            # Save the id of the created item
            created_item_ids.append(item_id)

            # Save the item in the database
            item.save()
            print(f"Item {item_id} saved")

            # Iterate over the item's statistics
            for stat_name, stat_value in item_data['stats'].items():
                # Find or create the Stat instance
                stat, created = Stat.objects.get_or_create(name=stat_name)
                # Create an instance of ItemStat
                item_stat = ItemStat(
                    item=item,
                    stat=stat,
                    amount=stat_value
                )
                # Save the ItemStat in the database
                item_stat.save()

            # Iterate over the item's tags
            for tag_name in item_data['tags']:
                # Find or create the Tag instance
                tag, created = Tag.objects.get_or_create(name=tag_name)
                # Associate the tag with the current item
                item.tags.add(tag)


        else:
            print(f"The item with identification '{item_id}' will not be saved because 'inStore' is false.")


# Iterate over item data and create the 'from' and 'into' relationships
for item_id, item_data in data['data'].items():
    if item_id in created_item_ids:
        item = Item.objects.get(identification=item_id)
        # Save the 'from' and 'into' data if they exist
        for related_item_id in item_data.get('from', []):
            related_item = Item.objects.filter(identification=related_item_id).first()
            if related_item:
                item.item_from.add(related_item)
            else:
                print(f"The item with identification '{related_item_id}' was not found, skipping the relationship.")

        for related_item_id in item_data.get('into', []):
            related_item = Item.objects.filter(identification=related_item_id).first()
            if related_item:
                item.item_into.add(related_item)
            else:
                print(f"The item with identification '{related_item_id}' was not found, skipping the relationship.")

        # Save changes to the 'from' and 'into' relationships
        item.save()
