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


def segment_scan(stub, ip_add_seg, mode_seg, name_cl):
    nm = nmap.PortScanner()
    if mode_seg == 'SYN':
        nm.scan(ip_add_seg, arguments='-sV')
        for host in nm.all_hosts():
            Host = host
            State = nm[host].state()
            if 'tcp' in nm[host]:
                Open_ports = list(nm[host]['tcp'].keys())
                print(Open_ports)
            else:
                print("No open TCP ports found.")

            stub.segment_scan(prot_pb2.DataClientSegment(
                name_cl=name_cl, host=Host, state=State, open_ports=f'{Open_ports}'))

    stub.segment_scan(prot_pb2.DataClientSegment(
        name_cl=name_cl, message='Done'))


def send_keep_alive_messages(stub):
    while True:
        # Отправляем служебное сообщение на сервер
        request = prot_pb2.HelloRequest(name="Ping")
        stub.SayHello(request)
        time.sleep(30)  # Отправляем сообщение каждые 10 секунд


def run():

    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    name_cl = '2'
    ping_thread = threading.Thread(
        target=send_keep_alive_messages, args=(stub,))
    ping_thread.daemon = True
    ping_thread.start()
    # Запускаем отдельный поток для отправки пингов
    while True:
        connect(stub, name_cl)


if __name__ == "__main__":
    run()
