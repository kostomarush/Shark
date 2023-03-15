
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, ClientBD


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)

    
class RPCServicer(prot_pb2_grpc.RPCServicer):
    def scan(self, request, context):
        data_server = DataServer.objects.in_bulk()
        for id in data_server:
            if (data_server[id].tag != 'Done') and (data_server[id].client == None or data_server[id].client.ip_client == request.id_client or request.message == f'{data_server[id].client.id}'):
                if request.message != '':
                    DataServer.objects.filter(id = id).update(client = request.message,
                    tag = 'Processing')
                ip = data_server[id].ip
                port = data_server[id].port
                mode = data_server[id].mode
                response = prot_pb2.DataServer(ip=ip, port=port, mode=mode)
                if request.ip_status != '' or request.vendor != '':
                    data_in = ScanInfo(ip_status=request.ip_status, 
                    protocols=request.protocols, open_ports=request.open_ports,
                    state=request.state,vendor=request.vendor,os_family=request.os_family,
                    osgen=request.osgen)
                    DataServer.objects.filter(id = id).update(tag = 'Done')
                    data_in.save() 
                return response