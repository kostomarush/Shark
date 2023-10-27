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
    cve_report = response_segment.cve_report
    full_scan = response_segment.full_scan
    segment_scan(stub, ip_add_seg, mode_seg, name_cl, cve_report)
    stub.segment_scan(prot_pb2.DataClientSegment(
        name_cl=name_cl, message='Done'))
    
# def generate_chunk(chunks):
#     for data in chunks:
#         yield prot_pb2.DataChunk(data_chunk=data)


def segment_scan(stub, ip_add_seg, mode_seg, name_cl, cve_report):
    nm = nmap.PortScanner()
    host_info = {}
    if mode_seg == 'TCP':
        result = nm.scan(ip_add_seg, arguments='-sT')
        open_ports = 0
        if result['scan']:
            for host, scan_result in result['scan'].items():
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['tag'] = mode_seg
                host_info[host]['state'] = nm[host].state()
                host_info[host]['open_ports'] = []
                if 'tcp' in nm[host]:
                    host_info[host]['state_ports'] = 'open'
                    for port, info in scan_result['tcp'].items():
                        if cve_report == 'True':
                            cve_information = cve_info(host, port)
                        else:
                            cve_information = 'Empty'
                        port_data = {
                            'port': f'{port}',
                            'reason': info['reason'],
                            'service': info['name'],
                            'cve': cve_information
                        }
                        host_info[host]['open_ports'].append(port_data)
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
        open_ports = 0
        if result:
            for host, scan_result in result['scan'].items():
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['tag'] = mode_seg
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

    elif mode_seg == 'OS':
        # Выполняем сканирование
        result = nm.scan(ip_add_seg, arguments='-O')
        if result['scan']:
            for host, scan_result in result['scan'].items():
                host_info[host] = {}
                host_info[host]['host'] = host
                host_info[host]['tag'] = mode_seg
                host_info[host]['state'] = nm[host].state()
                prob_osmatch = scan_result['osmatch']
                if prob_osmatch:
                    osmatch = scan_result['osmatch'][0]
                    name = osmatch['name']
                    host_info[host][name] = {}
                    osclass = osmatch['osclass'][0]
                    host_info[host][name]['vendor'] = osclass.get('vendor', 'N/A')
                    host_info[host][name]['osfamily'] = osclass.get('osfamily', 'N/A')
                    host_info[host][name]['osgen'] = osclass.get('osgen', 'N/A')
                    host_info[host][name]['accuracy'] = osclass.get('accuracy', 'N/A')
                else:
                    print('OS None')
            stub.segment_scan(prot_pb2.DataClientSegment(
                name_cl=name_cl, host=f'{host_info}'))  
        else:
            print('hosts is down')

def cve_info(ip_add_seg, port): 
    nm = nmap.PortScanner()
    result = nm.scan(ip_add_seg, ports=f"{port}", arguments='-sV --script vulscan/ --script-args vulscandb=update_cve.csv')
    if result['scan']:
        cve_inf = result['scan'][ip_add_seg]['tcp'][port]['script']
        if cve_inf:
            all_chunk = cve_inf.get('vulscan', ''),
        else:
            all_chunk = 'No'
        
        return all_chunk[0]
    
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
