from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/my_socket/', consumers.GraphConsumer.as_asgi()),
    path('ws/my_socket_2/', consumers.ClientConsumer.as_asgi()),
    path('ws/my_socket_table/', consumers.TableConsumer.as_asgi()),
    path('ws/my_socket_task/', consumers.TaskConsumer.as_asgi()),
    path('ws/my_socket_add/', consumers.UpdateTable.as_asgi()),
    path('ws/cve_year/', consumers.UpdateCveInformationData.as_asgi()),
    path('ws/my_socket_client_seg/', consumers.ClientSegConsumer.as_asgi()),
    path('ws/table_seg_ipadd/', consumers.SegTableCl.as_asgi()),
    path('ws/table_seg_count/', consumers.TaskSegConsumer.as_asgi()),
    path('ws/table_seg_res/', consumers.UpdateTableSeg.as_asgi()),
]
