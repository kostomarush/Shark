import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)

    
class RPCServicer(prot_pb2_grpc.RPCServicer):

    def scan(self, request, context):
        #data_out = DataServer.objects.all()
        #ip = data_out[0].ip
        #port = data_out[0].port
        response = prot_pb2.DataServer(ip='127.0.0.1', port='1-1024', mode="SYN")
        if request.ip_status != '' or request.vendor != '':
            data_in = ScanInfo(ip_status=request.ip_status, protocols=request.protocols, open_ports=request.open_ports,state=request.state,vendor=request.vendor,os_family=request.os_family,osgen=request.osgen)
            data_in.save() 
        return response