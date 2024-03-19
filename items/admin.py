from django.contrib import admin
from .models import Item, Stat, ItemStat

# Define InlineModelAdmin for ItemStat
class ItemStatInline(admin.TabularInline):
    model = ItemStat

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'gold_base', 'gold_total', 'gold_sell']
    filter_horizontal = ['item_from', 'item_into']  # You can add item_from and item_into here
    inlines = [ItemStatInline]  # Add ItemStatInline to the ItemAdmin

@admin.register(ItemStat)
class ItemStatAdmin(admin.ModelAdmin):
    list_display = ['item', 'stat', 'amount']
