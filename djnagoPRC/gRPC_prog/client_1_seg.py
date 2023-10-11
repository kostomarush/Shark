import grpc
import prot_pb2
import prot_pb2_grpc
import nmap

    
def connect():
    name_cl = '1'
    channel = grpc.insecure_channel(
        'localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    while True:
        try:
            response_segment = stub.segment_scan(
                prot_pb2.DataClientSegment(name_cl=name_cl))
            ip_add_seg = response_segment.ip_address
            mode_seg = response_segment.mode

            segment_scan(stub, ip_add_seg, mode_seg, name_cl)
            stub.segment_scan(prot_pb2.DataClientSegment(
        name_cl=name_cl, message='Done'))
        except:
            pass


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
                    host_info[host]['open_ports'] = list(nm[host]['tcp'].keys())
                else:
                    host_info[host]['open_ports'] = 'down'
                    print("No open TCP ports found.")
                
                print(host_info)
            stub.segment_scan(prot_pb2.DataClientSegment(
                    name_cl=name_cl, host=f'{host_info}'))
        else:
            print('hosts is down')


if __name__ == "__main__":
    connect()
