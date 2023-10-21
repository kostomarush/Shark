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
        result = nm.scan(ip_add_seg, arguments='-sS')
        host_info = {}
        open_ports = 0
        if result:
            for host, scan_result in result['scan'].items():
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['state'] = nm[host].state()
                host_info[host]['open_ports'] = []
                if 'tcp' in nm[host]:
                    host_info[host]['state_ports'] = 'open'
                    for port, info in scan_result['tcp'].items():
                        port_data = {
                            'port': f'{port}',
                            'reason': info['reason'],
                            'service': info['name']
                        }
                        host_info[host]['open_ports'].append(port_data)
                        open_ports += 1
                else:
                    host_info[host]['state_ports'] = 'down'
                    print("No open TCP ports found.")

                print(host_info)
            stub.segment_scan(prot_pb2.DataClientSegment(
                name_cl=name_cl, host=f'{host_info}'))
        else:
            print('hosts is down')

    elif mode_seg == 'UDP':
        result = nm.scan(ip_add_seg, arguments='-sU')
        host_info = {}
        open_ports = 0
        if result:
            for host, scan_result in result['scan'].items():
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['state'] = nm[host].state()
                host_info[host]['open_ports'] = []
                if 'udp' in nm[host]:
                    host_info[host]['state_ports'] = 'open'
                    for port, info in scan_result['udp'].items():
                        port_data = {
                            'port': f'{port}',
                            'reason': info['reason'],
                            'service': info['name']
                        }
                        host_info[host]['open_ports'].append(port_data)
                        open_ports += 1
                else:
                    host_info[host]['state_ports'] = 'down'
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
    name_cl = '1'
    ping_thread = threading.Thread(
        target=send_keep_alive_messages, args=(stub, name_cl))
    ping_thread.daemon = True
    ping_thread.start()

    while True:
        try:  # Запускаем отдельный поток для отправки пингов
            connect(stub, name_cl)
        except:
            pass


if __name__ == "__main__":
    run()
