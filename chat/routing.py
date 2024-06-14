from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username1>\w+)_(?P<username2>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
