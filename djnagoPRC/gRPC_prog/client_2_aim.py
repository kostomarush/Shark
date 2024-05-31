import grpc
import prot_pb2
import prot_pb2_grpc
import time
import nmap
import threading


def connect(stub: prot_pb2_grpc.RPCStub, name_cl: str):
    response_aim = stub.scan(prot_pb2.DataClient(name_cl=name_cl))
    ip_address = response_aim.ip_address
    port = response_aim.port
    mode = response_aim.mode
    cve_report = response_aim.cve_report
    scan(stub, ip_address, port, mode, cve_report, name_cl)
    stub.scan(prot_pb2.DataClient(name_cl=name_cl, message='Done'))
    


def scan(stub, ip_address, port, mode, cve_report, name_cl):
    host_info = {}
    nm = nmap.PortScanner()
    if mode == 'TCP':
        result = nm.scan(ip_address, ports=port, arguments='-sT', sudo=True)
        if result['scan']:
            host_info['host'] = ip_address
            host_info['tag'] = mode
            host_info['state'] = nm[ip_address].state()
            host_info['ports'] = []
            if 'tcp' in nm[ip_address]:
                host_info['state_ports'] = 'open'
                for port, info in nm[ip_address]['tcp'].items():
                    if cve_report == 'True':
                        cve_information = cve_info(ip_address, port)
                    else:
                        cve_information = 'Empty'
                    port_data = {
                                'port': f'{port}',
                                'state': info['state'],
                                'reason': info['reason'],
                                'service': info['name'],
                                'cve': cve_information
                                }
                    host_info['ports'].append(port_data)
            else:
                host_info['ports'] = 'down'
                print("No open TCP ports found.")

            stub.scan(prot_pb2.DataClient(
                    name_cl=name_cl, data=f'{host_info}'))

        else:
            print('hosts is down')
    
    elif mode == 'UDP':
        result = nm.scan(ip_address, ports=port, arguments='-sU', sudo=True)
        if result['scan']:
            host_info['host'] = ip_address
            host_info['tag'] = mode
            host_info['state'] = nm[ip_address].state()
            host_info['ports'] = []
            if 'udp' in nm[ip_address]:
                host_info['state_ports'] = 'open'
                for port, info in nm[ip_address]['udp'].items():
                    if cve_report == 'True':
                        cve_information = cve_info(ip_address, port)
                    else:
                        cve_information = 'Empty'
                    port_data = {
                                'port': f'{port}',
                                'state': info['state'],
                                'reason': info['reason'],
                                'service': info['name'],
                                'cve': cve_information
                                }
                    host_info['ports'].append(port_data)
            else:
                host_info['ports'] = 'down'
                print("No open TCP ports found.")

            stub.scan(prot_pb2.DataClient(
                    name_cl=name_cl, data=f'{host_info}'))

        else:
            print('hosts is down')

    elif mode == 'OS':
        # Выполняем сканирование
        result = nm.scan(ip_address, arguments='-O', sudo=True)
        if result['scan']:
            host_info['host'] = ip_address
            host_info['tag'] = mode
            host_info['state'] = nm[ip_address].state()
            prob_osmatch = result['scan'][ip_address]['osmatch']
            if prob_osmatch:
                osmatch = result['scan'][ip_address]['osmatch'][0]
                name = osmatch['name']
                host_info[name] = {}
                osclass = osmatch['osclass'][0]
                host_info[name]['vendor'] = osclass.get('vendor', 'N/A')
                host_info[name]['osfamily'] = osclass.get('osfamily', 'N/A')
                host_info[name]['osgen'] = osclass.get('osgen', 'N/A')
                host_info[name]['accuracy'] = osclass.get('accuracy', 'N/A')
            else:
                print('OS None')
            stub.scan(prot_pb2.DataClient(
                name_cl=name_cl, data=f'{host_info}'))  
        else:
            print('hosts is down')
                

            
def cve_info(ip_add_seg, port): 
    nm = nmap.PortScanner()
    result = nm.scan(ip_add_seg, ports=f"{port}", arguments='-sV --script vulscan/ --script-args vulscandb=update_cve.csv')
    cve_inf = result['scan'][ip_add_seg]['tcp'][port]['script']
    if cve_inf:
        all_chunk = cve_inf.get('vulscan', 'Emptys'),
    else:
        all_chunk = 'No'
    
    return all_chunk[0]


        
        

def send_keep_alive_messages(stub, name_cl):
    while True:
        # Отправляем служебное сообщение на сервер
        request = prot_pb2.HelloRequest(message="Ping", name=name_cl)
        stub.SayHello(request)


def run():

    channel = grpc.insecure_channel(
        'localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    name_cl = '5'
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
