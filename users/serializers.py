from rest_framework import serializers
from .models import LinkedAccount, FollowSummoner

class LinkedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedAccount
        fields = 'game_name', 'tagline', 'server', 'main_server'

class FollowSummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowSummoner
        fields = 'game_name', 'tagline', 'server', 'main_server'

