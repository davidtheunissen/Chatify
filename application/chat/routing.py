from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/group/<group_name>", RoomConsumer.as_asgi())
]