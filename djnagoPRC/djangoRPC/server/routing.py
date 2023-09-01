from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/my_socket/', consumers.GraphConsumer.as_asgi()),
]