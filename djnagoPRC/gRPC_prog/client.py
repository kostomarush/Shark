import grpc
import prot_pb2, prot_pb2_grpc
import nmap


def scan():
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response = stub.scan(prot_pb2.DataClient(message = 'Hello'))
    nm = nmap.PortScanner()
    ip_address = response.ip
    port = response.port
    #SYN ACK Scan:
    if response.mode == 'SYN':
        nm.scan(ip_address,'1-1024', '-v -sS')
        ip_status = nm[ip_address].state()
        protocols = nm[ip_address].all_protocols()
        open_ports = nm[ip_address]['tcp'].keys()
        for port in open_ports:
            print(nm[ip_address]['tcp'][port]['state'])
            
    #UDP Scan
    if response.mode == 'UDP':
        nm.scan(ip_address, '1-1024', '-v -sU')
        ip_status = nm[ip_address].state()
        protocols = nm[ip_address].all_protocols()
        open_ports = nm[ip_address]['udp'].keys()
        for port in open_ports:
            print(nm[ip_address]['udp'][port]['state'])
    #Comprehensive Scan
    nm.scan(ip_address, '1-1024', '-v -sS -sV -sC -A -O')
    ip_status = nm[ip_address].state()
    protocols = nm[ip_address].all_protocols()
    open_ports = nm[ip_address]['tcp'].keys()
    #OS Detection
    qwe = nm.scan(ip_address, arguments="-O")['scan'][ip_address]['osmatch']
    print(qwe)
    #stub.scan(prot_pb2.DataClient(scan_info = 'scanning'))

if __name__ == "__main__":
    scan()
        