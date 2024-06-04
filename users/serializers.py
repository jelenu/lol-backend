from rest_framework import serializers
from .models import LinkedAccount

class LinkedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedAccount
        fields = 'game_name', 'tagline', 'server', 'main_server'
