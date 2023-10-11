import prot_pb2
import prot_pb2_grpc
import grpc
from django_grpc_framework.decorators import grpc_method
import threading

class RPCServicer(prot_pb2_grpc.RPCServicer):
    
    def __init__(self, server):
        super(RPCServicer, self).__init__(server)
        self.client_contexts = {}



    @grpc_method
    def your_rpc_method(self, request, context):
        client_id = context.peer()
        self.client_contexts[client_id] = context
        self.start_keepalive_monitor(client_id, context)

        # Ваша реализация метода gRPC

    def start_keepalive_monitor(self, client_id, context):
        # Запускаем монитор активности клиента
        def monitor_activity():
            while not context.is_active():
                pass  # Можно добавить дополнительную логику при отсутствии активности
            self.client_disconnected(client_id)
        
        activity_monitor = threading.Thread(target=monitor_activity)
        activity_monitor.start()

    def client_disconnected(self, client_id):
        # Вызывается, когда клиент отключился
        if client_id in self.client_contexts:
            context = self.client_contexts[client_id]
            context.abort(grpc.StatusCode.DEADLINE_EXCEEDED, "Client Disconnected: Your connection has been closed due to inactivity.")
            del self.client_contexts[client_id]
