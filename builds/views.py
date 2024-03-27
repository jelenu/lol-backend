from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Tag, Stat, Item, RuneSlot
from .serializers import TagSerializer, StatSerializer, ItemSerializer
from rest_framework import status

class TagStatItemView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        stats = Stat.objects.all()
        items = Item.objects.all()

        tag_serializer = TagSerializer(tags, many=True)
        stat_serializer = StatSerializer(stats, many=True)
        item_serializer = ItemSerializer(items, many=True)

        return Response({
            'tags': tag_serializer.data,
            'stats': stat_serializer.data,
            'items': item_serializer.data
        })
