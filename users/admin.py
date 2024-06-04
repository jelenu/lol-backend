from django.contrib import admin
from .models import LinkedAccount

@admin.register(LinkedAccount)
class LinkedAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_name', 'tagline', 'server', 'main_server', 'verified', 'temp_icon_id')
