from django.contrib import admin
from .models import LinkedAccount, FollowSummoner, FriendRequest

@admin.register(LinkedAccount)
class LinkedAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_name', 'tagline', 'server', 'main_server', 'verified', 'temp_icon_id')


@admin.register(FollowSummoner)
class FollowSummonerAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_name', 'tagline', 'server')
    

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'accepted')