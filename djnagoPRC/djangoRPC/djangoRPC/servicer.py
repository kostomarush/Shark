
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, ClientBD



def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)

    
class RPCServicer(prot_pb2_grpc.RPCServicer):
    def scan(self, request, context):
        data_server = DataServer.objects.in_bulk()
        response = prot_pb2.DataServer()
        for id in data_server:
            if data_server[id].tag == 'Processing' and f'{data_server[id].client.id}' == request.id_client:
                if request.message == 'End':
                    DataServer.objects.filter(id = id).update(tag = 'Done')
                    return response
                data_in = ScanInfo(ip_status=request.ip_status, 
                protocols=request.protocols, open_ports=request.open_ports,
                state=request.state,vendor=request.vendor,os_family=request.os_family,
                osgen=request.osgen)
                data_in.save()
                channel_layer = get_channel_layer()
                
                # if request.message == 'End':
                #     DataServer.objects.filter(id = id).update(tag = 'Done')
                return response

            elif data_server[id].tag == 'False':
                DataServer.objects.filter(id = id).update(client = request.id_client, tag = 'Processing')
                ip = data_server[id].ip
                port = data_server[id].port
                mode = data_server[id].mode
                response_start = prot_pb2.DataServer(ip=ip, port=port, mode=mode)
                return response_start
            