
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer
import time


def grpc_hook(server):
    prot_pb2_grpc.add_RPCServicer_to_server(RPCServicer(), server)


class RPCServicer(prot_pb2_grpc.RPCServicer):
    def scan(self, request, context):
        data_server = DataServer.objects.in_bulk()
        response = prot_pb2.DataServer()
        print(response)

        for id in data_server:
            if data_server[id].tag == 'Proc' and f'{data_server[id].client.id}' == request.id_client:
                if request.message == 'End':
                    save_cl = DataServer.objects.get(id=id)
                    save_cl.tag = 'Done'
                    save_cl.save()
                    return response
                large_string = ""
                for req in request:
                    large_string += req.data_chunk
                data_in = ScanInfo(ip_status=request.ip_status,
                                   protocols=request.protocols, open_ports=request.open_ports,
                                   state=request.state, data_chunk=request.data_chunk)

                data_in.save()
                return response
            elif data_server[id].tag == 'False':
                DataServer.objects.filter(id=id).update(
                client=request.id_client, tag='Proc')
                ip = data_server[id].ip
                port = data_server[id].port
                mode = data_server[id].mode
                response_start = prot_pb2.DataServer(
                    ip=ip, port=port, mode=mode)
                return response_start
