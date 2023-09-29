import grpc
import prot_pb2
import prot_pb2_grpc
import nmap


def connect():
    id_cl = '2'
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response_segment = stub.segment_scan(prot_pb2.DataClientSegment(name_cl = id_cl))
    ip_add_seg = response_segment.ip_address
    mode_seg = response_segment.mode

    segment_scan(stub, ip_add_seg, mode_seg, id_cl)


def segment_scan(stub, ip_add_seg, mode_seg, id_cl):
    nm = nmap.PortScanner()
    if mode_seg == 'SYN':
        nm.scan(ip_add_seg, arguments='-sV', sudo='True')
        for host in nm.all_hosts():
            Host = host
            State = nm[host].state()
            if 'tcp' in nm[host]:
                Open_ports = list(nm[host]['tcp'].keys())
            else:
                print("No open TCP ports found.")
    
        stub.segment_scan(prot_pb2.DataClientSegment(name_cl=id_cl, host=Host, state=State, open_ports=f'{Open_ports}'))
            
    else:
        pass
    
    stub.scan(prot_pb2.DataClientSegment(name_cl=id_cl, message='Compleate'))

if __name__ == "__main__":
    connect()
