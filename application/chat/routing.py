from django.urls import path, re_path
from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>\w+)/$', RoomConsumer.as_asgi())
]