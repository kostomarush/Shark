import grpc
import time
from concurrent import futures
import grpc_pb2
import grpc_pb2_grpc

class DataServicer(grpc_pb2_grpc.DataServicer):
    def scanning(self, request, context):
        print(request.state_port)
        return grpc_pb2.DataFromServer(ip = '127.0.0.1', port ='22')


def serv():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    grpc_pb2_grpc.add_DataServicer_to_server(DataServicer(), server)
 
    # запускаемся на порту 6066
    print('Starting server on port 6066.')
    server.add_insecure_port('[::]:6066')
    server.start()
 
    # работаем час или до прерывания с клавиатуры
    try:
        while True:
            None
    except KeyboardInterrupt:
        server.stop(0)
 
 
if __name__ == '__main__':
    serv()