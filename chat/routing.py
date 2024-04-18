from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path("ws/group/<str:group_name>", RoomConsumer.as_asgi())
]