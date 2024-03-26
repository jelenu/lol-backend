import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lol.settings')
django.setup()

from builds.models import RunePath, RuneSlot

# Load the JSON
with open('runes.json', 'r') as f:
    data = json.load(f)

# Iterate over each fragment of the JSON
for fragment in data:
    # Create a RunePath for each fragment
    rune_path = RunePath.objects.create(
        id=fragment['id'],
        key=fragment['key'],
        icon=fragment['icon'],
        name=fragment['name']
    )

    # Get the slot index
    for index, slot_data in enumerate(fragment['slots']):
        slot_number = index

        # Create a RuneSlot for each rune in the slot
        for rune_data in slot_data['runes']:
            rune_slot = RuneSlot.objects.create(
                id=rune_data['id'],
                key=rune_data['key'],
                icon=rune_data['icon'],
                name=rune_data['name'],
                slot_number=slot_number,
                rune_path=rune_path
            )
