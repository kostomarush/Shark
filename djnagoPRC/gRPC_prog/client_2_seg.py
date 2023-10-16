import grpc
import prot_pb2
import prot_pb2_grpc
import time
import nmap
import threading


def connect(stub: prot_pb2_grpc.RPCStub, name_cl: str):
    response_segment = stub.segment_scan(
        prot_pb2.DataClientSegment(name_cl=name_cl))
    ip_add_seg = response_segment.ip_address
    mode_seg = response_segment.mode
    segment_scan(stub, ip_add_seg, mode_seg, name_cl)
    stub.segment_scan(prot_pb2.DataClientSegment(
        name_cl=name_cl, message='Done'))


def segment_scan(stub, ip_add_seg, mode_seg, name_cl):
    nm = nmap.PortScanner()
    if mode_seg == 'SYN':
        nm.scan(ip_add_seg, arguments='-sV')
        all_hosts = nm.all_hosts()
        host_info = {}
        if all_hosts:
            for host in all_hosts:
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['state'] = nm[host].state()
                if 'tcp' in nm[host]:
                    host_info[host]['open_ports'] = list(
                        nm[host]['tcp'].keys())
                else:
                    host_info[host]['open_ports'] = 'down'
                    print("No open TCP ports found.")

                print(host_info)
            stub.segment_scan(prot_pb2.DataClientSegment(
                name_cl=name_cl, host=f'{host_info}'))
        else:
            print('hosts is down')


def send_keep_alive_messages(stub, name_cl):
    while True:
        # Отправляем служебное сообщение на сервер
        request = prot_pb2.HelloRequest(message="Ping", name=name_cl)
        stub.SayHello(request)


def run():

    channel = grpc.insecure_channel(
        'localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    name_cl = '2'
    ping_thread = threading.Thread(
        target=send_keep_alive_messages, args=(stub, name_cl))
    ping_thread.daemon = True
    ping_thread.start()
    try:
        while True:  # Запускаем отдельный поток для отправки пингов
            connect(stub, name_cl)
    except:
        pass


if __name__ == "__main__":
    run()
