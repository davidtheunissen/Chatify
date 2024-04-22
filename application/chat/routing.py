from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/room/<str:room_name>", RoomConsumer.as_asgi())
]