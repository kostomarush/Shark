from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/my_socket/', consumers.GraphConsumer.as_asgi()),
    path('ws/my_socket_2/', consumers.ClientConsumer.as_asgi()),
]
