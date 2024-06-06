from rest_framework import serializers
from .models import LinkedAccount, FollowSummoner, FriendRequest

class LinkedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedAccount
        fields = 'game_name', 'tagline', 'server', 'main_server'
        read_only_fields = 'game_name', 'tagline', 'server', 'main_server'

class FollowSummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowSummoner
        fields = 'game_name', 'tagline', 'server', 'main_server'
        read_only_fields = 'game_name', 'tagline', 'server', 'main_server'

class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username', read_only=True)
    receiver = serializers.CharField(source='receiver.username', read_only=True)
    class Meta:
        model = FriendRequest
        fields = 'sender', 'receiver', 'accepted'
        read_only_fields = 'sender', 'receiver', 'accepted'
