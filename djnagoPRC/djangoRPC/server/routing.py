from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/my_socket/', consumers.GraphConsumer.as_asgi()),
    path('ws/my_socket_2/', consumers.ClientConsumer.as_asgi()),
    path('ws/my_socket_table/', consumers.TableConsumer.as_asgi()),
    path('ws/my_socket_task/', consumers.TaskConsumer.as_asgi()),
    path('ws/my_socket_add/', consumers.UpdateTable.as_asgi()),
    # path('ws/my_socket_cve_level/', consumers.LevelCve.as_asgi())
]
