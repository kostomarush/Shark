
import prot_pb2
import prot_pb2_grpc
from server.models import ScanInfo, DataServer, SegmentScan, SegmentResult, IPAddress, ClientBD
from concurrent import futures
import threading
import time
import grpc


class RPCServicer(prot_pb2_grpc.RPCServicer):

    def __init__(self):
        self.text = ''
        self.last_ping_time = time.time()

    def segment_scan(self, request, context):
        data_segment = IPAddress.objects.in_bulk()
        response = prot_pb2.DataSegment()
        for i in data_segment:
            if data_segment[i].tag == 'Proc' and f'{data_segment[i].client}' == request.name_cl:
                if request.message:
                    save_data_seg = IPAddress.objects.get(id=i)
                    save_data_seg.tag = 'Done'
                    save_data_seg.save()
                    return response

                elif request.host:
                    result = IPAddress.objects.get(id=data_segment[i].id)
                    alls_info = request.host
                    all_info = eval(alls_info)
                    for host, info in all_info.items():
                        save_data_in_segment = SegmentResult(host=info['host'], state_scan=info['state'],
                                                             open_ports=info['open_ports'], result=result)
                        save_data_in_segment.save()
                    return response

            elif data_segment[i].tag == 'False':
                IPAddress.objects.filter(id=i).update(
                    client=request.name_cl, tag='Proc')
                ip_address = data_segment[i].address
                mode = data_segment[i].seg_scan.mode
                id_task = data_segment[i].id
                response_start = prot_pb2.DataSegment(
                    ip_address=ip_address, mode=mode)
                return response_start

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

    def SayHello(self, request, context):
        if request.name == "Ping":
            # Обработка сообщения PING
            self.last_ping_time = time.time()
            return prot_pb2.HelloReply(message="Received PING")
        else:
            # Обработка других сообщений
            return prot_pb2.HelloReply(message="Received")


def check_ping_thread(my_service):
    while True:
        if time.time() - my_service.last_ping_time > 30:
            print("Клиент не отправлял PING в течение 30 секунд")
        time.sleep(1)


def grpc_hook(server):
    my_service = RPCServicer()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prot_pb2_grpc.add_RPCServicer_to_server(my_service, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # Создаем и запускаем поток для проверки PING
    ping_check_thread = threading.Thread(
        target=check_ping_thread, args=(my_service,))
    ping_check_thread.start()

    try:
        ping_check_thread.join()
    except KeyboardInterrupt:
        server.stop(0)
