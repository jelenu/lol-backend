from rest_framework import serializers
from .models import Tag, Stat, Item, ItemStat

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = '__all__'

class ItemStatSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()

    class Meta:
        model = ItemStat
        fields = ('stat', 'amount')

class ItemSerializer(serializers.ModelSerializer):
    stats = ItemStatSerializer(source='itemstat_set', many=True, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'