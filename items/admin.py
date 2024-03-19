from django.contrib import admin
from .models import Item, Stat, ItemStat, Tag

# Define InlineModelAdmin for ItemStat
class ItemStatInline(admin.TabularInline):
    model = ItemStat

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'gold_base', 'gold_total', 'gold_sell']
    filter_horizontal = ['item_from', 'item_into']
    inlines = [ItemStatInline]

@admin.register(ItemStat)
class ItemStatAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'stat_name', 'amount']

    def item_name(self, obj):
        return obj.item.name

    def stat_name(self, obj):
        return obj.stat.name

    item_name.short_description = 'Item'
    stat_name.short_description = 'Stat'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']