
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, ClientBD


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)

    
class RPCServicer(prot_pb2_grpc.RPCServicer):
    def scan(self, request, context):
        data_server = DataServer.objects.all() 
        data_server

        
        response = prot_pb2.DataServer(ip=ip, port=port, mode=mode)
        if request.ip_status != '' or request.vendor != '':
            data_in = ScanInfo(ip_status=request.ip_status, protocols=request.protocols, open_ports=request.open_ports,state=request.state,vendor=request.vendor,os_family=request.os_family,osgen=request.osgen)
            data_in.save() 
        return response