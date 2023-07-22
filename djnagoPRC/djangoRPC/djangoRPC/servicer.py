
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, ClientBD
from asgiref.sync import sync_to_async
from server.consumers import GraphConsumer



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
                # Обновление данных для графика
                #chart_data = sync_to_async(GraphConsumer.get_date())
                
                # Передача обновленных данных для графика всем подключенным клиентам через WebSockets
                #channel_layer = get_channel_layer()
                #async_to_sync(channel_layer.group_send)('chart_group', {
                #    'type': 'send_chart_data',
                #    'chart_data': chart_data,
                #})
                
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
                