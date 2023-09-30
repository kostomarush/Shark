import grpc
import prot_pb2
import prot_pb2_grpc
import nmap


def connect():
    name_cl = '3'
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
        except:
            pass


def segment_scan(stub, ip_add_seg, mode_seg, name_cl):
    nm = nmap.PortScanner()
    if mode_seg == 'SYN':
        nm.scan(ip_add_seg, arguments='-sV')
        for host in nm.all_hosts():
            Host = host
            State = nm[host].state()
            if 'tcp' in nm[host]:
                Open_ports = list(nm[host]['tcp'].keys())
            else:
                print("No open TCP ports found.")

            stub.segment_scan(prot_pb2.DataClientSegment(
                name_cl=name_cl, host=Host, state=State, open_ports=f'{Open_ports}'))

    stub.segment_scan(prot_pb2.DataClientSegment(
        name_cl=name_cl, message='Done'))


if __name__ == "__main__":
    connect()
