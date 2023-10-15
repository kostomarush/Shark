import prot_pb2, prot_pb2_grpc
from prot_pb2_grpc import RPCServicer
import time
import threading


def check_ping_thread(my_service):
    while True:
        if time.time() - my_service.last_ping_time > 30:
            print("Клиент не отправлял PING в течение 30 секунд")
        time.sleep(1)

def grpc_hook(server):
    my_service = RPCServicer()
    prot_pb2_grpc.add_RPCServicer_to_server(my_service, server)

    # Создаем и запускаем поток для проверки PING
    ping_check_thread = threading.Thread(
        target=check_ping_thread, args=(my_service,))
    ping_check_thread.start()

    try:
        ping_check_thread.join()
    except KeyboardInterrupt:
        server.stop(0)