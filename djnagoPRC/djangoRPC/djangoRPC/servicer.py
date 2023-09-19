
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer
import time


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)


class RPCServicer(prot_pb2_grpc.RPCServicer):

    def __init__(self):
        self.text = ''

    def scan(self, request, context):
        data_server = DataServer.objects.in_bulk()
        response = prot_pb2.DataServer()

        for data_id in data_server:
            if data_server[data_id].tag == 'Proc' and f'{data_server[data_id].client.id}' == request.id_client:
                if request.message == 'End':
                    save_cl = DataServer.objects.get(id=data_id)
                    save_cl.tag = 'Done'
                    save_cl.save()
                    return response
                data_in = ScanInfo.objects.all().delete()
                data_in = ScanInfo(ip_status=request.ip_status,
                                   protocols=request.protocols, open_ports=request.open_ports,
                                   state=request.state, data_chunk=self.text)

                data_in.save()
                return response
            elif data_server[data_id].tag == 'False':
                DataServer.objects.filter(id=data_id).update(
                client=request.id_client, tag='Proc')
                ip = data_server[data_id].ip
                port = data_server[data_id].port
                mode = data_server[data_id].mode
                response_start = prot_pb2.DataServer(
                    ip=ip, port=port, mode=mode)
                return response_start

    def chunk(self, request, context):
        for req in request:
            self.text += req.data_chunk
        return prot_pb2.Empty(result='done')