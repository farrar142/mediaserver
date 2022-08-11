# chat/routing.py
from django.urls import re_path, path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/test/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
