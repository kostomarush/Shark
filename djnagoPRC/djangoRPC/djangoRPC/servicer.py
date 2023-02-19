import prot_pb2
import prot_pb2_grpc
from server.models import DataPorts, DataServer


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)

    
class RPCServicer(prot_pb2_grpc.RPCServicer):

    def scan(self, request, context):
        data_out = DataServer.objects.all()
        ip = data_out[0].ip
        port = data_out[0].port
        response = prot_pb2.DataServer(ip=ip, port=port)
        data = request.state
        print(data)
        data_in = DataPorts(data=request.scan_info)
        data_in.save()
        return response